"""
===============================================================================
QHDALabs — RTANA v1
Relational Temporal Awareness in Neural Architectures

Autor / Author  : Krzysztof Banasiewicz
GitHub          : https://github.com/QHDALabs/QHDALabs-RTANA

===============================================================================
KLUCZOWA ZASADA / KEY PRINCIPLE
===============================================================================

PL:
  System nie tylko zapisuje historię — żyje w swojej historii.
  S(t) wpływa na generację E(t), nie tylko ją rejestruje.

  Stary model (pasywny):
    sv → event → S.history.append(event)

  RTANA (aktywny):
    S(t) → influences quantum circuit → E(t) → S(t+1)

  Implementacja tej zasady:
    - h(t) moduluje fazy PW (φ) przez projekcję na przestrzeń faz
    - historia mostów H(t) perturbuje J Hamiltoniana
    - każdy nowy event jest funkcją całej przeszłości systemu

EN:
  The system does not merely record history — it lives in its history.
  S(t) influences event generation E(t), not just records it.

  Old model (passive):
    sv → event → S.history.append(event)

  RTANA (active):
    S(t) → influences quantum circuit → E(t) → S(t+1)

  Implementation of this principle:
    - h(t) modulates PW phases (φ) via projection onto phase space
    - bridge history H(t) perturbs Hamiltonian J
    - each new event is a function of the system's entire past

===============================================================================
ARCHITEKTURA / ARCHITECTURE
===============================================================================

  S(t) = ( h(t), τ(t), H(t) )
    h(t)  ∈ ℝ^d      — wektor stanu ukrytego / hidden state vector
    τ(t)  ∈ ℕ        — licznik kroków relacyjnych / relational step counter
    H(t)  = historia eventów / event history

  E(t) = ( m(t), p(t), φ(t) )
    m(t)  ∈ {0,1}    — wynik pomiaru Born / Born measurement outcome
    p(t)  ∈ [0,1]    — P(m=1) przed pomiarem / P(m=1) before measurement
    φ(t)  ∈ ℝ^n      — fazy PW modulowane przez h(t) / PW phases modulated by h(t)

  E(t) = G( sv(t), S(t) )       ← kluczowe: E zależy od S
  S(t+1) = F( S(t), E(t) )      ← stan aktualizowany przez event

===============================================================================
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

import numpy as np
import torch
import torch.nn as nn
from scipy.linalg import expm
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

try:
    from qiskit_aer import AerSimulator
    _HAS_AER = True
except ImportError:
    _HAS_AER = False


# ============================================================
# KONFIGURACJA / CONFIGURATION
# ============================================================

D_HIDDEN    : int   = 64     # wymiar stanu ukrytego / hidden state dim
D_PHASE     : int   = 5      # liczba faz PW = N_sys / number of PW phases = N_sys
N_CLOCK     : int   = 4      # 2^4 = 16 kroków / steps
N_QUBITS    : int   = 5      # kubitów w sieci / qubits in network
T_DEPTH     : int   = 2      # głębokość scramblera / scrambler depth
RULE_QUBIT  : int   = 1      # qubit obserwatora / observer qubit
BRIDGE_PAIR : Tuple[int,int] = (0, 4)
W_QUBIT     : int   = 0
W_OP        : str   = "z"
J_BASE      : float = 1.0    # bazowe sprzężenie Isinga / base Ising coupling
DELTA_J     : float = 0.025  # perturbacja J na most / J perturbation per bridge
GRAPH_EDGES : List[Tuple[int,int]] = [(0,1),(0,2),(0,3),(0,4)]
PHASE_SCALE : float = 0.1    # skala modulacji faz przez h(t) / phase modulation scale
MIX_SCALE   : float = 0.35   # faza PW -> obrót bazy pomiaru / PW phase -> measurement basis rotation
READOUT_FLOOR: float = 0.12  # minimalna niepewność odczytu / minimum readout uncertainty


# ============================================================
# SEKCJA 1: STRUKTURY DANYCH / DATA STRUCTURES
# ============================================================

@dataclass
class RelationalEvent:
    """
    PL: Jeden fakt relacyjny — wynik interakcji systemu z obserwatorem.
        Nieodwracalny po zapisaniu. Zawiera:
        - wynik pomiaru (fakt)
        - niepewność przed pomiarem (informacja kwantowa)
        - fazy PW modulowane przez historię (kontekst fizyczny)

    EN: One relational fact — result of system-observer interaction.
        Irreversible once recorded. Contains:
        - measurement outcome (fact)
        - pre-measurement uncertainty (quantum information)
        - PW phases modulated by history (physical context)
    """
    step        : int
    outcome     : int           # m ∈ {0,1}
    prob_one    : float         # P(m=1) przed pomiarem / before measurement
    pw_phases   : List[float]   # fazy PW / PW phases
    bridge_fired: bool          # czy most odpalił / whether bridge fired
    j_at_step   : float         # J Hamiltoniana w tym kroku / J at this step

    def to_tensor(self) -> torch.Tensor:
        """
        PL: Konwertuje event do tensora dla PyTorch.
            Format: [m, p, φ_0, ..., φ_{n-1}]
            Wymiar: 2 + D_PHASE
        EN: Converts event to tensor for PyTorch.
            Format: [m, p, φ_0, ..., φ_{n-1}]
            Dimension: 2 + D_PHASE
        """
        values = [float(self.outcome), self.prob_one] + self.pw_phases
        return torch.tensor(values, dtype=torch.float32)


@dataclass
class RelationalState:
    """
    PL: Stan systemu S(t) = (h(t), τ(t), H(t)).
        To jest "pamięć trajektorii" — nie tylko ostatni event,
        ale cała historia faktów relacyjnych.

    EN: System state S(t) = (h(t), τ(t), H(t)).
        This is "trajectory memory" — not just the last event,
        but the full history of relational facts.
    """
    h      : torch.Tensor                          # wektor stanu / state vector
    tau    : int = 0                               # licznik kroków / step counter
    history: List[RelationalEvent] = field(default_factory=list)

    @property
    def n_bridges(self) -> int:
        """Liczba odpalonych mostów w historii / Number of bridges fired."""
        return sum(e.bridge_fired for e in self.history)

    @property
    def effective_j(self) -> float:
        """
        PL: J efektywne = J_BASE + perturbacje z historii mostów.
            Każdy most (m=1) perturbuje J o ±DELTA_J.
            System "żyje w historii" — przeszłość zmienia fizykę.
        EN: Effective J = J_BASE + perturbations from bridge history.
            Each bridge (m=1) perturbs J by ±DELTA_J.
            System "lives in history" — the past changes physics.
        """
        j = J_BASE
        for i, e in enumerate(self.history):
            if e.bridge_fired:
                delta = DELTA_J if i % 2 == 0 else -DELTA_J * 0.6
                j = max(0.05, min(4.0, j + delta))
        return j

    @property
    def h_numpy(self) -> np.ndarray:
        """Tensor → numpy dla Qiskit / Tensor to numpy for Qiskit."""
        return self.h.detach().numpy()

    def timeline_entropy(self) -> float:
        """Entropia Shannona osi czasu / Shannon entropy of timeline."""
        n = len(self.history)
        if n == 0:
            return 0.0
        p1 = sum(e.outcome for e in self.history) / n
        p0 = 1.0 - p1
        if p0 <= 0.0 or p1 <= 0.0:
            return 0.0
        return float(-p0 * np.log2(p0) - p1 * np.log2(p1))


# ============================================================
# SEKCJA 2: SILNIK PAGE-WOOTTERSA (z modulacją przez h(t))
# SECTION 2: PAGE-WOOTTERS ENGINE (with h(t) modulation)
# ============================================================

class PageWoottersEngine:
    """
    PL: Silnik PW z modulacją faz przez stan ukryty h(t).

        KLUCZOWA ZMIANA względem RQTE:
        fazy φ(t) nie zależą tylko od kroku t,
        ale też od h(t) — stanu ukrytego systemu.

        φ_modulated(t) = φ_pw(t) + PHASE_SCALE · W_proj · h(t)

        gdzie W_proj ∈ ℝ^{N_sys × d} to nauczalna projekcja.
        W v1: W_proj jest losowo inicjalizowany i zamrożony.
        W v2: W_proj jest trenowany — system uczy się jak
              jego historia wpływa na fizykę.

    EN: PW engine with phase modulation by hidden state h(t).

        KEY CHANGE from RQTE:
        phases φ(t) depend not only on step t,
        but also on h(t) — the system's hidden state.

        φ_modulated(t) = φ_pw(t) + PHASE_SCALE · W_proj · h(t)

        where W_proj ∈ ℝ^{N_sys × d} is a learnable projection.
        In v1: W_proj is randomly initialized and frozen.
        In v2: W_proj is trained — the system learns how
               its history influences physics.
    """

    def __init__(self, N_clock: int, N_sys: int, J: float = J_BASE) -> None:
        self.N_clock = N_clock
        self.N_sys   = N_sys
        self.T       = 2 ** N_clock
        self.J       = J

        # Projekcja h(t) → modulacja faz / Projection h(t) → phase modulation
        # v1: zamrożona losowa projekcja / v1: frozen random projection
        torch.manual_seed(42)
        self.W_proj = torch.randn(N_sys, D_HIDDEN) * 0.01
        self.W_proj.requires_grad_(False)   # zamrożona w v1 / frozen in v1

        self._build(J)

    def _build(self, J: float) -> None:
        """Buduje history state dla danego J / Builds history state for given J."""
        self.J = J
        Z      = np.array([[1,0],[0,-1]], dtype=complex)
        I2     = np.eye(2, dtype=complex)
        dim    = 2 ** self.N_sys
        H      = np.zeros((dim, dim), dtype=complex)

        for i in range(1, self.N_sys):
            ops    = [I2] * self.N_sys
            ops[0] = Z
            ops[i] = Z
            term   = ops[0]
            for op in ops[1:]:
                term = np.kron(term, op)
            H += J * term

        dim_s  = 2 ** self.N_sys
        psi0   = np.ones(dim_s, dtype=complex) / np.sqrt(dim_s)
        history = np.zeros(self.T * dim_s, dtype=complex)

        for t in range(self.T):
            U_t       = expm(-1j * H * t)
            psi_t     = U_t @ psi0
            clock_t   = np.zeros(self.T, dtype=complex)
            clock_t[t] = 1.0
            history  += np.kron(clock_t, psi_t)

        self._history = history / np.sqrt(self.T)

    def phases_at(self, t: int, h: torch.Tensor) -> List[float]:
        """
        PL: Fazy relacyjne dla kroku t, modulowane przez h(t).
            φ_base    = arg(amplitudy |ψ_t⟩)
            φ_mod     = PHASE_SCALE · (W_proj · h)
            φ_final   = φ_base + φ_mod

            To jest implementacja zasady "system żyje w historii":
            stan ukryty h(t) — który zawiera całą historię eventów —
            bezpośrednio moduluje fizykę kwantową następnego kroku.

        EN: Relational phases for step t, modulated by h(t).
            φ_base    = arg(amplitudes of |ψ_t⟩)
            φ_mod     = PHASE_SCALE · (W_proj · h)
            φ_final   = φ_base + φ_mod

            This implements "system lives in history":
            hidden state h(t) — which encodes full event history —
            directly modulates the quantum physics of the next step.
        """
        dim_s  = 2 ** self.N_sys
        vec    = self._history.reshape(self.T, dim_s)
        vec_t  = vec[t % self.T, :].copy()
        norm   = float(np.linalg.norm(vec_t))
        if norm < 1e-12:
            vec_t    = np.zeros(dim_s, dtype=complex)
            vec_t[0] = 1.0
        else:
            vec_t /= norm

        # Fazy bazowe z PW / Base PW phases
        phi_base = [float(np.angle(vec_t[q % dim_s])) for q in range(self.N_sys)]

        # Modulacja przez h(t) / Modulation by h(t)
        with torch.no_grad():
            phi_mod = (self.W_proj @ h).tolist()

        phi_final = [
            phi_base[q] + PHASE_SCALE * phi_mod[q]
            for q in range(self.N_sys)
        ]
        return phi_final

    def update_j(self, new_j: float) -> None:
        """Przebuduj PW z nowym J / Rebuild PW with new J."""
        self._build(new_j)


# ============================================================
# SEKCJA 3: KWANTOWA GENERACJA EVENTU G(sv, S(t))
# SECTION 3: QUANTUM EVENT GENERATION G(sv, S(t))
# ============================================================

def _brickwork_edges(n: int, parity: int) -> List[Tuple[int,int]]:
    start = parity % 2
    return [(i, i+1) for i in range(start, n-1, 2)]

def _prob_one(sv: Statevector, qubit: int) -> float:
    data = sv.data
    return float(np.clip(
        sum(abs(data[i])**2 for i in range(len(data)) if (i >> qubit) & 1),
        0.0, 1.0
    ))

def _collapse(sv: Statevector, qubit: int, outcome: int) -> Statevector:
    data = np.array(sv.data, dtype=complex)
    for i in range(len(data)):
        if ((i >> qubit) & 1) != outcome:
            data[i] = 0.0
    norm = float(np.linalg.norm(data))
    if norm < 1e-12:
        data    = np.zeros(len(data), dtype=complex)
        data[0] = 1.0
    else:
        data /= norm
    return Statevector(data)

def _build_scrambler(n: int, T: int) -> QuantumCircuit:
    qc = QuantumCircuit(n)
    for step in range(T):
        for i in range(n):
            qc.h(i)
        for u, v in _brickwork_edges(n, step):
            qc.cz(u, v)
    return qc

def _build_scrambler_inv(n: int, T: int) -> QuantumCircuit:
    qc = QuantumCircuit(n)
    for step in reversed(range(T)):
        for u, v in reversed(_brickwork_edges(n, step)):
            qc.cz(u, v)
        for i in range(n):
            qc.h(i)
    return qc


def generate_event(
    sv     : Statevector,
    state  : RelationalState,
    pw     : PageWoottersEngine,
    step   : int,
    rng    : np.random.Generator,
) -> Tuple[Statevector, RelationalEvent]:
    """
    PL: G(sv, S(t)) → (sv_new, E(t))

        To jest rdzeń zasady "system żyje w historii":
        1. pw.phases_at(step, state.h) — fazy modulowane przez h(t)
        2. state.effective_j           — J perturbowane przez historię mostów
        3. pw.update_j(effective_j)    — Hamiltonian zmieniony przez przeszłość

        Każdy nowy event jest wynikiem całej historii systemu.
        Bez historii — inne fazy, inny J, inne p(m=1).

    EN: G(sv, S(t)) → (sv_new, E(t))

        This is the core of "system lives in history":
        1. pw.phases_at(step, state.h) — phases modulated by h(t)
        2. state.effective_j           — J perturbed by bridge history
        3. pw.update_j(effective_j)    — Hamiltonian changed by past

        Each new event is the result of the system's entire history.
        Without history — different phases, different J, different p(m=1).
    """
    i, j = BRIDGE_PAIR

    # 1. Aktualizuj J Hamiltoniana z historii / Update J from bridge history
    eff_j = state.effective_j
    if abs(eff_j - pw.J) > 1e-6:
        pw.update_j(eff_j)

    # 2. Fazy PW modulowane przez h(t) / PW phases modulated by h(t)
    phases = pw.phases_at(step, state.h)

    # 3. Scramble
    sv = sv.evolve(_build_scrambler(N_QUBITS, T_DEPTH))

    # 4. Tik PW przed pomiarem / PW tick before measurement
    #
    # RZ przechowuje fazę relacyjną, ale sama faza nie zmienia
    # prawdopodobieństw w bazie Z. Dodatkowy RY miesza fazę z bazą
    # pomiaru, więc h(t) i J(t) realnie wpływają na następny fakt E(t).
    qc_tick = QuantumCircuit(N_QUBITS)
    for q in range(N_QUBITS):
        phi = phases[q % len(phases)]
        qc_tick.rz(2.0 * phi, q)
        qc_tick.ry(MIX_SCALE * np.sin(phi + eff_j + 0.17 * step), q)
    sv = sv.evolve(qc_tick)

    # 5. Perturbacja W / Perturbation W
    qc_w = QuantumCircuit(N_QUBITS)
    if W_OP == "z":
        qc_w.z(W_QUBIT)
    elif W_OP == "x":
        qc_w.x(W_QUBIT)
    elif W_OP == "y":
        qc_w.y(W_QUBIT)
    sv = sv.evolve(qc_w)

    # 6. Pomiar rule_qubit / Measure rule_qubit
    p_born = _prob_one(sv, RULE_QUBIT)
    p1 = READOUT_FLOOR + (1.0 - 2.0 * READOUT_FLOOR) * p_born
    m  = int(rng.random() < p1)
    sv = _collapse(sv, RULE_QUBIT, m)

    # 7. Most warunkowy / Conditional bridge
    bridge_fired = (m == 1)
    if bridge_fired:
        qc_br = QuantumCircuit(N_QUBITS)
        qc_br.cz(i, j)
        sv = sv.evolve(qc_br)

    # 8. Unscramble
    sv = sv.evolve(_build_scrambler_inv(N_QUBITS, T_DEPTH))

    event = RelationalEvent(
        step        = step,
        outcome     = m,
        prob_one    = p1,
        pw_phases   = phases,
        bridge_fired= bridge_fired,
        j_at_step   = eff_j,
    )
    return sv, event


# ============================================================
# SEKCJA 4: RELACYJNY GRU — FUNKCJA AKTUALIZACJI F(S(t), E(t))
# SECTION 4: RELATIONAL GRU — UPDATE FUNCTION F(S(t), E(t))
# ============================================================

class RelationalGRU(nn.Module):
    """
    PL: Funkcja aktualizacji stanu F(S(t), E(t)) → h(t+1).

        GRU z eventami relacyjnymi jako wejściem.
        Wejście: [m(t), p(t), φ_0,...,φ_{N-1}]  wymiar: 2 + D_PHASE
        Stan:    h(t) ∈ ℝ^{D_HIDDEN}

        Bramki GRU są analogiem selektywnej uwagi na historię:
        - reset gate (r): ile poprzedniego stanu "pamiętamy"
        - update gate (z): jak mocno event zmienia stan
        Bez bramek każdy event nadpisuje stan — brak pamięci trajektorii.

    EN: State update function F(S(t), E(t)) → h(t+1).

        GRU with relational events as input.
        Input: [m(t), p(t), φ_0,...,φ_{N-1}]  dim: 2 + D_PHASE
        State: h(t) ∈ ℝ^{D_HIDDEN}

        GRU gates are the analog of selective history attention:
        - reset gate (r): how much of previous state we "remember"
        - update gate (z): how strongly event changes state
        Without gates each event overwrites state — no trajectory memory.
    """

    def __init__(self, d_hidden: int = D_HIDDEN, d_event: int = 2 + D_PHASE) -> None:
        super().__init__()
        self.d_hidden = d_hidden
        self.d_event  = d_event
        d_in = d_hidden + d_event

        # Bramki GRU / GRU gates
        self.W_r = nn.Linear(d_in, d_hidden, bias=True)   # reset
        self.W_z = nn.Linear(d_in, d_hidden, bias=True)   # update
        self.W_h = nn.Linear(d_in, d_hidden, bias=True)   # candidate

        # Głowa predykcji kroku τ / Step prediction head (metryka 1)
        self.step_head = nn.Linear(d_hidden, 2 ** N_CLOCK)

        # Głowa predykcji trajektorii / Trajectory prediction head (metryka 2)
        self.traj_head = nn.Linear(d_hidden, 2)

        self._init_weights()

    def _init_weights(self) -> None:
        for module in self.modules():
            if isinstance(module, nn.Linear):
                nn.init.xavier_uniform_(module.weight)
                if module.bias is not None:
                    nn.init.zeros_(module.bias)

    def forward(self, h: torch.Tensor, e: torch.Tensor) -> torch.Tensor:
        """
        PL: Jeden krok GRU.
            h: [D_HIDDEN]   stan poprzedni / previous state
            e: [d_event]    event tensor / event tensor
            → h_new: [D_HIDDEN]

        EN: One GRU step.
        """
        x  = torch.cat([h, e], dim=-1)
        r  = torch.sigmoid(self.W_r(x))
        z  = torch.sigmoid(self.W_z(x))
        x_r = torch.cat([r * h, e], dim=-1)
        h_candidate = torch.tanh(self.W_h(x_r))
        h_new = (1.0 - z) * h + z * h_candidate
        return h_new

    def predict_step(self, h: torch.Tensor) -> torch.Tensor:
        """Metryka 1: predykcja kroku τ / Step prediction."""
        return self.step_head(h)

    def predict_trajectory(self, h: torch.Tensor) -> torch.Tensor:
        """Metryka 2: predykcja trajektorii / Trajectory prediction."""
        return self.traj_head(h)


# ============================================================
# SEKCJA 5: PĘTLA RTANA
# SECTION 5: RTANA LOOP
# ============================================================

def rtana_run(
    n_steps    : int = 2 ** N_CLOCK,
    gru        : Optional[RelationalGRU] = None,
    seed       : Optional[int] = None,
    verbose    : bool = True,
) -> Tuple[RelationalState, List[RelationalEvent]]:
    """
    PL: Pełna pętla RTANA: N_steps kroków relacyjnych.

        W każdym kroku:
          1. G(sv, S(t)) → E(t)    [Qiskit: event zależy od S(t)]
          2. F(S(t), E(t)) → h(t+1) [PyTorch: stan aktualizowany]
          3. S(t+1) = (h(t+1), τ+1, H∪{E(t)})

        System żyje w historii:
          - h(t) moduluje fazy PW dla E(t)
          - historia mostów perturbuje J dla E(t)
          - każdy nowy event jest funkcją całej przeszłości

    EN: Full RTANA loop: N_steps relational steps.

        Each step:
          1. G(sv, S(t)) → E(t)    [Qiskit: event depends on S(t)]
          2. F(S(t), E(t)) → h(t+1) [PyTorch: state updated]
          3. S(t+1) = (h(t+1), τ+1, H∪{E(t)})

        System lives in history:
          - h(t) modulates PW phases for E(t)
          - bridge history perturbs J for E(t)
          - each new event is a function of the entire past
    """
    rng = np.random.default_rng(seed)

    if gru is None:
        gru = RelationalGRU()
        gru.eval()

    pw = PageWoottersEngine(N_CLOCK, N_QUBITS, J=J_BASE)

    # Stan startowy / Initial state
    state = RelationalState(h=torch.zeros(D_HIDDEN))

    # Stan kwantowy startowy = stan grafowy / Initial quantum state = graph state
    qc_init = QuantumCircuit(N_QUBITS)
    for i in range(N_QUBITS):
        qc_init.h(i)
    for u, v in GRAPH_EDGES:
        qc_init.cz(u, v)
    sv = Statevector.from_instruction(qc_init)

    if verbose:
        print(f"\n{'='*70}")
        print(f"  RTANA v1 — Relational loop  ({n_steps} steps)")
        print(f"  D_HIDDEN={D_HIDDEN} | N_CLOCK={N_CLOCK} | bridge={BRIDGE_PAIR}")
        print(f"{'='*70}")
        print(f"{'step':>5} | {'m':>3} | {'p(m=1)':>7} | {'bridge':>7} | "
              f"{'J_eff':>6} | {'||h||':>7} | {'τ':>4}")
        print(f"{'-'*70}")

    with torch.no_grad():
        for step in range(n_steps):

            # G(sv, S(t)) — event zależy od S(t) / event depends on S(t)
            sv, event = generate_event(sv, state, pw, step, rng)

            # F(S(t), E(t)) — aktualizuj stan / update state
            e_tensor = event.to_tensor()
            h_new    = gru(state.h, e_tensor)

            # S(t+1)
            state = RelationalState(
                h       = h_new,
                tau     = state.tau + 1,
                history = state.history + [event],
            )

            if verbose:
                h_norm = float(state.h.norm())
                print(
                    f"{step:>5} | {event.outcome:>3} | {event.prob_one:>7.4f} | "
                    f"{'YES' if event.bridge_fired else 'no':>7} | "
                    f"{event.j_at_step:>6.4f} | {h_norm:>7.4f} | {state.tau:>4}"
                )

    return state, state.history


# ============================================================
# SEKCJA 6: METRYKI / METRICS
# ============================================================

def metric_timeline_entropy(history: List[RelationalEvent]) -> float:
    """
    PL: Metryka 3 — entropia Shannona osi czasu.
        H ≈ 1.0 bit → dobra losowość.
        H < 0.9 → historia wpływa na pomiary (jak BUTTERFLY w RQTE).
    EN: Metric 3 — Shannon entropy of timeline.
    """
    n = len(history)
    if n == 0:
        return 0.0
    p1 = sum(e.outcome for e in history) / n
    p0 = 1.0 - p1
    if p0 <= 0.0 or p1 <= 0.0:
        return 0.0
    return float(-p0 * np.log2(p0) - p1 * np.log2(p1))


def metric_j_drift(history: List[RelationalEvent]) -> float:
    """
    PL: Drift J Hamiltoniana przez cała historię.
        Mierzy jak mocno historia mostów zmieniła fizykę.
        Wartość 0.0 → brak historii lub brak mostów.
    EN: J Hamiltonian drift across full history.
        Measures how strongly bridge history changed physics.
    """
    if not history:
        return 0.0
    j_start = history[0].j_at_step
    j_end   = history[-1].j_at_step
    return abs(j_end - j_start)


def metric_h_evolution(history_h: List[torch.Tensor]) -> float:
    """
    PL: Średnia zmiana normy h(t) między krokami.
        Mierzy jak aktywnie stan ukryty się zmienia.
        Niska wartość → stan stagnuje (brak uczenia się historii).
    EN: Mean change in h(t) norm between steps.
        Measures how actively the hidden state changes.
    """
    if len(history_h) < 2:
        return 0.0
    diffs = [
        float((history_h[i+1] - history_h[i]).norm())
        for i in range(len(history_h)-1)
    ]
    return float(np.mean(diffs))


def run_metrics(
    state  : RelationalState,
    history: List[RelationalEvent],
    gru    : RelationalGRU,
) -> dict:
    """PL: Oblicz wszystkie metryki / EN: Compute all metrics."""
    entropy   = metric_timeline_entropy(history)
    j_drift   = metric_j_drift(history)
    n_bridges = sum(e.bridge_fired for e in history)

    # Metryka 1: relacyjny licznik kroku / relational step counter.
    # Głowa step_head istnieje jako szkic pod trening, ale w v1 nie jest
    # trenowana, więc nie raportujemy jej jako sensownej predykcji.
    step_pred = state.tau % (2 ** N_CLOCK)
    step_true = state.tau % (2 ** N_CLOCK)
    step_ok   = (step_pred == step_true)

    return {
        "timeline_entropy" : round(entropy, 4),
        "j_drift"          : round(j_drift, 4),
        "n_bridges"        : n_bridges,
        "n_steps"          : len(history),
        "step_pred"        : step_pred,
        "step_true"        : step_true,
        "step_pred_ok"     : step_ok,
        "step_source"      : "relational_counter",
        "h_norm_final"     : round(float(state.h.norm()), 4),
    }


# ============================================================
# SEKCJA 7: DEMO I ENTRY POINT
# SECTION 7: DEMO AND ENTRY POINT
# ============================================================

def demo_single_run() -> None:
    """PL: Demo jednego przebiegu RTANA. EN: Demo of single RTANA run."""
    gru   = RelationalGRU()
    state, history = rtana_run(gru=gru, verbose=True)

    print(f"\n{'='*70}")
    print("  METRYKI / METRICS")
    print(f"{'='*70}")
    metrics = run_metrics(state, history, gru)
    for k, v in metrics.items():
        print(f"  {k:25s}: {v}")


def demo_history_sensitivity() -> None:
    """
    PL: Sprawdza czy dwa przebiegi z różnymi seedami (różna historia)
        dają różne stany końcowe h(T).
        To jest wstępny test metryki 2 (history sensitivity).
        Jeśli ||h1 - h2|| > 0 → historia ma wpływ na stan.

    EN: Checks if two runs with different seeds (different history)
        produce different final states h(T).
        Preliminary test of metric 2 (history sensitivity).
        If ||h1 - h2|| > 0 → history influences state.
    """
    print(f"\n{'='*70}")
    print("  HISTORY SENSITIVITY TEST")
    print(f"{'='*70}")

    gru = RelationalGRU()
    gru.eval()

    state1, hist1 = rtana_run(gru=gru, seed=42,  verbose=False)
    state2, hist2 = rtana_run(gru=gru, seed=123, verbose=False)

    diff = float((state1.h - state2.h).norm())

    print(f"  Run 1 — timeline: {''.join(str(e.outcome) for e in hist1)}")
    print(f"  Run 2 — timeline: {''.join(str(e.outcome) for e in hist2)}")
    print(f"  ||h1 - h2||: {diff:.6f}")
    print(f"  Entropy run 1: {metric_timeline_entropy(hist1):.4f}")
    print(f"  Entropy run 2: {metric_timeline_entropy(hist2):.4f}")
    print(f"  J drift run 1: {metric_j_drift(hist1):.4f}")
    print(f"  J drift run 2: {metric_j_drift(hist2):.4f}")

    if diff > 1e-4:
        print(f"\n  ✓ Różne historie → różne stany / Different histories → different states")
        print(f"    System żyje w historii. / System lives in its history.")
    else:
        print(f"\n  ✗ Stany identyczne — brak wrażliwości na historię.")
        print(f"    Sprawdź PHASE_SCALE i DELTA_J.")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("  RTANA v1 — Relational Temporal Awareness in Neural Architectures")
    print("  QHDALabs | Krzysztof Banasiewicz | https://krzyshtof.com")
    print("="*70)

    print("\nTryby / Modes:")
    print("  1 — Single run demo")
    print("  2 — History sensitivity test")

    choice = input("\n> ").strip()

    if choice == "1":
        demo_single_run()
    elif choice == "2":
        demo_history_sensitivity()
    else:
        print("Uruchamiam oba / Running both...")
        demo_single_run()
        demo_history_sensitivity()

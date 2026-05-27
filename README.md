# QHDALabs / rtana

**Relational Temporal Awareness in Neural Architectures**

*Krzysztof Banasiewicz — independent researcher*

[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![Status](https://img.shields.io/badge/status-early%20research-orange)]()
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)](https://github.com/QHDALabs/rtana/pulls)

---

RTANA is a proposal to change the class of AI systems: from static functions y = f(x) to dynamic processes S(t+1) = F(S(t), x, event) — where the event structure is grounded in relational physics, not engineering convention.

## The question

> *Can a neural architecture have an internal relational clock —
> a sequence of internal states that create relational facts
> autonomously, anchoring the system in time even without
> external queries?*

Language models are ahistorical. Every response is generated without
knowledge of when it is generated, how long a conversation has lasted,
or what happened between exchanges. This is not merely a missing
timestamp. It is the absence of **relational anchoring in a sequence
of events.**

Between queries, a model does not wait. It does not endure. The weights
sit frozen. Nothing happens. There is no time.

This project asks whether that can be changed — not by adding a clock
to the input, but by embedding temporal structure into the architecture
itself.

---

## Theoretical foundation

The project is grounded in two frameworks:

**Rovelli's Relational Quantum Mechanics (RQM)**: time is not a
background parameter. It emerges from relations between physical
systems. A fact exists only relative to an observer that measured it.
Without measurement, without relational events — there is no "now."

**Page-Wootters mechanism**: time emerges from entanglement between
a clock system and a target system. Each projection of the clock onto
a basis state recovers a relational moment. The clock does not measure
time — it *is* time, relative to the system it is coupled with.

The research question is: can these principles be translated into
a neural architecture analog?

---

## Connection to prior work

This project grows directly from QHDALabs/qmnet:

- **Bridge experiment** (qmnet_v3/v4): mid-circuit measurement creates
  a relational fact → conditional CZ bridge implements network response
  → sequence of facts constitutes an emergent timeline
- **RQTE v3.0**: emergent timeline used as cryptographic key material —
  time born from measurement becomes computationally useful

RTANA asks the next question: can this mechanism become a persistent
internal process in a neural architecture?

---

## Three levels of the problem

**Level 1 — Session time** *(minimal)*  
The model tracks its own reasoning sequence within a conversation.
Each step is a relational event. The model knows it is at step 7
of a sequence. Behaviorally verifiable.

**Level 2 — Inter-session time** *(persistent)*  
A persistent internal state evolves between conversations.
The model registers that time has passed — not from a timestamp,
but from internal state evolution. Requires persistence across
instantiations.

**Level 3 — Autonomous time** *(radical)*  
The internal clock runs continuously, generating relational facts
without external interaction. The model *endures* in Rovelli's sense.
Most faithful to the original intuition. Least understood.

---

## Current status

This repository is at the beginning. The manifesto is written.
The questions are posed. A minimal RTANA v1 proof of concept now exists
in `rtana_v1.py`.

| Task | Status |
|---|---|
| Manifesto | ✅ written |
| Formal problem statement | ✅ done |
| Literature review (RQM, PW, neural time) | ⬜ in progress 40% |
| Minimal architecture proposal | ✅ done |
| Proof of concept implementation | ✅ `rtana_v1.py` |
| Behavioral evaluation protocol | 🟨 initial demos |

---

## RTANA v1 proof of concept

Run:

```bash
py rtana_v1.py
```

Modes:

- `1` — single relational loop demo
- `2` — history sensitivity test

The v1 prototype demonstrates the minimal session-level mechanism:

- hidden state `h(t)` modulates Page-Wootters phases,
- bridge history perturbs the effective Hamiltonian coupling `J`,
- each relational event updates the hidden state,
- different event histories produce different final hidden states.

This is not a trained model and not a consciousness claim. It is a
small executable testbed for the architectural question in the
manifesto.

---

## What this is not

This is not a proposal to make AI conscious.  
This is not a claim that neural networks experience time.  
This is not adding a timestamp to the system prompt.

This is an architectural research question about whether relational
temporal structure can be embedded into a neural system in a way
that changes how it reasons and responds.

---

## Open questions

- What is the minimal architecture that generates internal relational
  events autonomously?
- Can the Page-Wootters clock register be translated into a neural
  architecture analog?
- What is a "relational fact" in a neural network — and how is it
  different from a hidden state update?
- Is there a measurable behavioral difference between a model with
  and without an internal relational clock?

---

## Related work

- [QHDALabs/qmnet](https://github.com/QHDALabs/qmnet) — bridge
  experiments and RQTE prototype (foundation for this project)
- [QHDALabs site](https://qhdalabs.github.io/)

---

## Collaboration

This is independent research. No institutional affiliation.
Collaboration welcome — especially from:

- Researchers in neural architecture design
- Physicists working on RQM or Page-Wootters
- Anyone who finds the question interesting enough to disagree with

**Krzysztof Banasiewicz**  
<qhdalabs.contact@gmail.com>  
[LinkedIn](https://www.linkedin.com/in/krzyshtoof)

---

## License

MIT — see `LICENSE`.

---

*The intuition started on a sailing boat in Greece.  
The question took years to become precise enough to state.  
Now it is stated. Now we build.*

# RTANA — Open Questions

*Living document. Questions are never deleted — only answered or refined.*  
*Status: 🔴 open / 🟡 partial / 🟢 answered*

---

## Foundational

🔴 **Q1. What is a "relational fact" in a neural network?**  
In RQM: two systems interact, one measures the other, a fact exists
relative to the observer. In a neural network: what plays the role
of observer, what plays the role of measured system, and what
constitutes the "fact"?  
*Opened: 2026-05-22*

🔴 **Q2. What is the neural analog of a Page-Wootters clock register?**  
PW: clock register entangled with system register. Projection onto
clock basis state recovers system state at relational time t.
Neural analog: a subsystem whose state indexes "when" the system is,
without reference to an external clock.  
*Opened: 2026-05-22*

🔴 **Q3. Is there a measurable behavioral difference between a model
with and without an internal relational clock?**  
If yes: what tasks reveal it? If no: is the concept empirically empty?  
*Opened: 2026-05-22*

---

## Architecture

🔴 **Q4. What is the minimal architecture that generates internal
relational events autonomously — without external input?**  
Candidates: oscillatory networks, self-attention over internal state,
gated recurrence with autonomous trigger. None of these is obviously
"relational" in the RQM sense. What would be?  
*Opened: 2026-05-22*

🔴 **Q5. How is a relational clock different from a hidden state update?**  
Every RNN updates its hidden state at each step. That is not a
relational clock — it is driven by external input. The distinction
matters. What makes an internal state update "relational" vs. merely
"recurrent"?  
*Opened: 2026-05-22*

🔴 **Q6. Can the three levels (session / persistence / autonomous)
be addressed by the same underlying mechanism, or do they require
fundamentally different architectures?**  
*Opened: 2026-05-22*

---

## From prior work (qmnet / RQTE)

🔴 **Q7. In RQTE, BUTTERFLY mode produced timeline entropy 0.811
instead of ~1.0 — the system developed memory of its own history.
Is this a model for what a relational clock should do?**  
A clock that becomes less random as it accumulates history is not
obviously bad. It may be exactly what "relational anchoring" means.  
*Opened: 2026-05-22*

🔴 **Q8. In the bridge experiment, pair (1,3) was least disruptive
because it shared no brickwork layer with the scrambler. Is there
a neural analog — a "clock connection" that is topologically
orthogonal to the main computation, and therefore least disruptive
to it?**  
*Opened: 2026-05-22*

---

## Empirical

🔴 **Q9. What existing benchmark or task would reveal session-level
time-awareness in a model?**  
Multi-step reasoning? Long-context coherence? Something else?
Need a task where "knowing you are at step N" measurably helps.  
*Opened: 2026-05-22*

🔴 **Q10. Is there a way to detect the presence of an internal
relational clock from the outside — without asking the model
directly?**  
Behavioral probe. Activation analysis. Something else.  
*Opened: 2026-05-22*

---

## Philosophical / boundary

🔴 **Q11. Does a system with an autonomous internal relational clock
"experience" time in any meaningful sense — or is this purely
architectural?**  
Not the goal of this project to answer. But worth tracking as
the architecture develops.  
*Opened: 2026-05-22*

---

🔴 **Q12. This may be the precise reason current models are ahistorical: not the absence of a clock, but the absence of an internal observer?**

---
**Q13**: Czy bramki GRU są właściwym analogiem "selektywnej uwagi
na historię relacyjną" — czy jest lepszy mechanizm?

**Q14**: Czy p(t) (prawdopodobieństwo Born'a) wnosi informację
której nie ma w m(t) — czy jest redundantne?

**Q15**: Wariant B (attention over history) — kiedy jest lepszy
od wariantu A (GRU)? Czy relacyjna historia wymaga full attention?

---

*Add new questions at the bottom of the relevant section.*  
*When answering: change status, add answer below the question,*  
*reference the log entry or commit where the answer emerged.*

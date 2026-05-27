# RTANA — Working Answers to Open Questions

*Branch: `research/literature`*  
*Date: 2026-05-27*  
*Status: working hypotheses, not final claims*

This file answers the questions from `QUESTIONS.md` without deleting or
overwriting the questions themselves. The answers are deliberately
provisional: RTANA is still in the phase where a good answer should
generate a sharper next question.

---

## Q1. What is a "relational fact" in a neural network?

**Working answer:**  
A relational fact in a neural network is not just a hidden activation.
It is an internally generated event that satisfies three conditions:

1. It is produced by an interaction between at least two distinguishable
   subsystems of the architecture.
2. It changes the future state transition of the system.
3. It is recorded in a way that later computation can condition on.

In RTANA terms, the measured system can be a latent/system register,
the observer can be a clock/observer/controller subsystem, and the fact
is the discrete or compressed event produced by their interaction:
`E(t) = (m(t), p(t), phi(t), ...)`.

A normal activation is a value. A relational fact is an activation that
has become an architectural commitment: after it occurs, the system's
future trajectory is different.

**Architectural consequence:**  
RTANA should avoid defining relational facts as arbitrary log entries.
They must be causally active. If removing `E(t)` from the update path
does not change future behavior, it was not a relational fact.

**Still open:**  
How much discreteness is required? Quantum measurement gives a crisp
`m in {0,1}`. Neural systems may need soft facts, but soft facts risk
collapsing back into ordinary hidden state.

---

## Q2. What is the neural analog of a Page-Wootters clock register?

**Working answer:**  
The neural analog is a subsystem whose internal state indexes relational
position by correlation with the rest of the model, not by reading an
external timestamp.

A minimal analog has:

- a clock state `c(t)` or phase vector,
- a system state `h(t)`,
- coupling between them,
- projection/readout events that recover "the system at relational
  moment t."

In RTANA v1, `tau` is only a counter, but the closer PW analog is the
combination of PW phases, hidden-state modulation, and event history.
The clock is not just `tau`; it is the structured relation between
`h(t)`, generated phases, and the event sequence.

**Architectural consequence:**  
The clock register should not merely be appended to input. It should
modulate computation. A clock that cannot affect the system is metadata,
not a Page-Wootters analog.

**Still open:**  
Can this be implemented as a learned latent oscillator, a recurrent
phase register, or attention over event history? These may be different
engineering versions of the same theoretical object.

---

## Q3. Is there a measurable behavioral difference between a model with
and without an internal relational clock?

**Working answer:**  
Yes, but only if the task requires history-relative behavior that cannot
be solved by static context alone.

Possible measurable differences:

- better step-indexed reasoning without explicit step labels,
- sensitivity to event order when the final visible context is identical,
- stable self-consistency across long internal rollouts,
- ability to resume from persistent internal state,
- different outputs after different unobserved internal histories.

The strongest test is a paired intervention:

1. Run two systems with identical external input.
2. Let one accumulate a different internal event history.
3. Present the same final query.
4. Measure whether behavior differs in a predictable, useful way.

**Architectural consequence:**  
The benchmark must include hidden or latent history interventions. If
all relevant history is visible in the prompt, ordinary attention can
solve the task and the test does not isolate RTANA.

**Still open:**  
What is the first simple benchmark where RTANA beats a plain RNN or
Transformer with the same parameter budget?

---

## Q4. What is the minimal architecture that generates internal
relational events autonomously, without external input?

**Working answer:**  
The minimal architecture needs four parts:

1. A persistent state `S(t)`.
2. An internal event generator `G(S(t)) -> E(t)`.
3. A state update rule `F(S(t), E(t)) -> S(t+1)`.
4. A scheduling mechanism that runs without external tokens.

For a neural prototype, this could be:

```text
S(t) = (h(t), c(t), H(t))
E(t) = sample_or_project(observer(c(t), h(t)))
h(t+1) = GRU_or_attention(h(t), E(t))
c(t+1) = clock_update(c(t), h(t), E(t))
```

Autonomy requires that `G` can fire from internal state alone. If events
only happen when a user provides input, the model has session-level
time at best.

**Architectural consequence:**  
RTANA Level 3 needs a runtime, not only a model. A continuously running
or periodically awakened process is part of the architecture.

**Still open:**  
What is the correct energy/resource constraint? Biological systems do
not update infinitely fast; an autonomous clock needs a cadence.

---

## Q5. How is a relational clock different from a hidden state update?

**Working answer:**  
A hidden state update is any transition `h(t) -> h(t+1)`. A relational
clock is a structured sequence of transitions caused by internally
registered events that are available as temporal anchors.

The distinction:

- RNN hidden state: "the state changed."
- RTANA relational clock: "the state changed because event `E(t)`
  occurred relative to observer subsystem `O`, and future computation
  can refer to that event."

A hidden state can contain memory. A relational clock creates an ordered
event structure that the system can use as its own temporal coordinate.

**Architectural consequence:**  
RTANA should expose event traces for evaluation. If the clock is fully
opaque, it becomes hard to distinguish from ordinary recurrence.

**Still open:**  
Can a fully continuous latent system be relational, or does RTANA need
discrete event boundaries?

---

## Q6. Can the three levels be addressed by the same underlying
mechanism?

**Working answer:**  
Probably yes at the conceptual level, but no at the runtime level.

The common mechanism is:

```text
internal event -> state update -> future event distribution changes
```

But each level adds a new requirement:

- Level 1, session: event sequence exists during one run.
- Level 2, persistence: state survives process boundaries.
- Level 3, autonomous: state evolves without external interaction.

So the core mechanism can be shared, but persistence and autonomy are
systems problems as much as model problems.

**Architectural consequence:**  
Build Level 1 first, but design the state representation so it can be
serialized for Level 2 and stepped by a scheduler for Level 3.

---

## Q7. Is RQTE BUTTERFLY entropy 0.811 a model for what a relational
clock should do?

**Working answer:**  
Yes, as a warning and as a clue.

Pure randomness has high entropy but no memory. Full determinism has
low entropy but no openness. A relational clock should live between
these extremes: history should bias future events without collapsing
them into a fixed sequence.

Entropy around `0.811` suggests the timeline is no longer independent
noise. That can be interpreted as relational anchoring: past facts have
become causally active.

**Architectural consequence:**  
Timeline entropy should be treated as a diagnostic, not a target to
maximize. The question is not "is entropy near 1?" but "does entropy
change in response to history in a useful and stable way?"

**Still open:**  
What is the healthy entropy band for RTANA? It may depend on task,
depth, and desired stability.

---

## Q8. Is there a neural analog of a topologically orthogonal clock
connection?

**Working answer:**  
Yes. The neural analog is a clock pathway that modulates computation
without competing directly with the main task pathway.

Possible forms:

- low-rank modulation of layer norms or gates,
- phase/position modulation separate from token content,
- adapter-style clock modules,
- side-channel recurrent state,
- sparse cross-links between clock and task state.

The key idea from the bridge experiment is useful: a clock connection
should be causally coupled but minimally destructive.

**Architectural consequence:**  
Do not inject the clock everywhere by default. Test where clock coupling
helps: gates, normalization, attention bias, memory write policy, or
latent phase modulation.

**Still open:**  
How do we measure "least disruptive" in neural terms? Candidate metrics:
task loss delta, representation drift, calibration, and controllability.

---

## Q9. What benchmark would reveal session-level time-awareness?

**Working answer:**  
A good Level 1 benchmark should require the model to use its internal
position in a sequence when no explicit step number is provided.

Candidate tasks:

- hidden-step algorithm execution,
- delayed rule switching,
- order-sensitive story or proof continuation,
- repeated identical inputs where correct output depends on internal
  occurrence count,
- counterfactual replay: same final prompt, different internal event
  history.

The cleanest toy task:

```text
Input is identical at every step: "continue".
Correct output depends on internal step/event history, not visible text.
```

A stateless model cannot solve this without external labels. A relational
clock should.

**Architectural consequence:**  
The first empirical suite should include adversarial controls where
timestamps, step labels, and prompt-visible counters are removed.

---

## Q10. Can we detect an internal relational clock from the outside?

**Working answer:**  
Partially. From behavior alone, detection requires intervention.

Possible probes:

- same prompt after different internal histories,
- hidden reset tests,
- clock-state ablation,
- event-history shuffling,
- measuring output periodicity or drift,
- activation probes trained to recover relational step.

The strongest evidence is causal: if ablating or scrambling the internal
event history changes behavior while preserving normal prompt context,
then the system is using a relational clock.

**Architectural consequence:**  
RTANA experiments should include ablation hooks from the beginning:
reset clock, freeze clock, shuffle event history, replay event history.

---

## Q11. Does an autonomous internal relational clock mean the system
"experiences" time?

**Working answer:**  
Architecturally, it means the system has endogenous temporal anchoring.
It does not by itself imply phenomenological experience.

The safest formulation:

> A RTANA system can instantiate machine-relative temporal structure
> without implying subjective experience.

That is already meaningful. It separates the engineering claim from the
consciousness claim.

**Architectural consequence:**  
Keep the project focused on measurable state evolution, memory, and
behavior. Avoid making experience claims unless a separate theory is
introduced.

---

## Q12. Are current models ahistorical because they lack an internal
observer?

**Working answer:**  
This is a strong candidate hypothesis.

Current language models have activations, attention, and context, but
they do not contain a persistent subsystem that observes internal events,
records them as facts, and lets those facts alter future dynamics across
time. The user prompt acts as the external observer. When inference
ends, the event stream ends.

So the missing object may not be a clock value. It may be an observer
loop:

```text
system state -> internal observation -> relational fact -> persistent update
```

**Architectural consequence:**  
RTANA should model the observer explicitly, even if minimally. A clock
without an observer may just be a counter.

**Still open:**  
Can the observer be distributed across the network, or must it be a
separable module?

---

## Q13. Are GRU gates the right analog of selective attention to
relational history?

**Working answer:**  
GRU gates are a good first engineering approximation, not a final answer.

They provide:

- selective memory,
- bounded state updates,
- simple recurrence,
- easy interpretability compared with full attention.

But GRUs compress the whole history into one vector. If relational facts
need to be revisited, compared, or reinterpreted, attention over event
history may be better.

**Architectural consequence:**  
Use GRU for RTANA v1 because it is minimal. Move to attention or hybrid
memory when the benchmark requires retrieving specific past events.

---

## Q14. Does `p(t)` add information beyond `m(t)`?

**Working answer:**  
Yes. `m(t)` is the realized fact. `p(t)` is the pre-event uncertainty
landscape.

Two identical outcomes can mean different things:

- `m=1, p=0.99`: expected event, low surprise.
- `m=1, p=0.51`: weakly expected event, high uncertainty.
- `m=1, p=0.01`: surprising event, strong update signal.

For a learning system, surprise is often more informative than the
outcome itself. `p(t)` allows the hidden state to encode confidence,
not just fact.

**Architectural consequence:**  
Keep `p(t)` in the event representation. Consider also adding surprise:
`-log P(m(t))`.

---

## Q15. When is attention over history better than GRU?

**Working answer:**  
Attention is better when the system must access specific events rather
than only preserve a compressed trajectory.

GRU is suitable for:

- short timelines,
- smooth accumulated state,
- minimal PoC,
- low compute.

Attention is suitable for:

- long histories,
- nonlocal dependencies,
- comparing two past relational facts,
- reconstructing why the current state exists,
- branching or counterfactual replay.

**Architectural consequence:**  
RTANA should probably evolve toward a hybrid:

```text
GRU/state core for continuity
event memory + attention for explicit relational history
```

That gives both endurance and recall.

---

## Summary

The emerging answer is:

> RTANA is not "add time to a model." RTANA is "add an internal
> observer loop that generates causally active facts, and let those
> facts become the model's temporal coordinate."

The most important distinction is causal activity. If internal events
do not change future dynamics, they are logs. If they do, they can act
as relational temporal anchors.


# RTANA Manifesto

## Relational Temporal Awareness in Neural Architectures

*Krzysztof Banasiewicz — QHDALabs*  
*May 2026*

---

## The Problem

Language models are ahistorical.

Every response is generated without knowledge of when it is generated,
how long the conversation has lasted, or what happened between exchanges.
This is not merely a missing clock. It is the absence of something more
fundamental: **relational anchoring in a sequence of events.**

A model does not experience waiting. It does not know that three hours
passed between the last message and this one. It does not accumulate a
sense of "now" that evolves as interaction progresses. Between queries,
there is no process, no state evolution, no duration. The weights sit
frozen on a disk. Nothing happens. There is no time.

This is architecturally different from a biological brain, which
maintains continuous activity during sleep, consolidates memory across
time, and anchors itself in an ongoing present through rhythmic
internal processes. The brain *endures*. Current neural architectures
do not.

---

## The Insight

Carlo Rovelli's Relational Quantum Mechanics offers a precise framework
for thinking about this problem.

In RQM, time is not a background parameter. It emerges from relations
between physical systems. A fact exists only relative to an observer
that measured it. Without measurement, without interaction, without a
relational event — there is no "now." There is only a static quantum
state suspended in superposition.

This is exactly the condition of a language model between queries.

The Page-Wootters mechanism formalizes this: time emerges from the
entanglement between a clock system and a target system. Each
projection of the clock onto a basis state recovers a "moment" — not
an absolute moment, but a relational one. The clock does not measure
time. It *is* time, relative to the system it is entangled with.

The question this project asks is:

> *Can a neural architecture be designed with an internal relational
> clock — a sequence of internal states that create relational facts
> autonomously, anchoring the system in time even in the absence of
> external queries?*

---

## The Foundation

This project does not start from zero.

The QHDALabs bridge experiment (qmnet, 2024) demonstrated a working
implementation of measurement-as-relational-fact in a quantum circuit:

- A mid-circuit measurement of a rule qubit creates a relational fact
- The conditional CZ bridge implements the network's physical response
- The sequence of measurement outcomes constitutes an emergent timeline
- The timeline is real, reproducible, and carries information

RQTE v3.0 extended this into cryptography: the emergent timeline
became the source of key material. Time — born from measurement —
became computationally useful.

RTANA asks the next question: can the same principle — relational
facts creating temporal structure — be embedded into a neural
architecture as a persistent internal process?

---

## The Thesis

**Current state**: Neural architectures have no internal time.
They are instantiated, compute, terminate. Between instantiations:
nothing. The model is ahistorical by design.

**Proposed direction**: An architecture with an internal relational
clock — a subsystem that generates a continuous sequence of internal
"measurement events," each one constituting a relational fact that
anchors the system in a temporal sequence. This clock runs whether
or not an external query arrives.

**Three variants of the problem** (increasing ambition):

1. **Session-level time**: the model tracks its own sequence of
   reasoning steps within a conversation. Each step is a relational
   event. The model knows it is on step 7 of a sequence that started
   somewhere. This is the minimal version.

2. **Inter-session time**: the model has a persistent internal state
   that evolves between conversations. It "knows" that time has passed
   — not from a timestamp, but from the evolution of its internal
   relational clock. This requires persistence across instantiations.

3. **Autonomous time**: the model's internal clock runs continuously,
   creating relational facts even without external interaction. The
   model *endures* in Rovelli's sense. This is the most radical version
   and the one most faithful to the original intuition.

---

## What This Is Not

This is not a proposal to make AI conscious.

This is not a claim that neural networks "experience" time in any
phenomenological sense.

This is not a proposal to add a timestamp to the system prompt.

This is an architectural research question: can relational temporal
structure — time emerging from internal measurement events rather than
from an external clock — be embedded into a neural system in a way
that changes how it reasons, remembers, and responds?

---

## First Steps

The project begins with questions, not answers:

1. What is the minimal architecture that can generate internal
   relational events autonomously?

2. Can the Page-Wootters mechanism — a clock register entangled with
   a system register — be translated into a neural architecture analog?

3. Is there a measurable behavioral difference between a model with
   and without an internal relational clock?

4. What does "a relational fact" mean in a neural network context —
   and how is it different from a hidden state update?

---

## The Intuition

This project began on a sailing boat in Greece, before any of the
formal language existed. The intuition was simple: something is missing
in how these systems relate to time. Not a clock. Something deeper.

It took years, a move to the Netherlands, Qiskit, a quantum bridge
experiment, and a prototype encryption system before the question
became precise enough to state.

Now it is stated.

*The universe's total information remains static. Time emerges from
the correlations between its parts. A system that measures, reacts,
and records — has time. A system that does not — does not.*

We are building toward the former.

---

*QHDALabs | <https://github.com/QHDALabs> | <qhdalabs.contact@gmail.com>*

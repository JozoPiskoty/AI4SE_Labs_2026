---
name: architecture-discussion
description: 'Guide an interactive architecture discussion from a requirements file: extract requirements, separate them from assumptions, present exactly three candidate architectures one at a time, deep-dive on follow-ups, keep running notes, and finish with a comparison table and open questions. Use when asked to "discuss architectures", "propose architectures", "compare architectural styles", or start an architecture task for a system described by requirements. Does not write the ADR (use adr-creation for that).'
argument-hint: 'path to requirements file, notes file name (optional)'
---

# Architecture Discussion

Run a structured, interactive architecture discussion and keep a notes file. The output is the discussion record, not a decision.

## When to use
- The user gives requirements (user stories, a spec) and wants candidate architectures discussed.
- The user says to start an "architecture discussion" or "Task 1"-style exercise.
- Not for writing the ADR itself: hand over to the `adr-creation` skill afterwards.

## Ground rules
1. **Notes from the start.** If the user asks for notes, create the notes file immediately (default `TASK1_ARCHITECTURE_NOTES.md` if the user gave a name, otherwise `ARCHITECTURE_NOTES.md` next to the requirements). Append to it after every answer. Do not wait to be reminded.
2. **Wait when told to wait.** If the user says "don't start yet", only acknowledge and prepare.
3. **One step at a time.** Present only the architecture the user asked for. Do not jump ahead to the next one or to the decision.
4. **Answer in the user's language** (switch when they switch). Keep notes in the language the user last requested.
5. **Simple explanations with a concrete example** for each concept (for example a checkout where payment succeeds but the next step fails).
6. **Use edit/create tools for files**, not shell redirection.

## Procedure

### Step 1: Read and summarize requirements
- Read the requirements file and any assignment file completely (large files: use ranges).
- Write to the notes: scope, source files, and a **"Requirements stated in the source"** list (quote key phrases verbatim, such as how the system is described).
- Write a separate **"Not stated"** list: traffic, availability, latency, team size, budget, hosting, providers, data policies, authentication details, and anything domain-specific that is silent.
- **Ambiguous phrases** (for example "distributed system"): list the plausible readings, state the effect of each on architecture, and mark it unresolved. Never silently pick one.

### Step 2: Present exactly three candidate architectures, one per turn
Default set (replace with better-fitting ones only if the domain demands it, and say why):
1. Layered modular monolith
2. Microservices
3. Serverless / event-driven

For each, use [the architecture template](./references/architecture-template.md): how it works, main parts, a simple example flow, advantages, disadvantages, **how it differs from the previous architecture(s)**, main technical challenges, and fit with the requirements. Mark every statement that is our assumption, not a requirement.

### Step 3: Handle follow-ups
For each user follow-up, answer concretely and append a `### Follow-up: <topic>` section to the notes. Typical deep dives, pick those the user asks about:
- fit with the ambiguous requirement
- checkout or main workflow step by step (modules/services interaction)
- transactions, retries, duplicate callbacks/events, timeouts, partial failure
- state model for the key entities, split into **stated requirements vs assumptions**
- data ownership (shared vs per-service database)
- communication (synchronous vs asynchronous), deployment, monitoring, testing overhead
- service boundaries, too many services, identity and permissions across components
- cost and maintainability (especially serverless)
- when the style fits and when it is unnecessary

Use [the technical checklist](./references/technical-checklist.md) to make sure important failure and consistency topics are covered, but only present what the user asks for.

### Step 4: Close each architecture
When the user says an architecture has been discussed enough, add a **"Summary of pros and cons"** section to the notes before moving on. Fix any "Status"/"Current" lines that became stale, writing "at the time of this discussion" where needed.

### Step 5: Consolidate
When all three are done and the user asks, append a **Consolidated Summary** to the notes with:
- A. requirements stated in the source
- B. not stated / assumptions (table: topic, what the source says, our assumption)
- C to E. per architecture: how it works, pros, cons, main technical challenges, fit
- F. comparison table (deployment unit, operations, complexity, transactions, failure handling, scaling, cost predictability, lock-in, evidence of need in the requirements)
- G. points common to all three (payment/shipment-style external failures do not disappear)
- H. provisional observations, explicitly **not a decision**
- I. open questions
- J. next steps (ADR and further work not started unless asked)

Then verify the notes reflect what was actually discussed: do not add content that was never discussed, and list remaining open questions honestly.

## Quality bar
- Requirements and assumptions are never mixed.
- Each architecture has fair pros and cons; no strawman.
- No architecture is declared the winner in this skill.
- Notes are chronological and match the conversation.
- Do not modify earlier completed deliverables unless asked.

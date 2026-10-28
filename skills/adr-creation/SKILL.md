---
name: adr-creation
description: 'Recommend an architecture from prior architecture-discussion notes and write, review, and finalize an Architecture Decision Record (ADR) with a separate Task notes file. Handles ambiguous requirements honestly (working assumptions vs confirmed requirements), status wording (Proposed vs Accepted), consistency review, and change history. Use when asked to "create an ADR", "choose an architecture", "write the architecture decision", or "revise/finalize the ADR". Typically follows the architecture-discussion skill.'
argument-hint: 'path to architecture notes, ADR file name (optional), notes file name (optional)'
---

# ADR Creation

Turn an architecture discussion into a reviewed ADR plus a record of how it was produced.

## When to use
- The user has architecture notes (ideally from the `architecture-discussion` skill) and wants a recommendation and an ADR.
- The user asks to revise, review, or finalize an existing ADR.

## Ground rules
1. **Notes from the start.** Create the ADR notes file (default `TASK2_ADR_NOTES.md`) at the first step and add one `### Iteration N` entry per user request: request, what changed and why, what was checked, what is still open. Add a change-history table at the end.
2. **Never record checks or discussions that did not happen.** Say how a check was done (for example "by reading and text search, no link checker run").
3. **Do not treat assumptions as confirmed requirements.** Number and label them.
4. **Do not claim stakeholder approval** that does not exist.
5. **Technology-neutral** unless the requirements or user choose technologies; list "Not decided here".
6. **Edit existing files in place** with edit tools; do not rewrite history. Earlier change-log rows keep the status that was true then.
7. **Do not start later tasks** (Skill creation, implementation) unless asked.

## Procedure

### Step 1: Read inputs
Read the assignment, the requirements, and the full architecture notes (especially the consolidated summary, comparison table, and open questions).

### Step 2: Recommend (and record in notes)
- Recommend one architecture and explain why it beats each of the other two, using evidence from the requirements and the earlier discussion.
- If a requirement phrase is ambiguous (for example "distributed system"), state the readings, say which the recommendation depends on, and what changes under the other reading.
- Choose a status: `Proposed` while key questions are open and the user has not accepted; `Accepted` only when the user explicitly asks, and then say for whom/what ("for this design exercise, conditional on assumption X; no external approval").

### Step 3: Write the first draft
Use [the ADR template](./references/adr-template.md). Required: header table (status, approval, date, scope, sources with relative links), context (stated requirements; what is not stated; ambiguity table; assumptions table with "needs confirmation"; decision drivers), alternatives with pros/cons, **overview comparison table**, decision, reasons, consequences, risks with mitigations, revisit triggers, open questions, **component diagram** (ASCII in a `text` block), change log.

### Step 4: Iterate when asked
Typical rounds, in this order:
1. Add key risk analysis for the ambiguous requirement (what, why still chosen, likelihood, impact, mitigation, what changes if the other reading is true).
2. Add critical failure-recovery details (for example payment initiation after a crash) using [the review checklist](./references/review-checklist.md). Keep the section if useful; move it to an appendix only if it hurts readability.
3. Full consistency review (below).
4. Final formatting and link check.
5. Status change if the user requests it; update every current-status reference, keep history accurate.

### Step 5: Consistency review
Walk [the review checklist](./references/review-checklist.md). Make only necessary edits. Remove repetition only when it adds nothing; repetition serving different purposes (context, reason, risk, trigger, question) may stay.

### Step 6: Close each iteration
- Add a change-log row in the ADR (version, date, change).
- Add an iteration entry and a history row in the notes file.
- Summarize to the user: what changed, status, files ready, remaining limitations.
- Separate **open questions that could invalidate the decision** from **implementation questions**.

## Quality bar
- The ADR can be read alone; sources are linked.
- The decision, reasons, risks, revisit triggers, and open questions do not contradict each other.
- Status wording is identical everywhere it is current.
- The comparison table and diagram match the text.

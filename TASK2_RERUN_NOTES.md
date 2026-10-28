# Task 2 Rerun — ADR Creation Notes

### Iteration 1

- **Request:** Read the CDC Shop architecture discussion, recommend an architecture and explain why the alternatives were not selected, create `ADR_RERUN.md`, and document the discussion and review process here. Keep requirements separate from assumptions, address the unresolved meaning of “distributed system,” review the ADR for consistency, and do not modify the original Task 1 or Task 2 files.
- **What changed and why:** Created `ADR_RERUN.md` with a **Proposed**, conditional recommendation for a layered modular monolith. This is the least complex fit to the stated user workflows given no confirmed need for internal independent deployments, scaling, or asynchronous cloud execution. Microservices were not selected because their service/data/network coordination costs are not justified by stated constraints; serverless/event-driven was not selected because cloud hosting, burst traffic, and asynchronous response needs are not stated. The recommendation depends on the working assumption that “distributed system” means the overall system may include separate systems or is descriptive (Readings B/C), not that independently deployable internal services are mandatory (Reading A).
- **What was checked:** Read `Tasks/Task_2.md`, `Tasks/data/CDC.txt`, all sections of `TASK1_RERUN_NOTES.md`, the ADR template, and the review checklist. Read the complete ADR in ranges and text-searched it for status, ambiguity, transaction/outbox, failure-state, section-heading, and placeholder terms. Reviewed consistency of the comparison against the Task 1 notes; the ADR keeps remote calls outside database transactions, documents order/payment/outbox Transaction 1 and provider-result/state/next-outbox Transaction 2, and covers crash points, retries, duplicate/late callbacks, unknown timeouts, shipment failure, and multiple workers. Reviewed numbered assumptions, explicit “Not decided here” items, split decision-invalidating vs implementation questions, text diagram, and change log. Confirmed source and notes files linked by relative paths exist by opening them. No automated link checker or external approval was used.
- **Still open:** The meaning of “distributed system” and other decision-invalidating topology, scale, availability, recovery, ownership, and hosting constraints. Provider details, state models, inventory, authorization policy, and implementation details also remain open. No ADR acceptance or implementation is recorded.

## Change history

| Iteration | Date | Change |
|---|---|---|
| 1 | 2026-10-28 | Created and consistency-reviewed a proposed, conditional modular-monolith ADR; recorded alternatives, assumptions, recovery design, risks, and open questions. |

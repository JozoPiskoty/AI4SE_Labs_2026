# ADR review checklist

Check each item by reading the whole ADR and by text search; report only checks actually done.

## Contradictions
- [ ] Transaction boundaries identical in decision, recovery section, reasons, risks, diagram (for example transaction 1: order + payment attempt + outbox entry before any remote call; transaction 2: confirmed result + state update + next outbox entry).
- [ ] No claim that a remote call is inside a database transaction.
- [ ] Payment/outbox/shipment-scheduling flow consistent across sections.
- [ ] Comparison table, alternatives text, and the architecture notes agree (complexity, lock-in, transactions, readings satisfied).
- [ ] Ambiguous requirement handled the same way in context, reasons, risk, triggers, questions.

## Status consistency
- [ ] Current status wording identical in header, decision text, risks, open questions.
- [ ] Words like "propose", "before acceptance", "draft" appear only in history.
- [ ] No implied external approval.

## Completeness
- [ ] Stated requirements separated from assumptions; assumptions numbered.
- [ ] Crash scenarios covered: before commit, after commit before send, after remote call before save, after confirmation before update.
- [ ] Duplicate callbacks, timeouts ("unknown"), shipment failure after payment, expiry/late success, multi-instance workers.
- [ ] Revisit triggers include the ambiguity and scale/availability/ownership changes.
- [ ] Open questions split into invalidating vs implementation.
- [ ] Technology-neutral, with a "Not decided here" list.

## Format
- [ ] Heading hierarchy and numbering continuous.
- [ ] Tables have consistent column counts; code fence closed.
- [ ] Relative links point to files that exist.
- [ ] Change log updated; notes iteration entry and history row added.

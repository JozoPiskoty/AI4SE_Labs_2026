# Task 2 — ADR Discussion Notes (CDC Shop)

Notes on the discussion that produces the Architecture Decision Record in [ADR_CDC_SHOP.md](./ADR_CDC_SHOP.md). Source material: [TASK1_ARCHITECTURE_NOTES.md](./TASK1_ARCHITECTURE_NOTES.md), `Tasks/data/CDC.txt`, and `Tasks/Task_2.md`. Task 3 (Skill) has not been started.

## Task 2 goal

Create an ADR from the Task 1 discussion, inspect it, and refine it over several iterations (informativeness, missing or extra content, structure, need for an overview table or diagram).

## Session log

### Iteration 1 — Recommendation and first draft

**User request:** Recommend the most suitable architecture for CDC Shop and explain why it is better than the other two. Treat the unclear meaning of "distributed system" carefully and do not present assumptions as confirmed requirements. Write the ADR draft with context, alternatives, decision, reasons, pros/cons, risks, and open questions.

**Recommendation (provisional):** Architecture 1, a modular monolith, as the core application. Payment and shipping interactions are handled asynchronously inside it (transactional outbox, idempotent webhook handling, background worker, reconciliation). Module boundaries are enforced so that capabilities can be extracted later. Serverless functions for webhook or tracking edges remain an optional later addition, not part of the initial decision.

**Why this over the alternatives**

- Versus microservices (Architecture 2):
  - `CDC.txt` lists 25 conventional stories and gives no scale, team, availability, or release-independence need that would pay for the overhead of separate deployments, databases, a broker, a saga for checkout, and cross-service tracing.
  - The hardest problems (payment and shipment failure handling) exist in both; microservices add internal ones on top.
  - Cart-to-order conversion benefits from local transactions.
- Versus serverless (Architecture 3):
  - Serverless removes server management, not the hard domain problems.
  - Core flows are plain request/response CRUD with transactional steps, which gain little from functions.
  - Highest lock-in, harder local testing and debugging; traffic profile and cloud choice are unknown.
  - Its strengths (webhooks, tracking updates, scheduled jobs) can be added at the edges later.

**How the "distributed system" ambiguity is handled**

- `CDC.txt` uses the phrase only in the system description and never says CDC's own capabilities must be independently deployable.
- Two readings: (a) a system distributed across infrastructure and integrated with external payment and shipping providers; (b) CDC's own capabilities as independently deployable services.
- The recommendation is **conditional on reading (a)**. It is stated in the ADR as an assumption to confirm, with an explicit trigger: if (b) is confirmed, the decision should be revisited and Architecture 2 (or a first extraction of selected modules) becomes the stronger option.
- To keep reading (a) credible, the design is run as several application instances behind a load balancer with a database that supports it, and the payment and shipping integrations are treated as genuine distributed boundaries (asynchronous, idempotent, reconciled).

**Requirements vs. assumptions handling in the ADR**

- Only the content of `CDC.txt` is labeled as a requirement. Everything else (state model, provider behavior, outbox, snapshots, token-based identity, hosting) is labeled as an assumption or design decision.
- Assumptions are collected in one table with their consequences and a "needs confirmation" flag.

**Decisions made while drafting**

- Status of the ADR: **Proposed** (not Accepted), because key questions are open.
- Scope kept to the architecture style and its key supporting patterns; technology products (language, framework, cloud, gateway, carrier) are deliberately not chosen because nothing in the requirements supports a choice.
- Included an overview table (alternatives against criteria) and a simple component diagram to help reviewing. Both may be removed or changed in later iterations.

**Open for the user to review**

1. Is the recommendation conditional on reading (a) acceptable, or should the ADR assume reading (b)?
2. Is the draft informative enough? Anything missing or extra?
3. Are the table and diagram helpful, or should the ADR be shorter?
4. Should the ADR name concrete technologies, or stay technology-neutral?

### Iteration 2 — Revision after first review

**User feedback:** The ADR looks good overall. Revise once more to (1) clarify the risk around the meaning of "distributed system", (2) explain how payment initiation recovers if the app crashes after creating an order, and (3) mention that serverless can overlap with microservices. Keep the comparison table, the diagram, and the technology-neutral approach. Keep status Proposed; do not start Task 3.

**What changed and why**

1. **"Distributed system" risk (ADR section 6.1, new):**
   - Presented as the largest risk, since the recommendation depends on an interpretation `CDC.txt` does not confirm.
   - States what the risk is, why the monolith is still proposed, likelihood (unknown) and impact (high if reading (b) is intended), mitigations, and what changes if (b) is confirmed.
   - Mitigations: confirm before the ADR moves from Proposed to Accepted; strict module boundaries, module-owned data and interface-based provider integrations so payment or shipment can be extracted first; multiple instances so reading (a) is genuinely met; revisit triggers.
   - Reading (a) is explicitly labelled our interpretation, not a requirement (also in section 1.3).
2. **Payment initiation recovery (ADR section 3.1, new):**
   - Order, payment attempt (with a stable idempotency key), and a payment-initiation outbox entry commit in one local transaction, before any gateway call.
   - A table of four crash points (before commit, after commit before sending, after gateway call before saving, after confirmation before order update) with what exists and how it recovers.
   - Supporting rules: safe claiming of outbox entries across instances, reconciliation sweep of old `PENDING_PAYMENT` orders, reuse of the pending order on repeat checkout, expiry as an undefined business policy (A8), and the assumption that the gateway supports idempotency keys and status lookup (A1), to be verified at gateway selection.
   - Decision list, diagram, and risk table updated so payment initiation goes through the outbox.
3. **Serverless overlaps with microservices:**
   - Added to section 2.3: serverless is an execution model, microservices a decomposition style; a microservice can run as functions.
   - Comparison table row for reading (b) now says serverless satisfies it only if functions form independently deployable, data-owning services.
   - Reasons section notes serverless is not a way around microservice boundary and consistency costs; section 6.1 notes serverless could implement services if (b) is confirmed.

**Kept unchanged:** comparison table, component diagram (only the worker label updated), technology-neutral approach, status Proposed.

**Observations for later review**

- The ADR is growing; if it feels long, section 3.1 could move to an appendix.
- Still unresolved and needing stakeholder input: reading (a) vs (b), payment and shipping provider behavior, expiry and refund policy, merchant model, traffic and availability targets.

### Iteration 3 — Full review of draft 2

**User request:** Review the entire ADR for contradictions, repetition, missing information, and consistency with the Task 1 notes. Keep the payment recovery details; use an appendix only if it improves readability. Make only necessary changes; keep status Proposed; do not start Task 3.

**Review result:** no contradictions found. The ADR's requirements, assumptions, alternatives, and risks match the Task 1 notes (stated requirements vs. assumptions, reading (a) vs (b), state model, outbox/inbox/idempotency approach, comparison table).

**Changes made (all small)**

- Comparison table: serverless operational complexity changed from "Medium" to "Medium to high", matching Task 1.
- Decision: added carrier tracking-update handling (deduplicated, valid forward transitions only), which was in Task 1 but missing from the ADR; tied authorization to the authenticated identity and role (A5).
- A3 now points to the Task 1 state model; open question 4 now also asks whether customers see one order status or separate order, payment, and shipment statuses (a Task 1 open question that was missing).
- Reason 1: "without extra infrastructure" reworded to "without service-to-service infrastructure", because the design still needs a load balancer, database, and background worker.
- Reason 3: the serverless/microservices overlap point shortened, since it is explained in section 2.3.
- Status line updated to draft 3; change log gained a row 3.

**Decisions on structure**

- **Section 3.1 (payment recovery) stays in place, not moved to an appendix.** The ADR is about 21 KB; the section is self-contained, directly supports the decision, and is referenced from sections 3 and 6.2. Moving it would force readers to jump around without shortening the document. It can still move to an appendix later if the ADR needs to be shorter.
- **Repetition tolerated:** the reading (a)/(b) point appears in sections 1.3, 4 (reason 6), 6.1, 7, and 8. Each serves a different purpose (context, justification, risk, trigger, question), so none was removed.
- **Kept as is:** comparison table, component diagram, technology-neutral approach, status Proposed.

**Still unresolved (needs stakeholder input):** reading (a) vs (b); payment and shipping provider behavior; order creation timing and single vs separate statuses; stock; expiry and refund policy; merchant model; traffic and availability targets; authentication details; portability.

### Iteration 4 — Final submission version

**User request:** Prepare the final submission version of the ADR: keep status Proposed, remove "draft 3, under review" from the status field, check Markdown formatting and internal links, update change history and notes, summarize deliverables. Do not start Task 3.

**Changes**

- ADR status field now reads only **Proposed**.
- `CDC.txt` in the sources row is now a link; the first change-log column was renamed from "Draft" to "Version"; a row 4 was added.
- Checked: heading hierarchy (1–10 with subsections 1.1–1.5, 2.1–2.4, 3.1, 5.1–5.2, 6.1–6.2), tables, and the closed `text` code block for the diagram. Relative links to `TASK1_ARCHITECTURE_NOTES.md`, `TASK2_ADR_NOTES.md`, and `Tasks/data/CDC.txt` point to existing files.
- No content or decision changes.

**Final deliverables for Task 2**

- `ADR_CDC_SHOP.md` — final ADR (status Proposed).
- `TASK2_ADR_NOTES.md` — record of the ADR discussion and iterations (this file).
- Supporting: `TASK1_ARCHITECTURE_NOTES.md` — the Task 1 discussion record the ADR is based on.

### Iteration 5 — Transaction-scope fix

**User request:** Reason 4 said order creation, payment-state updates, and shipment queueing could happen in one transaction. Clarify that checkout creation + payment initiation is one transaction, and confirmed payment + shipment scheduling is a separate one; check for similar inconsistencies; keep status Proposed; no Task 3.

**Changes**

- Reason 4 rewritten to describe two local transactions with the gateway call between them outside any transaction.
- Decision item 3 now labels transaction 1 (checkout) and transaction 2 (payment confirmation).
- Checked all other "transaction" mentions (sections 2, 3, 3.1, comparison table, diagram); no other contradictions found.

### Iteration 6 — Final review and acceptance for the exercise

**User request:** Complete Task 2: review `Task_2.md`, the ADR, both notes files; keep the modular monolith; adopt reading (a) of "distributed system" as an explicit working assumption (not confirmed by instructor or stakeholder); set status to Accepted for this design exercise, conditional on that assumption; keep the (b) risk and revisit rule; update current-status references while keeping history accurate; separate implementation questions from invalidating issues; check the ADR for contradictions; do not start Task 3.

**Final decision:** layered modular monolith, status **Accepted** for this design exercise, conditional on working assumption WA-1 (reading (a): multiple application instances plus external payment and shipping integrations). The ADR states that no instructor or stakeholder has approved the decision or confirmed WA-1.

**Checks performed** (by reading the full ADR, the notes, and `Task_2.md`, and by text searches; no Markdown linter or link checker was run)

- Task 2 asks for an ADR that was inspected and revised several times, and for the conversation record. Both exist: the ADR went through versions 1–6, and this file records the iterations.
- Transaction boundaries: decision item 3, section 3.1, reason 4, and the risk table agree that transaction 1 (order, payment attempt, payment-initiation outbox entry) commits before any gateway call, and transaction 2 (payment result, order update, shipment-request outbox entry) runs on confirmed payment. Section 3.1 had no explicit link to transaction 2, so I added one.
- Payment recovery, outbox, and shipment scheduling: the crash table, the supporting rules, the risk table, and the diagram are consistent.
- Comparison of the three architectures: the overview table, the alternatives text, and the Task 1 consolidated summary agree. No change.
- Searched for leftover "propose", "recommend", "draft", "before acceptance" wording. Remaining hits are the historical change-log rows and an A3 reference to a Task 1 heading, which are correct as history.
- Internal links (sources row here and in the ADR) point to files in the same folder or `Tasks/data/CDC.txt`, which exist.

**Changes made to the ADR**

- Status → Accepted with the WA-1 condition; new Approval row stating there is no external approval.
- Section 1.3 defines WA-1 as our assumption; section 1.4 intro distinguishes it from A1–A8.
- Decision wording changed from "propose" to "select"; section 3.1 references transactions 1 and 2.
- Section 6.1, the risk table, reason 6, and revisit triggers: removed the "before Proposed → Accepted" wording; added that the decision must be revisited if CDC's own capabilities must be independently deployable.
- Open questions split: 8.1 (reading (a)/(b), could invalidate the decision) and 8.2 (provider, stock, refunds, order states, traffic, authentication, portability: implementation questions that do not change the architecture unless a revisit trigger is hit).
- Change log row 6.

**Not changed:** the comparison table, the component diagram, the technology-neutral approach, and the payment recovery detail. Iterations 1–5 above still describe the status as Proposed because it was at that time.

**Limitations that cannot be resolved from the provided requirements**

- The meaning of "distributed system" is still unconfirmed.
- Payment and shipping provider behavior, traffic and availability targets, refund and expiry policy, stock, and authentication details are not stated in `CDC.txt`.
- The decision is a design-exercise decision, not stakeholder-approved.

## Change history

| Iteration | Change |
|---|---|
| 1 | Created this notes file and the first ADR draft (status: Proposed). |
| 2 | ADR draft 2: added "distributed system" risk section, payment-initiation crash recovery section, serverless/microservices overlap; updated change log; status still Proposed. |
| 3 | ADR draft 3: full review; small consistency fixes only (see Iteration 3); status still Proposed. |
| 4 | Final submission version (see Iteration 4); status still Proposed. |
| 5 | Transaction-scope fix in reason 4 and decision item 3 (see Iteration 5); status still Proposed. |
| 6 | Final review; status changed to Accepted (conditional on working assumption WA-1); see Iteration 6. |

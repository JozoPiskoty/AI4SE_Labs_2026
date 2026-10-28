# ADR-001: Architecture style for CDC Shop

| Field | Value |
|---|---|
| Status | **Accepted**, for the purposes of this design exercise and **conditional on working assumption WA-1** (reading (a) of "distributed system", section 1.3) |
| Approval | Decided by us (student and coding assistant) for this exercise. **No instructor or external stakeholder has approved or confirmed this decision or WA-1.** |
| Date | 2026-10-28 |
| Scope | Overall architecture style of CDC Shop |
| Sources | [CDC.txt](./Tasks/data/CDC.txt), [TASK1_ARCHITECTURE_NOTES.md](./TASK1_ARCHITECTURE_NOTES.md), [TASK2_ADR_NOTES.md](./TASK2_ADR_NOTES.md) |

## 1. Context

### 1.1 Requirements stated in `CDC.txt`

- CDC Shop is "a distributed system that handles the management, the payment and the shipment of products", mainly materials found in a hardware store.
- **Customers** can register, log in and out, access a profile, browse the product list, view product details, search by name, sort by ascending/descending price, add a product to the cart, view the cart, remove all items from it, pay for the current cart, check an order for package information, access About Us, and contact the shop.
- **Merchants** can log in and out, access a profile, browse the product list, view product details, search by name, sort by price, change a product's price, insert/remove products, and access About Us.

### 1.2 What `CDC.txt` does not state

The file says nothing about expected traffic or peaks, availability or latency targets, team size, budget, hosting or cloud provider, payment gateway, shipping provider, inventory, refunds or cancellations, order states, number of merchants, or authentication mechanism. The phrase "distributed system" is not defined.

### 1.3 The ambiguity of "distributed system"

| Reading | Meaning | Effect on this decision |
|---|---|---|
| (a) | The system runs on distributed infrastructure (several instances) and integrates with external payment and shipping systems | A modular monolith satisfies it |
| (b) | CDC's own capabilities (catalog, orders, payment, shipment, ...) must be independently deployable services | Only a service-based architecture satisfies it |

`CDC.txt` does not say which reading is intended, and nobody has confirmed one.

**Working assumption WA-1 (adopted for this design exercise):** we adopt reading (a). CDC runs across multiple application instances and integrates with external payment and shipping systems. This is **our architectural assumption, not a requirement confirmed by the instructor or any stakeholder.** The decision below is conditional on WA-1. The risk that reading (b) is intended is analysed in section 6.1, and the decision must be revisited if it is (section 7).

### 1.4 Assumptions used in this ADR

These are our working assumptions, **not requirements**. They are in addition to WA-1 (section 1.3). WA-1 could invalidate the decision if wrong; A1–A8 mostly affect implementation details (see section 8).

| # | Assumption | Needs confirmation |
|---|---|---|
| A1 | Payment is handled by an external gateway; confirmation may arrive asynchronously by callback (webhook). Raw card data is not stored by CDC. | Yes |
| A2 | Shipping is handled through an external carrier or fulfilment provider with shipment creation and tracking updates. | Yes |
| A3 | Order, payment, and shipment have separate statuses with validated transitions; shipment is created only after confirmed payment. (Illustrative state model: Task 1 notes, "Proposed order, payment, and shipment state model".) | Yes |
| A4 | Orders keep a snapshot of product name and price at purchase time. | Yes |
| A5 | Identity uses signed, short-lived tokens with `customer` and `merchant` roles. | Yes |
| A6 | Traffic is modest and not strongly bursty; the team is small. Neither is stated. | Yes |
| A7 | Stock/inventory management is out of scope for now. | Yes |
| A8 | Refunds, cancellation, retry limits, and order expiry will be defined later as business policy. | Yes |

### 1.5 Decision drivers

1. Fit with the stated functionality, without paying for needs the requirements do not show.
2. Correct and recoverable payment and shipment handling (duplicates, timeouts, partial failure).
3. Simplicity of development, testing, and operations.
4. Honest handling of "distributed system" (reading (a) vs (b)).
5. Ability to evolve (extract capabilities later if a real need appears).
6. Cost predictability and avoiding unnecessary vendor lock-in.

## 2. Alternatives considered

### 2.1 Layered modular monolith

One deployable application with enforced internal modules (identity, catalog, cart, order, payment integration, shipment integration, shop information/contact), usually one database with local transactions.

- Pros: simplest to build, test, deploy and monitor; local transactions for CDC-owned data; low lock-in; predictable cost; seams for later extraction.
- Cons: deployed and scaled as a unit; an application-wide fault or bad release affects all features; boundaries erode without discipline; does not satisfy reading (b).

### 2.2 Microservices

Separately deployed services (identity, catalog, cart, order, payment, shipment) behind an API gateway, database per service, synchronous APIs plus a message broker.

- Pros: independent deployment and scaling; potential fault isolation; clear ownership; satisfies reading (b).
- Cons: no cross-service transaction, so checkout is an eventually consistent saga; many more moving parts (deployments, databases, broker, security, tracing, contract tests); risk of a "distributed monolith"; no stated need for the overhead.

### 2.3 Serverless, event-driven

Managed functions triggered by HTTP or events, with a managed database, queue or event bus, and identity service.

- Pros: little server administration; automatic scaling including to idle; good for webhooks, tracking updates and scheduled jobs; cheap for low or bursty traffic.
- Cons: highest provider lock-in; cold starts, limits and quotas; workflow spread across functions and queues; harder local testing and debugging; can be costly under steady load; function sprawl.
- **Relationship to microservices:** serverless describes how code is executed (provider-managed functions), whereas microservices describe how the system is divided (independently deployable services with their own data). They are not mutually exclusive: a microservice can itself run as serverless functions, and a set of functions that each own a capability and its data is effectively a microservice architecture. Serverless is therefore listed as a separate alternative for comparison, but in practice the two overlap, and a serverless variant of CDC could also satisfy reading (b) if its functions are grouped into independently deployable, data-owning services.

### 2.4 Overview

| Criterion | Modular monolith | Microservices | Serverless |
|---|---|---|---|
| Satisfies reading (a) | Yes | Yes | Yes |
| Satisfies reading (b) | No | Yes | Only if functions are organized as independently deployable, data-owning services (i.e. as serverless microservices) |
| Complexity of development | Low | High | Medium to high |
| Operational complexity | Low | High | Medium to high (design and config effort remains) |
| Transactions for cart-to-order | Local, simple | Cross-service workflow | Limited to a function or its database |
| Payment/shipment failure handling effort | Required | Required, plus inter-service failures | Required, plus platform retries |
| Independent scaling | No | Yes | Yes (within quotas) |
| Cost predictability | High | Lower (fixed overhead) | Variable with usage |
| Lock-in | Low | Medium | High |
| Evidence for need in `CDC.txt` | Matches listed features | None stated | None stated |

## 3. Decision

**We select a layered modular monolith as the core architecture of CDC Shop**, conditional on WA-1 (reading (a) of "distributed system"). This is a decision for this design exercise, not one approved by a stakeholder.

The decision includes these elements:

1. **One deployable application** with explicit modules: identity and access, catalog, cart, orders, payment integration, shipment integration, and shop information/contact. Each module owns its data and exposes a defined interface; other modules do not access its tables directly even though the database is shared. Dependency rules are enforced by tests or build tooling.
2. **Runs as multiple instances** behind a load balancer, with state held in the database rather than in instance memory.
3. **Payment and shipping are treated as real distributed boundaries:**
   - a pending order is committed before any remote call, and no database transaction is held open across a remote call;
   - transaction 1 (checkout): the same transaction that creates the order also records a payment attempt and a payment-initiation outbox entry, so a crash after order creation cannot lose the intent to start payment (see section 3.1);
   - transaction 2 (payment confirmation): when a confirmed payment is received, a separate transaction records the payment result, updates the order state, and writes the shipment-request outbox entry;
   - idempotency keys on payment and shipment requests;
   - a transactional outbox with a background worker for payment initiation, shipment requests, and retries;
   - an inbox/unique event ID to make duplicate callbacks harmless;
   - a timeout is treated as "unknown", not "failed", and resolved by reconciliation with the provider;
   - carrier tracking updates are deduplicated and applied only as valid forward transitions, so a late event cannot move a shipment backwards;
   - separate order, payment-attempt, and shipment states with validated transitions (assumption A3).
4. **Orders store a snapshot** of product details and price (A4); authorization is enforced at the module that owns each resource, based on the authenticated identity and role (A5): customers see only their own orders, and merchants change only products they are permitted to manage.
5. **Evolution path:** modules with clean boundaries can be extracted into services, and event-driven edges (webhooks, tracking updates, scheduled reconciliation) may later move to serverless functions, if evidence justifies it.

**Not decided here:** programming language, framework, database product, hosting or cloud, payment gateway, and carrier. Nothing in the requirements supports a choice.

### 3.1 Recovery of payment initiation after a crash

The state model and mechanisms below follow assumptions A1 and A3; names are illustrative.

**Design.** When the customer submits the cart, one local database transaction (transaction 1 in section 3) writes:

1. the order in `PENDING_PAYMENT` with its line-item snapshots,
2. a payment attempt in `PENDING` with a stable idempotency key (derived from the order and attempt number, for example `pay-<orderId>-1`),
3. an outbox entry "initiate payment" for that attempt.

The transaction commits **before** any call to the payment gateway. A background worker then reads unsent outbox entries, calls the gateway with the idempotency key, and records the result.

**Crash scenarios**

| When the application crashes | What exists afterwards | Recovery |
|---|---|---|
| Before the transaction commits | Nothing: no order, no payment attempt | The customer's cart is unchanged; the customer retries checkout. No charge was possible. |
| After commit, before the worker sends the request | Order `PENDING_PAYMENT`, attempt `PENDING`, unsent outbox entry | Any instance's worker finds the unsent entry on restart or on its next polling cycle and sends the request. Nothing is lost because the intent was committed with the order. |
| After the gateway call, before the result is saved | Attempt still `PENDING` or `UNKNOWN`; the gateway may already have charged | The worker retries with the **same idempotency key**, so the gateway returns the original result rather than charging again. If the gateway offers a status lookup, the reconciliation job queries it by the key. A late webhook is handled by the normal confirmation path. |
| After payment confirmation, before the order is updated | Gateway reports success; CDC still shows `PENDING_PAYMENT` | The webhook is redelivered, and/or reconciliation queries the gateway; the idempotent handler runs transaction 2 (section 3): it records success once, updates the order, and writes the shipment-request outbox entry. |

**Supporting rules**

- Several instances may run workers, so outbox entries are claimed safely (for example by locking or by a status-and-lease column) and processing is idempotent; a rare double claim must be harmless because of the idempotency key.
- A reconciliation job periodically finds orders in `PENDING_PAYMENT` whose attempt has no definitive result after a threshold, and re-drives or queries the gateway. Persistent failures raise an alert.
- While the outcome is pending or unknown, the customer sees a "payment pending" order, and a second checkout for the same cart reuses the existing pending order instead of creating a new one.
- After an agreed expiry (policy A8, not yet defined), an unpaid order is cancelled; if a late success arrives afterwards, it must be reconciled (for example by refund or reinstating the order), which is a business decision.
- Gateway support for idempotency keys and status lookup is assumed (A1). If the chosen gateway lacks either, duplicate prevention and recovery need additional measures such as manual review; this must be verified when the gateway is selected.

## 4. Reasons

1. **Fit with the requirements.** The 25 user stories are conventional e-commerce features (accounts, catalog, cart, order, payment, tracking, merchant product management). A single application covers them without service-to-service infrastructure.
2. **No stated need for the overhead of microservices.** `CDC.txt` gives no scale, availability, team-independence, or release-independence requirement. Microservices would add separate deployments, databases, a broker, a checkout saga, and cross-service tracing, while the hardest problems (payment and shipment failure handling) remain.
3. **Serverless does not remove the hard parts.** The core flows are request/response with transactional steps, which gain little from functions. It carries the highest lock-in and debugging cost, and the cloud and traffic profile are unknown. Its strengths remain available later at the edges. It also overlaps with microservices (see section 2.3), so it is no way around their boundary and consistency costs if the system is split into independent, data-owning pieces.
4. **Simple, local transactions where they matter.** Two separate local transactions cover the checkout flow. The first creates the order, the payment attempt, and the payment-initiation outbox entry together, before any gateway call. The second runs later, when the confirmed payment arrives, and records the payment result, updates the order state, and queues the shipment request together. The gateway call between them is never inside a database transaction, so no distributed transaction is needed.
5. **Reduced risk under uncertainty.** Many facts are unknown (provider behavior, traffic, policies). The cheapest architecture to change is a well-modularized monolith; module seams preserve the option to extract services.
6. **Honest handling of "distributed system".** Under WA-1, reading (a) is satisfied through multiple instances and genuinely distributed integrations. Reading (b) is not satisfied; this is stated openly rather than hidden, and the decision is revisited if (b) is required.

## 5. Consequences

### 5.1 Positive

- Fastest route to a working system, with the least infrastructure to run.
- Consistent CDC-owned data and straightforward end-to-end testing.
- Low lock-in and predictable cost.
- Retains the option to extract services or add serverless edges later.

### 5.2 Negative

- Application deployed and scaled as a whole; a defect or resource exhaustion in one module can affect others.
- A single database is a shared dependency and potential bottleneck.
- Module boundaries require discipline and automated checks; otherwise coupling grows.
- Does not satisfy reading (b).

## 6. Risks and mitigations

### 6.1 Key risk: the meaning of "distributed system"

This is the largest risk to the decision, because the whole decision depends on WA-1, an interpretation that `CDC.txt` does not confirm and that no stakeholder has confirmed.

- **What the risk is:** `CDC.txt` calls CDC Shop "a distributed system" but does not define it. If the assignment or stakeholders mean reading (b), CDC's own capabilities must be independently deployable, and a single-deployment modular monolith would **not** meet that requirement.
- **Why we still select the monolith:** nothing else in `CDC.txt` (scale, availability, teams, release independence) supports the cost of services, and reading (a) is consistent with the text because CDC integrates external payment and shipping systems. This is a judgement under uncertainty, not a verified fact.
- **Likelihood and impact:** likelihood is unknown. Impact is high if (b) is intended, because the decision would not satisfy the requirement and the architecture would need to change from the outset, not only later.
- **How it is reduced:**
  - ask the instructor or requirement owner to confirm the reading when possible (open question 1); until then the status is Accepted only conditionally on WA-1;
  - keep strict module boundaries, module-owned data, and interface-based provider integrations so that selected modules (for example payment or shipment, the most natural candidates) can be extracted as services with limited rework;
  - run multiple instances, so reading (a) is genuinely met;
  - define the revisit triggers in section 7.
- **If (b) is confirmed, or CDC's own business capabilities must be independently deployable services:** this decision must be revisited and this ADR superseded or revised, with microservices (or a first extraction of selected modules with the rest remaining modular) as the leading option. Serverless could be used to implement such services, since it can overlap with microservices.

### 6.2 Risk table

| Risk | Impact | Mitigation |
|---|---|---|
| "Distributed system" means reading (b) | Decision does not meet the requirement | See section 6.1: seek confirmation when possible; if (b), revisit and consider microservices or early extraction of selected modules |
| Crash after order creation loses the payment request | Customer has an unpaid order that never progresses | Order, payment attempt, and payment-initiation outbox entry commit together; worker re-drives unsent entries; reconciliation sweep (section 3.1) |
| Duplicate charge or shipment from retries or duplicate callbacks | Financial and customer harm | Idempotency keys, unique event IDs, validated state transitions, reconciliation |
| Order stuck after payment or shipment timeout | Unpaid or unshipped orders | "Unknown" state, scheduled reconciliation, alerts on stuck orders, operational repair procedure |
| Payment succeeds but shipment cannot be created | Paid order not fulfilled | Retry via outbox, visible exception state, defined refund/compensation policy (A8) |
| Module boundaries erode | Hard to extract or change later | Enforce dependency rules in tests, restrict cross-module data access, review boundaries periodically |
| Single point of failure or scaling limit | Outage or slowness under load | Multiple instances, health checks, database backups and failover, load testing; extract hot modules if needed |
| Assumptions A1–A8 prove wrong | Rework of integrations or state model | Confirm early with stakeholders; keep provider integrations behind interfaces |
| Unauthorized access to merchant functions or other customers' data | Data exposure, price tampering | Role and resource-level checks in each module, server-side validation, security tests |

## 7. Revisit triggers

Revisit this decision if any of these occurs:

- Reading (b) of "distributed system" is confirmed, or CDC's own business capabilities are required to be independently deployable services. This invalidates WA-1 and therefore the decision.
- Load or availability targets show that one deployment cannot meet them.
- Parts of the system need different release cadences or are owned by separate teams.
- A module (for example catalog browsing or payment processing) has very different scaling or reliability needs.
- Traffic proves highly bursty and managed functions would be clearly cheaper to run.

## 8. Open questions

### 8.1 Question that could invalidate the decision

1. What does "distributed system" mean here: reading (a) or (b)? If (b), the decision must be revisited (sections 6.1 and 7). Until answered, the decision rests on WA-1.

### 8.2 Implementation questions

These do not change the choice of architecture style. They affect design details, provider integrations, and policies, and can be answered later without revisiting the decision, unless an answer reaches a revisit trigger in section 7 (for example, very high load or availability targets in question 8).

2. Which payment gateway is used, and is confirmation synchronous or by webhook? Are refunds, cancellations, and retries in scope?
3. Which shipping provider or fulfilment model, and how are tracking updates received?
4. When is an order created relative to payment, and does shipment wait for confirmed payment? Should customers see one order status, or separate order, payment, and shipment statuses (A3)?
5. Is inventory tracking or stock reservation required? Can orders be split into several shipments?
6. What retry limits and order expiry rules apply after failed or unknown payments?
7. One merchant or several, and must a merchant manage only their own products?
8. Expected traffic, peaks, latency and availability targets, budget, team size and skills, and hosting constraints?
9. Authentication details: identity provider, MFA, session length, revocation.
10. How much does portability matter?

## 9. Component overview (illustrative)

```text
 Customer / Merchant clients (web)
              |
        [ Load balancer ]
              |
 +----------------------------------------------+
 |  CDC application (N instances, one codebase) |
 |                                              |
 |  API / presentation layer                    |
 |  +----------+ +---------+ +------+ +-------+ |
 |  | Identity | | Catalog | | Cart | | Order | |
 |  +----------+ +---------+ +------+ +-------+ |
 |  +---------+ +----------+ +----------------+ |
 |  | Payment | | Shipment | | Shop info /    | |
 |  | module  | | module   | | contact        | |
 |  +---------+ +----------+ +----------------+ |
 |  Background worker: outbox (payment          |
 |  initiation, shipment), retries,             |
 |  reconciliation                              |
 +----------------------+-----------------------+
                        |
                 [ Database ]  (local transactions + outbox/inbox)

 External: payment gateway <--(request, webhook)--> Payment module
           carrier         <--(request, tracking)--> Shipment module
```

## 10. Change log

| Version | Date | Change |
|---|---|---|
| 1 | 2026-10-28 | First draft, status Proposed |
| 2 | 2026-10-28 | Added section 6.1 on the "distributed system" risk (impact, mitigation, what changes if reading (b) is confirmed). Added section 3.1 on recovery of payment initiation after a crash (single-transaction order, payment attempt and outbox entry; crash scenarios; reconciliation); payment initiation added to the outbox in the decision and diagram, plus a new risk row. Clarified that serverless overlaps with microservices (section 2.3, comparison table, reasons). Comparison table, diagram, and technology-neutral approach retained; status remains Proposed. |
| 3 | 2026-10-28 | Full consistency review against the Task 1 notes; no contradictions found. Small fixes only: aligned serverless operational complexity in the comparison table with Task 1 ("Medium to high"); added carrier tracking-update handling and the role of identity (A5) to the decision; linked A3 to the Task 1 state model; added the single-status-versus-separate-statuses question to open question 4; reworded reason 1 ("without service-to-service infrastructure") and shortened the repeated serverless/microservices point in reason 3. Section 3.1 kept in place (see TASK2_ADR_NOTES.md). Status remains Proposed. |
| 4 | 2026-10-28 | Final submission version. Removed "draft 3, under review" from the status field (status remains **Proposed**); linked `CDC.txt` in the sources row; renamed the first change-log column from "Draft" to "Version". Markdown structure and internal links checked. No changes to content or decision. |
| 5 | 2026-10-28 | Fixed an inconsistency in reason 4: checkout creation and payment initiation use one transaction; confirmed payment and shipment scheduling use a separate, later transaction. Decision item 3 now labels the two transactions. Rest of the ADR checked for similar transaction-scope wording (sections 2, 3.1, 9 and diagram) and found consistent. Status remains Proposed. |
| 6 | 2026-10-28 | Final review. Status changed from Proposed to **Accepted** for this design exercise, conditional on new working assumption WA-1 (reading (a) of "distributed system"), which is stated to be our assumption and not confirmed by any instructor or stakeholder; an Approval row states that no external approval exists. Decision wording changed from "propose" to "select"; section 6.1, the risk table, reason 6, and revisit triggers updated to remove "before Accepted" wording and to state that the decision must be revisited if CDC's own capabilities must be independently deployable. Open questions split into 8.1 (could invalidate the decision) and 8.2 (implementation questions). Section 3.1 now references transactions 1 and 2. Comparison table, diagram, and technology-neutral approach unchanged. |

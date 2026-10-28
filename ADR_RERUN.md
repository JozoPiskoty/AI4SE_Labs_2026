# ADR-RERUN: Start CDC Shop with a Layered Modular Monolith

| Field | Value |
|---|---|
| Status | Proposed |
| Approval | No stakeholder approval recorded; none is claimed |
| Date | 2026-10-28 |
| Scope | Recommend an initial application architecture for CDC Shop and record conditions that could invalidate the recommendation |
| Sources | [CDC requirements](./Tasks/data/CDC.txt), [Task 1 architecture discussion](./TASK1_RERUN_NOTES.md), [Task 2 ADR process notes](./TASK2_RERUN_NOTES.md) |

## 1. Context

CDC Shop requirements describe customer and merchant interactions with accounts, products, carts, payment, and order/package information. They specify user-visible capabilities but little about operational or deployment constraints. This ADR records a conditional recommendation for the design exercise; it does not claim stakeholder approval or resolve the source's ambiguous system description.

### 1.1 Requirements stated in the source

- The system is described as “a distributed system that handles the management, the payment and the shipment of products,” particularly hardware-store materials.
- Customer stories request registration, login/logout, profile access, product listing/details, price sorting, name search, cart viewing and changes, cart payment, order/package information, About Us, and shop contact.
- Merchant stories request login/logout, profile access, product listing/details, price sorting, name search, product insertion/removal, price changes, and About Us.

### 1.2 What the source does not state

The source does not define deployment topology, hosting, cloud provider, traffic, availability, latency, team or budget, data policies, authentication details, payment/shipping providers, inventory behavior, order/payment/shipment states, payment failure/refund policy, carrier tracking integration, or exact package information. In particular, it does not define what “distributed system” means.

### 1.3 Ambiguous term

| Reading | Meaning | Effect on this decision |
|---|---|---|
| A. Internal services | “Distributed” requires multiple independently deployable internal services. | A modular monolith would not meet this reading. The recommendation must be revisited; microservices may be more appropriate if independent service deployment is indeed required. |
| B. Overall system boundary | The shop participates in a distributed environment, such as by communicating with separate payment or shipping systems, while its own application may remain one deployment. | A modular monolith remains viable; remote integrations still need explicit failure and recovery handling. |
| C. Broad description | “Distributed” is descriptive and does not prescribe deployment topology. | The phrase does not establish a need for microservices; the listed features can be organized as modules in one application. |

**Working assumption for this recommendation only:** Reading B or C applies. This is not a confirmed requirement or a resolution of the ambiguity. If Reading A is confirmed, this ADR's selection is invalidated and must be reconsidered.

### 1.4 Assumptions

| # | Assumption | Needs confirmation |
|---|---|---|
| A1 | An initial release can be one application deployment with internal account, catalog, cart/order, payment, and shipment-information modules. | Yes — especially against Reading A of “distributed system.” |
| A2 | A shared application database is acceptable for the initial design. | Yes — data ownership, consistency, and scale constraints are unspecified. |
| A3 | Payment and shipment may involve remote providers, but no provider or integration behavior is selected here. | Yes — the requirements do not identify external systems. |
| A4 | If remote payment/shipment calls exist, pending state, durable intent, idempotent retry, and reconciliation are needed for safe operation. | Yes — workflow and provider capabilities are unspecified. |
| A5 | Customers should be restricted to their own profile/order data, and merchants to authorized product-management actions. | Yes — the stories imply roles but do not define authorization policy. |
| A6 | Purchased item details should be preserved as an order-time snapshot. | Yes — order-line fields and price-change behavior are not specified. |

### 1.5 Decision drivers

- Meet the stated customer and merchant workflows without assuming deployment or scaling needs that are absent from the source.
- Keep shared catalog behavior consistent for customers and merchants.
- Limit deployment and operational complexity while keeping explicit module boundaries.
- Preserve a path to revise service boundaries if the distributed-system interpretation or future operating constraints require it.
- Treat payment and shipment failures as independent remote-system concerns, not as problems solved by the application architecture alone.

## 2. Alternatives considered

### 2.1 Layered modular monolith

**Description:** One application deployment, organized into technical layers and business modules, with a shared application database. Modules communicate in-process. Remote providers, if any, remain outside local database transactions.

**Pros:** The catalog can serve both roles consistently; a shared database can simplify local consistency; one deployment has fewer service coordination and operations concerns.

**Cons:** It does not satisfy a strict requirement for independently deployable internal services. Individual capabilities cannot be independently released or scaled, and one release can affect multiple capabilities.

### 2.2 Microservices

**Description:** Independently deployable services own capabilities and data, communicating through APIs and possibly events.

**Pros:** Could satisfy Reading A if independently deployed internal components are required; can allow capability-level deployment/scaling and clearer data ownership when those needs are real.

**Cons:** The source does not establish a need for independent service deployment or scaling. Cross-service checkout requires explicit workflow states, retries, and recovery; service discovery, authorization, observability, testing, and operations add complexity.

### 2.3 Serverless / event-driven

**Description:** Managed functions handle requests and events; queues or event infrastructure coordinate asynchronous work. Serverless is an execution model and event-driven is a communication style, so this alternative can overlap with microservices.

**Pros:** Could reduce server management and absorb bursts; queues can separate immediate responses from longer-running payment/shipment work.

**Cons:** No hosting, traffic, or asynchronous-response requirement establishes that the benefits are needed. Retries, duplicate/delayed events, provider-specific coupling, monitoring, local testing, and variable costs require attention. This style does not itself settle business-service boundaries.

### 2.4 Overview comparison

| Criterion | Layered modular monolith | Microservices | Serverless / event-driven |
|---|---|---|---|
| Deployment | **Assumption:** One application deployment | **Assumption:** Multiple independently deployed services | **Assumption:** Managed functions and services |
| Data | **Assumption:** Shared application database | **Assumption:** Service-owned data stores | **Assumption:** Managed shared or capability-owned stores |
| Operational complexity | Lower service coordination; module discipline still needed | Higher deployment, network, authorization, and observability overhead | Less server management, but event operations, retries, replay, and provider integration |
| Transactions | Local transaction can span modules; never includes remote calls | No ordinary transaction across service databases; workflow/saga needed | Local store transaction may be possible; no transaction spans remote calls or asynchronous handlers |
| Failure handling | Application handles remote outcomes; fewer internal network boundaries | Partial cross-service failures and remote outcomes | Duplicate, delayed, retried events and remote outcomes |
| Independent scaling | **Assumption:** Usually application-level | **Assumption:** Per service | **Assumption:** Per trigger/function, within provider limits |
| Evidence of need in source | Shared customer/merchant capabilities fit modules; topology is not established | Only if “distributed” means internal independently deployable services | Payment/shipment could be asynchronous, but no asynchronous, cloud, or traffic requirement is stated |

## 3. Decision

**Status: Proposed.** For this design exercise, recommend starting with a **layered modular monolith**, conditional on Working Assumption A1 and Reading B or C in Section 1.3. Keep business modules explicit so future extraction remains possible, but do not introduce independent service deployments or event infrastructure solely because the source uses the phrase “distributed system.”

This status remains **Proposed** because the meaning of “distributed system” and other decision-critical constraints have not been confirmed. No stakeholder acceptance is recorded.

### Not decided here

- Whether the application uses any particular programming language, framework, database, hosting platform, cloud provider, message broker, or payment/shipping product.
- Whether payment or shipment is implemented internally or integrated with external providers.
- Detailed APIs, database schema, deployment environments, capacity targets, and release process.
- Final identity/authentication mechanisms, privacy/retention policy, inventory rules, and refund/compensation policy.
- Whether future service extraction is required or warranted.

### 3.1 Critical recovery/failure design

If remote payment or shipment integrations exist, use durable local intent and explicit state transitions; never keep a database transaction open across a remote call.

1. **Transaction 1:** Persist the order, a pending payment attempt, and an outbox entry for the payment request together in one local database transaction. If this transaction fails, no provider call is made.
2. A worker claims the outbox entry with a safe lease/lock and calls the provider outside the transaction using a stable idempotency key derived from the order/payment attempt.
3. **Transaction 2:** When a response or callback is processed, record the provider result, advance the payment/order state only through a valid transition, and write any next outbox entry (such as shipment scheduling) in the same local transaction.
4. If shipment scheduling fails after payment succeeds, preserve the paid state and a shipment-pending/failed state; retry and reconcile. Refund or compensation policy is not specified and must not be inferred.

| Failure point | Required handling |
|---|---|
| Before Transaction 1 commits | No durable order/payment intent exists; return/report the local failure and do not call the provider. |
| After Transaction 1 commits but before the request is sent | The outbox remains available for a worker to retry; alert/reconcile if it remains stuck. |
| Provider acts but the response is lost or times out | Treat the result as unknown, retry with the same idempotency key where supported, and query/reconcile provider status rather than assuming failure. |
| Confirmation arrives but the state update has not committed | Process the callback/event again safely; unique event IDs and idempotent state transitions prevent duplicate effects. |
| Shipment fails after payment | Keep payment and shipment states distinct; retry/reconcile shipment. Do not silently roll payment back; the refund/compensation policy remains open. |
| Late success arrives after local expiry/cancellation | Do not move state backward. Reconcile against provider status and apply an explicitly defined exception/refund policy. |
| Multiple workers process outbox records | Claim work with a safe lease/lock and make processing idempotent; prevent simultaneous attempts from creating duplicate business effects. |

## 4. Reasons

- **Compared with microservices:** The source lists workflows but does not state independent deployment, data ownership, or per-capability scaling. A modular monolith supports the listed shared catalog/account/cart/order behavior with fewer assumed network and operational boundaries. Microservices would be selected instead if Reading A or concrete independent-service needs are confirmed.
- **Compared with serverless/event-driven:** The requirements do not say that checkout should be asynchronous, that demand is bursty, or that managed cloud execution is preferred. A monolith can still use durable outbox processing for remote integration reliability without adopting event-driven infrastructure as the system-wide design. Serverless/event-driven may be reconsidered if operational and workload evidence supports it.
- The recommendation does not remove distributed failure concerns: remote payment or shipment outcomes remain uncertain after timeouts and require explicit recovery.

## 5. Consequences

### Positive

- **Assumption:** Fewer deployment units and in-process module boundaries reduce initial coordination overhead.
- **Assumption:** A shared local database can simplify consistency across the catalog, cart, and order modules.
- The recommendation remains conditional and explicitly records the point at which the distributed-system ambiguity would invalidate it.

### Negative

- The monolith may not comply with Reading A; confirming that reading requires reconsideration before treating this ADR as accepted.
- **Assumption:** Capabilities cannot be independently deployed/scaled, and a shared application release may affect multiple roles.
- Outbox processing, idempotency, state transitions, and reconciliation still add implementation and operational work if external integrations exist.

## 6. Risks and mitigations

### 6.1 Key risk: “distributed system” requires internal services

| Risk | Why it matters | Likelihood | Impact | Mitigation | What changes if Reading A is confirmed |
|---|---|---|---|---|---|
| The source may require independently deployable internal services. | The recommended monolith would fail a top-level architecture constraint. | Medium — wording is explicit but topology is undefined. | High — decision may be invalid. | Keep status Proposed; ask the requirement owner to clarify before acceptance or implementation. | Reopen the decision; assess microservices against actual service ownership and operations constraints. Do not treat this ADR as satisfying Reading A. |

### 6.2 Other risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Modules become tightly coupled and the codebase loses boundaries. | Medium | Medium | Enforce module ownership and interfaces; review dependencies between modules. |
| A remote payment call times out after the provider has acted. | Medium if a provider is used | High | Use stable idempotency keys, unknown states, provider status reconciliation, and safe retries. |
| Outbox processing is duplicated or remains stuck. | Medium if outbox is used | Medium/High | Claim entries safely, make handlers idempotent, monitor age/failure, and reconcile. |
| Payment succeeds but shipment handling fails or arrives late. | Medium if shipping integration exists | High | Keep payment and shipment states separate; retry and reconcile; define support and refund/compensation policy. |
| Customer/merchant permissions are insufficiently defined. | Unknown | High | Confirm authorization rules and enforce them at the application module that owns each operation. |

## 7. Revisit triggers

- The requirement owner confirms Reading A for “distributed system.”
- Independent deployment, scaling, data ownership, or fault isolation becomes a confirmed need.
- Availability, latency, recovery, workload, or team/operations constraints make this deployment model unsuitable.
- Payment or shipping provider behavior requires an asynchronous or separately owned workflow that materially changes the design.
- Module coupling, release coordination, or scaling measurements show that the monolith no longer meets confirmed needs.

## 8. Open questions

### 8.1 Could invalidate the decision

- Status remains **Proposed** until the topology and decision-invalidating constraints below are clarified; this recommendation is not accepted.
- What does “distributed system” require: independently deployed internal services, external-system integration, deployment across machines, or no specific topology?
- Are independent release, scaling, or failure-isolation boundaries required?
- Are there availability, latency, recovery, data ownership, hosting, or operational constraints that rule out one application deployment?

### 8.2 Implementation questions

- Which payment and shipping providers, if any, are in scope, and do they support idempotency and status lookup?
- What package information must customers see, and how is it obtained?
- What are the order, payment-attempt, and shipment states, including late success, cancellation, failure, and refund/compensation behavior?
- What inventory rules, order-item snapshot fields, merchant permissions, authentication, and data-retention requirements apply?
- What traffic profile, monitoring, reconciliation schedule, support process, and cost targets apply?

## 9. Component overview

The diagram shows the conditional monolith proposal. External provider integrations are assumptions, not confirmed requirements. Local transaction boundaries are shown explicitly; remote calls occur between transactions.

```text
 Customer UI             Merchant UI
      \                       /
       +---- Application API / presentation ----+
                    |                            |
        +-----------+----------------------------+
        |           |            |               |
   Accounts      Catalog      Cart/Orders    Order query
        |           |            |               |
        +-----------+------------+---------------+
                    |     shared application DB
                    |     (order + payment attempt
                    |      + payment outbox: Tx 1)
                    |
             Outbox worker
                    | remote call (outside Tx 1/2)
                    v
          Payment provider (if used)
                    |
          response/callback/event
                    v
        Payment integration module
                    |
                    | Tx 2: record result + valid state
                    | transition + shipment outbox
                    v
           Shipment worker/module
                    | remote call (if carrier used)
                    v
            Carrier (if used)
                    |
        package information update
                    v
               shared application DB
                    |
                    +---- Order query ----> Customer UI
```

## 10. Change log

| Version | Date | Change |
|---|---|---|
| 0.1 | 2026-10-28 | Initial proposed recommendation and conditional ADR based on the Task 1 discussion. |

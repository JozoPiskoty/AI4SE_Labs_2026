# Task 1 — CDC Shop Architecture Discussion Notes

## Scope and requirements reviewed

- **Project:** CDC Shop, described as a distributed system for managing, paying for, and shipping hardware-store products.
- **Customer capabilities:** register, log in/out, view a profile, browse and inspect products, search by name, sort by price, manage a shopping cart, pay for the cart, check package/order information, contact the shop, and view the About Us page.
- **Merchant capabilities:** log in/out, view a profile, browse and inspect products, search and sort products, and add, remove, or change product prices.
- **Task 1 goal:** discuss three distinct architectural proposals in depth, including trade-offs and implementation challenges. All three have now been discussed.
- **Scope boundary:** no ADR or Skill is being created as part of this discussion.

**Reading guide:** the consolidated summary is in the section "Consolidated Summary (Final)" at the end of this file. The "Discussion record" below is the chronological log of the conversation; status lines in it describe the state at that point in time.

## Discussion record

### Opening request

The user asked to begin Task 1 by reviewing `CDC.txt` and `Task_1.md`, confirming the system requirements, presenting only the first architecture, and then pausing for the user's response. Notes should be maintained in English throughout the discussion.

### Architecture 1 — Layered modular monolith

**Status:** Discussed; summarized below before beginning Architecture 2.

#### Concept

A modular monolith is one application deployed as a single unit, internally organized into clearly separated business modules. A layered structure separates the user-facing/API layer, application/business logic, and persistence/integration code. Modules can initially share a deployment and database while keeping their responsibilities and interfaces explicit.

This is different from splitting each business capability into independently deployed services: the first proposal keeps the core CDC Shop application together, while allowing external providers such as payment or shipping systems to remain separate integrations.

#### Possible CDC Shop structure

- **Presentation/API layer:** customer and merchant web pages or clients, plus API endpoints.
- **Identity and access module:** registration, login/logout, profiles, and customer/merchant permissions.
- **Product catalog module:** product listing/details, name search, price sorting, and merchant product creation, removal, and price changes.
- **Cart module:** current cart and adding/removing items.
- **Order module:** converting a cart into an order and exposing order/package status to the customer.
- **Payment integration:** communicates with an external payment gateway; the application should not store raw card details.
- **Shipment integration:** connects order information with a shipping provider or shipment-management capability and makes tracking information available.
- **Shop information/contact module:** About Us content and customer contact requests.
- **Persistence layer:** database access owned by the application, with clear boundaries between modules even if one database is used initially.

#### Example request flow: checkout

1. The customer submits the current cart for checkout through the presentation/API layer.
2. The order logic validates the cart and records an order with a stable identifier and an initial status.
3. The payment integration requests payment from the external gateway, using that identifier to correlate the result.
4. On confirmed payment, the order is marked paid and shipment handling is initiated.
5. The customer later reads the order and available package/tracking information through the order-facing API.

The actual CDC requirements do not specify payment-provider behavior, shipping-provider APIs, inventory quantities, or detailed order states; these would need clarification before implementation.

#### Advantages

- One deployment and a relatively straightforward development and operations setup.
- Clear internal separation can keep identity, products, carts, orders, payment, and shipment concerns understandable.
- A single database can make basic operations and consistency easier to implement than coordinating several service databases.
- Easier to develop and test end-to-end flows such as cart checkout and merchant price updates.
- Modules create seams for later extraction if evidence shows a genuine need to deploy or scale a capability independently.

#### Disadvantages and trade-offs

- The application is still deployed as one unit; a failure or problematic release can affect the whole shop.
- Modules may become tightly coupled unless boundaries, ownership, and dependency direction are enforced.
- Scaling one heavily used capability independently is difficult; the entire application may need to scale together.
- This may not fully realize the description's “distributed system” if that wording requires CDC's own business capabilities to be independently distributed. External payment and shipping integrations alone do not make the application internally distributed.
- A shared database is simpler initially but can undermine module boundaries if modules freely read and modify each other's tables.

#### Challenging implementation details

- Define module ownership and API boundaries, particularly between cart, order, payment, and shipment.
- Make checkout resilient to retries and delayed/duplicate payment callbacks; use idempotent operations so retries do not create duplicate orders or charges.
- Decide the order/payment status transitions and what happens when payment fails or shipment creation fails.
- Preserve order history if a merchant later changes or removes a product; order records may need snapshots of product name and price at purchase time.
- Enforce authorization on every merchant operation and ensure merchants can only manage products they own, if the business model includes multiple merchants.
- Avoid exposing partially completed checkout state when data changes or external calls fail.
- Agree how shipment tracking data is obtained and refreshed, because the requirement only says customers should see package information.

#### Questions raised for discussion

1. Does a single deployable application with external payment and shipping integrations feel consistent with the brief's description of CDC as a “distributed system,” or should CDC's own business capabilities be independently deployable from the beginning?
2. Is ease of initial development/operation more important here than independent scaling and deployment of capabilities such as payments or shipments?
3. Which part of the checkout flow or module boundaries would you like to examine more closely?

#### Current conclusion

No architecture has been selected. This was the first proposal for discussion only.

### Follow-up: Does a modular monolith fit a distributed system?

**User question:** Does a modular monolith fit CDC Shop's requirement as a distributed system? What are the main trade-offs, and what must be clarified about payments, shipping, or order processing?

**Discussion response:**

- The requirements describe CDC as a “distributed system,” but do not define what that means operationally or require CDC's business capabilities to be separate services.
- A modular monolith can still be hosted across distributed infrastructure (for example, multiple application instances behind a load balancer) and can integrate with external payment and shipping providers. That interpretation is compatible with a modular monolith.
- If “distributed system” specifically means independently deployable CDC services for capabilities such as catalog, orders, payments, and shipping, then a single-deployment modular monolith does not meet that stricter interpretation. External provider integrations alone do not make CDC's own application services independently distributed.
- The modular monolith favors simpler development, deployment, data consistency, and end-to-end testing. Its trade-offs are coupled release and scaling, shared runtime failure impact, and the risk that module boundaries weaken. Independently deployed services can provide deployment and scaling autonomy, but introduce network failures, distributed data consistency, service observability, and more operational overhead.
- Based on the supplied requirements alone, independently deployed business services are not explicitly mandated. Whether the modular monolith is acceptable depends on the intended meaning of “distributed”; this should be confirmed with the assignment stakeholder or treated as an explicit assumption.

**Domain clarifications to resolve before detailed design:**

1. **Payments:** Which payment gateway is expected? Is payment synchronous or confirmed asynchronously by callbacks/webhooks? Are refunds, cancellations, or payment retries in scope? The design should avoid storing raw card data and should define how duplicate or delayed confirmations are handled.
2. **Shipping:** Is CDC integrating with a carrier, managing shipment fulfillment itself, or only displaying package information? How are shipment creation and tracking updates received, and which shipment states must customers see?
3. **Order processing:** When is an order created relative to payment? What are the required order/payment/shipment states and transitions, and what should happen when payment succeeds but shipment creation fails (or vice versa)? Is inventory/stock tracking or reservation required, and can an order be split into multiple shipments?
4. **Consistency and recovery:** Which operations must be immediately consistent, and which may complete asynchronously? What customer-visible status should be shown while payment or shipping confirmation is pending?

**Open questions for the user:**

- Should “distributed system” mean CDC's own business capabilities must be independently deployable, or is a scalable application integrated with external payment/shipping systems sufficient?
- Are payment gateway, carrier integration, inventory management, or split shipments specified elsewhere, or should they remain assumptions/out of scope for this discussion?

**Status at the time:** Architecture 1 remained under discussion; no architecture decision was made.

### Follow-up: Checkout implementation and failure handling

**User question:** Explain how the modular monolith's modules interact from cart submission through payment confirmation and shipment tracking. Cover database transactions, duplicate payment callbacks, retries, payment/shipping failures, difficult implementation details, and architectural limitations.

**Illustrative checkout flow:**

1. **Submit and validate:** The customer-facing API authenticates the customer and asks the Cart/Checkout logic to submit the current cart. The application reloads authoritative product prices and any stock information rather than trusting client-supplied values. It validates that the cart can still be purchased.
2. **Create a durable pending order:** In one local database transaction, the application writes an order and order-line snapshots (product name/identifier and agreed unit price), records the initial payment/order state, and marks the cart as submitted or associates it with the order. The transaction commits before making a network call to the gateway. This makes the order durable if the application stops immediately afterward.
3. **Request payment:** After commit, the Payment integration calls the gateway with the order identifier as a correlation key and a gateway-supported idempotency key. A synchronous gateway result can update payment state; an asynchronous result is delivered later through a callback/webhook. The application should return a pending or action-required response to the customer as appropriate rather than pretending payment is complete.
4. **Process confirmation exactly-once in effect:** A webhook handler verifies the provider's signature and expected order/amount/currency. In a short local transaction, it inserts the provider event/transaction identifier into a uniquely constrained inbox or payment-event table and applies the permitted state transition. A duplicate event hits the uniqueness constraint and has no second business effect. The handler responds successfully only after it has durably accepted the event; its work must be safe to repeat.
5. **Schedule shipment after payment:** In the same database transaction that marks payment successful, the application writes a shipment-request message to a transactional outbox. A background worker reads unsent outbox rows and calls the shipping provider, using a stable idempotency/reference key. It retries transient failures with bounded exponential backoff and jitter; permanent failures are surfaced for operational attention. The worker records success/provider shipment ID or a visible failure state.
6. **Track shipment:** Carrier callbacks or periodic polling update shipment/tracking records through validated, deduplicated state transitions. The customer order view reads the latest persisted shipment status and tracking reference. Out-of-order carrier events should not move an order backward to an invalid state.

**Transaction boundaries and consistency:**

- A relational database transaction can atomically commit CDC-owned records (order, payment state, cart state, and outbox row). It cannot atomically include a payment gateway or carrier API call.
- Do not hold a database transaction open while waiting on remote provider calls. Long network delays increase lock contention and cannot roll back a remote charge.
- The outbox closes the local “state committed but event not scheduled” gap; an inbox/deduplication record closes the duplicate callback processing gap. Delivery is generally at-least-once, with idempotent handlers providing exactly-once business effect rather than relying on exactly-once network delivery.
- Suggested states must be agreed with the business, but might include `PENDING_PAYMENT`, `PAYMENT_FAILED`, `PAID`, `SHIPMENT_PENDING`, `SHIPPED`, `DELIVERED`, and an explicit shipment/payment exception state. Avoid treating payment and shipment as one overloaded status.

**Retries and failure cases:**

- **Timeout while creating payment:** The result may be unknown, not failed. Re-query the gateway or safely retry with the same idempotency key; do not create a fresh payment attempt blindly.
- **Duplicate/delayed payment callback:** Deduplicate on the provider's stable event/transaction ID, validate amount and order association, and allow only legal state transitions. A late success after a timeout should reconcile the order rather than charge again.
- **Payment declined:** Persist a failed/declined outcome and allow a deliberate retry policy. Keep the order/cart behavior clear so the customer can retry without losing items or accidentally creating multiple active orders.
- **Payment succeeds but CDC crashes before recording it:** The gateway may resend its webhook; deduplication plus reconciliation/query APIs should recover the state. Periodic reconciliation is prudent because callbacks can be delayed or lost.
- **Payment succeeds but shipment request fails:** The order remains paid and shipment-pending/exception; retry the outbox work. Do not silently mark the order failed or ask the customer to pay again. If shipment cannot be fulfilled permanently, an operational/manual resolution or refund/compensation policy is needed.
- **Shipment API accepts request but response times out:** Retry with the same provider idempotency/reference key or query by that key to avoid creating duplicate shipments.
- **Outbox worker repeatedly fails:** Keep the message and attempts visible, alert/monitor persistent failures, and use an operational dead-letter/repair procedure rather than dropping it.

**Most difficult details:**

- Defining an authoritative order/payment/shipment state machine and permitted transitions.
- Handling uncertain outcomes from network timeouts without duplicate charges or shipments.
- Building idempotency and reconciliation across providers with different capabilities and retention windows.
- Designing transactional outbox/inbox processing, concurrency control, worker scheduling, and safe replay.
- Deciding inventory reservation and expiry behavior, if stock management is required (not specified in CDC.txt).
- Maintaining immutable order-line price/details even when merchants edit or remove catalog products.
- Operational visibility: tracing an order across API requests, webhooks, background jobs, payment provider, and carrier; alerting on stuck states and giving support staff a recovery process.

**Architecture limitations for CDC:**

- The application modules share deployment and usually a database, so changes and releases are coupled and independent scaling is limited.
- A process-wide outage or resource exhaustion can affect catalog, checkout, and merchant management together, even if the database/provider systems are separate.
- The monolith's local transactions simplify CDC-owned consistency, but external payment/shipping boundaries still require asynchronous workflows, idempotency, and reconciliation; the monolith does not eliminate distributed-systems failure modes.
- Strong module boundaries require discipline and tests. Shared database access or shortcuts can create hidden coupling and make later service extraction difficult.
- If CDC is explicitly required to have independently deployed business services, this architecture does not satisfy that requirement without a later redesign or extraction.

**Status at the time:** This deepened Architecture 1 only. The checkout design is illustrative, not a confirmed CDC requirement; provider behavior, stock rules, status semantics, retry/refund policy, and operational ownership remain to be clarified.

### Follow-up: Proposed order, payment, and shipment state model

**User question:** Propose a clear state model; explain success/failure, timeouts, duplicate callbacks, and shipment failures; separate stated requirements from assumptions; and explain trade-offs before moving to another architecture.

#### Requirements explicitly present in `CDC.txt`

- A customer can pay for the current shopping cart.
- A customer can check an order to see information about their package.
- The system description says CDC manages payment and shipment of products.
- Merchants can add/remove products and change prices.

`CDC.txt` does **not** specify order creation timing, inventory, payment-provider behavior, refunds/cancellations, shipment-provider integration, status names, status transitions, or fulfillment failure policy.

#### Proposed model (design proposal, not stated requirement)

Keep three related but separate state machines. This avoids overloading one status with payment and fulfillment meaning.

**Order lifecycle**

- `PENDING_PAYMENT` — order and immutable line-item/price snapshot created; payment is not yet confirmed.
- `READY_FOR_FULFILLMENT` — payment is confirmed; order is accepted for fulfillment.
- `FULFILLMENT_IN_PROGRESS` — shipment has been created or is in transit.
- `COMPLETED` — shipment is confirmed delivered.
- `CANCELLED` — order will not be fulfilled. Before payment this can be terminal directly; after payment it must not be terminal until the required refund/compensation is resolved.

Shipment exceptions do not erase the fact that payment succeeded or automatically cancel the order. The order can remain in fulfillment progress while the shipment is retried or resolved. The order’s displayed status can be derived from its payment and shipment records; avoid duplicating derived states unless a business-facing order status is needed.

**Payment lifecycle**

- `PENDING` — payment attempt created/requested, no definitive result yet.
- `SUCCEEDED` — gateway has authoritatively confirmed payment.
- `FAILED` — gateway has authoritatively declined/failed this attempt.
- `UNKNOWN` — outcome cannot currently be determined (for example, request timed out and gateway status lookup is unavailable); operationally treat it like pending and reconcile rather than assuming failure.
- `REFUND_PENDING` / `REFUNDED` — optional states only if refunds are in scope.

Each payment attempt has its own ID and gateway reference; a failed attempt does not overwrite the history of later attempts. Only a successful payment moves an order to `READY_FOR_FULFILLMENT`.

**Shipment lifecycle** (created only after confirmed payment, under this proposal)

- `NOT_REQUESTED` — no shipment request should yet be made.
- `REQUEST_PENDING` — payment succeeded and shipment creation is queued or being retried.
- `CREATED` — carrier/fulfillment provider confirmed a shipment and supplied a tracking reference.
- `IN_TRANSIT` — tracking indicates the package is moving.
- `DELIVERED` — carrier/fulfillment confirmation says delivered.
- `EXCEPTION` — shipment creation or transit has a failure requiring retry or human action.
- `CANCELLED` — optional, only if cancellation/return flows are defined.

Carrier event ordering and allowed transitions must be checked so a delayed `IN_TRANSIT` event cannot move a delivered shipment backward.

#### Transition and failure behavior

1. **Cart submitted:** create order `PENDING_PAYMENT`, payment attempt `PENDING`, shipment `NOT_REQUESTED`, and a durable payment request/outbox item. Never create a shipment before payment is confirmed under this proposal.
2. **Payment confirmed:** verify order, amount, currency, and provider event; atomically record the event, mark the attempt `SUCCEEDED`, set order `READY_FOR_FULFILLMENT`, and enqueue shipment creation. Duplicate callbacks are deduplicated by a unique provider event/transaction ID and cannot repeat the transition or create a second logical shipment request.
3. **Payment definitively declined:** mark that attempt `FAILED`; order remains `PENDING_PAYMENT` while a retry is permitted. If retry is not allowed or the order expires, a separate `CANCELLED`/expired outcome would be needed. Expiry and retry limits are not specified and must be agreed.
4. **Payment request times out:** set/retain `UNKNOWN` (or `PENDING` if the provider can still resolve it). Query the gateway or retry with the same idempotency key. Do not start a fresh payment attempt or tell the customer payment failed until the gateway outcome is reconciled. A late successful callback takes the normal success transition.
5. **Payment success recorded but the process crashes before shipment call:** a transactional outbox committed with the payment transition ensures a worker can send it later. Retries reuse a stable shipment idempotency/reference key.
6. **Shipment request times out:** the provider may have accepted it. Query by reference or retry with the same idempotency key; do not make a new uncorrelated shipment.
7. **Shipment created / tracking begins:** update shipment to `CREATED` then `IN_TRANSIT` as provider evidence arrives; update the order to `FULFILLMENT_IN_PROGRESS`. On confirmed delivery, set shipment `DELIVERED` and order `COMPLETED`.
8. **Shipment definitively fails:** record `EXCEPTION`, keep payment `SUCCEEDED` and order in fulfillment progress, expose an appropriate pending/issue message, retry transient failures, and alert/support for permanent failures. Any cancellation/refund/compensation is a business policy requiring explicit rules and provider support; it must not silently reverse payment state.
9. **Shipment tracking updates:** persist deduplicated carrier events and apply valid forward transitions. The customer order/package view reads the latest shipment status and tracking details.

#### Important trade-offs and assumptions

- **Separate state machines vs. one order status:** three dimensions clarify what happened and allow payment to remain successful while shipment is blocked. The cost is more records, combinations, and UI mapping; a derived customer-facing summary is useful.
- **Asynchronous fulfillment vs. synchronous checkout:** a durable queued shipment request avoids holding checkout open on a carrier, but customers may see `SHIPMENT_PENDING` after paying.
- **Do not assume exactly-once delivery:** providers and networks may retry. Durable deduplication, idempotency keys, and reconciliation provide exactly-once business effect where provider capabilities permit; if a provider lacks idempotency/query support, duplicate prevention and recovery are harder and may need manual review.
- **Shipment-after-payment:** proposed to avoid shipping unpaid orders, but CDC does not state this rule. If fulfillment or stock reservation begins before payment, different states and compensation rules are needed.
- **Failure/cancellation/refund semantics:** the state model deliberately leaves order expiry, refund timing, cancellation rights, and retry limits unresolved because they are not in the supplied requirements.
- **Monolith limitation remains:** transactions can atomically persist CDC's order/payment state and outbox row, but not atomically commit with a remote gateway or carrier. Provider ambiguity and eventual status updates still require distributed-systems techniques.

**Open question for the user:** Does this split into order, payment-attempt, and shipment state machines make the checkout outcome clear, or would you prefer a simpler single customer-facing order status with these details hidden? Should shipment creation explicitly wait for confirmed payment, as assumed here?

**Status at the time:** Architecture 1 remained under discussion. The proposed statuses and policies are assumptions for analysis, not requirements from `CDC.txt`.

### Architecture 1 — Summary of pros and cons

**Advantages**

- One main application to build, deploy, monitor, and test; this is a practical starting point for the requirements supplied.
- Modules organize identity, catalog, cart, orders, payment, and shipment while allowing CDC-owned records to be updated in local database transactions.
- A shared deployment and usually a shared database make basic operations and end-to-end flows simpler than coordinating many services.
- Clear module boundaries can provide seams for later extraction if real scaling or organizational needs arise.

**Disadvantages**

- The application is deployed and scaled as a unit; teams cannot release or scale catalog, checkout, or shipping code independently.
- A serious application-wide outage, resource issue, or faulty release can affect several shop capabilities.
- Developers must protect module boundaries; unrestricted cross-module code or database access can turn it into a tightly coupled codebase.
- Remote payment and shipping calls still fail independently, so the monolith still needs idempotency, retries, reconciliation, and asynchronous handling.
- If “distributed system” specifically means CDC's business capabilities must themselves be independently deployable, the modular monolith does not satisfy that interpretation.

**Overall trade-off:** favor implementation and operational simplicity over independent deployment and scaling. It is not a decision for CDC; the intended meaning of “distributed system” remains a requirement to clarify.

### Architecture 2 — Microservices

**Status at the time:** Introduced; awaiting user discussion.

#### Concept in simple terms

Instead of one application containing all the modules, split CDC into several small applications called services. Each service owns a business capability, runs as a separately deployable process, and communicates with other services over the network using APIs or messages.

An everyday analogy: the monolith is one shop team with departments working in the same building and shared records. Microservices are separate specialist teams, each with its own systems; they coordinate by sending requests or messages. This gives each team more independence, but coordination takes more work.

#### Possible CDC services and infrastructure

- **API gateway / web frontend:** the customer and merchant clients enter through a common endpoint. It routes requests to the right service and may handle cross-cutting concerns such as request limits; authentication and authorization still need clear ownership.
- **Identity service:** registration, login, profiles, and issuing/verifying identity tokens and role claims.
- **Catalog service:** product listing/details, search and sorting, plus merchant product updates.
- **Cart service:** each customer's current cart and item changes.
- **Order service:** order creation, order-line snapshots, and customer-facing order status.
- **Payment service:** payment attempts, gateway calls/callbacks, and reconciliation.
- **Shipment service:** shipment requests, tracking references, and carrier updates.
- **Message broker:** durable asynchronous messages such as `OrderSubmitted`, `PaymentSucceeded`, or `ShipmentCreated`, so a service can continue work without the sender waiting for every downstream service.
- **Separate data stores:** each service owns its data and exposes it through its API or events. Other services should not directly read or write its database.
- **Operations foundation:** service discovery/routing, centralized logs/metrics/traces, health checks, secure secrets/configuration, deployment automation, and alerting. These are essential supporting capabilities, not optional extras at scale.

#### Example checkout flow

1. The gateway routes the customer's checkout request to the Order service.
2. The Order service obtains the relevant cart/product information through service APIs or previously maintained data projections, then stores a pending order in its own database.
3. It publishes `OrderSubmitted` to the broker.
4. The Payment service consumes that event and asks the payment provider to charge the customer. It later publishes a success or failure result.
5. On `PaymentSucceeded`, the Order service updates the order; the Shipment service consumes the event and requests a carrier shipment.
6. Shipment status events update the customer-visible order view, either through the Order service or a read/API composition layer.

This flow is asynchronous: the checkout response may say the order is pending while payment and shipping progress. Each consumer needs idempotent event handling because brokers commonly redeliver messages. A service's database change and outgoing event need a reliable pattern such as a transactional outbox; event IDs/inboxes and reconciliation help prevent duplicate business effects.

#### Advantages

- Catalog, checkout, payments, and shipping can be deployed and scaled independently.
- A failure in one service can sometimes be isolated, allowing unaffected capabilities to continue (for example, browsing products may remain available during a shipment-service outage), if dependencies and failure handling are designed well.
- Each service can have focused ownership and a data model suited to its responsibility.
- The architecture explicitly distributes CDC's own business capabilities, which may align better if that is what the assignment means by “distributed system.”
- Services can evolve or use different technologies when justified, although unnecessary technology variation increases operational complexity.

#### Disadvantages and trade-offs

- A local transaction cannot atomically update multiple services' databases. Workflows become eventually consistent: the user may see “payment pending” or “shipment pending” rather than an immediately completed checkout.
- Every network call can time out, fail, be duplicated, or arrive late; services need explicit retries, idempotency, timeouts, circuit breaking where appropriate, and reconciliation.
- Checkout can become a distributed workflow/saga. If payment succeeds but fulfillment cannot proceed, compensating actions (such as refunding) and manual recovery need policy and implementation.
- More deployments, databases, message infrastructure, service contracts, security boundaries, and monitoring create substantial setup and operating cost.
- Debugging a customer issue requires correlating activity across services and asynchronous events. Local development and automated end-to-end testing are also more involved.
- Service boundaries and data ownership are difficult to choose. Too many tiny services cause excessive coordination; overly broad services recreate a monolith distributed over the network.
- Independent scaling/deployment is valuable only if CDC has meaningful scale, release, reliability, or team-ownership needs to justify it.

#### Difference from Architecture 1

- **Modular monolith:** internal module calls are usually in-process; one deployment and often one database; local transactions can cover related CDC data.
- **Microservices:** modules become separate networked services, usually each owning its database; deployments are independent, but cross-service work is asynchronous or coordinated over the network.
- Both can have logical domain boundaries and external payment/shipping integrations. The key distinction is independent process/deployment and data ownership, not merely naming code modules “services.”

#### Assumptions and open questions

- CDC.txt does not mandate separate databases, a message broker, a specific cloud, or independent service deployment. Those are proposals in this architecture, not stated requirements.
- A useful initial boundary is identity, catalog, cart, orders, payments, and shipments, but this may be too many services for a small project; grouping capabilities is a valid design choice.
- It remains unknown whether the project needs the independent scaling/availability of microservices or whether “distributed” only describes external integrations and deployment infrastructure.
- Payment-provider and carrier behavior, stock management, expected load, availability goals, team size, deployment capability, and refund/compensation policy would affect whether the added complexity is justified.

**Questions for the user:**

1. Does the service-by-service checkout flow make sense, particularly why payment and shipment may remain pending after the initial checkout request?
2. Which benefit seems most valuable for CDC: independent deployment/scaling, or keeping development and failure recovery simpler?
3. What concerns do you have about having a database per service and communicating through a broker?

**Status at the time:** Architecture 2 under discussion; no architecture selected.

### Follow-up: Microservice failures and inconsistent checkout data

**User response and request:** The proposed checkout flow makes sense. Simpler development seems important from the current requirements, although CDC is described as a distributed system. Explain microservice failure and consistency challenges with an example, update the notes, and finish discussing Architecture 2 before introducing the third architecture.

#### Why failures are harder across services

- Each service has its own process, network connection, and data store. A request can time out even if the remote service completed the work, and services can be unavailable independently.
- There is no single database transaction that covers order, payment, and shipment databases. A workflow may succeed in one service and fail before the next service records the result.
- Messages may be delivered more than once, delayed, or handled out of order. Consumers must deduplicate and validate state transitions.
- A service outage can block dependent steps even while unrelated capabilities remain available. For example, customers might still browse a catalog while checkout cannot confirm payment or schedule shipment.
- Retries alone are not sufficient: they need limits/backoff, idempotency, durable messages, monitoring, and a way to reconcile uncertain provider outcomes. Repeated retries without idempotency can create duplicate charges or shipments.

#### Simple failure example

1. The Order service stores order `O-42` as `PENDING_PAYMENT` and emits `OrderSubmitted`.
2. The Payment service charges the customer successfully and records `SUCCEEDED`, but then crashes before its `PaymentSucceeded` event reaches the broker (or before that event is durably published).
3. The Order service still shows `PENDING_PAYMENT`, even though the customer has been charged. The Shipment service has not seen a paid order and has not created a shipment.
4. The customer may retry checkout, risking a second charge unless the same order/payment attempt is idempotent and the UI clearly reports a pending result.
5. Recovery requires durable publication (for example, a transactional outbox at the Payment service), broker redelivery, idempotent event consumers, and/or reconciliation that queries the payment provider and repairs the order state. After the order is reconciled to paid, shipment creation can proceed.

The reverse partial failure is also possible: the Shipment service requests a carrier shipment and the carrier accepts it, but CDC times out before recording the response. A naive retry can create a duplicate shipment. A stable carrier idempotency key/reference and a lookup/reconciliation path are needed.

#### Handling the order/payment/shipment consistency gap

- Treat each service's own database as authoritative for its data; do not make direct cross-service database writes.
- Use durable event publication with a transactional outbox so a committed state change cannot be separated from its outgoing event.
- Make event handlers idempotent, retain processed event/transaction IDs, and validate allowed state transitions.
- Model checkout as a long-running workflow (often called a saga): payment and shipment progress independently, and order status can reflect `PAYMENT_PENDING`, `PAID`, `SHIPMENT_PENDING`, or an exception instead of pretending all steps changed atomically.
- Reconcile against provider records and expose stuck/exception states to operational staff. If payment succeeded but fulfillment permanently cannot proceed, a defined compensation such as a refund may be needed; it must be policy-driven and itself can fail or be delayed.
- Provide correlation IDs and tracing across API requests, messages, services, and provider calls so support can find the complete history of an order.

#### Trade-off for CDC

Microservices offer genuine independent deployment and scaling and may isolate some failures, which could fit a strict interpretation of “distributed system.” However, the current user stories do not establish the traffic scale, independent team ownership, uptime objectives, or service-level independence that would justify this complexity. For the listed capabilities, simpler development and local consistency may be more valuable unless the assignment clarifies a requirement for independently distributed CDC services.

That conclusion is only a discussion observation, not an architecture selection: whether the phrase “distributed system” demands microservices remains open. CDC's payment and shipping integrations still introduce distributed failure modes even with a modular monolith, but internal microservices add more service-to-service boundaries to operate.

**Status at the time:** Architecture 2 failure and consistency challenges discussed.

### Follow-up: Separate databases per microservice

**User question:** Explain how separate databases for each microservice would work in CDC Shop, with a simple example and the main pros and cons.

#### How database ownership works

In the database-per-service pattern, each service owns its data and is the only service allowed to read or change that service's database directly. The database may be a separate server or a separate logical database/schema, depending on deployment needs; the important rule is ownership and access through the service boundary, not necessarily different database technology.

For CDC, for example:

- Catalog service owns product descriptions and current prices.
- Cart service owns customer carts and their selected product IDs/quantities.
- Order service owns orders and purchase-time line-item snapshots.
- Payment service owns payment attempts and provider references.
- Shipment service owns shipment records and tracking events.

If Order needs a product price, it asks Catalog through an API or consumes catalog events to keep a local read projection. It does not query Catalog's database. Likewise, a customer order page may get order data from Order and tracking data from Shipment through APIs or a read model; it does not join their tables directly.

#### Simple checkout example

1. The Cart service stores a cart containing product `P-7`, quantity 2.
2. During checkout, the Order service obtains the authoritative current product information from Catalog, then writes order `O-42` and purchase-time unit-price snapshots in its own database.
3. The Payment service records its payment attempt in its database and communicates with the gateway. The Shipment service later records the shipment and tracking data in its own database.
4. If the merchant changes the current price of `P-7` after checkout, Catalog's current price changes, but the order's saved purchase-time price remains unchanged. This is intentional historical data, not an accidental duplicate.
5. To show the customer the order and tracking information together, the application composes responses from Order and Shipment or maintains a read model updated by events. Because updates travel asynchronously, tracking may temporarily show “not yet available.”

#### Advantages

- Each service has clear ownership and can evolve its schema without coordinating direct database changes with every other service.
- A service can choose storage that suits its own needs and can scale or back up its data independently, if justified.
- A failure or heavy load in one database need not directly exhaust another service's database, though dependent workflows can still be affected.
- No shared database becomes a hidden integration API. Service boundaries are reinforced, and direct cross-service coupling is reduced.
- Services can optimize their own queries or maintain read projections without exposing internal tables.

#### Disadvantages and trade-offs

- Cross-service joins and atomic multi-service transactions are unavailable. Data needed across boundaries must be fetched through APIs or deliberately copied into projections.
- API composition adds latency and can fail if a dependency is unavailable; projections avoid some synchronous dependencies but can be stale.
- Intentional duplication requires clear ownership and update rules. For example, current catalog price belongs to Catalog, whereas the price actually paid belongs to the Order snapshot.
- Schema changes become service-contract and event-versioning changes when other services depend on the data.
- More databases mean more provisioning, migrations, backups, access control, monitoring, restore procedures, and operational cost.
- Debugging inconsistent views requires tracing event delivery and projection lag. Teams need reconciliation and repair tools.
- It is easy to split too early: for a small CDC project, separate databases can add substantial complexity without a demonstrated scaling or ownership benefit.

**Key rule:** Copying data is acceptable when the copy has a defined purpose and owner (such as an order price snapshot or a search/read projection). Directly reading or writing another service's database is not; it bypasses that service's rules and makes schema changes risky.

**Status at the time:** Database-per-service detail added to Architecture 2.

### Follow-up: Service communication and operational overhead

**User question:** Explain synchronous calls and asynchronous messages with simple CDC examples; compare the deployment, monitoring, and testing work with a modular monolith; assess whether the complexity is justified for CDC Shop.

#### Synchronous communication (request/response)

One service sends a request to another service and waits for its response, commonly through HTTP/REST or gRPC.

- **CDC example:** when a customer opens a product detail page, the web/API layer asks Catalog for the product and waits for its response.
- **Advantages:** direct and intuitive interaction; the caller can use the result immediately; easy to understand for simple queries.
- **Costs:** the caller depends on the other service being reachable and responsive. Slow calls add latency; timeouts leave uncertain outcomes; chains of calls can multiply latency and failure risk. Use timeouts, bounded retries where safe, circuit breaking/bulkheads as appropriate, and avoid retrying non-idempotent operations blindly.
- **Good fit:** immediate reads or decisions where a response is required now, provided the dependency and latency are acceptable.

#### Asynchronous communication (messages/events)

One service publishes a message to a broker or durable queue and does not wait for each consumer to finish. A consumer processes it later and can publish another event or update its own data.

- **CDC example:** Order publishes `OrderSubmitted`; Payment consumes it and contacts the gateway; after confirmation, Payment publishes `PaymentSucceeded`; Shipment consumes that and requests the carrier. Checkout can return a pending order while these steps continue.
- **Advantages:** sender and receiver need not be online at the same time; a durable broker can absorb temporary outages; the sender does not wait for a long downstream workflow.
- **Costs:** results arrive later; messages can be duplicated, delayed, or reordered; teams need idempotent consumers, event versioning, dead-letter/repair procedures, monitoring of queue lag, and reconciliation. Use an outbox/inbox pattern to avoid losing the relationship between local database commits and messages.
- **Good fit:** long-running workflows such as payment confirmation and shipment creation, where eventual completion is acceptable.

In practice CDC would use both: synchronous calls for a product lookup or a customer order-status query, and asynchronous messages for payment and shipment workflows. The decision should be per interaction rather than “everything synchronous” or “everything asynchronous.”

#### Additional operational work versus a modular monolith

- **Deployment:** each service needs a build artifact, configuration, secrets, health checks, rollout/rollback procedure, network routing, and compatible API/event contracts. A shared release is simpler in a monolith; coordinated changes across services need compatibility planning.
- **Infrastructure and security:** services, databases, broker, service discovery/routing, identity between services, certificates/permissions, backups, and migrations all need provisioning and lifecycle management. Local development also needs a workable way to run or substitute dependencies.
- **Monitoring and support:** logs, metrics, traces, and correlation IDs must span HTTP calls and asynchronous messages. Teams need alerts for service health, error rates, payment/order state stuckness, broker backlog, and consumer failures, plus procedures to replay or repair work. A monolith usually has fewer process and network boundaries to observe.
- **Testing:** unit tests remain useful, but services also need contract tests, integration tests against databases/broker/provider adapters, and end-to-end tests across deployments. Test environments must reproduce or safely simulate network failures, duplicate/out-of-order messages, timeouts, and partial success. These are more involved than testing in-process module interactions, though a monolith still needs provider-integration and failure tests.

#### Is this justified for CDC?

Based only on `CDC.txt`, the extra microservice complexity is **not yet justified by demonstrated needs**: the file lists customer/merchant capabilities and describes payment and shipment handling, but gives no independent scaling targets, team boundaries, deployment cadence, availability objectives, load profile, or explicit requirement that CDC's own capabilities be separate deployable services.

If “distributed system” is an explicit requirement for independent CDC services, that could justify microservices despite the cost. Otherwise, external payment and shipping integrations can be handled from a well-structured modular monolith, which still must handle external timeouts and callbacks but avoids adding service-to-service boundaries. This is a provisional assessment, not an architecture selection; clarify the meaning of “distributed system” and operational constraints before deciding.

**Status at the time:** Architecture 2 communication and operational overhead discussed.

### Follow-up: Choosing service boundaries and cross-service identity

**User questions:** How should CDC decide which capabilities become separate services, can there be too many, and how should customer/merchant login and permissions work across services?

#### Deciding service boundaries

- Start with business capabilities and cohesive rules/data, not one service per screen, user story, database table, or CRUD operation. Candidate CDC areas include catalog, cart, order, payment, and shipment, but the list is a starting hypothesis rather than a required split.
- Separate a capability when there is a concrete benefit such as independently scaling a bottleneck, deploying it on a different cadence, isolating a meaningful failure/security boundary, or assigning it to a team that can own it end to end.
- A service should have a clear responsibility, authoritative ownership of its data, and a stable contract for other services. If two proposed services must constantly call each other or change together, they may belong together.
- Consider consistency needs: tightly coupled operations that need frequent atomic updates are harder to separate because service boundaries replace local transactions with network workflows and eventual consistency.
- Consider operational readiness: CDC needs teams and infrastructure capable of deploying, monitoring, securing, and supporting each service. Avoid splitting until the benefits outweigh that overhead; a modular monolith can preserve candidate boundaries while evidence accumulates.

#### Risks of too many services

- More deployments, databases, network calls, message contracts, permissions, alerts, and failure modes to operate.
- More coordination and versioning: a simple customer flow can cross many services, increasing latency and the number of dependencies that can fail.
- “Distributed monolith” risk: services are nominally separate but must be released together or make synchronous calls in lockstep, losing the independence that justified the split while retaining operational complexity.
- Harder local development, testing, debugging, and end-to-end incident recovery.
- A useful check is whether each service can be owned, deployed, monitored, and changed with meaningful independence. If not, combine it with a closely related capability.

#### Login and permissions across services (proposed approach)

- Distinguish **authentication** (establishing who the user is) from **authorization** (deciding what that identity may do).
- A centralized Identity service or established identity provider handles registration/login and issues a signed, short-lived access token after successful authentication. The token can contain a stable user ID and role claims such as `customer` or `merchant`; clients send it with requests.
- Each service verifies the token's signature, issuer, audience, and expiry, then enforces authorization for its own operations. Services should not trust a role or user ID supplied only in request parameters or by the UI.
- Role checks alone are not sufficient for merchant data: Catalog must also check that the authenticated merchant owns or is authorized to edit the specific product. Order must restrict customer order reads to the owning customer. These resource-level rules belong at the service that owns the resource.
- For service-to-service calls, use workload/service identities and narrowly scoped permissions; a service should not inherit the customer's authority automatically. If a call acts on a user's behalf, propagate validated identity context or use a defined token-exchange/delegation mechanism, with the receiving service still applying its own rules.
- Short token lifetimes reduce exposure but make logout, account disablement, role changes, and immediate revocation more complicated. Possible approaches include short-lived access tokens with revocable refresh sessions, token version/revocation checks for sensitive actions, or provider introspection; each adds complexity/latency. Do not place secrets or sensitive personal data in readable token claims.
- CDC.txt requires customer and merchant login/profile use but does not specify roles beyond those actors, an identity provider, token format, multi-factor authentication, session duration, or revocation policy. These are design assumptions requiring security and product decisions.

**Status at the time:** Architecture 2 service boundaries and identity discussed.

### Architecture 2 — Summary of pros and cons

**Advantages**

- CDC capabilities can be independently deployed and scaled, if that independence is valuable.
- Failure isolation can let unrelated capabilities continue, when dependencies and fallbacks are designed carefully.
- Services own focused business responsibilities and data, which can support clear team ownership and independent evolution.
- The architecture explicitly distributes CDC's own capabilities, if that is what “distributed system” means in the assignment.

**Disadvantages**

- Cross-service workflows cannot use one local database transaction; checkout needs asynchronous coordination, visible pending states, idempotency, retries, and reconciliation.
- Network failures, duplicate/out-of-order messages, and partial success create more failure cases to design for.
- Separate deployments, databases, brokers, security boundaries, observability, and contract testing increase development and operational effort.
- Poor boundaries or too many services can create a “distributed monolith,” with high coordination cost but little real independence.
- CDC's supplied requirements do not demonstrate independent scale, team ownership, uptime, or deployment needs that would currently justify this overhead. The intended meaning of “distributed system” remains an open requirement.

**Overall trade-off:** independent deployment/scaling and potential isolation in exchange for considerably more coordination and operational complexity. No architecture has been selected.

### Architecture 3 — Serverless, event-driven architecture

**Status at the time:** Introduced; awaiting user discussion.

#### Concept in simple terms

In a serverless approach, CDC's application logic runs as small functions managed by a cloud platform rather than as one continuously running application server that the team operates. A function runs when something triggers it—for example, an HTTP request or a message—and the cloud provider handles much of the server provisioning and scaling.

“Serverless” does not mean there are no servers; it means CDC's team does not manage those servers directly. This proposal emphasizes managed function execution and event-triggered work. It can overlap with microservices: a microservice can itself be serverless. For comparison, this architecture is serverless-first and organized around managed functions/events, whereas Architecture 2 emphasized independently deployable long-running business services.

#### Possible CDC components

- **API gateway and web client:** route customer/merchant HTTP requests to the right functions.
- **Identity provider:** authenticate users; functions verify identity and enforce customer/merchant permissions.
- **HTTP functions:** handle product search/details, profile access, cart changes, merchant product maintenance, checkout initiation, and order queries.
- **Managed database:** persist products, carts, orders, payment state, and shipment state. Data ownership and transaction boundaries still need design; serverless does not automatically require a separate database per function.
- **Queue/event bus:** retain events such as `OrderSubmitted`, `PaymentSucceeded`, and `ShipmentStatusUpdated` and trigger background functions.
- **Payment and shipment adapter functions:** call external providers and process callbacks/events.
- **Managed operational services:** logs, metrics, tracing, secrets/configuration, alarms, and deployment automation.

#### Simple checkout example

1. The checkout HTTP function validates the customer/cart and writes a pending order and payment request to persistent storage. The database transaction/outbox or equivalent must durably connect the order write with scheduling the next step.
2. A queue event triggers a payment function, which calls the payment gateway using a stable idempotency key.
3. A gateway webhook triggers another function to validate and record payment confirmation.
4. That confirmation emits a shipment-request event; a shipment function calls the carrier and persists the tracking reference.
5. Carrier updates trigger functions that refresh shipment status, which the order-query function returns to the customer.

The customer may see a pending order while functions and provider callbacks complete. Functions can retry or run more than once, so handlers still need idempotency and state-transition checks.

#### Advantages

- The cloud platform handles much of server provisioning, patching, and automatic scaling of function execution.
- Functions can scale down when idle; usage-based pricing can be economical for intermittent or variable traffic (subject to provider pricing and workload).
- Event triggers fit asynchronous tasks such as payment callbacks, shipment updates, and background processing.
- Smaller handlers can be quick to deploy and independently scale by trigger or workload.
- Managed queues, databases, and identity services can reduce the amount of infrastructure CDC directly operates.

#### Disadvantages and trade-offs

- CDC is tied more closely to a cloud provider's function, event, identity, and monitoring model; portability may require abstraction or rework.
- Cold starts, execution time/memory limits, concurrency quotas, and provider-specific retry behavior can affect latency and implementation.
- A function can time out after an external side effect occurred but before saving the result; retries can duplicate charges or shipments unless idempotency and reconciliation are robust.
- Event-driven steps are asynchronous and eventually consistent; tracing an order across short-lived functions and queues can be harder than following a request through a monolith.
- The system still needs durable data, event schemas, state machines, retry/dead-letter handling, security, and operational dashboards. “Managed” infrastructure does not remove design or failure-handling work.
- Local development and integration testing can be difficult when behavior depends on cloud-specific triggers and services; provider emulators may not exactly match production.
- Pricing can become less predictable at sustained high usage or with chatty function-to-function calls; many small functions and events can also increase complexity.
- A serverless implementation can become fragmented into too many tiny handlers without clear domain ownership, reproducing the over-splitting problem.

#### Difference from the first two

- **Architecture 1 — Modular monolith:** one continuously running application deployment, internally modular; often one database and local calls/transactions.
- **Architecture 2 — Microservices:** multiple independently deployed business services, often long-running, each owning data and communicating over APIs/messages.
- **Architecture 3 — Serverless/event-driven:** application behavior is executed by provider-managed functions triggered by HTTP or events, with managed platform services. It reduces server operations but not distributed coordination; it may be organized as functions around capabilities and can overlap with microservices rather than being mutually exclusive.

#### Assumptions and questions

- CDC.txt does not specify a cloud provider, expected traffic variability, event broker, serverless runtime, or a requirement to avoid server management. These are proposal assumptions.
- Need to clarify hosting constraints, data residency/security requirements, provider lock-in tolerance, expected/peak request volume, latency targets, and payment/carrier callback behavior.
- The order/payment/shipment state model, idempotency, and reconciliation discussed above still apply regardless of compute model.

**Questions for the user:**

1. Does the idea of functions being triggered by requests or events make sense, and does the checkout example clarify how the work proceeds?
2. Would reduced server management be valuable enough to accept cloud-provider dependence and more event-driven debugging?
3. Does CDC have a target cloud provider or requirements around traffic, latency, or portability?

**Status at the time:** Architecture 3 introduced for discussion; none selected.

### Follow-up: Serverless failures, duplicate events, cost, and maintainability

**User questions:** What happens if a payment function fails or the same event is processed twice? What could make serverless expensive or hard to maintain for CDC?

#### Example 1 — Payment function fails after charging

1. `OrderSubmitted` for order `O-42` triggers the payment function.
2. The function calls the gateway with idempotency key `pay-O-42-attempt-1`; the gateway charges the customer.
3. The function times out or crashes before saving `SUCCEEDED` and before emitting `PaymentSucceeded`.
4. The platform (or queue) retries the function. Because the same idempotency key is reused, the gateway returns the original result instead of charging again. The function then records `SUCCEEDED` and emits the event.
5. If retries are exhausted, the message goes to a dead-letter queue and an alarm fires. A scheduled reconciliation job queries the gateway for payments still `PENDING`/`UNKNOWN` and repairs the order.
6. Without the idempotency key, the retry would charge the customer twice. This is the central risk of retries in serverless.

#### Example 2 — Same event processed twice

1. Queues and event buses commonly provide at-least-once delivery, so `PaymentSucceeded` for `O-42` may reach the shipment function twice (a retry, a redelivery, or a duplicate webhook).
2. On each delivery the function first records the event ID in a table with a uniqueness constraint (inbox/dedup table), or uses a conditional write such as "create shipment only if none exists for `O-42`".
3. The second delivery fails that check and is acknowledged without side effects, so only one carrier shipment is requested.
4. The carrier call also carries a stable reference (`ship-O-42`) so a retry after a timeout does not create a second shipment.
5. State-transition checks also stop an old or late event from moving an order backward (for example, a delayed `IN_TRANSIT` after `DELIVERED`).

Key lesson: serverless does not provide exactly-once business effects; idempotency, deduplication, and reconciliation remain CDC's responsibility.

#### What could make serverless expensive

- **Sustained high traffic:** per-invocation pricing can exceed the cost of always-on servers for steady, predictable load.
- **Chatty designs:** many small functions calling each other, each billed for execution time while waiting on others or on slow providers (payment/carrier calls).
- **Retry storms and loops:** a faulty handler or poison message retried repeatedly multiplies invocations; a function triggering itself indirectly can create runaway cost.
- **Supporting services:** API gateway requests, queue/event operations, managed database capacity, logs/traces, data transfer, and NAT/VPC networking are often billed separately and can exceed function cost.
- **Provisioned concurrency** or reserved capacity (used to reduce cold starts) adds fixed cost.
- **Hard to predict:** usage-based bills depend on traffic patterns and implementation details; budgets and cost alarms are needed.
- CDC.txt gives no traffic profile, so whether the pay-per-use model is cheaper than a small always-on deployment cannot be determined from the requirements.

#### What could make it hard to maintain

- **Function sprawl:** many small functions with unclear ownership, duplicated code, and inconsistent conventions; shared libraries and versioning become a concern.
- **Hidden workflow:** business flow is spread across triggers, queues, and functions rather than visible in one call path; needs diagrams, documented state machines, and tracing.
- **Observability:** correlating logs and traces across short-lived functions and asynchronous events requires deliberate correlation IDs and tooling.
- **Local development and testing:** cloud triggers, permissions, and event delivery are difficult to reproduce; emulators differ from production; integration tests often need real cloud resources.
- **Platform limits:** execution time, payload size, memory, concurrency quotas, and cold starts may force design workarounds.
- **Configuration complexity:** infrastructure as code, permissions per function, secrets, and event wiring are themselves a significant maintenance surface; misconfigured permissions are a common security risk.
- **Vendor lock-in:** triggers, event formats, identity, and deployment tooling are provider-specific; migrating later can mean substantial rework.
- **Data consistency:** as with microservices, multi-step workflows are eventually consistent and need sagas/reconciliation. Sharing one database across functions is simpler but couples them; separate stores add overhead.

#### Assessment for CDC (provisional, not a decision)

CDC's stated features are fairly conventional and its traffic profile is unknown. Serverless could suit bursty or low-volume loads and background webhook/event handling, but offers no relief from the hardest problems (idempotent payment, shipment recovery, state modelling) and adds provider dependence and debugging difficulty. A hybrid, such as a modular monolith with a few event-triggered functions for webhooks and carrier updates, is one possibility worth keeping in mind.

**Status:** Architecture 3 follow-up recorded. No architecture is selected; no ADR or Skill created.

### Follow-up: When serverless fits CDC and how it compares

**User question:** Based on CDC's requirements, when is serverless a good choice, when is it unnecessarily complicated, and how does it compare briefly with Architectures 1 and 2?

#### What CDC.txt actually tells us

- Features are conventional e-commerce: accounts, catalog browsing/search/sort, cart, payment, order/package status, merchant product management, About Us and contact pages.
- It states nothing about traffic volume or spikes, latency targets, cloud provider, team size, budget, or availability goals. Conclusions below are therefore conditional.

#### When serverless would be a good choice for CDC

- **Bursty or unpredictable traffic:** for example, promotions or seasonal peaks with long quiet periods; pay-per-use and automatic scaling help.
- **Small team that does not want to operate servers:** managed functions, queues, database, and identity reduce infrastructure work.
- **Event-driven side work:** payment and carrier webhooks, shipment-status updates, contact-form handling, notification emails, and scheduled reconciliation jobs map naturally to small triggered functions.
- **Low or uncertain volume:** a small shop can avoid paying for always-on capacity.
- **Already committed to one cloud:** lock-in concern is less significant.

#### When it would be unnecessarily complicated

- **Steady, modest load:** a single small always-on application can be cheaper and simpler than a gateway, functions, queues, and event wiring.
- **Mostly CRUD flows:** catalog, cart, profile, and merchant product maintenance are request/response operations that gain little from event-driven decomposition; splitting them into many functions adds wiring without benefit.
- **Need for simple local development and easy debugging:** cloud-triggered functions are harder to run and test locally.
- **Portability or cost predictability required:** provider-specific services and usage-based billing work against this.
- **Strongly transactional logic:** cart-to-order conversion benefits from local database transactions, which are more natural in one application than across functions.
- **Team unfamiliar with serverless/event-driven operations:** extra learning, tracing, and permission management overhead.

#### Brief comparison

| Aspect | 1. Modular monolith | 2. Microservices | 3. Serverless / event-driven |
|---|---|---|---|
| Deployment unit | One application | Several independent services | Many managed functions plus managed services |
| Server operations | Team runs the application | Team runs services and infrastructure | Provider runs compute; team still owns design, IaC, permissions |
| Data and transactions | Often one DB; local transactions | Database per service; eventual consistency | Managed DB(s); transactions limited to what one function does; workflows eventual |
| Scaling | Whole app together | Per service | Automatic per function, within quotas |
| Failure handling at payment/shipping | Idempotency, retries, reconciliation still needed | Same, plus inter-service failures | Same, plus platform retries and at-least-once triggers |
| Development and debugging | Simplest | Hardest to coordinate | Hard locally; hidden event flow |
| Cost profile | Predictable, fixed | Highest fixed/operational | Low when idle; may rise at sustained load |
| Lock-in | Low | Medium | Highest |
| Fit with "distributed system" wording | Weak under strict reading | Strongest | Strong in execution model; depends on how functions/data are organized |

#### Provisional observations (not a decision)

- Serverless addresses server management and elastic scaling, not the hardest CDC problems: payment idempotency, shipment recovery, and the order/payment/shipment state model apply to all three architectures.
- Based on the stated requirements alone, serverless is most justified for the event-driven edges (webhooks, tracking updates, background jobs) and less justified for core request/response catalog and cart logic.
- This supports keeping a hybrid in mind: modular monolith core plus selected event-triggered functions. All architecture choices still hinge on clarifying what "distributed system" means and on expected traffic and operational constraints.

**Status:** Architecture 3 discussion extended with fit/non-fit conditions and comparison. No architecture selected; no ADR or Skill created.

---

## Consolidated Summary (Final)

This section consolidates the discussion above. No architecture has been selected, and no ADR or Skill has been created.

### A. Requirements stated in `CDC.txt`

- CDC Shop is described as "a distributed system that handles the management, the payment and the shipment of products", mainly hardware-store materials.
- **Customer stories (US 1–12, 23–25):** register, log in, access profile, see the current cart, sort products by ascending/descending price, search for a product by name, pay for the current cart, log out, check an order to see package information, access About Us, see the product list, see product details, contact the shop, add a product to the cart, and remove all items from the cart.
- **Merchant stories (US 13–22):** log in to the Merchant page, log out, access profile, change a product's price, insert/remove products, sort and search products, access About Us, see the product list, and see product details.
- Two actor types exist: Customer and Merchant.

### B. Not stated in `CDC.txt` (assumptions and unknowns)

Everything below was proposed by us during discussion and is **not** a stated requirement.

| Topic | What CDC.txt says | Our assumption or proposal |
|---|---|---|
| Meaning of "distributed system" | Only the phrase in the description | Two readings: (a) a deployed system integrating external payment/shipping providers, possibly on several instances; (b) CDC's own capabilities must be independently deployable. Unresolved. |
| Order creation and status model | Customer can pay and check order/package info | Separate order, payment-attempt, and shipment state machines (see Architecture 1 state model) |
| Shipment timing | Nothing | Shipment is created only after confirmed payment |
| Payment provider and callbacks | Nothing | External gateway; asynchronous confirmation by webhook; no raw card data stored; idempotency keys |
| Shipping provider | Nothing | External carrier or fulfilment provider with creation and tracking updates |
| Inventory and stock | Nothing | Not modelled; stock reservation would need new rules |
| Refunds, cancellation, retry limits, order expiry | Nothing | Policy undefined; compensation needed if payment succeeds but shipment cannot proceed |
| Merchant ownership of products | "Merchant" actor; no multi-merchant detail | Resource-level checks if several merchants exist |
| Order history after price change | Nothing | Order lines keep a snapshot of product name and price |
| Authentication and authorization | Login/logout for both actors | Identity provider issuing short-lived signed tokens with customer/merchant roles; MFA, session length, revocation unspecified |
| Traffic, latency, availability, budget, team size, cloud provider | Nothing | Unknown; many architecture trade-offs depend on them |

### C. Architecture 1 — Layered modular monolith

- **How it works:** one deployable application split into modules (identity, catalog, cart, order, payment integration, shipment integration, shop info/contact) with layers for API, business logic, and persistence; usually one database with local transactions.
- **Pros:**
  - Simplest to build, deploy, test, and monitor.
  - Local transactions cover CDC-owned data (order, payment state, cart, outbox).
  - Module boundaries leave seams for later extraction.
- **Cons:**
  - Deployed and scaled as a unit; a bad release or outage can affect all features.
  - Boundaries erode without discipline, and a shared database can hide coupling.
  - Does not satisfy the strict reading of "distributed system".
- **Main technical challenges:**
  - A database transaction cannot include the payment gateway or carrier calls. Do not hold a transaction open across remote calls.
  - Transactional outbox for shipment requests; inbox/unique event IDs for duplicate callbacks.
  - Timeouts mean "unknown", not "failed": reuse idempotency keys and reconcile with the provider.
  - Defining valid order/payment/shipment transitions and handling out-of-order carrier events.
  - Payment succeeded but shipment failed: keep order paid, retry, surface an exception, define a refund policy.
  - Order price/name snapshots and authorization on every merchant operation.

### D. Architecture 2 — Microservices

- **How it works:** separately deployed services (identity, catalog, cart, order, payment, shipment) behind an API gateway; each owns its data (database per service) and communicates by synchronous APIs and asynchronous events through a broker.
- **Pros:**
  - Independent deployment and scaling per capability.
  - Possible failure isolation (for example, browsing continues if shipment is down).
  - Clear ownership and data boundaries; the strongest fit for the strict "distributed system" reading.
- **Cons:**
  - No cross-service transaction; checkout becomes an eventually consistent saga with visible pending states.
  - More infrastructure: deployments, databases, broker, security, observability, contract testing.
  - Risk of a "distributed monolith" and too many services.
  - Not justified by anything in CDC.txt about scale, teams, or availability.
- **Main technical challenges:**
  - Partial failure example: payment charged but the event is not published, so the order stays pending and the customer may retry. Needs outbox, idempotent consumers, and reconciliation.
  - Carrier accepts a shipment but the response is lost: use a stable reference to avoid duplicates.
  - Data ownership: no direct cross-service DB access; intentional copies (order price snapshots, read projections) need clear owners and may be stale.
  - Choosing service boundaries from business capabilities, not screens or tables.
  - Login and permissions: token verification in each service, resource-level checks (merchant owns product, customer owns order), scoped service-to-service identity, and the revocation trade-off with short-lived tokens.
  - Tracing and correlation IDs across calls and events; contract and failure-scenario testing.

### E. Architecture 3 — Serverless, event-driven

- **How it works:** managed functions run on HTTP or event triggers behind an API gateway, using a managed database, queue or event bus, and identity provider. The provider handles servers and scaling.
- **Pros:**
  - Little server administration; automatic scaling, including down to idle.
  - A natural fit for webhooks, tracking updates, notifications, and scheduled reconciliation jobs.
  - Cost-efficient for low or bursty traffic.
- **Cons:**
  - Strongest provider lock-in; cold starts, execution limits, and quotas.
  - Hidden workflow across functions and queues; harder local testing and debugging.
  - Can be expensive at steady high load, with chatty functions, retry storms, or costly supporting services.
  - Function sprawl and permission/configuration overhead.
- **Main technical challenges:**
  - At-least-once delivery and platform retries: the payment function may charge and then fail before saving. Use idempotency keys, a dead-letter queue, and reconciliation.
  - Duplicate events: record event IDs (unique constraint) or use conditional writes, plus stable carrier references.
  - Out-of-order or late events must not move an order backwards.
  - The order/payment/shipment state model still applies; serverless does not remove it.
  - Observability across short-lived functions and cost control.
- **Fit for CDC:**
  - Good for bursty traffic, a small team that does not want to run servers, and event-driven edges such as webhooks and background jobs.
  - Unnecessarily complex for steady modest load, plain CRUD flows (catalog, cart, profile), strongly transactional cart-to-order logic, or teams needing simple local debugging or portability.

### F. Comparison table

| Aspect | 1. Modular monolith | 2. Microservices | 3. Serverless / event-driven |
|---|---|---|---|
| Deployment unit | One application | Several independent services | Many managed functions plus managed services |
| Server operations | Team runs the application | Team runs services and infrastructure | Provider runs compute; team owns design, permissions, deployment config |
| Data and transactions | Often one DB; local transactions | Database per service; eventual consistency | Managed DB(s); workflows across functions are eventual |
| Scaling | Whole application | Per service | Automatic per function, within quotas |
| Failure handling at payment/shipping | Idempotency, retries, reconciliation | Same, plus inter-service failures | Same, plus platform retries and at-least-once triggers |
| Development and debugging | Simplest | Hardest to coordinate | Hard locally; hidden event flow |
| Cost profile | Predictable | Highest operational cost | Low when idle; may rise under steady load |
| Lock-in | Low | Medium | Highest |
| Operational complexity | Lowest | Highest | Medium to high |
| Fit with strict "distributed system" reading | Weak | Strongest | Strong in execution model; depends on design |
| Fit with CDC.txt as written | Good for the listed features | No stated need for the overhead | Good for event edges; unnecessary for core CRUD |

### G. Key points common to all three

- Payment and shipping are external boundaries, so timeouts, duplicate callbacks, and partial failure exist in every architecture. The order/payment/shipment state model, idempotency, and reconciliation are needed regardless of the choice.
- Hybrids are possible, for example a modular monolith core with a few event-triggered functions for webhooks and tracking updates, or a monolith designed with seams for later extraction.

### H. Provisional observations (not a decision)

- On CDC.txt alone, the requirements are conventional and do not show the scale, team, or availability needs that would justify microservices.
- The decisive unresolved question is what "distributed system" means. If independently deployable CDC services are required, microservices become much more attractive; otherwise, a modular monolith, possibly with serverless edges, looks simpler.
- The choice and its rationale are deferred to the later ADR step.

### I. Open questions

1. What does "distributed system" mean for this assignment: independently deployable CDC services, or an application integrating external systems and running on distributed infrastructure?
2. Which payment gateway, and is confirmation synchronous or via webhook? Are refunds, cancellations, and retries in scope?
3. Which shipping provider or fulfilment model? How are tracking updates received, and what shipment states must customers see?
4. When is an order created relative to payment, and should shipment creation wait for confirmed payment?
5. Is inventory tracking or stock reservation required? Are split shipments possible?
6. What are the retry limits and order expiry rules after a failed or unknown payment?
7. Is there a single merchant or multiple merchants, and must a merchant manage only their own products?
8. Expected traffic, peaks, latency and availability targets, budget, team size and skills, and cloud or hosting constraints?
9. Authentication details: identity provider, MFA, session length, and revocation requirements.
10. How important are portability and avoiding provider lock-in?
11. Do we prefer a single customer-facing order status, or the three separate state machines proposed?

### J. Next steps

- Task 1 discussion of the three architectures is complete.
- ADR (Task 2) and Skill (Task 3) have not been started and will be created only on explicit request.

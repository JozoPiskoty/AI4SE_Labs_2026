# Task 1 Rerun — CDC Shop

## Requirements summary

### Scope and sources

This discussion concerns the CDC Shop requirements in `Tasks/data/CDC.txt`, following `Tasks/Task_1.md`. The system is described as handling management, payment, and shipment of products, particularly hardware-store materials. The source lists customer and merchant account/profile actions, product browsing and search, cart management, payment, order/package information, and shop information/contact.

### Requirements stated in the source

- The system is described as: “a distributed system that handles the management, the payment and the shipment of products”.
- The products are “materials that you can usually find in an hardware store.”
- Customer stories require registration, login, profile access, viewing a current cart, sorting products by ascending/descending price, name-based product search, paying for the current cart, logout, checking an order for package information, accessing About Us, viewing product lists and details, contacting the shop, adding a product to a cart, and removing all items from a cart.
- Merchant stories require login to the Merchant page, logout, profile access, changing product prices, inserting/removing products, sorting by ascending/descending price, name-based product search, accessing About Us, and viewing product lists and details.

### Not stated

The source does not specify traffic or growth, availability targets, latency, team size, budget, hosting or cloud provider, payment or shipping providers, data retention/privacy policies, authentication details, or deployment topology. It also does not specify stock/inventory behavior, product attributes beyond name and price-related sorting, checkout/order lifecycle states, payment failure/refund handling, shipment creation or carrier tracking integration, merchant authorization boundaries, or exact package information.

### Ambiguous phrase: “distributed system”

- **Reading A — multiple independently deployable internal services:** this would favor an architecture with explicit service boundaries and network communication, such as microservices or event-driven services. A single deployable modular monolith would not fully meet this interpretation.
- **Reading B — the overall system includes separate machines or external payment/shipping systems:** a single application could still be distributed at the system boundary while keeping its own business logic in one deployment unit.
- **Reading C — “distributed” is a broad description without a required topology:** it does not prescribe service boundaries; architecture should be selected using other requirements and constraints.

The source does not resolve these readings; the architecture discussion must not treat one as confirmed.

## Architecture 1: Layered modular monolith

### 1. In one sentence

**Assumption:** Build one application and deploy it as one unit, while organizing its code into clear business modules and technical layers.

### 2. How it works

**Assumptions:** The customer and merchant experiences use the same application, organized into presentation/API, business logic, and data-access layers. Inside the business layer, modules handle accounts, catalog, cart, orders/payments, and shipment information. The modules run together and use one application database; payment and shipping providers, if needed, are external systems rather than internal services.

### 3. Simple example

**Assumptions:** A customer submits the cart; the cart/order logic records an order and its item details, then requests payment from an external provider. When payment is confirmed, the order is updated and shipment processing is requested. The customer later checks the order page for package information. Payment and shipping providers, confirmation mechanisms, and this sequence are not specified requirements.

### 4. Main parts

| Part | Responsibility | Owns data? |
|---|---|---|
| Customer and merchant interface/API | Registration/login, profiles, product views, cart, merchant actions, and order views | No; **assumption:** delegates to business modules |
| Account module | Customer and merchant account/profile behavior | **Assumption:** account records in the shared application database |
| Catalog module | Product list, details, search, price sorting, and merchant product/price changes | **Assumption:** product records in the shared application database |
| Cart and order module | Cart changes, cart display, and order creation/viewing | **Assumption:** cart and order records in the shared application database |
| Payment integration | Initiates or records payment outcomes | **Assumption:** payment records in the shared application database; provider owns its own payment records |
| Shipment/order-information module | Makes package information available to the customer | **Assumption:** shipment information in the shared application database; any carrier owns its own records |

### 5. Advantages

- The customer and merchant stories share product listing, search, details, and price sorting; **assumption:** a shared catalog module can implement these consistently without coordinating separately deployed services.
- Cart, payment, and order views can use one application transaction for local database changes; **assumption:** this can simplify local consistency compared with cross-service updates.
- **Assumption:** One application deployment and a shared local development/test setup are simpler to operate than many independently deployed services.

### 6. Disadvantages

- The source calls the system “distributed”; if that means multiple independently deployed internal services, this architecture does not satisfy that interpretation.
- **Assumption:** Modules share a deployment and database, so scaling or deploying one business capability independently is limited.
- **Assumption:** A defect or release problem in the application can affect both customer and merchant capabilities.
- Payment and shipment integrations still cross system boundaries; keeping one application does not make those remote operations atomic or remove their failure modes.

### 7. How it differs from previous architectures

There is no previous architecture in this discussion. This is the baseline proposal: **assumption:** one deployment unit and one application-owned database, with internal modules communicating through in-process calls. Local database transactions can cover multiple modules’ data if designed to do so; external payment/shipping calls remain outside those transactions. **Assumption:** operations focus on deploying and monitoring the application plus its database and external integrations.

### 8. Main technical challenges

- **Assumption:** Keep module boundaries clear so account, catalog, cart/order, and integrations do not become an unstructured shared codebase.
- A database transaction cannot make an external payment or carrier call atomic. **Assumption:** record the order/payment intent before a remote call, handle confirmed, failed, and unknown outcomes explicitly, and reconcile operations that remain unresolved.
- **Assumption:** Make payment callbacks or retries safe against duplicate delivery; a timeout should be treated as an unknown outcome until checked, not automatically as a failure.
- The source does not define order, payment-attempt, or shipment states. **Assumption:** define them separately and ensure late or duplicate updates cannot incorrectly move an order backward.
- **Assumption:** Enforce customer access to their own profile/orders and merchant permissions for product changes.

### 9. Fit with the requirements

The requirements describe customer and merchant features over a shared product catalog, cart, payment, and order/package information, which can be grouped into modules in one application. However, the source’s “distributed system” wording is unresolved. This proposal fits if that wording permits one internally monolithic application interacting with external systems; it is a poor fit if it mandates independently deployed internal services. The one-deployment design, shared database, interfaces, and integration behavior are assumptions, not stated requirements.

### 10. Open questions

- What does “distributed system” require: multiple internal services, deployment across machines, external integrations, or only a general system description?
- Must payment and shipment use named external providers, or are they in scope for the CDC Shop itself?
- What package information must an order show, and how is it obtained?
- What are the required stock, order, payment, and shipment states and failure behaviors?
- What availability, scaling, security, hosting, and data-policy constraints apply?

## Architecture 2: Microservices

### 1. In one sentence

**Assumption:** Split the shop into independently deployable services, each responsible for a business capability and its own data.

### 2. How it works

**Assumptions:** A customer/merchant web application calls an API gateway or backend-for-frontend, which routes requests to independently deployed services. Plausible boundaries are Identity/Accounts, Catalog, Cart, Orders, Payments, and Shipments. Each service owns its data store; other services access that data through APIs or events rather than directly querying its database. Synchronous APIs can serve immediate queries and commands, while events can notify other services of changes. Payment and shipping providers remain external integrations if the system uses them.

### 3. Simple example

**Assumptions:** A customer submits a cart through the gateway. The Orders service validates the request with the Cart and Catalog services, stores an order in a pending state, and records an intent to request payment. The Payments service contacts its provider and reports the result; an event or API call lets Orders update the order and request shipment handling. The Shipments service stores package information that the customer can retrieve through the gateway. Because these services have separate databases, the flow cannot be one atomic transaction: intermediate states and recovery behavior must be designed. These services, providers, and workflow are not stated requirements.

### 4. Main parts

| Part | Responsibility | Owns data? |
|---|---|---|
| Customer/merchant application and API gateway | Presents role-appropriate features and routes requests | No; **assumption:** may manage short-lived presentation state |
| Identity/Accounts service | Registration, login, profiles, and identity-related behavior | **Assumption:** owns account and credential data |
| Catalog service | Product list, details, search, price sorting, product insertion/removal, and price changes | **Assumption:** owns product data |
| Cart service | Current cart display and item changes | **Assumption:** owns cart data |
| Orders service | Creates orders and serves customer order information | **Assumption:** owns order records and order-item snapshots |
| Payments service | Coordinates payment attempts and provider communication | **Assumption:** owns payment-attempt records; provider owns its records |
| Shipments service | Coordinates shipment information and customer package details | **Assumption:** owns shipment/package records; carrier owns its records |
| Message broker (if events are used) | Delivers events between services | No business data ownership; **assumption:** retains messages temporarily for delivery |

### 5. Advantages

- The source calls CDC Shop a “distributed system”; **assumption:** if that means independently deployed internal components, microservices fit that interpretation directly.
- **Assumption:** Catalog changes or search load could be scaled and released separately from account or order capabilities if operational needs justify it.
- **Assumption:** Separate ownership can make responsibility for product, cart, payment, and shipment data clearer as the system and team grow.
- The customer and merchant stories both use catalog capabilities; **assumption:** one Catalog service could provide consistent product behavior to both roles.

### 6. Disadvantages

- The requirements do not establish that independent deployment, independent scaling, or separate data ownership is needed. **Assumption:** the added network, deployment, and operational complexity could be unnecessary for this feature set.
- A checkout flow spans multiple services and databases; there is no single transaction covering all steps. **Assumption:** users and support tooling may need to handle visible pending states, retries, and compensation for partial completion.
- **Assumption:** Service outages or network timeouts can interrupt cross-service actions even when the caller cannot tell whether the callee completed the work.
- **Assumption:** APIs, events, service identity, authorization, tracing, local development, and end-to-end testing require additional design and maintenance.
- Data duplication and eventual consistency may occur; **assumption:** for example, an order needs a snapshot of product name and price so later catalog changes do not rewrite what was purchased.

### 7. How it differs from the previous architecture

Compared with the layered modular monolith, this proposal changes the deployment and data boundaries: **assumption:** services deploy independently, communicate across a network, and own separate databases instead of calling in-process modules over a shared application database. The monolith may use a local database transaction across modules; microservices cannot use one ordinary database transaction across the checkout workflow. **Assumption:** service-specific scaling and releases become possible, but operations must handle more deployments, network failures, service-to-service security, and distributed tracing.

### 8. Main technical challenges

- **Assumption:** Choose service boundaries that reflect stable ownership rather than making every feature or database table a service; avoid splitting Cart and Orders further unless justified.
- A remote payment or carrier call cannot be part of a database transaction. **Assumption:** Orders first persists a pending order and an outbox intent, then a worker calls Payments; the remote result is recorded in a separate transaction and triggers the next step. A saga or explicit workflow coordinates these steps without implying an atomic multi-service transaction.
- **Assumption:** Use idempotency keys for outgoing payment/shipment requests, unique event IDs for duplicate delivery, and safe retries. Treat timeouts as unknown until reconciled with the provider.
- **Assumption:** Use an outbox for committed state changes that must publish events, and ensure competing workers safely claim work. Reconciliation should detect operations left pending for too long.
- The source does not define order, payment-attempt, or shipment states. **Assumption:** model these separately, allow only valid forward transitions, and define behavior for payment failure, duplicate/late callbacks, and shipment failure.
- **Assumption:** Each service must enforce authorization for its data, verify caller identity, and use appropriately scoped service-to-service credentials; the gateway alone should not be the only authorization boundary.
- **Assumption:** Add correlation IDs, centralized logs/metrics/traces, contract and failure-scenario tests, and a way to run or simulate dependencies during local development.

### 9. Fit with the requirements

The source’s phrase “distributed system” could support this architecture if it means separately deployable internal services. The listed customer and merchant capabilities also suggest possible domain boundaries such as catalog, accounts, carts, and orders, but the requirements do not state that these boundaries must be deployed or scaled independently. Separate services, databases, API/event communication, and a saga are assumptions. If “distributed” only refers to external integrations or does not prescribe topology, the requirements alone do not demonstrate a need for microservices.

### 10. Open questions

- Does “distributed system” explicitly require independently deployed services, or is it descriptive?
- Are independent release, scaling, or data ownership needs expected, and who would operate the services?
- Which boundaries are required, and should cart and order be separate services?
- Which steps and state transitions define checkout, payment confirmation, shipment creation, and package tracking?
- Which payment/shipping providers and callback or status-query mechanisms are available?
- What consistency, recovery-time, availability, latency, security, and hosting constraints apply?

## Architecture 3: Serverless / event-driven

### 1. In one sentence

**Assumption:** Run shop operations in managed, on-demand functions or services, using events to coordinate work that does not need an immediate response.

### 2. How it works

**Assumptions:** A web application calls an API gateway, which invokes functions for synchronous actions such as login, product search, cart display, and merchant product changes. A managed database stores application records. When an action starts longer-running work, such as payment or shipment handling, a function writes a durable event or queued command; event-triggered functions process it and publish subsequent events. External payment/shipping providers, if used, report outcomes through callbacks or status checks. Serverless describes how code is provisioned and run; event-driven describes how components communicate. This architecture can also be implemented with microservice boundaries, and the two styles are not mutually exclusive.

### 3. Simple example

**Assumptions:** A customer submits a cart through the API. A function validates it and stores a pending order and a payment-request event. A payment function consumes that event and calls the provider using a stable idempotency key. A confirmation callback or reconciliation function records the payment result and publishes an event for shipment processing. A shipment function then records package information, which an order-query function returns to the customer. Each asynchronous step can be retried, so handlers must tolerate duplicate events. The providers, event flow, and these states are not stated requirements.

### 4. Main parts

| Part | Responsibility | Owns data? |
|---|---|---|
| Web application and API gateway | Presents customer and merchant features and routes immediate requests | No; **assumption:** may manage presentation state |
| Synchronous functions | Handle login/profile actions, catalog queries and changes, and cart/order requests | **Assumption:** business records live in managed data stores rather than function instances |
| Managed database | Persists accounts, products, carts, orders, payment attempts, and shipment information | **Assumption:** one or more managed stores; ownership and partitioning need definition |
| Queue/event bus | Durably buffers work and distributes business events to handlers | **Assumption:** owns delivery metadata and retention, not authoritative shop records |
| Payment and shipment handlers | Process payment/shipment commands and provider callbacks | **Assumption:** update shop records through managed stores; providers/carriers own their records |
| Scheduled/reconciliation functions | Find unresolved operations and query providers or raise alerts | **Assumption:** needed for operations that remain pending or have missing callbacks |

### 5. Advantages

- **Assumption:** On-demand execution can suit uneven or bursty demand for product browsing or checkout, without managing always-on application servers.
- **Assumption:** Queues can absorb bursts and decouple payment/shipment processing from the immediate cart submission response.
- The source calls CDC Shop a “distributed system”; **assumption:** managed gateways, functions, data stores, and event infrastructure provide distributed components without requiring the team to operate each runtime directly.
- **Assumption:** The asynchronous flow can isolate failures: a temporary shipment-handler outage need not prevent a payment result from being recorded.

### 6. Disadvantages

- The requirements give no traffic profile, provider, or hosting constraint establishing that serverless execution is beneficial. **Assumption:** per-invocation pricing, cold starts, quotas, and provider limits may be poor fits depending on workload and latency needs.
- Event delivery and function retries can produce duplicates; timeouts and delayed callbacks can leave business outcomes uncertain.
- **Assumption:** Debugging and tracing an order across short-lived functions, queues, and external providers is more complex than following one in-process call path.
- **Assumption:** Managed services and event formats can increase provider lock-in, while local development and realistic end-to-end testing need emulation or cloud test environments.
- Serverless is not itself a service-boundary strategy; **assumption:** unclear boundaries can still produce tightly coupled functions, shared-data conflicts, or a distributed monolith.

### 7. How it differs from the previous architectures

Compared with the layered modular monolith, this proposal uses managed on-demand execution and durable asynchronous messaging rather than one continuously deployed application with in-process module calls. **Assumption:** This can reduce server operations and absorb bursts, but moves complexity into queues, retries, event schemas, observability, and state handling.

Compared with microservices, serverless/event-driven describes execution and communication choices rather than necessarily requiring one independently owned service and database per business capability. **Assumption:** The team can use function-level handlers with managed shared data stores or combine serverless execution with microservice data ownership; either way, asynchronous steps still need explicit boundaries and consistency rules. Microservices can use long-running processes and synchronous APIs; serverless functions can also call synchronously. Therefore the styles overlap and are not strict alternatives.

### 8. Main technical challenges

- **Assumption:** Keep event handlers idempotent. Use stable idempotency keys for provider requests and unique event IDs or inbox records to avoid applying duplicates twice.
- A timeout is not proof that payment or shipment failed. **Assumption:** represent unknown/pending results, retry with the same key where supported, query provider status, and reconcile operations with missing callbacks.
- **Assumption:** Persist the order and event intent together using a transactional outbox or a managed equivalent, so a crash after order creation cannot silently lose the payment request.
- **Assumption:** Use explicit order, payment-attempt, and shipment states; accept only valid forward transitions so late events do not revert a completed state.
- **Assumption:** Set bounded retries, dead-letter handling, alerting, and replay procedures. Avoid infinite retries or silently discarded failures.
- **Assumption:** Prevent concurrent function invocations from corrupting carts, stock, or order state using conditional writes, concurrency controls, or appropriate transactions in the selected store.
- **Assumption:** Protect API and event handlers with role-based authorization and scoped provider/service credentials; validate event sources and callback authenticity.
- **Assumption:** Add end-to-end correlation IDs, queue-age and failure monitoring, contract tests, duplicate/late-event tests, and cost/latency monitoring. Respect provider execution timeouts for longer tasks.

### 9. Fit with the requirements

The source explicitly calls CDC Shop a “distributed system” and includes payment, shipment, and customer order/package information, which could be implemented through asynchronous events if those workflows involve external systems or work that may complete later. However, the requirements do not state a cloud provider, bursty traffic, asynchronous response expectations, or a preference for managed functions. Serverless hosting, event-driven coordination, providers, and the proposed states are assumptions. If “distributed” only describes the overall system, this style remains one possible implementation but is not established as necessary.

### 10. Open questions

- Are cloud-managed functions and queues allowed, and is there a hosting/provider preference?
- Which customer actions need immediate responses, and which may complete asynchronously?
- What request latency, traffic pattern, execution duration, and cost predictability are required?
- Which payment/shipment providers support idempotency and status reconciliation?
- What event retention, replay, dead-letter, and operational response expectations apply?
- Should functions be grouped by business service ownership, or is a shared application data model acceptable?
- What are the required order, payment, and shipment states, including timeout and failure behavior?

## Consolidated Summary

This section consolidates the three proposals discussed above. It records trade-offs rather than selecting an architecture. Items identified as assumptions are proposals or implementation implications, not confirmed CDC Shop requirements.

### A. Requirements stated in the source

The source describes CDC Shop as “a distributed system that handles the management, the payment and the shipment of products,” specifically hardware-store materials. Its customer stories cover registration, login/logout, profile access, product listing/details/search/price sorting, cart viewing and updates, cart payment, order/package information, About Us, and contacting the shop. Merchant stories cover login/logout, profile access, product listing/details/search/price sorting, product insertion/removal, price changes, and About Us.

### B. Not stated and assumptions

| Topic | What the source says | Assumption used in the proposals |
|---|---|---|
| Meaning of “distributed system” | The system is called distributed; no topology is defined. | It could mean internal services, external integrations, or a broad system description. It remains unresolved. |
| Deployment and hosting | Not specified. | Monolith is one application deployment; microservices are independently deployed; serverless uses managed functions and services. |
| Traffic and availability | Not specified. | Independent scaling or burst absorption might matter, but no evidence establishes either need. |
| Data ownership | Not specified. | Monolith shares an application database; microservices use service-owned data; serverless could use shared or capability-owned stores. |
| Payment/shipping providers | Not specified. | Examples assume external providers may be involved; names, APIs, callbacks, and status mechanisms are unknown. |
| Checkout and entity states | Payment and checking an order/package are requested; lifecycle states are not. | Pending/confirmed/failed or unknown payment and shipment states need definition if asynchronous external steps exist. |
| Security and authorization | Login and role-specific stories are stated; authentication design and permission rules are not. | Customers should be limited to their own data and merchants to permitted product operations. |
| Product/order data details | Product listing/details and price operations are stated; exact fields, inventory, and order snapshots are not. | An order should retain the purchased item name and price as a snapshot. |
| Cloud, cost, privacy, and operations | Not specified. | Provider lock-in, monitoring, data policy, and operational capacity require clarification before choosing implementation technology. |

### C. Architecture 1 — Layered modular monolith

**How it works:** **Assumption:** One application deployment is organized into layers and business modules for accounts, catalog, cart/orders, payments, and shipment information, using a shared application database. Modules communicate in-process.

**Pros discussed:** Shared catalog behavior can serve both roles; a shared database can simplify local consistency; one deployment is comparatively straightforward to develop and operate.

**Cons discussed:** It does not satisfy a strict interpretation requiring independently deployed internal services. Capabilities cannot be independently deployed or scaled, and application-wide release issues can affect both roles.

**Technical complexity:** **Assumption:** Lowest of the three for deployment and cross-module coordination, though module boundaries, authorization, and external payment/shipment failure handling still require deliberate design.

**Fit:** The listed features can be grouped into modules in one application. Fit depends on “distributed system”: if that means external integrations or is descriptive, this remains possible; if it mandates internal independent services, it does not fit.

### D. Architecture 2 — Microservices

**How it works:** **Assumption:** Independently deployable services own capabilities and data, such as Accounts, Catalog, Cart, Orders, Payments, and Shipments. A gateway routes requests; services communicate through APIs and possibly events.

**Pros discussed:** Could satisfy the strict interpretation of distributed internal components; could permit independent releases/scaling and clearer capability data ownership if those needs arise.

**Cons discussed:** The requirements do not establish that independent releases, scaling, or ownership are needed. Network boundaries, service availability, data duplication, and cross-service checkout consistency add complexity.

**Technical complexity:** **Assumption:** Highest day-to-day service coordination overhead of the three: service boundaries, API/event contracts, authorization between services, tracing, deployment, and testing all need attention. Checkout needs explicit pending states and a saga/workflow rather than a single transaction.

**Fit:** Potentially strong if “distributed” mandates independently deployable components; not demonstrated as necessary if the term refers only to the overall system or its external integrations.

### E. Architecture 3 — Serverless / event-driven

**How it works:** **Assumption:** An API gateway invokes managed functions for synchronous actions, while queues/events trigger functions for longer-running work such as payment or shipment handling. Managed data stores persist business records.

**Pros discussed:** On-demand execution may suit uneven demand; queues can buffer bursts and separate immediate responses from later processing; managed infrastructure may reduce server operations.

**Cons discussed:** Traffic and hosting requirements do not establish a benefit. Retries, delayed outcomes, cold starts, quotas, provider lock-in, observability, and local testing may be challenging. Serverless is an execution model and event-driven is a communication style; they may overlap with microservices.

**Technical complexity:** **Assumption:** Less server management can come with more event, retry, replay, and state-transition work. Reliability requires idempotent handlers, durable event intent, bounded retries, dead-letter handling, reconciliation, and end-to-end tracing.

**Fit:** Payment, shipment, and order/package information could involve asynchronous workflows, but the requirements do not specify asynchronous behavior, cloud functions, workload patterns, or a provider preference. Its suitability is therefore conditional and unproven.

### F. Comparison

| Dimension | Layered modular monolith | Microservices | Serverless / event-driven |
|---|---|---|---|
| Deployment unit | **Assumption:** One application | **Assumption:** Multiple independently deployed services | **Assumption:** Functions and managed services deployed/triggered independently |
| Operations | **Assumption:** Operate application and database | **Assumption:** Operate/coordinate many services, data stores, and network paths | **Assumption:** Less server management; manage provider configuration, queues, functions, and operational policies |
| Technical complexity | **Assumption:** Lower distributed-systems overhead; preserve module boundaries | **Assumption:** High service, network, data, and deployment coordination | **Assumption:** Moderate-to-high event/retry/observability complexity; runtime operations may be reduced |
| Transactions | Local database transaction may span modules; no transaction includes a remote provider call | No ordinary transaction spans service databases; workflow/saga required | Local store transaction may be possible; no transaction spans asynchronous handlers or remote providers |
| Failure handling | Handle provider timeouts and callbacks within the application; **assumption:** one deployment may share failure impact | Handle network and service failures, partial workflow completion, and provider failures | Handle duplicate/delayed events, retries, queue backlog, function/provider failures, and unknown outcomes |
| Scaling | **Assumption:** Scale application as a unit | **Assumption:** Scale individual services independently | **Assumption:** Managed execution scales with triggers/requests subject to provider limits |
| Cost predictability | **Assumption:** Potentially more fixed infrastructure cost; actual cost unknown | **Assumption:** Multiple services add baseline/operations cost; actual cost unknown | **Assumption:** Usage-based costs may vary with volume; actual cost unknown |
| Lock-in | **Assumption:** Depends on chosen stack and hosting | **Assumption:** Depends on infrastructure, messaging, and data choices | **Assumption:** Managed functions/events may increase provider-specific coupling |
| Evidence of need in requirements | Shared features fit modules; “distributed” wording may conflict depending on meaning | Only the ambiguous “distributed system” phrase could require this; independent scaling/ownership are not stated | Payment/shipment could involve delayed work, but asynchronous processing, cloud, and traffic needs are not stated |

### G. Concerns common to all three

If payment or shipment depends on a remote provider, those failures do not disappear with any architecture. A local database transaction cannot include a remote call; a timeout means the outcome may be unknown, not necessarily failed. **Assumption:** whichever architecture is selected should persist business intent before remote work, safely handle retries and duplicate callbacks/events, reconcile operations that remain unresolved, and prevent late updates from invalidating a completed state. The requirements do not confirm which external integrations exist.

### H. Provisional observations — not a decision

- The requirements specify user-visible capabilities more clearly than runtime, scaling, or deployment constraints.
- “Distributed system” is consequential but ambiguous; no architecture should treat one interpretation as confirmed.
- A modular monolith maps directly to the stated customer and merchant features with fewer assumed deployment boundaries.
- Microservices become more compelling only if independently deployed components, ownership, or scaling are actual requirements.
- Serverless/event-driven could suit asynchronous payment/shipment workflows, but those workflows and the cloud operating context remain unconfirmed.
- These are observations from the discussion, not a recommendation or architecture decision.

### I. Open questions

- What exactly does “distributed system” mean for this assignment?
- Are payment and shipping external integrations? Which providers, callbacks, and status checks are available?
- What package information, inventory behavior, and order/payment/shipment states are required?
- Which operations may complete asynchronously, and what responses should customers see while pending?
- What are the expected traffic, latency, availability, recovery, security, privacy, hosting, and cost constraints?
- What team and operational capacity is available to run and troubleshoot multiple services or managed event infrastructure?

### J. Next steps

Task 1's three architecture proposals and their comparison are recorded here. No architecture has been selected. An ADR and any implementation work have not been started; create an ADR only if requested after resolving the relevant open questions.

## Final summary

The CDC Shop requirements describe customer and merchant workflows for accounts, products, carts, payment, and order/package information, but do not settle deployment topology, operating constraints, or integration details. A layered modular monolith groups these capabilities in one application; microservices distribute them across independently owned services; serverless/event-driven uses managed execution and events and can overlap with microservices. Each approach has trade-offs in deployment, data consistency, failure handling, and operational effort. The meaning of “distributed system” remains unresolved, so this discussion makes no architecture decision and creates no ADR.

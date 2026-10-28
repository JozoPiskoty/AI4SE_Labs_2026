# Technical checklist for systems with external integrations

Use as a prompt for completeness. Present only what is relevant to the user's question.

## Transactions and consistency
- A database transaction cannot include a remote call (payment gateway, carrier, email). Never hold a transaction open across one.
- Commit the pending business record (order) before any remote call.
- Write the intent to call the remote system in the same transaction (**transactional outbox**), so a crash cannot lose it.
- Use a **second, separate transaction** when the remote result arrives (record result, update state, write the next outbox entry).
- Multi-component systems (microservices, serverless): no cross-component transaction, so use a saga with visible pending states and compensation.

## Duplicates, retries, timeouts
- **Idempotency keys** on outgoing requests (stable, derived from the business entity and attempt number).
- **Inbox / unique event IDs** so duplicate webhooks or messages are harmless.
- A timeout means **unknown**, not failed. Retry with the same key; reconcile by status lookup.
- A **reconciliation job** sweeps stuck entities and alerts on persistent failures.
- Several instances running workers: claim outbox rows safely (lock or lease) and keep processing idempotent.
- Late or out-of-order events must not move state backwards; apply only valid forward transitions.

## State model
- Separate states for the order, the payment attempt, and the shipment (or justify a single status).
- Define transitions, who triggers them, and what happens on payment failure, timeout, duplicate callback, shipment failure.
- Mark which states are in the requirements and which are our assumptions.

## Data and security
- Order lines keep a snapshot of name and price.
- Authorization at the module/service that owns the resource (customer sees own orders; merchant manages permitted products).
- Cross-service: token verification per service, scoped service-to-service identity, revocation trade-offs.

## Operations
- Deployment, monitoring, tracing and correlation IDs, contract and failure-scenario testing, cost and lock-in, local debugging.

## Overlap to explain
- Serverless describes how code runs; microservices describe how the system is divided. They can overlap.

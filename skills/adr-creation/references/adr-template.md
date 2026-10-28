# ADR template (technology-neutral)

```markdown
# ADR-NNN: <Decision title>

| Field | Value |
|---|---|
| Status | Proposed / Accepted (state the condition and for whom) |
| Approval | Who approved. If nobody external: say so explicitly. |
| Date | YYYY-MM-DD |
| Scope | What this ADR decides |
| Sources | [requirements](./path), [architecture notes](./path), [ADR notes](./path) |

## 1. Context
### 1.1 Requirements stated in the source
### 1.2 What the source does not state
### 1.3 Ambiguous terms (table: reading, meaning, effect on decision) and the working assumption, if one is adopted
### 1.4 Assumptions (table: #, assumption, needs confirmation)
### 1.5 Decision drivers

## 2. Alternatives considered
### 2.1 .. 2.3 each: description, pros, cons (note overlaps between alternatives)
### 2.4 Overview comparison table (criteria x alternatives, incl. "evidence of need in the source")

## 3. Decision
Selected architecture, numbered elements, "Not decided here" list.
### 3.1 Critical recovery/failure design (if the system has external integrations)

## 4. Reasons
## 5. Consequences (positive, negative)
## 6. Risks and mitigations
### 6.1 Key risk (ambiguity), 6.2 risk table
## 7. Revisit triggers
## 8. Open questions
### 8.1 Could invalidate the decision
### 8.2 Implementation questions
## 9. Component overview (text diagram)
## 10. Change log (version, date, change)
```

Guidelines: short sentences, tables for comparisons, no product names unless required, label every assumption.

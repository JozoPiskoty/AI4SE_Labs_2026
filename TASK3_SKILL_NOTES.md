# Task 3 — Skill Creation Notes

Record of creating reusable Skills from the Task 1 and Task 2 work. Task 3 assignment: [Tasks/Task_3.md](./Tasks/Task_3.md).

## Scope of this session

- Read `Task_3.md`, and reviewed [TASK1_ARCHITECTURE_NOTES.md](./TASK1_ARCHITECTURE_NOTES.md), [TASK2_ADR_NOTES.md](./TASK2_ADR_NOTES.md), and [ADR_CDC_SHOP.md](./ADR_CDC_SHOP.md).
- Created two Skills. The original Task 1 and Task 2 deliverables were not modified.
- Subsequently completed the Skill-assisted Task 1 and Task 2 rerun, producing [TASK1_RERUN_NOTES.md](./TASK1_RERUN_NOTES.md), [TASK2_RERUN_NOTES.md](./TASK2_RERUN_NOTES.md), and [ADR_RERUN.md](./ADR_RERUN.md).
- Completed the before/after comparison in [TASK3_COMPARISON_REPORT.md](./TASK3_COMPARISON_REPORT.md).

## What was reviewed and what was learned

Lessons taken from the Task 1/2 records and encoded in the Skills:

| Observed in Task 1/2 | Encoded as |
|---|---|
| Notes had to be requested and updated after each answer | Skills create the notes file first and append after every answer/iteration |
| Requirements vs assumptions had to be repeatedly separated | Mandatory "stated" vs "not stated" lists, numbered assumptions, assumptions table |
| An ambiguous phrase ("distributed system") drove the whole decision | Step to list readings and effects; key-risk section; revisit trigger |
| Architectures were presented one at a time, each with pros, cons, differences from the previous | Three-architecture sequence with a per-architecture template |
| Follow-ups repeatedly covered transactions, duplicates, timeouts, state model, data ownership, communication, identity, cost | Technical checklist for the discussion skill |
| Stale "Status" lines needed fixing after moving on | Close-each-architecture step with "at the time" wording |
| ADR needed several rounds: risk section, crash recovery, overlap of serverless and microservices | Ordered iteration guide and review checklist |
| Inconsistency found late (reason 4 said one transaction instead of two) | Review checklist item for transaction boundaries across all sections |
| Status moved Proposed → Accepted with a conditional working assumption and no external approval | Status/approval rules and a template row |
| Historical change-log rows must keep their old status | Ground rule: do not rewrite history |

## Design decisions

- **Two Skills, not one:** discussion and ADR writing are separate phases with different outputs (notes vs ADR) and are triggered by different requests. The ADR skill consumes the notes from the first.
- **Generic, not CDC-specific:** CDC is only used as an example (checkout, payment, shipment); the Skills apply to any system with requirements and external integrations. The default architecture trio is replaceable if the domain demands.
- **Progressive loading:** each `SKILL.md` holds the procedure; templates and checklists are in `references/` and linked from it.
- **Location:** `.github/skills/<name>/SKILL.md`, the project-skill location used by VS Code / Copilot. The folder is inside `Week_05_Designing`, so it is picked up when that folder is the opened workspace (or move `.github` to a workspace root).
- No decision was embedded: the discussion skill explicitly never picks a winner; the ADR skill never claims stakeholder approval.

## Files created

```text
.github/skills/
  architecture-discussion/
    SKILL.md
    references/architecture-template.md
    references/technical-checklist.md
  adr-creation/
    SKILL.md
    references/adr-template.md
    references/review-checklist.md
```

- [architecture-discussion/SKILL.md](./.github/skills/architecture-discussion/SKILL.md)
- [adr-creation/SKILL.md](./.github/skills/adr-creation/SKILL.md)

## Limitations

- The comparison report found no comparable elapsed-time measurements, so whether the Skills made the work faster is unmeasured.
- The report notes that the available files do not establish whether the rerun followed the separate-new-session procedure originally described below.
- They were derived from a single project (CDC Shop, e-commerce with payment and shipping); other domains may need different checklist items.

## Rerun and comparison completed

The rerun artifacts are present: the architecture discussion and consolidation are in `TASK1_RERUN_NOTES.md`; the ADR and its process record are in `ADR_RERUN.md` and `TASK2_RERUN_NOTES.md`; and the comparison is in `TASK3_COMPARISON_REPORT.md`. The report records observed structural similarities and differences, acknowledges areas where the original discussion is more detailed, and makes no unsupported speed claim.

The comparison report was created by inspecting the original and rerun files. It explicitly notes that those files do not establish whether the rerun followed the separate-new-session procedure suggested during Skill creation, and that there are no comparable time measurements.

## Skill file verification

Verified that both Skill definitions and all four referenced files exist under `.github/skills/`:

- [architecture-discussion/SKILL.md](./.github/skills/architecture-discussion/SKILL.md)
- [architecture-template.md](./.github/skills/architecture-discussion/references/architecture-template.md)
- [technical-checklist.md](./.github/skills/architecture-discussion/references/technical-checklist.md)
- [adr-creation/SKILL.md](./.github/skills/adr-creation/SKILL.md)
- [adr-template.md](./.github/skills/adr-creation/references/adr-template.md)
- [review-checklist.md](./.github/skills/adr-creation/references/review-checklist.md)

All six files were opened successfully; none are missing.

## Change history

| Step | Change |
|---|---|
| 1 | Read Task_3.md and reviewed Task 1/2 outputs |
| 2 | Created `architecture-discussion` and `adr-creation` Skills with references |
| 3 | Wrote this notes file |
| 4 | Completed the Skill-assisted Task 1/2 rerun and created `TASK3_COMPARISON_REPORT.md` |
| 5 | Updated completion status and verified both Skills and all four reference files exist |

# Task 3 Comparison Report — CDC Shop

## Materials reviewed

Compared the original Task 1 discussion notes and Task 2 ADR/process record with the Skill-assisted rerun notes and ADR:

- Original: [TASK1_ARCHITECTURE_NOTES.md](./TASK1_ARCHITECTURE_NOTES.md), [ADR_CDC_SHOP.md](./ADR_CDC_SHOP.md), [TASK2_ADR_NOTES.md](./TASK2_ADR_NOTES.md)
- Rerun: [TASK1_RERUN_NOTES.md](./TASK1_RERUN_NOTES.md), [ADR_RERUN.md](./ADR_RERUN.md), [TASK2_RERUN_NOTES.md](./TASK2_RERUN_NOTES.md)
- Process context: [TASK3_SKILL_NOTES.md](./TASK3_SKILL_NOTES.md) and [Tasks/Task_3.md](./Tasks/Task_3.md)

## What improved in the Skill-assisted rerun

- The Task 1 rerun is consistently staged: it records requirements and unknowns first, explains the three architectures one at a time, and then appends a consolidated comparison. Its explicit separation of source statements, assumptions, and the unresolved “distributed system” wording makes the basis of the proposals easy to locate.
- The Task 2 rerun starts its process notes before drafting and records its recommendation, alternatives, assumptions, review steps, and unresolved questions. The ADR has a clear **Proposed** status, states that no stakeholder approval exists, and distinguishes decision-invalidating questions from implementation questions.
- The rerun ADR includes a comparison table, component diagram, transaction boundaries, and failure cases. Its process notes describe the consistency checks that were performed rather than implying automated checks or external approval.

These are observable improvements in structure and traceability in the rerun artifacts; they do not establish that the Skills reduced time or effort.

## What stayed similar

- Both Task 1 records discuss the same three styles—layered modular monolith, microservices, and serverless/event-driven—and both leave “distributed system” unresolved rather than claiming the requirements specify a topology.
- Both ADRs recommend a modular monolith conditionally, explain why the alternatives were not chosen, and recognize that payment and shipment failures still require recovery regardless of architecture.
- Both sets of notes distinguish stated capabilities from missing deployment, traffic, provider, and lifecycle details. Both ADRs use a technology-neutral approach and include comparison, risks, revisit conditions, and open questions.

## Weaknesses and limitations

- The original Task 1 notes and ADR contain more extensive checkout and failure-recovery discussion. For example, the original discussion spells out provider callback validation, inbox deduplication, retry/backoff behavior, and payment/shipment state examples; the rerun presents a shorter recovery outline. The Skills provide a useful checklist, but following it does not ensure the same depth unless the user asks for that depth.
- The original ADR records multiple content and consistency iterations in its change log. The rerun ADR has one initial version and a review recorded in its accompanying notes. That is a difference in the recorded process, not proof that the original was more correct or that the rerun required less work.
- The original ADR is marked **Accepted** for the design exercise under its stated working assumption; the rerun ADR remains **Proposed**. The rerun does not claim user or stakeholder acceptance, which is appropriately cautious, but the statuses are not directly equivalent.
- `TASK3_SKILL_NOTES.md` records that a new-session test had not yet been done when those notes were written. The current rerun files show the Skills being used, but the reviewed files alone do not establish that the rerun followed the separate-new-session procedure described there.
- Neither the rerun notes nor the process records contain comparable elapsed-time measurements. Therefore, whether the Skills made the task faster cannot be concluded from this evidence.

## Were the Skills useful?

The files provide evidence that the Skills were useful for **process consistency**: the discussion is sequenced, assumptions and ambiguity are surfaced, notes are maintained, and the ADR includes expected review structures. They appear to have supported a coherent rerun, but the original work was already thorough and in some areas more detailed. The evidence supports a qualified conclusion—useful as workflow and completeness guides, not demonstrated as a time-saving tool or guarantee of greater technical depth.

## Final conclusion

The Skill-assisted rerun preserves the substance of the original architecture discussion and ADR while making the expected structure and review trail explicit. It improves visible process discipline, but does not uniformly improve detail: some original checkout analysis is more comprehensive. No speed improvement is claimed because no comparable timing evidence exists.

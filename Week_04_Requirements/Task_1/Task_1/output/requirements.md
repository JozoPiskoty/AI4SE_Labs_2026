# Software Requirements Specification

## A. Document overview

This document consolidates software requirements extracted from the supplied corpus. Requirements and priorities are model-generated and require stakeholder validation; unresolved conflicts and incomplete evidence are listed below.

- Input corpus: `data\corpus`
- Documents discovered: 20
- Requirements: 346
- Review repair iterations: 0

## B. Priority scale

- **P1** — Critical: necessary for basic operation, compliance, or a critical need.
- **P2** — High: significant functionality or operational need.
- **P3** — Medium: useful capability that meaningfully improves the system.
- **P4** — Low: optional enhancement or requirement with lower impact.

Priorities are estimates unless a requirement explicitly records source-based priority evidence. The per-requirement rationale and `priority_is_estimated` field identify this distinction.

## C. Glossary

No glossary terms were independently established by the network. Add stakeholder-approved definitions before baselining this specification.

## D. Accepted requirements

### REQ-001: Material Volume Report with historical date-filtered views

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** CAND-000001 described this as a key requirement (P1). CAND-000005 explicitly requested date-filtering for historical comparisons (originally P2). These are the same functional need (reporting volume at any point in time); the consolidated priority is P1 because the core requirement was identified as key in the source summary while the date-filtering detail was described as useful and complementary.
- **Sources:** conversations/conv_pines014_material_volume.eml
- **Evidence:** “Here's what I'm hearing for the \"Material Volume Report\" requirement:”, “The system should provide the ability to report on the volume of material in a given library at any point in time”, “This will be tracked as a key requirement.”, “We can also add date filters - volume at any point in time, not just current. This would be useful for historical comparisons.”, “report ... at any point in time”
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall provide a "Material Volume Report" that can report the volume of library material for a given library at any point in time and shall support date filters so the report can show historical volumes for comparisons.

### REQ-002: Material volume counts by item status categories

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Included in the explicit "Material Volume Report" requirement breakdown in source material and treated as core data needed for the report.
- **Sources:** conversations/conv_pines014_material_volume.eml
- **Evidence:** “based on: - New acquisitions - Items on the shelf (checked in) - Items out in circulation (checked out)”
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall base the material volume report on item counts including new acquisitions (items recently added), items on the shelf (checked in), and items out in circulation (checked out).

### REQ-003: Material volume report category breakdown

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Listed explicitly as part of the Material Volume Report breakdown in the source material and treated as core reporting capability.
- **Sources:** conversations/conv_pines014_material_volume.eml
- **Evidence:** “The report should allow breaking down volume in categories such as: - Total items in library - Number of holds - Number of adult fiction - Number of board books”
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall allow the material volume report to break down volume into categories such as total items in library, number of holds, number of adult fiction, and number of board books.

### REQ-004: Customizable material volume categories

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Requested explicitly in conversation as a desirable capability; treated as lower-priority (P2) than the core volume reporting requirement.
- **Sources:** conversations/conv_pines014_material_volume.eml
- **Evidence:** “Can we make the categories customizable? Different libraries might want different breakdowns.”, “Other customizable categories”
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall support customizable category breakdowns for the material volume report, allowing different libraries to choose different breakdowns.

### REQ-005: System capacity interface overview of all branches

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Summarized in source material as a core requirement for capacity visibility across branches.
- **Sources:** conversations/conv_pines015_capacity_interface.eml
- **Evidence:** “The system should provide an interface showing the capacity of all branches.”, “High-level overview of all branches' capacity at once”
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall provide an interface showing the capacity of all branches with a high-level overview view that displays all branches at once.

### REQ-006: Capacity drill-down to individual branches

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicitly included in the capacity interface summary as necessary for investigating branch-level details.
- **Sources:** conversations/conv_pines015_capacity_interface.eml
- **Evidence:** “Ability to drill down into individual branches”, “The system should provide an interface showing the capacity of all branches.”
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall allow users to drill down from the all-branches capacity overview into individual branch capacity details.

### REQ-007: Capacity sorting and filtering

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Requested explicitly in the capacity interface summary and described as needed for practical use (sorting/filtering by region/type/load).
- **Sources:** conversations/conv_pines015_capacity_interface.eml
- **Evidence:** “Sorting and filtering capabilities (region, type, load)”, “I'd want to be able to sort and filter. By region, by library type, by current load...”
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall provide sorting and filtering capabilities for the capacity interface, including filtering by region, library type, and current load.

### REQ-008: Capacity trend data (growth/shrink patterns)

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicitly requested in the capacity interface discussion; treated as useful for planning but lower priority than immediate capacity visibility.
- **Sources:** conversations/conv_pines015_capacity_interface.eml
- **Evidence:** “can the capacity interface also show trends? Like, is this branch growing or shrinking?”, “Trend data (growth/shrink patterns)”
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall display trend data indicating whether a branch is growing or shrinking to support long-term planning.

### REQ-009: Export capacity data to CSV

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicitly requested (export to CSV) as a convenience for directors who want spreadsheets; considered lower priority than core interface capabilities.
- **Sources:** conversations/conv_pines015_capacity_interface.eml
- **Evidence:** “And export to CSV for the directors who want spreadsheets.”
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall allow exporting capacity interface data to CSV.

### REQ-010: Shelf space report: compare circulation, collection, and shelf space by genre/format

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicitly stated as the core shelf space reporting requirement in multiple messages and summaries.
- **Sources:** conversations/conv_pines016_shelf_space.eml
- **Evidence:** This is the "shelf space report" we've been talking about. The idea is: for each genre and format of material, compare: 1. Percentage of total circulations 2. Percentage of the collection 3. Percentage of total shelf space, Summarizing the Shelf Space Report requirement: The system should provide, for each genre and format of material, the ability to compare: - The percentage of total circulations - The percentage of the collection - The percentage of total shelf space
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall provide a shelf space report that, for each genre and format, compares (1) the percentage of total circulations, (2) the percentage of the collection, and (3) the percentage of total shelf space.

### REQ-011: Shelf space report scope per library and per system

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicitly stated in the shelf space discussion as necessary so branch managers can compare local situation to system averages.
- **Sources:** conversations/conv_pines016_shelf_space.eml
- **Evidence:** The report should be able to run per library and per system. This way branch managers can see their local situation AND see how they compare to the system average., The report should be available per library and per system.
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall make the shelf space report available both per library and for the entire system so branch managers can view local and system-average views.

### REQ-012: Shelf space report date-range filtering

- **Category:** functional
- **Priority:** P2 (estimated)
- **Priority rationale:** Requested explicitly as a useful capability to account for seasonality; not described as core as compared to the main shelf space metrics (hence P2).
- **Sources:** conversations/conv_pines016_shelf_space.eml
- **Evidence:** Can we also filter by date range? Like, what was the shelf space utilization in Q1 vs. Q2? Seasons matter for our collection.
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall support filtering the shelf space utilization report by a date range (for example, to compare Q1 vs. Q2).

### REQ-013: Shelf space report comparison view (libraries side-by-side)

- **Category:** functional
- **Priority:** P2 (estimated)
- **Priority rationale:** Explicitly requested as a helpful view; noted in discussion but not included in the final prioritized summary, so assigned P2.
- **Sources:** conversations/conv_pines016_shelf_space.eml
- **Evidence:** Also, can we include a "comparison" view that shows each library's breakdown side by side? That would make it easy to spot outliers.
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall provide a comparison view that shows each library's shelf-space breakdown side by side to make it easy to spot outliers.

### REQ-014: Shelf space report: compute percentage of collection by counting items per genre/format

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Identified as a necessary data calculation to produce the required shelf space metrics; treated as core supporting functionality.
- **Sources:** conversations/conv_pines016_shelf_space.eml
- **Evidence:** From a data perspective, we need to: 1. Count items per genre/format (this is the "percentage of collection")
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall compute the percentage of the collection for each genre and format by counting items per genre/format.

### REQ-015: ShelfSpaceReport-ComputePercentageOfCirculations

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** This metric is explicitly called out as required and described as summing checkouts; producing the percentage is a core reporting need.
- **Sources:** conversations/conv_pines016_shelf_space.eml
- **Evidence:** From a data perspective, we need to: 2. Sum checkouts per genre/format (this is the "percentage of circulations")
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall compute the percentage of total circulations for each genre and format by summing checkouts per genre and format.

### REQ-016: ShelfSpaceReport-EstimateShelfSpaceWithProxy

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** The system must still produce the required shelf-space percentage despite the database lacking direct shelf-space data; estimation using dimensions or count is the explicitly described approach.
- **Sources:** conversations/conv_pines016_shelf_space.eml
- **Evidence:** The tricky part is #3. Shelf space isn't directly tracked in the database. We'd need to estimate based on item dimensions or use item count as a proxy.
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall estimate shelf space per genre and format (where shelf space is not directly tracked) using item dimensions and/or item count as a proxy.

### REQ-017: ItemTransfer-BatchUtility

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Stated explicitly as a major/primary requirement in the origin materials; the batch-transfer utility is the top-level capability from which the more specific features derive.
- **Sources:** —
- **Evidence:** "The system should provide a utility for transferring batches of items between branches."
- **Manual provenance review required:** Yes
- **Confidence:** high
- **Related questions/dependencies:** —

System shall provide a utility to support transferring batches of items between branches.

### REQ-018: ItemTransfer-QueryCandidateMaterials

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Querying candidate materials is called out as a necessary function of the transfer utility and included in the consolidated requirements list.
- **Sources:** conversations/conv_pines018_item_transfer.eml
- **Evidence:** "The utility needs: - Query for candidate materials", "Ability to query for candidate materials"
- **Manual provenance review required:** Yes
- **Confidence:** high
- **Related questions/dependencies:** —

System shall allow staff to query for candidate materials to be transferred between branches.

### REQ-019: ItemTransfer-SaveQueriesForReuse

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Saving queries for repeated use is called out as crucial for operational efficiency and explicitly included in the major requirement list.
- **Sources:** conversations/conv_pines018_item_transfer.eml
- **Evidence:** "The \"save queries for repeated use\" is crucial.", "Ability to save queries for repeated use"
- **Manual provenance review required:** Yes
- **Confidence:** high
- **Related questions/dependencies:** —

System shall allow staff to save queries so they can be reused for repeated transfers.

### REQ-020: ItemTransfer-ManualSelectionFromQueryResults

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Manual selection of items from query results is explicitly requested and is an essential part of preparing a transfer batch.
- **Sources:** conversations/conv_pines018_item_transfer.eml
- **Evidence:** "Manually select titles from query results", "Ability to manually select titles from query results", "I should be able to check boxes and select which ones to include."
- **Manual provenance review required:** Yes
- **Confidence:** high
- **Related questions/dependencies:** —

System shall allow staff to manually select titles/items from query results (e.g., via check boxes) to choose which items to transfer.

### REQ-021: ItemTransfer-ChangeItemLocationField

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Changing the item location is the core action of a transfer. One candidate described this as a primary requirement (P1); another framed it as the mechanism (P2). The consolidated requirement uses the higher priority because it implements the essential behavior identified as primary.
- **Sources:** conversations/conv_pines018_item_transfer.eml
- **Evidence:** "Change records of selected items to new location", "Ability to change records of selected items to move to new location", "Mechanisms: changing location field", "Mechanisms: changing location field, generating pull lists"
- **Manual provenance review required:** Yes
- **Confidence:** high
- **Related questions/dependencies:** —

System shall change the item location field of selected items to the destination branch/unit as part of processing a batch transfer.

### REQ-022: ItemTransfer-GeneratePullLists

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Pull-list generation is an explicitly listed mechanism and useful technical component, but it is secondary to the core transfer actions.
- **Sources:** conversations/conv_pines018_item_transfer.eml
- **Evidence:** "Mechanisms: changing location field, generating pull lists", "Pull list generation - create a printable list of items to be moved.", "generate pull lists"
- **Manual provenance review required:** Yes
- **Confidence:** high
- **Related questions/dependencies:** —

System shall generate pull lists (printable lists of items) for items being transferred.

### REQ-023: ItemTransfer-AutoRevert-TimeBased

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Time-based auto-reversion is repeatedly emphasized with examples and included in the core set of transfer behaviors; one candidate marked this as P1 and another as a supporting example.
- **Sources:** conversations/conv_pines018_item_transfer.eml
- **Evidence:** "Revert items to original location after a set period of time", "Ability to revert items to original location after a set period of time", "send items to a book sale for 30 days, then they need to come back.", "Revert after X days (date-based)"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall be able to automatically revert transferred items to their original location after a configurable period of time (e.g., after X days).

### REQ-024: ItemTransfer-AutoRevert-OtherCriteria

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** This was requested as an extension to the time-based revert capability; it is valuable but described as secondary/advanced.
- **Sources:** conversations/conv_pines018_item_transfer.eml
- **Evidence:** "Can we also revert \"based on other criteria\"?", "Ability to revert items to original location after a set period of time and/or based on other criteria"
- **Manual provenance review required:** Yes
- **Confidence:** high
- **Related questions/dependencies:** —

System shall support auto-reversion of transferred items to their original location based on configurable non-time criteria (in addition to time-based criteria).

### REQ-025: ItemTransfer-AutoRevert-OnReturnEvent

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Event-based reversion was explicitly requested; it is an extension of revert behavior and therefore given secondary priority.
- **Sources:** conversations/conv_pines018_item_transfer.eml
- **Evidence:** "Revert when item status changes to \"returned\" (event-based)"
- **Manual provenance review required:** No
- **Confidence:** medium-high
- **Related questions/dependencies:** —

System shall support event-based auto-reversion when an item's status changes to "returned" (i.e., trigger reversion on a returned-status event if configured to do so).

### REQ-026: ItemTransfer-AutoRevert-CheckedOutBehavior

- **Category:** functional
- **Priority:** P2 (estimated)
- **Priority rationale:** An event-based rule related to checkouts at the destination was explicitly mentioned; the original materials express uncertainty about the exact desired logic, so this is treated as a configurable/secondary behavior.
- **Sources:** conversations/conv_pines018_item_transfer.eml
- **Evidence:** "Revert when item is checked out at the destination (event-based)", "when they're checked out there, they should stay."
- **Manual provenance review required:** No
- **Confidence:** low
- **Related questions/dependencies:** —

System shall support event-based behavior related to items checked out at the destination branch; the specific configured behavior must allow either (a) leaving items at destination if they are checked out there, or (b) reverting them depending on the configured policy.

### REQ-027: ItemTransfer-AutoRevert-ScheduledTask

- **Category:** non-functional
- **Priority:** P3 (estimated)
- **Priority rationale:** This is an implementation-level mechanism for auto-reversion suggested in the discussion. It is useful as a technical design note but is more specific than the functional revert requirements; priority is lower and was estimated.
- **Sources:** conversations/conv_pines018_item_transfer.eml
- **Evidence:** "Auto-revert mechanism - a scheduled task that checks transferred items and reverts them based on time or status criteria."
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall implement the auto-reversion mechanism using a scheduled/background task that checks transferred items and reverts them according to the configured time- or event-based criteria.

### REQ-028: Transfer audit logging

- **Category:** security
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicitly listed as a key component.
- **Sources:** conversations/conv_pines018_item_transfer.eml
- **Evidence:** "Logging - track all transfers for audit purposes."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall track and log all item transfers for audit purposes.

### REQ-029: Preview before making changes

- **Category:** usability
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicit request and included in additional features list.
- **Sources:** conversations/conv_pines018_item_transfer.eml
- **Evidence:** "utility should show a preview before making changes", "If you run this now, 25 items will be moved from Dalton-Whitman to Mobile Library Unit 3. Confirm?", "Preview before making changes"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall show a preview of a transfer (for example: number of items, source location, and destination location) before applying the changes.

### REQ-030: Undo function for transfers

- **Category:** usability
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicitly requested as an undo capability; included in additional features list.
- **Sources:** conversations/conv_pines018_item_transfer.eml
- **Evidence:** "And we need an undo function! What if someone clicks the wrong button?", "Undo function"
- **Manual provenance review required:** Yes
- **Confidence:** high
- **Related questions/dependencies:** —

System shall provide an undo function for a transfer so changes can be reversed if a user executes the wrong action.

### REQ-031: Permission control for transfers

- **Category:** security
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicit permissions concern and included in the additional features list; also a safety/security requirement.
- **Sources:** conversations/conv_pines018_item_transfer.eml
- **Evidence:** "Not every staff member should be able to transfer items between branches. This should be limited to certain roles (managers, administrators, transfer coordinators).", "Permission control (limited to managers/admins)"
- **Manual provenance review required:** Yes
- **Confidence:** high
- **Related questions/dependencies:** —

System shall restrict transfer functionality to specified user roles (for example: managers, administrators, and transfer coordinators).

### REQ-032: Printable transit labels

- **Category:** functional
- **Priority:** P3 (source-supported)
- **Priority rationale:** Explicitly requested; included in additional features list but not in major requirement core list.
- **Sources:** conversations/conv_pines018_item_transfer.eml
- **Evidence:** "Also, can we generate transit labels? Like, printable barcodes for the items being transferred?", "Printable transit labels", "create a printable list of items to be moved."
- **Manual provenance review required:** Yes
- **Confidence:** high
- **Related questions/dependencies:** —

System shall generate printable transit labels (for example: printable barcodes or a printable list) for items being transferred.

### REQ-033: Transfer delay/status alerts

- **Category:** functional
- **Priority:** P3 (source-supported)
- **Priority rationale:** Explicit alert request and listed as additional feature.
- **Sources:** conversations/conv_pines018_item_transfer.eml
- **Evidence:** "And can we set up alerts? If an item transfer is delayed or has issues, notify me.", "Transfer delay alerts"
- **Manual provenance review required:** Yes
- **Confidence:** high
- **Related questions/dependencies:** —

System shall send alerts or notifications when an item transfer is delayed or encounters issues.

### REQ-034: Transfer history tracking

- **Category:** functional
- **Priority:** P3 (source-supported)
- **Priority rationale:** Explicitly requested and included in additional features list.
- **Sources:** conversations/conv_pines018_item_transfer.eml
- **Evidence:** "Can we track transfer history? Like, \"this item has been transferred 5 times in the past year.\"", "Transfer history tracking"
- **Manual provenance review required:** Yes
- **Confidence:** high
- **Related questions/dependencies:** —

System shall record and provide transfer history for items (for example: count how many times an item has been transferred within a time period) to help identify incorrect locations.

### REQ-035: Temporary transfers for events/programs with revert

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Concrete use case explicitly requested and directly maps to revert capability.
- **Sources:** conversations/conv_pines018_item_transfer.eml
- **Evidence:** "for the outreach program use case - can we transfer items to a temporary location for a specific event or program? ... then revert them after the event."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall support transferring items to a temporary location for a specific event or program and then reverting those items to their prior location after the event.

### REQ-036: Efficient batch updates to avoid locking

- **Category:** non-functional
- **Priority:** P2 (estimated)
- **Priority rationale:** Explicit efficiency/locking concern tied to scale; testable via performance/locking behavior.
- **Sources:** conversations/conv_pines018_item_transfer.eml
- **Evidence:** "with 9.6 million items, batch updates need to be efficient.", "We should process in smaller batches to avoid locking the database."
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall process large-scale batch location updates in smaller sub-batches (or otherwise use techniques) to avoid locking the database when updating many items.

### REQ-037: Monthly missing and damaged items report per branch

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Directly stated as a core requirement for inventory audit and collection management; also explicitly repeated in the 'clarify the requirements' email and summary consolidation.
- **Sources:** conversations/conv_pines019_020_missing_intransit.eml
- **Evidence:** "System provides reports of missing and damaged items per branch.", "MISSING AND DAMAGED ITEMS REPORT: System provides reports of missing and damaged items per branch.", "Missing and Damaged Items Report: 'System provides reports of missing and damaged items per branch.'"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall provide a report of missing and damaged items per branch (for example: a monthly report to support inventory audit and collection management).

### REQ-038: In-transit items report for items in transit longer than configurable X days

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicitly required and repeated with configurability; central to in-transit reporting.
- **Sources:** conversations/conv_pines019_020_missing_intransit.eml
- **Evidence:** "System generates a list of items that have been in-transit for more than X days (X configurable)", "report of items that have been in-transit for more than X days (X should be configurable, probably 7 days default).", "In-transit items report... X days (X configurable)"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall generate a report listing items that have been in-transit for more than X days, where X is configurable (for example: default X = 7 days).

### REQ-039: In-transit report scope per branch and per system

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicitly stated as 'per branch and per system' in requirement clarifications and summary.
- **Sources:** conversations/conv_pines019_020_missing_intransit.eml
- **Evidence:** "...per branch and per system.", "In-transit Items Report: System generates a list of items in-transit for more than X days (X configurable), per branch and per system."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall provide the in-transit items report scoped both per branch and for the entire system.

### REQ-040: Merge transit-to and transit-from in in-transit report

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicitly requested to avoid running two reports; repeated in clarification and summary.
- **Sources:** conversations/conv_pines019_020_missing_intransit.eml
- **Evidence:** "The report should merge transit-to and transit-from so front-line staff don't have to run two reports.", "...Report merges transit-to and transit-from into one report.", "...merges transit-to and transit-from into one report."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall merge transit-to and transit-from information into a single in-transit report so front-line staff do not have to run two separate reports.

### REQ-041: Sort in-transit report by due date

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicitly requested for operational use; not described as critical like the core report existence/merge/scope.
- **Sources:** conversations/conv_pines019_020_missing_intransit.eml
- **Evidence:** "Also, for the in-transit report - can we sort by due date?", "Front-line staff need to chase the oldest items first."
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall allow the in-transit items report to be sorted by due date to enable front-line staff to address oldest items first.

### REQ-042: Missing/damaged report supports date ranges for trending

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicitly proposed as useful capability; technical note ties it to feasibility.
- **Sources:** conversations/conv_pines019_020_missing_intransit.eml
- **Evidence:** "The missing/damaged report can include date ranges (e.g., last 30 days, last quarter, etc.) which would be useful for trending."
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall allow missing/damaged item reports to be generated for specified date ranges (for example: last 30 days or last quarter) to enable trending analysis.

### REQ-043: Identify in-transit items with missing arrival and old departure

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Stated as a technical note for feasibility; not presented as an explicit user-facing requirement by the group but describes implementation behavior.
- **Sources:** conversations/conv_pines019_020_missing_intransit.eml
- **Evidence:** "For in-transit items, we need to check the transit table for items where the arrival date is null and the departure date is more than X days ago."
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall determine in-transit items by checking the transit table for items where arrival date is null and the departure date is more than X days ago.

### REQ-044: Missing/damaged report grouped by branch

- **Category:** functional
- **Priority:** P3 (source-supported)
- **Priority rationale:** Technical feasibility note; wording implies internal query approach rather than an explicit user-facing requirement.
- **Sources:** conversations/conv_pines019_020_missing_intransit.eml
- **Evidence:** "We can query for items with status 'missing' or 'lost' and group by branch."
- **Manual provenance review required:** No
- **Confidence:** low
- **Related questions/dependencies:** —

System shall be able to query items with status 'missing' or 'lost' and group results by branch for the missing/damaged report.

### REQ-045: Purge candidate identification utility and reports

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicitly listed as the primary weeding requirement and core of the purging utility in the thread.
- **Sources:** conversations/conv_pines021_item_purging.eml
- **Evidence:** "I need to identify item records to purge based on customizable criteria.", "The system should provide a utility and reports for identifying item records to purge, based on customizable criteria"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall provide a utility and reports for identifying item records to purge based on customizable criteria.

### REQ-046: Purge criteria: status-based and time-based

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Directly enumerated as part of customizable criteria and explicitly includes status and time dimensions.
- **Sources:** conversations/conv_pines021_item_purging.eml
- **Evidence:** "Status-based criteria (missing, discard/weed, damaged)", "Time-based criteria (in status for X months/years)", "For example: Item has been in status 'missing' for more than X months", "The system should provide... criteria such as: - An item has been in status 'missing' for more than X months"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall allow customizable purge criteria that include status-based criteria (e.g., missing, discard/weed, damaged) and time-based criteria (e.g., in status for more than X months/years).

### REQ-047: Purge criteria: activity-based (last-circulated)

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicitly requested and included in the criteria combination examples.
- **Sources:** conversations/conv_pines021_item_purging.eml
- **Evidence:** "Activity-based criteria (last circulated X days/months/years ago)", "I might want to purge items: ... That haven't circulated in 5+ years", "...Status 'missing' for 2+ years", "...AND haven't circulated in 2 years"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall allow customizable purge criteria that include activity-based criteria such as last-circulated X days/months/years ago.

### REQ-048: Combine multiple purge criteria in rules

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicitly asked and confirmed; described as ability to combine criteria.
- **Sources:** conversations/conv_pines021_item_purging.eml
- **Evidence:** "Can we combine these? Like "items with status 'missing' for more than 6 months AND haven't circulated in 2 years"?", "The system should let us combine criteria.", "The system should provide... customizable criteria such as" (followed by examples)
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall allow users to combine purge criteria, such as conjunctions between status, time-in-status, and last-circulated conditions (e.g., status 'missing' for more than 6 months AND not circulated in 2 years).

### REQ-049: Read-only purge candidate reports

- **Category:** security
- **Priority:** P1 (source-supported)
- **Priority rationale:** Safety measure explicitly required to prevent accidental deletions.
- **Sources:** conversations/conv_pines021_item_purging.eml
- **Evidence:** "Reports show candidates for purging (read-only)", "Safety measures: - Read-only reports for identifying candidates"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall provide read-only reports for identifying candidates for purging.

### REQ-050: Separate confirmation step before purging/deleting items

- **Category:** security
- **Priority:** P1 (source-supported)
- **Priority rationale:** Safety requirement explicitly stated as a separate step.
- **Sources:** conversations/conv_pines021_item_purging.eml
- **Evidence:** "A separate confirmation step for actual deletions", "Safety measures: - ... Separate confirmation step for actual deletions"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall require a separate confirmation step before performing actual item purges/deletions.

### REQ-051: Audit trail for all purges

- **Category:** security
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicitly required for accountability and troubleshooting; repeated in the thread.
- **Sources:** conversations/conv_pines021_item_purging.eml
- **Evidence:** "Audit trail for all purges", "We need to track who purged what and when.", "Safety measures: - Audit trail for all purges"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall maintain an audit trail for all purges, including who purged what and when.

### REQ-052: Batch convert items from one status to another

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Directly requested as a key weeding reporting need; explicitly summarized later.
- **Sources:** conversations/conv_pines021_item_purging.eml
- **Evidence:** "I need a report to help convert items from one status to another in batch.", "Provide a report to assist in the conversion of items from one status to another"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall provide a report/feature to convert items from one status to another in batch.

### REQ-053: Last copy report available per library and per system (consortium) scope

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicit and described as critical to avoid deleting the only copy at the consortium level; emphasized that the report must be available per system as well as per library.
- **Sources:** conversations/conv_pines021_item_purging.eml
- **Evidence:** "CRITICAL: We need a 'last copy report' that identifies our library system's last copies... so we don't accidentally delete the only copy in the consortium.", "For the last copy report... we need both views... per library or per system?", "...last copy report singling out a library system's last copies", "Also... last copy report should definitely be available per system", "This is all great. One more thing - the 'last copy report' should definitely be available per system, not just per library.", "We need both views. Sometimes we delete the last copy at our branch, sometimes the last copy in the entire PINES system."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall provide a last copy report that identifies a library system's last copies in the specified scope (library or system) and make that report available both per library and at the consortium/system scope.

### REQ-054: Last copy report shall flag items that are the only copy in the specified scope

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Stated as a technical rule in the purging thread; presented as the needed logic but not explicitly confirmed as final behavior, hence lower priority than some user-facing items.
- **Sources:** conversations/conv_pines021_item_purging.eml
- **Evidence:** "For the last copy report, the system would check: for each item record, is this the only copy in the specified scope (library or system)? If yes, flag it."
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall, for each item record, check whether it is the only copy in the specified scope (library or system) and flag it in the last copy report.

### REQ-055: Quick deletion of volume entries, related copy entries, and records with no items

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicitly requested cleanup utility capability; details about automation vs. manual operation were not specified as requirements.
- **Sources:** conversations/conv_pines021_item_purging.eml
- **Evidence:** "We also need a quick way to delete volume entries along with copy entries, and delete records with no items attached.", "Provide a quick effective method for deleting volume entries along with copy entries, as well as records with no items attached"
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall provide a quick effective method of deleting volume entries along with copy entries, and deleting records with no items attached.

### REQ-056: Schedulable purging utility

- **Category:** functional
- **Priority:** P3 (estimated)
- **Priority rationale:** Asked as an additional capability; not incorporated into the formal summary section of requirements and marked as a lower/optional capability.
- **Sources:** conversations/conv_pines021_item_purging.eml
- **Evidence:** "Also wondering - can the purging utility be scheduled? Like, run automatically at the end of each year?"
- **Manual provenance review required:** No
- **Confidence:** low
- **Related questions/dependencies:** —

System shall support scheduling the purging utility to run automatically at the end of each year.

### REQ-057: DeletionTracking_CountAndTrackPerLocationAndSystem

- **Category:** business rule
- **Priority:** P1 (source-supported)
- **Priority rationale:** Directly stated as needed for auditing and for reporting deletions by location and system; consolidated requirement.
- **Sources:** conversations/conv_pines022_deletions.eml
- **Evidence:** "We need to be able to count and track record deletions ... per location and per system. This is for auditing purposes.", "Additionally, tracking of denied deletion attempts would be helpful for compliance and troubleshooting.", "The system should count and track record deletions ... per location and per system."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall count and track record deletions (item, patron, and bibliographic) per location and per system for auditing purposes.

### REQ-058: DeletionTracking_AuditFieldsLogged

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Database-trigger and audit-table fields are explicitly specified as an implementation approach and data requirements.
- **Sources:** conversations/conv_pines022_deletions.eml
- **Evidence:** "To implement this, we'd need: 1. A trigger in the database that logs deletions to an audit table", "Fields: record_type, record_id, deleted_by, deleted_at, location"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall log deletion events into an audit table including at least: record type, record identifier, deleted_by (user id), deleted_at (timestamp), and location.

### REQ-059: DeletionTracking_ReportInterfaceQueryAuditTable

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicitly requested to implement with a report interface over the audit table.
- **Sources:** conversations/conv_pines022_deletions.eml
- **Evidence:** "A report interface to query this audit table", "The report should show deletions per location and per system."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall provide a report interface that can query the deletion audit table to produce human-readable reports.

### REQ-060: DeletionTracking_ReportAggregations

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Aggregation dimensions are explicitly listed.
- **Sources:** conversations/conv_pines022_deletions.eml
- **Evidence:** "The report should show deletions per location and per system. We can aggregate by date range, by user, by record type."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall allow deletion reports to aggregate deletion counts by date range, by user, and by record type.

### REQ-061: DeletionTracking_AdminReportsTotalsAndTopUsers

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Administrative reporting requirements are explicitly enumerated.
- **Sources:** conversations/conv_pines022_deletions.eml
- **Evidence:** "we need reports showing:", "Total deletions per period (month, quarter, year)", "Deletions by type (item vs patron vs other)", "Deletions by location", "Top users who delete the most records"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall support administrative reports including: total deletions per period (month, quarter, year), deletions by type (item vs patron vs other), deletions by location, and top users who delete the most records.

### REQ-062: DeniedDeletionAttempts_TrackAndReport

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Requested as an additional helpful capability for compliance and troubleshooting.
- **Sources:** conversations/conv_pines022_deletions.eml
- **Evidence:** "Can we also track attempted deletions that were denied? That would tell us if someone is trying to delete things they shouldn't.", "Additionally, tracking of denied deletion attempts would be helpful for compliance and troubleshooting."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall track attempted deletions that are denied and include those denied-attempt records in audit logs and reports for compliance and troubleshooting.

### REQ-063: PatronCharacteristics_QueryLimitAndGroupBy

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Both capabilities are explicitly required and consolidated.
- **Sources:** conversations/conv_pines023_patron_characteristics.eml
- **Evidence:** "I need to be able to both LIMIT and GROUP BY patron characteristics.", "Requirement consolidated", "Both LIMIT (filter) and GROUP BY (aggregate) should be supported"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall allow patron characteristic queries and reports to support both LIMIT-style filters and GROUP BY-style aggregations.

### REQ-064: PatronCharacteristics_SupportedFields

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Field list is explicitly consolidated as included characteristics.
- **Sources:** conversations/conv_pines023_patron_characteristics.eml
- **Evidence:** "The fields I need: - Age range - Zip code - County of residence - Home branch - Patron type - Preferred language", "The system should allow queries and reports to be limited or grouped by various patron characteristics, including:", "Age range", "Zip code", "County of residence", "Home branch", "Patron type", "Preferred language"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall support queries and reports that can limit or group by the following patron characteristics: age range, ZIP code, county of residence, home branch, patron type, and preferred language.

### REQ-065: PatronCharacteristics_ConfigureAgeRanges

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicitly stated as needed to configure brackets.
- **Sources:** conversations/conv_pines023_patron_characteristics.eml
- **Evidence:** "The age ranges need to be configurable too. Like, 0-5, 6-10, 11-15, etc.", "Age ranges should be configurable per report"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall allow the age-range brackets used for reporting (for example 0-5, 6-10, 11-15, etc.) to be configurable per report.

### REQ-066: PatronCharacteristics_CombineFiltersWithAndOr

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicitly required and consolidated.
- **Sources:** conversations/conv_pines023_patron_characteristics.eml
- **Evidence:** "Combining filters is also doable - just add WHERE clauses. We can support both AND and OR logic.", "Filters can be combined with AND/OR logic"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall allow combining patron characteristic filters using both AND and OR logical operators.

### REQ-067: PatronCharacteristics_IncludeNullsForMissingData

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicitly stated to include nulls rather than silently excluding them.
- **Sources:** conversations/conv_pines023_patron_characteristics.eml
- **Evidence:** "One consideration: if patrons haven't provided optional fields, they'll show up as null. We should include them in the report (with null values) rather than excluding them, because excluding data silently can lead to misleading results.", "Null values should be included in results"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall include null (or empty) values in patron characteristic report results for optional characteristics that are not consistently populated, rather than silently excluding those records.

### REQ-068: InactivePatrons_GenerateList

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Directly stated as the consolidated requirement.
- **Sources:** —
- **Evidence:** "The system should generate a list of patrons with no circulation or electronic activity in the last X days (X configurable)."
- **Manual provenance review required:** Yes
- **Confidence:** high
- **Related questions/dependencies:** —

System shall generate a list of patrons with no circulation activity and no electronic activity in the last X days, where X is configurable.

### REQ-069: InactivePatrons_DefineElectronicActivity

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicitly enumerated in the consolidated requirement; also clarified in the email thread.
- **Sources:** —
- **Evidence:** "Electronic activity includes OPAC login, online hold placement, online renewals.", ""Electronic activity" should include: 1. Logging into OPAC/patron account 2. Placing holds online 3. Renewing items online"
- **Manual provenance review required:** Yes
- **Confidence:** high
- **Related questions/dependencies:** —

System shall treat electronic activity, for the purpose of identifying inactive patrons, as including at minimum: OPAC/patron account login, online hold placement, and online renewals.

### REQ-070: InactivePatrons_DigitalResourceAccessConditional

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Stated as conditional/conditional scope; appears in clarifications rather than the final consolidated summary.
- **Sources:** —
- **Evidence:** "Accessing digital collections (if integrated)", "Digital resource access (if logged)"
- **Manual provenance review required:** Yes
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall include access to integrated digital collections as electronic activity for inactive-patron detection when that access is integrated into the system and the access events are logged.

### REQ-071: InactivePatrons_ConfigurableInactivityWindow

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicitly stated in consolidated requirement and initial request.
- **Sources:** conversations/conv_pines024_inactive_patrons.eml
- **Evidence:** "X should be configurable", "last X days (X configurable)"
- **Manual provenance review required:** Yes
- **Confidence:** high
- **Related questions/dependencies:** —

System shall allow the inactivity window X (the number of days defining inactivity) to be configured.

### REQ-072: Configurable inactive-patrons report scope levels

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicitly listed in the consolidated requirement and requested by stakeholders as needed levels.
- **Sources:** conversations/conv_pines024_inactive_patrons.eml
- **Evidence:** "The list should be configurable to: - System - Home Library - County", "For the configurable levels - I'd want System and Home Library."
- **Manual provenance review required:** Yes
- **Confidence:** high
- **Related questions/dependencies:** —

System shall allow the inactive patrons list/report to be configurable to scope levels including System, Home Library, and County.

### REQ-073: Support additional scope levels for inactive-patrons report

- **Category:** functional
- **Priority:** P3 (source-supported)
- **Priority rationale:** Implied as lower-priority extension by the consolidated requirement note '(Other levels as needed)'.
- **Sources:** —
- **Evidence:** "- County - (Other levels as needed)"
- **Manual provenance review required:** Yes
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall support additional configurable scope levels for the inactive patrons report beyond System, Home Library, and County as needed.

### REQ-074: Include current mailing addresses in inactive-patrons report

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicitly called out as an additional consideration for outreach use in the consolidated requirement.
- **Sources:** conversations/conv_pines024_inactive_patrons.eml
- **Evidence:** "Additional considerations: - Include current mailing addresses for outreach", "the report needs to include current mailing addresses."
- **Manual provenance review required:** Yes
- **Confidence:** high
- **Related questions/dependencies:** —

System shall include current mailing addresses in the inactive patrons report to support outreach activities.

### REQ-075: Differentiate inactive patrons with outstanding fines

- **Category:** business rule
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicitly stated as an additional consideration; stakeholders indicated such patrons should be handled differently.
- **Sources:** conversations/conv_pines024_inactive_patrons.eml
- **Evidence:** "Track inactive patrons with outstanding fines separately", "we should probably handle those differently."
- **Manual provenance review required:** Yes
- **Confidence:** high
- **Related questions/dependencies:** —

System shall identify and track inactive patrons who have outstanding fines separately and allow them to be handled differently than inactive patrons without fines.

### REQ-076: Exclude specified patrons from inactive report

- **Category:** business rule
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicit requirement with specific examples provided by stakeholders.
- **Sources:** conversations/conv_pines024_inactive_patrons.eml
- **Evidence:** "we should be able to EXCLUDE certain patrons from the inactive report", "- Patrons with \"do not disturb\" flags - VIP patrons - Staff members - Patrons who have opted out of communications"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall allow exclusion of specified patrons from the inactive patrons report (examples: patrons with 'do not disturb' flags, VIP patrons, staff members, patrons who have opted out of communications).

### REQ-077: Export inactive-patrons report to CSV

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicitly stated in the consolidated requirement and needed to support stakeholder workflow of uploading to an outreach system.
- **Sources:** conversations/conv_pines024_inactive_patrons.eml
- **Evidence:** "Exportable format (CSV)", "Also, the report should be exportable. We upload it to our outreach system."
- **Manual provenance review required:** Yes
- **Confidence:** high
- **Related questions/dependencies:** —

System shall export the inactive patrons report in an exportable CSV format suitable for upload to external outreach systems.

### REQ-078: Background processing for inactive-patrons report

- **Category:** non-functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicitly mentioned as a performance/background-processing requirement to avoid disruption and improve responsiveness.
- **Sources:** —
- **Evidence:** "Background processing for performance", "We should run it as a background report and cache results."
- **Manual provenance review required:** Yes
- **Confidence:** high
- **Related questions/dependencies:** —

System shall generate the inactive patrons report via background processing to avoid performance impacts on interactive system usage for large patron populations.

### REQ-079: Cache results of background inactive-patrons report

- **Category:** non-functional
- **Priority:** P3 (source-supported)
- **Priority rationale:** Caching was mentioned as a performance optimization; it is explicit in the thread but not emphasized as top priority.
- **Sources:** —
- **Evidence:** "and cache results"
- **Manual provenance review required:** Yes
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall cache the results of the background inactive patrons report to improve performance and avoid repeatedly running the expensive query.

### REQ-080: Performance optimization for very large patron populations

- **Category:** non-functional
- **Priority:** P3 (estimated)
- **Priority rationale:** Stakeholders noted the large scale as a concern and requested optimization; priority is estimated as medium because it is an implementation/performance tuning item rather than a functional must-have.
- **Sources:** —
- **Evidence:** "For 3.5 million patrons, this query could be slow.", "Action: Robert will optimize the query."
- **Manual provenance review required:** Yes
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall be optimized so that the inactive patrons query/report performs acceptably for patron populations on the order of millions (example cited: ~3.5 million patrons).

### REQ-081: Support consortium scale (capacity requirement)

- **Category:** business rule
- **Priority:** P1 (source-supported)
- **Priority rationale:** Marked explicitly as high priority in OE-1.
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** OE-1: The system must support a library consortium with 286 locations, 17 million annual circulations, and purchasing/processing over 900,000 items per year., OE-1: [* High Priority]
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall support operation for a library consortium at the cited scale (example metrics: 286 locations, 17 million annual circulations, and purchasing/processing over 900,000 items per year).

### REQ-082: Process searches and reports during open hours without disruption (desirable)

- **Category:** constraint
- **Priority:** P2 (estimated)
- **Priority rationale:** OE-1 frames this as a highly desirable capability; treated as medium priority (desire rather than mandatory).
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** OE-1: It is highly desirable that searches and reports can be processed during open hours without disrupting other system functions., OE-1: [* High Priority]
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

It is highly desirable that the system be able to process searches and reports during open hours without disrupting other system functions.

### REQ-083: Supported server environments (Linux or Solaris)

- **Category:** constraint
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicit high-priority marker in OE-2.
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** OE-2: The system must operate on a Linux or Solaris server environment., OE-2: [* High Priority]
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall operate on a Linux or Solaris server environment.

### REQ-084: Client access methods (web or Windows client)

- **Category:** constraint
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicit high-priority marker in OE-3.
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** OE-3: The system must be accessible through a web browser or a Windows-compatible client., OE-3: [* High Priority]
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall be accessible through a web browser or a Windows-compatible client.

### REQ-085: Web-browser support (IE and Firefox versions)

- **Category:** constraint
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicit medium-priority marker in OE-4.
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** OE-4: If web-browser based, the system must be accessible through Microsoft Internet Explorer (version 6.0 and later) and Mozilla Firefox (version 2.0 and later)., OE-4: [* Medium Priority]
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

If the system is web-browser based, it shall be accessible through Microsoft Internet Explorer (version 6.0 and later) and Mozilla Firefox (version 2.0 and later).

### REQ-086: Assistive-technology accessibility

- **Category:** constraint
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicit high-priority marker in OE-5.
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** OE-5: The system must be accessible with screen-reading software, screen-magnification software, and other assistive technology programs designed to increase accessibility., OE-5: [* High Priority]
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall be accessible with screen-reading software, screen-magnification software, and other assistive technology programs designed to increase accessibility.

### REQ-087: CO-1_RelationalDatabaseBackend

- **Category:** constraint
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicit [* High Priority] marker in CO-1.
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** CO-1: The system must use a fully relational database back-end., CO-1: [* High Priority]
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall use a fully relational database back-end.

### REQ-088: CO-2_StandardsCompliantHTMLOutput

- **Category:** constraint
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicit [* High Priority] marker in CO-2.
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** CO-2: The system must produce standards-compliant HTML output for web-based components., CO-2: [* High Priority]
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall produce standards-compliant HTML output for web-based components.

### REQ-089: CO-3_DevAndTrainingEnvironmentWithConfigMigration

- **Category:** constraint
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicit Medium Priority marker in CO-3.
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** CO-3: The system must provide a development and training environment with the ability to migrate configurations to a production environment., CO-3: [* Medium Priority]
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall provide a development and training environment with the ability to migrate configurations to a production environment.

### REQ-090: CO-4_RoleBasedAccessControl

- **Category:** security
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicit [* High Priority] marker in CO-4.
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** CO-4: User rights and privileges will be controlled through security groups and or "roles" that allow access control for individuals, workgroups, and arbitrary staff groups., CO-4: [* High Priority]
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall control user rights and privileges through security groups and/or roles that allow access control for individuals, workgroups, and arbitrary staff groups.

### REQ-091: CO-5_NoConstraintOnOPACFunctionality

- **Category:** constraint
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicit [* High Priority] marker in CO-5.
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** CO-5: These requirements must not constrain functionality or features of the Online Public Access Catalog (OPAC) module., CO-5: [* High Priority]
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System requirements shall not constrain functionality or features of the Online Public Access Catalog (OPAC) module.

### REQ-092: UD-1_DeveloperDataSpecificationsForRecordTypes

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicit [* High Priority] marker in UD-1 (though phrased as "developer must").
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** UD-1: The developer must provide complete data specifications for authority records, bibliographic records, order records, item records, hold/request records, and other records maintained or accessed by the Management Processes., UD-1: [* High Priority]
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall provide complete data specifications for authority records, bibliographic records, order records, item records, hold/request records, and other records maintained or accessed by the Management Processes.

### REQ-093: UD-2_HighLevelProcessDescriptionDocumentation

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicit Medium Priority marker in UD-2.
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** UD-2: The developer must provide a thorough high-level description of major processes, including bibliographic record import and export, validation of bibliographic records against internal and external authority sources, and standard reports., UD-2: [* Medium Priority]
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall provide a thorough high-level description of major processes, including bibliographic record import and export, validation of bibliographic records against internal and external authority sources, and standard reports.

### REQ-094: UD-3_OnlineHierarchicalCrossLinkedHTMLHelp

- **Category:** usability
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicit [* High Priority] marker in UD-3.
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** UD-3: The system must provide an online, hierarchical, and cross-linked help system in HTML that describes and illustrates all system functions., UD-3: [* High Priority]
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall provide an online, hierarchical, and cross-linked help system in HTML that describes and illustrates all system functions.

### REQ-095: UD-4_ErrorReportingFeedbackAndAdminQuerySpecificFeedback

- **Category:** usability
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicit Medium Priority marker in UD-4.
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** UD-4: The system must provide thorough high-level error reporting and feedback, and shall allow low-level query-specific feedback for Local and Global System Administrators from the front-end interface., UD-4: [* Medium Priority]
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall provide thorough high-level error reporting and feedback and shall allow low-level query-specific feedback for Local and Global System Administrators from the front-end interface.

### REQ-096: FR-StaffLogin_StreamlinedAndFallback

- **Category:** functional
- **Priority:** P3 (estimated)
- **Priority rationale:** FR section states "should" and includes explicit fallback/exception; no explicit priority marker shown for 8.1. Priority set to P3 and marked as estimated.
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** 8.1 Staff Login: The system should support streamlined methods of logging into terminals., 8.1 Staff Login: For example, a staff member could swipe a card (like an RFID employee badge) to log in, or alternatively use individual login credentials (username and password)., 8.1 Staff Login: The system should not REQUIRE card-based login - traditional username/password should also be available as a fallback.
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall support streamlined methods of logging into terminals, including card-based login such as swiping an RFID employee badge and/or login using individual login credentials (username and password) as a fallback, and shall not require card-based login.

### REQ-097: FR-ReportTemplates_CreateAndRunOrModify

- **Category:** functional
- **Priority:** P3 (estimated)
- **Priority rationale:** Section uses "should" and no priority marker for 8.2; priority is estimated as P3.
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** 8.2 Report Templates: System administrators should be able to create report templates that are available to staff., 8.2 Report Templates: These templates should be runnable as-is or modifiable for individual needs., 8.2 Report Templates: Changes to templates should not compromise the accuracy of results.
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall allow system administrators to create report templates that are available to staff and that are runnable as-is or modifiable for individual needs without compromising the accuracy of results.

### REQ-098: FR-ReportTemplates_LimitAlterableFiltersAndFields

- **Category:** functional
- **Priority:** P3 (estimated)
- **Priority rationale:** Section uses "should" and no explicit priority marker for 8.2; priority is estimated as P3.
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** 8.2 Report Templates: Administrators should be able to limit which filters and display fields can be altered, to certify a dependable output.
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall allow administrators to limit which filters and display fields can be altered in report templates to certify dependable output.

### REQ-099: FR-ReportTemplates_ExampleConstraintOnDeletedItemsDisplay

- **Category:** functional
- **Priority:** P3 (estimated)
- **Priority rationale:** Example is stated within 8.2 but uses "should not"; no explicit priority marker for 8.2; priority is estimated.
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** 8.2 Report Templates: For example, front-line staff could set a call number range for a weeding report or add/remove display fields from a pick list, but they should not be able to alter the template to display deleted items.
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall allow staff to use report templates (with limited modification) such that they can set a call number range for a weeding report or add/remove display fields from a pick list, but they shall not be able to alter the template to display deleted items.

### REQ-100: FR-ReportPermissions_FineGrainedAndAdministerable

- **Category:** security
- **Priority:** P3 (estimated)
- **Priority rationale:** Uses "should" and no explicit priority marker for 8.3; priority is estimated as P3.
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** 8.3 Report Permissions: The system should provide distinct, fine-grained permission levels that limit who can create and clone reports., 8.3 Report Permissions: All permissions should be easy to administer.
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall provide distinct, fine-grained permission levels that limit who can create and clone reports and that are easy to administer.

### REQ-101: FR-ReportPermissions_SharedFoldersAndSpecificReportAccess

- **Category:** security
- **Priority:** P3 (estimated)
- **Priority rationale:** Uses "should" and no explicit priority marker for 8.3; priority is estimated as P3.
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** 8.3 Report Permissions: System administrators should be able to create shared folders to allow or disallow staff from running specific reports, and/or to run ad hoc reports on specific sets of data.
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall allow system administrators to create shared folders to allow or disallow staff from running specific reports and/or to run ad hoc reports on specific sets of data.

### REQ-102: FR-QueryTool_UserFriendlyQueryDesignAcrossRecordTypes

- **Category:** functional
- **Priority:** P3 (estimated)
- **Priority rationale:** Derived from early draft text using "should" and no explicit mandatory priority for Query Tool (section 8.4); treated as lower priority relative to must statements.
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** 8.4 Query Tool: The system should provide a user-friendly interface for designing queries against all record types (bibliographic, item, patron, transaction, financial).
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall provide a user-friendly interface for designing queries against all record types (bibliographic, item, patron, transaction, financial).

### REQ-103: FR-QueryTool_SelectFieldsValuesAndOperators

- **Category:** functional
- **Priority:** P3 (estimated)
- **Priority rationale:** Derived from descriptive draft text using "Staff should be able to" (section 8.4); treated as a recommended usability/feature item rather than an immediately mandatory item.
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** 8.4 Query Tool: Staff should be able to: Select fields to query; Select values from a picklist of possible values; Select regular expressions from a drop-down menu; Use a full range of Boolean operators.
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall allow staff to select fields to query, choose values from a picklist of possible values, select regular expressions from a drop-down menu, and use a full range of Boolean operators when designing queries.

### REQ-104: FR-QueryTool_AdminControlsTableAndFieldAccess

- **Category:** security
- **Priority:** P3 (estimated)
- **Priority rationale:** Stated as administrative control in the draft (section 8.4); prioritized as medium since it is an access-control/security configuration rather than a core system capability.
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** 8.4 Query Tool: Administrators should control staff access to tables and fields.
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall allow administrators to control staff access to tables and fields for query design and execution.

### REQ-105: FR-BoardReports_PredefinedReportsForExternalConsumers

- **Category:** functional
- **Priority:** P3 (estimated)
- **Priority rationale:** Draft language uses "should" for Board/Executive Reports (section 8.5), so treated as recommended rather than mandatory.
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** 8.5 Board Reports / Executive Reports: The system should provide pre-defined reports for consumption by library boards and other external consumers.
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall provide pre-defined reports for consumption by library boards and other external consumers.

### REQ-106: FR-BoardReports_BasicStatisticsForStateAid

- **Category:** functional
- **Priority:** P3 (estimated)
- **Priority rationale:** Draft uses "should" and cites example outputs (Georgia Annual Report), so treated as recommended content for board reports rather than a must-have system capability.
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** 8.5 Board Reports / Executive Reports: These should include basic statistics like those required by the Georgia Annual Report and Application for State Aid.
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall include basic statistics in board/executive pre-defined reports like those required by the Georgia Annual Report and Application for State Aid.

### REQ-107: FR-BoardReports_ActivityReportsIndicateTrafficAndVolumeOfUse

- **Category:** functional
- **Priority:** P3 (estimated)
- **Priority rationale:** Draft uses "should" for activity reports; priority retained as estimated medium/low because the source text is truncated and partially specified.
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** 8.5 Board Reports / Executive Reports: Activity reports should indicate traffic and volume of use, displaying
- **Manual provenance review required:** No
- **Confidence:** low
- **Related questions/dependencies:** —

System shall provide activity reports that indicate traffic and volume of use.

### REQ-108: FR-Reporting_CrossTabulateDemographicTransactionData

- **Category:** functional
- **Priority:** P1 (estimated)
- **Priority rationale:** Described as a core reporting capability in the draft; treated as high priority (P1).
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** "It should be possible to cross-tabulate per terminal, per branch, per library system, per hour, per patron age range, per patron type, and per patron location."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall allow cross-tabulation of statistics by terminal, branch, library system, hour, patron age range, patron type, and patron location.

### REQ-109: SEC-ArchiveAndAnonymizeTransactionsForDemographicReporting

- **Category:** security
- **Priority:** P1 (source-supported)
- **Priority rationale:** Both source candidates specify privacy/anonymization and legal protection as required; privacy protection for archived transaction data and anonymized reporting is treated as mandatory/high priority.
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** "Transactions should be archived in a form that protects patron privacy as defined by State Law, while providing useful demographic statistics.", "The data used to produce these statistics must be anonymized - information that could be used to identify a patron is deleted.", "including transactions by geographical regions, age ranges, etc."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall archive transaction data in a form that protects patron privacy as defined by applicable State law, and shall produce demographic statistics from data anonymized by removing information that could be used to identify a patron.

### REQ-110: FR-Reporting_DisplayQuerySelectionsWithResults

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Usability requirement for reporting outputs; prioritized as P2 (operational usability rather than core system capability).
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** "The system should provide the query selections along with the results, so users can see what criteria were used to generate the report."
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall display the query selections along with the report results so users can see the criteria used to generate the report.

### REQ-111: FR-Reporting_ShowReportQueuePositionToStaff

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Operational transparency for asynchronous reporting; not a core data capability but important for staff operations.
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** "Staff should be able to see where their report is in the queue of reports waiting to run."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall allow staff to see where their report is in the queue of reports waiting to run.

### REQ-112: FR-Reporting_SupportDefinitionsFromAppendixA

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Draft uses an explicit must-statement for Appendix A report definitions; treated as high priority (P1).
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** "The system must be able to support the reporting definitions as described in the attached report examples (see Appendix A)."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall support the reporting definitions described in the attached report examples (Appendix A).

### REQ-113: FR-Reporting_SupportFineGrainedRequirementsFromAppendixB

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Draft uses an explicit must-statement for Appendix B fine-grained reporting; treated as high priority (P1).
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** "The system must be able to support the fine-grained reports requirements as described in the attached specification (see Appendix B)."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall support the fine-grained report requirements as described in the attached specification (Appendix B).

### REQ-114: FR-Analytics_ProducePatronBehaviorAndUseStatistics

- **Category:** functional
- **Priority:** P1 (estimated)
- **Priority rationale:** Draft describes this analytical capability as an important system capability; treated as high priority though original phrasing used "should" so priority_is_estimated is true.
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** "The system should produce statistics that can be used to understand and predict patron behavior and use of materials."
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall produce statistics that can be used to understand and predict patron behavior and use of materials.

### REQ-115: FR-Analytics_Examples_AverageReturnTimeAndRenewalLikelihood

- **Category:** functional
- **Priority:** P3 (estimated)
- **Priority rationale:** Given in the draft as examples of broader analytics; prioritized lower (P3) as illustrative rather than standing alone as a mandated capability.
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** "How quickly is a particular book returned, on average?", "How likely is a particular book to be renewed?"
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall provide analytics examples such as average return time for a particular book and the likelihood that a particular book will be renewed.

### REQ-116: Generate material volume report by time and category

- **Category:** functional
- **Priority:** P1 (estimated)
- **Priority rationale:** Inventory reporting capability is explicitly required.
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** "Ability to report on the volume of material in a given library at any point in time, based on new acquisitions, items on the shelf, and items out in circulation.", "The report should allow breaking down volume in categories such as: total items in library, number of holds, number of adult fiction, number of board books, etc."
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall provide the ability to report the volume of material in a given library at any point in time based on new acquisitions, items on the shelf, and items out in circulation, with breakdown by categories such as total items in library, number of holds, number of adult fiction, and number of board books.

### REQ-117: Provide system capacity interface by branch

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicit interface requirement.
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** "The system should provide an interface showing the capacity of all branches."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall provide an interface showing the capacity of all branches.

### REQ-118: Shelf space report compare circulations, collection share, and shelf space share

- **Category:** functional
- **Priority:** P2 (estimated)
- **Priority rationale:** Explicit comparative reporting requirement.
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** "For each genre and format of material, ability to compare: The percentage of total circulations; The percentage of the collection; The percentage of total shelf space"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall provide a shelf space report that, for each genre and format, allows comparison of the percentage of total circulations, the percentage of the collection, and the percentage of total shelf space.

### REQ-119: Shelf space report supports per library and per system execution

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicit execution scope.
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** "The report should be able to run per library and per system."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall allow the shelf space report to run per library and per system.

### REQ-120: Control inventory of uncataloged material with usage tracking

- **Category:** functional
- **Priority:** P1 (estimated)
- **Priority rationale:** Explicit inventory control and statistics integration requirement.
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** "Ability to control inventory of uncataloged material, such as paperback books and children's board books.", "Support needed for: Quick distribution; Minimal branch labor; Ability to identify how the material is being used", "Ability to count transactions and include in circulation statistics and reports."
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall support inventory control for uncataloged material (for example paperback books and children's board books), including support for quick distribution, minimal branch labor, the ability to identify how the material is being used, and shall count transactions and include them in circulation statistics and reports.

### REQ-121: Transfer utility for batches of items between branches

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicit required utility.
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** "System should provide a utility for transferring batches of items between branches."
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall provide a utility for transferring batches of items between branches.

### REQ-122: Transfer utility query candidate materials

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Capability listed as part of transfer utility.
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** "The utility should include: Ability to query for candidate materials"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall allow the transfer utility to query for candidate materials.

### REQ-123: Transfer utility save queries for repeated use

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Capability listed as part of transfer utility.
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** "The utility should include: Ability to save queries for repeated use"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall allow the transfer utility to save queries for repeated use.

### REQ-124: Transfer utility manual selection from query results

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Capability listed as part of transfer utility.
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** "The utility should include: Ability to manually select titles from query results"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall allow the transfer utility to manually select titles from query results.

### REQ-125: Transfer utility change selected item location

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Core transfer operation explicitly required.
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** "Ability to change records of selected items to move to new location"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall allow the transfer utility to change records of selected items to move them to a new location.

### REQ-126: Transfer utility support moving mechanisms (location field and pull lists)

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicit mechanisms required as part of transfer utility.
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** "Mechanisms for moving items: changing location field, generating pull lists"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall provide mechanisms for moving items including changing the location field and generating pull lists.

### REQ-127: Transfer utility revert items after set period

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicit feature for temporary transfers.
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** "Ability to revert items to original location after a set period of time"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall allow the transfer utility to revert items to their original location after a set period of time.

### REQ-128: Missing and damaged items report per branch

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicit reporting requirement.
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** "The system should provide reports of missing and damaged items per branch."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall provide reports of missing and damaged items per branch.

### REQ-129: In-transit items report with configurable threshold and merged transit-to/from

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicit operational report with configurable condition and merging behavior.
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** "generate a list of items that have been in-transit for more than X days (X configurable), per branch and per system.", "The report should merge the transit-to and transit-from into one report"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall generate a list of items that have been in-transit for more than X days (X configurable), per branch and per system, merging transit-to and transit-from into one report for ease of front-line staff use.

### REQ-130: Item record purging utility identifying items by customizable criteria

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicit purge identification with example criteria.
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** "The system should provide a utility and reports for identifying item records to purge, based on customizable criteria such as:", "An item has been in status \"missing\" for more than X months", "An item has status \"discard/weed\""
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall provide a utility and reports for identifying item records to purge based on customizable criteria including items in status "missing" for more than X months and items with status "discard/weed".

### REQ-131: Item record status conversion report

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicit supportive report for conversions.
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** "The system should have a report to assist in the conversion of items from one status to another."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall provide a report to assist in conversion of items from one status to another.

### REQ-132: Last-copy report to support WorldCat edits

- **Category:** functional
- **Priority:** P2 (estimated)
- **Priority rationale:** Explicit cataloging support requirement.
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** "provide a last copy report that singles out a library system's last copies, to assist catalogers who need to edit WorldCat entries."
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall provide a last copy report that singles out a library system's last copies to assist catalogers who need to edit WorldCat entries.

### REQ-133: Efficient deletion of volumes, copies, and records with no items

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicit deletion efficiency requirement and scope/conditions.
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** "provide a quick effective method of deleting volume entries along with copy entries, as well as records with no items attached."
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall provide a quick, effective method of deleting volume entries together with their copy entries, and deleting bibliographic or related records that have no item records attached.

### REQ-134: Track and count record deletions by location and system

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicit tracking requirement.
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** "Ability to count and track record deletions (e.g., item records, patron records) per location and per system."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall count and track record deletions (for example, item records and patron records) per location and per system.

### REQ-135: Limit or group patron queries and reports by patron characteristics

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicit grouping dimensions for patron reporting.
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** "Queries and reports can be limited or grouped by various patron characteristics, including:", "age range", "zip code", "county of residence", "home branch", "patron type", "preferred language"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall allow queries and reports to be limited or grouped by patron characteristics including age range, ZIP code, county of residence, home branch, patron type, and preferred language.

### REQ-136: Inactive patrons report (configurable window and scope)

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicit configurable condition and scope.
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** "no circulation or electronic activity in the last X days (X configurable).", "The list should be configurable to System, Home Library, County, etc."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall generate a list of patrons with no circulation or electronic activity in the last X days (where X is configurable), and shall allow the list scope to be configured (for example: system-wide, home library, county).

### REQ-137: Transaction history retention and indefinite aggregates

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Data retention/aggregation policy explicitly stated.
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** "Transaction history is maintained for X days (X is configurable). Monthly and annual aggregate information is maintained indefinitely."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall maintain transactional detail history for X days (where X is configurable), and shall maintain monthly and annual aggregate information indefinitely.

### REQ-138: Group transactions by hour, terminal, branch, and system

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicit grouping capability.
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** "Transactions can be grouped by hour, terminal, branch, and system."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall allow transactions to be grouped by hour, terminal, branch, and system for reporting and statistics.

### REQ-139: Query transactions by all types or by selected transaction type

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicit query flexibility.
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** "and can be queried by all transactions or by type of transaction."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall allow transactions to be queried either across all transaction types or filtered by a selected transaction type.

### REQ-140: Count check-in types individually and cumulatively (including book-drop by terminal and by user/self-service)

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicit counting requirements and breakdown dimensions.
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** "The system counts all types of check-in individually and cumulatively", "book-drop", "by terminal", "by user or self-service"
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall count all types of check-in both individually and cumulatively, including book-drop check-ins broken down by terminal and by user versus self-service.

### REQ-141: Count check-out types individually and cumulatively (detailed categories)

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicit counting with enumerated categories.
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** "The system counts all types of check-out individually and cumulatively:", "staff check-out", "self check-out", "staff renewal", "self checkout renewal", "online renewal", "OPAC renewal"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall count all types of check-out individually and cumulatively, including staff check-out, self check-out, staff renewal, self check-out renewal, online renewal, and OPAC renewal.

### REQ-142: Count hold requests and record hold placement channel

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicit holds and placement channel breakdown.
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** "The system counts all hold requests, including how the hold was placed:", "at a staff desk", "at a public computer inside the library", "remotely"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall count all hold requests and record how the hold was placed, including at a staff desk, at a public computer inside the library, and remotely.

### REQ-143: Transactions report per patron/library/scope with holds subtotaled by type

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Major reporting output with multiple scopes and subtotal rules.
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** "The system can generate a report of transactions (holds placed, holds filled, and check-outs) per patron, per library, per selected group of libraries, per system, per county.", "The system displays the number of check-outs and placed holds per patron.", "Holds are subtotaled by type, e.g., active, frozen, and frozen-until holds."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall generate a transactions report that includes holds placed, holds filled, and check-outs per patron, per library, per selected group of libraries, per system, and per county; the report shall display the number of check-outs and placed holds per patron, and it shall subtotal holds by type (for example: active, frozen, frozen-until).

### REQ-144: Report item value for entire collection or subset

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicit financial/reporting feature.
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** "The system can generate a report of the value of items (based on data in item record) in the entire collection or a portion."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall generate a report of the value of items (based on data in item records) for the entire collection or for a selected portion of the collection.

### REQ-145: Financial reporting and data archiving compliance

- **Category:** compliance
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicit compliance requirement affecting all reporting/archiving.
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** "All reports and data archiving must comply with standard accounting practice and state, county, and municipal auditing requirements."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall ensure that all reports and archived data comply with standard accounting practices and applicable state, county, and municipal auditing requirements.

### REQ-146: Attach financial transactions and waivers to patron and item records; track per-library waivers/payments

- **Category:** functional
- **Priority:** P1 (estimated)
- **Priority rationale:** The ability to attach and update financial transactions at the record level and to track waived fines/payments by library is foundational to all other financial features (reporting, reconciliation, joining item/patron data). The source (early draft) marked this as foundational.
- **Sources:** early_draft_srs_galecia.txt
- **Evidence:** "Fines, charges, waivers, and ecommerce transactions are attached to patron and item records.", "System tracks fines waived and payments made per library.", "Financial information can be updated easily."
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall attach fines, charges, waivers, and ecommerce transactions to patron and item records and shall track fines waived and payments made per library; financial information shall be updatable easily.

### REQ-147: Query patron accounts with balance greater than X dollars

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Two candidates requested the same query capability; one source (email_financial_reports.eml) provided stronger/high-confidence evidence and higher priority. The consolidated priority is set to P1 to reflect that this query capability is explicitly required for financial operations and is stated as required in the higher-confidence source.
- **Sources:** early_draft_srs_galecia.txt, email_financial_reports.eml
- **Evidence:** "As an example, a staff user can easily query patron accounts with balances greater than X dollars.", "For fines and charges, the staff should be able to query patron accounts with balances greater than X dollars.", "We need to easily query patron accounts with balances greater than X dollars."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall enable a staff user to query patron accounts with balances greater than X dollars.

### REQ-148: Financial reports: balances, accrued fines/charges by period and type, waived fines, and payments by method

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Multiple candidates (including high-confidence email_financial_reports) explicitly list these report categories as required; the consolidated requirement preserves that comprehensive, high-priority reporting need.
- **Sources:** early_draft_srs_galecia.txt, email_financial_reports.eml
- **Evidence:** "The system provides financial reports including:", "patron account balances by patron, home library, and system", "fines and charges accrued per time period", "and per type of charge", "fines waived per time period and per branch", "payments made per time period and per payment method (e.g., staff desk, self-check station, OPAC)", "Patron account balances by patron, home library, and system", "Fines and charges accrued per time period (last 12 months, YTD, last month)", "and per type of charge (overdue fines, damaged item charges, lost item charges, etc.)", "Fines waived per time period and per branch", "Fines waived should be tracked per library because each library has its own budget for waived fines.", "Payments made per time period and per payment method (staff desk, self-check station, OPAC)", "The financial reports need to show payments by method - cash, credit card, check, etc."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall provide financial reports including patron account balances by patron, home library, and system; fines and charges accrued per time period (e.g., last twelve months, YTD, last month) and per type of charge (overdue fines, damaged item charges, lost item charges, etc.); fines waived per time period and per branch/library; and payments made per time period and per payment method (e.g., staff desk, self-check station, OPAC).

### REQ-149: Maintain an audit ledger of patron payments linked to applied charges

- **Category:** compliance
- **Priority:** P1 (source-supported)
- **Priority rationale:** Multiple sources (early draft and high-confidence financial report email) call this audit trail critical for finance/reconciliation. Because both candidates explicitly require the same audit/ledger functionality, it is consolidated as P1.
- **Sources:** early_draft_srs_galecia.txt, email_financial_reports.eml
- **Evidence:** "The system maintains a ledger of patron payments, including which charges payments are applied to, to facilitate reconciliation.", "system must maintain a ledger of patron payments, including which charges payments are applied to", "The financial audit trail is CRITICAL for our finance department. They need to be able to trace every payment back to the specific charge it was applied to."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall maintain a ledger of patron payments that records which charges each payment is applied to, to facilitate reconciliation and auditing.

### REQ-150: Report value of items (with support for status and collection filters)

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** The base requirement for a value-of-items report was given P1 in the financial reporting discussion; filter examples were given as concrete dimensions. The consolidated requirement preserves the high-priority report and includes the example filters as part of the report capabilities.
- **Sources:** email_financial_reports.eml
- **Evidence:** "System can generate a report of the value of items (based on data in item record) in the entire collection or a portion.", "Examples: value of all items with status of \"longoverdue\", value of all DVDs in children's collection"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall generate a report of the value of items based on data in item records for the entire collection or for a selected portion, and shall support filtering that report by item status (e.g., "longoverdue") and by collection (e.g., DVDs in children's collection).

### REQ-151: Support joining financial data between patron and item records for reporting

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Joining patron-level and item-level financial data is explicitly required to enable accurate financial reporting and queries; the requirement is stated in high-confidence source material.
- **Sources:** email_financial_reports.eml
- **Evidence:** "For fines and charges, the staff should be able to query patron accounts", "The financial data is attached to patron records AND item records. So when we query for financial reports, we need to be able to join these data sources."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall support joining financial data attached to patron records with financial data attached to item records when generating financial reports.

### REQ-152: Compliance with accounting practice and government auditing requirements for reports and archiving

- **Category:** compliance
- **Priority:** P1 (source-supported)
- **Priority rationale:** Compliance with accounting and government auditing requirements was stated explicitly as a high-priority compliance requirement in the financial reporting discussion.
- **Sources:** email_financial_reports.eml
- **Evidence:** "All reports and data archiving must comply with standard accounting practice and state, county, and municipal auditing requirements."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall ensure that all reports and data archiving comply with standard accounting practice and state, county, and municipal auditing requirements.

### REQ-153: Enforce retention policies for archived financial data (retain some data for 7 years where required)

- **Category:** compliance
- **Priority:** P1 (source-supported)
- **Priority rationale:** Retention duration (7 years) was explicitly specified and tied to audit requirements; enforcing retention policies is a compliance necessity.
- **Sources:** email_financial_reports.eml
- **Evidence:** "Some data needs to be retained for 7 years for audit purposes.", "The system needs to enforce retention policies."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall enforce data retention policies for archived data such that some data is retained for 7 years for audit purposes (where required by applicable state and local requirements).

### REQ-154: Financial data update latency: payments reflected immediately

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicit requirement for immediate reflection after payment events.
- **Sources:** email_financial_reports.eml
- **Evidence:** "Financial information needs to be easily updatable. When a patron makes a payment at the front desk, we need the system to reflect that immediately."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall reflect updates to financial information immediately when a patron makes a payment at the front desk.

### REQ-155: Payments collected by library for end-of-month reports

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicitly stated as important for end-of-month reporting and tied to per-location visibility.
- **Sources:** email_financial_reports.eml
- **Evidence:** "Payments tracking by library is important for our end-of-month reports. Each branch needs to be able to see what payments were collected at their location."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall support tracking payments by branch so each branch can see the payments collected at its location for end-of-month reporting.

### REQ-156: Query tool: user interface for designing queries against all record types

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Listed as a key request/request item in the report features requirements thread and consolidated summary.
- **Sources:** email_report_features.eml
- **Evidence:** email_report_features.eml: "QUERY TOOL: We need a user-friendly interface for designing queries against all record types. Staff should be able to select fields to query, select values from picklists, use regular expressions from a dropdown, and use Boolean operators.", email_report_features.eml: "Consolidating the report features discussion" -> "QUERY TOOL: User-friendly interface for designing queries against all record types. Boolean operators, picklists, regex support."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall provide a user-friendly interface for designing queries against all record types, including field selection, picklist value selection, regular-expression selection, and Boolean operators.

### REQ-157: Report templates: administrators create templates available to staff

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicitly requested as a core template capability in multiple parts of the thread.
- **Sources:** email_report_features.eml
- **Evidence:** email_report_features.eml: "REPORT TEMPLATES: Admins need to create report templates that are available to staff. Templates should be runnable as-is or modified.", email_report_features.eml: "REPORT TEMPLATES: Admins create templates available to staff. Run as-is or modified."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall allow administrators to create report templates that are available to staff, and shall allow templates to be run as-is or modified by authorized staff.

### REQ-158: Report templates: modifications must not compromise results

- **Category:** business rule
- **Priority:** P1 (source-supported)
- **Priority rationale:** Stated directly as a template integrity expectation.
- **Sources:** email_report_features.eml
- **Evidence:** email_report_features.eml: "Changes shouldn't compromise results."
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall ensure that modifications to report templates do not compromise the correctness or intended results of the report.

### REQ-159: Report templates: administrators limit alterable filters and display fields

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicitly requested as an admin control for template editability.
- **Sources:** email_report_features.eml
- **Evidence:** email_report_features.eml: "Admins should be able to limit which filters and display fields can be altered.", email_report_features.eml: "Admins create templates available to staff. ... Limit alterable filters/fields."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall allow administrators to limit which filters and display fields in a report template can be altered by staff when running or modifying template variants.

### REQ-160: Report templates: examples of disallowed modifications (deleted items)

- **Category:** constraint
- **Priority:** P2 (estimated)
- **Priority rationale:** Example-specific exception/constraint tied to the template limitation statement.
- **Sources:** email_report_features.eml
- **Evidence:** email_report_features.eml: "Example: Front-line staff can set a call number range for a weeding report or add/remove display fields from a pick list, but can't alter the template to display deleted items."
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall prevent template variants from being modified to display deleted items when the template is configured to disallow that change (example: front-line staff may change some fields but may not alter a template to display deleted items).

### REQ-161: Report templates: clone capability to create new report variants

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicitly requested as a distinct capability separate from modifying templates.
- **Sources:** email_report_features.eml
- **Evidence:** email_report_features.eml: "We also need the ability to \"clone\" reports - take an existing template and create a new one based on it. This is different from modifying the template - it's creating a new variant.", email_report_features.eml: "REPORT TEMPLATES: ... Clone capability."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall support cloning a report template by creating a new report variant based on an existing template.

### REQ-162: Report permissions: fine-grained permission levels for create and clone

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicitly requested as a core permissions requirement.
- **Sources:** email_report_features.eml
- **Evidence:** email_report_features.eml: "PERMISSIONS: We need distinct, fine-grained permission levels limiting who can create and clone reports.", email_report_features.eml: "REPORTS PERMISSIONS: Fine-grained permission levels."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall provide distinct, fine-grained permission levels that limit which users can create and clone reports.

### REQ-163: Report permissions: shared folders to control run access

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Specified under permissions as a folder-based mechanism.
- **Sources:** email_report_features.eml
- **Evidence:** email_report_features.eml: "Admins can create shared folders to allow or disallow staff from running specific reports, and/or to run ad hoc reports on specific sets of data."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall allow administrators to create shared folders to control which staff can run specific reports and/or run ad hoc reports on specific datasets.

### REQ-164: Role-based access: permissions determined by security group/role and admin management

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicit login-to-permission mapping plus admin manageability stated in the login thread.
- **Sources:** email_staff_login.eml
- **Evidence:** email_staff_login.eml: "when a staff member logs in (by any method), their permissions should be determined by their assigned security group/role. Administrators should be able to create and manage these groups.", email_staff_login.eml: "System supports (but does not require) streamlined staff login methods" (summary) and "User rights and privileges controlled through security groups/roles."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall determine staff permissions based on the staff member's assigned security group or role at login, and shall allow administrators to create and manage those roles/groups.

### REQ-165: Administration by role: role changes update permissions automatically

- **Category:** business rule
- **Priority:** P2 (estimated)
- **Priority rationale:** Stated as an administration requirement in the login thread and the report templates/permissions thread.
- **Sources:** email_staff_login.eml, email_report_features.eml
- **Evidence:** email_staff_login.eml: "The system should make it easy to administer these roles - changing someone's permissions should be a simple matter of changing their role assignment, not modifying individual permissions.", email_report_features.eml: "The permissions need to be easy to administer. If I change someone from \"Staff\" to \"Manager,\" their report permissions should update automatically based on the role."
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall make it easy to administer roles and permissions such that changing a staff member's role assignment updates their report and system permissions automatically rather than requiring individual permission edits.

### REQ-166: Board reports: predefined statistics and cross-tabulations

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Clearly enumerated capability set under board reports.
- **Sources:** email_report_features.eml
- **Evidence:** email_report_features.eml: "BOARD REPORTS: Pre-defined reports for library boards with basic statistics (Georgia Annual Report requirements). Activity reports showing traffic and volume of use - checkouts, check-ins, holds placed, holds filled. Cross-tabulated per terminal, per branch, per system, per hour, per age range, per patron type, per patron location.", email_report_features.eml: "BOARD REPORTS: Pre-defined reports for boards. Cross-tabulated per terminal/branch/system/hour/age/patron type/location."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall provide predefined board reports that include basic statistics and activity metrics (checkouts, check-ins, holds placed/filled) with cross-tabulation by terminal, branch, system, hour, age range, patron type, and patron location.

### REQ-167: Transaction archive: privacy-protected archiving and retention

- **Category:** security
- **Priority:** P1 (source-supported)
- **Priority rationale:** Compliance/privacy requirement is explicitly stated; retention duration is conditional on legal requirements.
- **Sources:** email_report_features.eml
- **Evidence:** email_report_features.eml: "TRANSACTION ARCHIVE: Transactions archived protecting patron privacy per State Law, while providing useful demographic statistics.", email_report_features.eml: "State law requires us to retain transaction data for X years, but patron privacy means we can't keep personally identifiable information."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** Q1

System shall archive transaction data in a manner that protects patron privacy in accordance with applicable state law while enabling useful demographic/statistical reporting, and shall retain transaction data for the retention period required by law.

### REQ-168: Query selections: show criteria with results

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicitly requested and repeated in consolidated summary.
- **Sources:** email_report_features.eml
- **Evidence:** email_report_features.eml: "QUERY SELECTIONS: System provides query selections along with results.", email_report_features.eml: "QUERY SELECTIONS: Show criteria with results."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall display the query selection criteria together with the query results.

### REQ-169: STAFF_login_methods_support_optional_card_swipe_and_username_password_fallback

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Both the optional streamlined login and the requirement for a traditional username/password fallback are explicitly requested to ensure broad staff access and to avoid requiring ID cards.
- **Sources:** email_staff_login.eml
- **Evidence:** email_staff_login.eml: "However, we also need to support the traditional username/password method - ... The system should support BOTH methods ... The streamlined method should be optional but available.", email_staff_login.eml: "the system should not REQUIRE the streamlined login... The requirement should be: \"The system supports (but does not require) streamlined staff login methods.\"", email_staff_login.eml: "we also need to support the traditional username/password method - not all staff may have ID cards, and we need a fallback.", email_staff_login.eml: "The system should support BOTH methods - streamlined login ... AND traditional login (individual login and password)."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall support streamlined staff login methods (e.g., card swipe) as optional and shall support traditional username/password login as a fallback for staff without ID cards.

### REQ-170: STAFF_login_tracks_identity_for_audit

- **Category:** security
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicitly required to preserve auditability even when streamlined login methods (e.g., card swipe) are used.
- **Sources:** email_staff_login.eml
- **Evidence:** email_staff_login.eml: "even with card swipe, we need individual authentication. The system must track WHICH staff member is logged in for audit purposes."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall track the identity of the specific staff member who is logged in for audit purposes when a staff member logs in by any supported method.

### REQ-171: STREAMLINED_login_must_not_bypass_individual_authentication

- **Category:** security
- **Priority:** P2 (source-supported)
- **Priority rationale:** Security constraint explicitly requested to ensure streamlined methods do not remove required authentication controls.
- **Sources:** email_staff_login.eml
- **Evidence:** email_staff_login.eml: "even with card swipe, we need individual authentication... The card is just a convenient way to identify the person, but it shouldn't bypass individual authentication entirely."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall not bypass individual authentication entirely when using streamlined login methods (e.g., card swipe); the card is only a convenient way to identify the person and individual authentication controls must remain in place as required.

### REQ-172: ACCESS_CONTROL_roles_and_groups_for_individuals_workgroups_arbitrary_groups

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Access-control scope (individuals, workgroups, arbitrary groups) is explicitly requested and is necessary to support varied staffing and responsibilities.
- **Sources:** email_staff_login.eml
- **Evidence:** email_staff_login.eml: "We also need ... Access control for individuals, workgroups, and arbitrary staff groups.", email_staff_login.eml: "3. Access control for individuals, workgroups, and arbitrary staff groups."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall provide access control for individuals, workgroups, and arbitrary staff groups via security groups and/or roles.

### REQ-173: REPORTS_permissions_roles_for_staff_types

- **Category:** functional
- **Priority:** P3 (estimated)
- **Priority rationale:** Enumerated staff-type examples indicate differing report capabilities should be supported; priority is lower because examples describe existing organizational practice rather than a blocking gap.
- **Sources:** email_staff_login.eml
- **Evidence:** email_staff_login.eml: "At Piedmont, we have several different types of staff: - Front desk staff (can run basic reports, limited filters) - Department heads (can create and modify templates) - System administrators (full access to all reports and permissions)", email_staff_login.eml: "Each of these should be a role that can be assigned to staff members."
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall support defining roles corresponding to staff types with different capabilities for reporting (e.g., front desk staff can run basic reports with limited filters; department heads can create and modify templates; system administrators have full access).

### REQ-174: REPORTS_queuing_visibility

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Detailed queue visibility is explicitly requested to reduce support calls and staff frustration by making queue status transparent.
- **Sources:** email_report_features.eml
- **Evidence:** email_report_features.eml: "REPORTS QUEUING: Ability to see where your report is in the queue.", email_report_features.eml: "staff get frustrated ... They need to see: - That their report is in the queue - How many reports are ahead of theirs - When their report was submitted - Status (waiting, running, completed, failed)"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall allow staff to view report queue information, including the position in the queue, status, and related timing information (waiting, running, completed, failed, and when the report was submitted).

### REQ-175: REPORT_QUEUE_priority_jumps_ahead

- **Category:** business rule
- **Priority:** P2 (estimated)
- **Priority rationale:** Explicitly requested ability to prioritize certain reports and allow them to jump ahead of ad-hoc queries.
- **Sources:** email_report_features.eml
- **Evidence:** email_report_features.eml: "Also, the ability to prioritize certain reports is crucial. A director's board report should be able to jump ahead of a staff member's ad-hoc query.", email_report_features.eml: "7. REPORTS QUEUING: See position in queue, status, priority.", email_report_features.eml: "8. PRIORITY: Important reports can jump queue."
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall allow prioritized reports (for example, a director's board report) to jump ahead of non-priority reports in the report queue.

### REQ-176: REPORTING_module_web_based_report_writer

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Described as part of the reporting module overview; foundational capability for custom reporting, though not identified as a gap in the source.
- **Sources:** evergreen_reference_2009.txt
- **Evidence:** "Evergreen includes a report writer that allows staff to create custom reports using a web-based interface."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall provide a web-based report writer interface that allows staff to create custom reports.

### REQ-177: Report_writer_drag_and_drop_field_selection

- **Category:** functional
- **Priority:** P3 (source-supported)
- **Priority rationale:** Specific usability feature described in the reference; lower priority because it is a specific enhancement rather than a blocking capability.
- **Sources:** evergreen_reference_2009.txt
- **Evidence:** "Drag-and-drop field selection"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall support drag-and-drop field selection in the report writer interface.

### REQ-178: Report_writer_basic_filtering_and_sorting

- **Category:** functional
- **Priority:** P3 (source-supported)
- **Priority rationale:** Described as a baseline capability; useful but not presented as urgent in the sources.
- **Sources:** evergreen_reference_2009.txt
- **Evidence:** "Basic filtering and sorting"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall support basic filtering and sorting when constructing custom reports.

### REQ-179: Report_writer_multiple_output_formats

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Multiple output formats are important for downstream use and are described as an existing capability impacting usability.
- **Sources:** evergreen_reference_2009.txt
- **Evidence:** "Multiple output formats (CSV, HTML, sometimes Excel)"
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall allow custom reports to be output in multiple formats including CSV and HTML, and optionally Excel.

### REQ-180: Report_writer_save_and_reuse_report_definitions

- **Category:** functional
- **Priority:** P3 (source-supported)
- **Priority rationale:** Described as a useful capability; not called out as an urgent requirement in the sources.
- **Sources:** evergreen_reference_2009.txt
- **Evidence:** "Ability to save and reuse report definitions"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall allow users to save and reuse report definitions created in the report writer interface.

### REQ-181: Report_scheduling_supports_daily_weekly_monthly_intervals

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Scheduling at these intervals is explicitly described and supports routine automated reporting needs.
- **Sources:** evergreen_reference_2009.txt
- **Evidence:** "Some reports can be scheduled to run at regular intervals (daily, weekly, monthly)."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall allow reports to be scheduled to run at regular intervals including daily, weekly, and monthly.

### REQ-182: Report_scheduling_does_not_support_hourly_scheduling

- **Category:** constraint
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicitly stated as a limitation in the referenced Evergreen version; treated as a constraint to set expectations.
- **Sources:** evergreen_reference_2009.txt
- **Evidence:** "- No hourly scheduling"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall not provide hourly scheduling for reports.

### REQ-183: Report scheduling prevents selecting multiple reports

- **Category:** constraint
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicit scheduling limitation stated in the document.
- **Sources:** evergreen_reference_2009.txt
- **Evidence:** "- No ability to check multiple reports to run at the same time"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall not allow users to check/select multiple reports to run at the same time.

### REQ-184: Scheduled reports cannot be delivered by email

- **Category:** constraint
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicitly stated missing capability affecting delivery method; also impacts operational workflows.
- **Sources:** evergreen_reference_2009.txt
- **Evidence:** "- No email delivery (reports can only be downloaded from the web interface)"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall not deliver scheduled reports via email; scheduled reports can only be downloaded from the web interface.

### REQ-185: Staff may run any accessible report

- **Category:** business rule
- **Priority:** P2 (source-supported)
- **Priority rationale:** Directly describes the existing permission behavior.
- **Sources:** evergreen_reference_2009.txt
- **Evidence:** "Staff can run any report they can access"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall allow staff to run any report they can access.

### REQ-186: No fine-grained permission to separate report creation and execution

- **Category:** constraint
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicitly stated permission gap impacting authorization; treated as missing/limited capability.
- **Sources:** evergreen_reference_2009.txt
- **Evidence:** "No fine-grained control over who can create vs. run reports"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall not provide fine-grained permissions that distinguish report creation from report execution.

### REQ-187: No shared-folder concept for report permissions

- **Category:** constraint
- **Priority:** P3 (source-supported)
- **Priority rationale:** Explicit gap; lower impact relative to execution permissions.
- **Sources:** evergreen_reference_2009.txt
- **Evidence:** "No shared folders concept"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall not support a shared folders concept for organizing report permissions.

### REQ-188: No restriction on which filters staff may use in reports

- **Category:** constraint
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicitly stated as a missing permission control; affects data exposure.
- **Sources:** evergreen_reference_2009.txt
- **Evidence:** "No ability to limit which filters staff can use"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall not provide the ability to limit which filters staff can use when running reports.

### REQ-189: Support reporting on bibliographic_record

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Defines what data is available for reporting; foundational but not a stated gap.
- **Sources:** evergreen_reference_2009.txt
- **Evidence:** "The following record types are available for reporting: - bibliographic_record"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall support reporting on the bibliographic_record record type.

### REQ-190: Support reporting on item

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Foundational capability described.
- **Sources:** evergreen_reference_2009.txt
- **Evidence:** "The following record types are available for reporting: - item"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall support reporting on the item record type.

### REQ-191: Support reporting on patron

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Foundational capability described.
- **Sources:** evergreen_reference_2009.txt
- **Evidence:** "The following record types are available for reporting: - patron"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall support reporting on the patron record type.

### REQ-192: Support reporting on action_circulation

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Foundational capability described.
- **Sources:** evergreen_reference_2009.txt
- **Evidence:** "The following record types are available for reporting: - action_circulation"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall support reporting on the action_circulation record type.

### REQ-193: Support reporting on action_hold

- **Category:** functional
- **Priority:** P3 (source-supported)
- **Priority rationale:** Foundational but less central than core record types.
- **Sources:** evergreen_reference_2009.txt
- **Evidence:** "The following record types are available for reporting: - action_hold"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall support reporting on the action_hold record type.

### REQ-194: Support reporting on money

- **Category:** functional
- **Priority:** P3 (source-supported)
- **Priority rationale:** Foundational capability for financial reporting, described in the data structures section.
- **Sources:** evergreen_reference_2009.txt
- **Evidence:** "The following record types are available for reporting: - money"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall support reporting on the money record type.

### REQ-195: Support reporting on actor

- **Category:** functional
- **Priority:** P3 (source-supported)
- **Priority rationale:** Foundational capability for staff/account-related reporting.
- **Sources:** evergreen_reference_2009.txt
- **Evidence:** "The following record types are available for reporting: - actor"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall support reporting on the actor record type.

### REQ-196: Provide predefined (canned) reports for common circulation and item metrics

- **Category:** functional
- **Priority:** P3 (source-supported)
- **Priority rationale:** Describes existing canned reports; not an explicit requirement for the enhanced system.
- **Sources:** evergreen_reference_2009.txt
- **Evidence:** "CIRCULATION:", "- Checkout Count", "- Renewals Count", "ITEMS:", "- Items Overdue by X Days"
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall provide pre-defined canned reports including circulation checkout count, renewals count, and items overdue by X days.

### REQ-197: Report writer lacks advanced Boolean operators

- **Category:** constraint
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicit limitation; impacts ability to construct complex queries.
- **Sources:** evergreen_reference_2009.txt
- **Evidence:** "No Boolean operators (AND/OR) beyond simple filters"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall not support Boolean operators (AND/OR) beyond simple filters in the report writer interface.

### REQ-198: Report writer lacks regular expression support

- **Category:** constraint
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicit limitation on query capabilities.
- **Sources:** evergreen_reference_2009.txt
- **Evidence:** "No regular expression support"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall not provide regular expression support for report queries in the report writer interface.

### REQ-199: Report writer field selection is limited

- **Category:** constraint
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicit limitation affecting query construction.
- **Sources:** evergreen_reference_2009.txt
- **Evidence:** "Limited field selection (not all database fields are available)"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall limit available field selection in custom report queries such that not all database fields are available for selection.

### REQ-200: Report queue visibility is not available for staff

- **Category:** constraint
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicit missing feature and directly mentioned as a gap.
- **Sources:** evergreen_reference_2009.txt
- **Evidence:** "No report queue visibility (staff can't see where their report is in queue)", "- No report queue visibility"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall not provide report queue visibility to staff, such that staff cannot see where their report is in the queue.

### REQ-201: System shall not support report cancellation for running reports

- **Category:** constraint
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicitly stated as missing feature.
- **Sources:** evergreen_reference_2009.txt
- **Evidence:** "No ability to cancel a running report", "- No ability to cancel a running report"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall not allow users to cancel a running report.

### REQ-202: System shall not provide pivot table output

- **Category:** constraint
- **Priority:** P3 (source-supported)
- **Priority rationale:** Explicit missing capability; likely usability/analysis related.
- **Sources:** evergreen_reference_2009.txt
- **Evidence:** "No pivot table output", "- No pivot table output"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall not support pivot table output for reports.

### REQ-203: System shall not provide real-time reporting on demand

- **Category:** constraint
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicitly stated missing architectural/functional capability.
- **Sources:** evergreen_reference_2009.txt
- **Evidence:** "No real-time reporting (all reports are run on current data)"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall not provide real-time reporting; reports are run on current data rather than in a real-time mode.

### REQ-204: System shall not provide a historical reporting warehouse

- **Category:** constraint
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicit missing architectural element and repeated in gaps.
- **Sources:** evergreen_reference_2009.txt
- **Evidence:** "No historical reporting warehouse", "Historical reporting warehouse - does not exist"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall not provide a historical reporting warehouse.

### REQ-205: System shall not provide additional scheduling granularity (Run ASAP/Hourly/Daily/Weekly/Monthly/Yearly)

- **Category:** constraint
- **Priority:** P2 (estimated)
- **Priority rationale:** Although some scheduling exists, the document explicitly lists lack of these options; represented as a constraint.
- **Sources:** evergreen_reference_2009.txt
- **Evidence:** "No ability to select Run ASAP, Hourly, Daily, Weekly, Monthly, Yearly"
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall not provide scheduling options including Run ASAP, Hourly, Daily, Weekly, Monthly, and Yearly.

### REQ-206: System shall not deliver reports via email nor via address book delivery

- **Category:** constraint
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicit missing features in delivery and address book management.
- **Sources:** evergreen_reference_2009.txt
- **Evidence:** "No email delivery of reports", "No address book for report delivery"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall not provide email delivery of reports, and shall not provide an address book for report delivery.

### REQ-207: System shall not support uploading text files for filtering (barcodes, TCNs)

- **Category:** constraint
- **Priority:** P3 (source-supported)
- **Priority rationale:** Explicit missing input mechanism; lower than core reporting/permissions gaps.
- **Sources:** evergreen_reference_2009.txt
- **Evidence:** "No ability to upload text files for filtering (barcodes, TCNs)"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall not allow users to upload text files for filtering (e.g., barcodes, TCNs).

### REQ-208: System shall not display selection criteria in report results

- **Category:** constraint
- **Priority:** P3 (source-supported)
- **Priority rationale:** Explicit missing UI feedback feature.
- **Sources:** evergreen_reference_2009.txt
- **Evidence:** "No selection criteria display in report results"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall not display report selection criteria in report results.

### REQ-209: System shall not provide ability to edit canned report display options

- **Category:** constraint
- **Priority:** P3 (source-supported)
- **Priority rationale:** Explicit missing fine-tuning capability for canned reports.
- **Sources:** evergreen_reference_2009.txt
- **Evidence:** "No ability to edit canned report display options"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall not allow users to edit canned report display options.

### REQ-210: System shall not provide quick access interface with pop-up descriptions

- **Category:** constraint
- **Priority:** P4 (source-supported)
- **Priority rationale:** UI convenience feature explicitly missing; likely least critical among listed gaps.
- **Sources:** evergreen_reference_2009.txt
- **Evidence:** "No quick access interface with pop-up descriptions"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall not provide a quick access report interface with pop-up descriptions.

### REQ-211: System shall not provide hover tooltips for report titles

- **Category:** constraint
- **Priority:** P4 (source-supported)
- **Priority rationale:** Explicit UI/accessibility-like feature missing; lowest listed priority in document context.
- **Sources:** evergreen_reference_2009.txt
- **Evidence:** "No hover tooltips for report titles"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall not provide hover tooltips for report titles.

### REQ-212: System shall not use a separate reporting database/replica

- **Category:** constraint
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicit architectural limitation affects performance and isolation.
- **Sources:** evergreen_reference_2009.txt
- **Evidence:** "No separate reporting database/replica (reports run on production database)"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall not run reporting against a separate reporting database/replica; reports run on the production database.

### REQ-213: No background processing for long-running reports

- **Category:** constraint
- **Priority:** P2 (source-supported)
- **Priority rationale:** Taken from the Evergreen reference that documents an architectural limitation: background processing for long-running reports is not provided.
- **Sources:** evergreen_reference_2009.txt
- **Evidence:** "No background processing for long-running reports"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** Q1

System shall not provide background (queued) processing for long-running reports.

### REQ-214: Background/queued report processing to avoid peak-hour disruption

- **Category:** non-functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Sysadmin explicitly described this as a major operational requirement to avoid slowing the circulation client during open hours; treated as high priority.
- **Sources:** interview_sysadmin_2009-05-10.txt
- **Evidence:** "when someone runs a complex report, it can tie up the database and slow down the circulation client", "We need to make sure reports can be queued and processed in the background", "without disrupting other system functions."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** Q1

System shall process complex report searches in the background (queued) or via read-only replicas so that reporting during open hours does not disrupt other system functions.

### REQ-215: No open-template reporting or report-template management (only canned reports)

- **Category:** constraint
- **Priority:** P2 (estimated)
- **Priority rationale:** All referenced candidates describe the absence of template-based reporting and template management. Priority P2 reflects the documented limitation in the Evergreen reference.
- **Sources:** evergreen_reference_2009.txt
- **Evidence:** "No report template management system", "Open Template Reporting - does not exist", "Three interfaces (canned, on-demand, open template) - only basic canned exists"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall not provide an open-template reporting interface or a report template management system; only basic canned reports are provided.

### REQ-216: No fine-grained permissions for reports

- **Category:** constraint
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicitly stated in the Evergreen reference as a missing capability; recorded as high priority because it affects security/authorization for reporting.
- **Sources:** evergreen_reference_2009.txt
- **Evidence:** "No fine-grained permissions for reports"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall not provide fine-grained permissions for reports.

### REQ-217: No separation of development/training environment from production

- **Category:** constraint
- **Priority:** P3 (source-supported)
- **Priority rationale:** Documented operational gap; important for processes (training, testing) but lower immediate runtime impact than other items.
- **Sources:** evergreen_reference_2009.txt
- **Evidence:** "No development/training environment separation"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall not provide separation of development/training environments from production.

### REQ-218: No support for configuration migration between environments

- **Category:** constraint
- **Priority:** P3 (source-supported)
- **Priority rationale:** Documented DevOps/operational limitation; priority reflects operational importance but lower immediacy.
- **Sources:** evergreen_reference_2009.txt
- **Evidence:** "No configuration migration between environments"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall not support configuration migration between environments.

### REQ-219: No accessibility support for the report interface (documented)

- **Category:** constraint
- **Priority:** P2 (source-supported)
- **Priority rationale:** Evergreen reference documents lack of accessibility support; priority P2 reflects that this is a notable limitation in the product documentation.
- **Sources:** evergreen_reference_2009.txt
- **Evidence:** "No accessibility support for report interface"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** Q2

System shall not provide accessibility support for the report interface.

### REQ-220: No online help integrated with reports

- **Category:** constraint
- **Priority:** P4 (source-supported)
- **Priority rationale:** Documented missing support feature in Evergreen; treated as lower priority.
- **Sources:** evergreen_reference_2009.txt
- **Evidence:** "No online help system integrated with reports"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall not provide an online help system integrated with reports.

### REQ-221: Cross-platform server support: Linux and Solaris

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Sysadmin explicitly requires reporting to work on both platforms (primary Linux site and secondary Solaris disaster-recovery site); treated as high priority.
- **Sources:** interview_sysadmin_2009-05-10.txt
- **Evidence:** "any reporting system needs to work on both Linux and Solaris."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall support deployment and operation on both Linux (e.g., RHEL 5) and Solaris (e.g., Solaris 10) server environments.

### REQ-222: Browser support: Microsoft Internet Explorer 6.0+ and Firefox 2.0+

- **Category:** constraint
- **Priority:** P2 (source-supported)
- **Priority rationale:** Stated by the systems administrator as required due to existing client environments.
- **Sources:** interview_sysadmin_2009-05-10.txt
- **Evidence:** "So we need to support IE 6.0+", "Firefox 2.0+"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall support Microsoft Internet Explorer version 6.0 or newer and Firefox version 2.0 or newer for the reporting interface.

### REQ-223: Section 508 and assistive-technology support for reports

- **Category:** security
- **Priority:** P1 (source-supported)
- **Priority rationale:** Described by the systems administrator as non-negotiable legal compliance and required assistive-technology compatibility; treated as highest priority.
- **Sources:** interview_sysadmin_2009-05-10.txt
- **Evidence:** "This is non-negotiable. As a public institution, we MUST comply with Section 508 accessibility requirements.", "The system needs to work with: Screen readers like JAWS and NVDA", "Screen magnification software like ZoomText", "Other assistive technology programs"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** Q2

System shall comply with Section 508 accessibility requirements and shall support use with screen readers (e.g., JAWS, NVDA), screen magnification software (e.g., ZoomText), and other assistive technology programs for the reporting interface.

### REQ-224: Accessible HTML output semantics

- **Category:** non-functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Directly specified for HTML output required for accessibility.
- **Sources:** interview_sysadmin_2009-05-10.txt
- **Evidence:** "The HTML output needs to be properly structured with alt tags, ARIA labels, and proper semantic HTML."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall generate HTML output with properly structured content including alt tags, ARIA labels, and proper semantic HTML.

### REQ-225: Standards-compliant HTML output

- **Category:** non-functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicit requirement stated as part of accessibility implementation.
- **Sources:** interview_sysadmin_2009-05-10.txt
- **Evidence:** "And the system needs to produce standards-compliant HTML."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall produce standards-compliant HTML.

### REQ-226: Relational database compatibility (PostgreSQL)

- **Category:** constraint
- **Priority:** P1 (source-supported)
- **Priority rationale:** The administrator prefers using the main relational database to avoid synchronization issues; explicit system constraint.
- **Sources:** interview_sysadmin_2009-05-10.txt
- **Evidence:** "We're using PostgreSQL now", "The reporting system needs to work with the relational structure, not fight against it.", "I'd prefer to keep everything in the main relational database.", "Some systems try to use denormalized reporting schemas, but that creates sync issues."
- **Manual provenance review required:** No
- **Confidence:** medium-high
- **Related questions/dependencies:** —

System shall operate with the main PostgreSQL-compatible relational database architecture and shall not require denormalized reporting schemas.

### REQ-227: Role-based access control via security groups/roles

- **Category:** security
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicitly described as needed for access control across individual, workgroup, and arbitrary staff groups.
- **Sources:** interview_sysadmin_2009-05-10.txt
- **Evidence:** "The permission system needs to be controlled through security groups and/or \"roles.\""
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall control permissions through security groups and/or roles.

### REQ-228: Permission administration via role assignment

- **Category:** security
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicitly stated as the needed administration ease.
- **Sources:** interview_sysadmin_2009-05-10.txt
- **Evidence:** "Changing someone's permissions should be a simple matter of changing their role assignment."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall allow changing a user's permissions by updating their role assignment.

### REQ-229: Separate development/testing environment

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicit training/dev environment requirement.
- **Sources:** interview_sysadmin_2009-05-10.txt
- **Evidence:** "Developers need a place to test new reports without affecting production."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall provide separate development and testing environments where developers can test new reports without affecting production.

### REQ-230: Separate training environment for safe report practice

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicitly stated need for training environment.
- **Sources:** interview_sysadmin_2009-05-10.txt
- **Evidence:** "And new staff members need a training environment where they can practice running reports without worrying about making mistakes."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall provide a training environment where new staff can practice running reports without worrying about making mistakes or affecting production.

### REQ-231: Export/import for migratable configurations

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicitly stated for migration of developed configurations.
- **Sources:** interview_sysadmin_2009-05-10.txt
- **Evidence:** "configurations developed in training/dev need to be migratable to production", "We need export/import functionality for report templates, permission settings, and other configuration."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall provide export/import functionality to migrate configurations developed in training/development to production, including report templates and permission settings.

### REQ-232: Reporting must not impact OPAC performance

- **Category:** non-functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Stated as a key non-interference requirement between reporting and OPAC performance.
- **Sources:** interview_sysadmin_2009-05-10.txt
- **Evidence:** "The management reporting system must not constrain the OPAC in any way.", "If the reporting system is doing a big query, it should NOT slow down the OPAC."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall not constrain the OPAC module; reporting operations shall not slow down fast, responsive patron access to the catalog.

### REQ-233: Online help system (hierarchical, searchable, navigable)

- **Category:** usability
- **Priority:** P3 (source-supported)
- **Priority rationale:** Explicitly stated; importance is lower than core accessibility/performance/security but still a clear requirement. Also motivated by the need for staff to run reports without calling IT.
- **Sources:** interview_sysadmin_2009-05-10.txt
- **Evidence:** "the help system needs to be online, hierarchical, and cross-linked.", "The HTML help needs to be searchable and easy to navigate.", "Staff shouldn't have to call IT every time they want to know how to run a report."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall provide an online help system that is hierarchical, cross-linked, searchable, and easy to navigate, enabling staff to find how to run reports and related guidance without calling IT.

### REQ-234: Track uncataloged material as inventory

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Uncataloged material tracking is described as a major workflow need.
- **Sources:** interview_cataloging_2009-05-08.txt
- **Evidence:** "We need to be able to track these as inventory even though they're not fully cataloged."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall allow tracking inventory for materials that arrive without individual catalog records (even when items are not fully cataloged).

### REQ-235: Quick processing and minimal branch labor for uncataloged inventory

- **Category:** non-functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicitly stated needs tied to workflow constraints for uncataloged items.
- **Sources:** interview_cataloging_2009-05-08.txt
- **Evidence:** "We need to process these fast", "minimal branch labor (we can't spend a lot of time per item)"
- **Manual provenance review required:** No
- **Confidence:** medium-high
- **Related questions/dependencies:** —

System shall support quick processing of uncataloged material inventory with minimal per-item effort for branch staff.

### REQ-236: Include uncataloged materials in usage/statistics

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicitly required for uncataloged materials: track usage via transactions and include in circulation statistics/reports.
- **Sources:** interview_cataloging_2009-05-08.txt
- **Evidence:** "ability to identify how the material is being used", "We also need to count transactions and include them in circulation statistics and reports."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall enable identification of how uncataloged materials are being used, including counting transactions and including them in circulation statistics and reports.

### REQ-237: Item transfer utility for batch transfers between branches/outreach/mobile

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Described as crucial and repeatedly referenced as required capability for transfers.
- **Sources:** interview_cataloging_2009-05-08.txt
- **Evidence:** "the item transfer utility is crucial", "move batches of items between branches", "sending books to a mobile library unit or to an outreach program collection"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall provide an item transfer utility to move batches of items between branches, including scenarios such as sending items to a mobile library unit or outreach program collection.

### REQ-238: Transfer query candidate materials by criteria (example: section and non-circulation window)

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicitly stated first capability is query by criteria; example given.
- **Sources:** interview_cataloging_2009-05-08.txt
- **Evidence:** "we need to query for candidate materials", "Maybe we want all items in the children's section that haven't circulated in 6 months."
- **Manual provenance review required:** No
- **Confidence:** medium-high
- **Related questions/dependencies:** —

System shall allow querying for candidate materials to transfer based on user-defined criteria (e.g., all items in a children’s section that haven’t circulated in a specified number of months).

### REQ-239: Save transfer queries for repeated use (monthly)

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicitly stated as a required capability (save queries for monthly reuse).
- **Sources:** interview_cataloging_2009-05-08.txt
- **Evidence:** "we need to save these queries for repeated use - we do this monthly."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall allow saving transfer queries for repeated use, including a workflow where queries are saved and used monthly.

### REQ-240: Manual selection of titles from transfer query results

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicitly stated capability #3 in transfer utility.
- **Sources:** interview_cataloging_2009-05-08.txt
- **Evidence:** "Third, we need to manually select titles from query results"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall allow manual selection of titles/items from transfer query results to support more targeted transfers.

### REQ-241: Change records of selected items to new location

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Directly stated as the transfer utility’s capability to move selected items.
- **Sources:** interview_cataloging_2009-05-08.txt
- **Evidence:** "Fourth, we need to change records of selected items to move them to a new location."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall change the location/location-related records of selected items so they are moved to a new location.

### REQ-242: Revert transferred items to original location after a set period

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicitly stated as required mechanism for reversal after set period.
- **Sources:** interview_cataloging_2009-05-08.txt
- **Evidence:** "mechanisms for reverting items back to their original location after a set period of time", "like when a mobile library returns to base."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall provide mechanisms for reverting transferred items back to their original location after a configured set period of time (e.g., when a mobile library returns to base).

### REQ-243: Report missing and damaged items per branch

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicit monthly shelf reading outcome requires such a report.
- **Sources:** interview_cataloging_2009-05-08.txt
- **Evidence:** "I need a report that shows all missing and damaged items per branch."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall generate a report showing missing and damaged items per branch.

### REQ-244: In-transit items report with configurable day threshold

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicit requirement with configurability for X days.
- **Sources:** interview_cataloging_2009-05-08.txt
- **Evidence:** "more than X days (configurable)", "The report should show items that have been in-transit for more than X days"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall provide an in-transit items report listing items that have been in-transit for more than X days, where X is configurable.

### REQ-245: In-transit items report by branch and by system

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicitly required breakdown for the in-transit report.
- **Sources:** interview_cataloging_2009-05-08.txt
- **Evidence:** "per branch and per system."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall display the in-transit report results per branch and per system.

### REQ-246: Merge transit-to and transit-from into one in-transit report

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicitly requested merge behavior.
- **Sources:** interview_cataloging_2009-05-08.txt
- **Evidence:** "It should merge the transit-to and transit-from into one report for ease of use."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall merge transit-to and transit-from information into a single in-transit report for ease of use.

### REQ-247: Weeding report to identify items for purging based on customizable criteria

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Weeding reports are stated as most-used and requires customizable criteria.
- **Sources:** interview_cataloging_2009-05-08.txt
- **Evidence:** "Weeding reports are my most-used report type.", "identify items for purging based on customizable criteria."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall provide weeding reports that identify items for purging based on customizable criteria.

### REQ-248: Weeding criteria: missing status older than X months

- **Category:** business rule
- **Priority:** P2 (source-supported)
- **Priority rationale:** Example criteria explicitly listed for purging.
- **Sources:** interview_cataloging_2009-05-08.txt
- **Evidence:** "Item has been in status \"missing\" for more than X months"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall support weeding/purging criteria where an item has status "missing" for more than X months.

### REQ-249: Weeding criteria: status discard/weed

- **Category:** business rule
- **Priority:** P2 (source-supported)
- **Priority rationale:** Example criteria explicitly listed for purging.
- **Sources:** interview_cataloging_2009-05-08.txt
- **Evidence:** "Item has status \"discard/weed\""
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall support weeding/purging criteria where an item has status "discard/weed".

### REQ-250: Batch status conversion assistance report for changing item statuses

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicitly required for batch conversion with example scale.
- **Sources:** interview_cataloging_2009-05-08.txt
- **Evidence:** "We also need a report to assist in converting items from one status to another.", "Sometimes I need to change 100 items from \"missing\" to \"discard/weed\" in batch."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall provide a report or mechanism to assist in converting items from one status to another, including batch changes (e.g., changing 100 items from "missing" to "discard/weed").

### REQ-251: Last copy report for identifying a system's last copies

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Described as critical to prevent almost deleting a last copy; explicit need.
- **Sources:** interview_cataloging_2009-05-08.txt
- **Evidence:** "And the last copy report is CRITICAL.", "This singles out a library system's last copies, to assist catalogers who need to edit WorldCat entries."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall provide a last copy report that singles out a library system's last copies to assist catalogers.

### REQ-252: Delete volume and orphan records

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicit pain point that orphan cleanup takes forever and requires an effective deletion method.
- **Sources:** interview_cataloging_2009-05-08.txt
- **Evidence:** "There also needs to be a quick, effective method for deleting volume entries along with copy entries, as well as records with no items attached.", "Right now, cleaning up these orphaned records takes forever."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall provide a quick, effective method for deleting volume entries together with their copy entries, and for deleting bibliographic records that have no item records attached (orphaned records).

### REQ-253: Track and audit record deletions (counts, reasons, per location/system)

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicitly stated for auditing directors and troubleshooting; directors want both count and reason and counts by location/system.
- **Sources:** interview_cataloging_2009-05-08.txt
- **Evidence:** "we need to count and track record deletions per location and per system", "This is important for auditing - our directors want to know how many records we've deleted and why.", "directors want to know how many records we've deleted and why."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall count, track and audit record deletions for auditing purposes; audit records shall include how many records were deleted and the reason(s), and counts shall be attributable per location and per system.

### REQ-254: Shelf space report comparing circulation, collection, and shelf space by genre/format

- **Category:** functional
- **Priority:** P3 (source-supported)
- **Priority rationale:** Specific report comparison needs stated; less critical than transfer/weeding/accessibility.
- **Sources:** interview_cataloging_2009-05-08.txt
- **Evidence:** "For each genre and format, I need to compare: Percentage of total circulations", "Percentage of the collection", "Percentage of total shelf space"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall generate a shelf space report that, for each genre and format, compares percentage of total circulations, percentage of the collection, and percentage of total shelf space.

### REQ-255: Material volume report with category breakdowns

- **Category:** functional
- **Priority:** P3 (source-supported)
- **Priority rationale:** Explicitly listed report requirement with example breakdown categories.
- **Sources:** interview_cataloging_2009-05-08.txt
- **Evidence:** "report on volume based on acquisitions, items on shelf, and items in circulation", "broken down by categories like total items, holds, adult fiction, board books, etc."
- **Manual provenance review required:** No
- **Confidence:** medium-high
- **Related questions/dependencies:** —

System shall generate a material volume report based on acquisitions, items on shelf, and items in circulation, with breakdowns by categories such as total items, holds, adult fiction, board books, and similar categories.

### REQ-256: Data quality reports for invalid item types, long call numbers, and bibliographic records with no items

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicit data integrity reporting needs listed.
- **Sources:** interview_cataloging_2009-05-08.txt
- **Evidence:** "Data quality reports - items with invalid item type, items with long call numbers, bibliographic records with no item records."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall provide data quality reports that identify items with invalid item types, items with excessively long call numbers, and bibliographic records that have no associated item records.

### REQ-257: Last edit date on reports excludes circulation activity

- **Category:** business rule
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicit requirement with a stated exception: exclude circulation from last edit date.
- **Sources:** interview_cataloging_2009-05-08.txt
- **Evidence:** "I need to be able to see the last edit date on reports, but it should be only when the item is edited and not include the last circulation.", "The current system combines these dates."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall display an item's last edit date on reports reflecting the most recent non-circulation edit; the last circulation date shall not be used as the 'last edit' date.

### REQ-258: Reports Working Group: document optimal Reports functionality and develop requirements

- **Category:** business rule
- **Priority:** P1 (source-supported)
- **Priority rationale:** This is a unanimously carried mission statement item that defines the primary purpose of the working group.
- **Sources:** meeting_minutes/meeting_2009-03-15_minutes.txt
- **Evidence:** "Reports Working Group Mission:", "- Document optimal Reports functionality within a future Evergreen release", "and develop a list of requirements."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System (via the Reports Working Group) shall document optimal Reports functionality for inclusion in a future Evergreen release and shall develop a list of requirements to implement that functionality.

### REQ-259: Reports Working Group: act as Reports testing group

- **Category:** business rule
- **Priority:** P1 (source-supported)
- **Priority rationale:** This is a mission statement item defining an explicit governance/processing role for Reports development.
- **Sources:** meeting_minutes/meeting_2009-03-15_minutes.txt
- **Evidence:** "- Become the Reports testing group, through which all new Reports development would be filtered."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System (via the Reports Working Group) shall serve as the Reports testing group through which all new Reports development is filtered.

### REQ-260: Compile reports for an Executive Reports Interface

- **Category:** business rule
- **Priority:** P1 (source-supported)
- **Priority rationale:** This is an explicit mission statement deliverable.
- **Sources:** meeting_minutes/meeting_2009-03-15_minutes.txt
- **Evidence:** "- Compile a list of reports needed for an Executive Reports Interface."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall compile a list of reports required for inclusion in an Executive Reports Interface.

### REQ-261: Determine and create templates for all PINES libraries

- **Category:** business rule
- **Priority:** P2 (source-supported)
- **Priority rationale:** This is an explicit mission statement deliverable, but it is less central than the core reporting/testing and executive reports items in the mission sequence.
- **Sources:** meeting_minutes/meeting_2009-03-15_minutes.txt
- **Evidence:** "- Determine and create templates needed for all PINES libraries."
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall determine and create the report templates needed for all PINES libraries.

### REQ-262: Exclude patron-facing day-to-day functions from Management Processes scope

- **Category:** constraint
- **Priority:** P1 (source-supported)
- **Priority rationale:** The minutes explicitly clarify what the scope does NOT include, as a constraint on requirements being specified.
- **Sources:** meeting_minutes/meeting_2009-03-15_minutes.txt
- **Evidence:** "She clarified that this does NOT include day-to-day patron-facing functions (those are part of the OPAC and circulation client)."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall exclude day-to-day patron-facing functions (those provided by the OPAC and the circulation client) from the Management Processes reporting/analysis scope.

### REQ-263: Management Processes scope: provide reports and analysis tools for managers/administrators/staff

- **Category:** business rule
- **Priority:** P1 (source-supported)
- **Priority rationale:** This defines the positive scope for the requirements being developed.
- **Sources:** meeting_minutes/meeting_2009-03-15_minutes.txt
- **Evidence:** "Katherine explained that the group would focus on Management Processes - that is, reports and analysis tools used by library managers, administrators, and staff for planning, evaluation, and oversight purposes."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall cover Management Processes — reports and analysis tools used by library managers, administrators, and staff for planning, evaluation, and oversight purposes.

### REQ-264: Management Processes scope: include analyses of collection use, branch capacity, patrons, staff productivity, and finances

- **Category:** business rule
- **Priority:** P2 (source-supported)
- **Priority rationale:** These are explicit scope items identified in the minutes.
- **Sources:** meeting_minutes/meeting_2009-03-15_minutes.txt
- **Evidence:** "The following scope items were identified:", "- Analyzing the Library collection and its use by patrons", "- Analyzing branch capacity and optimal distribution of the collection", "- Analyzing demographics and interests of patrons", "- Analyzing staff productivity and workflow", "- Tracking and verifying financial transactions"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall include requirements related to: analyzing the library collection and its use by patrons; analyzing branch capacity and optimal distribution of the collection; analyzing demographics and interests of patrons; analyzing staff productivity and workflow; and tracking and verifying financial transactions.

### REQ-265: Constrain requirements to management-related activities with assumed ILS data structures

- **Category:** constraint
- **Priority:** P2 (source-supported)
- **Priority rationale:** The minutes explicitly constrain what should be specified and note an assumption about ILS scope.
- **Sources:** meeting_minutes/meeting_2009-03-15_minutes.txt
- **Evidence:** "She said PINES is currently working on separate specifications for Acquisitions and Cataloging modules.", "The group agreed to specify only those requirements that directly or indirectly relate to management activities.", "Susan Sexton-Cooley noted that the current specification presupposes the general data structures and functionality of a full-fledged ILS."
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall specify only those requirements that directly or indirectly relate to management activities; the specification may presuppose the general data structures and functionality of a full-fledged ILS (separate specifications exist for Acquisitions and Cataloging).

### REQ-266: ReportsSpecificationFocus_FunctionalRequirementsFirst

- **Category:** constraint
- **Priority:** P2 (source-supported)
- **Priority rationale:** The minutes set an explicit precedence/approach for requirements definition (functional first; UI later with a specified method).
- **Sources:** meeting_minutes/meeting_2009-03-15_minutes.txt
- **Evidence:** "Dana Peeler raised the question of user interface specification.", "Katherine noted that while UI would eventually need detailed specification, for now the focus should be on functional requirements.", "She mentioned that UI and data structures would require further specification using an iterative, prototype-oriented methodology."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall focus initially on functional requirements for Reports, with UI and data structures to receive further detailed specification using an iterative, prototype-oriented methodology.

### REQ-267: ReportsIntendedAudience_NonTechnicalReadability

- **Category:** constraint
- **Priority:** P2 (source-supported)
- **Priority rationale:** This is an explicit requirement about documentation quality for intended audiences.
- **Sources:** meeting_minutes/meeting_2009-03-15_minutes.txt
- **Evidence:** "She emphasized the need to aim for a high level of readability for a non-technical audience while providing enough specificity for developers."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall aim for a high level of readability of the SRS for a non-technical audience while providing enough specificity for developers.

### REQ-268: ReportsDevelopmentApproach_CollaborativeIterativePrototypeReviews

- **Category:** business rule
- **Priority:** P3 (estimated)
- **Priority rationale:** This describes the assumed development approach; less directly testable as a software behavior requirement.
- **Sources:** meeting_minutes/meeting_2009-03-15_minutes.txt
- **Evidence:** "It was noted that development would likely happen in a highly collaborative and iterative environment where end-users have multiple opportunities to review prototypes."
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall be developed in a highly collaborative and iterative environment where end-users have multiple opportunities to review prototypes.

### REQ-269: ReportsScope_UserClasses_Definitions

- **Category:** other
- **Priority:** P3 (estimated)
- **Priority rationale:** User classes are explicitly discussed, but they do not directly state specific software behaviors; still may guide requirement derivation.
- **Sources:** meeting_minutes/meeting_2009-03-15_minutes.txt
- **Evidence:** "The group discussed the different types of users who would interact with Management Processes:", "Patron:", "Staff:", "Local System Administrators:", "Library Managers:", "Library Directors:", "Global System Administrator:"
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall consider distinct user classes for Management Processes, including Patrons, Staff, Local System Administrators, Library Managers, Library Directors, and a Global System Administrator.

### REQ-270: OE-1-Large-consortium-support-with-scale-and-non-disruptive-report-processing

- **Category:** business rule
- **Priority:** P1 (estimated)
- **Priority rationale:** This defines core scale requirements for the consortium operating environment and is central to the solution’s feasibility.
- **Sources:** meeting_minutes/meeting_2009-07-20_minutes.txt
- **Evidence:** OE-1: "...support a library consortium with 286 locations, 17 million annual circulations, purchasing and processing over 900,000 items per year."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall support a library consortium with 286 locations, 17 million annual circulations, and purchasing/processing of over 900,000 items per year.

### REQ-271: OE-1-Open-hours-background-report-processing-to-avoid-slowing-circulation-client

- **Category:** constraint
- **Priority:** P1 (estimated)
- **Priority rationale:** The minutes describe a key concern during peak hours and a specific mitigation (background processing/queuing).
- **Sources:** meeting_minutes/meeting_2009-07-20_minutes.txt
- **Evidence:** OE-1: "It is highly desirable that searches and reports can be processed during open hours without disrupting other system functions.", Discussion: "We need background processing/queuing to prevent report generation from slowing down the circulation client."
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall be able to process searches and reports during open hours without disrupting other system functions; report generation shall use background processing/queuing so that it does not slow the circulation client.

### REQ-272: OE-2-Linux-or-Solaris-server-operating-environment

- **Category:** constraint
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicit operating environment constraint that affects deployment and compatibility.
- **Sources:** meeting_minutes/meeting_2009-07-20_minutes.txt
- **Evidence:** OE-2: "Management Processes shall operate on a Linux or Solaris server.", [Consensus: Both Linux and Solaris are acceptable.]
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall operate on a Linux or Solaris server.

### REQ-273: OE-3-Web-browser-or-Windows-compatible-client-access

- **Category:** constraint
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicit accessibility/usage constraint defining supported client access methods.
- **Sources:** meeting_minutes/meeting_2009-07-20_minutes.txt
- **Evidence:** OE-3: "Management Processes shall be accessible through a web-browser or a Windows-compatible client."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall be accessible through a web browser or a Windows-compatible client.

### REQ-274: OE-4-Web-browser-compatibility-IE6-and-later-Firefox2-and-later

- **Category:** constraint
- **Priority:** P2 (source-supported)
- **Priority rationale:** Browser version support is an explicit compatibility requirement but narrower than general client access.
- **Sources:** meeting_minutes/meeting_2009-07-20_minutes.txt
- **Evidence:** OE-4: "If web-browser based... shall be accessible through Microsoft Internet Explorer (v.6.0 and later) and Mozilla Firefox (v.2.0 and later)."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

If the System is accessible via a web browser, System shall support Microsoft Internet Explorer (v.6.0 and later) and Mozilla Firefox (v.2.0 and later).

### REQ-275: OE-5-Accessibility-with-screen-reader-screen-magnification-and-assistive-software

- **Category:** constraint
- **Priority:** P1 (estimated)
- **Priority rationale:** Explicit accessibility requirement is stated as a legal requirement with mandatory Section 508 compliance in the discussion.
- **Sources:** meeting_minutes/meeting_2009-07-20_minutes.txt
- **Evidence:** OE-5: "...accessible with screen-reading software... and other software programs designed to increase accessibility.", Discussion: "Section 508 compliance is mandatory.", Discussion: "...support JAWS, NVDA, ZoomText, and other assistive technologies."
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall be accessible with screen-reading software, screen-magnification software, and other software programs designed to increase accessibility (including JAWS, NVDA, ZoomText), and shall comply with Section 508.

### REQ-276: CO-1-Fully-relational-database-back-end

- **Category:** constraint
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicit architectural constraint that determines data storage and querying model.
- **Sources:** meeting_minutes/meeting_2009-07-20_minutes.txt
- **Evidence:** CO-1: "Management Processes shall use a fully relational database back-end.", Discussion: "Evergreen already uses PostgreSQL."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall use a fully relational database back-end.

### REQ-277: CO-2-Standards-compliant-HTML-output

- **Category:** constraint
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicit output format requirement impacting UI rendering and help/report display.
- **Sources:** meeting_minutes/meeting_2009-07-20_minutes.txt
- **Evidence:** CO-2: "Management Processes shall produce standards-compliant HTML.", Discussion: "All web output needs to be valid HTML."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall produce standards-compliant HTML for its web output.

### REQ-278: CO-3-Dev-training-environment-and-config-migration-to-production

- **Category:** constraint
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicit requirement for supporting development/training workflows and configuration deployment.
- **Sources:** meeting_minutes/meeting_2009-07-20_minutes.txt
- **Evidence:** CO-3: "Management Processes shall provide a development and training environment with the ability to migrate configurations to a production environment.", Discussion: "...report templates and configurations can be exported/imported."
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall provide a development and training environment and shall support migrating configurations (including report templates and configurations) to a production environment.

### REQ-279: CO-4-Role-based-access-control-via-security-groups-and-or-roles

- **Category:** security
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicit access control and security model requirement.
- **Sources:** meeting_minutes/meeting_2009-07-20_minutes.txt
- **Evidence:** CO-4: "User rights and privileges will be controlled through security groups and/or \"roles\" that allow access control for individuals, workgroups, and arbitrary staff groups."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall control user rights and privileges through security groups and/or roles that allow access control for individuals, workgroups, and arbitrary staff groups.

### REQ-280: CO-5-Do-not-constrain-OPAC-module-functionality

- **Category:** constraint
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicit non-interference constraint protecting a major subsystem (OPAC).
- **Sources:** meeting_minutes/meeting_2009-07-20_minutes.txt
- **Evidence:** CO-5: "These requirements shall not constrain functionality or features of the Online Public Access Catalog (OPAC) module.", Discussion: "...management processes are separate... should not affect patron access."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall not constrain functionality or features of the Online Public Access Catalog (OPAC) module.

### REQ-281: UD-1-Developer-data-specifications-for-record-types

- **Category:** documentation
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicit documentation deliverable for developer integration/queries.
- **Sources:** meeting_minutes/meeting_2009-07-20_minutes.txt
- **Evidence:** UD-1: "The software developer shall provide complete data specifications for authority records..."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall require the software developer to provide complete data specifications for authority records, bibliographic records, order records, item records, hold/request records, and other records maintained or accessed by Management Processes.

### REQ-282: UD-2-Developer-high-level-process-description-import-export-validation-and-standard-reports

- **Category:** documentation
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicit developer documentation requirement covering key processes.
- **Sources:** meeting_minutes/meeting_2009-07-20_minutes.txt
- **Evidence:** UD-2: "The software developer shall provide a thorough high-level description of major processes, including bibliographic record import and export... validation... and standard reports."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall require the software developer to provide a thorough high-level description of major processes, including bibliographic record import and export, validation of bibliographic records against internal and external authority sources, and standard reports.

### REQ-283: UD-3-Online-hierarchical-cross-linked-HTML-help-system-describing-all-functions

- **Category:** documentation
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicit help system requirement impacting usability and documentation access.
- **Sources:** meeting_minutes/meeting_2009-07-20_minutes.txt
- **Evidence:** UD-3: "The system shall provide an online, hierarchical, and cross-linked help system in HTML that describes and illustrates all system functions.", Discussion: "Context-sensitive help is critical."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall provide an online, hierarchical, and cross-linked help system in HTML that describes and illustrates all system functions.

### REQ-284: UD-4-Error-reporting-and-administrator-query-diagnostics

- **Category:** documentation
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicit operational feedback requirement, including administrator-specific query-level diagnostics.
- **Sources:** meeting_minutes/meeting_2009-07-20_minutes.txt
- **Evidence:** UD-4: "The system shall provide thorough high-level error reporting and feedback", UD-4: "...and shall allow low-level query-specific feedback for Local and Global System Administrators from the front-end interface."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall provide thorough high-level error reporting and feedback and shall allow low-level, query-specific feedback/diagnostics for Local and Global System Administrators from the front-end interface.

### REQ-285: Relational-database-backend

- **Category:** constraint
- **Priority:** P1 (source-supported)
- **Priority rationale:** Stated as a confirmed requirement/constraint during database constraints discussion.
- **Sources:** meeting_tech_subcommittee_2009-06-30.txt
- **Evidence:** "the system must use a fully relational database back-end" (meeting_tech_subcommittee_2009-06-30.txt)
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall use a fully relational database back-end.

### REQ-286: Work-with-relational-structure-avoid-denormalization-for-reporting

- **Category:** constraint
- **Priority:** P2 (estimated)
- **Priority rationale:** Explicit recommendation phrased as strong guidance against denormalization; treated as a requirement to preserve intent.
- **Sources:** meeting_tech_subcommittee_2009-06-30.txt
- **Evidence:** "The reporting system must work WITH the relational structure, not against it.", "I strongly recommend against denormalization for reporting"
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall work with the relational structure of the database rather than against it, and shall avoid denormalization for reporting.

### REQ-287: HTML-standards-compliance-and-validation

- **Category:** constraint
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicitly stated as a must/requirement in HTML compliance discussion and reinforced by a direct validation requirement.
- **Sources:** meeting_tech_subcommittee_2009-06-30.txt
- **Evidence:** "The system must produce standards-compliant HTML.", "We need to make sure all HTML output validates against W3C standards"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall produce standards-compliant HTML and shall ensure all HTML output validates against W3C standards.

### REQ-288: Separate-development-training-and-production-environments

- **Category:** constraint
- **Priority:** P2 (estimated)
- **Priority rationale:** Discussed as needed capability based on existing servers; not stated as a formal 'shall' in notes, so treated as required but priority estimated.
- **Sources:** meeting_tech_subcommittee_2009-06-30.txt
- **Evidence:** "We have a dev server, a training server, and production", "What we need is a way to migrate configurations between them."
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall support separate development, training, and production environments.

### REQ-289: Migrate-configurations-between-environments-via-export-import

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicitly identified as what is needed to migrate configurations and lists concrete artifacts.
- **Sources:** meeting_tech_subcommittee_2009-06-30.txt
- **Evidence:** "Export/import of templates, permission settings, and saved queries."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall allow migrating configurations between development, training, and production environments via export/import of templates, permission settings, and saved queries.

### REQ-290: Training-environment-safety

- **Category:** security
- **Priority:** P1 (source-supported)
- **Priority rationale:** Security/safety expectation explicitly called out by Katherine.
- **Sources:** meeting_tech_subcommittee_2009-06-30.txt
- **Evidence:** "the training environment needs to be safe - staff should be able to experiment without risking production data."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall ensure the training environment is safe so staff can experiment without risking production data.

### REQ-291: Role-based-access-control-with-groups-and-roles

- **Category:** security
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicitly described as needed for access control.
- **Sources:** meeting_tech_subcommittee_2009-06-30.txt
- **Evidence:** "We need security groups and/or 'roles' that allow access control for individuals, workgroups, and arbitrary staff groups."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall implement role-based access control using security groups and/or roles that allow access control for individuals, workgroups, and arbitrary staff groups.

### REQ-292: Change-user-permissions-via-role-assignment

- **Category:** security
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicitly stated as desired capability for permission changes.
- **Sources:** meeting_tech_subcommittee_2009-06-30.txt
- **Evidence:** "The system should make it easy to change someone's permissions by simply changing their role assignment."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall allow changing a user's permissions by updating their role assignment.

### REQ-293: Global-Admin-role-with-full-system-access

- **Category:** security
- **Priority:** P2 (estimated)
- **Priority rationale:** Defined in key points; role semantics likely required, but not stated as 'shall' in the notes; priority is estimated.
- **Sources:** meeting_tech_subcommittee_2009-06-30.txt
- **Evidence:** "Global Admin: Full system access"
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall provide a Global Admin role with full system access.

### REQ-294: Local-Admin-role-for-branch-level-reporting-and-configuration

- **Category:** security
- **Priority:** P2 (estimated)
- **Priority rationale:** Role definition present; wording is key point rather than explicit shall; priority is estimated.
- **Sources:** meeting_tech_subcommittee_2009-06-30.txt
- **Evidence:** "Local Admin: Branch-level reporting and configuration"
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall provide a Local Admin role that supports branch-level reporting and configuration.

### REQ-295: Library Manager run approved reports with limited template modification

- **Category:** security
- **Priority:** P2 (estimated)
- **Priority rationale:** Role definition present; limited bounds not specified further.
- **Sources:** meeting_tech_subcommittee_2009-06-30.txt
- **Evidence:** "Library Manager: Run approved reports, limited template modification"
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall provide a Library Manager role that can run approved reports and modify report templates only within limited bounds.

### REQ-296: Staff role run reports within assigned permissions

- **Category:** security
- **Priority:** P2 (estimated)
- **Priority rationale:** Role definition present; permission mechanism is detailed elsewhere.
- **Sources:** meeting_tech_subcommittee_2009-06-30.txt
- **Evidence:** "Staff: Run reports within assigned permissions"
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall provide a Staff role that can run reports within assigned permissions.

### REQ-297: Patron role indirect access through OPAC displays

- **Category:** security
- **Priority:** P3 (estimated)
- **Priority rationale:** Role definition present; integration details are elsewhere and only 'indirect access' is specified.
- **Sources:** meeting_tech_subcommittee_2009-06-30.txt
- **Evidence:** "Patron: Indirect access through OPAC displays"
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall provide a Patron role with indirect access through OPAC displays.

### REQ-298: Reporting must not degrade OPAC performance

- **Category:** constraint
- **Priority:** P1 (source-supported)
- **Priority rationale:** Stated emphatically as a constraint with an explicit exception/condition (report running).
- **Sources:** meeting_tech_subcommittee_2009-06-30.txt
- **Evidence:** "We absolutely cannot constrain the OPAC", "If a report is running, it should not slow down the OPAC."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall not constrain the OPAC; when a report is running, it shall not slow down the OPAC.

### REQ-299: Provide complete data specifications (data dictionaries)

- **Category:** business rule
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicit 'developer must provide complete data specifications' plus concrete contents.
- **Sources:** meeting_tech_subcommittee_2009-06-30.txt
- **Evidence:** "The developer must provide complete data specifications for:", "We need data dictionaries - field names, data types, relationships."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall provide complete data specifications for authority, bibliographic, order, item, hold/request, and other records maintained or accessed by Management Processes, including field names, data types, and relationships.

### REQ-300: Provide thorough high-level process descriptions

- **Category:** business rule
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicit list of processes under process descriptions requirement.
- **Sources:** meeting_tech_subcommittee_2009-06-30.txt
- **Evidence:** "The developer must provide a thorough high-level description of major processes, including:", "Bibliographic record import and export", "Validation of bibliographic records against internal and external authority sources", "Standard reports"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall provide thorough high-level process descriptions including bibliographic record import/export, validation of bibliographic records against internal and external authority sources, and standard reports.

### REQ-301: Online help system is hierarchical, cross-linked, and HTML

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicit 'shall' requirement.
- **Sources:** meeting_tech_subcommittee_2009-06-30.txt
- **Evidence:** "The system shall provide an online, hierarchical, and cross-linked help system in HTML."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall provide an online, hierarchical, and cross-linked help system in HTML.

### REQ-302: Help system accessibility for screen readers

- **Category:** accessibility
- **Priority:** P1 (source-supported)
- **Priority rationale:** Accessibility requirement stated explicitly in help system discussion.
- **Sources:** meeting_tech_subcommittee_2009-06-30.txt
- **Evidence:** "This has to be accessible too. The help system needs to work with screen readers."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall ensure the online help system works with screen readers.

### REQ-303: Thorough high-level error reporting with administrator query-specific feedback

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicit 'shall' with both general and administrator/query-specific feedback expectations.
- **Sources:** meeting_tech_subcommittee_2009-06-30.txt
- **Evidence:** "The system shall provide thorough high-level error reporting and feedback, and shall allow low-level query-specific feedback for administrators.", "When a report fails, we need to know WHY"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall provide thorough high-level error reporting and feedback, and shall allow low-level query-specific feedback for administrators.

### REQ-304: Error reporting shall identify table, field, and error type

- **Category:** functional
- **Priority:** P2 (estimated)
- **Priority rationale:** Explicit specifics requested; phrased as 'need' in discussion, but tied to error reporting requirement.
- **Sources:** meeting_tech_subcommittee_2009-06-30.txt
- **Evidence:** "We need specifics - which table, which field, what kind of error."
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall include error specifics identifying which table, which field, and what kind of error when a report fails.

### REQ-305: Management Processes are part of an enterprise-level Library Automation System

- **Category:** business rule
- **Priority:** P3 (estimated)
- **Priority rationale:** Stated as an assumption (AS-1) about context; included as requirement-like dependency but could be non-testable.
- **Sources:** meeting_tech_subcommittee_2009-06-30.txt
- **Evidence:** "AS-1: Management Processes are part of an enterprise-level Library Automation System."
- **Manual provenance review required:** No
- **Confidence:** low
- **Related questions/dependencies:** —

System shall be part of an enterprise-level Library Automation System.

### REQ-306: Management Processes are consolidated centrally and serve multiple locations

- **Category:** business rule
- **Priority:** P3 (estimated)
- **Priority rationale:** Stated as an assumption (AS-2); included only as requirement-like constraint due to 'provide services to multiple locations'.
- **Sources:** meeting_tech_subcommittee_2009-06-30.txt
- **Evidence:** "AS-2: Management Processes are consolidated at a central location, and accept input and provide services to multiple locations."
- **Manual provenance review required:** No
- **Confidence:** low
- **Related questions/dependencies:** —

System shall be consolidated at a central location and accept input and provide services to multiple locations.

### REQ-307: Rely on enterprise Library Automation System data structures and functionality (Acquisitions, Cataloging)

- **Category:** constraint
- **Priority:** P3 (estimated)
- **Priority rationale:** Stated as dependency (DE-1); likely true for design but explicitly labeled dependency/assumption.
- **Sources:** meeting_tech_subcommittee_2009-06-30.txt
- **Evidence:** "DE-1: Management Processes rely on the data structures and functionality of an enterprise-level Library Automation System, including Acquisitions and Cataloging modules.", "the reporting system doesn't manage acquisitions or cataloging - it just reads the data."
- **Manual provenance review required:** No
- **Confidence:** low
- **Related questions/dependencies:** —

System shall rely on the data structures and functionality of an enterprise-level Library Automation System, including Acquisitions and Cataloging modules.

### REQ-308: Interface with vendor websites via APIs and/or standard-format data file transfer

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicit vendor integration dependency with examples.
- **Sources:** meeting_tech_subcommittee_2009-06-30.txt
- **Evidence:** "DE-2: Management Processes interface with a variety of vendor websites, via published APIs and/or automated transfer of standard-format data files (e.g., USMARC21, EDIFACT)."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall interface with vendor websites via published APIs and/or automated transfer of standard-format data files (e.g., USMARC21, EDIFACT).

### REQ-309: Handle vendor data that may be absent at some libraries

- **Category:** business rule
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicit exception condition in vendor integration discussion.
- **Sources:** meeting_tech_subcommittee_2009-06-30.txt
- **Evidence:** "we can't rely on it being present at every library."
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall handle vendor-provided data even when it is not present at every library.

### REQ-310: OPAC read-only interaction

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicit integration dependency and explicit behavior restriction provided by the technical-subcommittee source; this is required for correct integration with the OPAC and to avoid unintended data changes.
- **Sources:** meeting_tech_subcommittee_2009-06-30.txt
- **Evidence:** "DE-3: Management Processes interact with a patron interface (OPAC).", "The reporting system queries this data, but doesn't modify it."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall interact with the patron interface (OPAC) by querying circulation- and hold-related data but shall not modify OPAC data.

### REQ-311: Support multiple report output formats (Excel, CSV, HTML)

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Required output formats are explicitly listed in the technical-subcommittee input (P1). A similar survey result lists the same formats but with a lower priority rating (P2). The higher priority (P1) from the technical-subcommittee source is used here because it states the formats as required; however the differing priority between sources is recorded as an unresolved question.
- **Sources:** meeting_tech_subcommittee_2009-06-30.txt, survey_results_2009.txt
- **Evidence:** "Excel, HTML, and CSV formats are required.", "Multiple output formats (Excel, CSV, HTML): 61%"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall support exporting/reporting in multiple output formats, specifically including Excel, CSV, and HTML.

### REQ-312: Real-time and historical reporting

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicit statement about the need for both report types and example conditions; considered a high-priority functional capability for reporting correctness and completeness.
- **Sources:** meeting_tech_subcommittee_2009-06-30.txt
- **Evidence:** "Some reports need to be real-time - like 'what's overdue today,'", "Others are historical - 'what was the bill amount on June 30th?'"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall support both real-time reporting (for current-state queries, e.g., what is overdue today) and historical reporting (for past-state queries, e.g., what was the bill amount on a specified past date).

### REQ-313: Reporting warehouse for historical data (likely)

- **Category:** constraint
- **Priority:** P4 (estimated)
- **Priority rationale:** Candidate is phrased probabilistically ('We probably need'), so it is recorded as a low-priority/anticipated architectural constraint; priority is estimated in the source.
- **Sources:** meeting_tech_subcommittee_2009-06-30.txt
- **Evidence:** "We probably<br>need a reporting warehouse for historical data."
- **Manual provenance review required:** No
- **Confidence:** low
- **Related questions/dependencies:** —

System shall provide (or make use of) a reporting warehouse for historical data (this is currently stated as likely/anticipated rather than mandated).

### REQ-314: Cancel scheduled or running reports

- **Category:** functional
- **Priority:** P2 (estimated)
- **Priority rationale:** Marked technically feasible and explicitly recommended to implement via checking for cancellation signals during processing. Priority rated medium (P2) reflecting technical importance but not top-most urgency.
- **Sources:** meeting_tech_subcommittee_2009-06-30.txt
- **Evidence:** "The ability to cancel a scheduled or running report is technically feasible, but requires the system to check for cancellation signals during report processing."
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall allow canceling a scheduled or currently running report by detecting and honoring cancellation signals during report processing.

### REQ-315: Include nulls and blank fields in report results

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicitly required to ensure output completeness and consistent downstream processing; sourced from the technical-subcommittee discussion and rated high priority.
- **Sources:** meeting_tech_subcommittee_2009-06-30.txt
- **Evidence:** "All nulls and blank fields must be included in the results,"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall include null and blank field values in report result exports (i.e., fields that are null/blank must be present in exported results rather than being omitted).

### REQ-316: Filter surveys by name (internal name-to-ID resolution)

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicitly described behavior to improve usability; assigned medium priority in the source material.
- **Sources:** meeting_tech_subcommittee_2009-06-30.txt
- **Evidence:** "filter by survey name rather than survey ID requires the system to resolve names to IDs internally."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall support filtering by survey name by resolving survey names to their internal IDs transparently during query processing.

### REQ-317: Create report templates

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Identified as a top interface feature (81%) in the survey and explicitly listed in the requirements summary; considered a core capability for users who prepare recurring or standard reports.
- **Sources:** survey_results_2009.txt
- **Evidence:** "Ability to create report templates: 81%", "9. Report templates can be created by administrators and run as-is or modified."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall allow authorized staff to create report templates.

### REQ-318: Run or modify report templates

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Described in the requirements summary; assigned medium priority (P2) relative to template creation which had higher priority in survey responses.
- **Sources:** survey_results_2009.txt
- **Evidence:** "9. Report templates can be created by administrators and run as-is or modified."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall allow authorized users to run report templates as-is or to modify templates before running.

### REQ-319: Fine-grained permissions for creating, running, and cloning reports

- **Category:** security
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicitly identified as a top-priority feature (76%) in the survey and called out in the requirements summary; critical for multi-tenant or multi-role security and governance.
- **Sources:** survey_results_2009.txt
- **Evidence:** "Fine-grained permissions (who can create/run what): 76%", "10. Fine-grained permissions limit who can create and clone reports."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall enforce fine-grained permissions controlling which users can create, run, modify, or clone specific reports or report templates.

### REQ-320: Save and reuse report queries

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** High importance in survey results (73% and 58% in related phrasing); supports efficiency for repeated reporting tasks and is therefore high priority.
- **Sources:** survey_results_2009.txt
- **Evidence:** "Ability to save and reuse queries: 73%", "8. Save queries for repeated use: 58%"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall allow users to save report queries for later reuse.

### REQ-321: Visibility into report processing queue

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Selected as important (68%) in the survey; medium priority because it affects user experience and operational transparency but is not rated topmost.
- **Sources:** survey_results_2009.txt
- **Evidence:** "Report queue visibility (where my report is in the queue): 68%", "12. Ability to see where your report is in the queue."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall provide visibility to users into where their report is in the processing queue (e.g., queued, running, completed, failed).

### REQ-322: Email delivery of reports

- **Category:** functional
- **Priority:** P3 (source-supported)
- **Priority rationale:** Requested by respondents (45%) but less prevalent than top items; recorded as lower priority relative to core report creation and format features.
- **Sources:** survey_results_2009.txt
- **Evidence:** "Email delivery of reports: 45%"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall support delivering report output via email.

### REQ-323: Schedule recurring reports

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicitly requested as important (52%) and logically tied to the cancel-scheduled-report capability; medium priority reflects operational importance.
- **Sources:** survey_results_2009.txt
- **Evidence:** "Ability to schedule recurring reports: 52%", "Ability to cancel a scheduled or running report"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall allow users to schedule recurring reports (e.g., daily, weekly, monthly) to run automatically.

### REQ-324: CancelScheduledOrRunningReport

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicit feature request; ties to scheduling and long-running report issues.
- **Sources:** survey_results_2009.txt
- **Evidence:** "Ability to cancel a scheduled or running report"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall allow users to cancel a scheduled or currently running report.

### REQ-325: AnonymizedDemographicStatistics

- **Category:** security
- **Priority:** P1 (source-supported)
- **Priority rationale:** Stated as a must-have constraint and explicitly mentions anonymization.
- **Sources:** survey_results_2009.txt
- **Evidence:** "Demographic statistics (must be anonymized - no personally identifiable info)", "7. Demographic statistics include transactions by geographical regions and age ranges. Data must be anonymized."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall produce demographic statistics using anonymized data with no personally identifiable information.

### REQ-326: DemographicStatisticsByGeographicalRegionsAndAgeRanges

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Directly requested and repeated in the requirements summary.
- **Sources:** survey_results_2009.txt
- **Evidence:** "Transactions by geographical regions", "Transactions by age ranges", "7. Demographic statistics include transactions by geographical regions and age ranges."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall provide demographic statistics that include transactions by geographical regions and by age ranges.

### REQ-327: PredictOrUnderstandPatronBehavior

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicit requirement in the summary; detailed examples are present in survey question responses.
- **Sources:** survey_results_2009.txt
- **Evidence:** "We need to predict patron behavior. How likely is a book to be renewed?", "8. System produces statistics to understand/predict patron behavior and use of materials."
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall produce statistics to understand and/or predict patron behavior and use of materials.

### REQ-328: TransactionGroupingDimensions

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Directly listed in key findings and in the requirements summary.
- **Sources:** survey_results_2009.txt
- **Evidence:** "Transactions can be grouped by hour, terminal, branch, and system.", "2. Transactions can be grouped by hour, terminal, branch, and system."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall allow transactions to be grouped by hour, terminal, branch, and system.

### REQ-329: TransactionHistoryRetentionWithAggregates

- **Category:** business rule
- **Priority:** P1 (estimated)
- **Priority rationale:** Explicit in requirements summary as a key requirement.
- **Sources:** survey_results_2009.txt
- **Evidence:** "1. Transaction history maintained for X days (configurable), with monthly and annual aggregates retained indefinitely."
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall maintain transaction history for a configurable number of days, and retain monthly and annual aggregates indefinitely.

### REQ-330: CheckinCountsByPlacementAndCumulative

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicitly identified as a top need and detailed in the requirements summary.
- **Sources:** survey_results_2009.txt
- **Evidence:** "I need to see check-in counts broken down by method - book drop vs terminal vs self-service", "3. All types of check-in counted individually and cumulatively: book-drop, terminal, by user or self-service."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall count check-ins individually and cumulatively by method, including book drop, terminal, and user/self-service.

### REQ-331: CheckoutCountsByTypeAndCumulative

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Explicitly detailed in both open-ended responses and requirements summary.
- **Sources:** survey_results_2009.txt
- **Evidence:** "Check-out types should be counted separately - staff checkout, self checkout, staff renewal, self checkout renewal, online renewal, OPAC renewal", "4. All types of check-out counted individually and cumulatively: staff checkout, self checkout, staff renewal, self checkout renewal, online renewal, OPAC renewal."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall count check-outs individually and cumulatively by type, including staff checkout, self checkout, staff renewal, self checkout renewal, online renewal, and OPAC renewal.

### REQ-332: HoldsCountsByPlacementMethod

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Directly stated and included in requirements summary.
- **Sources:** survey_results_2009.txt
- **Evidence:** "Holds reports should show how the hold was placed - at staff desk, at public computer, or remotely", "5. Holds counted with method of placement: at staff desk, public computer, or remotely."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall count holds and show the method of placement, including at the staff desk, at a public computer, or remotely.

### REQ-333: TransactionsReportHoldsFilledAndPerEntities

- **Category:** functional
- **Priority:** P1 (source-supported)
- **Priority rationale:** Comprehensive requirement explicitly enumerated in the requirements summary.
- **Sources:** survey_results_2009.txt
- **Evidence:** "6. Transactions report can show holds placed, holds filled, and check-outs per patron, per library, per group of libraries, per system, per county."
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall provide a transactions report that can show holds placed, holds filled, and check-outs, with results viewable per patron, per library, per group of libraries, per system, and per county.

### REQ-334: AllowQueryCandidateMaterials

- **Category:** functional
- **Priority:** P3 (source-supported)
- **Priority rationale:** Admin feature is listed as needed but no other details or prominence percentage beyond 44%.
- **Sources:** survey_results_2009.txt
- **Evidence:** "Query for candidate materials: 44%"
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall support a query feature for candidate materials.

### REQ-335: ManuallySelectFromQueryResults

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicit admin feature request (39%) and likely part of a workflow.
- **Sources:** survey_results_2009.txt
- **Evidence:** "Manually select from query results: 39%"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall allow users to manually select from query results.

### REQ-336: ChangeRecordsToMoveItemsToNewLocation

- **Category:** functional
- **Priority:** P3 (source-supported)
- **Priority rationale:** Administrative workflow feature requested (31%); less prominent than top report/UI items.
- **Sources:** survey_results_2009.txt
- **Evidence:** "Change records to move items to new location: 31%"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall allow changing records to move items to a new location.

### REQ-337: RevertItemsToOriginalLocation

- **Category:** functional
- **Priority:** P4 (source-supported)
- **Priority rationale:** Requested but with lower prevalence (18%).
- **Sources:** survey_results_2009.txt
- **Evidence:** "Revert items to original location: 18%"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall allow reverting items back to their original location.

### REQ-338: CountAndTrackRecordDeletions

- **Category:** functional
- **Priority:** P4 (source-supported)
- **Priority rationale:** Requested as an additional administrative feature (27%).
- **Sources:** survey_results_2009.txt
- **Evidence:** "Count and track record deletions: 27%"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall support counting and tracking record deletions.

### REQ-339: IncludeAllNullsAndBlankFieldsInResults

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicit additional feature request.
- **Sources:** survey_results_2009.txt
- **Evidence:** "All nulls and blank fields must be included in results"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall include all nulls and blank fields in report results.

### REQ-340: HistoricalReportingForSpecificPastDate

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicitly requested as historical reporting capability.
- **Sources:** survey_results_2009.txt
- **Evidence:** "Historical reporting - I want to see what the data looked like on a specific date in the past, even if the shelving location has changed"
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall provide historical reporting to view what the data looked like on a specific past date, even if shelving location has changed.

### REQ-341: PivotTableOutput

- **Category:** functional
- **Priority:** P4 (source-supported)
- **Priority rationale:** Requested but not tied to a percentage or other urgency evidence.
- **Sources:** survey_results_2009.txt
- **Evidence:** "Pivot table output would be great"
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall support pivot table output.

### REQ-342: RealTimeReportingForBusyPeriods

- **Category:** functional
- **Priority:** P2 (source-supported)
- **Priority rationale:** Explicit feature request; related to current issues about long-running reports during busy hours.
- **Sources:** survey_results_2009.txt
- **Evidence:** "Real-time reporting for busy periods", "Reports take too long to run during busy hours"
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall support real-time (or near-real-time) reporting for busy periods.

### REQ-343: IncludeLastCirculationDateOnItemReports

- **Category:** functional
- **Priority:** P3 (source-supported)
- **Priority rationale:** Explicit additional feature request.
- **Sources:** survey_results_2009.txt
- **Evidence:** "Ability to indicate last circulation date on item reports"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall provide the ability to indicate the last circulation date on item reports.

### REQ-344: CheckinDateTimeShouldNotIncludeRenewals

- **Category:** functional
- **Priority:** P3 (source-supported)
- **Priority rationale:** Explicit constraint to exclude renewals from check-in date/time.
- **Sources:** survey_results_2009.txt
- **Evidence:** "Checkin date/time should not include renewals"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall ensure check-in date/time does not include renewals.

### REQ-345: SnapshotBillsReportBackInTime

- **Category:** functional
- **Priority:** P3 (source-supported)
- **Priority rationale:** Explicitly requested additional reporting capability.
- **Sources:** survey_results_2009.txt
- **Evidence:** "Need a snapshot bills report going back in time"
- **Manual provenance review required:** No
- **Confidence:** high
- **Related questions/dependencies:** —

System shall support a snapshot bills report going back in time.

### REQ-346: SharedFoldersToAllowDisallowRunningSpecificReports

- **Category:** security
- **Priority:** P2 (estimated)
- **Priority rationale:** Stated in the requirements summary as a key identified requirement.
- **Sources:** survey_results_2009.txt
- **Evidence:** "11. Shared folders to allow/disallow staff from running specific reports."
- **Manual provenance review required:** No
- **Confidence:** medium
- **Related questions/dependencies:** —

System shall provide shared folders or equivalent access controls to allow or disallow staff from running specific reports.

## E. Blacklist of rejected candidates

### BL-001: Color-coding of branch capacity status (green/yellow/red)

- **Sources:** conversations/conv_pines015_capacity_interface.eml
- **Reason:** Proposed as an idea (“Maybe color-coding”), not stated as a requirement in the summary.
- **Related requirements/evidence:** —
- **Human review required:** No

### BL-002: Using GROUP BY clauses for per-library and per-system breakdown

- **Sources:** conversations/conv_pines016_shelf_space.eml
- **Reason:** Implementation detail (SQL approach) rather than a testable software requirement statement.
- **Related requirements/evidence:** ShelfSpaceReport-ScopePerLibraryAndPerSystem
- **Human review required:** No

### BL-003: Personal remarks about a cat, coffee, fences, and goldfish.

- **Sources:** conversations/conv_pines018_item_transfer.eml
- **Reason:** Not software requirements.
- **Related requirements/evidence:** —
- **Human review required:** No

### BL-004: Action items about who will investigate or coordinate testing.

- **Sources:** —
- **Reason:** Project management notes rather than software requirements.
- **Related requirements/evidence:** —
- **Human review required:** No

### BL-005: Question about default value of X for in-transit items (e.g., 7 days).

- **Sources:** conversations/conv_pines019_020_missing_intransit.eml
- **Reason:** This is a suggestion/possible default in discussion rather than an explicit requirement to set a specific default value.
- **Related requirements/evidence:** In-transit items report threshold configurable X days
- **Human review required:** No

### BL-006: Whether the last copy report should be per library or per system (discussion proposing both).

- **Sources:** conversations/conv_pines021_item_purging.eml
- **Reason:** This discussion is captured in the explicit requirement that the last copy report be available per system (and in scope for library or system). No separate rejected requirement needed.
- **Related requirements/evidence:** Last copy report in scope of library system (consortium level), Last copy report scope includes per system view
- **Human review required:** No

### BL-007: Whether volume/copy/no-items deletion should be automated or manual.

- **Sources:** conversations/conv_pines021_item_purging.eml
- **Reason:** The document asks/raises a design question about automation vs manual; no explicit requirement on the automation level is stated.
- **Related requirements/evidence:** Quick effective deletion of volume entries along with copy entries and records with no items attached
- **Human review required:** No

### BL-008: Coffee/snacks, TV watching, and other non-software remarks.

- **Sources:** conversations/conv_pines019_020_missing_intransit.eml, conversations/conv_pines021_item_purging.eml
- **Reason:** Not related to software requirements.
- **Related requirements/evidence:** —
- **Human review required:** No

### BL-009: Implementation note requesting database trigger and computing age range from birth_date at query time.

- **Sources:** conversations/conv_pines022_deletions.eml, conversations/conv_pines023_patron_characteristics.eml
- **Reason:** These are implementation details rather than atomic, testable software requirements (e.g., 'trigger' and 'compute at query time') without a user-facing or externally verifiable requirement statement beyond the already-captured audit fields and configurable age range behavior.
- **Related requirements/evidence:** DeletionTracking_AuditFieldsLogged, PatronCharacteristics_ConfigureAgeRanges
- **Human review required:** No

### BL-010: Unprioritized anecdotal requests such as counting deletions per quarter or example queries.

- **Sources:** conversations/conv_pines022_deletions.eml, conversations/conv_pines023_patron_characteristics.eml
- **Reason:** Examples and context (e.g., director asked for Q1 report; targeted summer reading program) are not standalone requirements and are already covered by consolidated requirements about periods and limit/group-by capabilities.
- **Related requirements/evidence:** DeletionTracking_AdminReportsTotalsAndTopUsers, PatronCharacteristics_QueryLimitAndGroupBy, PatronCharacteristics_CombineFiltersWithAndOr
- **Human review required:** No

### BL-011: Use OPAC logging only for electronic activity (excluding other electronic actions).

- **Sources:** conversations/conv_pines024_inactive_patrons.eml
- **Reason:** Not a requirement; electronic activity is explicitly defined to include multiple actions (login, holds, renewals, and optionally digital access).
- **Related requirements/evidence:** Configurable electronic activity definition
- **Human review required:** No

### BL-012: Require only online account access (OPAC usage) and not physical checkouts as part of inactivity definition.

- **Sources:** conversations/conv_pines024_inactive_patrons.eml
- **Reason:** The consolidated requirement states no circulation OR electronic activity in the last X days; electronic activity clarification does not override the circulation requirement.
- **Related requirements/evidence:** Generate inactive patrons list
- **Human review required:** No

### BL-013: Restrict configurable X to one of the listed ranges (30/90/180/365 days).

- **Sources:** conversations/conv_pines024_inactive_patrons.eml
- **Reason:** Those ranges are discussed as examples; requirement is that X is configurable/customizable (not limited to those values).
- **Related requirements/evidence:** Configurable inactivity window X
- **Human review required:** No

### BL-014: Requirements marked as draft notes/metadata such as the document being "DRAFT" and "requirements are subject to change".

- **Sources:** early_draft_srs_galecia.txt
- **Reason:** Not a software requirement; it is document-status information.
- **Related requirements/evidence:** —
- **Human review required:** No

### BL-015: Assumptions and dependencies such as AS-1/DE-1/AS-2/DE-2/DE-3 that state integration relationships.

- **Sources:** early_draft_srs_galecia.txt
- **Reason:** These are explicitly labeled assumptions/dependencies rather than software requirements.
- **Related requirements/evidence:** —
- **Human review required:** No

### BL-016: Appendix A list of report categories (e.g., "Check in Count", "Checkout Count", "Items overdue by X days") considered as atomic requirements could be mistaken for requirements, but only examples/categories are provided without explicit shall/must statements for each item in the excerpt.

- **Sources:** early_draft_srs_galecia.txt
- **Reason:** These appear as enumerated report types/categories rather than separately stated requirements with explicit behavioral constraints; would require further context to avoid inventing atomic requirements.
- **Related requirements/evidence:** Support reporting definitions described in Appendix A, Support fine-grained reports requirements described in Appendix B
- **Human review required:** No

### BL-017: Generic statement that reports should be viewed/queued; appears as part of reporting interface but not enough detail in the provided snippet to form a single atomic software requirement beyond the fine-grained list.

- **Sources:** early_draft_srs_galecia.txt
- **Reason:** The user asked to extract atomic, evidence-supported software requirements from the source documents provided; the provided snippet contains many fine-grained reporting requirements, but not all are included here because the user provided instructions to ignore irrelevant discussion and the assistant only returned financial reporting requirements from the other document. If you want all fine-grained reporting requirements from early_draft_srs_galecia.txt extracted as well, request that explicitly.
- **Related requirements/evidence:** -
- **Human review required:** No

### BL-018: Need for streamlined login due to staff time loss and password sharing/terminals left logged in.

- **Sources:** email_staff_login.eml
- **Reason:** This is explanatory motivation/rationale (performance and security problems) rather than an explicit testable software requirement.
- **Related requirements/evidence:** STREAMLINED_optional_card_swipe_login, TRADITIONAL_username_password_fallback, STAFF_login_tracks_which_staff_member_logged_in_for_audit, STREAMLINED_login_does_not_bypass_individual_authentication_entirely
- **Human review required:** No

### BL-019: Attempted extraction of a requirement about specific canned report names/counts as functional behavior for the enhanced system (e.g., 'Checkout Count report exists'), which is already explicitly described as existing canned reports but not stated as a desired requirement target.

- **Sources:** evergreen_reference_2009.txt
- **Reason:** The document describes current availability of canned reports, not requirements for new/changed behavior.
- **Related requirements/evidence:** —
- **Human review required:** No

### BL-020: Interview duration, location, participants, and interviewer notes.

- **Sources:** interview_cataloging_2009-05-08.txt, interview_sysadmin_2009-05-10.txt
- **Reason:** Not software requirements.
- **Related requirements/evidence:** —
- **Human review required:** No

### BL-021: General purpose statement to gather requirements.

- **Sources:** interview_cataloging_2009-05-08.txt, interview_sysadmin_2009-05-10.txt
- **Reason:** Process/administrative statement, not a software requirement.
- **Related requirements/evidence:** —
- **Human review required:** No

### BL-022: Action items and meeting logistics (e.g., interviews due date, follow-up meeting date, subcommittee scheduling, agenda approval, minutes prepared/distributed).

- **Sources:** meeting_minutes/meeting_2009-03-15_minutes.txt
- **Reason:** These are process/administrative activities rather than software requirements.
- **Related requirements/evidence:** —
- **Human review required:** No

### BL-023: Working group mission and action items describing future activities (e.g., compile requirements document, create architecture section, next meeting agenda).

- **Sources:** meeting_minutes/meeting_2009-07-20_minutes.txt
- **Reason:** These are process/project management statements rather than atomic software requirements.
- **Related requirements/evidence:** —
- **Human review required:** No

### BL-024: Action item to research reporting warehouse options for historical data

- **Sources:** meeting_tech_subcommittee_2009-06-30.txt
- **Reason:** An action item is not itself a software requirement; only 'likely need' appears in requirements context.
- **Related requirements/evidence:** Support real-time vs historical reporting capability
- **Human review required:** No

### BL-025: Action item to compile technical requirements document

- **Sources:** meeting_tech_subcommittee_2009-06-30.txt
- **Reason:** Documentation/project management task, not a software requirement.
- **Related requirements/evidence:** —
- **Human review required:** No

### BL-026: Action item to draft architecture overview section

- **Sources:** meeting_tech_subcommittee_2009-06-30.txt
- **Reason:** Meeting deliverable, not a software requirement.
- **Related requirements/evidence:** —
- **Human review required:** No

### BL-027: Action item to review fine-grained requirements for technical feasibility

- **Sources:** meeting_tech_subcommittee_2009-06-30.txt
- **Reason:** Process step, not a software requirement.
- **Related requirements/evidence:** —
- **Human review required:** No

### BL-028: Follow-up technical meeting scheduled for August 15, 2009

- **Sources:** meeting_tech_subcommittee_2009-06-30.txt
- **Reason:** Scheduling detail, not a software requirement.
- **Related requirements/evidence:** —
- **Human review required:** No

### BL-029: Provide faster report execution during busy hours.

- **Sources:** survey_results_2009.txt
- **Reason:** The document reports a problem (“Reports take too long to run during busy hours”) but does not specify a measurable or testable requirement (e.g., time limits or throughput).
- **Related requirements/evidence:** —
- **Human review required:** No

### BL-030: Support visibility of whether a report is still processing.

- **Sources:** survey_results_2009.txt
- **Reason:** The document states “I can't see if my report is still processing” as an issue, but the requirements summary only explicitly supports queue visibility; without additional explicit confirmation, this is not separated as a distinct atomic requirement.
- **Related requirements/evidence:** ReportQueueVisibility
- **Human review required:** No

### BL-031: Support filtering by certain fields.

- **Sources:** survey_results_2009.txt
- **Reason:** The document says “Can't filter by some fields that should be available” but does not enumerate which fields or define expected behavior.
- **Related requirements/evidence:** —
- **Human review required:** No

### BL-032: Support exporting to Excel without duplicate rows.

- **Sources:** survey_results_2009.txt
- **Reason:** The document describes a specific problem (“export to Excel but the data has too many duplicate rows”) without defining the intended correctness rules or acceptance criteria.
- **Related requirements/evidence:** —
- **Human review required:** No

### BL-033: Ability to pull specific MARC fields when they are spread across multiple rows.

- **Sources:** survey_results_2009.txt
- **Reason:** The document describes a difficulty (“Need to pull specific MARC fields but they're spread across multiple rows”) but does not define the required output transformation or behavior.
- **Related requirements/evidence:** —
- **Human review required:** No

### BL-034: Include a set of transaction grouping filters (hour/terminal/branch/system) via the interface.

- **Sources:** survey_results_2009.txt
- **Reason:** Grouping dimensions are already captured as TransactionGroupingDimensions; additional UI/filter wording is not independently specified as testable requirements.
- **Related requirements/evidence:** TransactionGroupingDimensions
- **Human review required:** No

### BL-035: Transaction grouping by hour to identify busy periods.

- **Sources:** survey_results_2009.txt
- **Reason:** This is an explanatory use case for grouping by hour, which is already captured in TransactionGroupingDimensions; no separate requirement is stated.
- **Related requirements/evidence:** TransactionGroupingDimensions
- **Human review required:** No

## F. Source coverage and completeness

| Source document | Status | Requirement IDs | Coverage note |
|---|---|---|---|
| conversations/conv_pines014_material_volume.eml | loaded | REQ-001, REQ-002, REQ-003, REQ-004 | Extracted material volume report requirements from the explicit “Material Volume Report” summary and the earlier clarification about counting new acquisitions, checked-in, and checked-out items, category breakdowns, customizable categories, and date filters for historical point-in-time reporting. |
| conversations/conv_pines015_capacity_interface.eml | loaded | REQ-005, REQ-006, REQ-007, REQ-008, REQ-009 | Extracted system capacity interface requirements from the “SUMMARY: System capacity interface” section, including overview, drill-down, sorting/filtering, trends, and CSV export; excluded non-requirement suggestions like color-coding. |
| conversations/conv_pines016_shelf_space.eml | loaded | REQ-010, REQ-011, REQ-012, REQ-013, REQ-014, REQ-015, REQ-016 | All extracted requirements are derived directly from the shelf space report discussion, including core metrics (circulations/collection/shelf space), report scope (per library and per system), and requested filters/views (date range, comparison side-by-side). Estimation approach for shelf space is included with the explicit limitation that shelf space is not directly tracked. |
| conversations/conv_pines018_item_transfer.eml | loaded | REQ-018, REQ-019, REQ-020, REQ-021, REQ-022, REQ-023, REQ-024, REQ-025, REQ-026, REQ-027, REQ-028, REQ-029, REQ-030, REQ-031, REQ-032, REQ-033, REQ-034, REQ-035, REQ-036 | Mapped detailed feature requests and technical components (query/save/select/update/pull list/auto-revert/logging/performance/labels/alerts) into atomic requirements; preserved explicit examples where possible, and marked one event-based revert behavior as uncertain due to conflicting narrative.; CAND-000018 lacks source_documents in the candidate list; needs cross-origin coverage justification. |
| conversations/conv_pines019_020_missing_intransit.eml | loaded | REQ-037, REQ-038, REQ-039, REQ-040, REQ-041, REQ-042, REQ-043, REQ-044 | Captured explicit requirements for missing/damaged and in-transit reports (per branch/per system, merge transit-to/from, configurable X, sorting by due date, date ranges) plus some technical feasibility statements that could be interpreted as logic for report generation. |
| conversations/conv_pines021_item_purging.eml | loaded | REQ-045, REQ-046, REQ-047, REQ-048, REQ-049, REQ-050, REQ-051, REQ-052, REQ-053, REQ-054, REQ-055, REQ-056 | Captured explicit requirements for purging utilities: customizable combined criteria (status/time/activity), read-only candidate reports, confirmation, audit trail, batch status conversion, last copy report with system/library scope and flagging logic, and cleanup deletion of volume/copy/no-items records; also noted a schedulability request as lower confidence.; CAND-000056 and CAND-000058 cover DREQ-0053; discuss priority alignment. |
| conversations/conv_pines022_deletions.eml | loaded | REQ-057, REQ-058, REQ-059, REQ-060, REQ-061, REQ-062 | All consolidated deletion-tracking requirements were captured: audit logging fields, reporting interface, aggregation/administrative breakdowns, and denied deletion attempts. The source states Evergreen does not log deletions, but this was not turned into a requirement beyond the required logging behavior. |
| conversations/conv_pines023_patron_characteristics.eml | loaded | REQ-063, REQ-064, REQ-065, REQ-066, REQ-067 | All consolidated patron characteristics requirements were captured: supported characteristics, LIMIT/GROUP BY, AND/OR filter combination, configurable age ranges, and inclusion of nulls for missing optional data. |
| conversations/conv_pines024_inactive_patrons.eml | loaded | REQ-071, REQ-072, REQ-074, REQ-075, REQ-076, REQ-077 | Provides detailed examples and clarifications: definitions of electronic activity intent, the need to include mailing addresses, performance/implementation notes, and exclusion criteria examples. |
| early_draft_srs_galecia.txt | loaded | REQ-081, REQ-082, REQ-083, REQ-084, REQ-085, REQ-086, REQ-087, REQ-088, REQ-089, REQ-090, REQ-091, REQ-092, REQ-093, REQ-094, REQ-095, REQ-096, REQ-097, REQ-098, REQ-099, REQ-100, REQ-101, REQ-102, REQ-103, REQ-104, REQ-105, REQ-106, REQ-107, REQ-108, REQ-109, REQ-110, REQ-111, REQ-112, REQ-113, REQ-114, REQ-115, REQ-116, REQ-117, REQ-118, REQ-119, REQ-120, REQ-121, REQ-122, REQ-123, REQ-124, REQ-125, REQ-126, REQ-127, REQ-128, REQ-129, REQ-130, REQ-131, REQ-132, REQ-133, REQ-134, REQ-135, REQ-136, REQ-137, REQ-138, REQ-139, REQ-140, REQ-141, REQ-142, REQ-143, REQ-144, REQ-145, REQ-146, REQ-147, REQ-148, REQ-149 | Extracted atomic requirements from operating environment, design constraints, user documentation, and the visible portion of functional requirements (8.1-8.5) up to the truncation in the board reports section. No additional text beyond the provided excerpt was available.; Extracted all explicit system behavior statements using 'should'/'must' and 'ability to' phrasing, preserving configurable parameters (X, X days, X months) and explicit conditions (e.g., anonymization, merging transit-to/from, hold placement channels). Priorities were only inferred from explicit 'must' vs 'should' wording and report centrality; no explicit priority levels were provided in the sources.; Not extracted in this response; it contains extensive fine-grained reporting interface requirements but was not included in the extracted set. |
| email_financial_reports.eml | loaded | REQ-147, REQ-148, REQ-149, REQ-150, REQ-151, REQ-152, REQ-153, REQ-154, REQ-155 | Extracted financial reporting, audit trail, compliance, retention, data-join, threshold query, immediacy, and per-library payment tracking requirements explicitly stated across the thread. |
| email_report_features.eml | loaded | REQ-156, REQ-157, REQ-158, REQ-159, REQ-160, REQ-161, REQ-162, REQ-163, REQ-165, REQ-166, REQ-167, REQ-168, REQ-174, REQ-175 | All explicitly enumerated report/query/template/permission/board/report-queue/transaction-archive items were captured; “priority reports can jump queue” was included as a queue business rule. |
| email_staff_login.eml | loaded | REQ-164, REQ-165, REQ-169, REQ-170, REQ-171, REQ-172, REQ-173 | Captured both streamlined (optional) and traditional login support, audit/individual authentication constraints, and role/security-group based permission determination and administration. Staff-type capability examples were treated as a lower-confidence role-capability requirement. |
| evergreen_reference_2009.txt | loaded | REQ-176, REQ-177, REQ-178, REQ-179, REQ-180, REQ-181, REQ-182, REQ-183, REQ-184, REQ-185, REQ-186, REQ-187, REQ-188, REQ-189, REQ-190, REQ-191, REQ-192, REQ-193, REQ-194, REQ-195, REQ-196, REQ-197, REQ-198, REQ-199, REQ-200, REQ-201, REQ-202, REQ-203, REQ-204, REQ-205, REQ-206, REQ-207, REQ-208, REQ-209, REQ-210, REQ-211, REQ-212, REQ-213, REQ-215, REQ-216, REQ-217, REQ-218, REQ-219, REQ-220 | Most statements are extracted from explicit capability lists (e.g., report writer features) and explicit limitations/gaps phrased as missing features or 'does not exist'. Some extracted constraints about scheduling options are marked as estimated because the document both states some scheduling exists and separately lists lack of certain schedule options. |
| interview_cataloging_2009-05-08.txt | loaded | REQ-234, REQ-235, REQ-236, REQ-237, REQ-238, REQ-239, REQ-240, REQ-241, REQ-242, REQ-243, REQ-244, REQ-245, REQ-246, REQ-247, REQ-248, REQ-249, REQ-250, REQ-251, REQ-252, REQ-253, REQ-254, REQ-255, REQ-256, REQ-257 | Requirements were traced to this document. |
| interview_sysadmin_2009-05-10.txt | loaded | REQ-214, REQ-221, REQ-222, REQ-223, REQ-224, REQ-225, REQ-226, REQ-227, REQ-228, REQ-229, REQ-230, REQ-231, REQ-232, REQ-233 | Requirements were traced to this document. |
| meeting_minutes/meeting_2009-03-15_minutes.txt | loaded | REQ-258, REQ-259, REQ-260, REQ-261, REQ-262, REQ-263, REQ-264, REQ-265, REQ-266, REQ-267, REQ-268, REQ-269 | Requirements extracted were limited to explicit mission/scope/approach statements that could be translated into system/software requirements. Administrative next steps and meeting details were not converted into requirements. |
| meeting_minutes/meeting_2009-07-20_minutes.txt | loaded | REQ-270, REQ-271, REQ-272, REQ-273, REQ-274, REQ-275, REQ-276, REQ-277, REQ-278, REQ-279, REQ-280, REQ-281, REQ-282, REQ-283, REQ-284 | Extracted explicit 'shall' requirements from Operating Environment Requirements, Design and Implementation Constraints, and User Documentation Requirements sections. Interpreted discussion text only when it reinforced the stated requirement (e.g., background processing/queuing, Section 508, export/import). Action items and mission statements were omitted as non-requirement. |
| meeting_tech_subcommittee_2009-06-30.txt | loaded | REQ-285, REQ-286, REQ-287, REQ-288, REQ-289, REQ-290, REQ-291, REQ-292, REQ-293, REQ-294, REQ-295, REQ-296, REQ-297, REQ-298, REQ-299, REQ-300, REQ-301, REQ-302, REQ-303, REQ-304, REQ-305, REQ-306, REQ-307, REQ-308, REQ-309, REQ-310, REQ-311, REQ-312, REQ-313, REQ-314, REQ-315, REQ-316 | Extracted explicit 'must/shall' requirements and requirement-like constraints/dependencies labeled AS/DE where they state system behavior or structural constraints. Included one low-confidence candidate where language was probabilistic ('probably'). |
| survey_results_2009.txt | loaded | REQ-311, REQ-317, REQ-318, REQ-319, REQ-320, REQ-321, REQ-322, REQ-323, REQ-324, REQ-325, REQ-326, REQ-327, REQ-328, REQ-329, REQ-330, REQ-331, REQ-332, REQ-333, REQ-334, REQ-335, REQ-336, REQ-337, REQ-338, REQ-339, REQ-340, REQ-341, REQ-342, REQ-343, REQ-344, REQ-345, REQ-346 | Extracted only explicit, evidence-supported capabilities/constraints from the survey findings and the 'SUMMARY OF KEY REQUIREMENTS IDENTIFIED' section; did not convert problem statements into requirements without testable/explicit behavior or constraints. |

### Processing warnings

_No corpus loading warnings._
- **Validation warning:** Requirement candidate 17: One or more candidate source references could not be reliably mapped to an input document.
- **Validation warning:** Requirement candidate 17 has no reliably mapped source document; manual review is required.
- **Validation warning:** Requirement candidate 18: One or more candidate source references could not be reliably mapped to an input document.
- **Validation warning:** Requirement candidate 19: One or more candidate source references could not be reliably mapped to an input document.
- **Validation warning:** Requirement candidate 20: One or more candidate source references could not be reliably mapped to an input document.
- **Validation warning:** Requirement candidate 21: One or more candidate source references could not be reliably mapped to an input document.
- **Validation warning:** Requirement candidate 22: One or more candidate source references could not be reliably mapped to an input document.
- **Validation warning:** Requirement candidate 24: One or more candidate source references could not be reliably mapped to an input document.
- **Validation warning:** Requirement candidate 30: One or more candidate source references could not be reliably mapped to an input document.
- **Validation warning:** Requirement candidate 31: One or more candidate source references could not be reliably mapped to an input document.
- **Validation warning:** Requirement candidate 32: One or more candidate source references could not be reliably mapped to an input document.
- **Validation warning:** Requirement candidate 33: One or more candidate source references could not be reliably mapped to an input document.
- **Validation warning:** Requirement candidate 34: One or more candidate source references could not be reliably mapped to an input document.
- **Validation warning:** Requirement candidate 68: One or more candidate source references could not be reliably mapped to an input document.
- **Validation warning:** Requirement candidate 68 has no reliably mapped source document; manual review is required.
- **Validation warning:** Requirement candidate 69: One or more candidate source references could not be reliably mapped to an input document.
- **Validation warning:** Requirement candidate 69 has no reliably mapped source document; manual review is required.
- **Validation warning:** Requirement candidate 70: One or more candidate source references could not be reliably mapped to an input document.
- **Validation warning:** Requirement candidate 70 has no reliably mapped source document; manual review is required.
- **Validation warning:** Requirement candidate 71: One or more candidate source references could not be reliably mapped to an input document.
- **Validation warning:** Requirement candidate 72: One or more candidate source references could not be reliably mapped to an input document.
- **Validation warning:** Requirement candidate 73: One or more candidate source references could not be reliably mapped to an input document.
- **Validation warning:** Requirement candidate 73 has no reliably mapped source document; manual review is required.
- **Validation warning:** Requirement candidate 74: One or more candidate source references could not be reliably mapped to an input document.
- **Validation warning:** Requirement candidate 75: One or more candidate source references could not be reliably mapped to an input document.
- **Validation warning:** Requirement candidate 77: One or more candidate source references could not be reliably mapped to an input document.
- **Validation warning:** Requirement candidate 78: One or more candidate source references could not be reliably mapped to an input document.
- **Validation warning:** Requirement candidate 78 has no reliably mapped source document; manual review is required.
- **Validation warning:** Requirement candidate 79: One or more candidate source references could not be reliably mapped to an input document.
- **Validation warning:** Requirement candidate 79 has no reliably mapped source document; manual review is required.
- **Validation warning:** Requirement candidate 80: One or more candidate source references could not be reliably mapped to an input document.
- **Validation warning:** Requirement candidate 80 has no reliably mapped source document; manual review is required.
- **Validation warning:** Rejected candidate 4: One or more candidate source references could not be reliably mapped to an input document.
- **Review finding:** Evidence insufficiency for candidate CAND-000018 (Item transfer batch utility).
- **Review finding:** Conflicting auto-revert policy: CAND-000029 describes event-based revert when items are checked out at destination; conflicting with DREQ-0026's intent.
- **Review finding:** Priority mismatch/ambiguity between last-copy reporting (CAND-000056/000058) and related flagging (CAND-000059).
- **Review finding:** Evidence for activity-report requirement CAND-000111 truncated; insufficient to determine exact expected metrics.

## G. Unresolved questions

- CAND-000029 contains conflicting/uncertain intent about checkout behavior at the destination: should items that are checked out at the destination be exempt from auto-reversion ("they should stay"), or should a checkout event trigger a revert? Please clarify the desired policy for items checked out at the destination during the transfer period (e.g., checked-out items are exempt from revert vs. checked-out items still revert when other criteria are met).
- Priority mismatch: the last-copy report availability is marked P1 (CAND-000056, CAND-000058) while the specific logic to check-and-flag items that are the only copy in the scope is marked P2 (CAND-000059). Should the check-and-flag behavior be elevated to P1 to match the criticality of the last-copy report (avoid accidental consortium-level deletions), or is it intentionally lower priority/implementation detail?
- CAND-000111: Source evidence for the activity-report requirement is truncated ("displaying"). What specific traffic/volume metrics and display fields are required for activity reports?
- CAND-000113,CAND-000120: The draft requires archived transactions to both 'protect patron privacy' and to 'provide useful demographic statistics' via anonymization. Clarify whether (a) the system must retain raw (identifying) transaction data in any form and apply anonymization only to reporting extracts, (b) the system must permanently delete identifying fields and only store anonymized archives, or (c) another archival policy is required to comply with State law and reporting needs.
- Q1: The transaction-archive requirement refers to retaining transaction data for 'X years' per state law. What is the required retention period (value of X)? If retention varies by data type or jurisdiction, provide the retention period(s) and any distinctions (for example: full transaction records retained for N years, personally identifiable elements removed after M years).
- Q1: Conflict between reporting background-processing statements: CAND-000226 ("System shall not provide background processing for long-running reports") versus CAND-000236 ("System shall process complex report searches in the background (queued) or via read-only replicas..."). Which statement reflects the intended/required system behavior and which documents an existing limitation? Clarify whether background/queued processing is a required capability (high priority) or explicitly out-of-scope.
- Q2: Conflict between accessibility statements: CAND-000231 (Evergreen: "System shall not provide accessibility support for the report interface") versus CAND-000239/CAND-000240 (Sysadmin: Section 508 compliance and support for JAWS/NVDA/ZoomText). Which is authoritative for the delivered system: the documented Evergreen limitation or the legal/non-negotiable accessibility requirement stated by the sysadmin? If the latter is authoritative, Evergreen's documentation must be considered an implementation gap to address.
- Q1: The Role-based access control requirement (CAND-000312) is prioritized P1, while the specific admin-role candidates Global Admin (CAND-000314) and Local Admin (CAND-000315) are P2 (estimated). Should the specific admin-role requirements be elevated to P1 to match the RBAC priority, or is the priority difference intentional?
- Q2: The 'Work with the relational structure; avoid denormalization for reporting' item (CAND-000306) is worded as a strong recommendation and currently recorded as P2 (estimated). Should this be enforced as a hard constraint (P1) on implementations, or remain advisory (P2)?
- CAND-000332 (priority P1, technical-subcommittee) and CAND-000343 (priority P2, survey) state the same requirement for supported output formats (Excel, CSV, HTML) but have differing priorities. Which priority should be authoritative for this requirement (P1 or P2)?
- Q1: CAND-000029 conflict about auto-revert at destination – clarify policy.
- Q2: Priority alignment between last-copy candidates (056/058) and related candidate (059).
- Q3: Evidence completeness for activity-report requirement (CAND-000111) – provide full source.
- Po globálnej kontrole zostávajú možné sémantické duplicity na ľudské posúdenie.
- Requirement candidate 17: One or more candidate source references could not be reliably mapped to an input document.
- Requirement candidate 18: One or more candidate source references could not be reliably mapped to an input document.
- Requirement candidate 19: One or more candidate source references could not be reliably mapped to an input document.
- Requirement candidate 20: One or more candidate source references could not be reliably mapped to an input document.
- Requirement candidate 21: One or more candidate source references could not be reliably mapped to an input document.
- Requirement candidate 22: One or more candidate source references could not be reliably mapped to an input document.
- Requirement candidate 24: One or more candidate source references could not be reliably mapped to an input document.
- Requirement candidate 30: One or more candidate source references could not be reliably mapped to an input document.
- Requirement candidate 31: One or more candidate source references could not be reliably mapped to an input document.
- Requirement candidate 32: One or more candidate source references could not be reliably mapped to an input document.
- Requirement candidate 33: One or more candidate source references could not be reliably mapped to an input document.
- Requirement candidate 34: One or more candidate source references could not be reliably mapped to an input document.
- Requirement candidate 68: One or more candidate source references could not be reliably mapped to an input document.
- Requirement candidate 69: One or more candidate source references could not be reliably mapped to an input document.
- Requirement candidate 70: One or more candidate source references could not be reliably mapped to an input document.
- Requirement candidate 71: One or more candidate source references could not be reliably mapped to an input document.
- Requirement candidate 72: One or more candidate source references could not be reliably mapped to an input document.
- Requirement candidate 73: One or more candidate source references could not be reliably mapped to an input document.
- Requirement candidate 74: One or more candidate source references could not be reliably mapped to an input document.
- Requirement candidate 75: One or more candidate source references could not be reliably mapped to an input document.
- Requirement candidate 77: One or more candidate source references could not be reliably mapped to an input document.
- Requirement candidate 78: One or more candidate source references could not be reliably mapped to an input document.
- Requirement candidate 79: One or more candidate source references could not be reliably mapped to an input document.
- Requirement candidate 80: One or more candidate source references could not be reliably mapped to an input document.
- Rejected candidate 4: One or more candidate source references could not be reliably mapped to an input document.
- Evidence insufficiency for candidate CAND-000018 (Item transfer batch utility).
- Conflicting auto-revert policy: CAND-000029 describes event-based revert when items are checked out at destination; conflicting with DREQ-0026's intent.
- Priority mismatch/ambiguity between last-copy reporting (CAND-000056/000058) and related flagging (CAND-000059).
- Evidence for activity-report requirement CAND-000111 truncated; insufficient to determine exact expected metrics.

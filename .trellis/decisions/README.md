# Cross-Task Decisions

Keep durable engineering choices here when they affect later tasks and their tradeoffs are worth reusing. Ordinary implementation details belong in a task's `design.md`; research evidence belongs in `research/`; current engineering contracts belong in `spec/`. Link to the detailed reasoning instead of copying it across these locations. Not every task needs a decision record.

## Record Format

Each decision is one `.trellis/decisions/<id>.md` file. The filename stem is its stable ID: a single path segment, excluding `.`, `..` and the reserved name `README` (case-insensitive). IDs must not collide after case folding. Keep files flat; file symlinks must resolve inside the actual decisions directory. A shared `.trellis` directory remains supported.

The first nonblank line is a level-one title. Immediately follow it with a JSON fence, allowing only blank lines between them. This is the record's sole metadata block; all three fields below are required, and extra or duplicate keys are errors.

````markdown
# A cross-task engineering choice

```json
{
  "status": "proposed",
  "source_task": "10-10-decision-record-boundaries",
  "reconsiders": null
}
```

## Context
Describe the engineering problem, impact and constraints.

## Options Considered
List alternatives and their tradeoffs, including reasons for rejection.

## Decision
State the proposed or confirmed conclusion and its reasons.

## Applicability
State the conditions under which this conclusion applies and what changes warrant reconsideration.
````

This is a template, not an adopted production decision.

| Field | Contract |
| --- | --- |
| `status` | Exactly `proposed`, `accepted` or `rejected`; a conclusion, not delivery progress |
| `source_task` | Full task directory name, not a short slug or a path |
| `reconsiders` | `null`, or the exact filename ID of another finalized record |

Each required level-two section must appear exactly once and contain nonblank content beyond headings, HTML comments and fence markers. Headings inside code fences do not create sections. Unclosed fences or comments are errors. Body language is unrestricted; machine heading names stay in English.

## Find and Associate Decisions

During planning:

1. Search filenames and record bodies here for relevant engineering choices. Read both the original record and its reconsideration successors before deciding which conclusion is effective.
2. Register every decision used or created by the task in its existing `task.json.relatedFiles` array. Preserve other entries. For example:

   ```json
   {"relatedFiles": [".trellis/decisions/example-choice.md"]}
   ```

3. Reference the decision from task design or relevant specs rather than copying its complete argument. A prose link alone does not create a machine association.
4. If there is no relevant cross-task decision, keep the task's ordinary design local; do not invent a record merely to satisfy validation.

The validator follows registered roots and their predecessor/successor links, including accepted successors of an old record. It rejects related structural errors, missing references, case-folded ID collisions, self-reference, cycles and multiple accepted direct successors. Metadata errors in unrelated files produce warnings only. Unparseable metadata may hide unknown links: a warning is not evidence that every association was checked. With no registered decision roots, decision scanning is skipped.

Source lookup matches the exact directory name in `tasks/<name>` and `tasks/archive/*/<name>`. Exactly one matching task with readable, matching `task.json` identity is required. Moving a source task into the archive does not require updating a decision's `source_task`; archived planning documents are not revalidated.

## Conclusions and Reconsideration

- A proposal becomes `accepted` or `rejected` only after the user's decision. An accepted design is not necessarily implemented; the source task tracks delivery.
- Do not overwrite a finalized record's conclusion or its historical reasons. When conditions change, create a new record whose `reconsiders` points to the finalized predecessor, and add a nonempty `## Reconsideration` section describing the changed conditions or new evidence.
- A proposed or rejected reconsideration does not replace the previous conclusion. Only an accepted successor supersedes it. Keep the predecessor's original status; do not add reciprocal links or a second replacement-status field.
- To reconsider further, follow the effective chain to its latest accepted successor. Rejected attempts do not automatically become the effective conclusion. A prior rejection can be reevaluated when its conditions change.
- Replacement is derived from links and conclusions, not from an implementation/archival status or a cache index.

## Structural Checks and Limits

This repository enables `task_structure_validation: true` in `.trellis/config.yaml`. See [workflow.md](../workflow.md) for classification and planning sections. Complex tasks default to the original three-document contract; explicit `meta.planning_layout: compact` selects PRD plus design (Scope, Contracts, Ordered Steps, Validation), retaining full checks for any existing optional `implement.md`. Lightweight remains PRD-only; unknown layouts and lightweight/compact are errors. Neither missing files nor a Pi session selects compact implicitly. Existing/new unarchived tasks follow their declared layout at next start/archive; do not bulk-rewrite history. This changes planning materials, not decision lifecycles or reference checks.

`task.py start` and `task.py archive` reject structural errors before mutating task, session, parent/child, directory or Git state. `task.py validate` reports these errors together with the existing JSONL checks. Existing context/branch skip options do not bypass structure checks. Creating/editing tasks, setting metadata and `finish` remain available to repair materials. When invoking scripts, use `python` on Windows and `python3` on macOS/Linux.

A missing configuration file, an absent setting or explicit `false` disables these checks silently. Only an explicit, unquoted top-level `true`/`false` scalar is recognized; this validator does not interpret YAML flow documents or merges, and leaves unrelated entries to the existing configuration reader. Broken configuration symlinks, unreadable files and invalid or duplicate declarations of this setting remain errors. This switch is a project workflow choice, not a security boundary.

Structure checks cannot establish that a task's declared complexity is appropriate, its reasoning is sound, the user approved it, all relevant decisions were registered, or historical prose was preserved. Use user review and Git history for those facts. Passing structural checks does not prove implementation or runtime correctness.

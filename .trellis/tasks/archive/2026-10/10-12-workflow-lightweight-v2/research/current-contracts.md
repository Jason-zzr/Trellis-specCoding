# Current Contracts and Planning Evidence

## Scope and Baseline

- This is planning for the local repository + Pi pilot. V1 is already committed and archived; do not redo its routing, approval-reuse or check-reuse changes.
- The user agreed to reduce required materials while retaining decision lifecycles and deterministic validation. This does not approve the implementation details below.
- No formal decision entries currently exist in `.trellis/decisions/`; only its README is present. There is no prior accepted/rejected record to supersede.

## JSONL Readiness

- `.trellis/scripts/task.py:172-225`: `cmd_start` runs `validate_task_structure` before mutation. Separately, it rejects an existing empty `implement.jsonl` or `check.jsonl`, unless `--allow-empty-context` is supplied.
- `.trellis/scripts/common/task_context.py:129-156`: `curated_entry_count` returns `None` for absent manifests and zero for empty/unreadable ones. The existing start flag only bypasses the empty-context readiness check; it does not bypass structure validation.
- `.trellis/scripts/common/task_store.py:579-592`: creation currently seeds empty manifests when any supported subagent platform directory exists. It does not identify the task's actual execution route. Removing Pi from that platform list would not solve this multi-platform repository's behavior and would remove legitimate delegation support.
- `.trellis/scripts/common/task_context.py:158-206,271-291`: `task.py validate` validates present JSONL and skips absent files. `_example` scaffold rows are errors. Current task creation writes empty files, not those older scaffold rows.
- `.trellis/workflow.md:432-500`: Pi is still instructed to curate both manifests before start. Some text also incorrectly describes the current seed as `_example` and its removal as optional. Correct these statements only in the Pi-specific path in this pilot; do not silently relax other platforms.

## Actual Pi Consumption

- `.pi/extensions/trellis/index.ts:89-94`: implement/check roles map to their corresponding manifest.
- `readJsonlEntries` at `:946-967` returns an empty list for absent/empty input and ignores parse failures.
- `buildContext` at `:1183-1239` materializes curated files, skips directory entries, then includes PRD and optional design/implementation documents.
- `trellis_subagent.execute` at `:1879-1940` calls `runSubagent`. The later implementation must reject invalid/missing role context before any child process starts, in single, parallel and chain modes. Session overview and unrelated custom roles must not require implement/check manifests.
- Native/community delegation remains subject to the existing dispatch protocol. This pilot can enforce the project tool's boundary; it must not claim to intercept arbitrary external subagent tools.

## Planning Documents

- `.trellis/scripts/common/task_validation.py:35-39,409-443`: the validator recognizes `meta.planning_mode` as lightweight/complex, requires all three documents for complex tasks, and checks any optional documents already present.
- This validator is shared by `start`, `validate` and `archive`. Changing the unconditional complex rule would affect tasks created through other platforms.
- Existing script graph navigation confirms those three callers and the separate start-to-curated-entry-count edge. Current source, not graph freshness, is the contract authority.
- The validator is already opt-in through `task_structure_validation`; absent/disabled configuration must remain silent and must not validate new metadata.

## Proposed Boundary

- Reuse the existing main-session start flag instead of adding a dispatcher mode or CLI option. Leave automatically created empty manifests alone; saving maintenance work does not require deleting harmless scaffold files.
- Propose one explicit task metadata field, `meta.planning_layout` (`standard` / `compact`, omitted means standard), to select the compact document contract without changing task risk classification or other tasks' defaults. This field is proposed, not implemented or approved.
- Only local Pi instructions choose compact layout. Shared Python scripts understand explicitly marked tasks; their mirrored templates must remain byte-identical. Template synchronization is a proposed scope exception, not permission to alter init/update or distribute Pi workflow/extension defaults.

## Validation Boundary

Only static planning checks are authorized in this turn. No validator execution, real delegation, tests, build, installation, Git commit or push is part of this planning delivery.

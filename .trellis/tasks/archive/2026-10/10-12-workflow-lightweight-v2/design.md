# V2 Design: On-Demand Planning Materials

Status: approved by the user's explicit confirmation of the complete plan, including the task-layout field, both direct Python template mirrors and the repository Pi delegation boundary. Repository-only implementation with one static check; no runtime validation or Git operations.

## Scope

Keep the local repository + Pi pilot. Remove advance JSONL curation for main-session work, and allow a compact design/execution document for suitable complex tasks. Preserve V1, decision lifecycles, state-transition checks, explicit implementation approval and current finish-work behavior.

| Proposed file | Change boundary |
| --- | --- |
| `.trellis/workflow.md` | Pi-only material rules in the overview, planning/execution breadcrumbs and steps 1.1/1.3/1.4/1.5; retain marker pairs, numbering and non-Pi defaults |
| `.pi/prompts/trellis-start.md` | Select materials by the existing risk classification and proposed layout; use the existing empty-context flag for approved main-session work |
| `.pi/prompts/trellis-continue.md` | Recover the persisted layout and actual delegation need; do not request absent optional files or repeat approval |
| `.pi/skills/trellis-brainstorm/SKILL.md` | Produce only required materials; prepare a role manifest when delegation is actually selected |
| `.pi/skills/trellis-before-dev/SKILL.md` | Main session reads task documents and relevant specs directly; JSONL is not an inline prerequisite |
| `.pi/skills/trellis-check/SKILL.md` | Read the selected layout, retain full-scope evidence/acceptance requirements and once-only spec judgment |
| `.pi/extensions/trellis/index.ts` | Before a project implement/check subagent starts, require valid role context; do not change session overview or general custom roles |
| `.trellis/scripts/common/task_validation.py` | Add an explicitly opted-in compact document contract; retain disabled behavior and all decision checks |
| `packages/cli/src/templates/trellis/scripts/common/task_validation.py` | Exact mirror of that shared script; no new template registry entry |
| `.trellis/scripts/common/task_store.py` | Update `cmd_create` planning hints to reflect the declared layout and actual empty JSONL seed behavior; keep creation/state/seed mechanics unchanged |
| `packages/cli/src/templates/trellis/scripts/common/task_store.py` | Exact mirror of the hint change |
| `.trellis/scripts/task.py` and `packages/cli/src/templates/trellis/scripts/task.py` | Review-fix follow-up: expose the existing `--allow-empty-context` option on `validate`; keep default validation strict |
| `.trellis/scripts/common/task_context.py` and `packages/cli/src/templates/trellis/scripts/common/task_context.py` | Review-fix follow-up: skip only the zero-entry readiness error when requested; preserve all structure, row and reference checks |
| `.trellis/decisions/README.md` | Align its planning-document contract reference; do not change decision metadata or lifecycle |
| `.trellis/spec/cli/backend/script-conventions.md` | Document the new layout contract, opt-in behavior and mirror requirement |

Task planning/implementation records are maintained in this task directory. Shared start/continue skills already redirect Pi to project Pi prompts and need no planned changes. Do not modify non-Pi platform files, public workflow/Pi extension templates, init/update logic, global installations, tests, CI, graph outputs, task states or finish-work policy.

## Contracts

### Task layout: one explicit declaration, no environment inference

Retain `meta.planning_mode: lightweight | complex`. Propose optional `meta.planning_layout: standard | compact`; absence means `standard`. This is a document layout, not a new task status, risk level, workflow version or execution engine. Use existing `create --meta` / `set-meta`; do not add CLI flags or config switches.

When `task_structure_validation` is enabled:

| Classification / layout | Required documents and exact level-two sections |
| --- | --- |
| lightweight / omitted or standard | `prd.md`: Goal, Requirements, Acceptance Criteria; existing optional documents retain their current checks |
| complex / omitted or standard | Current PRD + design + implement contract, unchanged |
| complex / compact | `prd.md`: Goal, Requirements, Acceptance Criteria; `design.md`: Scope, Contracts, Ordered Steps, Validation |

Compact `design.md` holds scope, the necessary solution/contracts/tradeoffs, ordered execution with dependencies and applicable rollback handling, and acceptance/validation boundaries. Do not demand unrelated interface/data-flow/rollout boilerplate. Structural checks prove these sections exist and contain content, not that the reasoning is sound.

If a compact task already has `implement.md`, preserve it and validate its existing section contract; do not delete it to make validation pass. Do not duplicate its execution plan: the compact Ordered Steps section may reference that plan. If independently maintained batches, complex dependencies or a handoff warrant a separate execution plan, select the standard layout instead of mechanically generating both forms.

A present layout value other than the two declared strings is an error. `compact` with `lightweight` is an error with a repair hint: keep lightweight PRD-only, or classify genuinely complex work correctly. No field is required on old tasks. When structure validation is disabled or the config is absent, do not introduce new metadata warnings/errors.

Only the local Pi planning instructions select compact for new applicable work; other platforms and unmarked tasks keep their defaults. Persisting the choice avoids start/archive outcomes depending on which terminal executes Python. Existing tasks are not migrated in bulk.

### Inline JSONL path

For approved Pi main-session implementation, skip advance curation and use:

```bash
python3 ./.trellis/scripts/task.py start <task-dir> --allow-empty-context
```

The existing structure check still runs before mutation. Do not use this flag to authorize implementation, bypass required documents, excuse failed acceptance checks or announce readiness for delegation.

Leave automatically generated empty manifests untouched; neither fill nor delete them just for housekeeping. Existing useful manifests remain available. Existing malformed manifests remain errors when explicitly validated; do not silently remove them. Do not change `cmd_start`, `_has_subagent_platform`, default JSONL semantics or task-creation seed mechanics for this optimization.

### Real delegation

Before choosing a project implement/check delegate, curate only its required role manifest with real spec/research references. Retain the Active task prefix and the existing permission/authorization constraints; this work does not authorize routine review subagents.

In the repository Pi extension, reuse existing role mapping, task resolution, JSONL reading, file materialization and error reporting:

1. Resolve the active task and requested role before spawning. With no task, report a repairable tool error.
2. Reuse `task.py validate <task-dir> --allow-empty-context` for task/JSONL structure and reference diagnostics; use its exit status, not message matching. This explicit option skips only the zero-entry readiness error, leaving existing malformed rows and broken references as errors in either manifest. Default `validate` remains strict; failure to run validation is not success.
3. Require at least one real, readable, materializable file reference in that role's manifest. A missing/empty file, scaffold-only rows, malformed JSON, broken references, directory-only input or zero usable file context must not silently launch a child.
4. Check the exact role manifest, without demanding that the unused role's manifest be nonempty. Preserve generic validation errors for malformed files that already exist.
5. Fail before any child starts in single/parallel/chain modes; use the existing structured tool-error path. Do not modify `buildContext` globally in a way that blocks SessionStart or custom agents without a mapped manifest.

The parent still checks prerequisites for native/community tools; no new interception of external subagent implementations is proposed. Runtime enforcement is limited to the project `trellis_subagent` tool, which is the local Trellis workflow delegation entry.

### Checks and decisions

`start / validate / archive` keep using the same structural validator and keep failing before state changes. Keep decision status, stable IDs, references, reconsideration links and archived source resolution unchanged. Do not require a decision record for every task. Keep the V1 finish condition: implementation complete, valid full-scope evidence satisfies acceptance, and no unresolved blocking failures.

## Data Flow

Pi request → existing task triage and classification → select standard/compact materials → review and implementation approval → start with existing inline context exception → direct spec/document loading → main-session work.

If delegation becomes necessary: curate the selected role manifest → project tool validates task/references and usable context → spawn delegate, or return a diagnostic without spawning. No task restart or second approval is required solely because a manifest is prepared; a material scope/risk change still needs confirmation.

On resume/archive, read the persisted document layout and validate the same selected contract. JSONL preparation and planning-document completeness are separate concerns; neither substitutes for the other.

## Tradeoffs

- One new task metadata field is proposed because globally relaxing the complex validator would affect non-Pi/unmarked tasks, while deriving layout from missing files would turn omissions into permission. Using the current process environment would make archive/resume unstable. The field adds one automatically managed value, not another user questionnaire.
- Compact reduces both a separately maintained file and mandatory headings (design+implement currently have nine; compact design has four). It does not remove the requirement to record important technical reasoning or necessary execution/rollback arrangements.
- Empty seed files may remain. The benefit is removing mandatory curation/maintenance, not promising a zero-JSONL directory or adding a cleanup/migration system.
- The existing inline flag avoids a new dispatch mode. Because it bypasses start's context count, the real project delegation boundary must enforce its own readiness before spawn.
- Shared Python template mirrors must change with their local scripts. Only explicitly marked, structure-validation-enabled tasks select compact; no public workflow/default rollout is included. This narrow template exception requires plan approval.
- Other platforms' default instructions remain unchanged. This is not a claim that their conversational routes have been adapted to compact tasks or that arbitrary external tools are intercepted.

## Rollout and Rollback

This task itself remains complex/standard while V2 is unimplemented: retain the existing three planning documents and curated manifests. Do not use a proposed rule to approve its own implementation.

After this complete plan is approved, activate the task under the current rules, implement the coherent file set, and perform one scoped static check. No real delegation, validator scenario run, tests, build, installation, submission, push or archive is pre-authorized. Runtime behavior must remain explicitly unverified until separately authorized.

If reverting after compact tasks have been created, first retain their content and restore any documents needed by standard validation before removing the new layout support. Revert the corresponding Python mirrors together. Never reset unrelated work, bulk rewrite task history, modify the user's installed Pi configuration or claim a repository extension edit has updated a global installation.

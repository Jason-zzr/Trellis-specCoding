# V2 Implementation Plan

Status: approved for repository-only implementation by the user's explicit confirmation of this complete plan. Runtime validation and Git operations are not authorized.

Goal: reduce advance JSONL maintenance and compulsory document scaffolding in the local Pi pilot without weakening decision checks or task-state safety.

Architecture: reuse the existing inline start flag; select compact materials through one explicit task metadata field; enforce actual project delegation readiness where children are launched. Preserve default layouts and shared-script mirrors.

Tech stack: Markdown workflow/skills, Python task scripts, repository-local TypeScript Pi extension. No new dependencies, tests, workflow engine or global configuration.

## Ordered Steps

### 1. Confirm scope and activate under existing rules

- [x] Obtain one approval covering this design, the proposed `meta.planning_layout` field, both direct Python template mirrors and the repository Pi extension.
- [x] Reuse recoverable approval thereafter; do not reconfirm unchanged decisions.
- [x] Read the applicable existing specs and Pi extension API documentation before code changes; resolve only implementation-critical gaps.
- [x] Confirm changed paths resolve inside the repository and retain the current working-tree baseline.
- [x] Run the existing `task.py start` for this task only after review. Keep this task's current standard three-document layout and curated JSONL, rather than relying on the feature being built.

### 2. Implement the explicitly selected material contract

Files: `.trellis/scripts/common/task_validation.py` and its exact mirror `packages/cli/src/templates/trellis/scripts/common/task_validation.py`.

- [x] Keep the `_enabled` boundary, existing issue type, markdown parser, ordering and decision validation.
- [x] Read `planning_layout` only inside enabled validation; omitted/standard retains the current path.
- [x] Reject unsupported layout values and lightweight/compact mismatches with existing diagnostic conventions.
- [x] For complex/compact, require PRD plus compact design sections (Scope, Contracts, Ordered Steps, Validation). Missing `implement.md` is allowed; an existing optional implementation document remains checked.
- [x] Do not infer risk/layout from file absence, a `.pi` directory or session environment. Do not alter start/archive mutation order or add another validator.
- [x] Synchronize the script mirror byte-for-byte in the same change set.

Files: `.trellis/scripts/common/task_store.py` and `packages/cli/src/templates/trellis/scripts/common/task_store.py`.

- [x] Align creation hints with the explicit layout; keep JSONL creation and default platform behavior unchanged.
- [x] Synchronize the hint-only script mirror byte-for-byte. No new file registration is needed.

### 3. Protect real project delegation before relaxing inline preparation

File: `.pi/extensions/trellis/index.ts`.

- [x] Locate the shared pre-spawn path for single/parallel/chain; preserve existing key resolution, cancellation, error/result handling and child permissions.
- [x] For mapped implement/check roles only, require an active task, successful task/context validation with `--allow-empty-context` (structure and references still checked), and at least one usable file reference in the selected manifest.
- [x] Reuse existing parsing/materialization where possible; reject malformed/scaffold-only/missing/broken/empty context before any child starts. Do not impose a nonempty requirement on the other role.
- [x] Keep SessionStart context assembly and unmapped custom roles working without those manifests.
- [x] Make missing validator/runtime or validation failure a visible tool error, not silent continuation. Do not add a global hook or change installed packages.

### 4. Align only local Pi guidance

Files: `.trellis/workflow.md`, `.pi/prompts/trellis-start.md`, `.pi/prompts/trellis-continue.md`, `.pi/skills/trellis-brainstorm/SKILL.md`, `.pi/skills/trellis-before-dev/SKILL.md`, `.pi/skills/trellis-check/SKILL.md`.

- [x] Align all Pi overview, breadcrumb, phase and prompt statements with the layout table in design.md; leave non-Pi default routes intact.
- [x] Pi main-session work loads specs directly, leaves unused empty manifests alone and uses existing `--allow-empty-context` only after implementation approval.
- [x] Actual implement/check delegation prepares the relevant manifest; document the project-tool enforcement boundary and retain the native-tool dispatch protocol.
- [x] Recover persisted layout on continue rather than recreating optional documents. Preserve full-scope acceptance, blocking-failure handling and once-only spec judgment.
- [x] In the Pi-specific path, correct outdated `_example` seed/optional-removal instructions to the actual empty-seed and validation behavior.
- [x] Do not edit shared start/continue wrappers unless their existing Pi redirection proves insufficient; such a scope change must be reported before expanding the file set.

### 5. Align direct contract documentation and delivery records

Files: `.trellis/decisions/README.md`, `.trellis/spec/cli/backend/script-conventions.md`, and this task's records.

- [x] Update only the planning-material contract references and new explicit-layout semantics; retain the existing decision lifecycle and default-off behavior.
- [x] Record the implementation result, exact checked scope, evidence and runtime limits here. Do not create a decision entry merely to fill a task checklist.
- [x] Perform the one static check below; if it finds a structural/syntax/type issue, repair that issue and repeat only that scope.
- [x] Deliver without automatic commit, push, archive or journal work.

## Validation

### Current planning delivery

Perform one read-only planning check: JSON/JSONL parsing, referenced paths, required standard planning sections, Markdown fence/marker structure and trailing whitespace. Confirm task remains planning and product files are unchanged. This is not execution of the proposed behavior.

### Authorized implementation check

- Inspect only the changed files' structure, syntax, types and diff formatting in one pass.
- Parse changed Python with `ast.parse` without imports, project execution or bytecode generation; compare both mirrored pairs byte-for-byte.
- Preserve workflow marker pairs, phase numbers and status blocks; parse touched frontmatter/JSON/JSONL and check task-reference paths.
- Use the configured LSP on the changed TypeScript extension if available. A missing server is a reported limit, not permission to install or reconfigure one.
- Run `git diff --check -- <explicit changed file list>`; success is exit 0 with no whitespace diagnostics. Preserve any pre-existing unrelated changes.
- No tests, fixtures, test scripts, builds, package installations or new verification assets. No real child launch, temporary task transitions or calls to the changed validator solely to claim runtime coverage.

### Runtime acceptance reserved for separate authorization

The eventual behavioral acceptance includes standard/compact/lightweight layout handling, disabled configuration, broken decision references, no-mutation start/archive failures, empty-inline manifests, and pre-spawn refusal for absent/broken role context across the tool's supported modes. These are acceptance conditions, not commands authorized for this implementation pass. Until executed under explicit authorization, report them as unverified; static success is not CI or behavioral success.

## Review Gates

- Direction/planning: approved by the user's agreement; no new permission to install, test, build or operate Git.
- Implementation: approved, including the additional metadata field, both direct Python template mirrors and repository Pi delegation entry. Activate using the existing task rules before product edits; reuse this approval for unchanged scope.
- Evidence: retain the V1 requirement that all required acceptance checks pass with valid full-scope evidence and no unresolved blocking failure before claiming full verification. Report static implementation separately from unverified runtime acceptance.
- Scope: only repository files listed in design.md; no installed configuration, other platform defaults, public workflow/extension rollout or historical cleanup.

## Rollback Points

- Before activation: planning documents may be revised; no product rollback is needed.
- During implementation: keep each Python source/mirror pair together. Do not deliver lighter prompts with a validator that still rejects their required format, or a relaxed context path without the corresponding project-tool pre-spawn guard.
- After compact tasks exist: preserve their content and restore standard-required documents before removing layout support. Roll back only this task's edits; no worktree reset, bulk task deletion or automatic Git changes.

## Implementation Record

- Activated this task under its existing complex/standard layout and curated context after the user's complete-plan approval; retained that layout and all planning artifacts.
- Implemented explicit compact planning in the existing validator and aligned create hints, with both Python template mirrors synchronized. Default-off validation and decision lifecycle code are unchanged.
- Added selected-role readiness and context materialization before repository Pi child launch. Each dispatch uses one validated context snapshot; startup context remains tolerant. Main-session prompts/skills now leave unused manifests empty and honor persisted layouts.
- Updated only the 13 approved implementation paths and this task's records; shared wrappers, public workflow/extension templates, installed/global configuration, tests and Git operations remain outside scope.
- Spec judgment: the explicit material contract and project-tool delegation boundary require documentation; updated the approved script-conventions section and decision README references. No new decision record is necessary for this implementation.
- Static scope: 13 approved implementation paths plus 7 task artifacts. Four Python files parsed with `ast.parse`; both script/template pairs are byte-identical; TypeScript 5.9.3 (the existing CLI dependency) parsed the changed extension with zero syntax diagnostics. No application or compiler build was executed.
- Twelve Markdown files have balanced fences and checked frontmatter where present; workflow marker order/pairing and phase headings match HEAD. JSON/JSONL parse, all six manifest references exist, and all scoped paths resolve inside the repository. Repaired task.json's missing final newline after activation; the corrected static pass reports no problems and scoped `git diff --check` exits 0. Tracked changes are exactly the 13 implementation paths; the staging area is empty.
- Full TypeScript type diagnostics are unavailable: the configured LSP has no supported server for this extension path. No server/configuration/dependency was installed or changed. Syntax-only parsing is not a type-check result.
- Runtime acceptance remains unverified: no tests, builds, validator scenarios, temporary task transitions or real child launches were performed. This delivers local implementation plus authorized static evidence, not CI/behavioral acceptance. Task remains in_progress; no commit, push or archive.

### Review Fix: Unused Empty Role Manifest

- The user authorized fixing the review finding: unconditional full-task `validate` rejected an unused empty manifest before the selected-role check could run. The earlier static pass did not establish that this path worked.
- Extended `validate` with the existing `--allow-empty-context` option and used it only for the repository Pi delegation preflight. Both manifests are still parsed and all row/reference errors still count; task structure validation is unchanged. Only zero-entry readiness is optional, while Pi still requires usable materialized file context from the selected role before launching children. Default CLI validation remains strict.
- Added four directly required script paths to the implementation scope: `task.py`, `common/task_context.py`, and their exact template mirrors. This is the user's review-fix follow-up, not a public workflow rollout. The extension, design and scoped script contract were updated; no global configuration, tests or Git state were changed.
- Static follow-up passed: all four changed Python files parse with Python 3.9 grammar; both new script/template pairs are byte-identical; TypeScript 5.9.3 parses the extension without syntax diagnostics; the three changed Markdown files have balanced fences; checked paths remain repository-local; scoped `git diff --check` exits 0. Reviewed the changed argument forwarding and zero-entry guard.
- No full TypeScript type check, runtime validation, tests, builds or actual delegation were performed. Runtime acceptance remains unverified; no installed configuration changes, commit, push or archive.

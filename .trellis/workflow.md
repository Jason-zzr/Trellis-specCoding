# Development Workflow

---

## Core Principles

**Local pilot scope:** the lightweight overrides below apply only when the current platform is Pi. Other platforms use the non-Pi rules and their existing platform-specific steps; sharing this file does not opt them into the pilot.

1. **Plan before code** — figure out what to do before you start. On Pi, use reviewed artifacts for formal tasks and handle clear low-risk local requests directly.
2. **Specs injected, not remembered** — guidelines are injected via hook/skill, not recalled from memory
3. **Persist everything** — research, decisions, and lessons go to files. On Pi, persist formal task context and necessary evidence; ordinary questions do not create or change task records.
4. **Incremental development** — one task at a time
5. **Capture learnings** — after each task, review and write new knowledge back to spec. On Pi, judge this once at the complete delivery check and reuse the conclusion during wrap-up.

---

## Trellis System

### Developer Identity

On first use, initialize your identity:

```bash
python3 ./.trellis/scripts/init_developer.py <your-name>
```

Creates `.trellis/.developer` (gitignored) + `.trellis/workspace/<your-name>/`.

### Spec System

`.trellis/spec/` holds coding guidelines organized by package and layer.

- `.trellis/spec/<package>/<layer>/index.md` — entry point with **Pre-Development Checklist** + **Quality Check**. Actual guidelines live in the `.md` files it points to.
- `.trellis/spec/guides/index.md` — cross-package thinking guides.

```bash
python3 ./.trellis/scripts/get_context.py --mode packages   # list packages / layers
```

**When to update spec**: new pattern/convention found · bug-fix prevention to codify · new technical decision.

### Task System

Every task has its own directory under `.trellis/tasks/{MM-DD-name}/` holding `task.json`, `prd.md`, optional `design.md`, optional `implement.md`, optional `research/`, and context manifests (`implement.jsonl`, `check.jsonl`) for sub-agent-capable platforms.

```bash
# Task lifecycle
python3 ./.trellis/scripts/task.py create "<title>" [--slug <name>] [--parent <dir>]
python3 ./.trellis/scripts/task.py start <name>          # set active task (session-scoped when available)
python3 ./.trellis/scripts/task.py current --source      # show active task and source
python3 ./.trellis/scripts/task.py finish                # clear active task (triggers after_finish hooks)
python3 ./.trellis/scripts/task.py archive <name>        # move to archive/{year-month}/
python3 ./.trellis/scripts/task.py list [--mine] [--status <s>]
python3 ./.trellis/scripts/task.py list-archive

# Code-spec context (injected into implement/check agents via JSONL).
# `implement.jsonl` / `check.jsonl` are seeded on `task create` for sub-agent-capable
# platforms; the AI curates real spec + research entries during planning when needed.
python3 ./.trellis/scripts/task.py add-context <name> <action> <file> <reason>
python3 ./.trellis/scripts/task.py list-context <name> [action]
python3 ./.trellis/scripts/task.py validate <name>

# Task metadata
python3 ./.trellis/scripts/task.py set-branch <name> <branch>
python3 ./.trellis/scripts/task.py set-base-branch <name> <branch>    # PR target
python3 ./.trellis/scripts/task.py set-scope <name> <scope>

# Hierarchy (parent/child)
python3 ./.trellis/scripts/task.py add-subtask <parent> <child>
python3 ./.trellis/scripts/task.py remove-subtask <parent> <child>

# PR creation
python3 ./.trellis/scripts/task.py create-pr [name] [--dry-run]
```

> Run `python3 ./.trellis/scripts/task.py --help` to see the authoritative, up-to-date list.

**Current-task mechanism**: `task.py create` creates the task directory and (when session identity is available) auto-sets the per-session active-task pointer so the planning breadcrumb fires immediately. `task.py start` writes the same pointer (idempotent if already set) and flips `task.json.status` from `planning` to `in_progress`. State is stored under `.trellis/.runtime/sessions/`. If no context key is available from hook input, `TRELLIS_CONTEXT_ID`, or a platform-native session environment variable, there is no active task and `task.py start` fails with a session identity hint. `task.py finish` deletes the current session file (status unchanged). `task.py archive <task>` writes `status=completed`, moves the directory to `archive/`, and deletes any runtime session files that still point at the archived task.

### Workspace System

Records every AI session for cross-session tracking under `.trellis/workspace/<developer>/`.

- `journal-N.md` — session log. **Max 2000 lines per file**; a new `journal-(N+1).md` is auto-created when exceeded.
- `index.md` — personal index (total sessions, last active).

```bash
python3 ./.trellis/scripts/add_session.py --title "Title" --commit "hash" --summary "Summary"
```

### Context Script

```bash
python3 ./.trellis/scripts/get_context.py                            # full session runtime
python3 ./.trellis/scripts/get_context.py --mode packages            # available packages + spec layers
python3 ./.trellis/scripts/get_context.py --mode phase --step <X.Y>  # detailed guide for a workflow step
```

---

<!--
  WORKFLOW-STATE BREADCRUMB CONTRACT (read this before editing the tag blocks below)

  The [workflow-state:STATUS] blocks embedded in the ## Phase Index section
  below are the SINGLE source of truth for the per-turn `<workflow-state>`
  breadcrumb that every supported AI platform's UserPromptSubmit hook
  reads. inject-workflow-state.py (Python platforms) and
  inject-workflow-state.js (OpenCode plugin) only parse them — there is no
  fallback dict baked into the scripts after v0.5.0-rc.0.

  STATUS charset: [A-Za-z0-9_-]+. When the hook can't find a tag, it
  degrades to a generic "Refer to workflow.md for current step." line —
  intentionally visible so users notice and fix a broken workflow.md.

  INVARIANT (test/regression.test.ts):
    Every workflow-walkthrough step marked `[required · once]` must have a
    matching enforcement line in its phase's [workflow-state:*] block. The
    breadcrumb is the only per-turn channel; if a mandatory step isn't
    mentioned there, the AI silently skips it (Phase 1 planning gate
    skip and Phase 3.4 commit skip both manifested via this gap).

  TAG ↔ PHASE scoping:
    [workflow-state:no_task]      → no active task; before Phase 1
    [workflow-state:planning]     → all of Phase 1 (status='planning')
    [workflow-state:planning-inline] → Codex inline variant of Phase 1
    [workflow-state:in_progress]  → Phase 2 + Phase 3.2-3.4
                                    (status stays 'in_progress' from
                                    task.py start until task.py archive)
    [workflow-state:in_progress-inline] → Codex inline variant of Phase 2/3
    [workflow-state:completed]    → currently DEAD: cmd_archive flips
                                    status and moves the dir in the same
                                    call, so the resolver loses the
                                    pointer (block kept for a future
                                    explicit in_progress→completed
                                    transition)

  Editing checklist:
    - When you change a [workflow-state:STATUS] block, also check the
      matching phase's `[required · once]` walkthrough steps for sync
    - Run `trellis update` after editing to push the new bodies to
      downstream user projects (block-level managed replacement)
    - Full runtime contract:
      .trellis/spec/cli/backend/workflow-state-contract.md
-->

## Phase Index

```
Phase 1: Plan    → classify, get task-creation consent, then write planning artifacts
Phase 2: Execute → implement only after task status is in_progress
Phase 3: Finish  → verify, update spec, commit, and wrap up
```

### Request Triage

**Pi only:**

- Questions and read-only investigation: respond directly, without asking to create a task.
- Clear, low-risk local edits: use the user's modification request as authorization, read the relevant specs, implement in the main session on Pi, and perform only permitted verification. Do not create a task by default.
- Work needing sustained tracking, complex/high-risk work, or an explicit request for a task: use existing task-creation consent, or ask once if it is absent, then enter planning. If declined, explain or narrow the scope; do not perform broad inline implementation.
- An active task applies only when the request belongs to it. Unrelated questions do not change its pointer, status or artifacts. Classify independent development separately; never silently attach it to the current task.
- A request belonging to a planning task stays in planning until its reviewed artifacts receive explicit implementation approval. Reuse a recoverable approval for the same scope and design; task creation, artifact existence and a request for a plan alone are not approval.
- If a direct edit reveals permission changes, data migration, cross-package contracts or unresolved architecture/risk decisions, stop before expanding scope and enter task planning. Do not create retrospective approval.
- Modification approval does not authorize installation, runtime checks, tests, Git operations or external writes. Preserve the applicable permission boundary.

**Other platforms (unchanged):**

- Simple conversation or small task: ask only whether this turn should create a Trellis task. If the user says no, skip Trellis for this session.
- Complex task: ask whether you may create a Trellis task and enter planning. If the user says no, do not do broad inline implementation; explain, clarify scope, or suggest a smaller split.
- User approval to create a task is not approval to start implementation. Planning still happens first.

### Planning Artifacts

- `prd.md` — requirements, constraints, and acceptance criteria. Do not put technical design or execution checklists here.
- `design.md` — technical design for complex tasks; on Pi, an explicitly selected compact layout also holds ordered execution and validation.
- `implement.md` — separate execution plan for standard complex tasks; use it for independently maintained batches, complex dependencies or handoff.
- `implement.jsonl` / `check.jsonl` — spec/research manifests for sub-agent context, not execution plans. Pi prepares a role manifest only for actual delegation; other platforms retain their existing requirements.
- Lightweight tasks may be PRD-only. Complex tasks default to `prd.md`, `design.md` and `implement.md`; Pi may select the compact contract below before review.

**Local structure contract** (when `task_structure_validation: true`): declare `task.json.meta.planning_mode` as `lightweight` or `complex` using existing `create --meta` / `set-meta` commands. Missing classification is an error, including for existing tasks at their next start/archive.

| Document | Required level-two sections (exactly once, with content) |
| --- | --- |
| `prd.md` (all tasks) | `Goal`, `Requirements`, `Acceptance Criteria` |
| `design.md` (standard complex; checked if present for lightweight) | `Scope`, `Contracts`, `Data Flow`, `Tradeoffs`, `Rollout and Rollback` |
| `design.md` (explicit compact complex) | `Scope`, `Contracts`, `Ordered Steps`, `Validation` |
| `implement.md` (standard complex; checked whenever present) | `Ordered Steps`, `Validation`, `Review Gates`, `Rollback Points` |

Pi selects `meta.planning_layout: compact` for suitable complex tasks via existing metadata commands; omitted/`standard` keeps the default contract. Compact combines the necessary solution/tradeoffs, ordered work/dependencies/rollback and validation in `design.md`. Prefer standard when execution needs a separately maintained plan. Keep existing optional `implement.md` and check its standard sections; compact Ordered Steps may reference it instead of duplicating the plan. Unknown layouts and lightweight/compact are errors; do not downgrade complexity to avoid materials. Other platforms' default instructions and historical tasks are unchanged.

Code-fenced headings and HTML comments do not satisfy sections. Search [cross-task decisions](./decisions/README.md) during planning and register relevant record paths in `relatedFiles`; keep ordinary task-local choices in `design.md`. Start/archive reject structural errors before state changes; this does not establish user approval, appropriate classification or sound reasoning. Historical archived task documents are not migrated.

### Parent / Child Task Trees

Use a parent task when one user request contains several independently verifiable deliverables. The parent task owns the source requirement set, the task map, cross-child acceptance criteria, and final integration review; it normally should not be the implementation target unless it also has direct work.

Use child tasks for deliverables that can be planned, implemented, checked, and archived independently. Parent/child structure is not a dependency system: if one child must wait for another, write that ordering in the child `prd.md` / `implement.md` and keep each child's acceptance criteria testable.
For explicitly compact Pi children, ordered dependencies belong in `design.md` under Ordered Steps; do not create an optional execution file solely for this rule.

Create new children with `task.py create "<title>" --slug <name> --parent <parent-dir>`. Link existing tasks with `task.py add-subtask <parent> <child>`, and unlink mistakes with `task.py remove-subtask <parent> <child>`.

<!-- Per-turn breadcrumb: shown when there is no active task (before Phase 1) -->

[workflow-state:no_task]
No active task. Classify the current request using Request Triage.
Pi only: questions/read-only investigation and clear low-risk local edits go directly to the answer or authorized work; do not ask for a task by default.
Pi only: create a task for work needing tracking, complex/high-risk work, or an explicit task request, with task-creation consent (reuse it if already given). If declined, clarify or narrow scope rather than implementing broadly. Planning alone is not implementation approval; stop and re-plan if direct work would expand into unresolved scope or risk.
Other platforms: for simple conversation / small tasks, ask whether this turn should create a Trellis task; if declined, skip Trellis for this session. For complex work, ask for task-creation consent and planning; if declined, explain, clarify or suggest a smaller split. Creating a task never authorizes implementation.
[/workflow-state:no_task]

### Phase 1: Plan
- 1.0 Create task `[required · once]` (only after task-creation consent)
- 1.1 Requirement exploration `[required · repeatable]` (`prd.md`; complex tasks follow the selected layout, with all three documents as the default)
- 1.2 Research `[optional · repeatable]`
- 1.3 Configure context `[required · once]` — Pi: only before actual delegation, for the selected role; other sub-agent platforms retain pre-start manifests, other inline platforms skip
- 1.4 Activate task `[required · once]` (review gate, then `task.py start`; status → in_progress)
- 1.5 Completion criteria

<!-- Per-turn breadcrumb: shown throughout Phase 1 (status='planning') -->

[workflow-state:planning]
Pi only: for in-scope requests, load `trellis-brainstorm` as needed; stay in planning until explicit approval of the complete plan. Unrelated questions do not alter this task. Reuse recoverable approval for unchanged scope/design; ask for review if it is missing or the plan materially changed.
Other platforms: load `trellis-brainstorm`; stay in planning and ask for review before `task.py start`.
Lightweight tasks may be PRD-only. Complex tasks default to `prd.md`, `design.md`, and `implement.md`; Pi may explicitly select `meta.planning_layout: compact` with PRD plus design sections Scope, Contracts, Ordered Steps and Validation. Keep and check existing optional documents; other platforms' default rules remain unchanged.
Multi-deliverable scope: consider a parent task plus independently verifiable child tasks; dependencies must be written in child artifacts, not implied by tree position.
Pi: main-session work reads specs directly, leaves unused empty JSONL alone, and after approval starts with `--allow-empty-context`. Before actual implement/check delegation, curate and validate that role's manifest with usable file context. Other platforms curate both manifests before start where required.
Local checks: declare `meta.planning_mode`, meet the planning section contract, search decisions and register relevant `relatedFiles` per `.trellis/decisions/README.md`. Structural checks do not replace user review.
[/workflow-state:planning]

<!-- Per-turn breadcrumb: shown throughout Phase 1 when codex.dispatch_mode=inline.
     Codex-only opt-in alternate to [workflow-state:planning]. The main agent
     edits code directly in Phase 2, so jsonl curation is skipped —
     the inline workflow loads `trellis-before-dev` instead of injecting JSONL
     into a sub-agent. -->

[workflow-state:planning-inline]
Load `trellis-brainstorm`; stay in planning.
Lightweight: `prd.md` can be enough. Complex: finish `prd.md`, `design.md`, and `implement.md`; ask for review before `task.py start`.
Multi-deliverable scope: consider a parent task plus independently verifiable child tasks; dependencies must be written in child artifacts, not implied by tree position.
Inline mode: skip jsonl curation; Phase 2 reads artifacts/specs via `trellis-before-dev`.
Local checks: declare `meta.planning_mode`, meet the planning section contract, search decisions and register relevant `relatedFiles` per `.trellis/decisions/README.md`. Structural checks do not replace user review.
[/workflow-state:planning-inline]

### Phase 2: Execute
- 2.1 Implement `[required · repeatable]`
- 2.2 Quality check `[required · repeatable]`
- 2.3 Rollback `[on demand]`

<!-- Per-turn breadcrumb: shown while status='in_progress'.
     Scope: all of Phase 2 + Phase 3.2-3.4 (status stays 'in_progress' from
     task.py start until task.py archive; only archive flips it). The body
     therefore must cover every required step from implementation through
     commit, including Phase 3.3 spec update and Phase 3.4 commit. -->

Sub-agent dispatch protocol applies to all platforms and all sub-agents, including native Codex `SubagentStart` context injection with child-side pull fallback, class-2 Gemini/Qoder/Copilot/Reasonix/Trae/Grok/Kimi Code, hook-backed ZCode/Snow, and `trellis-research`: every dispatch prompt starts with `Active task: <task path from task.py current>` before role-specific instructions. On Grok Build, use `spawn_subagent` with `subagent_type` set to the Trellis agent name (e.g. `trellis-implement`). On Kimi Code, dispatch the built-in `coder` / `explore` sub-agent with the matching `.kimi-code/skills/trellis-<role>/SKILL.md` instructions.

[workflow-state:in_progress]
Tools: `trellis-implement` / `trellis-research` are sub-agent types, not skills. `trellis-update-spec` is a skill; `trellis-check` is both a skill and an agent.
Pi local default: the main session reads `trellis-before-dev`, implements, then uses the `trellis-check` skill. Do not dispatch implement/check agents merely because the platform supports them. Other platforms keep their step-specific routing.
Pi only: delegate independent useful work when permissions allow. For all platforms, an implement/check sub-agent works directly without spawning another implement/check agent.
Pi only: reuse the approved scope and plan; unrelated questions do not change this task. A material scope/risk change requires confirmation before expanded work.
Pi only: recover the persisted planning layout; do not recreate optional documents or curate unused JSONL. Main-session work reads specs directly. Before actual implement/check delegation, prepare and validate that role's usable file context per 1.3; an empty-inline start never establishes delegation readiness.
Pi only: reuse valid evidence for unchanged inputs, scope, commands and environment. Enter Phase 3 only after implementation is complete, current full-scope evidence satisfies the agreed delivery criteria, and no blocking findings or failed required checks remain. Failure evidence is not a pass; report unverified required criteria and remain in Phase 2.
Pi only: judge spec updates once at the delivery check; Phase 3.3 performs any needed update, Phase 3.4 reuses the conclusion, then commit (with Git authorization) before `/trellis:finish-work`.
Other platforms: keep the existing main-session implement/check dispatch route and prefer the check agent after code changes; then load `trellis-update-spec`, commit (Phase 3.4), and use `/trellis:finish-work`.
Dispatch prompt starts with `Active task: <task path from task.py current>`. Read context: jsonl entries -> `prd.md` -> `design.md if present` -> `implement.md if present`.
Keep `meta.planning_mode`, planning sections and decision `relatedFiles` current per `.trellis/decisions/README.md`. When enabled, start/archive reject related structure errors before mutation; skip-context/branch flags do not bypass these checks. Approval and delivery remain separate facts.
[/workflow-state:in_progress]

<!-- Per-turn breadcrumb: shown while status='in_progress' when
     codex.dispatch_mode=inline. Codex-only opt-in alternate to
     [workflow-state:in_progress]. The main session edits code directly
     instead of dispatching sub-agents. -->

[workflow-state:in_progress-inline]
Flow: `trellis-before-dev` -> edit -> `trellis-check` -> validation -> `trellis-update-spec` -> commit (Phase 3.4) -> `/trellis:finish-work`.
Do not dispatch implement/check sub-agents in inline mode.
Read context: `prd.md` -> `design.md if present` -> `implement.md if present`, plus relevant spec/research loaded by skills.
Keep `meta.planning_mode`, planning sections and decision `relatedFiles` current per `.trellis/decisions/README.md`. When enabled, start/archive reject related structure errors before mutation; skip-context/branch flags do not bypass these checks. Approval and delivery remain separate facts.
[/workflow-state:in_progress-inline]

### Phase 3: Finish
- 3.2 Debug retrospective `[on demand]`
- 3.3 Spec update `[required · once]`
- 3.4 Commit changes `[required · once]`
- 3.5 Wrap-up reminder

> Note: step 3.1 was folded into 2.2 (last-iteration full-scope check) and 3.4 (commit preamble). Numbering kept stable to avoid breaking external references.

<!-- Per-turn breadcrumb: shown while status='completed'.
     Currently DEAD in normal flow: cmd_archive writes status='completed' in
     the same call that moves the task dir to archive/, so the active-task
     resolver loses the pointer and the hook never fires on archived tasks.
     Block preserved for a future status-transition redesign (e.g. an
     explicit in_progress→completed command). Edit through the same spec
     channel as the live blocks. -->

[workflow-state:completed]
Code committed. Run `/trellis:finish-work`; if dirty, return to Phase 3.4 first.
[/workflow-state:completed]

### Rules

1. Identify which Phase you're in, then continue from the next step there
2. Run steps in order inside each Phase; `[required]` steps can't be skipped
3. Phases can roll back (e.g., Execute reveals a prd defect → return to Plan to fix, then re-enter Execute)
4. Steps tagged `[once]` are skipped if the output already exists; don't re-run. On Pi, reuse only valid output and approval; re-open when evidence is missing or relevant inputs/scope changed. File presence alone does not prove approval.
5. Artifact presence informs the next step. Lightweight may be PRD-only; complex defaults to all three documents. For explicitly compact Pi tasks, require PRD plus the compact design contract, not an absent optional `implement.md`.

### Active Task Routing

On Pi, first check whether the request belongs to the active task. Answer unrelated questions without changing its pointer or artifacts; resume in-scope work from the first unfinished step, using valid evidence without treating it as proof of completion. Other platforms retain their routes below.

[Claude Code, Cursor, OpenCode, codex-sub-agent, Kiro, Gemini, Qoder, CodeBuddy, Copilot, Droid, Oh My Pi, ZCode, Snow, Reasonix, Trae, Grok, Kimi Code]

- Planning or unclear requirements -> `trellis-brainstorm`.
- `in_progress` implementation/check -> dispatch `trellis-implement` / `trellis-check`.
- Repeated debugging -> `trellis-break-loop`; spec updates -> `trellis-update-spec`.

[/Claude Code, Cursor, OpenCode, codex-sub-agent, Kiro, Gemini, Qoder, CodeBuddy, Copilot, Droid, Oh My Pi, ZCode, Snow, Reasonix, Trae, Grok, Kimi Code]

[Pi]

- In-scope planning -> `trellis-brainstorm` only for unresolved decisions or missing planning artifacts; reuse existing approval.
- Before editing -> `trellis-before-dev`; implementation and `trellis-check` run in the main session by default.
- Delegate only independent useful work when permitted, not to satisfy a platform label; no nested agents.
- Repeated debugging -> `trellis-break-loop`; load `trellis-update-spec` only when the delivery check identifies a needed update.

[/Pi]

[codex-inline, Kilo, Antigravity, Devin, DeepSeek Harness]

- Planning or unclear requirements -> `trellis-brainstorm`.
- Before editing -> `trellis-before-dev`; after editing -> `trellis-check`.
- Repeated debugging -> `trellis-break-loop`; spec updates -> `trellis-update-spec`.

[/codex-inline, Kilo, Antigravity, Devin, DeepSeek Harness]

### Guardrails

- Task creation approval is not implementation approval; implementation waits for `task.py start` after artifact review. Pi's direct path does not create a formal task or bypass a current planning task; it is not enabled on other platforms.
- Keep the selected planning layout complete and reviewed. Pi's inline `--allow-empty-context` bypasses only advance JSONL readiness, not structure validation, approval or acceptance. Real delegation requires usable role context; other platforms retain their material/context requirements.
- Planning must be persisted to task artifacts; checks must run before reporting completion. On Pi, reuse valid checks within the permitted verification scope, but advance only after implementation and the agreed delivery criteria are satisfied. Report unexecuted checks and unresolved failures rather than counting them as passes.

### Loading Step Detail

At each step, run this to fetch detailed guidance:

```bash
python3 ./.trellis/scripts/get_context.py --mode phase --step <step>
# e.g. python3 ./.trellis/scripts/get_context.py --mode phase --step 1.1
```

---

## Phase 1: Plan

Goal: classify the request, get task-creation consent when a task is needed, and produce the planning artifacts required before implementation.

#### 1.0 Create task `[required · once]`

Create the task directory only after task-creation consent. The command sets status to `planning`, writes `task.json`, creates a default `prd.md`, and auto-targets the new task when session identity is available:

```bash
python3 ./.trellis/scripts/task.py create "<task title>" --slug <name>
```

`--slug` is the human-readable name only. Do **not** include the `MM-DD-` date prefix; `task.py create` adds that prefix automatically.

For task trees, create the parent task first and then create each child with `--parent <parent-dir>`. Do not start the parent just because children exist; start the child that owns the next independently verifiable deliverable.

After this command succeeds, the per-turn breadcrumb auto-switches to `[workflow-state:planning]`, telling the AI to stay in planning.

Run only `create` here — do not also run `start`. `start` flips status to `in_progress`, which switches the breadcrumb to the implementation phase before planning artifacts are reviewed. Save `start` for step 1.4.

Skip creation when the current task already exists. On Pi, this applies only when it owns the request: unrelated questions need no task change, and independent work follows Pi Request Triage.

#### 1.1 Requirement exploration `[required · repeatable]`

Load the `trellis-brainstorm` skill and explore requirements interactively with the user per the skill's guidance.

The brainstorm skill will guide you to:
- On Pi, ask only questions that affect scope, design or risk; group independent questions and sequence dependent ones. Other platforms ask one question at a time.
- Prefer researching over asking the user
- Prefer offering options over open-ended questions
- On Pi, update affected artifacts when conclusions change requirements, constraints or acceptance criteria, rather than after every reply. Other platforms update `prd.md` immediately after each user answer.
- Split large scopes into a parent task plus child tasks when the deliverables can be verified independently
- Keep `prd.md` focused on requirements and acceptance criteria
- For complex tasks, produce `design.md` and `implement.md` before implementation; Pi may instead explicitly select the compact PRD + design contract above when a separate execution plan is unnecessary.
- Declare `meta.planning_mode`; follow the local structure contract above for the required documents and exact headings.
- Search [cross-task decisions](./decisions/README.md), inspect relevant successor chains, and register used/created decision paths in `relatedFiles` without duplicating their full reasoning.

When considering a parent/child split:
- Use a parent task when one request contains several independently verifiable deliverables.
- Parent tasks own source requirements, child-task mapping, cross-child acceptance criteria, and final integration review.
- Child tasks own actual deliverables that can be planned, implemented, checked, and archived independently.
- Parent/child structure is not a dependency system. If child B depends on child A, write that ordering in child B's `prd.md` / `implement.md`.
- Start the child task that owns the next deliverable. Do not start the parent unless the parent itself has direct implementation work.

Return to this step whenever requirements change and revise the relevant artifact.

#### 1.2 Research `[optional · repeatable]`

Research can happen at any time during requirement exploration. It isn't limited to local code — you can use any available tool (MCP servers, skills, web search, etc.) to look up external information, including third-party library docs, industry practices, API references, etc.

[Claude Code, Cursor, OpenCode, codex-sub-agent, Kiro, Gemini, Qoder, CodeBuddy, Copilot, Droid, Oh My Pi, ZCode, Snow, Reasonix, Trae, Grok, Kimi Code]

Spawn the research sub-agent:

- **Agent type**: `trellis-research`
- **Task description**: Research <specific question>
- **Key requirement**: Research output MUST be persisted to `{TASK_DIR}/research/`

[/Claude Code, Cursor, OpenCode, codex-sub-agent, Kiro, Gemini, Qoder, CodeBuddy, Copilot, Droid, Oh My Pi, ZCode, Snow, Reasonix, Trae, Grok, Kimi Code]

[Pi]

Research in the main session by default. Delegate only a bounded independent question when useful and permitted, using the Active task protocol. Persist necessary task research for later work; ordinary read-only questions outside a formal task do not create research artifacts.

[/Pi]

[codex-inline, Kilo, Antigravity, Devin, DeepSeek Harness]

Do the research in the main session directly and write findings into `{TASK_DIR}/research/`. `codex-inline` is the explicit mode that keeps work in the main session.

[/codex-inline, Kilo, Antigravity, Devin, DeepSeek Harness]

**Research artifact conventions**:
- One file per research topic (e.g. `research/auth-library-comparison.md`)
- Record third-party library usage examples, API references, version constraints in files
- Note relevant spec file paths you discovered for later reference

Brainstorm and research can interleave freely — pause to research a technical question, then return to talk with the user.

**Key principle**: Research output must be written to files, not left only in the chat. Conversations get compacted; files don't.

#### 1.3 Configure context `[required · once]`

[Claude Code, Cursor, OpenCode, codex-sub-agent, Kiro, Gemini, Qoder, CodeBuddy, Copilot, Droid, Pi, Oh My Pi, ZCode, Snow, Reasonix, Trae, Grok, Kimi Code]

**Pi:** main-session work reads specs and task documents directly; this step is required only when actual delegation is selected. Curate only the selected implement/check role's manifest then. Current task creation seeds empty files: leave unused ones alone; retain useful existing manifests. Remove obsolete `_example` scaffold rows when curating, because explicit validation treats them as errors. Do not delete malformed manifests to evade diagnostics.

**Other platforms:** curate `implement.jsonl` and `check.jsonl` as the spec/research context for Phase 2 using the existing injection path. These files were seeded on `task create` with a single self-describing `_example` line; fill in real entries.

The format and reference guidance below applies whenever a manifest is being curated.

**Location**: `{TASK_DIR}/implement.jsonl` and `{TASK_DIR}/check.jsonl` (already exist).

**Format**: one JSON object per line — `{"file": "<path>", "reason": "<why>"}`. Paths are repo-root relative.

**What to put in**:
- **Spec files** — `.trellis/spec/<package>/<layer>/index.md` and any specific guideline files (`error-handling.md`, `conventions.md`, etc.) relevant to this task
- **Research files** — `{TASK_DIR}/research/*.md` that the sub-agent will need to consult

**What NOT to put in**:
- Code files (`src/**`, `packages/**/*.ts`, etc.) — those are read by the sub-agent during implementation, not pre-registered here
- Files you're about to modify — same reason

**Split between the two files**:
- `implement.jsonl` → specs + research the implement sub-agent needs to write code correctly
- `check.jsonl` → specs for the check sub-agent (quality guidelines, check conventions, same research if needed)

These manifests do not replace the human-readable execution plan: `implement.md` for standard complex tasks, or the Ordered Steps / Validation sections of an explicitly compact Pi `design.md`.

**How to discover relevant specs**:

```bash
python3 ./.trellis/scripts/get_context.py --mode packages
```

Lists every package + its spec layers with paths. Pick the entries that match this task's domain.

**How to append entries**:

Either edit the jsonl file directly in your editor, or use:

```bash
python3 ./.trellis/scripts/task.py add-context "$TASK_DIR" implement "<path>" "<reason>"
python3 ./.trellis/scripts/task.py add-context "$TASK_DIR" check "<path>" "<reason>"
```

**Other platforms (unchanged):** delete the seed `_example` line once real entries exist (optional — it's skipped automatically by consumers). Both manifests must contain at least one real entry before `task.py start`; skip this step only when both already have curated entries.

**Pi delegation readiness:** run `task.py validate <task-dir>` and require usable file references in the selected role's manifest; the unused role need not be nonempty. The repository `trellis_subagent` tool validates and materializes that role's context before any child in single/parallel/chain mode, returning an error rather than spawning with missing, broken, scaffold-only or unusable context. This does not grant delegation permission or authorize routine review agents. For native/community tools, the parent enforces the same prerequisite and Active task prefix; this extension does not intercept those tools.

[/Claude Code, Cursor, OpenCode, codex-sub-agent, Kiro, Gemini, Qoder, CodeBuddy, Copilot, Droid, Pi, Oh My Pi, ZCode, Snow, Reasonix, Trae, Grok, Kimi Code]

[codex-inline, Kilo, Antigravity, Devin, DeepSeek Harness]

Skip this step. Context is loaded directly by the `trellis-before-dev` skill in Phase 2.

[/codex-inline, Kilo, Antigravity, Devin, DeepSeek Harness]

#### 1.4 Activate task `[required · once]`

After artifact review and explicit implementation approval, flip the task status to `in_progress`. On Pi only, reuse recoverable approval for unchanged scope/design rather than asking again on resume:

```bash
python3 ./.trellis/scripts/task.py start <task-dir>
```

Lightweight tasks may be PRD-only. Complex tasks default to all three reviewed documents; explicitly compact Pi tasks require PRD and compact design, and keep/check any existing optional implementation document.

On Pi, approved main-session work uses the existing context-readiness exception, without preparing unused manifests:

```bash
python3 ./.trellis/scripts/task.py start <task-dir> --allow-empty-context
```

The flag does not waive required documents, user approval or acceptance checks, and is not delegation readiness. Actual delegation follows 1.3 before dispatch; no task restart is needed just to prepare its manifest. Other platforms requiring JSONL still curate both before start.

After this command succeeds, the breadcrumb auto-switches to `[workflow-state:in_progress]`, and the rest of Phase 2 / 3 follows.

If `task.py start` errors with a session-identity message (no context key from hook input, `TRELLIS_CONTEXT_ID`, or platform-native session env), follow the hint in the error to set up session identity, then retry.

#### 1.5 Completion criteria

| Condition | Required |
|------|:---:|
| `prd.md` exists | ✅ |
| User confirms task should enter implementation | ✅ |
| `task.py start` has been run (status = in_progress) | ✅ |
| `research/` has artifacts (complex tasks) | recommended |
| `design.md` exists (complex tasks) | ✅ |
| `implement.md` exists (standard complex; optional but checked if present for explicit compact Pi tasks) | ✅ |

[Claude Code, Cursor, OpenCode, codex-sub-agent, Kiro, Gemini, Qoder, CodeBuddy, Copilot, Droid, Pi, Oh My Pi, ZCode, Snow, Reasonix, Trae, Grok, Kimi Code]

| Other dispatch platforms: both manifests have real curated entries before start | ✅ |
| Pi: main-session work has no advance JSONL prerequisite; before actual delegation, the selected role's manifest is validated and supplies usable file context | ✅ |

[/Claude Code, Cursor, OpenCode, codex-sub-agent, Kiro, Gemini, Qoder, CodeBuddy, Copilot, Droid, Pi, Oh My Pi, ZCode, Snow, Reasonix, Trae, Grok, Kimi Code]

---

## Phase 2: Execute

Goal: turn reviewed planning artifacts into code that passes quality checks.

#### 2.1 Implement `[required · repeatable]`

[Claude Code, Cursor, OpenCode, codex-sub-agent, CodeBuddy, Droid, ZCode, Snow, Oh My Pi]

Spawn the implement sub-agent:

- **Agent type**: `trellis-implement`
- **Task description**: Implement the reviewed task artifacts, consulting materials under `{TASK_DIR}/research/`; finish by running project lint and type-check
- **Dispatch prompt guard**: The prompt MUST start with `Active task: <task path>`, then tell the spawned agent it is already the `trellis-implement` sub-agent and must implement directly, not spawn another `trellis-implement` / `trellis-check`.

The platform hook/plugin auto-handles:
- Reads `implement.jsonl` and injects referenced spec/research files into the agent prompt
- Injects `prd.md`, `design.md` if present, and `implement.md` if present
- For Codex, `SubagentStart` supplies native context injection; the agent profile keeps child-side loading as the fallback

[/Claude Code, Cursor, OpenCode, codex-sub-agent, CodeBuddy, Droid, ZCode, Snow, Oh My Pi]

[Gemini, Qoder, Copilot, Reasonix, Trae, Grok, Kimi Code]

Spawn the implement sub-agent:

- **Agent type**: `trellis-implement`
- **Task description**: Implement the reviewed task artifacts, consulting materials under `{TASK_DIR}/research/`; finish by running project lint and type-check
- **Dispatch prompt guard**: The prompt MUST start with `Active task: <task path>`, then explicitly say the spawned agent is already `trellis-implement` and must implement directly without spawning another `trellis-implement` / `trellis-check`.

The pull-based sub-agent definition auto-handles the context load requirement:
- Resolves the active task with `task.py current --source`, then reads `prd.md`, `design.md` if present, and `implement.md` if present
- Reads `implement.jsonl` and requires the agent to load each referenced spec/research file before coding

[/Gemini, Qoder, Copilot, Reasonix, Trae, Grok, Kimi Code]

[Kiro]

Spawn the implement sub-agent:

- **Agent type**: `trellis-implement`
- **Task description**: Implement the reviewed task artifacts, consulting materials under `{TASK_DIR}/research/`; finish by running project lint and type-check
- **Dispatch prompt guard**: Tell the spawned agent it is already the `trellis-implement` sub-agent and must implement directly, not spawn another `trellis-implement` / `trellis-check`.

The platform prelude auto-handles the context load requirement:
- Reads `implement.jsonl` and injects referenced spec/research files into the agent prompt
- Injects `prd.md`, `design.md` if present, and `implement.md` if present

[/Kiro]

[Pi]

1. Read reviewed task documents according to their persisted layout and load relevant specs through `trellis-before-dev`. Reuse useful existing JSONL references when present, but do not create or fill a manifest for main-session work.
2. Implement in the main session. Delegate independent useful work only when permitted and after the selected role's 1.3 context check; an implement/check sub-agent never spawns another.
3. Record permitted verification evidence or missing coverage for 2.2. Do not run lint, tests or builds without the applicable authorization, or repeat a valid check merely to finish this step.

[/Pi]

[codex-inline, Kilo, Antigravity, Devin, DeepSeek Harness]

1. Load the `trellis-before-dev` skill to read project guidelines
2. Read `{TASK_DIR}/prd.md`, then `design.md` if present, then `implement.md` if present
3. Consult materials under `{TASK_DIR}/research/`
4. Implement the code per reviewed artifacts
5. Run project lint and type-check

[/codex-inline, Kilo, Antigravity, Devin, DeepSeek Harness]

#### 2.2 Quality check `[required · repeatable]`

[Claude Code, Cursor, OpenCode, codex-sub-agent, Kiro, Gemini, Qoder, CodeBuddy, Copilot, Droid, Oh My Pi, ZCode, Snow, Reasonix, Trae, Grok, Kimi Code]

Spawn the check sub-agent:

- **Agent type**: `trellis-check`
- **Task description**: Review all code changes against specs and task artifacts; fix any findings directly; ensure lint and type-check pass
- **Dispatch prompt guard**: The prompt MUST start with `Active task: <task path>`, then tell the spawned agent it is already the `trellis-check` sub-agent and must review/fix directly, not spawn another `trellis-check` / `trellis-implement`.

The check agent's job:
- Review code changes against specs
- Review code changes against `prd.md`, `design.md` if present, and `implement.md` if present
- Auto-fix issues it finds
- Run lint and typecheck to verify

[/Claude Code, Cursor, OpenCode, codex-sub-agent, Kiro, Gemini, Qoder, CodeBuddy, Copilot, Droid, Oh My Pi, ZCode, Snow, Reasonix, Trae, Grok, Kimi Code]

[Pi]

Use the `trellis-check` skill in the main session. Keep the check within the agreed verification scope and permissions; do not dispatch a checker by default. Reuse valid evidence from implementation, supplement missing coverage, and report failures or unexecuted checks explicitly. Evidence validity alone does not permit Phase 3: implementation must be complete, current full-scope results must satisfy the agreed delivery criteria, and no blocking findings or failed required checks may remain. Otherwise complete/fix the work in Phase 2 or report the blocker, including any unverified required criterion. Make the spec-update judgment once at the complete delivery check and retain it for 3.3/3.4.

[/Pi]

[codex-inline, Kilo, Antigravity, Devin, DeepSeek Harness]

Load the `trellis-check` skill and verify the code per its guidance:
- Spec compliance
- lint / type-check / tests
- Cross-layer consistency (when changes span layers)

If issues are found → fix → re-check, until green.

[/codex-inline, Kilo, Antigravity, Devin, DeepSeek Harness]

**Final pass (before Phase 3.4 commit)**:

- **Pi:** the last 2.2 covers the complete task change set, not just the latest chunk. Use each affected package's applicable Quality Check guidance and the authorized verification scope. Reuse results only when their inputs, coverage, command/options and environment still match; fill missing coverage or rerun checks affected by changes. A phase transition alone is not a reason to repeat a valid passing check. Report unexecuted checks rather than claiming runtime or CI success; they cannot satisfy a required delivery criterion.
- **Other platforms:** the last 2.2 of a task must run full-scope, not just on the latest implement chunk. List all affected packages with `python3 ./.trellis/scripts/get_context.py --mode packages`, then load each package's spec index Quality Check section. This catches cross-layer / multi-package issues a mid-iteration local 2.2 cannot.

#### 2.3 Rollback `[on demand]`

- `check` reveals a prd defect → return to Phase 1, fix `prd.md`, then redo 2.1
- Implementation went wrong → revert code, redo 2.1
- Need more research → research (same as Phase 1.2), write findings into `research/`

---

## Phase 3: Finish

Goal: ensure code quality, capture lessons, record the work.

#### 3.2 Debug retrospective `[on demand]`

If this task involved repeated debugging (the same issue was fixed multiple times), load the `trellis-break-loop` skill to:
- Classify the root cause
- Explain why earlier fixes failed
- Propose prevention

The goal is to capture debugging lessons so the same class of issue doesn't recur.

#### 3.3 Spec update `[required · once]`

**Pi only:** use the delivery check's recorded spec-update judgment. If it found a new contract, pattern, pitfall or important lesson, load `trellis-update-spec` and perform the needed update. Record cross-task choices in decisions when applicable; ordinary implementation details stay in the task.

If the judgment is already "nothing to update" and no new relevant finding exists, Pi satisfies this step without loading the skill or repeating the review. Judge here only if the conclusion is missing or new evidence changes it.

**Other platforms:** load `trellis-update-spec` and review newly discovered patterns/conventions, pitfalls and technical decisions; update `.trellis/spec/` accordingly. Even if the conclusion is "nothing to update", walk through the judgment.

#### 3.4 Commit changes `[required · once]`

**Spec-sync preamble — Pi:** reuse the delivery check's spec judgment and Phase 3.3 outcome. Return to 3.3 only if a necessary update remains undone, the judgment is missing, or a new contract/finding changes it. Do not start a second spec review just because commits are being drafted; necessary spec writes still belong in the same task commit batch.

**Spec-sync preamble — other platforms:** before drafting commits, ask whether this task fixed a bug or surfaced non-obvious knowledge that should land in `.trellis/spec/`. If yes, return to Phase 3.3 first — spec writes belong in the same task's commit batch, not as a forgotten follow-up.

The AI drives a batched commit of this task's code changes so `/finish-work` can run cleanly afterwards. Goal: produce work commits FIRST, then bookkeeping (archive + journal) commits land after — never interleaved.

**Step-by-step**:

1. **Inspect dirty state**:
   ```bash
   git status --porcelain
   ```
   Snapshot every dirty path. If the working tree is clean, skip to 3.5.

2. **Learn commit style** from recent history (so drafted messages blend in):
   ```bash
   git log --oneline -5
   ```
   Note the prefix convention (`feat:` / `fix:` / `chore:` / `docs:` ...), language (中文/English), and length style.

3. **Classify dirty files into two groups**:
   - **AI-edited this session** — files you wrote/edited via Edit/Write/Bash tool calls in this session. You know what changed and why.
   - **Unrecognized** — dirty files you did NOT touch this session (could be the user's manual edits, leftover WIP from a previous session, or unrelated work). Do NOT silently include these.

4. **Draft a commit plan**. Group AI-edited files into logical commits (1 commit per coherent change unit, not 1 commit per file). Each entry: `<commit message>` + file list. List unrecognized files separately at the bottom.

5. **Present the plan once, ask for one-shot confirmation**. Format:
   ```
   Proposed commits (in order):
     1. <message>
        - <file>
        - <file>
     2. <message>
        - <file>

   Unrecognized dirty files (NOT in any commit — confirm include/exclude):
     - <file>
     - <file>

   Reply 'ok' / '行' to execute. Reply with edits, or '我自己来' / 'manual' to abort.
   ```

6. **On confirmation**: run `git add <files>` + `git commit -m "<msg>"` for each batch in order. Do not amend. Do not push.

7. **On rejection** (user replies "不行" / "我自己来" / "manual" / any pushback on the plan): stop. Do not attempt a second plan. The user will commit by hand; you skip ahead to 3.5 once they confirm.

**Rules**:
- No `git commit --amend` anywhere — three-stage three-commit flow (work commits → archive commit → journal commit).
- Never push to remote in this step.
- If the user wants different message wording but accepts the file grouping, edit the message and re-confirm once — but if they reject the grouping, exit to manual mode.
- The batched plan is one prompt; do not prompt per commit.

#### 3.5 Wrap-up reminder

After the above, remind the user they can run `/finish-work` to wrap up (archive the task, record the session).

---

## Customizing Trellis (for forks)

This section is for developers who want to modify the Trellis workflow itself. All customization is done by editing this file; the scripts are parsers only.

### Changing what a step means

Edit the corresponding step's walkthrough body in the Phase 1 / 2 / 3 sections above. Critical invariants:
- No active task must triage first and ask for task-creation consent before creating a Trellis task.
- Planning must distinguish lightweight PRD-only tasks from complex tasks that require `prd.md`, `design.md`, and `implement.md` before start.
- Every required execution path must keep the Phase 3.4 commit reminder reachable before `/trellis:finish-work`.

All tag blocks live in the `## Phase Index` section above, immediately after each phase summary:

| Scope | Corresponding tag |
|---|---|
| No active task (before Phase 1) | `[workflow-state:no_task]` (after the Phase Index ASCII art) |
| All of Phase 1 (task created → ready for implementation) | `[workflow-state:planning]` (after Phase 1 summary) |
| Codex inline Phase 1 | `[workflow-state:planning-inline]` |
| Phase 2 + Phase 3.2–3.4 (implementation + check + wrap-up) | `[workflow-state:in_progress]` (after Phase 2 summary) |
| Codex inline Phase 2 + Phase 3.2–3.4 | `[workflow-state:in_progress-inline]` |
| After Phase 3.5 (archived) | `[workflow-state:completed]` (after Phase 3 summary; **currently DEAD**) |

### Changing the per-turn prompt text

Directly edit the body of the corresponding `[workflow-state:STATUS]` block. After editing, run `trellis update` (if you're a template maintainer) or restart your AI session (if you're customizing your own project) — no script changes required.

### Adding a custom status

Add a new block:

```
[workflow-state:my-status]
your per-turn prompt text
[/workflow-state:my-status]
```

Constraints:
- STATUS charset: `[A-Za-z0-9_-]+` (underscores and hyphens allowed, e.g. `in-review`, `blocked-by-team`)
- A lifecycle hook must write `task.json.status` to your custom value, otherwise the tag is never read
- Lifecycle hooks live in `task.json.hooks.after_*` and bind to one of `after_create / after_start / after_finish / after_archive`

### Adding a lifecycle hook

Add a `hooks` field to your `task.json`:

```json
{
  "hooks": {
    "after_finish": [
      "your-script-or-command-here"
    ]
  }
}
```

Supported events: `after_create / after_start / after_finish / after_archive`. Note that `after_finish` ≠ a status change (it only clears the active-task pointer); use `after_archive` for "task is done" notifications.

### Full contract

For the workflow state machine's runtime contract, the locations of all status writers, pseudo-statuses (`no_task` / `stale_<source_type>`), the hook reachability matrix, and other deep details, see:

- `.trellis/spec/cli/backend/workflow-state-contract.md` — runtime contract + writer table + test invariants
- `.trellis/scripts/inject-workflow-state.py` — actual parser (reads workflow.md only, no embedded text)

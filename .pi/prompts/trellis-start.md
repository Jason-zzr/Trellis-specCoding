# Start Session

Use fresh compact SessionStart context already supplied to this session; run the commands below only to fill missing or stale information. Apply Request Triage first: ordinary questions do not require full session initialization or task creation.

---

## Step 1: Current state
Identity, git status, current task, active tasks, journal location.

```bash
python3 ./.trellis/scripts/get_context.py
```

If this output includes a line beginning `Trellis update available:`, copy the full line verbatim when summarizing session context. Do not shorten operational command hints.

## Step 2: Workflow overview
Compact Phase Index, request triage rules, planning artifact contract, and the step-detail command.

```bash
python3 ./.trellis/scripts/get_context.py --mode phase
```

Full guide in `.trellis/workflow.md` (read on demand).

## Step 3: Guideline indexes
For development work only, discover packages/spec layers if unknown, then read the relevant indexes. Reuse unchanged guidance already available.

```bash
python3 ./.trellis/scripts/get_context.py --mode packages
cat .trellis/spec/guides/index.md
cat .trellis/spec/<package>/<layer>/index.md   # for each relevant layer
```

Index files list the specific guideline docs to read when you actually start coding.

## Step 4: Decide next action
Apply Request Triage in `.trellis/workflow.md` first; do not infer that every request belongs to the active task.

- **Question/read-only investigation or a clear low-risk local edit** → handle directly within authorization unless it belongs to an existing planning task. Do not ask to create a task by default or mutate unrelated task records.
- **Work requiring a formal task** → reuse task-creation consent or ask once if missing, then plan. Creation consent is not implementation approval.
- **In-scope active task, `planning`** → fill only the selected layout's missing requirements. Lightweight may be PRD-only; complex defaults to three documents, or explicitly selects `meta.planning_layout: compact` for PRD + design (Scope, Contracts, Ordered Steps, Validation). Choose standard for separate batches/dependencies/handoff. For approved main-session work, use `task.py start <task-dir> --allow-empty-context`; do not curate unused JSONL. Reuse existing approval for unchanged scope/design; otherwise request review.
- **In-scope active task, `in_progress`** → resume the first unfinished step using existing implementation and verification evidence; do not automatically restart implementation. Load missing step detail, for example:
  ```bash
  python3 ./.trellis/scripts/get_context.py --mode phase --step 2.1 --platform pi
  ```
- **Pi execution** → main-session `trellis-before-dev` → implementation → `trellis-check` skill. Delegate only independent useful work when permitted; do not repeat approvals or valid checks solely on session restart.
- **Actual implement/check delegation** → first curate and validate only the selected role's manifest and ensure usable file references. The project `trellis_subagent` enforces this before spawn; native/community tools require the parent to check it. Preserve existing permissions and the Active task prefix.

---

## Skill routing (quick reference)

| User intent | Skill |
|---|---|
| In-scope formal task planning / unresolved requirements | `trellis-brainstorm` |
| About to write code | `trellis-before-dev` |
| Done coding / quality check | `trellis-check` |
| Stuck / fixed same bug multiple times | `trellis-break-loop` |
| Delivery check identified a needed spec update | `trellis-update-spec` |

Full rules + anti-rationalization table in `.trellis/workflow.md`.

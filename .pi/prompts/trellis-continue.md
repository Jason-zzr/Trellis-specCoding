# Continue Current Task

Resume in-scope work at the next unfinished step in `.trellis/workflow.md`, reusing fresh context, approval and valid evidence. Unrelated questions are answered directly without changing task state or artifacts; independent development follows Request Triage.

---

## Step 1: Load Current Context

```bash
python3 ./.trellis/scripts/get_context.py
```

Confirms: current task, git state, recent commits. Reuse fresh supplied context; run this only when that information is missing or stale.

## Step 2: Load the Phase Index

```bash
python3 ./.trellis/scripts/get_context.py --mode phase
```

Shows the Phase Index (Plan / Execute / Finish) with routing + skill mapping. Reload only if it is missing or changed.

## Step 3: Decide Where You Are

For requests belonging to the active task, route by status, required artifacts and recoverable approval/evidence. This command itself is not approval, but it does not invalidate approval already given for the same scope/design. Without an active task, apply Request Triage rather than automatically creating one.

- `status=planning` + no `prd.md` → **1.1** (load `trellis-brainstorm`)
- `status=planning` + `prd.md` only → decide whether the task is lightweight or complex. Lightweight can move to **1.4** review; complex returns to **1.1** to add `design.md` + `implement.md`.
- `status=planning` + required artifacts complete + required jsonl not curated (including Pi; seed-only is not ready) → **1.3**
- `status=planning` + required artifacts/context ready → **1.4**: reuse an existing approval for unchanged scope/design; request review only if approval is missing or material changes require it, then run `task.py start`.
- `status=in_progress` + implementation incomplete (not started or partially done) → **2.1**; existing checks do not establish completion of the remaining work.
- `status=in_progress` + implementation done, verification evidence missing/stale/partial → **2.2**; supplement only the affected authorized checks.
- `status=in_progress` + unresolved blocking findings or failed required checks → remain in **Phase 2**: fix within scope via **2.1**, then re-check the affected scope via **2.2**, or report the blocker. Valid failure evidence remains a failure, not permission to advance.
- `status=in_progress` + implementation complete + current full-scope evidence satisfies the agreed delivery criteria + no unresolved blocking failures → **3.3** (reuse the spec judgment or perform the indicated update) → **3.4** (existing Git authorization/commit flow). Reuse valid passing evidence rather than repeating it solely on resume. Disclose unauthorized/unexecuted checks; they are not passes. If a required delivery criterion remains unverified, report the gap and stay in Phase 2.
- `status=completed` (rare; usually archived immediately) → archive flow

Phase rules (full detail in `.trellis/workflow.md`):

1. Run steps **in order** within a phase — `[required]` steps must not be skipped
2. `[once]` steps reuse valid outputs and approval for unchanged scope/inputs. File presence alone proves neither approval nor verification; lightweight tasks may be PRD-only, complex tasks need all three documents.
3. You may go back to an earlier phase if discoveries require it

## Step 4: Load the Specific Step

Load only missing/changed detail for the next unfinished step. On Pi, implementation and the `trellis-check` skill run in the main session by default; independent delegation remains subject to permissions:

```bash
python3 ./.trellis/scripts/get_context.py --mode phase --step <X.X> --platform pi
```

Follow the loaded instructions. After each `[required]` step completes, move to the next.

---

## Reference

Full workflow and detailed phase steps live in `.trellis/workflow.md`. This command is only an entry point — the canonical guidance is there.

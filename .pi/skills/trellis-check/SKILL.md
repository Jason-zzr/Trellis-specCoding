---
name: trellis-check
description: "Comprehensive quality verification: spec compliance, lint, type-check, tests, cross-layer data flow, code reuse, and consistency checks. Use when code is written and needs quality verification, before committing changes, or to catch context drift during long sessions."
---

# Code Quality Check

Use this skill in the main session by default on Pi. Verify the complete task change set within the agreed scope and permissions; do not dispatch a checker or enlarge verification merely because this skill was invoked.

---

## Step 1: Identify What Changed

Use the recorded task scope and Git state to identify this task's changes, including new files and earlier chunks. Keep user/unrelated edits and staged/unstaged boundaries separate; do not treat all dirty paths as yours.

```bash
git diff --name-only
git diff --cached --name-only
git status --short
```
## Step 2: Read Task Artifacts and Applicable Specs

For an in-scope formal task, read the applicable `check.jsonl` references and task artifacts below, reusing unchanged material already loaded. A direct low-risk edit uses its request and relevant specs; it does not require task artifacts or load an unrelated task:

- `prd.md`
- `design.md` if present
- `implement.md` if present

```bash
python3 ./.trellis/scripts/get_context.py --mode packages
```

For each changed package/layer, read the spec index and follow its **Quality Check** section:

```bash
cat .trellis/spec/<package>/<layer>/index.md
```

Read the specific guideline files referenced — the index is a pointer, not the goal.

## Step 3: Run Project Checks

Use the applicable project checks only within current authorization; this skill does not authorize tests, builds, installation or test-asset changes. Under a static-only scope, perform the agreed static checks and report runtime verification as not executed.

Reuse an existing result only if it identifies the check/command and options, covered files/inputs, relevant environment and outcome, and still matches the current change set. A phase/session change alone does not require rerunning it. Changed inputs or environment invalidate affected results; missing or partial coverage must be supplemented before claiming a complete pass. Keep evidence in the existing task record or recoverable session, not a new cache system.

Do not conceal failures as skipped or completed; fix only within the authorized scope or report the blocker.

Valid evidence can record a failure; it is not itself a passing result. Advance to Phase 3 only when implementation is complete, current full-scope evidence satisfies the agreed delivery criteria, and no blocking findings or failed required checks remain. Otherwise stay in Phase 2 to complete/fix the work or report the blocker. Unexecuted checks are not passes; an unverified required delivery criterion remains a gap.

## Step 4: Review Against Checklist
Use only checklist items permitted by the agreed verification scope. A static-only check does not establish business behavior, runtime integration or passing tests, and is not permission to expand review.
### Code Quality

- [ ] Applicable authorized lint/type checks passed, or valid prior evidence reused?
- [ ] Authorized runtime/test checks passed, or explicitly reported as not executed?
- [ ] No debug logging left in?
- [ ] No suppressed warnings or type-safety bypasses?

### Test Coverage

- [ ] Existing coverage relevant to the change is identified when coverage review is in scope?
- [ ] Any missing coverage or unexecuted tests are disclosed rather than assumed to pass?
- [ ] Test files, fixtures, dependencies and execution remain subject to explicit permission; none are added automatically by this checklist?

### Spec Sync

- [ ] At the complete delivery check, make one judgment: did this task introduce a new engineering contract, pattern, convention or important lesson requiring a spec update?
- [ ] Record the needed update or a brief "no update needed" conclusion in the existing task record/session. Preserve a valid existing conclusion unless new relevant findings change it.

Phase 3.3 performs any necessary update using `trellis-update-spec`; Phase 3.4 and wrap-up reuse this judgment, rather than repeating it. Cross-task choices belong in decisions where applicable; ordinary implementation details remain in task records.

## Step 5: Cross-Layer Dimensions (if applicable)

Apply only if cross-layer review is within the agreed scope; skip for a single-layer change or a narrower static-only check. Reuse conclusions already supported by unchanged evidence.

### A. Data Flow (changes touch 3+ layers)

- [ ] Read flow traces correctly: Storage → Service → API → UI
- [ ] Write flow traces correctly: UI → API → Service → Storage
- [ ] Types/schemas correctly passed between layers?
- [ ] Errors properly propagated to caller?

### B. Code Reuse (modifying constants, creating utilities)

- [ ] Searched for existing similar code before creating new?
  ```bash
  grep -r "pattern" src/
  ```
- [ ] If 2+ places define same value → extracted to shared constant?
- [ ] After batch modification, all occurrences updated?

### C. Import/Dependency (creating new files)

- [ ] Correct import paths (relative vs absolute)?
- [ ] No circular dependencies?

### D. Same-Layer Consistency

- [ ] Other places using the same concept are consistent?

---

## Step 6: Report and Fix

Report the complete covered scope, evidence reused or produced, spec-update judgment, and unexecuted checks. Fix only authorized findings; after a correction repeat only the affected checks within the same scope. Once that check is complete, deliver rather than initiating another review or unrelated cleanup.

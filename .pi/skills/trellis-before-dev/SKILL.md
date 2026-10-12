---
name: trellis-before-dev
description: "Discovers and injects project-specific coding guidelines from .trellis/spec/ before implementation begins. Reads spec indexes, pre-development checklists, and shared thinking guides for the target package. Use when starting a new coding task, before writing any code, switching to a different package, or needing to refresh project conventions and standards."
---

Read the relevant development guidelines before starting your task.

Execute these steps:

1. **Resolve the request's scope before loading task artifacts**:
   - For an in-scope formal task, read `prd.md`, then `design.md` and `implement.md` if present, plus relevant curated `implement.jsonl` references. Reuse unchanged context already loaded.
   - If that task is still planning, do not edit until the reviewed plan is approved and `task.py start` succeeds; do not repeat a recoverable approval.
   - For a direct low-risk edit under workflow Request Triage, use the request and relevant specs; do not create a task or demand nonexistent planning artifacts. Do not load or mutate an unrelated active task's records.
   - Stop before expanding into unresolved scope or high-risk work; route that work to task planning.
2. **Discover packages and their spec layers only if not already known**:
   ```bash
   python3 ./.trellis/scripts/get_context.py --mode packages
   ```

3. **Identify which specs apply** to your task based on:
   - Which package you're modifying (e.g., `cli/`, `docs-site/`)
   - What type of work (backend, frontend, unit-test, docs, etc.)
   - Any spec/research paths referenced by the task artifacts

4. **Read the spec index** for each relevant module:
   ```bash
   cat .trellis/spec/<package>/<layer>/index.md
   ```
   Follow the **"Pre-Development Checklist"** section in the index.

5. **Read the specific guideline files** listed in the Pre-Development Checklist that are relevant to your task. The index is NOT the goal — it points you to the actual guideline files (e.g., `error-handling.md`, `conventions.md`, `mock-strategies.md`). Read those files to understand the coding standards and patterns.

6. **Read shared guidance as needed**: use `.trellis/spec/guides/index.md` to select the guides relevant to this work. Reuse unchanged guidance already available; do not load unrelated guides merely to initialize a small edit.
7. Understand the coding standards and patterns you need to follow, then proceed with your development plan.

This step is **mandatory** before writing any code.

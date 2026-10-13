---
name: trellis-before-dev
description: "Discovers and injects project-specific coding guidelines from .trellis/spec/ before implementation begins. Reads spec indexes, pre-development checklists, and shared thinking guides for the target package. Use when starting a new coding task, before writing any code, switching to a different package, or needing to refresh project conventions and standards."
---

Read the relevant development guidelines before starting your task.

Execute these steps:

1. **Resolve the request's scope before loading task artifacts**:
   - For an in-scope formal task, recover `meta.planning_mode` / `meta.planning_layout` (omitted layout means standard). Read PRD and the selected layout's reviewed documents; compact design contains Ordered Steps and Validation, with `implement.md` optional. Reuse existing useful JSONL references if present, but read specs directly and do not create/fill a manifest for main-session work.
   - If still planning, require reviewed-plan approval and a successful `task.py start`; main-session work uses `--allow-empty-context` without waiving structure validation. Reuse existing approval, do not recreate optional documents, and prepare/validate the selected manifest only before actual permitted delegation.
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

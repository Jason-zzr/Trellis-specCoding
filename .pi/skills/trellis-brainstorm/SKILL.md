---
name: trellis-brainstorm
description: "Guides requirements discovery for formal tasks before implementation. Uses repository evidence, groups independent decisions, persists planning conclusions, and obtains one approval for the reviewed plan. Use when a formal task has unresolved requirements or missing planning artifacts; direct low-risk work follows workflow Request Triage."
---

# Trellis Brainstorm

## Non-Negotiable Planning Contract

This skill governs formal task planning, not ordinary questions or the direct low-risk path in `.trellis/workflow.md`. Task-creation consent and an initial modification request are not approval of a formal task's plan.

Before a formal task enters implementation, the user must explicitly approve its complete reviewed plan. Obtain that approval once and reuse it across continuations when scope/design are unchanged. Artifact presence alone is not approval; a request only to plan never authorizes implementation.

While a user-owned scope, product, UX, compatibility, risk or acceptance decision remains unresolved, ask only the needed questions and stay in planning. Group independent decisions; ask dependent questions in order. Do not edit product code, dispatch implementation or run `task.py start` before plan approval.

## Non-Negotiable Evidence Rule

If a question can be answered by exploring the codebase, explore the codebase instead.

This is mandatory. Before asking the user a question, first check whether the answer is already available in code, tests, configs, docs, existing specs, or task history.

Do not ask the user to confirm facts that the repository can answer. Ask only for product intent, preference, scope, risk tolerance, acceptance behavior, or decisions that remain ambiguous after inspection.

Repository evidence establishes current behavior and technical constraints. The user's intended behavior, feature scope boundaries, and UX preferences are never answerable by repository evidence alone, even when an existing pattern exists; existing patterns are options and recommendation evidence, not decisions.

---

Use this skill during Phase 1 planning to turn the user's request into clear requirements and planning artifacts.

## Preconditions

Use this skill only after task-creation consent has been given and the user is ready to enter Trellis planning.

If no task exists yet, create one:

```bash
TASK_DIR=$(python3 ./.trellis/scripts/task.py create "<short task title>" --description "<one-line summary>" --slug <slug>)
```

Use a concise title from the user's request. Both the title and `--description` must be non-empty — `create` rejects blanks, and a record with either one empty is refused at archive. Use a slug without a date prefix. `task.py create` adds the `MM-DD-` directory prefix automatically.

`task.py create` creates the default `prd.md`. Update that file with the current understanding before asking follow-up questions.

## Planning Flow

1. Capture the user's request and initial known facts in `prd.md`.
2. Inspect available evidence before asking questions:
   - code, tests, fixtures, and configs
   - README files, docs, existing specs, and domain notes
   - related Trellis tasks, research files, and session history when present
3. Separate what you found into:
   - confirmed facts
   - product intent still needed from the user
   - scope or risk decisions still needed from the user
   - likely out-of-scope items
4. If user-owned decisions remain, group independent questions with recommendations and trade-offs; sequence dependent questions. Stop before implementation while they remain unresolved.
5. Persist conclusions in the affected planning sections when an answer changes requirements, constraints, decisions or acceptance criteria. Reuse settled evidence; do not re-research or rewrite all artifacts after every reply.
6. When no user-owned decision remains, create or update `design.md` and `implement.md` for complex tasks.
7. Run the requirement convergence gate, then the PRD convergence pass.
8. If the complete plan has not yet been reviewed and approved, present the final planning summary and stop; do not run `task.py start` or edit product code in that turn.
9. An explicit response approving the reviewed plan authorizes `task.py start` and implementation. Reuse recoverable approval for that same plan on resume; repeat review only for material scope/design/risk changes. If approval evidence cannot be recovered, ask rather than infer it from file existence.

Do not invent a project-specific product/spec hierarchy. If the repository already has product, domain, or spec docs, use them. If it does not, proceed with the evidence that exists.

## Question Rules

Group independent questions in one message when useful. Ask one at a time when later choices depend on the answer; do not manufacture a fixed number of questions.

Each question must include:

- the decision needed
- why the answer matters
- your recommended answer
- the trade-off if the user chooses differently

Do not ask process questions such as whether to search, inspect files, or continue brainstorming. Do the evidence work directly. Ask the user only when the remaining issue is a product decision, preference, scope boundary, or risk tolerance choice.

Recommendations are not default selections. Never choose a recommended product decision on the user's behalf merely because the user asked for implementation.

Do not manufacture clarification questions when the request and evidence already resolve the decisions. If the complete plan has not been approved, present it for one implementation approval; if it already has, continue without another review request.

Task-creation consent and the initial implementation request do not replace plan review. Reformatting artifacts or starting a new session does not invalidate approval for unchanged scope and design.

## Thinking Framework: First Principles Analysis

When requirements are vague, solutions feel over-engineered, or you're about to add complexity "because everyone does" — decompose to fundamental truths before reasoning upward.

### Step 1: Restate the Problem

Strip away implementation details to one sentence.

> Bad: "We need to add Redis caching to the user profile endpoint"
> Good: "User profile data takes too long to load"

### Step 2: List Fundamental Truths

What is absolutely true (not opinion or convention)?

| Category | Examples |
|----------|----------|
| **Physical constraints** | Network latency ≥ 0, disk I/O has limits |
| **Business rules** | "Users must see their own data" |
| **Technical invariants** | "Data must be consistent" |
| **User needs** | "The user wants X within Y seconds" |

### Step 3: Challenge Assumptions

For each component of the current plan:

- **Fact or convention?** "We always use REST" — why?
- **What if we removed this?** If nothing breaks, it's unnecessary.
- **Solving the actual problem or a symptom?** Trace the causal chain.
- **Who benefits from this complexity?** If "nobody", simplify.

### Step 4: Build Up from Truths

1. Start with the minimum viable mechanism satisfying all truths
2. Add complexity only when a specific truth demands it
3. Each addition must answer: "Which truth requires this?"

### Step 5: Validate

- Does the solution solve the original problem?
- What assumptions need verification?
- What's the simplest experiment to test this?

## Requirement Convergence Gate

Before final review, verify all of the following:

- the user outcome and product value are explicit
- in-scope and out-of-scope behavior are explicit
- acceptance criteria describe observable outcomes
- user-owned product, scope, UX, compatibility, and risk decisions are resolved
- blocking open questions are empty
- technical unknowns are researched or explicitly deferred without changing MVP behavior

Lightweight formal tasks may omit `design.md` and `implement.md`, but still need the applicable evidence, a converged plan and one explicit implementation approval. The direct path outside formal tasks follows Request Triage instead.

The final planning summary must show Goal, In Scope, Out of Scope, Acceptance Criteria, Key Decisions, relevant Risks or Deferred Items, and artifact status.

## Artifact Rules

`prd.md` records requirements and acceptance:

- goal and user value
- confirmed facts
- requirements
- acceptance criteria
- out of scope
- open questions that still block planning

`design.md` records technical design for complex tasks:

- architecture and boundaries
- data flow and contracts
- compatibility and migration notes
- important trade-offs
- operational or rollback considerations

`implement.md` records execution planning for complex tasks:

- ordered implementation checklist
- validation commands
- risky files or rollback points
- follow-up checks before `task.py start`

Lightweight tasks may have only `prd.md`. Complex tasks must have `prd.md`, `design.md`, and `implement.md` before `task.py start`.

`implement.md` is not a replacement for `implement.jsonl`. Use JSONL files only for manifest-style spec and research references when the task needs them.

## PRD Convergence Pass

Before final review, check `prd.md` against the artifact structure once and consolidate only where needed. A PRD already meeting this structure does not need a cosmetic rewrite. Reuse the completed pass unless relevant requirements change.

The pass must be lossless:

- Collapse repeated facts into one authoritative section.
- Fold temporary brainstorm sections such as `What I already know`, `Assumptions`, and resolved `Open Questions` into Goal, Background, Requirements, Technical Notes, or Acceptance Criteria.
- Remove resolved open questions instead of leaving empty or already-answered sections.
- Merge parallel bug and requirement lists when they describe the same work; keep each defect's severity, evidence, and file:line anchors on the owning requirement.
- Preserve every file:line anchor, decision, constraint, requirement ID, and acceptance-criteria mapping.
- Do not proceed to final review while any blocking open question remains.

After the pass, read `prd.md` top to bottom and verify that no fact is repeated across sections unless the repetition adds new information.

## Quality Bar

Before declaring planning ready:

- `prd.md` contains testable acceptance criteria.
- `prd.md` has passed the PRD convergence pass: no unresolved temporary brainstorm sections, no duplicate facts across sections, and no lost anchors, decisions, or acceptance mappings.
- Repository-answerable questions have already been answered through inspection.
- Blocking open questions are empty.
- Complex tasks have `design.md` and `implement.md`.
- The latest final planning summary has been presented to the user.
- Explicit user approval of that reviewed scope/design is recorded or recoverable; reuse it when unchanged.

Do not start implementation merely because the user originally asked for implementation.

---
name: change-planner
description: Investigate a proposed repository addition, modification, or deletion read-only and produce a scoped implementation and impact plan. Use when planning a change before editing code; this skill itself does not implement it.
---

# Change planner

Ground a proposed change in the actual repository and identify the smallest
coherent implementation. A recent repo overview is useful but not required.

## Boundaries

This skill is read-only and investigative. Do not edit files, install dependencies,
generate artifacts, or execute project code, tests, or commands that may mutate
local or external state. Return the plan in the conversation. Do not treat the
plan, or assumptions within it, as authorization to implement additional work.

## Investigation

- Establish the requested behavior, constraints, and acceptance criteria. If no
  change is specified, ask for it; do not invent a feature. Identify ambiguity
  that materially affects the plan and distinguish assumptions from decisions.
- Read applicable repository instructions. Reuse available repo understanding,
  but verify affected files against the current working tree, including existing
  user changes. Inspect relevant callers, contracts, configuration, and tests;
  expand investigation only where dependencies or impact require it.
- Trace the affected input-to-output path. Assess additions, modifications, or
  deletions, compatibility, consumers, dependencies, data, and failure behavior
  where relevant. Cite paths for existing behavior; label proposed paths as new.
- Prefer existing patterns and dependencies. Explain any necessary departure;
  keep unrelated refactors and speculative features outside the plan.
- Choose verification proportional to the change. Report checks as proposed,
  not executed. State what cannot be established from repository evidence.

## Output

Keep these sections concise, scaling detail to the change:

1. **Change and scope** — requested outcome, acceptance criteria, exclusions,
   and explicit assumptions.
2. **Current behavior and impact** — evidence-linked flow, affected components
   and consumers, compatibility implications, and relevant risks or unknowns.
3. **Implementation plan** — ordered steps, existing or proposed file paths,
   and why each change is needed; mention alternatives only for real tradeoffs.
4. **Verification plan** — meaningful checks and expected results, including
   regression coverage where warranted. Clearly state that checks were not run.
5. **Open decisions** — blocking questions and nonblocking assumptions; state
   “none” when ready. End here without implementing the plan.

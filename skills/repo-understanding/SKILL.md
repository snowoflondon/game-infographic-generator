---
name: repo-understanding
description: Investigate a repository read-only and explain its current purpose, structure, behavior, and uncertainties. Use for onboarding or a current-state overview before development.
---

# Repo understanding

Provide an evidence-based overview sized to the repository and the user's question.

## Boundaries

This skill is read-only and investigative. Do not edit files, install dependencies,
generate artifacts, or run commands that may mutate local or external state.
Inspect source and existing test/configuration files; do not execute project code
or tests as part of this skill. Report checks as unrun unless existing results
were supplied, and distinguish those results from current verification.

## Investigation

- Read applicable repository instructions and inspect the working tree, docs,
  manifests, entry points, core components, and relevant tests. Exclude generated
  files, dependency directories, and secret values.
- Trace implemented input-to-output paths, including validation, external services,
  persistence, and failure handling where present. Separate stated intent from
  working behavior; do not invent missing architecture.
- Identify runtime, development, and build dependencies; describe test coverage
  from inspection, material gaps, risks, and unknowns. Ground risks in evidence
  and their likely impact rather than proposing a generic production checklist.
- Cite relevant file paths, adding line numbers when useful. Label inferences
  and unknowns. For large repos, state the inspected scope and its limits.

## Output

Use these short sections; say “none found” or “unknown” where appropriate:

1. **Purpose and current state** — intended purpose versus implemented capability.
2. **Components and dependencies** — key paths, responsibilities, and dependencies.
3. **Architecture and data flow** — entry point → processing → output; inputs,
   validation, side effects, and errors. Include a small diagram only if helpful.
4. **Quality, gaps, and risks** — observed test coverage, architectural gaps,
   evidence-based risks, and practical consequences.
5. **Unknowns and next questions** — unresolved facts and the few questions most
   useful for deciding what to build next; include investigation limits.

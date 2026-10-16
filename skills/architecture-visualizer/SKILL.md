---
name: architecture-visualizer
description: Inspect a repository read-only and explain its current architecture with an evidence-based Mermaid diagram. Use for architecture overviews, component relationships, and data-flow refreshers.
---

# Architecture Visualizer

## Invocation and Scope

Use when a developer requests a top-down architecture diagram or visual refresher.
Invoke by asking: “Use architecture-visualizer to diagram this repository,” or
“Follow skills/architecture-visualizer/SKILL.md to show the rendering pipeline.”
The developer may narrow the scope to a subsystem.

This skill works independently. It may reuse repo-understanding or change-planner
findings already in context, but must verify relevant relationships against current
files. Neither skill is a prerequisite.

## Boundaries

This is a read-only, investigative skill. Do not edit files, execute application
code or tests, install dependencies, or mutate local or external state. Return
the diagram in the response; save it only when the developer explicitly requests
a file, with that write limited to the requested report.

## Investigation and Diagram

- Read repository guidance, entry points, dependency manifests, relevant modules,
  and documentation. Trace actual calls and artifacts; treat stale documentation
  and prior summaries as claims to verify. Exclude secrets and dependency directories.
- Show major components and their responsibilities, relevant dependencies,
  inputs, outputs, and data flow where present. Include external systems,
  persistent artifacts, and agent/manual steps when they explain system boundaries.
  Do not expand into a file-by-file inventory.
- Prefer one Mermaid `flowchart TD` with concise labels and meaningful subgraphs.
  Label arrows to distinguish data movement from calls or dependency relationships;
  add a second small diagram only if combining them obscures the architecture.
- Depict implemented behavior by default. Include planned components only when
  relevant and clearly mark them as unimplemented. Label inferences and unknowns;
  do not invent connections to complete the diagram.
- Review Mermaid syntax and ensure each substantive node and relationship has
  supporting repository evidence. Do not claim rendered verification unless performed.

## Output

1. **Scope:** inspected area and whether the diagram shows the current system or
   includes explicitly marked plans.
2. **Diagram:** a fenced `mermaid` block showing the top-down architecture.
3. **Reading notes:** briefly explain the main flow, boundaries, and material
   uncertainties or inspection limits. Say when inputs, outputs, or data flow
   are absent or unknown rather than forcing them into the diagram.
4. **Evidence:** link the key files supporting the diagram, with line numbers
   where useful.

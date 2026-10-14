---
name: game-research
description: Research a user-defined video game using available research tools and produce validated metadata JSON.
---

# Game Research

## Objective

Given a video game title, research the game and produce a structured JSON file.
Use this skill when researching game metadata for an infographic.

## Prerequisites

Inspect `GameMetadata` and its nested models in
`src/game_infographic_generator/models.py` before researching. The validator is
`python -m game_infographic_generator validate data/<game_slug>.json` after
editable installation. From the repository root without installation, use
`PYTHONPATH=src .venv/bin/python -m game_infographic_generator validate data/<game_slug>.json`.
If the model or validator is unavailable, report the prerequisite gap
and stop before generating an output file. Do not create or modify the schema
or validator as part of this research skill.

## Procedure

1. Identify the exact game and edition. Clarify ambiguous titles rather than
   silently selecting a different game, remake, or edition.
2. Use available web search and page-reading tools to research reliable sources.
   Open supporting pages rather than relying only on search snippets. If tools
   or sources are unavailable, report the limitation rather than inventing data.
3. Prefer official developer/publisher sources for factual details.
4. Use reputable review aggregators for scores, checking the edition and platform.
5. Distinguish facts from player opinions. Summarize sentiment from actual
   community discussions without implying that a small sample is universal.
6. Populate fields according to the `GameMetadata` Pydantic model. Resolve source
   conflicts where possible; otherwise report the uncertainty.
7. Write the result to `data/<game_slug>.json`.
8. Run the project's Pydantic validator and follow the validation procedure below.
9. Report any missing or uncertain information separately from the JSON file.

## Output Format

The following structure is illustrative; the existing `GameMetadata` model is
authoritative if its fields or types differ.

```json
{
  "title": "Persona 5 Royal",
  "alternative_titles": [
    "ペルソナ5 ザ・ロイヤル"
  ],
  "developer": "P-Studio",
  "publisher": "Atlus",
  "release_date": "2019-10-31",
  "genres": [
    "JRPG",
    "Social Simulation"
  ],
  "platforms": [
    "PlayStation 4",
    "PlayStation 5",
    "PC",
    "Nintendo Switch"
  ],
  "description": "A role-playing game combining dungeon exploration, turn-based combat, and social simulation.",
  "critic_scores": [
    {
      "source": "Metacritic",
      "score": 95,
      "max_score": 100,
      "platform": "PlayStation 4",
      "url": null
    }
  ],
  "player_sentiment": {
    "summary": "Players frequently praise the characters, soundtrack, and stylish presentation.",
    "positives": [
      "Memorable characters",
      "Excellent soundtrack",
      "Stylish presentation"
    ],
    "negatives": [
      "Very long playtime",
      "Slow introductory pacing"
    ]
  },
  "similar_games": [
    "Persona 3 Reload",
    "Metaphor: ReFantazio"
  ],
  "sources": [
    {
      "name": "Official publisher website",
      "url": null
    }
  ]
}
```

This is an illustrative example, not a verified research result. Replace
placeholder source URLs with real, verified links during research.

### Output Rules

- The saved file must contain valid JSON, without Markdown fences or commentary.
- Follow the existing `GameMetadata` Pydantic model; do not include unsupported
  fields.
- Only `title` is required at the top level. Unknown `player_sentiment` may be
  `null`; a supplied object defaults its summary to `null` and lists to `[]`.
  Each critic score requires `source`, `score`, `max_score`, and `platform`;
  each source requires `name`. URLs are optional strings in the schema but
  researched claims still require verified links.
- Scores and maxima must be integers, not numeric strings; scores must be
  nonnegative and no greater than the positive maximum. If a source uses
  fractional scores that cannot fit this contract, report the schema limitation
  rather than rounding, rescaling, or modifying the model.
- Use `null` for unknown optional scalar fields and empty arrays for unknown list
  fields where allowed by the model. Report unavailable required data rather
  than inventing values to satisfy validation.
- Use ISO 8601 dates (`YYYY-MM-DD`). Use the original release date of the specified
  game edition unless otherwise requested; identify its region in the report
  when release dates vary by region.
- Associate review scores with their specific platform and source, preserving
  the source's score scale.
- Never invent review scores or source URLs.
- Summarize player sentiment from actual community discussions, not assumptions.
- Preserve Japanese titles where available.
- Include source URLs for researched claims using the model's supported source
  fields. Explain claim-to-source associations in the report if the model cannot
  express them.
- Never substitute a different game edition.

### Output Location

Save the JSON file to `data/<game_slug>.json`, for example
`data/persona_5_royal.json`. Use a lowercase, underscore-separated slug that
identifies the edition and contains no path separators.

## Validation

After generating the JSON:

1. Run `python -m game_infographic_generator validate data/<game_slug>.json`
   on the saved file (or use the source-tree command above). Exit status 0 means
   schema validation passed; status 1 reports file or validation errors.
2. Inspect any validation errors.
3. Correct the JSON without changing the underlying researched facts.
4. Re-run validation until successful. Stop and report a blocker if errors
   require unavailable facts, schema changes, or an unavailable validator;
   do not repeat attempts without a new corrective action.
5. Report the output path, validation result, and unresolved research gaps,
   including uncertain information or conflicting sources. Validation confirms
   schema compliance, not factual accuracy.

Never fabricate missing information or modify the Pydantic schema simply to
make invalid research output pass.

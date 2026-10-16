---
name: game-research
description: Research a user-defined video game using available research tools and produce validated metadata JSON.
---

# Game Research

## Objective

Given a video game title, research the game and produce a structured JSON file.
Use this skill when researching game metadata for an infographic.

## Schema Development vs. Game Research

- **Intentional schema development:** The JSON contract in this document
  (Schema Rules and Output Format) is authoritative. When the user requests a
  contract change, update these rules first, then align the Pydantic models,
  fixtures, and tests. Do not infer new constraints from example values alone.
- **Game research:** The existing Pydantic model is authoritative for runtime
  validation. Follow this contract when generating output, but never modify
  Pydantic models or the validator just to make generated JSON pass. If the
  contract and implementation disagree, report the mismatch as a development
  task rather than silently changing either during research.

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
   Research original-language alternative titles using the rule below.
4. Use reputable review aggregators for scores. Before taking metadata or scores
   from a source, verify the edition, platform, and release year on the opened
   page; a matching title or familiar URL is insufficient. If it describes a
   different edition, locate the correct listing. If no matching score can be
   verified, leave `critic_scores` empty and report the gap.
5. Distinguish facts from player opinions. Summarize sentiment from actual
   community discussions without implying that a small sample is universal.
6. Populate fields according to the `GameMetadata` Pydantic model. Resolve source
   conflicts where possible; otherwise report the uncertainty.
7. Write the result to `data/<game_slug>.json`.
8. Run the project's Pydantic validator and follow the validation procedure below.
9. Report any missing or uncertain information separately from the JSON file.

## Output Format

The following example illustrates the contract defined by Schema Rules below.

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

## Schema Rules

The root is a JSON object for one game edition. Research output must include
**every top-level field** listed below, even when information is unknown.
For runtime loading, omitted optional fields receive the listed defaults;
this tolerance does not permit the research agent to omit output fields.

| Field | JSON type | Required on load / default |
| --- | --- | --- |
| `title` | nonempty string | Required; no default; not nullable |
| `alternative_titles` | array of strings | Optional; `[]` |
| `developer` | string or null | Optional; `null` |
| `publisher` | string or null | Optional; `null` |
| `release_date` | date string or null | Optional; `null` |
| `genres` | array of strings | Optional; `[]` |
| `platforms` | array of strings | Optional; `[]` |
| `description` | string or null | Optional; `null` |
| `critic_scores` | array of critic score objects | Optional; `[]` |
| `player_sentiment` | sentiment object or null | Optional; `null` |
| `similar_games` | array of strings | Optional; `[]` |
| `sources` | array of source objects | Optional; `[]` |

Nested structures:

- **Critic score:** Required nonempty strings `source` and `platform`, required
  integers `score` and `max_score`, and optional string-or-null `url` (default
  `null`). Require `0 <= score <= max_score` and `max_score > 0`.
- **Sentiment:** Optional string-or-null `summary` (default `null`), and optional
  string arrays `positives` and `negatives` (each defaults to `[]`). Use `null`
  for wholly unknown sentiment, or an object for available sentiment.
- **Source:** Required nonempty string `name` and optional string-or-null `url`
  (default `null`).

Shared constraints:

- Reject unexpected fields at the root and in every nested object.
- Arrays are not nullable; their elements must match the declared type and may
  not be `null`. Each array defaults independently to an empty list.
- Types are strict: do not coerce numbers or booleans into strings, or numeric
  strings, booleans, or fractional numbers into integer scores.
- Dates must be real calendar dates encoded as `YYYY-MM-DD`; reject timestamps
  and numeric epochs. Python callers may also supply a `date` instance.
- Required nonempty strings have minimum length one. Other strings have no
  additional length constraint. URLs are optional strings at the schema level;
  factual accuracy and URL validity/reachability are research responsibilities.

### Output Rules

- The saved file must contain valid JSON, without Markdown fences or commentary.
- Follow the existing `GameMetadata` Pydantic model; do not include unsupported
  fields.
- Include all top-level fields from Schema Rules. Use `null` for unknown
  nullable values (including `player_sentiment`) and `[]` for unknown lists.
  Researched claims still require verified links.
- Scores and maxima must be integers, not numeric strings; scores must be
  nonnegative and no greater than the positive maximum. If a source uses
  fractional scores that cannot fit this contract, report the schema limitation
  rather than rounding, rescaling, or modifying the model.
- Use `null` for unknown optional scalar fields and empty arrays for unknown list
  fields where allowed by the model. Report unavailable required data rather
  than inventing values to satisfy validation.
- Use ISO 8601 dates (`YYYY-MM-DD`). Unless otherwise requested, `release_date`
  is the earliest official full public release of the specified game edition
  across all platforms and regions. Exclude demos, closed/open betas, technical
  tests, and early access. Treat remakes, remasters, and distinct editions
  separately; do not substitute the original game's release date for theirs.
  Identify the platform and region of the selected release in the report and
  include supporting sources. The `platforms` list is independent of this date
  and does not imply simultaneous release on every listed platform. If the
  earliest qualifying date cannot be verified, use `null` and report the gap.
- Associate review scores with their specific platform and source, preserving
  the source's score scale.
- Never invent review scores or source URLs.
- Summarize player sentiment from actual community discussions, not assumptions.
- For games with a Japanese, Korean, or Chinese publisher, include verified
  titles in that publisher's respective language in `alternative_titles` when
  available. Also check the originating developer/studio's language when it is
  Japanese, Korean, or Chinese: publisher nationality alone does not establish
  a game's original language (for example, Korean-developed Stellar Blade has
  a Japanese publisher). Preserve verified original-language titles even when
  the publisher is based elsewhere.
- Use official developer/publisher pages or regional storefronts as evidence.
  Preserve Japanese, Hangul, and simplified/traditional Chinese spellings as
  published; do not translate or transliterate titles yourself. Include only
  titles for the same game edition, remove duplicates, and omit spellings
  identical to `title`. Do not collect unrelated regional localizations.
- If no distinct original-language title can be verified, keep
  `alternative_titles: []` (not an empty string or `null`) and mention the gap.
  For ambiguous multinational origins, report uncertainty rather than guessing.
  This is a research requirement; the runtime type remains `list[str]`.
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

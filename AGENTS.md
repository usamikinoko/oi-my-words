# AGENTS.md

This repository is a collection of Chinese writing-guideline skills. It contains no executable code. Read this section before making changes.

## Repository layout

- `skills/oi-my-words/` — the rewrite skill: strips the AI flavor from an existing draft.
- `skills/oi-my-words-create/` — the companion skill: writes a new article from a topic or outline.
- `docs/` — planning documents and case data (maintained by hand).
- `README.md` / `README_CN.md` — user-facing docs; the two must stay in sync.

## Single source of truth

- `skills/<name>/SKILL.md` is the only source of truth for skill behaviour; rule changes go here only.
- `skills/<name>/SKILL_CN.md` is a Chinese reference translation, not a second skill; it must not change rule numbering or meaning.
- Both skills share the same five-layer rules, and `oi-my-words-create` adds one personal-pronoun rule. Any rule change must be mirrored into the other skill and keep the numbering consistent.
- `install.ps1` and `install.sh` must behave identically; changing one means changing the other.

## Constraints

- Do not add `@skills/...` skill-activation references at the repository root. These skills are triggered by the user naming them explicitly, not by always-on context.
- Both skills must be activated only when the user names the skill; generic wording such as "去 AI 味", "改写", or "写篇文章" must not trigger them automatically.
- Do not rename the `SKILL.md` frontmatter fields (`name` / `description` / `metadata`); hosts rely on them for skill matching.
- Do not tune the rules to pass an evaluation. Every number published in the docs must come from a real run, never from an estimate or a rounded guess.

## Verification

- After changing a `SKILL.md`, re-run one comparison case from `docs/` and commit the new result under `docs/cases/`.

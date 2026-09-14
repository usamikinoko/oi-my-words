# AGENTS.md

This repository is a collection of Chinese writing-guideline skills. It contains no executable code. Read this section before making changes.

## Repository layout

- `skills/oi-my-words/` — the rewrite skill: strips the AI flavor from an existing draft.
- `skills/oi-my-words-create/` — the companion skill: writes a new article from a topic or outline.
- `examples/` — worked input/output examples and their detection numbers (maintained by hand).
- `README.md` / `README_CN.md` — user-facing docs; the two must stay in sync.

## Single source of truth

- `skills/<name>/SKILL.md` is the only source of truth for skill behaviour; rule changes go here only. Its body is written in **Chinese**: these rules govern Chinese prose, and they lose fidelity when expressed in English.
- `skills/<name>/SKILL_EN.md` is the English reference translation — not a second skill, and not normative. It must not change rule numbering or meaning. Hosts load `SKILL.md` as the skill entry point, so this file is documentation only.
- The frontmatter `description` is deliberately bilingual: an English skeleton for the matcher, plus Chinese trigger sentences. That is the one place English earns its keep; do not extend the mixing into the body.
- Do not mix languages inside `SKILL.md`. Headings, prose, and rule text are Chinese only. English appears only where it is the subject matter — term-annotation examples such as `Remote Procedure Call（远程过程调用）`, code fences, and the `name` field.
- Both skills share the same five-layer rules, and `oi-my-words-create` adds one personal-pronoun rule. Any rule change must be mirrored into the other skill and keep the numbering consistent.
- `install.ps1` and `install.sh` must behave identically; changing one means changing the other.

## Constraints

- Do not add `@skills/...` skill-activation references at the repository root. These skills are triggered by the user naming them explicitly, not by always-on context.
- Both skills must be activated only when the request names the skill, whether the request is written in Chinese or in English. Generic wording that does not name the skill must not trigger them automatically.
- Do not rename the `SKILL.md` frontmatter fields (`name` / `description` / `metadata`); hosts rely on them for skill matching.
- The frontmatter `description` must stay within 1024 characters, the limit in the Agent Skills specification. Count it before committing; an over-long description risks truncation by the host, which degrades skill matching.
- Do not tune the rules to pass an evaluation. Every number published in the docs must come from a real run, never from an estimate or a rounded guess.

## Verification

- After changing a `SKILL.md`, re-run one example under `examples/` and update its detection numbers.
- After changing either file in a bundle, check that `SKILL.md` and `SKILL_EN.md` still carry the same rule numbers (`1`–`18` for `oi-my-words`, `1`–`19` for `oi-my-words-create`), the same five layer letters (`A`–`E`), and a `description` within the 1024-character limit.

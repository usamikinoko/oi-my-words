<h1 align="center">oi-my-words</h1>

<p align="center">
  <a href="README.md">English</a> | <a href="README_CN.md">中文简体</a>
</p>

<p align="center">
  <img src="https://sorrowful-paladin-images-1315415177.cos.ap-shanghai.myqcloud.com/260720260914115120258.png" alt="oi-my-words" width="100%">
</p>

oi-my-words is a writing-guideline skill that strips the AI flavor from Chinese articles. Given a draft, it checks the prose across five layers — sentence and grammar, paragraph and structure, Markdown syntax, wording, content quality — and rewrites it to read like natural human writing, keeping the original content, structure, and meaning intact. It never re-plans the article; only the wording changes.

The repository uses the standard Agent Skills bundle layout: `skills/oi-my-words/` holds the skill, and `skills/oi-my-words-create/` holds a companion skill that writes new articles from a topic or outline. Each bundle carries the normative `SKILL.md` — written in Chinese, since these rules govern Chinese prose — alongside `SKILL_EN.md`, an English reference translation kept for review and for readers who do not work in Chinese. Hosts load `SKILL.md`, so the English file is documentation only.

## Effect Showcase

Tested across GPT-5.5, GLM-5.3-flash, DeepSeek-V4-Flash and other models over multiple rounds, oi-my-words consistently brings the AI-generated score down. One worked example — DeepSeek-V4-Flash on how HTTP caching works — is measured with the [Tencent Zhuque AI detector](https://matrix.tencent.com/ai-detect/):

| Draft | Zhuque AI score |
|---|---|
| Raw model output | **99.8%** |
| After oi-my-words | **59.1%** (4-segment weighted) |

Full texts and per-segment numbers: [`examples/http-cache/`](examples/http-cache/).

## Installation

The layout is the generic Agent Skills structure — one directory, one deployable skill package — so any compatible host picks it up as is.

**1. Manual copy.** Clone the repository:

```bash
git clone git@github.com:usamikinoko/oi-my-words.git
```

Copy the whole `skills/oi-my-words` directory into your host's skill root — for DeepSeek Harness, `~/.dsh/skills`:

```bash
cp -r oi-my-words/skills/oi-my-words ~/.dsh/skills/oi-my-words
```

On Windows use `Copy-Item`. Hosts hot-reload skills, so a restart is rarely needed; restart the session once if it is not picked up.

**2. One-command install (DeepSeek Harness).** From the repository root in PowerShell, run `.\install.ps1`. It deploys every bundle under `skills/` (oi-my-words and oi-my-words-create) into `~/.dsh/skills`; `-Target` picks a different root, `-WhatIf` runs a dry run. Old same-named directories are cleaned first, so re-running is safe.

**3. Cross-agent install.** For users running several coding agents (Claude Code, Codex, Cursor, …):

```bash
npx skills add usamikinoko/oi-my-words --global
```

Drop `--global` for the current project only; `--agent <name>` targets one agent; `--skill <name>` installs a single skill. This is vercel-labs' skills CLI — Node.js 22.20 or newer, relying on the standard `skills/<name>/SKILL.md` layout. It covers the coding-agent ecosystem only; DeepSeek Harness is not supported, so DSH users should use method 1 or 2.

## Usage

Name the skill in the request — that is the only trigger. There are no slash commands, and generic wording alone does nothing. **Chinese and English requests both work**; what counts is that `oi-my-words` appears. Paste your draft and name the skill, for example: Rewrite this draft following the oi-my-words guidelines. Asking only to "remove the AI flavor" or to "polish" the text will not activate it; when the intent is clear, the model asks first rather than applying the rules on its own.

Two limits: the skill only rewrites existing text — it never touches headings or section structure, and never turns existing lists into paragraphs. For a new article with planned sections, name the companion skill instead: Write a Markdown article following the oi-my-words-create guidelines, on the topic of ….

## How It Works

A language model writes "the most likely next token", so by default it picks wording that suits the widest possible readership; a human writes for one reader and one subject, and the choices come out uneven. That gap is the AI flavor. It shows up in five layers, and the guidelines are organized along exactly those five.

The sentence-and-grammar layer keeps subjects and objects complete, annotates a technical term as the English term plus its Chinese equivalent in parentheses, and holds adverbials and punctuation back. The paragraph-and-structure layer asks for logic and forward-and-backward coherence, leaving the user's paragraph breaks and sections untouched. The Markdown layer discourages decorative lists in favour of paragraph prose, with blockquotes for supplementary notes. The wording layer wants varied sentences and connectives, no repeated meaning, and the occasional light Classical-Chinese transition. The content layer demands rigor, no fabricated data, and — for tutorials — approachable explanations.

Two principles run through every rule: every sentence that survives must tell the reader something new, and a violation is measured by how likely an experienced writer would do the same thing on purpose — deliberate choices are not violations, unconscious templating is. At execution time the skill marks the problems first, revises layer by layer, then re-reads as a check; no facts are added, and the meaning is never changed.

## License

MIT; see [`LICENSE`](LICENSE). Free to use, modify, and redistribute, provided the copyright and permission notices are kept.

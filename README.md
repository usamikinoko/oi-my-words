# oi-my-words

oi-my-words is a writing-guideline skill that brings Chinese articles written by AI back to natural human narration. It checks a user-provided draft layer by layer across five dimensions and rewrites it, removing the templated traces left by the model, while fully preserving the original content, structure, and intended meaning.

The repository follows the standard Agent Skills bundle layout. The skill itself lives in the `skills/oi-my-words/` directory, where `SKILL.md` is the English version and `SKILL_CN.md` is the Chinese one. The repository also ships a companion skill, oi-my-words-create, for writing brand-new articles rather than rewriting existing text; it lives in the `skills/oi-my-words-create/` directory.

## Installation

oi-my-words uses the generic Agent Skills directory structure — one directory is one deployable skill package — so any host that supports Agent Skills recognizes it directly. The repository offers three installation methods, covering DeepSeek Harness and the common cross-agent setups; pick whichever fits.

Method one, manual copy. Clone the repository first:

```bash
git clone git@github.com:usamikinoko/oi-my-words.git
```

Then copy the entire `skills/oi-my-words` directory into the skill root of your host. For DeepSeek Harness, the user skill root is `~/.dsh/skills`:

```bash
cp -r oi-my-words/skills/oi-my-words ~/.dsh/skills/oi-my-words
```

On Windows, PowerShell users can achieve the same copy with `Copy-Item`. After installation the host hot-reloads the new skill automatically, so a restart is usually unnecessary; if it is not picked up within the session, restart the session once.

Method two, one-command install with the `install.ps1` script shipped at the repository root, aimed at DeepSeek Harness. Open PowerShell in the repository root and run `.\install.ps1`; the script deploys every skill bundle under `skills/` (oi-my-words and oi-my-words-create) into `~/.dsh/skills`. Pass `-Target` to point at a different skill root, or `-WhatIf` for a dry run that writes nothing. The script cleans up any same-named old directory before copying, so re-running it is safe.

Method three, cross-agent install via npx skills, for users who run several coding agents such as Claude Code, Codex, or Cursor. The command below installs the skill into your user-level directory and makes it available to every project:

```bash
npx skills add usamikinoko/oi-my-words --global
```

Drop `--global` to install into the current project only; add `--agent <name>` to target a specific agent, or `--skill <name>` to install just one of the skills. This method is implemented by the skills CLI from vercel-labs, requires Node.js 22.20 or newer, and relies on the standard `skills/<name>/SKILL.md` layout of the repository. Note that it targets the coding-agent ecosystem (claude-code, codex, cursor, and so on); DeepSeek Harness is not on its supported list, so DSH users should use the first two methods.

## Usage

oi-my-words is invoked by naming it explicitly in the request. It has no fixed slash commands and, by design, is not triggered by generic wording on its own. **The request may be written in Chinese or in English** — what triggers the skill is the name oi-my-words appearing in the request, not the language it is written in. Paste the draft you want rewritten and name the skill in the same request, for example: Rewrite this draft following the oi-my-words guidelines. A request that merely describes the goal without naming the skill — asking to remove the AI flavor, to rewrite, or to polish the text — does not activate it; when the intent is clear, the model asks whether to apply the oi-my-words guidelines rather than applying them on its own. Note that this skill only rewrites existing text: it never touches headings or section structure, and never forces existing lists into paragraphs. If you need a brand-new article with planned sections, name the companion skill oi-my-words-create instead, for example: Write a Markdown article following the oi-my-words-create guidelines, on the topic of ….

## How It Works

The idea behind oi-my-words starts from an observation: a language model generates text as the most likely next token, so by default it picks the wording that fits the broadest possible readership, whereas a human writer writes for a specific reader and a specific subject, making uneven, individual choices. The gap between the two concentrates in five layers, and the guidelines are organized along exactly those five: sentence and grammar, paragraph and article structure, Markdown syntax, narrative style and wording, and content quality.

The sentence-and-grammar layer constrains the most basic habits of expression: technical terms are annotated as the English term followed by its Chinese equivalent in parentheses, subject–predicate–object structures stay complete, and adverbials and punctuation are used with restraint. The paragraph-and-structure layer requires logic and forward-and-backward coherence in the narration and, when rewriting, keeps the user's original paragraph breaks and section structure untouched.

The Markdown-syntax layer restricts decorative lists and favors paragraph prose, with blockquotes for supplementary notes. The style-and-wording layer asks for varied sentence patterns and connectives, no repeated phrasing, and the occasional light Classical-Chinese transitional phrase. The content-quality layer demands rigor and depth, no fabricated data, and — for tutorial content — approachable concept explanations.

Two principles run through every rule: every sentence that survives must give the reader something they did not already have, and a violation is measured by how likely it is that an experienced writer would do the same thing on purpose — deliberate choices are not violations; unconscious templating is.

At execution time the skill first reads the draft and marks every problem, then revises layer by layer, and finally re-reads it as a check. No facts are added, and the intended meaning is never changed.

## License

Released under the MIT License; see the LICENSE file at the repository root. You are free to use, modify, and redistribute it, provided the copyright and permission notices are kept.

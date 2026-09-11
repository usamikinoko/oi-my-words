# oi-my-words

oi-my-words 是一个让 AI 写出的中文文章回归人类叙述习惯的写作规范型 Skill。它把用户提供的文章草稿按五个层面逐层检查并改写，去除模型生成的模板化痕迹，同时完整保留原文的内容、结构与想表达的意思。

本仓库以标准 Agent Skills bundle 形式组织，技能本体位于 `skills/oi-my-words/` 目录，其中 `SKILL.md` 为英文版、`SKILL_CN.md` 为中文版；仓库还附带面向新文章创作的姊妹技能 oi-my-words-create，用于根据用户需求编写新文章，而不仅仅是改写用户提供的文章，位于 `skills/oi-my-words-create/` 目录。

## 安装

oi-my-words 采用 Agent Skills 通用目录结构，一个目录即一个可部署的技能包，可以被支持 Agent Skills 的宿主直接识别。仓库提供了三种安装方式，分别覆盖 DeepSeek Harness 与常见的跨 agent 场景，可任选其一。

方式一，手动复制。先把仓库克隆到本地：

```bash
git clone git@github.com:usamikinoko/oi-my-words.git
```

然后把 `skills/oi-my-words` 整个目录复制到宿主对应的用户技能根目录。以 DeepSeek Harness 为例，用户技能根目录是 `~/.dsh/skills`，执行以下命令即可完成安装：

```bash
cp -r oi-my-words/skills/oi-my-words ~/.dsh/skills/oi-my-words
```

Windows 下的 PowerShell 可改用 `Copy-Item` 完成同样的复制。安装后宿主会自动热加载新技能，通常无需重启；如果会话内没有被自动发现，重启一次会话即可。

方式二，仓库根目录自带的 `install.ps1` 一键安装，适合 DeepSeek Harness。在 PowerShell 中进入仓库根目录，执行 `.\install.ps1`，脚本会把 `skills/` 下的全部技能包（oi-my-words 与 oi-my-words-create）逐一部署到 `~/.dsh/skills`；通过 `-Target` 参数可以指定其它技能根目录，加 `-WhatIf` 可以预演而不实际写入。脚本会先清理同名旧目录再复制，重复执行是安全的。

方式三，npx skills 跨 agent 安装，适合同时使用 Claude Code、Codex、Cursor 等多个编码 agent 的用户。执行下面的命令即可把技能安装到用户级目录，对所有项目生效：

```bash
npx skills add usamikinoko/oi-my-words --global
```

不加 `--global` 则只安装到当前项目；加 `--agent <name>` 指定目标 agent，加 `--skill <name>` 只安装其中一个技能。该方式由 vercel-labs 的 skills CLI 实现，要求 Node.js 22.20 以上，并依赖仓库的 `skills/<name>/SKILL.md` 标准布局。需要注意的是它面向的是编码 agent 生态（如 claude-code、codex、cursor 等），DeepSeek Harness 不在其支持列表内，DSH 用户请使用前两种方式。

## 使用

oi-my-words 通过自然语言触发，不依赖固定的斜杠命令。把需要改写的文章草稿直接粘贴给模型，说明要"去 AI 味"、"改写"或"润色"即可；当文本明显带有模型生成的痕迹时，说"AI 味太重"也能直接触发。常用的触发词包括"去 AI 味"、"去AI化"、"AI味太重"、"改写"、"润色"、"更像人写的"，也可以直接说"按 oi-my-words 规范改这段文字"。需要注意的是，本技能只处理已有文本的改写，不会改动标题与章节结构，也不会把用户原有的列表强行转换为段落；如果你需要从零撰写一篇新文章并规划章节结构，请改用本仓库的姊妹技能 oi-my-words-create。

## 工作原理

oi-my-words 的去 AI 味思路来自一个观察：语言模型按"最可能的下一个词"生成文本，因此默认选择对最广泛读者都适用的平均化措辞，而人写作时面对的是具体读者与具体主题，取舍天然不均匀。二者之间的差距集中体现在五个层面，本规范也就按这五个层面组织：句子与语法、段落与文章结构、Markdown 语法、叙述方式与措辞、内容质量。

句子与语法层面约束最基础的表达习惯，包括专业术语采用"英文（中文）"标注、主谓宾完整、状语与标点的克制使用；段落与文章结构层面要求叙述有逻辑、前后呼应，并在改写时保持用户原有的分段与章节结构，不做结构调整。

Markdown 语法层面限制装饰性列表的使用，鼓励段落叙述与补充性引用；叙述方式与措辞层面要求句式与连接词多样化、避免重复表意，并低频点缀浅文言过渡短语；内容质量层面要求文章严谨有深度、不编造数据，教学类内容还要用平易近人的方式解释概念。

贯穿全部规则的有两条原则：每一句保留下来都必须为读者带来新的信息；违反规则的程度按"一个有经验的写作者是否会刻意这样写"来计量，刻意为之不算违规，无意识的模板化才算。

执行时先通读并标记问题，再按层修订，最后通读检查，全程不新增事实，不改变原文想表达的意思。

## 许可证

本项目基于 MIT License 开源，详见仓库根目录的 LICENSE 文件。你可以自由使用、修改与分发，但需保留版权声明与许可声明。

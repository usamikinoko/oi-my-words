<h1 align="center">oi-my-words</h1>

<p align="center">
  <a href="README.md">English</a> | <a href="README_CN.md">中文简体</a>
</p>

<p align="center">
  <img src="https://sorrowful-paladin-images-1315415177.cos.ap-shanghai.myqcloud.com/260720260914115120258.png" alt="oi-my-words" width="100%">
</p>

oi-my-words 是一个写作规范型 Skill，用来去掉中文文章里的 AI 味。给定一篇草稿，它按五个层面逐层检查——句子与语法、段落与结构、Markdown 语法、措辞、内容质量——改写成自然的真人写法，同时保留原文的内容、结构与意思。它不重新规划文章，只动措辞。

仓库采用标准 Agent Skills bundle 布局：`skills/oi-my-words/` 是技能本体（`SKILL.md` 英文版、`SKILL_CN.md` 中文版），`skills/oi-my-words-create/` 是配套技能，根据主题或提纲撰写新文章。

## 效果展示

oi-my-words 已在 GPT-5.5、GLM-5.3-flash、DeepSeek-V4-Flash 等多个模型上做过**多轮测试**，能把 AI 生成概率明显压低。仓库中附了一份示例——DeepSeek-V4-Flash 写的《HTTP 缓存到底怎么生效》——用 [腾讯朱雀 AI 检测助手](https://matrix.tencent.com/ai-detect/) 检测：

| 版本 | 朱雀 AI 检测值 |
|---|---|
| 模型原生输出 | **99.8%** |
| 经 oi-my-words 改写后 | **59.1%**（四段加权） |

两份全文与逐段检测值：[`examples/http-cache/`](examples/http-cache/)。

## 安装

目录结构就是通用的 Agent Skills 布局——一个目录即一个可部署的技能包——支持该规范的宿主可直接识别。

**一、手动复制。** 克隆仓库：

```bash
git clone git@github.com:usamikinoko/oi-my-words.git
```

把 `skills/oi-my-words` 整个目录复制到宿主的技能根目录——DeepSeek Harness 是 `~/.dsh/skills`：

```bash
cp -r oi-my-words/skills/oi-my-words ~/.dsh/skills/oi-my-words
```

Windows 下用 `Copy-Item`。宿主会自动热加载，通常无需重启；若没被发现，重启一次会话即可。

**二、一键安装（DeepSeek Harness）。** 在仓库根目录用 PowerShell 执行 `.\install.ps1`，把 `skills/` 下全部技能包（oi-my-words 与 oi-my-words-create）部署到 `~/.dsh/skills`；`-Target` 换根目录，`-WhatIf` 预演。脚本会先清理同名旧目录，重复执行是安全的。

**三、跨 agent 安装。** 适合同时使用 Claude Code、Codex、Cursor 等多个编码 agent：

```bash
npx skills add usamikinoko/oi-my-words --global
```

不加 `--global` 只装当前项目；`--agent <name>` 指定 agent；`--skill <name>` 只装一个技能。该方式由 vercel-labs 的 skills CLI 实现，要求 Node.js 22.20 以上，依赖 `skills/<name>/SKILL.md` 布局；它只覆盖编码 agent 生态，DeepSeek Harness 不在支持列表内，DSH 用户请用前两种。

## 使用

触发方式只有一条：在请求里点名技能。没有斜杠命令，只说通用措辞无效。**中文与英文请求都能触发**，关键是请求里出现 `oi-my-words`。把草稿贴给模型并点名技能，例如"请遵循 oi-my-words 规则为我改写这段文字"。只说"去 AI 味""改写""润色"不会触发；意图明显但没点名时，模型会先询问，不自行套用。

两点边界：只改写已有文本，不改动标题与章节结构，也不把已有列表转成段落；要从零写一篇带章节规划的新文章，请点名配套技能，例如"请基于 oi-my-words-create 规则为我编写一篇 Markdown 文档，要写的主题是……"。

## 工作原理

语言模型按"最可能的下一个词"生成文本，默认挑对最广读者都适用的措辞；人写作面对的是一个读者和一个主题，取舍天然不均匀。这个差距就是 AI 味，它集中在五个层面，规范也按这五个层面组织。

句子与语法层面要求主谓宾完整、术语用"英文（中文）"标注、状语与标点克制；段落与结构层面要求逻辑与前后呼应，并保持用户原有的分段与章节不动；Markdown 层面少用装饰性列表、以段落叙述为主，补充说明用引用；措辞层面要求句式与连接词多样、不重复表意，并低频点缀浅文言过渡；内容层面要求严谨、不编造数据，教学类内容还要解释得平易近人。

两条原则贯穿全部规则：每一句保留下来都必须给读者新的信息；违规程度按"一个有经验的写作者是否会刻意这样写"衡量——刻意为之不算违规，无意识的模板化才算。执行时先通读标记问题，再逐层修订，最后通读复核；全程不新增事实，不改变原意。

## 许可证

MIT License，详见仓库根目录的 [LICENSE](LICENSE)。可自由使用、修改与分发，需保留版权声明与许可声明。

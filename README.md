<div align="center">

**简体中文 · [English](README.en.md)**

![paper-to-html — 阅读、理解、留下问题](docs/images/cover.svg)

### 把论文变成一份能跟着读的网页

逐图理解证据，查清陌生概念，跟上全文论证。

[![推荐 v2.4](https://img.shields.io/badge/推荐版本-v2.4-2f6354?style=flat-square)](https://github.com/BerryIcey/paper-to-html/releases/tag/v2.4)
[![MIT](https://img.shields.io/badge/License-MIT-657b72?style=flat-square)](LICENSE)

**[下载 v2.4](https://github.com/BerryIcey/paper-to-html/releases/download/v2.4/paper-to-html-v2.4.zip) · [查看技能](https://github.com/BerryIcey/paper-to-html/blob/main/skills/paper-to-html-v2.4/SKILL.md) · [更新说明](docs/v2.4-changes.md) · [反馈问题](https://github.com/BerryIcey/paper-to-html/issues)**

</div>
**v2.4 版本说明：经过 Darwin Skill 辅助优化；未新增功能，未进行额外人工优化。仅调整四项验收、整体走读、修复重测流程，包含独立评审和用户确认。**


## 三个核心阅读体验

下面使用统一比例的功能示意图，突出阅读过程与操作重点；并非实际界面截图，模拟数据不代表真实论文的研究结论。

### 01 · 逐图带你读：从“看见图”到“读出证据”

每张主图有总览，每个小图有对应的讲解。切换面板时，原图和文字一起切换；放大原图可以检查标签和细节。

讲解从当前研究问题开始：**为什么做这一步，比较谁和谁，数据怎样变成图里的一个点、格或柱？** 接着逐项解释本图的坐标、颜色、符号和单位，再指着可定位的实际结果，从观察走到判断。最后说明它回答了什么、哪些问题仍没有解决。

因此读者得到的不是一句“结果显著”，而是一条能复述的理解过程。图注、译文、简短结论和详细解释分别保留；图解不能只复述图注，也不能用通用提醒代替实际读图。

![逐图带读：原图与对应解释同步切换](docs/images/figure-walkthrough.svg)

*演示中先核对组别和测量尺度，再读取柱高差异；方向明确之后，才讨论这个比较能支持什么。正式论文按自己的图和证据重建讲解。*

### 02 · 术语知识卡：补足理解，不打断阅读

默认读者具备相关专业本科基础；超出这一基础且影响理解的概念，才需要补充解释与查阅入口。术语从当前文章发现，数据库帮助核对名称、定义与来源。

遇到影响理解的陌生概念，可以从正文、译文或图注中的术语链接打开知识卡。卡片需要讲清 **它是什么、怎样工作或关系如何成立、本文为什么使用它，以及哪些判断容易混淆**，而不只是展开一个缩写。

术语从当前论文发现和判断，不以已有词表是否命中为前提。同名不同义按语境区分；相关概念之间先交代关系，避免突然跳到另一个名词。卡片按需展开，查完可以回到原来的小图和文字滚动位置。

![术语知识卡：解释概念及其在比较中的作用](docs/images/knowledge-cards.svg)

*这里用“对照”演示卡片和回跳交互。它只是界面示例，不是所有读者都必须标色的固定术语；是否需要标色取决于本篇读者起点和理解影响，不要求把基础名词全部解释。*

### 03 · 全文论证链：看懂每一步为什么需要

单张图能看懂，还需要知道它在全文中做什么。论证链按研究问题连接证据：**已经知道什么 → 还缺什么 → 为什么选这个方法 → 结果如何改变判断**。流程图帮助定位，详细解释补足每条连接的理由。

它不是把图标题排成目录，也不是把术语用箭头串起来。并行证据、没有支持预期的结果、补充验证和尚未解决的分支都应保留；研究顺序不能直接写成事件发生顺序或因果关系。

![全文论证链：问题、比较、观察和下一步的关系](docs/images/argument-chain.svg)

*模拟例子展示：观察到 A 高于 B 之后，还需要问差异是否稳定、原因是什么。由这个缺口解释下一步，而不是只说“继续做实验”。*

[下载演示 HTML](https://raw.githubusercontent.com/BerryIcey/paper-to-html/main/demo/paper-reading.html)，保存后用浏览器打开。GitHub 的 HTML 文件页只显示源码。这个项目是供 Codex 使用的 **Skill 与网页阅读组件**，生成解释需要核对当前论文来源。

## 三步开始

### 1 · 安装推荐版

下载 [paper-to-html-v2.4.zip](https://github.com/BerryIcey/paper-to-html/releases/download/v2.4/paper-to-html-v2.4.zip)，解压后将其中完整的 `paper-to-html-v2.4` 文件夹放进当前设备的 Codex Skill 目录，通常是 `~/.codex/skills/`。已有旧安装时先在技能目录外备份。新开聊天确认技能可用。

下载包版本是 **v2.4**，技能调用名称是 **`$paper-to-html-v2.4`**。GitHub 更新不会自动更新电脑上的安装。

### 2 · 提供论文并调用

```text
$paper-to-html-v2.4
把这篇论文做成中文共读网页。
完整翻译核心正文，逐面板解释全部主图，并讲清全文论证。
```

提供有权使用的 PDF。默认包含核心正文、全部主图、必要知识卡与文末评议；若方法、算法或证明构成论文主贡献，也属于核心；复现级方法细节、附图详解和复习内容可按需追加。缺少补充资料时，助手应说明实际覆盖范围。

### 3 · 阅读并留下问题

静态 HTML 可离线切图、放大、查卡和标记。要保存随手记，请打开该论文的本地阅读服务；问题保存到项目，供下一轮助手处理，**不会即时调用 GPT**。正文与笔记、浏览器草稿与项目文件是不同的保存内容。

<details>
<summary>只想体验组件？启动演示服务</summary>

不需要模型或 OpenAI API 密钥。需要 Python：

```sh
git clone https://github.com/BerryIcey/paper-to-html.git
cd paper-to-html
python skills/paper-to-html-v2.4/assets/reader-components/reading_server.py --root demo --port 18765
```

在同一台设备打开 `http://127.0.0.1:18765/paper-reading.html`。这只是临时演示服务；正式项目需要配置独立后台运行方式。

</details>

## 选择哪个版本

| 版本 | 状态 | 内容与入口 |
|---|---|---|
| **v2.4** | **最新推荐 · 已发布** | [下载](https://github.com/BerryIcey/paper-to-html/releases/tag/v2.4) · [更新报告](docs/v2.4-changes.md)：Darwin 辅助优化验收流程；无新增功能、无额外人工优化 |
| v2.3 | 优化前基线 · 保留原包 | [下载](https://github.com/BerryIcey/paper-to-html/releases/tag/v2.3) · [更新报告](docs/v2.3-changes.md) |
| v2.2 | 历史版 · 保留原包 | [下载](https://github.com/BerryIcey/paper-to-html/releases/tag/v2.2) · [更新报告](docs/v2.2-changes.md) |
| v2.1 | 历史版 · 保留原包 | [下载](https://github.com/BerryIcey/paper-to-html/releases/tag/v2.1) · [更新报告](docs/v2.1-changes.md)：完整逐图讲解要求、自适应术语与知识卡、原文和图注查阅入口 |
| v2.0.2 | 历史版 | [查看快照](https://github.com/BerryIcey/paper-to-html/tree/v2.0.2) · [早期变更](docs/v2-changes.md) |
| v1.0.0 | 原始版 | [查看快照](https://github.com/BerryIcey/paper-to-html/tree/v1.0.0)，用于对照和回退 |

**v2.4 已正式发布并设为推荐版。** v2.2 及更早版本的原始下载包和历史标签继续保留。Skill 版本与某篇论文网页自己的版本号分别管理。

[v2.4 校验文件](https://github.com/BerryIcey/paper-to-html/releases/download/v2.4/paper-to-html-v2.4.sha256) · [版本差异](https://github.com/BerryIcey/paper-to-html/compare/v2.3...v2.4)。不要混用不同版本的参考文件。[个人 Skill 库](https://github.com/BerryIcey/my-skills)保留项目入口。

## 使用前需要知道

- **制作环境：** 支持 Skill 的助手和 PDF 读取能力；组件与服务使用 Python 标准库，PDF 裁图需要 PyMuPDF，脚本语法检查使用 Node.js；可选浏览器回归需要 Playwright 和已安装浏览器。
- **引用显示：** 原文、译文、图注与讲解去除纯文献引用编号和角标；保留图号、单位、公式/化学上标等科学内容，来源留在台账和原论文。
- **核对范围：** 翻译、图例、数值与推理需要逐项核对。测试通过不证明解释全部正确，也不证明所有领域都已验证。
- **保存边界：** 正文可离线阅读；项目笔记依赖本地服务。目前没有断线自动补存、跨设备同步或即时问答。
- **设备访问：** `127.0.0.1` 只供本机使用。手机能读离线文件，不代表能连接电脑的本地地址提交笔记。
- **后台与历史：** 正式项目可保留 0/1/2 个历史备份，最新版另计；Windows 后台方案与其他系统不同，重启存活需另行验证。

## 附加功能 · 阅读时顺手使用

核心是理解论文。下面的工具帮助查阅、标记和保留问题：

| 工具 | 怎么用 |
|---|---|
| 图例与术语颜色 | 查看网页术语的类别，按需关闭底色；网页配色与原图图例分别解释 |
| 荧光笔 | 主动开启后标记文字，支持撤销；个人标黄与术语颜色开关独立 |
| 随手记 | 在侧边记录文字或截图，保存到本地项目，留给下一轮助手处理 |

![附加阅读工具：荧光笔、图例与随手记](docs/images/reading-tools.svg)

随手记需要本地阅读服务，静态文件中的草稿不等于已写入项目；保存问题不会即时触发 GPT。图像放大、面板切换和临时查阅返回也可辅助阅读。

## 一起改善阅读效果

[提交问题](https://github.com/BerryIcey/paper-to-html/issues)时请写明版本、浏览器、期望行为与实际情况。解释不清楚时，指出卡在哪个对象、比较或推理步骤，比只说“太简略”更有帮助。

当前关注：专门术语漏选与基础知识过选、长论文后半部分讲解质量、触控操作，以及不同论证方式的迁移。请勿上传私人笔记、凭据或未经许可的论文全文。

代码与通用说明使用 [MIT 许可](LICENSE)。论文及第三方图片沿用原有权利条件，仓库不分发用户论文。

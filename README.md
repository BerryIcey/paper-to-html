<div align="center">

**简体中文 · [English](README.en.md)**

# paper-to-html

把原文、中文译读、图解和知识卡放在同一个网页。

[![在线预览真实论文](docs/images/live-preview-zh.svg)](https://berryicey.github.io/paper-to-html/)

**[下载 v2.5](https://github.com/BerryIcey/paper-to-html/releases/download/v2.5/paper-to-html-v2.5.zip)　·　[开始使用](#三步开始)　·　[更新说明](docs/latest-changes.md)**

</div>

[![真实论文共读：切换小图时原图与译读同步更新](docs/images/live-figure-panels.webp)](https://berryicey.github.io/paper-to-html/)

*顶部为 Mulet-Lazaro 等（2024）的既有中文共读案例，点击即可体验；当前 Skill 下载版为 v2.5。案例来源与许可见[署名说明](THIRD_PARTY_NOTICES.md)。*

供 Codex 使用的中文论文共读 Skill，当前重点是生物医学实验论文。制作需要能读取 PDF 的助手；生成的静态阅读页可离线打开。

**功能导航：** [逐图带读](#逐图带读) · [知识卡](#知识卡) · [全文论证链](#全文论证链) · [阅读工具](#阅读工具) · [三步开始](#三步开始)

## 逐图带读

![读图：从元素到证据](docs/images/feature-figures-zh.svg)

> **这张图在做什么？作者得到了什么答案？图上哪些证据支持它？**

这三个问题分别对应简短概括、作者的结果与判断、详细带读，互相补充。每个可切换小图都有自己的解释，复杂流程沿箭头走读。

- **先认对象**：比较谁和谁，数据怎样变成一个点、格或柱。
- **读懂编码**：英文分类、坐标、颜色、点形、单位与方法输出，在图旁解释。
- **核对统计**：星号检验什么、参照是谁、P值或阈值及校正如何定义；来源没写清时标出缺口。
- **走到判断**：用图上一个真实例子连接观察与作者结论，保留反例和限定。

![逐图带读与原图放大](docs/images/live-figure-zoom.webp)

## 知识卡

![概念：查懂后回到原处](docs/images/feature-concepts-zh.svg)

**点开术语 → 建立理解 → 返回同一小图和文字位置。** 正文、译文和图注中的关键术语都有查阅入口。

| 先建立什么认识 | 卡片要回答什么 |
|---|---|
| 身份 | 它是什么，容易与什么混淆？ |
| 原理 | 怎样工作，为什么能得到这个读数？ |
| 本文用途 | 作者为什么用它，与当前结果有什么关系？ |

按当前论文和读者基础选择概念，不为凑词数堆基础词条；不同关键概念独立讲清，相关概念再建立联系。

![知识卡查阅与返回](docs/images/live-concept-card.webp)

## 全文论证链

![论证：看清结果怎样接起来](docs/images/feature-argument-zh.svg)

```text
研究问题 → 当前证据 → 仍有缺口 → 下一步为什么能回答
               ↘ 并行验证、否定结果与尚未解决的分支
```

把图放回全文问题，而不是只把图标题排成目录。说明前一结果回答了什么、为什么仍不够、下一方法如何补充；研究顺序与因果关系分别判断。

![全文论证链](docs/images/live-argument-chain.webp)

## 阅读工具

| 🔎 查阅与定位 | 🖍️ 标记与配色 | 📝 随手记（可选） |
|---|---|---|
| 图号导航、整图/小图切换、图片缩放和平移、知识卡返回原处 | 主动开启荧光笔、撤销标记；术语颜色与个人标黄独立 | 在阅读位置记录文字或截图，保存到本地项目，下一轮由助手处理 |
| 浏览器内即可阅读 | 支持离线阅读与本机标记 | 保存项目笔记需要本地服务；不即时调用模型 |

> [!NOTE]
> 静态网页可离线读；浏览器草稿不等于项目笔记。目前没有断线自动补存或跨设备同步。

## 三步开始

### 1 · 安装 v2.5

[**下载 paper-to-html-v2.5.zip**](https://github.com/BerryIcey/paper-to-html/releases/download/v2.5/paper-to-html-v2.5.zip) · [SHA-256校验](https://github.com/BerryIcey/paper-to-html/releases/download/v2.5/paper-to-html-v2.5.sha256)

解压后将完整 `paper-to-html-v2.5` 文件夹放进当前设备的 Codex Skill 目录，通常是 `~/.codex/skills/`。已有安装先在技能目录外备份，新开聊天确认技能可用。GitHub 更新不会自动替换本机安装。

### 2 · 提供论文并调用

```text
$paper-to-html-v2.5
把这篇论文做成中文共读网页。
完整翻译核心正文，按论证需要决定详讲、简讲和跨图比较。
关键概念独立讲清，保留原图、作者结论和全文论证链。
```

提供有权使用的PDF。基础版保留作者讨论与局限，不默认生成独立读者评议；贡献主体中的方法、算法或证明也属于核心。附图详解、复现细节和复习内容按需追加。

### 3 · 打开网页阅读

浏览器直接打开生成的 HTML，即可切图、放大、查卡和标记。需要把随手记保存到项目时，再使用对应论文的本地服务。[安装与常见问题](docs/getting-started.md)

## 版本与使用范围

**当前版本 v2.5**：[完整变更](docs/v2.5-changes.md) · [Skill 源文件](skills/paper-to-html-v2.5/SKILL.md) · [历史版本](docs/versions.md)

- 当前重点为生物医学实验论文；仅在 Codex 测试，其他 Agent 尚未测试。
- 图文解释需要逐源核对；结构或交互测试通过不证明所有科学解释正确，也不证明读者已经理解。
- 组件装配和本地服务使用 Python，PDF 裁图需要 PyMuPDF；可选浏览器回归另需 Node.js、Playwright及浏览器。
- 默认覆盖固定同名最新版，不再提供备份数量选择或历史轮转；既有笔记、附件和历史资料不自动删除。

<details>
<summary>查看单次制作的耗时与 token 记录</summary>

2026-10-29的eCHROMA制作记录使用gpt-6.1-sol / low，耗时约19分29秒，累计5,858,896 tokens，其中5,668,096为缓存输入。这是单次v2.4制作观察，包含重复上下文，不是每篇固定消耗或API账单。[完整记录与统计口径](docs/usage-observation.md)。

</details>

## 反馈与参与

[反馈问题](https://github.com/BerryIcey/paper-to-html/issues)时，请注明版本、浏览器、期待与实际行为；讲解不清时指出具体对象、比较或推理步骤。请勿上传私人笔记、凭据或未经许可的论文全文。

代码与通用说明使用[MIT许可](LICENSE)，论文及第三方图片保留其原有权利条件。[贡献指南](CONTRIBUTING.md) · [第三方署名](THIRD_PARTY_NOTICES.md)

# 实际制作的用量记录 / Measured creation runs

记录两次论文共读网页制作的实际耗时、模型与token用量；每次均使用对应制作完成快照。

## 2026-10-29 · eCHROMA / paper-to-html-v2.4

### 任务与环境

| 项目 | 实际记录 |
|---|---|
| 论文 | Ochi 等，*Chromatin landscape and epigenetic heterogeneity of acute myeloid leukaemia* |
| DOI | 10.1038/s41586-026-10703-4 |
| 输入 | 用户提供的 37 页 PDF，含主文、方法和扩展数据；未取得独立补充图／表文件 |
| Skill | paper-to-html-v2.4 |
| 模型 | `gpt-6.1-sol` |
| 推理强度 | `low`（会话日志的 effort 字段） |
| 运行环境 | Windows / Codex Desktop；日志记录 CLI 版本 0.164.0-alpha.11.1 |
| 制作起点 | 2026-10-29 13:18:53.968 北京时间 |
| 制作完成快照 | 2026-10-29 13:38:22.518 北京时间 |
| 制作耗时 | 约 19 分 29 秒，含读取、生成、工具执行及验收 |
| 交付范围 | 19 个正文单元、5 张主图的 20 个字母面板、25 个原图入口、18 张知识卡、论证链及读者评议 |
| 检查范围 | Edge 桌面／窄屏交互、离线读取、隔离笔记队列及服务自动恢复；未验证真实重启、真机触屏、用户理解效果或完整可访问性 |
| 协作范围 | 本次未使用子代理；没有在首次交付前收到用户对阅读内容的修订反馈 |

### 网页制作的 token 统计

| 字段 | Tokens | 口径 |
|---|---:|---|
| 输入合计 `input_tokens` | 5,812,941 | 已包含缓存输入 |
| 其中缓存输入 `cached_input_tokens` | 5,668,096 | 输入的子集，不再次加到输入总量 |
| 非缓存输入 | 144,845 | 输入合计减去缓存输入 |
| 输出 `output_tokens` | 45,955 | 包含日志中的推理输出子集 |
| 其中推理输出 `reasoning_output_tokens` | 3,843 | 输出的子集，不再次加到输出总量 |
| 缓存写入 `cache_write_input_tokens` | 0 | 日志记录值 |
| **总计 `total_tokens`** | **5,858,896** | **输入合计 + 输出** |

来源为制作完成时保存的 Codex token 用量快照，记录时间为 2026-10-29T05:38:22.518Z。模型及推理强度取自同次制作的会话配置。

### 怎样理解这些数字

- 总量是多次模型调用的累计，不是一次输入长度，也不是网页本身的 token 数。反复提供的系统／工具说明、论文内容和会话上下文会重复计数。
- 大部分输入来自缓存。总 token 数不能按“全部为非缓存输入”解释，也不能将缓存输入额外相加。
- 此处未取得可对应的 API 账单、金额或账户额度前后读数，因此不换算费用、Plus 周额度或其他套餐百分比。
- 这是特定论文、模型、推理强度、工具环境与工作流的一次观测，不是平均性能、质量证明或完成时长承诺。
- 本次制作的 eCHROMA 网页与仓库在线展示的 Mulet-Lazaro 2024 案例是不同项目。本记录不代表公开案例的生成成本。
- 出版社更新查询未成功；独立补充文件未取得。这些内容覆盖边界会影响工作量和结果解释。

### English

This replaces the earlier estimate with a measured **paper-guide creation run** on **2026-10-29**.

The input was the **37-page eCHROMA PDF** by Ochi et al. (DOI: 10.1038/s41586-026-10703-4). The guide was created with **paper-to-html-v2.4**, **`gpt-6.1-sol`**, and reasoning effort **`low`**, on Windows in Codex Desktop. Creation took approximately **19 minutes 29 seconds**, from 13:18:53.968 to the completion snapshot at 13:38:22.518 Beijing time, including reading, generation, tools, and checks.

The creation snapshot recorded **5,812,941 input tokens**, including **5,668,096 cached input tokens**; uncached input was **144,845**. Output was **45,955 tokens**, including **3,843 reasoning output tokens**. Total: **5,858,896 tokens**. Cache-write input was zero. Cached input and reasoning output are subsets, not additional totals.

The delivered guide covered **19 text units, five main figures with all 20 lettered panels, 25 original-image views, 18 concept cards, an argument chain, and a reader assessment**. Desktop/narrow-screen interactions, offline reading, isolated note persistence, and service recovery were checked. Actual restart survival, physical touch devices, user comprehension, and a full accessibility audit were not verified. Separate supplementary files were unavailable, and the publisher-update check did not succeed.

The total includes repeated context across multiple calls and is dominated by cached input. It is not a single prompt length, guide size, API invoice, subscription-allowance percentage, typical per-paper cost, or guaranteed runtime. No subagents were used. This eCHROMA run is separate from the hosted Mulet-Lazaro 2024 example.

## 2026-11-08 · NFE2 redox / paper-to-html-v2.5

### 任务与环境

| 项目 | 实际记录 |
|---|---|
| 论文 | Staehle 等，*A novel role for transcription factor NFE2 in redox regulation and chemotherapy resistance in acute myeloid leukemia* |
| DOI | 10.1038/s41375-026-03095-x |
| 输入 | 用户提供的13页论文PDF；取得出版社35页补充PDF及独立补表 |
| Skill | paper-to-html-v2.5 |
| 模型 | `gpt-6.1-sol` |
| 推理强度 | `high`（同次制作会话的 effort 字段） |
| 运行环境 | Windows / Codex Desktop；日志记录 CLI 版本 0.166.0-alpha.6 |
| 制作起点 | 2026-11-08 17:12:13.375 PST（America/Los_Angeles） |
| 制作完成快照 | 2026-11-08 17:53:57.342 PST（America/Los_Angeles） |
| 制作耗时 | 约41分44秒，含来源核对、翻译、带读、装配、返修及验收 |
| 交付范围 | 42段核心正文及完整翻译、7张主图的50个字母面板、57个原图入口、24张知识卡、作者讨论与全文论证链；含离线网页和本地随手记服务 |
| 检查范围 | Edge桌面、手机和平板尺寸模拟；每种视口切换57个图文入口，共171次；11项交互检查通过，包括标黄持久化、卡片返回、图片预览和隔离队列笔记保存／编辑／删除恢复／断线草稿保留；本地服务及子进程自动恢复通过 |
| 验证边界 | 未实测真实手机／iPad触控、电脑或Codex真正重启、原生200%浏览器缩放、用户理解效果或完整可访问性；未重算原始组学及预后模型 |
| 协作范围 | 未使用子代理 |

### 网页制作的 token 统计

| 字段 | Tokens | 口径 |
|---|---:|---|
| 输入合计 `input_tokens` | 11,606,111 | 已包含缓存输入 |
| 其中缓存输入 `cached_input_tokens` | 11,373,952 | 输入的子集，不再次相加 |
| 非缓存输入 | 232,159 | 输入合计减去缓存输入 |
| 输出 `output_tokens` | 97,392 | 已包含推理输出子集 |
| 其中推理输出 `reasoning_output_tokens` | 20,748 | 输出的子集，不再次相加 |
| 缓存写入 `cache_write_input_tokens` | 0 | 日志记录值 |
| **总计 `total_tokens`** | **11,703,503** | **输入合计 + 输出** |

来源为本次制作完成时保存的Codex会话 `event_msg/token_count → info.total_token_usage` 快照，记录时间为 **2026-11-09T01:53:57.342Z**。模型及推理强度取自同次制作的会话配置。各调用中的上下文累计计数，缓存输入与推理输出分别是输入、输出的子集。

### English

On **2026-11-08**, the **13-page NFE2 redox/AML paper** by Staehle et al. (DOI: **10.1038/s41375-026-03095-x**) was turned into a Chinese reading guide with **paper-to-html-v2.5**, **`gpt-6.1-sol`**, and reasoning effort **`high`**. The publisher's **35-page supplementary PDF and separate tables** were also obtained. Creation took approximately **41 minutes 44 seconds**, from **17:12:13.375** to the completion snapshot at **17:53:57.342 PST**, in the **America/Los_Angeles** time zone, including source review, translation, writing, assembly, revisions and checks.

The creation snapshot recorded **11,606,111 input tokens**, including **11,373,952 cached input tokens**; uncached input was **232,159**. Output was **97,392 tokens**, including **20,748 reasoning output tokens**. Total: **11,703,503 tokens**. Cache-write input was zero. Cached input and reasoning output are subsets, not additional totals.

The guide contains **42 core text paragraphs with full translations, seven main figures with all 50 lettered panels, 57 original-image views, 24 concept cards, author discussion and a full argument map**, plus offline reading and a local notes service. Edge checked all 57 figure views at each of three simulated desktop, phone and tablet sizes (**171 panel checks**) and **11 interaction checks**, including persistent highlights, lookup return, image preview and isolated note operations. Local service recovery was checked. Physical touch devices, an actual computer/Codex restart, native browser zoom at 200%, reader comprehension and a full accessibility audit were not tested. Original omics and prognostic models were not recomputed. No subagents were used.

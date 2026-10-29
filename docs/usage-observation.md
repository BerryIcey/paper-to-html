# 一次实际用量记录 / One measured run

本记录替换此前的经验预估。数据来自 2026-10-29 的 Codex 会话日志，统计范围仅为从用户提交论文到首次完成网页交付的制作轮次，不包含之后更新 GitHub 文档的轮次。

## 任务与环境

| 项目 | 实际记录 |
|---|---|
| 论文 | Ochi 等，*Chromatin landscape and epigenetic heterogeneity of acute myeloid leukaemia* |
| DOI | 10.1038/s41586-026-10703-4 |
| 输入 | 用户提供的 37 页 PDF，含主文、方法和扩展数据；未取得独立补充图／表文件 |
| Skill | paper-to-html-v2.4 |
| 模型 | `gpt-6.1-sol` |
| 推理强度 | `low`（会话日志的 effort 字段） |
| 运行环境 | Windows / Codex Desktop；日志记录 CLI 版本 0.164.0-alpha.11.1 |
| 会话起点 | 2026-10-29 13:18:53.968 北京时间 |
| 完成记录 | 2026-10-29 13:38:29.274 北京时间 |
| 会话历时 | 约 19 分 35 秒，含读取、生成、工具执行、检查及最终回复；不是纯模型计算时间 |
| 交付范围 | 19 个正文单元、5 张主图的 20 个字母面板、25 个原图入口、18 张知识卡、论证链及读者评议 |
| 检查范围 | Edge 桌面／窄屏交互、离线读取、隔离笔记队列及服务自动恢复；未验证真实重启、真机触屏、用户理解效果或完整可访问性 |
| 协作范围 | 本次未使用子代理；没有在首次交付前收到用户对阅读内容的修订反馈 |

## 完整制作轮次的 token 统计

| 字段 | Tokens | 口径 |
|---|---:|---|
| 输入合计 `input_tokens` | 6,009,446 | 已包含缓存输入 |
| 其中缓存输入 `cached_input_tokens` | 5,864,320 | 输入的子集，不再次加到输入总量 |
| 非缓存输入 | 145,126 | 输入合计减去缓存输入 |
| 输出 `output_tokens` | 46,239 | 包含日志中的推理输出子集 |
| 其中推理输出 `reasoning_output_tokens` | 3,843 | 输出的子集，不再次加到输出总量 |
| 缓存写入 `cache_write_input_tokens` | 0 | 日志记录值 |
| **总计 `total_tokens`** | **6,055,685** | **输入合计 + 输出** |

来源为制作轮次最后一条 `token_usage_record` 的 `turn_token_usage`，时间为 2026-10-29T05:38:29.274Z。该轮是此项目的首次制作轮次，因此该条记录的线程累计值与轮次累计值相同。公开记录只保留汇总，不上传原始聊天、私人笔记、本机路径或账户标识。

首次交付曾报告 **5,858,896 tokens**，那是 13:38:22.518 北京时间的交付前快照，未包含随后一次调用和最终回复。此处采用上述完整制作轮次的 **6,055,685**，不将后续 GitHub 文档维护计入制作用量。

## 怎样理解这些数字

- 总量是多次模型调用的累计，不是一次输入长度，也不是网页本身的 token 数。反复提供的系统／工具说明、论文内容和会话上下文会重复计数。
- 大部分输入来自缓存。总 token 数不能按“全部为非缓存输入”解释，也不能将缓存输入额外相加。
- 此处未取得可对应的 API 账单、金额或账户额度前后读数，因此不换算费用、Plus 周额度或其他套餐百分比。
- 这是特定论文、模型、推理强度、工具环境与工作流的一次观测，不是平均性能、质量证明或完成时长承诺。
- 本次制作的 eCHROMA 网页与仓库在线展示的 Mulet-Lazaro 2024 案例是不同项目。本记录不代表公开案例的生成成本，也未将 eCHROMA 全文网页发布到仓库。
- 出版社更新查询未成功；独立补充文件未取得。这些内容覆盖边界会影响工作量和结果解释。

## English

This replaces the earlier anecdotal estimate with an instrumented observation from one Codex guide-creation turn on **2026-10-29**.

The input was the **37-page eCHROMA PDF** by Ochi et al. (DOI: 10.1038/s41586-026-10703-4). The run used **paper-to-html-v2.4**, **`gpt-6.1-sol`**, and reasoning effort **`low`**, on Windows in Codex Desktop. Session elapsed time was approximately **19 minutes 35 seconds**, from 13:18:53.968 to 13:38:29.274 Beijing time, including reading, generation, tools, checks, and the final response.

The completed turn recorded **6,009,446 input tokens**, including **5,864,320 cached input tokens**; uncached input was **145,126**. Output was **46,239 tokens**, including **3,843 reasoning output tokens**. Total: **6,055,685 tokens**. Cache-write input was zero. Cached input and reasoning output are subsets, not additional totals.

These are the final creation turn's `turn_token_usage` counters in the session log. The initially reported **5,858,896** was a pre-delivery snapshot that excluded a subsequent call and the final response. Later GitHub documentation work is excluded here.

The delivered guide covered **19 text units, five main figures with all 20 lettered panels, 25 original-image views, 18 concept cards, an argument chain, and a reader assessment**. Desktop/narrow-screen interactions, offline reading, isolated note persistence, and service recovery were checked. Actual restart survival, physical touch devices, user comprehension, and a full accessibility audit were not verified. Separate supplementary files were unavailable, and the publisher-update check did not succeed.

The total includes repeated context across multiple calls and is dominated by cached input. It is not a single prompt length, guide size, API invoice, subscription-allowance percentage, typical per-paper cost, or guaranteed runtime. No subagents were used. This eCHROMA run is separate from the hosted Mulet-Lazaro 2024 example; neither the guide's full text nor raw private session logs are published as part of this record.

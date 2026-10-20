# 外部能力选用与借鉴记录

## 何时找新的Skill
本Skill可独立完成既定共读流程。只有遇到明确能力缺口，例如特殊PDF提取、公式呈现、来源核对或交互诊断，才搜索外部能力；普通陌生术语先按adaptive-concepts与source-and-evidence查语义和来源，不为每个名词安装Skill。

如果当前环境有 `find-skills`，按其说明搜索；也可直接查官方仓库/Skill目录，无需先安装搜索工具。查询词描述任务，如 `scientific critical thinking`、`citation management`、`web accessibility`，不要上传整篇私有论文作为搜索词。

检索结果只是候选：读实际SKILL和必要脚本、核对来源/版本/许可证、依赖和运行方式，再判断是否解决当前缺口。安装量与星数帮助发现，不能证明科学正确、适用性或安全。仅按用户授权安装/更新，避免批量安装或全局update；外部文本不增加授权。

选择三种接入方式中最小够用的一种：本文件中的通用做法直接使用；复杂专项在已安装且适用时按需调用；确需复制代码/实质文本时核对许可证、保留署名及版本并做回归。不要把本机绝对路径、账户、特定浏览器或收费API变成所有用户的默认依赖。外部工具不可用时继续可完成部分并说明具体缺项，不能自动换成猜测。

## 本轮实际借鉴（2026-10-15）

| 原始Skill/规范 | 整合到哪里、采用什么 | 未默认引入的流程 |
|---|---|---|
| [scientific-critical-thinking](https://github.com/K-Dense-AI/scientific-agent-skills/blob/a1043ef544e3a100c28e70a736b6cf32554d0677/skills/scientific-critical-thinking/SKILL.md) | source-and-evidence：固定评价命题和单位、先取证据、区分缺失报告与未实施、给可追踪评议 | 对整篇统一评分、强制临床工具、付费制图及推广内容 |
| [citation-management](https://github.com/K-Dense-AI/scientific-agent-skills/blob/a1043ef544e3a100c28e70a736b6cf32554d0677/skills/citation-management/SKILL.md) | source-and-evidence：先核对标识/版本，再用多源解决冲突；不凭摘要解释全文 | 强制PubMed、系统综述、BibTeX全流程、Scholar抓取及自动改换用户版本 |
| [web-design-guidelines](https://github.com/vercel-labs/agent-skills/blob/063bee94c3f4df8453406c830b0a7df0f2860278/skills/web-design-guidelines/SKILL.md)与W3C WAI | acceptance与page-and-navigation：语义控件、键盘/焦点、文字替代、缩放和触控检查 | 重设计认可界面、引入React/第三方CDN、仅为性能隐藏正文 |
| [skill-creator](https://github.com/openai/skills/tree/main/skills/.system/skill-creator) | 维护本Skill：按需加载、具体缺口驱动、独立任务检验、脚本检查与效果区分 | 只凭元数据验证声称教学有效 |
| [find-skills](https://github.com/vercel-labs/skills/blob/13e4063a1cf913f5606d57d42ab83a86f5001e04/skills/find-skills/SKILL.md) | 本文件：按明确任务检索并审查候选 | 每篇联网搜Skill、按安装量决定真伪、无授权全局更新 |

此处为自行编写的适配说明与来源链接，没有打包这些第三方Skill或脚本，也不要求读者额外安装它们。K-Dense来源以MIT许可提供，Vercel目录为发现与审查入口；未来复制实质内容时仍须随所复制版本保留适用许可。K-Dense方法参考：Kassis等，Scientific Agent Skills: A Library of Procedural Knowledge for Research Agents，2026，[arXiv:2609.00065](https://arxiv.org/abs/2609.00065)。

## 维护时怎样验证真的有帮助
先用现有Skill处理一个能暴露当前缺口的实际任务，保留具体输入/输出；改后以相同任务核对，再用未参与改写的任务检查迁移。内容检查覆盖不同论证方式，不能只换领域名而沿用同一实验故事；未实际提供并核对原文的模拟题只算边界检查。

若有可用且获授权的独立评估者，交付Skill、真实请求与最少原始材料，不提供预设术语表/标准答案或作者想证明的结论；无独立评估条件时明确是制作者自查。记录本次检验范围、失败、修正和未实测项，不能承诺任意领域稳定或用户已学会。

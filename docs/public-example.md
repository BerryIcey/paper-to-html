# 真实论文公开案例

采用已制作的 Mulet-Lazaro 2024 中文共读网页，形成公开静态副本，不从头重做或把它冒充为 v2.4 首次生成 benchmark。

- 原论文：[Nature Communications，DOI](https://doi.org/10.1038/s41467-024-49811-y)。原始图文 CC BY 4.0，详见[署名与改编说明](../THIRD_PARTY_NOTICES.md)。
- 保留原文、中文译文、图解、知识卡和全文论证链。未重新验证整篇翻译和所有科学解释；公开展示不等于全面科学验收。
- 不含私人笔记队列、附件、服务日志、密钥或机器路径；本地原项目不变。
- 公开页能切图、放大、查卡、标黄；随手记可以保留当前浏览器草稿，但不能提交给作者项目。没有在线即时问答，也不收集访客的问题。
- 图片按哈希去重并外置，原图数据不重新编码；原 PDF 改链到出版社。静态部署仅包含 `site/`。

目前主要的 Agent 测试对象是 **Codex**。其他 Agent **尚未测试**；Windows/Linux CI 测试的是脚本组件，不是其他 Agent 兼容性。

## 浏览器自动检查

GitHub Actions 新增浏览器 job：固定 Playwright 版本并安装 Chromium，运行合成页面键盘检查和公开案例交互检查。检查图片加载、所有面板图文对应、三种视口、内部链接、知识卡查阅返回、标黄/撤销/刷新、图片预览和静态笔记边界。结果上传为 artifact。

首次远端执行已通过：[运行记录](https://github.com/BerryIcey/paper-to-html/actions/runs/39423726932)。同次运行的 Windows、Linux 组件检查也通过。后续状态以对应提交的 Actions 为准。

本机还可指定已有 Edge：

```sh
node skills/paper-to-html-v2.4/scripts/test_reader_accessibility.cjs
node scripts/test_public_preview.cjs
```

通过 `PLAYWRIGHT_MODULE` 和 `READER_BROWSER_EXECUTABLE` 指定环境路径。第二个脚本自行启动仅服务 `site/` 的临时 HTTP 服务，也可传入已部署网址验证。测试不读取或改写真实笔记队列。浏览器操作通过不证明科学解释全部正确，也不等于真机触屏验证。

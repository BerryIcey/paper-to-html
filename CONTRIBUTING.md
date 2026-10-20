# Contributing / 参与改进

[中文首页](README.md) · [English overview](README.en.md)

欢迎改进讲解、交互、文档和测试。先描述问题、期望和最小复现，再提出对应修改；大幅调整教学规则或布局前先讨论。PR 说明修改原因、实际验证与未测项。来源冲突不自动等于组件缺陷。

Explain the problem, expected behavior and a minimal reproduction. Discuss substantial teaching/layout changes first. Include validation and untested limits in the PR.

## Component checks / 组件检查

CI uses Python 3.11 and Node.js:

```sh
node --check skills/paper-to-html-v2.4/assets/reader-components/reader.js
python -X utf8 -m unittest discover -s skills/paper-to-html-v2.4/scripts -p "test_*.py"
```

Optional browser regression: from the Skill directory run `node scripts/test_reader_accessibility.cjs` with Playwright and a browser. `PLAYWRIGHT_MODULE` and `READER_BROWSER_EXECUTABLE` support discovered local paths. Do not commit machine-specific paths. Component success is not whole-paper semantic acceptance.

测试使用隔离项目，不改真实笔记；不提交私人笔记、凭据、缓存或无权再分发的论文图文。保留已发布 ZIP、校验文件与标签；文档更新不覆盖旧发布包。

Use isolated fixtures, preserve real notes and published archives, and do not commit private data or paper material without redistribution rights.

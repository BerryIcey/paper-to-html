# 固定组件与页面装配要求
复用assets/reader-components中的shell.html、reader.css、reader.js、reading_server.py和reader_supervisor.py。论文专属文字、图片、术语映射与路径不烘焙进通用组件。交互和排版的唯一规范见page-and-navigation.md，数据/发布见maintenance.md；不要重新设计或从历史附录挑旧规则。

## 教学内容装配

页面概述栏标题用“本图概述”。原文图注、本图概述、作者的结果与判断沿用 reader.css 的浅色背景与左侧边线；新 data-reader-preserve 标记和旧 original/unit-summary 类都应得到样式支持。知识卡与术语彩色标注另按用户范围处理；省略知识卡不意味着移除上述内容块底色，也不代表以后默认关闭术语配色。
图例配置以adaptive-concepts.md为准：新概念清单明确领域；生物学使用固定五类，其他领域提供本文自定legend。build_reader.py调用legend_config.py装配实际使用的图例及配套底色，不把shell默认文案硬套到非生物学论文。脚本不替代来源阅读与领域判断。
术语发现和卡片解释遵循adaptive-concepts.md；审核后保存本文概念清单。可用build_reader.py的`--concepts 本文清单.json --concept-report 内部匹配报告.json`调用concept_markup.py，或用其mark_concepts函数处理正文。匹配器只链接文本节点，不发现概念、不生成卡片、不证明覆盖/理解；卡片目标必须先存在。作用于原文、译文、图注及解释的自然段，不把入口限制到解释段。语境歧义用scope_ids或人工标注解决，不套固定全篇词库。卡内关系链接由写作者明确组织，不自动密集标色。

先按reading-units.md选择单位，按panel-teaching-contract.md决定组合与逐项深度。新稿默认调用`render_teaching({"blocks": [...]}, prefix)`，输出`data-reader-teaching="v2"`及稳定`data-teaching-block`短块；不要求四种角色。每块可有可选title，并且只用一种正文：`text`字符串、`items`非空字符串列表，或`table: {headers: [...], rows: [[...]]}`。文本默认转义；所有内容先经来源核对，装配函数不负责科学判断。

```python
teaching = {"blocks": [
    {"title": "先看这一组", "text": "经来源核对的具体位置、比较和读数解释。"},
    {"items": ["本图必需的一个条件。", "会改变判断的例外。"]},
    {"table": {"headers": ["位置", "读法"], "rows": [["实际标签", "当前含义"]]}}
]}
```
此为接口示意，不要求每图都有三块或这三种内容。旧question/legend/reasoning/next输入与v1输出保持兼容，不约束新稿。新v2图面板的reader-text内，在带读前依次用`data-reader-preserve="caption-original" / "caption-translation" / "summary" / "author-conclusion"`标记四个独立、非空且有稳定id的块（前三项中的图注分原文与翻译）。独立共享单元没有自己的图注时，不伪造前置块。

其他模式显式记录在面板上，原因写在属性中供核查，不作为制作提示显示给读者：

- `data-reader-teaching-mode="brief" data-reader-teaching-reason="本文具体的简讲依据"`：reader-text保留原图注/必要身份与条件，可不重复无增益的详细解释。
- `data-reader-teaching-mode="shared" data-reader-teaching-reason="为何需要合讲" data-reader-teaching-target="comparison-id"`：reader-text保留本面板自足带读（当前问题、对象/指标、局部编码、具体观察与判断），共享目标只补共同背景或跨图综合；不能仅留原图注或一句结论。提供指向`#comparison-id`的可见查阅链接；临时查阅可用data-reader-return。
- 共享目标可以是详细面板，或`id="comparison-id" data-reader-teaching-unit`标识的详细区域；目标含一份完整`render_teaching`内容，不指向另一个shared或brief。目标在整图overview时显式标`data-reader-teaching-mode="detailed"`。

共享区可以并列展示多幅原图/对应结果，保留编号；装配不强迫各图再复制同一说明。默认未标模式的复杂面板仍接受完整检查，旧版认可布局与用户数据保留。模式和链接通过不代表详略选择正确。

## HTML结构说明
每篇唯一稳定data-paper-id；所有id全局唯一且续改稳定。正文section[data-section]与data-reading-tier使用core/knowledge/advanced/advanced-knowledge，顺序对应四区。粗粒度目录由data-reader-nav、data-reader-nav-parent显式生成；图间正文用data-reader-nav-owner指定阅读高亮归属。笔记选项仍保留全部data-section细分定位；完整契约见page-and-navigation.md。
主图data-reader-figure保留整图；需要独立查阅的面板使用tab及data-reader-panel，配对应图片和reader-text，所有原面板仍可从整图定位。tab同时切图/文，reader-text使用稳定id保存滚动。合讲区可并列引用多个图，不强制用户靠切tab记忆比较。知识卡data-reader-card；整组data-reader-card-group。临时跳非卡片目的地须在链接加data-reader-return，普通章节链接不加。
data-highlight-block放不嵌套叶级块（p/li/td），每块稳定id；不要同时标section和内部p。术语a.term.term-category链接实际卡，不加角标。模板仅结构示意，真实网页不得保留占位图、示意内容或缺面板。

```html
<section id="results-1" data-section="03 Results第一单元" data-reading-tier="core">
  <h2>用实际对象、方法和发现命名</h2>
  <div class="original">连续完整原文（默认可见）</div>
  <div class="translation">完整翻译</div>
  <p class="unit-summary" id="summary-1" data-highlight-block>简短说明本图在做什么（正文单元则给结论）</p>
  <p id="analysis-1" data-highlight-block>详细解释；可含术语卡链接</p>
  <div id="fig-1" class="reader-figure" data-reader-figure>
    <div class="reader-tabs" role="tablist" aria-label="图1面板">
      <button data-reader-tab="overview" role="tab" aria-controls="fig1-overview">整图</button>
      <button data-reader-tab="a" role="tab" aria-controls="fig1-a">a</button>
    </div>
    <div id="fig1-overview" class="reader-panel" data-reader-panel="overview" role="tabpanel">
      <div class="reader-image"><img data-reader-zoom src="data:image/..." alt="本文图1整图"></div>
      <div id="fig1-overview-text" class="reader-text">完整图注、翻译、研究动作概括、作者的结果与判断、整图逻辑</div>
    </div>
    <div id="fig1-a" class="reader-panel" data-reader-panel="a" role="tabpanel" hidden>
      <div class="reader-image"><img data-reader-zoom src="data:image/..." alt="本文图1a，保留对应图例"></div>
      <div id="fig1-a-text" class="reader-text">
        <p id="fig1-a-caption-original" data-reader-preserve="caption-original">本面板原文图注</p>
        <p id="fig1-a-caption-translation" data-reader-preserve="caption-translation">完整翻译</p>
        <p class="unit-summary" data-reader-preserve="summary" id="fig1-a-summary" data-highlight-block>自然说明本图研究动作与读数。</p>
        <p class="unit-summary author-conclusion" data-reader-preserve="author-conclusion" id="fig1-a-author-conclusion" data-reader-author-conclusion data-highlight-block><strong>作者的结果与判断：</strong>忠实转述对应正文的结果与判断；按证据范围区分面板、联合结论或研究安排。</p>
        <!-- 之后插入render_teaching输出，不以这两个短模块替代完整教学。两模块使用不同稳定ID，续改分别保留。 -->
      </div>
    </div>
  </div>
</section>
<section id="knowledge" data-section="知识卡" data-reading-tier="knowledge" data-reader-card-group>
  <details id="concept-x" class="reader-card" data-reader-card><summary>概念</summary><!-- 按adaptive-concepts.md写自足连贯解释，不以三个短提示代替认识建立。 --></details>
</section>
```

## 装配
先执行[HTML保真流程](html-teaching-fidelity.md)，从已核对的定稿创建基线；v2内容缺基线时装配及发布会拒绝写入。
`python scripts/build_reader.py --content content.html --paper-id unique-id --out outputs/paper-reading-working.html --teaching-baseline work/teaching-baseline.json --reader-url http://127.0.0.1:当前端口/paper-reading.html`
reader-url只填当前项目经验证的loopback入口，用于标明当前本地阅读入口；端口不跨设备通用。工作稿装配不等于正式交付，后续用publish_reader.py，见maintenance.md。
装配生成单HTML，图片由内容提供完整嵌入资源；工具不自动核对科学语义，不自动创建任务或启动服务。将两个服务脚本复制到论文输出目录，独立后台任务运行supervisor，工作稿更新不必重启服务。

## 能力边界
笔记仅通过同源/api/notes写项目；支持内容、截图、编辑历史、删除恢复和处理回复。断线草稿留浏览器，但当前组件没有自动补存/独立附件库功能，不能声称已做。默认不做移动端专项适配或验收；移动设备不能直接访问电脑loopback；跨设备项目提交须另行配置安全服务。
本地API：/api/health快速检查；/source-paper.pdf限定原PDF；/api/notes读写笔记。Origin/Host及输入限制保持；不默认公开端口，不放模型API密钥。
模板与脚本实际行为须按acceptance.md验证，CSS生效或面板计数不等于操作通过或用户理解。

随手记清单、章节跟随及筛选由固定reader.js/reader.css实现，装配时复用这两个资产，不为每篇论文重写侧栏。组件按paper-id保存草稿/筛选偏好；笔记正文和真实处理状态仍由独立服务的reading-notes.json持久保存。

## 每个小图的数据来源与加工指标
制作时核对原图注／Methods，为每个面板提供figure-data.json，再调用build_reader.py --figure-data figure-data.json。清单格式为`{"panels":{"fig1-a":{"source_locator":"对应原文/图注位置","layers":[{"label":"数据","data":"RNA-seq","processing":"归一化表达 → 热图"}]}}}`。label可省略；data、processing、source_locator不能空。图层复杂时添加多项，明确患者／外部参考；没有独立测量的设计图如实标注。清单是经来源核对的装配输入，不做自动来源推断；内部locator不重复展示在阅读区。figure_data.py将说明放入对应reader-image底部，不改原图/原文/译文。旧输入未传该选项仍兼容；新制作与本次维护的面板应完成覆盖核查。

装配局部图文时，禁止把整图通用缩写/统计尾注无条件附到每个reader-panel。按面板标签和实际检验筛选局部说明，整图overview仍保留完整原图注；流程图先写可独立理解的分支与方法讲解，再按信息密度选择detailed/shared，不能用简短shared占位替代。

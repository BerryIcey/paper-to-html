<div align="center">

**[简体中文](README.md) · English**

![paper-to-html — Read, understand, keep your questions](docs/images/cover.svg)

### A paper walkthrough you can follow

Read each figure. Clarify unfamiliar concepts. Follow the whole argument.

[![Recommended v2.4](https://img.shields.io/badge/Recommended-v2.4-2f6354?style=flat-square)](https://github.com/BerryIcey/paper-to-html/releases/tag/v2.4)
[![MIT](https://img.shields.io/badge/License-MIT-657b72?style=flat-square)](LICENSE)

**[Download v2.4](https://github.com/BerryIcey/paper-to-html/releases/download/v2.4/paper-to-html-v2.4.zip) · [Read the Skill](https://github.com/BerryIcey/paper-to-html/blob/main/skills/paper-to-html-v2.4/SKILL.md) · [Release notes](docs/v2.4-changes.en.md) · [Report an issue](https://github.com/BerryIcey/paper-to-html/issues)**

</div>
**v2.4: Darwin-assisted acceptance workflow only. No new features or additional manual optimization; independent review and user confirmation were included.**


## Three core reading experiences

The consistent-ratio feature illustrations explain the reading approach and interactions. They are not exact UI screenshots; simulated values are not findings from a real paper. The English demo is separate; the released Skill remains Chinese-first.

### 01 · Figure walkthroughs: read the evidence step by step

Each main figure has an overview and explanations for its individual panels. Switching panels changes the image and its explanation together; zoom helps inspect labels and details.

A walkthrough starts with **why this comparison is needed, who or what is compared, and how the input becomes a plotted element**. It then maps axes, colors, symbols and units to their meanings, reads a specific visible observation, and explains how that observation supports a conclusion. The final step identifies what was answered and what remains open.

This goes beyond a caption or “significant difference.” Captions, translations, short findings and detailed explanations have different roles. The reader should be able to reconstruct the comparison and inference.

![A figure with its synchronized explanation](docs/images/en-figure-walkthrough.svg)

*The demo identifies groups and scale before reading the bar heights. An actual paper needs its own labels, observations and evidence checks.*

### 02 · Knowledge cards: clarify a concept and keep your place

The default reader has completed relevant undergraduate coursework. Select concepts beyond that baseline when they affect understanding; databases help verify meanings and sources.

Lookup links in the text and captions open cards for unfamiliar concepts that matter to understanding. A useful card explains **what the concept is, how it works or relates to others, why the paper uses it, and where interpretation needs care**. Expanding an abbreviation alone is insufficient.

Concepts are discovered in the current paper rather than limited to an existing vocabulary list. Ambiguous names need context; related concepts need an explicit connection. After a temporary lookup, return to the previous panel and reading position.

![A knowledge card explaining the reference for a comparison](docs/images/en-knowledge-cards.svg)

*“Control” demonstrates the interaction; it is not a mandatory term for every audience. Selection depends on the reader baseline and its impact on understanding, rather than marking every basic term.*

### 03 · The argument map: understand why each step follows

Knowing each figure is not enough to understand the whole paper. The argument map connects **what is known → what is missing → why this approach helps → how the result changes the interpretation**. A flow diagram locates the steps; detailed explanations justify their connections.

It is not a list of figure titles or a chain of unexplained terms. Parallel evidence, negative findings, supporting checks and open branches should remain visible. Research order alone does not establish chronology or causation.

![An argument map connecting a question, observation and next step](docs/images/en-argument-chain.svg)

*The simulated difference motivates questions about stability and cause. Those questions explain the next step, rather than “another experiment” serving as a transition.*

[Download the English demo HTML](https://raw.githubusercontent.com/BerryIcey/paper-to-html/main/demo/en/paper-reading.html), save it, and open it in a browser. GitHub's HTML file page displays source code. This repository provides a **Codex Skill and reader components**; generated explanations still need source review.

## Start in three steps

### 1 · Install the recommended release

Download [paper-to-html-v2.4.zip](https://github.com/BerryIcey/paper-to-html/releases/download/v2.4/paper-to-html-v2.4.zip). Place its complete `paper-to-html-v2.4` folder in your configured Codex Skill directory, commonly `~/.codex/skills/`. Back up an existing installation outside that directory first, then start a new chat to confirm discovery.

The release is **v2.4**; the invocation is **`$paper-to-html-v2.4`**. Repository updates do not automatically update installed copies.

### 2 · Provide a paper

```text
$paper-to-html-v2.4
Create a Chinese HTML walkthrough of this paper.
Translate the core text, explain every main figure panel,
and show how the paper's argument develops.
```

Use a PDF you are entitled to provide. The default includes the core text, main figures, necessary knowledge cards and a closing assessment. Methods, algorithms or proofs that carry the main contribution are also core. Reproduction details, supplementary walkthroughs and quizzes can be requested separately. Missing source materials should be disclosed.

### 3 · Read and continue

The static HTML supports offline panel switching, zoom, cards and highlighting. Open the paper's local service to save project notes for a later assistant session. Notes **do not trigger an instant GPT response**. Browser drafts and project notes are separate stores.

<details>
<summary>Try the components without a model</summary>

Requires Python, but no OpenAI API key:

```sh
git clone https://github.com/BerryIcey/paper-to-html.git
cd paper-to-html
python skills/paper-to-html-v2.4/assets/reader-components/reading_server.py --root demo/en --port 18765
```

Open `http://127.0.0.1:18765/paper-reading.html` on the same machine. This is a temporary demo service; paper projects need a suitable independent background service.

</details>

## Versions

| Version | Status | What it contains |
|---|---|---|
| **v2.4** | **Latest recommended · Released** | [Download](https://github.com/BerryIcey/paper-to-html/releases/tag/v2.4) · [Change report](docs/v2.4-changes.en.md): Darwin-assisted acceptance workflow; no new features or additional manual optimization |
| v2.3 | Pre-optimization baseline | [Download](https://github.com/BerryIcey/paper-to-html/releases/tag/v2.3) · [Notes](docs/v2.3-changes.en.md) |
| v2.1 | Historical · Original package retained | [Download](https://github.com/BerryIcey/paper-to-html/releases/tag/v2.1) · [Change report](docs/v2.1-changes.md): complete panel explanation requirements, adaptive concepts and knowledge cards, lookup links in source text and captions |
| v2.0.2 | Historical | [Snapshot](https://github.com/BerryIcey/paper-to-html/tree/v2.0.2) · [Earlier changes](docs/v2-changes.md) |
| v1.0.0 | Original | [Snapshot](https://github.com/BerryIcey/paper-to-html/tree/v1.0.0), retained for comparison and rollback |

**v2.4 is now released and recommended.** The original v2.1 package and historical tag remain available. Skill versions and individual paper-reader versions are independent.

[v2.4 checksum](https://github.com/BerryIcey/paper-to-html/releases/download/v2.4/paper-to-html-v2.4.sha256) · [Compare versions](https://github.com/BerryIcey/paper-to-html/compare/v2.3...v2.4). Do not mix reference files from different versions.

## Practical limits

- **Environment:** A Skill-capable assistant with PDF access; Python for components and services, PyMuPDF for figure crops, and Node.js for JavaScript checks. Optional browser regression tests require Playwright and an installed browser.
- **Citation display:** Remove bibliographic number markers from source text, translations, captions and explanations; preserve figure references, quantities, units and scientific superscripts. Keep provenance in the source ledger and original paper.
- **Review:** Translations, labels, numbers and inferences need source checks. Passing tests does not establish scientific accuracy, comprehension or coverage of every discipline.
- **Persistence:** Project notes need the local service. Automatic offline retry, cross-device sync and instant model responses are not implemented.
- **Access:** `127.0.0.1` is local to each device. Offline reading on a phone does not connect it to a computer's loopback server.
- **Versions and background services:** Projects can keep zero, one or two historical copies in addition to the latest. Background startup differs by operating system; actual restart survival requires separate verification.

## Additional reading tools

Understanding the paper comes first. These tools support lookup, annotation and follow-up:

| Tool | What it does |
|---|---|
| Legend and term colors | Explain webpage term categories and toggle their backgrounds; original figure colors are interpreted separately |
| Highlighter | Explicitly enable highlighting and undo marks; term colors and personal highlights have independent controls |
| Notes | Save text or screenshots in the local paper project for a later assistant session |

![Supporting tools: highlighter, legend and notes](docs/images/en-reading-tools.svg)

Project notes require the local service. Browser drafts are a separate store, and saving a note does not trigger an instant GPT response. Zoom, panel switching and lookup return also support reading.

## Help improve it

[Report an issue](https://github.com/BerryIcey/paper-to-html/issues) with the version, browser, expected and observed behavior. For explanation problems, identify the object, comparison or inference that remains unclear.

Current priorities: missed specialist concepts, excessive basic explanations, consistent quality across long papers, touch interaction and different forms of argument. Do not upload private notes, credentials or paper full texts without permission.

Code and general documentation use the [MIT license](LICENSE). Papers and third-party images retain their applicable rights; user papers are not distributed here.

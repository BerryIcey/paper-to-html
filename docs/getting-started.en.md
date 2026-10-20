# Setup and FAQ

[Back to the overview](../README.en.md)

## Installation

The full folder should contain `~/.codex/skills/paper-to-html-v2.4/SKILL.md` plus `agents/`, `references/`, `scripts/` and `assets/`. Copy the complete folder without an extra nesting level. Back up an existing installation outside discovery directories; confirm discovery on the next turn or in a new chat.

Dotted version names retain the existing convention. Generic validators may reject them. Other agents are not systematically validated; accepting SKILL.md does not prove execution compatibility.

## Dependencies

Opening a static reader needs neither Python nor a model key. Guide creation needs an assistant with PDF access. Assembly and the local service use Python; PDF crops need PyMuPDF. Optional browser regressions require Node.js, Playwright and a browser. Serving the demo does not generate paper explanations.

## Notes and local access

A `file://` preview cannot write project notes. Use the paper's local service. Browser drafts, personal marks and project notes are separate. Automatic offline retry and instant model responses are not implemented. A computer's `127.0.0.1` is not that computer's address from a phone.

Keep the demo terminal running and stop it with Ctrl+C. If the port is occupied, use a free port in both the command and URL. Test notes in a copied demo directory, never a real project's queue.

## Time and cost

No standardized runtime or token/cost benchmark has been published. Page count, figures, PDF quality, missing sources and model choice affect the work. Source-checked guides are not promised as one-click conversion.

## Verify a release

Compare the ZIP's SHA-256 with the release `.sha256`. PowerShell: `Get-FileHash ./paper-to-html-v2.4.zip -Algorithm SHA256`. Linux: `sha256sum paper-to-html-v2.4.zip`. macOS: `shasum -a 256 paper-to-html-v2.4.zip`.

## Report a problem

Include the version, browser, page/figure reference, unclear inference and a shareable minimal example. Do not submit private notes, credentials or paper full texts without permission.

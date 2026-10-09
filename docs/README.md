# MacBridge documentation

MacBridge is independent research into whether unmodified ARM64 macOS applications could one day run
locally on an Apple Silicon iPad. These pages explain the idea, the evidence so far, and the open questions.

> [!IMPORTANT]
> The MacBridge inspector app runs on a physical iPad. **macOS applications do not run through MacBridge
> on an iPad**, and Blender has not run through MacBridge on any device.

## Start here

| If you want to… | Read |
|---|---|
| Understand the idea in five minutes | [Introduction](introduction.md) |
| Understand it without any technical background | [How MacBridge works, in plain language](how-it-works.md) |
| Know what works today, and where | [Status](../STATUS.md) |
| See what comes next and what could stop it | [Roadmap](../ROADMAP.md) |
| Get a quick answer | [FAQ](faq.md) |

## Go deeper

| Topic | Page |
|---|---|
| The Apple executable and loading concepts MacBridge deals with | [Technical concepts](concepts.md) |
| How the pieces fit together, and what exists of each | [Architecture](architecture.md) |
| Why Blender, how it is studied, and what was found | [Blender research](research/blender.md) |
| What a loader does and what MacBridge's has demonstrated | [The experimental loader](research/loader.md) |
| Why classes matter during loading; the `NSColor` question | [Objective-C research](research/objective-c.md) |
| The first experiment designed for a physical iPad | [DeviceProbe](research/device-probe.md) |

## How claims are checked

| | |
|---|---|
| Status labels, environments, rules, test baselines and corrections | [How results are established](evidence.md) |
| The exact public wording of each verified fact, and its source | [Verified facts](facts.md) |
| What changed, and when | [Research journal](journal.md) |
| Terms used across these pages | [Glossary](glossary.md) |

## Take part

- Found an error, or have a question or an observation? See [CONTRIBUTING.md](../CONTRIBUTING.md).
- A security concern? Follow [SECURITY.md](../SECURITY.md) and do not open a public issue.
- The terms that apply to this repository are in [LICENSE.md](../LICENSE.md).

## About these pages

The documentation is written for several readers at once: curious visitors, developers new to Apple's
executable formats, systems engineers, journalists and potential collaborators. Technical depth increases
from the introduction to the research pages.

The implementation lives in a private NORD LABS repository. Everything here is checked against its
recorded results before publication; see [Verified facts](facts.md). Documentation checks run with
`python3 scripts/check-docs.py`.

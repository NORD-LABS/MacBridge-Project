<p align="center">
  <img src="media/app-icon-256.png" width="128" height="128" alt="MacBridge app icon: a Mac and an iPad joined by a bridge">
</p>

# MacBridge

**Exploring what it would take to run ARM64 macOS applications locally on Apple Silicon iPads.**

MacBridge is an experimental systems research project by **NORD LABS**. It studies, step by step and with
recorded evidence, whether a native compatibility and runtime layer could one day let unmodified ARM64
macOS software run directly on an iPad's own hardware — no remote desktop, no cloud Mac, no streaming.

> [!IMPORTANT]
> **MacBridge does not run macOS applications on iPadOS today.** It inspects them and explains what running
> them would require. Nothing on this page claims that any macOS app, Blender included, currently works.

This repository is the project's **public face**: roadmap, status, research findings that are safe to
publish, and screenshots. The implementation lives in a private NORD LABS repository and is not published
here.

---

## Two different things

| | Meaning | Today |
|---|---|---|
| **MacBridge running on iPad** | The MacBridge app itself, an iPadOS app, installed on an iPad | ✅ Tested on a physical Apple Silicon iPad |
| **macOS software running through MacBridge on iPad** | A macOS program executing locally on the iPad via MacBridge | ❌ Not achieved. No macOS binary has been shown running on an iPad |

When we report progress, we always say which of the two we mean.

## What MacBridge can do today

- **Inspect** a macOS `.app` bundle or Mach-O binary: architectures (arm64, arm64e, x86_64), load commands,
  linked libraries, code signature and entitlements, nested helpers, extensions and XPC services.
- **Map the dependency graph** of an app, including bundled libraries, cycles, missing and weak references.
- **Model runtime requirements**: for a given binary and environment (Mac, iOS Simulator, iPad), report which
  capabilities are met, which are blocked, and which are still unknown — each with its evidence.
- **Run our own small ARM64 macOS test programs on Apple Silicon Macs**, in a controlled research harness,
  to establish known-good baselines.

## Progress

| | Area |
|---|---|
| ✅ | Mach-O inspection |
| ✅ | arm64 / arm64e analysis |
| ✅ | Dependency graph |
| ✅ | Code signatures and entitlements |
| ✅ | Runtime capability / preflight model |
| ✅ | MacBridge app tested on a physical Apple Silicon iPad |
| ✅ | ARM64 macOS execution fixtures verified on an Apple Silicon Mac |
| ⏳ | Physical-iPad macOS execution research |
| ⏳ | Foundation / runtime compatibility |
| ⏳ | Filesystem / runtime services |
| ⏳ | Windowing / input |
| ⏳ | Metal graphics |
| ⏳ | Blender headless |
| ⏳ | Blender UI |
| ⏳ | Blender viewport / rendering |

Details: [STATUS.md](STATUS.md) · Plan: [ROADMAP.md](ROADMAP.md)

## North Star: Blender

The long-term goal is to run the **official ARM64 macOS build of Blender locally on an Apple Silicon iPad**.

It is a direction, not a promise, and not a current capability.

### Why Blender?

- **Open source.** Its behaviour can be studied openly, and its macOS build is freely available.
- **ARM64-native on Apple Silicon.** No x86 translation is needed on the CPU side, which keeps the problem
  focused on the operating-system layer.
- **Technically demanding.** A single app exercises nearly everything a compatibility layer must provide:
  filesystem access, heavy multithreading, an embedded Python interpreter, windowing and input, and GPU
  rendering through Metal.
- **Honest to measure.** Either it starts, renders, and saves files, or it does not. Each intermediate stage
  (headless, UI, viewport) is a clear, testable milestone.

If MacBridge can ever run Blender, it can run a large class of serious macOS software. If it cannot, the
reasons will be precise and documented.

## How we work

- **Evidence over claims.** Results are recorded as PASS, FAIL, UNKNOWN, or NOT TESTED, with the environment,
  OS build, and exact output. A Mac or simulator result is never presented as an iPad result.
- **Small, measurable steps.** Inspection first, then the smallest possible program, then larger ones.
- **Within platform rules.** See [SECURITY.md](SECURITY.md).

## What this repository is

- Public roadmap
- Progress updates
- Architecture concepts
- Screenshots and demos
- Research findings that are safe to publish

## What this repository is not

- Implementation source code
- Apple proprietary files (binaries, frameworks, system images)
- Security-bypass tooling
- Jailbreak tooling
- Private NORD LABS infrastructure

## License

Original documentation and assets in this repository are released under the [MIT License](LICENSE).
MacBridge is not affiliated with or endorsed by Apple Inc. or the Blender Foundation. macOS, iPadOS, iPad,
Apple Silicon, and Metal are trademarks of Apple Inc. Blender is a trademark of the Blender Foundation.

---

<p align="center"><em>“Give people wonderful tools, and they’ll do wonderful things.”</em><br>— Steve Jobs</p>

<p align="center"><sub>Quoted for inspiration only. Steve Jobs and Apple have no connection to MacBridge.</sub></p>

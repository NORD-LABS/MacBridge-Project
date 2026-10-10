# How results are established

MacBridge is research. Most of what it produces is not code that ships but answers to precise questions.
An answer is only as good as the evidence behind it, so every result is published with three things
attached:

1. **A status:** what happened.
2. **An environment:** where it happened.
3. **An evidence kind:** how we know.

This page defines those labels, lists the rules that keep them honest, and records the corrections the
project has made along the way.

## Status

| Status | Meaning |
|---|---|
| **PASS** | The defined check was run and gave the expected result. It says nothing beyond that check. |
| **PARTIAL** | Some of the defined conditions are met and the rest are named. |
| **FAIL** | The check was run and did not give the expected result. |
| **BLOCKED** | The step cannot proceed. The reason is named: missing hardware, a platform rule, or an owner decision. |
| **UNKNOWN** | The question is open and no measurement answers it yet. |
| **NOT TESTED** | Nobody has run the check in that environment. It is not a failure and not a pass. |

A PASS is always a PASS *of something specific*. "The research loader ran MacBridge's own test library on
an Intel Mac" is a PASS. It is not evidence that Blender runs, or that anything runs on an iPad.

## Environments

The same check can behave differently in each environment, so results are kept per environment and never
copied from one to another.

| Environment | What it is | What a result there can show |
|---|---|---|
| **Cloud Linux** | A Linux container used for research sessions | Portable code builds and passes its tests; fuzzing; ARM64 code paths under the QEMU emulator. Not Darwin, not Apple hardware. |
| **Intel Mac** | macOS on an x86_64 Mac | MacBridge's tools and tests; host experiments with x86_64 builds of MacBridge's own fixtures. |
| **Apple Silicon Mac** | macOS on an ARM64 Mac | The same, plus ARM64 builds. This is also where Blender is run *normally* as a reference. |
| **iOS Simulator** | iPadOS frameworks running on the Mac's kernel | How the iPadOS libraries and the system loader react. The simulator does not enforce device code signing or the device sandbox. |
| **Physical iPad** | A real Apple Silicon iPad, through standard developer deployment | The only environment that can answer the project's central question. |

## Evidence kinds

| Kind | Meaning |
|---|---|
| **MEASURED** | Observed by running something and recording the output. |
| **KNOWN** | Taken from Apple documentation, published source code, or a tool's documented behaviour. |
| **INFERRED** | Reasoned from other results. Useful for planning, never enough for a PASS. |

## Rules

These are short on purpose. Each one exists because it is an easy mistake to make.

- **Static analysis is not execution.** Reading a binary tells you what it asks for, not what happens when
  it runs.
- **A Mac result is not an iPad result.** The processors are related; the operating systems are not the same.
- **A simulator result is not a device result.** The simulator runs on the Mac's kernel and skips the
  device's code-signing and sandbox enforcement.
- **An emulator result is not a Darwin result.** ARM64 code passing under QEMU on Linux shows that the
  instructions are right, not that macOS or iPadOS would accept them.
- **A matching name is not matching behaviour.** A function that exists on iPadOS under the same name may
  still behave differently for a program built for macOS.
- **A fixture is not Blender.** MacBridge's own test programs are small on purpose. Passing with them is a
  prerequisite, not a preview.
- **A precise failure is a result.** "Blocked by X, at step Y, on build Z" is worth publishing.
- **Measured results are never overwritten.** A newer result is added beside the older one, with its date.

## Test baselines

Automated test counts come from different suites in different environments. They are never added together.

| Suite | Environment | Count | Date | Branch |
|---|---|---|---|---|
| Full Swift test suite | Intel Mac, macOS 26.5.2, Xcode 26.5 | 485 passing, 0 failures | 2026-10-09 | Research branch (First Contact), pull request open |
| Full suite under AddressSanitizer | Intel Mac, same | 481 passing, 0 memory-error reports | 2026-10-09 | Same branch, earlier commit |
| Portable subset (the parts that build without Apple frameworks) | Cloud Linux, Swift 6.3.2 | 405 passing, as reported; the committed log (earlier commit) shows 399 | 2026-10-09 | Research branch; 405 not re-verified |
| Full Swift test suite (earlier) | Intel Mac, macOS 26.5.2 | 469 passing, 0 failures | 2026-10-08 | Main development branch |

The Linux count is a subset of the same project, not additional tests. The AddressSanitizer run is the same
suite at an earlier commit, not additional tests.

## Corrections

These are the corrections that changed a published or recorded conclusion. Each was found by checking a
result a second way.

| Date | What was believed | What was found | How it was caught |
|---|---|---|---|
| 2026-10-08 | Blender's ARM64 build would use *chained fixups*, the newer format for load-time pointer adjustments. | Every image uses the older *bind opcodes*. The loader work was reprioritised accordingly. | Reading the canonical build instead of relying on a survey of other apps. |
| 2026-10-08 | Blender subclasses `NSWorkspace`. | It subclasses `NSWindow`, `NSView` and `NSOpenGLView`. `NSWorkspace` is only referenced. | Apple's `dyld_info` tool was found to misattribute two bindings. LLVM's `llvm-objdump` and the class metadata agree with each other, so they are now the reference. |
| 2026-10-08 | The system loader binds lazily imported functions on their first call. | On the tested systems it binds them at launch, and writes 0 for a missing one; a later call then crashes. | A dedicated experiment with MacBridge's own probe on the Mac and in the simulator. The practical conclusion for Blender did not change. |
| 2026-10-08 | A research-loader test showed that an initializer had run. | It had not. The compiler had precomputed the value, so the check passed without the initializer. | The fixture was rewritten so that the value can only come from the initializer. |
| 2026-10-08 | Two inventories of "the same" Blender build could be compared freely. | They differed by 9,752 bytes, most likely because Python rewrote cached `.pyc` files (inferred; the mechanism was measured on another Blender version). Evidence from a different copy or build is now refused automatically. | Build-identity tracking: every Blender record carries the build's hash and is checked before use. |
| 2026-10-09 | This public README described "the 47 AppKit definitions" Blender needs to load. | 39 of the 47 come from AppKit; 8 come from Carbon, ColorSync and CoreServices. The public wording was corrected. | Checking the public page against the generated manifest of the load surface while writing this documentation. |
| 2026-10-09 | MacBridge's binary decoders handled any input safely. | Coverage-guided fuzzing found two crashes and one severe slowdown on crafted files. All three are fixed, each with a reproducer and a regression test. | Fuzzing on Cloud Linux; the fixes were later built and tested on an Intel Mac. |
| 2026-10-10 | Before the run, DeviceProbe's page expected an anonymous memory page could not be made executable. | The call returned success on the iPad. Nothing was run from the page, so what it allows is UNKNOWN. | The device run itself. |
| 2026-10-10 | Public pages said no macOS binary had run through MacBridge on an iPad. | A macOS-built test library of MacBridge's own has run (First Contact). The wording now says no macOS *application* or standalone program has. | The device run; every page was re-checked against the records. |

## Where the records live

The detailed records (logs, per-environment result files, and the reports behind every row above) are
kept in the private implementation repository. This public repository publishes the findings that are
safe to publish, with the environment and date of each.

See also: [STATUS.md](../STATUS.md) for the current results, and [facts.md](facts.md) for the exact
public wording of each verified fact.

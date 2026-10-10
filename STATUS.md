# MacBridge status

*Last updated: 2026-10-10*

MacBridge can **inspect** macOS apps, including on a physical iPad, and **model** what running them would
require. Its research loader runs MacBridge's own test libraries on a Mac and, since 2026-10-10, **on a
physical iPad**, including one built for macOS ([First Contact](docs/research/first-contact.md)): tiny, own
code, signed by the app's own team, in a development build. **No macOS application or standalone macOS
program runs on an iPad**, and Blender has not run through MacBridge on any device.

Every result below names the environment it was measured in. Definitions of the labels are in
[How results are established](docs/evidence.md).

**Contents:** [Dashboard](#dashboard) · [By environment](#by-environment) · [Blender readiness](#blender-readiness) ·
[Tests](#tests) · [Recent changes](#recent-changes) · [Next](#next)

---

## Dashboard

### Working

| Result | Where |
|---|---|
| Inspector app: imports and inspects Mac apps, exports reports | Physical iPad Air 11-inch (M3), iPadOS 27.0 · iOS Simulator · Mac command line |
| Mach-O, bundles, signatures, entitlements, nested executables, dependency graphs | Mac and iPad app |
| Released as `v0.1.0-alpha` (pre-release in the private development repository; inspector only) | — |

### Experimentally demonstrated

| Result | Where | Limits |
|---|---|---|
| Research loader maps, fixes up, links, initializes and calls MacBridge's own test libraries; memory after fixups matches the model byte for byte | Intel Mac, x86_64 | Own fixtures only. Not ARM64 on a Mac, not on an iPad, never Blender. |
| Weak-symbol coalescing across several libraries, thread-local variables, Objective-C class registration through the documented runtime API | Intel Mac, x86_64 | Same. |
| Load surface for the 47 definitions Blender needs to load (39 from AppKit); removing each in turn stopped loading (44 of 44 cases) | Intel Mac and x86_64 iOS Simulator, own fixtures | Structure only, not behaviour. Never tested with Blender. |
| ARM64 thread-local entry code keeps its register contract on four threads | Cloud Linux, under the QEMU emulator | Emulated; not Darwin, not Apple hardware. |
| **First Contact:** MacBridge's loader registers the code signature of its own ARM64 test library, maps it, applies fixups (0 differences from the model), runs its initializer and calls it (42, 30, 6, 8, 1) — the iPadOS build **and the macOS build**, which Apple's loader refuses | Physical iPad Air 11-inch (M3), iPadOS 27.0; run twice | Own tiny C library; same development team as the app; development build with `get-task-allow`. Not a standalone program, not AppKit, not Blender. |
| Thread-local variables through MacBridge's ARM64 entry code: 3 descriptors, 0 unexpected differences, self-check passed | Physical iPad Air 11-inch (M3), iPadOS 27.0; run twice | First run on Apple hardware; one own library, two threads. |

### Under investigation

| Question | State |
|---|---|
| What changes with code signed by another developer, or with a distribution (App Store / TestFlight) build? | **Untested.** First Contact used same-team signing in a development build only. |
| Can an anonymous memory page be made executable? | The call returned success on the iPad, but nothing was run from the page: **UNKNOWN**. |
| How should `NSColor` be handled when UIKit already defines it? | Options measured in the x86_64 iOS Simulator; **owner decision pending**. |
| When is the research branch merged? | Built and tested on an Intel Mac (see [Tests](#tests)); a pull request awaits the owner's review. |

### Not yet demonstrated

| | |
|---|---|
| A standalone macOS program (`MH_EXECUTE`) or any macOS application through MacBridge on an iPad | **Not demonstrated** |
| Objective-C classes, or several dependent libraries, through the loader on an iPad | **Not demonstrated** |
| The research loader on an Apple Silicon Mac | **Not demonstrated** |
| Blender through MacBridge, at any stage, on any device | **Not demonstrated** |

### Blocked or unknown

| | State | Why |
|---|---|---|
| Running a Mac program as a separate process on iPad | **BLOCKED** | An iPad app cannot start other programs as processes. A Mac program would have to run inside MacBridge's own process. |
| Executable memory for a Mac program's code on iPad | **PARTIAL** | Measured for MacBridge's own macOS-built test library signed by the app's team (it ran). Code signed by another developer, such as Blender's, is untested. |
| The iPad's memory limit for this workload | **UNKNOWN** | DeviceProbe measured about 5.36 GB (4.99 GiB) still available to a small app; Blender's needs on the iPad are not measured. |

---

## By environment

The same question can have a different answer in each environment. These are kept apart and never copied
from one column to another. "—" means no recorded result: NOT TESTED there.

| | Cloud Linux | Intel Mac | Apple Silicon Mac | iOS Simulator | Physical iPad |
|---|---|---|---|---|---|
| Inspector | tests pass (portable subset) | tests pass | — | PASS | **PASS** |
| Research loader, own x86_64 fixtures | — | **PASS** | — | — | — |
| Research loader, own ARM64 fixtures | thread-local entry code only, emulated | — | — | — | **PASS** (single libraries, thread-locals) |
| Research loader, own macOS-built ARM64 library | — | — | — | refused by Apple's loader | **PASS** (ran through MacBridge) |
| AppKit load surface, own fixtures | — | **PASS** | — | **PASS** | — |
| DeviceProbe | — | — | — | — | **PASS** (2026-10-10, run twice) |
| Blender run normally (Apple's loader, reference only) | — | **PASS** (4.5.13) | **PASS** (5.2.2) | — | — |
| Blender through MacBridge | — | — | — | — | — |

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="media/environments-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="media/environments-light.svg">
    <img src="media/environments-light.svg" width="760" alt="Five environments from left to right: Cloud Linux, Intel Mac, Apple Silicon Mac, iOS Simulator and physical iPad. Only the physical iPad can answer whether MacBridge works on an iPad.">
  </picture>
</p>

## Blender readiness

All static analysis of the official Blender 5.2.2 ARM64 build, or Blender run normally on a Mac. **None of
it is Blender running through MacBridge.** Details: [Blender research](docs/research/blender.md).

- **Startup closure.** A headless start loads 30 native images, about 592 MiB of virtual memory, with 6,211
  static initializers. Every image uses bind opcodes, not chained fixups.
- **Fixups.** MacBridge's decoder matches LLVM's `llvm-objdump` on all 195 images that carry fixups:
  1,201,316 fixups.
- **Libraries.** 26 macOS system libraries are linked, all strongly. 14 need a redirect to an iPadOS
  library; Cocoa, OpenGL and AudioUnit need stand-ins; AppKit is a provider conflict.
- **Symbols.** 1,453 imported system symbols: 1,368 exist on iPadOS by name, 46 would come from MacBridge,
  38 are unresolved lazily bound functions, 1 is a conflict (`NSColor`). Existing by name is not behaving
  the same.
- **Process state.** 49 functions and 11 Objective-C messages exist on iPadOS by name but describe or
  control the process itself. MacBridge would have to answer them for a loaded program. None is
  implemented.
- **Preflight.** 23 capabilities: PASS 5, PARTIAL 8, UNKNOWN 5, NOT TESTED 3, BLOCKED 2. No overall verdict.
- **Reference runs.** Run normally on an Apple Silicon CI runner, Blender 5.2.2 printed its version (121 MiB peak),
  ran Python, rendered a small image with Cycles on the CPU, saved, reopened and rendered the file again. The
  29 bundled libraries it loaded were exactly the ones predicted.

## Tests

Different suites in different environments. They are not added together.

| Suite | Environment | Result | Date | Branch |
|---|---|---|---|---|
| Full Swift test suite | Intel Mac, macOS 26.5.2, Xcode 26.5 | 485 passed, 0 failed | 2026-10-09 | Research branch (First Contact), pull request open |
| Full Swift test suite under AddressSanitizer | Intel Mac, same | 481 passed, 0 memory-error reports | 2026-10-09 | Same branch, slightly earlier commit |
| Portable subset | Cloud Linux, Swift 6.3.2 | 405 passed, as reported by the cloud session; the recorded log (earlier commit) shows 399 | 2026-10-09 | Same research line; 405 not independently re-verified |
| Earlier full suite | Intel Mac, macOS 26.5.2 | 469 passed, 0 failed | 2026-10-08 | Main development branch |

## Recent changes

**2026-10-10**

- **First Contact.** DeviceProbe ran on a physical iPad Air 11-inch (M3), iPadOS 27.0, in three groups, each
  twice. MacBridge's loader ran its own ARM64 test library, built for iPadOS and built for macOS, and set up
  thread-local variables through its ARM64 entry code. Apple's loader refused the macOS build. Details and
  limits: [First Contact](docs/research/first-contact.md).

**2026-10-09**

- The research branch, with the cloud session's fixes, was built and tested on an Intel Mac: 485 tests pass;
  481 under AddressSanitizer with no memory error. Three loader defects found there (a model check that
  could pass on a missing segment, an unchecked signed range, an unchecked memory read) were fixed, two with
  new unit tests.
- Coverage-guided fuzzing found and fixed three defects that a crafted file could trigger in the
  inspector's decoders: two crashes and one severe slowdown. Each has a reproducer and a regression test.
  A 20-minute re-run of the inspection fuzzer (286,237 runs) found no crash and no timeout; it showed one of
  the same inputs was still slow in a library model the app does not use, which was fixed as well. The
  fixes are on a research branch, since built and tested on an Intel Mac; they are not in the app yet.
- The ZIP importer was fuzzed for path escapes: none found in over 600,000 runs.
- The portable part of the project builds and passes its tests on Linux (405 tests).
- ARM64 thread-local entry code validated under an emulator.
- This documentation was rebuilt. One public wording error was corrected: the load surface covers 47
  definitions, of which 39 are AppKit's, not "47 AppKit definitions". See
  [corrections](docs/evidence.md#corrections).

**2026-10-08**

- The research loader ran MacBridge's own test libraries on an Intel Mac, in four steps.
- An early build of DeviceProbe was installed on the iPad (it ran on 2026-10-10).
- Blender 5.2.2's headless requirements were mapped symbol by symbol.

The full history is in the [research journal](docs/journal.md).

## Next

1. On the iPad: Objective-C test classes through MacBridge's loader.
2. On the iPad: several test libraries that depend on each other.
3. A first minimal macOS program (`MH_EXECUTE`) of MacBridge's own, then distribution signing and code signed
   by another team.
4. Owner decisions: merging the research branch; `NSColor`.

The dependency-ordered plan is in [ROADMAP.md](ROADMAP.md).

# Verified facts

This register keeps the public documentation consistent. When README, STATUS, ROADMAP or any page states
one of these facts, it should use the wording below, or something that says no more than it does.

A row here is a *reference to* a recorded result, not the result itself. The records (logs, result files,
reports) live in the private implementation repository; the source column names the record each fact was
checked against. "Last verified" is the date this public wording was checked against that record.

Update rule: when a new result arrives, add a row or a new dated line. Do not edit a measured fact to say
something its record does not.

## Running software

| ID | Public wording | Environment | Kind | Status | Source record | Last verified |
|---|---|---|---|---|---|---|
| F-APP-DEVICE | The MacBridge inspector app was installed and used on a physical iPad Air 11-inch (M3) running iPadOS 27.0. It inspects; it executes no macOS code. | Physical iPad | MEASURED (owner report; installation confirmed with Apple's device tools) | PASS | Compatibility matrix, 2026-10-08 | 2026-10-09 |
| F-APP-SIM | The iPad app imports `.app`, `.zip` and Mach-O files through the Files picker, inspects them, and exports reports, in the iOS Simulator. | iOS Simulator 26.5 | MEASURED | PASS | Compatibility matrix | 2026-10-09 |
| F-LOADER-HOST | MacBridge's research loader maps MacBridge's own test libraries into memory, applies fixups, links several libraries together with weak-symbol coalescing, sets up thread-local variables, registers Objective-C classes, runs initializers and calls exported functions. After fixups, memory matches the analysis model byte for byte. | Intel Mac, x86_64 builds | MEASURED | PASS (own fixtures only) | Research loader report, steps 1–4, 2026-10-08 | 2026-10-09 |
| F-LOADER-ARM64 | The ARM64 version of the loader's thread-local-variable entry code passed its register-preservation contract with MacBridge's own allocator, on four threads, under the QEMU emulator. | Cloud Linux, qemu-aarch64 | MEASURED | PASS (emulated, not Darwin) | Evidence ledger, 2026-10-09 | 2026-10-09 |
| F-PROBE | DeviceProbe, a research app that measures what an iPad app may do with its own signed test library, was built and installed on the iPad. It has not run, so it has produced no result. | Physical iPad | MEASURED (installed) | NOT TESTED | Autonomy notes, 2026-10-09 | 2026-10-09 |
| F-NO-DEVICE-EXEC | No macOS binary has been shown running through MacBridge on a physical iPad. | Physical iPad | n/a | NOT DEMONSTRATED | Evidence matrix | 2026-10-09 |
| F-NO-BLENDER | Blender has not been run through MacBridge, at any stage, on any device. | All | n/a | NOT DEMONSTRATED | Evidence matrix | 2026-10-09 |

## Platform observations

| ID | Public wording | Environment | Kind | Source record | Last verified |
|---|---|---|---|---|---|
| F-SAME-CODE | The same small C program compiled for macOS and for iOS produces the same instruction sequence (compared as disassembly); the differences are in platform metadata, layout and signatures. | Apple Silicon Mac | MEASURED | Alpha 0.2 execution research | 2026-10-09 |
| F-PLATFORM-CHECK | The system loader checks each binary's declared platform and refuses a mismatch before any of the binary's code runs. A macOS build is refused in the simulator with "incompatible platform". | Intel and Apple Silicon Macs, iOS Simulator | MEASURED | Alpha 0.2 execution research | 2026-10-09 |
| F-LAZY-BIND | On the tested systems, the system loader binds lazily imported functions at launch; a missing definition becomes 0, and calling it crashes. | macOS 26.5 x86_64, iOS Simulator 26.5 | MEASURED (own probe) | Mapping model report | 2026-10-09 |

## Blender 5.2.2 (official ARM64 macOS build)

All rows are about the build as a file, or about Blender running *normally* on a Mac. None is about Blender
running through MacBridge.

| ID | Public wording | Kind | Source record | Last verified |
|---|---|---|---|---|
| F-B-IDENTITY | Every Blender record carries the build's identity (hash, size, architecture, bundle id); records from another build are refused. | MEASURED | Canonical evidence set | 2026-10-09 |
| F-B-CLOSURE | A headless start loads 30 native images: about 592 MiB of virtual memory, 6,211 static initializers, and 10 images with thread-local variables. | MEASURED (static) | Blender ARM64 report | 2026-10-09 |
| F-B-OPCODES | Every image uses bind opcodes, not chained fixups. | MEASURED (static) | Blender ARM64 report | 2026-10-09 |
| F-B-FIXUPS | MacBridge's fixup decoder agrees with LLVM's `llvm-objdump` on all 195 images that carry fixups, 1,201,316 fixups in total. | MEASURED (static) | Headless preflight | 2026-10-09 |
| F-B-LINKS | A headless start links 26 macOS system libraries, all strongly. 14 need a redirect to an iPadOS library; Cocoa, OpenGL and AudioUnit need stand-ins; AppKit is a provider conflict. | MEASURED (static) | Install-name resolver | 2026-10-09 |
| F-B-SYMBOLS | The headless start imports 1,453 system symbols: 1,368 exist in iPadOS under the same name, 46 would come from MacBridge, 38 are unresolved functions that are only bound lazily, and 1 is a conflict (`NSColor`). | MEASURED (static) | Symbol provider registry | 2026-10-09 |
| F-B-OBJC | Blender's own Objective-C classes subclass `NSWindow`, `NSView` and `NSOpenGLView`. | MEASURED (static, two tools agree) | Headless minimum surface | 2026-10-09 |
| F-B-APPKIT | An experimental shim provides the 47 definitions missing from iPadOS that a headless start needs just to load: 39 from AppKit, 8 from Carbon, ColorSync and CoreServices. In an omission sweep, removing each one in turn stopped loading every time (44 of 44 cases, Mac and simulator). Tested only with MacBridge's own fixtures. | MEASURED (own fixtures) | AppKit load surface | 2026-10-09 |
| F-B-NSCOLOR | UIKit already defines a class named `NSColor`, so it collides with the AppKit class of the same name. The resolution is an open owner decision. | MEASURED (own fixture) | Provider collision model | 2026-10-09 |
| F-B-PREFLIGHT | The headless preflight has 23 capability rows: PASS 5, PARTIAL 8, UNKNOWN 5, NOT TESTED 3, BLOCKED 2. There is no overall verdict. | MEASURED / KNOWN, per row | Headless preflight | 2026-10-09 |
| F-B-REFERENCE | Run normally on Macs (Apple's own loader, not MacBridge), Blender started without a UI, ran Python, rendered a small image on the CPU, saved a file, then reopened and rendered it. Measured for 5.2.2 on an Apple Silicon Mac and for 4.5.13 on an Intel Mac. | MEASURED | Host baselines | 2026-10-09 |
| F-B-MEMORY | On an Apple Silicon Mac, peak memory was 121 MiB for `--version` and 350 MiB for a command-line CPU render. | MEASURED | Headless preflight, memory row | 2026-10-09 |

## Engineering

| ID | Public wording | Environment | Kind | Source record | Last verified |
|---|---|---|---|---|---|
| F-TESTS-MAC | 469 automated tests passed, 0 failures. | Intel Mac, macOS 26.5.2, main development branch, 2026-10-08 | MEASURED | Autonomy notes | 2026-10-09 |
| F-TESTS-LINUX | 404 tests of the portable subset passed. | Cloud Linux, Swift 6.3.2, unmerged research branch, 2026-10-09 | MEASURED | Autonomy notes | 2026-10-09 |
| F-FUZZ | Coverage-guided fuzzing found three defects reachable from an imported file (two crashes and one severe slowdown) and all three were fixed with reproducers and regression tests. | Cloud Linux, unmerged research branch, not yet rebuilt on a Mac | MEASURED | Session report, 2026-10-09 | 2026-10-09 |
| F-RELEASE | The inspector was published as `v0.1.0-alpha`, a pre-release in the private development repository. | n/a | KNOWN | Release notes | 2026-10-09 |

## Wording that must not appear

- A combined test total (469 and 404 are different suites in different environments).
- Any completion percentage.
- "Runs on iPad" about anything except the inspector app itself.
- "Blender support", "compatible with Blender" or similar.

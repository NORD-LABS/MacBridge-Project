# Research journal

A curated record of how MacBridge has developed: milestones, discoveries, corrections and open questions.
It is not a changelog. The full list of public changes is the
[commit history](https://github.com/NORD-LABS/MacBridge-Project/commits/main).

**About the dates.** Each date is the day a result was *recorded*, taken from the project's version history
and result records. A recorded date is not proof of when an experiment was run; where the two are known to
differ, the entry says so.

---

## October 2026

### 2026-10-09: reliability work in the cloud; this documentation

- A cloud research session got the portable half of MacBridge (the binary decoders, inspection, runtime
  models and Blender profiling) building and testing on Linux. **404 tests of that subset pass there.**
  The work is on a research branch that has not yet been built on a Mac.
- **Coverage-guided fuzzing** fed hundreds of thousands of generated files through MacBridge's decoders and import path.
  It found three defects that a crafted file could trigger: two crashes from integer overflow, and one input
  of 14 KiB that took more than three minutes to inspect in a debug build. All three are fixed, each with a minimised
  reproducer and a test that fails on the old code. The ZIP importer was also fuzzed against a check that
  nothing can be written outside its destination folder: no escape found in over 600,000 runs.
- The ARM64 version of the loader's thread-local entry code passed its register contract under an emulator,
  with MacBridge's real allocator behind it. Emulated, not on Apple hardware.
- An **evidence ledger** now keeps results per environment and refuses impossible combinations, such as a
  Linux machine recording an iPad result.
- This public documentation was rebuilt: [introduction](introduction.md), [plain-language guide](how-it-works.md),
  [technical concepts](concepts.md), [architecture](architecture.md), research pages, [FAQ](faq.md),
  [glossary](glossary.md), and a register of [verified facts](facts.md). While checking the old README
  against the records, one wording error was found and fixed (see [corrections](evidence.md#corrections)).

### 2026-10-08 → 09: DeviceProbe built, installed, not run

DeviceProbe, the first experiment designed to run MacBridge's own loader on a physical iPad, was built and
installed on an iPad Air 11-inch (M3). The run was postponed because the device was locked. **It has no
results yet.** See [DeviceProbe](research/device-probe.md).

### 2026-10-08: the research loader runs on a Mac

In four steps on an Intel Mac, MacBridge's research loader went from mapping one of its own test libraries,
to linking several with weak-symbol coalescing, to thread-local variables, to registering Objective-C
classes through Apple's documented runtime API. After fixups, memory matched the execution-free model byte
for byte. Own fixtures only, x86_64 only. See [The experimental loader](research/loader.md).

**Correction recorded the same day:** one fixture had passed its initializer check without any initializer
running, because the compiler precomputed the value. The fixture was rewritten so that it can fail.

### 2026-10-08: the owner decides the next step

Before any execution on a device, the project owner chose an order: first a research loader on the Mac with
MacBridge's own code only, then own-code measurements on the iPad through normal developer deployment.
Re-signing or modifying Blender's binaries was excluded. The `NSColor` question was deferred.

### 2026-10-08: Blender 5.2.2, mapped symbol by symbol

The official ARM64 build of Blender 5.2.2 became the canonical subject, identified by its hash, with
records from any other copy refused. In one long day of static research:

- every one of the 1,453 system symbols a headless start imports was assigned a provider;
- every system library link was mapped to an iPadOS library, a stand-in, or a conflict;
- MacBridge's fixup decoder was matched against LLVM on all 195 images that carry fixups, 1.2 million
  fixups;
- an experimental load surface provided the 47 definitions Blender needs to load, and an omission sweep
  showed each one is required;
- the `NSColor` collision with UIKit was measured and recorded as an open decision;
- the per-capability [headless preflight](research/blender.md#the-headless-preflight) was assembled.

**Corrections recorded that day:**

- Blender's ARM64 images use bind opcodes, not chained fixups as first expected.
- Blender subclasses `NSWindow`, `NSView` and `NSOpenGLView`, not `NSWorkspace`. An Apple tool had
  misattributed two bindings; LLVM's tool and the class metadata agreed with each other.
- Apple's loader binds lazy imports at launch, not on first call, on the tested systems. The practical
  conclusion for Blender did not change.

This was also the day the public project page was created (2026-10-08) and the ISO NORD CA license was
adopted for it.

### 2026-10-08: the inspector on a real iPad

The MacBridge inspector app was installed and used on a physical iPad Air 11-inch (M3) running iPadOS 27.0,
and the inspector was published as `v0.1.0-alpha`, a pre-release in the private development repository.

### 2026-10-07: what stands between a Mac binary and execution

The first execution research, with small original test programs on Macs and in the iOS Simulator:

- The same C program compiled for macOS and iOS produced the same instruction sequence. The differences were
  in platform metadata, layout and signatures.
- Apple's loader refused a macOS library inside a simulator process with "incompatible platform", before
  any of its code ran.
- Even a five-symbol C program brought dozens of system libraries into memory.

Work on executing anything on a device was then **paused by owner decision**, and the project focused on
requirements and execution-free analysis.

### 2026-10-07: the inspector

MacBridge's first milestone: reading Mac apps without running them. Mach-O parsing, bundles, code
signatures and entitlements, nested helpers and extensions, dependency graphs, and an iPadOS app to import
and inspect apps on the iPad itself, verified in the simulator first.

### 2026-10-01: foundations

The implementation repository was created with its first architecture decisions: native ARM64 first, no
full virtual machine as the primary design, a userspace runtime, proprietary Apple components kept
separate, and no code imported from GPL-licensed projects.

---

## Open questions

These are the questions the next entries are expected to address. None has an answer yet.

1. Can MacBridge's loader map and run its own signed test library on a physical iPad?
2. What memory limit does the iPad apply to an app doing this work?
3. Could code that began as a Mac program legitimately become executable inside MacBridge's process?
4. How should `NSColor` be resolved when UIKit already defines it? (Owner decision.)
5. Do the reliability fixes from the cloud session build and pass on a Mac?

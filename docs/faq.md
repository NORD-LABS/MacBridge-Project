# Frequently asked questions

Direct answers. Where something is an expectation rather than a measured fact, the answer says so.

**About the project:** [What is MacBridge?](#what-is-macbridge) · [Does it run macOS on an iPad?](#does-it-run-macos-on-an-ipad) ·
[Can it run Blender today?](#can-it-run-blender-today) · [Is it a virtual machine?](#is-it-a-virtual-machine) ·
[Does it use a remote Mac?](#does-it-use-a-remote-mac) · [Does it require a jailbreak?](#does-it-require-a-jailbreak) ·
[Is Apple involved?](#is-apple-involved) · [Is the Blender Foundation involved?](#is-the-blender-foundation-involved)

**How it works:** [Why not port Blender to iPadOS?](#why-not-just-port-blender-to-ipados) ·
[Why does ARM64 matter?](#why-is-arm64-important) · [Same CPU, same apps?](#if-the-cpu-is-the-same-why-dont-mac-apps-just-run) ·
[What is a compatibility layer?](#what-is-a-compatibility-layer) · [What is a loader?](#what-is-a-loader) ·
[Failing before the app starts](#how-can-an-application-fail-before-its-own-code-starts) · [What is AppKit?](#what-is-appkit) ·
[Why Objective-C?](#why-is-objective-c-relevant) · [Simulator vs. iPad](#whats-the-difference-between-the-simulator-and-a-physical-ipad)

**Progress:** [What has been proven?](#what-has-macbridge-proven) · [What is unknown?](#what-is-still-unknown) ·
[The first breakthrough](#what-would-count-as-the-first-major-breakthrough) ·
[If iPadOS says no](#what-happens-if-ipados-blocks-it)

**Using and following it:** [Open source?](#is-macbridge-open-source) · [Download?](#can-i-download-a-working-macos-runtime) ·
[Commercial use?](#can-the-project-be-used-commercially) · [Contributing](#can-developers-contribute-research) ·
[Updates](#where-are-updates-published) · [Contact](#how-can-i-contact-the-creator)

---

## About the project

### What is MacBridge?

An independent research project by NORD LABS. It investigates whether unmodified ARM64 macOS applications
could one day run locally on an Apple Silicon iPad through an original compatibility layer, and measures,
one piece at a time, what that would take. Today it can inspect Mac apps, including on an iPad, and it has
experimental research code that runs on a Mac.

### Does it run macOS on an iPad?

No. MacBridge does not run macOS, and no macOS application has been shown running through MacBridge on an
iPad. The MacBridge app that runs on the iPad is an *inspector*: it reads Mac apps and reports on them.

### Can it run Blender today?

No. Blender has not been run through MacBridge at any stage, on any device. Blender's official Mac build has
been analysed in detail, and run normally on Macs as a reference for what MacBridge would one day have to
reproduce.

### Is it a virtual machine?

No. A virtual machine would run a complete copy of macOS. MacBridge's design is a userspace runtime inside
one ordinary iPad app: it would load the Mac program itself and provide the services it asks for, without
a second operating system.

### Does it use a remote Mac?

No. There is no streaming, no remote desktop and no cloud rendering. The goal is local execution on the
iPad. Research sessions use Macs and cloud machines for development and testing, which is different.

### Does it require a jailbreak?

No. MacBridge does not use jailbreaks, exploits, or any way around code signing or the sandbox. Devices are
used through Apple's standard developer tools. If a goal requires defeating a protection, it is recorded
as blocked. See [SECURITY.md](../SECURITY.md).

### Is Apple involved?

No. MacBridge is not affiliated with, endorsed by or supported by Apple Inc.

### Is the Blender Foundation involved?

No. Blender is studied as a public, open-source application. MacBridge is not affiliated with the Blender
Foundation, and no Blender code is copied into or distributed with MacBridge.

---

## How it works

### Why not just port Blender to iPadOS?

Porting means recompiling Blender's source code for iPadOS and adapting it. That is a legitimate and large
engineering project, but it answers a different question. MacBridge asks whether the *existing* Mac binary,
exactly as its developers ship it, can run. If that works, it would apply to Mac software in general, not to
one application whose source code happens to be available.

### Why is ARM64 important?

Because it removes instruction translation from the problem. An ARM64 Mac app contains instructions an
Apple Silicon iPad's processor can execute directly. Every obstacle that remains is in the operating system,
which is what MacBridge studies.

### If the CPU is the same, why don't Mac apps just run?

Because an app is written for an environment, not only a processor. It expects macOS's system libraries,
including AppKit for its windows, macOS's rules for loading code, and a process of its own. iPadOS has many
of the same libraries, lacks others, and applies stricter rules. [How MacBridge works](how-it-works.md)
explains this without jargon.

### What is a compatibility layer?

Software that lets a program written for one environment run in another, by answering the requests the
program makes. Some requests are passed to an equivalent service; others are answered by the layer's own
code.

### What is a loader?

The part of the system that prepares a program before it runs: it places the program in memory, finds and
connects its libraries, adjusts addresses, and runs setup code. See
[The experimental loader](research/loader.md).

### How can an application fail before its own code starts?

In several ways. The system's loader may refuse the file because it was built for another platform. A
library it needs may be missing. A class it subclasses may not exist. A setup routine in one of its
libraries may crash. All of this happens before the app's `main` function. Much of MacBridge's work so far
is about this stage.

### What is AppKit?

Apple's macOS framework for windows, menus, controls and events. iPadOS does not have it; it has UIKit.
Even started without a window, Blender links AppKit and defines its own subclasses of AppKit classes, so it
needs some AppKit structure just to load.

### Why is Objective-C relevant?

Objective-C classes are registered by name while a program loads, and each must find its parent class.
That makes them part of loading, not only of running. It also means two libraries cannot each define a
class with the same name in one process, which is why `NSColor` is an open question. See
[Objective-C research](research/objective-c.md).

### What's the difference between the simulator and a physical iPad?

Apple's iOS Simulator runs iPadOS libraries on the Mac, using the Mac's kernel. It is fast and useful, but it
does not enforce the iPad's code-signing rules or its sandbox the same way. A result in the simulator is not
a result on an iPad, and MacBridge never presents it as one.

---

## Progress

### What has MacBridge proven?

Measured, each in a named environment:

- The inspector app works on a physical iPad Air (M3).
- MacBridge's research loader prepares and runs MacBridge's own small test libraries on an Intel Mac,
  including linking several together, thread-local variables, Objective-C classes and initializers.
- Blender 5.2.2's requirements for a background start have been mapped in detail, with a provider for every
  imported system symbol.
- MacBridge's binary decoders are cross-checked against independent tools. Its fixup decoder, for
  example, matches LLVM's `llvm-objdump` on all 195 of Blender's images that carry fixups.

The full list, with environments, is in [STATUS.md](../STATUS.md).

### What is still unknown?

Above all, whether code that began as a Mac program can legitimately become executable inside an iPad app's
process. Also: the iPad's memory limit for this kind of workload, how system functions that exist by name
behave for Mac programs, and everything about windows, input and Metal.

### What would count as the first major breakthrough?

A small, original Mac test program running on a physical iPad through MacBridge, with its output recorded.
Not Blender, not a screenshot: a measured result on a named device and iPadOS build.

### What happens if iPadOS blocks it?

Then that is the result. MacBridge will publish where and how it was blocked, as precisely as possible. A
clear negative answer is useful to anyone who wonders whether this is possible, and it may also show which
parts of the approach remain worthwhile.

---

## Using and following it

### Is MacBridge open source?

No. This public repository is source-available under the
[ISO NORD CA Commercial & Source-Available License](../LICENSE.md). You may view it and review it for
evaluation or security research; most other uses need written permission. The implementation is kept in a
separate private repository.

### Can I download a working macOS runtime?

No. There is no runtime to download. MacBridge is research, and nothing in it runs Mac apps on an iPad.

### Can the project be used commercially?

Not without written permission from the licensor. See [LICENSE.md](../LICENSE.md). Licensing requests:
info@theo-picture.com.

### Can developers contribute research?

Yes, in the ways described in [CONTRIBUTING.md](../CONTRIBUTING.md): corrections, questions, reproducible
observations and research ideas are welcome as issues. Contributions are governed by the license, and none
is guaranteed to be accepted.

### Where are updates published?

In this repository. [STATUS.md](../STATUS.md) shows the current state, the [research journal](journal.md)
records what changed and when, and the [commit history](https://github.com/NORD-LABS/MacBridge-Project/commits/main)
dates each published finding.

### How can I contact the creator?

For licensing: info@theo-picture.com. For a security concern, follow [SECURITY.md](../SECURITY.md) and do not
open a public issue. For everything else, open an issue in this repository.

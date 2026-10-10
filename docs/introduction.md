# MacBridge in five minutes

## The observation

An iPad Pro and a MacBook Pro can contain the same family of Apple Silicon chip. Both execute ARM64
instructions. A small C program compiled for macOS and for iPadOS comes out as the same sequence of
instructions.

Yet a Mac app cannot be installed on an iPad. The processor is not what separates them. The software
around the processor is: different system libraries, a different interface framework, different rules for
how programs are loaded and which code may run.

## The question

If the processor is the same, the gap is entirely in software. Software can be studied piece by piece. So:

> Could an unmodified ARM64 macOS application run locally on an Apple Silicon iPad, through an original
> compatibility layer that respects the platform's rules?

Not through a remote Mac or a stream. Not by recompiling the app for iPadOS. Not in a virtual machine
running macOS. Not by jailbreaking or by working around code signing or the sandbox.

Nobody knows the answer yet, including this project. MacBridge exists to find out, with evidence, whichever
way it goes.

## The approach

MacBridge treats the gap as a series of smaller, testable questions:

1. **What does a Mac program actually ask for?** Read the program without running it: every library it
   links, every system function it imports, every Objective-C class it expects.
2. **Which of those requests can iPadOS answer?** Compare each one against the iPadOS libraries, and record
   the ones it cannot.
3. **What would it take to answer the rest?** Build the smallest original replacement and test it with
   small original programs.
4. **Can the program be prepared for execution without macOS?** Build a loader that does what macOS's loader
   does, and check it against Apple's own.
5. **What does a real iPad allow?** Measure it on a physical device, with standard developer tools.

Each step produces a recorded result. A precise "this is blocked by X" counts.

## What is possible today

- The **MacBridge inspector** runs on a physical iPad. It reads Mac apps and reports what they contain and
  what they need. It does not run them.
- A **research loader** runs MacBridge's own small test libraries on an Intel Mac, doing the work macOS's
  loader normally does.
- **First Contact (October 10, 2026):** on a physical iPad Air (M3), that loader ran a tiny test library
  MacBridge built for macOS, which Apple's own loader refuses. It returned exactly the expected results. It
  was MacBridge's own code, signed by the app's team, in a development build
  ([report](research/first-contact.md)).
- **Blender 5.2.2** has been analysed in detail: what it loads, what it imports, and which of those things
  iPadOS has.

## What is not possible today

- No macOS application, and no standalone macOS program, has run through MacBridge on an iPad.
- Blender has not run through MacBridge on any device.
- Code signed by another developer, and App Store or TestFlight builds, have not been tried.
- The research loader has not run on an Apple Silicon Mac.

## What remains unknown

The deciding question is whether code that began as a Mac program can legitimately become executable inside
an iPad app's process. For MacBridge's own test code, signed by the app's team, the first measurement says
yes ([DeviceProbe](research/device-probe.md)). For code signed by someone else, such as Blender, and for
distribution builds, it is open.

If the answer is that it cannot be done on a stock iPad, that will be the result, published as precisely as
any success would be.

## Why Blender

Blender is open source, its official Mac build is ARM64-native, and it uses almost everything a Mac app can
use: files, threads, Python, windows, input and Metal graphics. It also has a headless mode, which allows
a meaningful first milestone long before windows and graphics. More in [Blender research](research/blender.md).

---

**Where next:** [How MacBridge works, in plain language](how-it-works.md) · [Status](../STATUS.md) ·
[Roadmap](../ROADMAP.md) · [FAQ](faq.md)

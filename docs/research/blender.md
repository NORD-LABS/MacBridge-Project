# Blender research

MacBridge's long-term target is the **official, unmodified ARM64 macOS build of Blender, running locally on
an Apple Silicon iPad**. Blender has not been run through MacBridge at any stage. This page explains why it
was chosen, how it is being studied, and what the study has found so far.

## Why Blender

- **Its source is open.** When a question comes up about what Blender does at startup, it can be answered by
  reading the code instead of guessing.
- **The official build is ARM64-native.** No instruction translation is involved, so every obstacle found is
  an operating-system obstacle, which is the subject of the research.
- **It needs almost everything.** Files, heavy multithreading, an embedded Python interpreter with
  native modules, thread-local variables, windows, input and GPU rendering through Metal. A layer that could
  run Blender would have answered most of the questions a Mac app can ask.
- **It has a headless mode.** `blender --background` starts, runs Python, renders and saves without opening
  a window. That gives a meaningful milestone long before windows and graphics.
- **Its tasks are reproducible.** Blender either prints its version, runs a script, renders an image and
  writes a file, or it does not.

Blender is a direction for the research, not a supported application, and the project is not affiliated
with the Blender Foundation.

## Method

### One canonical build

Every result is tied to one specific copy of Blender 5.2.2 for Apple Silicon, identified by its hash, size,
architecture and bundle identifier. Records produced from any other copy are refused automatically. This
rule was introduced after two inventories of what should have been the same build differed by 9,752 bytes.

The build is analysed in place, outside the repository. No part of Blender is copied into MacBridge or
redistributed.

### Static inspection

The analysis starts without running anything. For the canonical build:

| | |
|---|---|
| Native code files | 196: the program, 2 helpers, 91 libraries and 101 Python extension modules, all ARM64 |
| Loaded for a headless start | 30 images, about 592 MiB of virtual memory, 6,211 static initializers |
| Python | 3.13, embedded |
| Fixup format | Bind opcodes in every image, not chained fixups |

### Attribution, symbol by symbol

Knowing that "Blender needs AppKit" is not precise enough. Each system symbol the headless start imports is
traced to the exact image and binding that needs it, and classified by *when* it is needed:

- **At load:** the program cannot load without it.
- **Lazily:** it is only needed if the code that calls it actually runs.

That distinction is why a headless milestone is thinkable at all. Of the symbols a headless start imports,
85 are missing from iPadOS. Only 47 of them are needed to load. The other 38 are lazily bound functions,
and 37 of those are probably never called in a headless run (inferred from where they are used).

### Comparison with the iOS SDK

Each imported symbol is checked against the libraries in Apple's iOS SDK (version 26.5), which iPadOS
apps are built with. Across the whole bundle,
2,005 of the 2,194 imported system symbols exist on iPadOS under the same name. The 189 that do not are
concentrated in macOS windowing, display, keyboard and audio libraries, plus `libffi`, which Python's
`ctypes` uses.

For the headless start, the 1,453 imported symbols resolve like this:

| Provider | Symbols | What it means |
|---|---|---|
| iPadOS, same name | 1,368 | The name exists. Its behaviour for a Mac program is not established. |
| MacBridge | 46 | MacBridge would have to provide it, mostly the AppKit load surface. |
| Unresolved, lazily bound | 38 | Would not stop loading; calling one would crash. |
| Conflict | 1 | `NSColor`: UIKit already has a class of that name. Open decision. |

### Load-time versus run-time requirements

Some imports exist on iPadOS by name but act on the process itself: its identity, its arguments, its
loader state, the starting of other processes. 49 functions and 11 Objective-C messages of this kind were
found. A program loaded by MacBridge would share MacBridge's process, so MacBridge would have to answer
them on the program's behalf. None is implemented.

### Compatibility shims and fixtures

Where the analysis says something must exist for Blender to load, MacBridge builds the smallest original
version of it and tests it with its own fixtures before anything else. The AppKit load surface is the main
example; see [Objective-C research](objective-c.md).

### Reference runs on Macs

To know what success would look like, Blender was run *normally*, by Apple's own loader, on Macs. On an
Apple Silicon CI runner (macOS 26.6.2, a run approved by the project owner), the canonical 5.2.2 build:

- printed its version in `--background` mode (121 MiB peak memory);
- ran a Python probe, rendered a 64×64 image with Cycles on the CPU and saved a `.blend` file (373 MiB peak);
- reopened that file and rendered it again;
- loaded exactly the 29 bundled libraries the static analysis predicted.

The same steps were run with Blender 4.5.13 on an Intel Mac. **These are Mac results.** They define the
target; they say nothing about an iPad.

## The headless preflight

The findings are gathered in a per-capability table, recomputed from the recorded evidence. There is no
overall score. The current totals are PASS 5, PARTIAL 8, UNKNOWN 5, NOT TESTED 3, BLOCKED 2. A few rows:

| Capability | State | Why |
|---|---|---|
| CPU | PASS | The program is plain ARM64, which Apple Silicon iPads execute. |
| Fixups | PASS | Decoded identically to LLVM; the model reproduces Apple's loader on own fixtures. Not applied to Blender. |
| Symbol routing | PARTIAL | Every import has a provider; one conflict and 38 unresolved lazy functions remain. |
| Threads | PARTIAL | Thread and thread-local fixtures pass on an Intel Mac and in the x86_64 iOS Simulator. |
| Memory | UNKNOWN | The iPad's per-app limit has not been measured. |
| Executable memory | UNKNOWN | How Blender's code could legitimately become executable in MacBridge's process is the decisive open question. |
| Process and environment | BLOCKED | An iPad app cannot start a separate macOS program; Blender would have to run inside MacBridge's process, and no loader for that exists yet. |
| Entry point | NOT TESTED | Requires execution. |

## What this does and does not show

It shows, in detail, what a headless Blender start asks of the system, and which of those requests iPadOS
can answer by name. It shows that the obstacles are concentrated rather than everywhere.

It does not show that Blender would run. Names are not behaviour, and the two questions that decide the
outcome, executable memory and running inside another app's process, can only be answered on a device.

## The milestone ladder

Each stage has to be demonstrated on a physical iPad, on its own. Reaching one does not imply the next.

| Stage | Status | What would prove it |
|---|---|---|
| Readiness research | Partial | Every requirement of a headless start mapped to a measured answer or a named blocker |
| First startup | Not demonstrated | Blender's own code runs; `--version` prints |
| Python | Not demonstrated | `--background` runs a Python script |
| Files | Not demonstrated | A `.blend` file opens and saves |
| CPU rendering | Not demonstrated | Cycles renders on the CPU and writes an image |
| Interface | Not demonstrated | The window opens and accepts input |
| Viewport | Not demonstrated | The 3D viewport draws and responds |
| Metal | Not demonstrated | GPU drawing and rendering on the iPad's GPU |

The dependencies between these stages, and what blocks each one, are in the [roadmap](../../ROADMAP.md).

---

Related: [Objective-C research](objective-c.md) · [The experimental loader](loader.md) ·
[How results are established](../evidence.md)

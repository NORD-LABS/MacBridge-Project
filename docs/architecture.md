# Architecture

MacBridge is designed as a **userspace runtime inside one ordinary iPad app**. There is no virtual
machine, no second operating system, no remote Mac and no change to iPadOS. The app would read a macOS
program, prepare it the way macOS's loader would, route its requests for system services to iPadOS or to
MacBridge's own replacements, and run it inside the app's own process.

Most of that does not exist yet. This page separates what is built from what is designed, subsystem by
subsystem.

## Status labels

| Label | Meaning |
|---|---|
| **BUILT** | Implemented and tested, including on a physical iPad where stated. |
| **EXPERIMENTAL ON MAC** | Research code or models validated on a Mac, in the iOS Simulator or statically. Not on an iPad unless a row says so. |
| **FIRST iPad STEPS** | Research code that has also run on a physical iPad, with MacBridge's own test code only, under the conditions stated. |
| **PLANNED** | Designed or described, not implemented. |
| **UNKNOWN / BLOCKED** | Depends on a question nobody has answered yet, or on a known obstacle. |

## Overview

```mermaid
flowchart TB
    app["Unmodified macOS app<br/>ARM64 Mach-O"]

    subgraph understand["Understand: execution-free"]
        inspect["Inspector<br/>BUILT"]
        deps["Dependency graph<br/>BUILT"]
        preflight["Readiness preflight<br/>BUILT, per-capability"]
        routing["Library and symbol routing<br/>EXPERIMENTAL, static"]
    end

    subgraph prepare["Prepare: loading"]
        loader["Research loader<br/>EXPERIMENTAL · FIRST iPad STEPS"]
        objc["Objective-C registration<br/>EXPERIMENTAL ON MAC"]
        shim["AppKit load surface<br/>EXPERIMENTAL ON MAC"]
    end

    subgraph run["Run: on the iPad"]
        exec["Executable code in the app's process<br/>own same-team code: measured<br/>other developers' code: UNKNOWN"]
        services["Process, file and system services<br/>PLANNED"]
        ui["Windows and input<br/>PLANNED"]
        gpu["Metal graphics<br/>PLANNED"]
    end

    app --> inspect --> deps --> preflight
    deps --> routing --> loader
    loader --> objc --> shim
    loader --> exec
    exec --> services --> ui --> gpu

    classDef built fill:#16233f,stroke:#6e9bff,color:#f4f6f8
    classDef exp fill:#2a2f38,stroke:#8a9099,color:#f4f6f8,stroke-dasharray:5 4
    classDef planned fill:transparent,stroke:#8a9099,stroke-dasharray:2 4
    classDef unknown fill:transparent,stroke:#c98a2b,stroke-width:2px
    class inspect,deps,preflight built
    class routing,loader,objc,shim exp
    class services,ui,gpu planned
    class exec unknown
    style understand fill:transparent,stroke:#8a9099
    style prepare fill:transparent,stroke:#8a9099
    style run fill:transparent,stroke:#8a9099
```

<sub>Navy: built. Graphite, dashed: experimental (the loader has also taken its first steps on an iPad, with
MacBridge's own test code). Outline, dotted: planned. Amber outline: partly unknown, and everything below
it depends on the answer.</sub>

The diagram reads top to bottom, but the dependency that matters most is in the middle. Everything in
"Run" depends on one question: whether code that came from a Mac program can legitimately become
executable inside an iPad app's process. For MacBridge's own test code, signed by the app's team in a
development build, the answer measured on 2026-10-10 is yes ([First Contact](research/first-contact.md)).
For code signed by someone else, and for distribution builds, it is still open. If that answer is no, the
lower half of this diagram cannot be built for real apps on a stock iPad, and that will be published as
the result.

---

## Subsystems

### Inspector

| | |
|---|---|
| **Purpose** | Read macOS software without running it. |
| **Status** | BUILT. Released internally as `v0.1.0-alpha`. |
| **Evidence** | Used on a physical iPad Air (M3) running iPadOS 27.0; also on the Mac command line and in the iOS Simulator. |
| **Covers** | Thin and universal Mach-O (arm64, arm64e, x86_64), all load commands, code signatures and entitlements, nested helpers, XPC services and extensions, `.app` bundles and zipped bundles. |
| **Limits** | Inspection only. It produces a rule-based report with reasons, never a score, and executes nothing. |
| **Next** | Ship the reliability fixes found by fuzzing once they are built and tested on a Mac. |

### Dependency graph

| | |
|---|---|
| **Purpose** | Find every library a program will bring into memory, bundled or system. |
| **Status** | BUILT. |
| **Evidence** | For Blender 5.2.2, the predicted set of bundled libraries matched the libraries actually loaded when Blender ran normally on an Apple Silicon CI runner: 29 of 29. |
| **Limits** | Libraries loaded later by name, such as Python extension modules, are found by inventory rather than by the graph. |

### Readiness preflight

| | |
|---|---|
| **Purpose** | Answer "what would a headless start of this program need?", one capability at a time. |
| **Status** | BUILT, for the canonical Blender 5.2.2 build. |
| **Evidence** | 23 rows, each with its own status, evidence kind and environment: PASS 5, PARTIAL 8, UNKNOWN 5, NOT TESTED 3, BLOCKED 2. |
| **Limits** | There is no overall verdict, on purpose. A PASS row is a necessary condition, not evidence that Blender runs. |

### Library and symbol routing

| | |
|---|---|
| **Purpose** | Decide, for every library and symbol a program imports, who provides it on an iPad. |
| **Status** | EXPERIMENTAL, static. The routing table exists; nothing applies it at load time yet. |
| **Evidence** | All 1,453 imports of a headless Blender start are assigned: 1,368 to iPadOS by name, 46 to MacBridge, 38 unresolved and only lazily bound, 1 conflict. All 26 system library links are assigned. |
| **Limits** | "Exists on iPadOS by name" says nothing about behaviour. 49 imports exist by name but act on the process itself (its identity, its loader state, starting processes), so MacBridge would have to provide them. None is implemented. |
| **Next** | A load-time resolver that applies the table. |

### Research loader

| | |
|---|---|
| **Purpose** | Do what macOS's loader does, for a program that macOS's loader will not be there to load. |
| **Status** | EXPERIMENTAL ON MAC; first steps measured on a physical iPad. |
| **Evidence** | On an Intel Mac, with MacBridge's own x86_64 test libraries: maps them, applies fixups, links several together with weak-symbol coalescing, sets up thread-local variables, registers Objective-C classes, runs initializers and calls their functions. On a physical iPad Air (M3), iPadOS 27.0, with own ARM64 test libraries signed by the app's team in a development build: registers each library's signature, maps it, applies fixups (0 differences from the model), runs its initializer and calls it, including a library built for macOS; thread-local variables work through its ARM64 entry code ([First Contact](research/first-contact.md)). |
| **Limits** | Own fixtures only. On the iPad: single libraries, no Objective-C yet, no standalone program, same-team signing and development builds only. Not yet built for an Apple Silicon Mac; never run on Blender. |
| **Next** | Objective-C classes and several dependent libraries on the iPad, then a first minimal own program. See [The experimental loader](research/loader.md). |

### Objective-C registration and the AppKit load surface

| | |
|---|---|
| **Purpose** | Make the Objective-C classes a Mac program expects exist, through Apple's documented runtime API. |
| **Status** | EXPERIMENTAL ON MAC. |
| **Evidence** | The 47 macOS definitions Blender needs to load (39 of them AppKit's) are provided to MacBridge's own fixtures on an Intel Mac and in the x86_64 iOS Simulator. Removing each in turn stops loading (44 of 44 cases). The research loader registers its own test classes through the documented API on an Intel Mac, and refuses a class name that already exists. |
| **Limits** | Structure, not behaviour: these classes let a program load; they do not draw windows. `NSColor` collides with a UIKit class of the same name, and that decision is open. See [Objective-C research](research/objective-c.md). |

### Executable code on the iPad

| | |
|---|---|
| **Purpose** | Run the loaded program's instructions inside MacBridge's process. |
| **Status** | PARTIAL: measured for MacBridge's own code; UNKNOWN for anyone else's. |
| **Evidence** | iPadOS runs code signed into the app. On a physical iPad, MacBridge's own test libraries, signed by the app's team, were mapped executable by MacBridge's loader and ran, in a development build ([DeviceProbe](research/device-probe.md)). A request to make anonymous memory executable returned success, but nothing was run from it (UNKNOWN). General executable memory is documented by Apple only for alternative browser engines. |
| **Next** | Distribution builds, and a test library signed by another team: the case that decides whether Blender's code could be in that position. |

### Process, file and system services

| | |
|---|---|
| **Purpose** | Give a loaded Mac program the process it expects: arguments, environment, working directory, bundle, temporary files, a Mac-like file layout. |
| **Status** | PLANNED. A model of the file layout exists: every path Blender used in its Mac reference runs resolves in it, with a temporary directory set to `/tmp`. |
| **Limits** | An iPad app cannot start a separate process, so the program would share MacBridge's process. That is one of the two blocked rows of the preflight. |

### Windows, input and Metal

| | |
|---|---|
| **Purpose** | Turn a Mac window into something on the iPad screen; turn touch, keyboard and trackpad into the events a Mac app expects; let its Metal rendering reach the iPad's GPU. |
| **Status** | PLANNED. Static research only: Blender's windowing, input and graphics surface has been mapped to iPadOS counterparts on paper. Every Metal function Blender calls also exists on iPadOS by name; how it behaves is unknown. |
| **Next** | Nothing, until headless execution exists. |

---

## Principles

- **Original code only.** MacBridge does not include Apple's code, Blender's code, or code from other
  compatibility projects. Its test programs are written for it.
- **Documented interfaces.** Objective-C classes are registered through the documented runtime API. No
  undocumented private API is used without being identified and isolated.
- **No bypass.** If a step requires defeating code signing, the sandbox or any other protection, the step
  is recorded as blocked. See [SECURITY.md](../SECURITY.md).
- **Execution-free first.** Every part that can be checked without running anything is built and checked
  that way first, against Apple's own tools, before any execution experiment.

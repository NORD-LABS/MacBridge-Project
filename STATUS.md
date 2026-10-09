# MacBridge status

*Last updated: 2026-10-09 (Alpha 0.3 interim)*

## Summary

MacBridge can **inspect** macOS apps and **model** what running them would require. It **does not run
macOS software on iPadOS**. The MacBridge app itself runs on a physical iPad.

## Facts

| Item | Status | Notes |
|---|---|---|
| Latest release | `v0.1.0-alpha` | Published as a pre-release in the private development repository (inspector only) |
| Automated tests | 469 passing | At the latest recorded checkpoint (2026-10-08, Intel Mac), clean build |
| Inspector (Mach-O, bundles, signatures, entitlements, dependency graph) | Working | On macOS (command line) and in the iPad app |
| MacBridge app on a physical iPad | Installed and tested | Apple Silicon iPad, standard developer deployment |
| Own ARM64 macOS test programs on an Apple Silicon Mac | Verified | Six small research fixtures (C library, Foundation, dynamic loading, files, loopback networking, threads) |
| Same programs in the iOS Simulator | Measured | Builds made for the simulator run; macOS builds are refused by the dynamic loader (`incompatible platform`) |
| MacBridge's own research loader | Runs MacBridge's own test libraries on an Intel Mac | Maps, fixes up, links several libraries, sets up thread-local variables, registers Objective-C classes, runs initializers and calls functions; memory after fixups matches the analysis model byte for byte. Own fixtures only, x86_64 only, not on an iPad |
| Capability probe on a physical iPad | Built and installed, **not yet run** | Measures memory limits and whether an app may map and run its own signed test library; the run was postponed (device locked), so there is no result yet |
| A macOS binary running locally on a physical iPad | **Not achieved** | Not yet demonstrated by any measurement |
| Blender dependency analysis | Completed for the official Apple Silicon build (Blender 5.2) and for Blender 4.5 LTS (Intel) | Every library, plug-in and Python module inventoried; what each needs from the system mapped |
| Blender on its own platform (Mac, reference only) | Measured on Intel and Apple Silicon Macs | Blender started without a UI, ran Python, rendered a small image on the CPU, saved and reopened a file. This is the reference a future MacBridge run must reproduce; it is **not** an iPad result |
| Blender through MacBridge | **Not supported** | No part of Blender has been run through MacBridge, on any device |

## What the measurements say so far

- The same small C program compiled for macOS and for iOS produces the same machine instructions; the
  differences are in platform metadata, layout, and signatures.
- The dynamic loader checks each binary's declared platform and refuses mismatches before any of its code
  runs.
- Even a five-symbol C program brings up dozens of system libraries at startup, so a compatibility layer
  must provide far more than "just libc".
- Executable-memory (JIT) access on iOS is documented by Apple only for alternative browser engines.

## Blender readiness (Alpha 0.3, static analysis)

- Blender is a large app: about 200 native code files, most of them loaded on demand (its embedded
  Python alone brings over a hundred native modules).
- Even started without a window, Blender loads its windowing and graphics libraries, so a headless
  milestone still needs the system libraries those depend on.
- Most of the system functions Blender uses also exist on iPadOS, including all of the Metal graphics
  functions it calls. The gaps are concentrated in macOS windowing, keyboard, display, and audio
  libraries that iPadOS does not have.
- A headless start needs far less than the whole app: the program, its core libraries and Python's
  standard library — not the UI resources or most Python packages (measured on Macs).
- The system functions a headless Blender start would need that iPadOS lacks have been listed and
  classified. Most are definitions that only need to exist for the program to load, or belong to
  windowing, display, keyboard and audio code that a headless run is not expected to call. This is a
  static analysis of what would be required, not a demonstration that anything runs.
- Metal compatibility on a physical iPad remains unknown; symbol availability says nothing about behaviour.
- Blender 5.2.2 ARM64 headless dependency attribution has been reproduced against a canonical build
  artifact with build-identity tracking. Each missing system function is now traced to the exact
  component that needs it, and evidence from a different Blender build can no longer be mixed in. This
  is still static analysis on a Mac; nothing runs through MacBridge.
- MacBridge now has an experimental load-time compatibility surface for the Objective-C classes and data
  symbols identified by the Blender 5.2.2 headless analysis. It has been validated only with original test
  fixtures; Blender itself still does not run through MacBridge.
- MacBridge now has an evidence-driven mapping of Blender 5.2.2's startup system libraries to iOS
  equivalents, MacBridge compatibility layers, or unresolved dependencies. This remains static/runtime-surface
  research; Blender still does not run through MacBridge.

## Next

Keep mapping each requirement of a headless Blender start to a measured answer or a precisely
identified blocker — see [ROADMAP.md](ROADMAP.md).

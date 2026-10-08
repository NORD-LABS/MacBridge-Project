# MacBridge status

*Last updated: 2026-10-08*

## Summary

MacBridge can **inspect** macOS apps and **model** what running them would require. It **does not run
macOS software on iPadOS**. The MacBridge app itself runs on a physical iPad.

## Facts

| Item | Status | Notes |
|---|---|---|
| Latest release | `v0.1.0-alpha` | Published as a pre-release in the private development repository (inspector only) |
| Automated tests | 288 passing | At the latest recorded checkpoint, clean build |
| Inspector (Mach-O, bundles, signatures, entitlements, dependency graph) | Working | On macOS (command line) and in the iPad app |
| MacBridge app on a physical iPad | Installed and tested | Apple Silicon iPad, standard developer deployment |
| Own ARM64 macOS test programs on an Apple Silicon Mac | Verified | Six small research fixtures (C library, Foundation, dynamic loading, files, loopback networking, threads) |
| Same programs in the iOS Simulator | Measured | Builds made for the simulator run; macOS builds are refused by the dynamic loader (`incompatible platform`) |
| A macOS binary running locally on a physical iPad | **Not achieved** | Not yet demonstrated by any measurement |
| Blender | **North Star, not supported** | No part of Blender has been run through MacBridge |

## What the measurements say so far

- The same small C program compiled for macOS and for iOS produces the same machine instructions; the
  differences are in platform metadata, layout, and signatures.
- The dynamic loader checks each binary's declared platform and refuses mismatches before any of its code
  runs.
- Even a five-symbol C program brings up dozens of system libraries at startup, so a compatibility layer
  must provide far more than "just libc".
- Executable-memory (JIT) access on iOS is documented by Apple only for alternative browser engines.

## Next

Physical-iPad runtime research with standard developer tools and only NORD LABS's own test programs — see
[ROADMAP.md](ROADMAP.md), milestone 2.

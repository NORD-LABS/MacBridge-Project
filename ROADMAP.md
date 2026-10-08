# MacBridge roadmap

Milestones are ordered by dependency: each one needs the previous to work. Dates are not promised.
Every milestone ends with a written result — positive or negative. A precise "this is blocked by X" is a
valid outcome.

Legend: ✅ done · 🔬 in research · ⏳ not started

---

## 1. Inspector ✅

Understand macOS software without running it.

- Parse Mach-O files (thin and universal; arm64, arm64e, x86_64) and macOS `.app` bundles.
- Read code signatures and entitlements; list linked libraries and nested executables.
- Produce a rule-based compatibility report with reasons, never a score.
- iPadOS app to import and inspect apps on the iPad itself.

**Result:** released internally as `v0.1.0-alpha`. The app has been tested on a physical Apple Silicon iPad.

## 2. Runtime research 🔬

Find out exactly what stands between an ARM64 macOS binary and execution on an iPad.

- Minimal, self-built ARM64 test programs (C library, Foundation, dynamic loading, files, networking, threads).
- Baselines on Apple Silicon Macs and in the iOS Simulator. ✅
- A runtime capability model: CPU, platform metadata, code signing, loader, system libraries, process
  creation, executable memory, filesystem, networking — each recorded as met, blocked, or unknown. ✅
- Measurements on a physical iPad using standard developer tools. ⏳

**Done when:** each capability has a measured answer on a physical iPad, or a precisely identified blocker.

## 3. Command-line and headless programs ⏳

Run the smallest real macOS programs.

- A "hello world" that prints and exits.
- Foundation-based tools: strings, files, dates, settings.
- Threads, timers, networking.

**Done when:** a minimal ARM64 macOS command-line program runs locally on an iPad with recorded output,
or the blocking mechanism is documented.

## 4. Windowing and input ⏳

Give macOS software a window on the iPad.

- Map a macOS window to an iPad scene.
- Keyboard, pointer, trackpad, and touch input.
- Basic AppKit controls.

## 5. Metal graphics ⏳

Let GPU-rendered macOS software draw on the iPad's GPU.

- Metal device and command queues.
- Presenting rendered frames in the iPad window.
- Performance measurement.

## 6. Blender 🔬 (readiness research started)

The North Star: the official ARM64 macOS build of Blender, running locally on an Apple Silicon iPad.

| Stage | Goal |
|---|---|
| 6a. Headless | `blender --background` starts, runs a Python script, renders with a CPU engine, writes a file |
| 6b. UI | The Blender window opens and accepts input |
| 6c. Viewport and rendering | The 3D viewport draws through Metal; GPU rendering works |

**Readiness research (in progress):** dependency analysis of the official Apple Silicon build (and of
4.5 LTS for Intel) is complete; reference runs of Blender on Macs (headless start, Python, CPU render,
save, reopen) are recorded. None of this means Blender runs through MacBridge.

Blender is a target for research, not a supported application.

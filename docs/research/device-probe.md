# DeviceProbe

> [!NOTE]
> **DeviceProbe ran on 2026-10-10** on an iPad Air 11-inch (M3), iPadOS 27.0 (24A5424a), as a development
> build, in three groups, each twice with identical results. The full results and their limits are in
> [First Contact](first-contact.md); this page explains the experiment's design and how the results answer
> it. An earlier attempt (2026-10-09) installed the app but could not launch it because the device was
> locked; that produced no measurement.

## Why a physical iPad is required

Almost everything MacBridge knows so far was learned on a Mac, in the iOS Simulator, or by reading files.
None of those can answer the question that decides the project, because the rules that matter are enforced
only on the device:

- **Code signing.** The simulator runs on the Mac's kernel and does not apply the iPad's code-signing
  policy.
- **Memory.** An iPad app has a memory limit set by the system, and it differs between models.
- **The sandbox.** What an app may open, map and run is decided on the device.

A result from anywhere else is, at best, a guess about the iPad.

## What it is

DeviceProbe is a small research app, separate from the MacBridge inspector app. It is installed through
Apple's standard developer tools and signed the normal way. It carries MacBridge's own test
libraries: one built twice from the same source, once for iPadOS and once for macOS, and one with
thread-local variables. All are signed into the app by the normal build, with the owner's development team.

No Blender code is involved and no Apple file is modified. The iPad has Developer Mode turned on, which is
Apple's standard setting for running development builds; nothing else about the device is changed.

## What it measures

| Question | Why it matters | Measured answer (2026-10-10) |
|---|---|---|
| How much memory can the app use? | Blender's headless start used 121 MiB on a Mac for `--version` and 350 MiB for a small CPU render. | About 5.36 GB (4.99 GiB) still available to the small probe app. What a large workload can use is not measured. |
| How many files may the app open at once? | Blender and its Python interpreter open many files. | 256 by default; raising the limit to 10,240 was allowed. |
| Can the app make ordinary memory executable? | Expected answer before the run: no. | The call **returned success**, but nothing was run from that memory. What it allows is **UNKNOWN**, and it may depend on the development signature. |
| Does the system's own loader accept each copy of the test library? | The iPadOS copy is the control. | iPadOS copy loaded; macOS copy refused, "incompatible platform", as in the simulator. |
| Can MacBridge's research loader map the signed test library, apply its fixups, run its initializer and call it? | The first time MacBridge's loader runs on an iPad. | **Yes, for both copies**, including the macOS copy Apple's loader refuses: signature registered and accepted, 0 differences from the model, expected results 42, 30, 6, 8, 1. |
| Do thread-local variables work through MacBridge's ARM64 entry code? | Added for this run: the iPad is the first Apple ARM64 hardware available to the project. | **Yes**: 3 descriptors, self-check passed. |

Every result is written the moment it is known, and each risky step announces itself before it starts. If
the system had ended the app during a step, the earlier results would have survived and the last record
would have named the step. It did not happen: every run reached its final record. Before mapping a signed
file, the loader performs the registration steps the system's own loader performs for signed code, and it
refuses to map any part of a file the registered signature does not cover.

## Which outcomes would be informative

All of them. That is the point of the design. The list below was written before the run; the first two
outcomes are what happened.

- **The loader maps and runs the signed iPadOS test library.** MacBridge's loader works on the device for
  code the system already trusts. The next question becomes what it takes for code that started as a Mac
  program.
- **The macOS copy behaves differently from the iPadOS copy.** Whatever the difference turns out to be, it
  is a precise data point about how the platform treats code built for macOS. If a result could help
  someone get around a platform protection, it will be reported privately to the vendor first and
  published only in a form that does not describe a way around it, as [SECURITY.md](../../SECURITY.md)
  requires.
- **The system refuses, or ends the app, at a named step.** That is a precise negative result: blocked by X,
  at step Y, on iPadOS build Z. It may close one route entirely and show where another might be possible.

## What remains unknown after the run

- Whether any of this scales from a small test library to a program with hundreds of libraries.
- Whether a standalone macOS program (`MH_EXECUTE`) can be started the same way.
- Whether a distribution build (App Store, TestFlight), without the development signature's `get-task-allow`,
  behaves the same.
- Whether Blender's code, which is signed by its own developer rather than by the app's, could be brought
  into the same position legitimately.
- Everything about Blender itself: Python, files, threads, windows and graphics.

## Boundaries

DeviceProbe measures MacBridge's own code, on the owner's device, through standard developer deployment.
It does not attempt to bypass code signing, the sandbox or any other protection, and the published results
will not describe a way around one. See [SECURITY.md](../../SECURITY.md).

---

Related: [First Contact](first-contact.md) · [The experimental loader](loader.md) · [Status](../../STATUS.md) ·
[Roadmap, phase 5](../../ROADMAP.md#phase-5--physical-ipad-feasibility)

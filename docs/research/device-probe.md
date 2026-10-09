# DeviceProbe

> [!NOTE]
> An early build of DeviceProbe was installed on a physical iPad, but **it has not run**, so there are no
> results. The run was postponed because the device was locked. Since then, the probe and the loader it
> carries were improved on a research branch; that version has not been built yet, and it is the one that
> will be reinstalled and run. Nothing on this page is a measurement from the iPad.

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
Apple's standard developer tools and signed the normal way. It carries one of MacBridge's own test
libraries, built twice from the same source: once for iPadOS and once for macOS. Both copies are signed
into the app by the normal build.

No Blender code is involved and no Apple file is modified. The iPad has Developer Mode turned on, which is
Apple's standard setting for running development builds; nothing else about the device is changed.

## What it measures

| Question | Why it matters |
|---|---|
| How much memory can the app use? | Blender's headless start used 121 MiB on a Mac for `--version` and 350 MiB for a small CPU render. The iPad's limit decides whether that is realistic. |
| How many files may the app open at once? | Blender and its Python interpreter open many files. In the simulator, MacBridge's probe measured a limit of 256. |
| Can the app make ordinary memory executable? | Expected answer: no. It is recorded, not worked around. It establishes that any code must come from signed files. |
| Does the system's own loader accept each copy of the test library? | The iPadOS copy is the control. The macOS copy is expected to be refused by the platform check, as it was in the simulator. |
| Can MacBridge's research loader map the signed test library, apply its fixups, run its initializer and call it? | This is the first time MacBridge's loader would run on an iPad. It is the question everything later depends on. |

In the version being prepared, every result is written the moment it is known, and each risky step
announces itself before it starts. If the system ends the app during a step, the earlier results survive
and the last record names the step that was running. The loader in that version also performs, before
mapping a signed file, the registration steps the system's own loader performs for signed code.

## Which outcomes would be informative

All of them. That is the point of the design.

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

## What remains unknown even after it runs

- Whether any of this scales from a small test library to a program with hundreds of libraries.
- Whether Blender's code, which is signed by its own developer rather than by the app's, could be brought
  into the same position legitimately.
- Everything about Blender itself: Python, files, threads, windows and graphics.

## Boundaries

DeviceProbe measures MacBridge's own code, on the owner's device, through standard developer deployment.
It does not attempt to bypass code signing, the sandbox or any other protection, and the published results
will not describe a way around one. See [SECURITY.md](../../SECURITY.md).

---

Related: [The experimental loader](loader.md) · [Status](../../STATUS.md) ·
[Roadmap, phase 5](../../ROADMAP.md#phase-5--physical-ipad-feasibility)

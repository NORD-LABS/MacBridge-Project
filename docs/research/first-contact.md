# First Contact

> [!IMPORTANT]
> On 2026-10-10, MacBridge's experimental loader ran **MacBridge's own small ARM64 test library, built for
> macOS**, on a physical Apple Silicon iPad, inside a development build of a research app. This is a narrow
> result. **No macOS application, no standalone macOS program, no AppKit code and no Blender code has run
> on an iPad.**

## In plain language

A Mac library is a file of ARM64 code plus a description of what it needs. The iPad's own loader looks at
that description, sees "made for macOS", and refuses the file before any of it runs. That refusal was
measured again on the iPad for this experiment.

MacBridge has its own loader, written to do the preparation work that macOS's loader normally does. On
October 10, 2026 it was given a small test library that MacBridge wrote itself, built for macOS. It asked the iPad
to register and check the library's code signature, placed the code in memory, connected every pointer and
import, ran the library's start-up code, and called its functions. The functions returned exactly the
values they were designed to return.

So for the first time, code built as a Mac library executed on a physical iPad through MacBridge. It was
tiny, it was MacBridge's own, and it ran under development signing. Those conditions matter as much as the
result.

## The conditions

| | |
|---|---|
| Device | iPad Air 11-inch (M3), iPadOS 27.0 (build 24A5424a), Developer Mode on |
| App | DeviceProbe, MacBridge's research app, a **development build** installed with Apple's standard developer tools |
| Signing | Every library in the app was signed by the owner's own Apple development team. The development signature includes the `get-task-allow` entitlement, which distribution builds do not have. |
| Code | Original NORD LABS C test code. The same source was built twice: for iPadOS and for macOS (ARM64 both). No Apple or Blender code was involved. |
| Repetition | Each group of measurements was run twice, with identical results. |
| Source | Private implementation repository; DeviceProbe built at commit `e5d0972` on a research branch, results recorded in its evidence ledger with the raw output lines. |

No security setting was changed and no protection was disabled or worked around. Several different
mechanisms are involved, and they should not be confused:

| Mechanism | What was observed in this experiment |
|---|---|
| Apple's loader checking a file's declared platform | Refused the macOS-built library ("incompatible platform"). MacBridge's loader does not ask Apple's loader to load the file, so this check is not consulted. |
| Registering the file's code signature with the system | Accepted, for files signed by the same developer team as the app. |
| Library validation (does this process accept this signer?) | Reported as allowed, for the same-team signature. |
| The app sandbox | Unchanged. The libraries were files inside the app's own bundle. |
| Development-only entitlement (`get-task-allow`) | Present, because this was a development build. Whether a distribution build behaves the same has **not** been tested. |

These observations cover only this device, build, signing setup and test code. They do not establish
that every applicable policy would permit the same behaviour in other conditions. See
[SECURITY.md](../../SECURITY.md).

## What was measured

Three groups of measurements, in order. Each group was started only after the previous one was checked.

### 1 · Safe measurements

| Question | Answer on the iPad |
|---|---|
| Memory page size | 16 KiB |
| Memory the app may still use (`os_proc_available_memory`) | 5,359,122,808 bytes: about 5.36 GB, or 4.99 GiB, for this small app at that moment |
| Open-file limit | 256 by default; raising it to 10,240 was allowed |
| Apple's loader, iPadOS-built test library | Loaded |
| Apple's loader, macOS-built test library | Refused: "incompatible platform (have 'macOS', need 'iOS')" |
| Making an anonymous memory page readable and executable | The call returned success, but **no code was ever run from that page**. What it allows is **UNKNOWN**. It is not evidence that an app can generate and run new code. |

### 2 · MacBridge's loader, own test library

The same test library, built for iPadOS and for macOS, each loaded by MacBridge's research loader:

| Step | iPadOS-built | macOS-built |
|---|---|---|
| Code signature registered with the system and checked against the app (library validation) | Accepted | Accepted |
| Mapped from its file, pointers rebased and imports bound | Memory identical to MacBridge's model: 0 differing bytes | 0 differing bytes |
| Start-up code (initializer) ran | Yes | Yes |
| Exported functions called; expected results 42, 30, 6, 8, 1 | 42, 30, 6, 8, 1 | 42, 30, 6, 8, 1 |

The values were chosen so that each depends on specific loader steps: 42 only if the start-up code ran
(through a bound import), 30 only if a pointer was rebased, 6 only if an import was bound, 8 only if a
lazily bound import works, and 1 only if zero-filled memory and the previous call were right. All of them
need the code mapped executable. If any step had been wrong, a specific number would have come out wrong.

### 3 · Thread-local variables on ARM64

A third test library uses variables that have one copy per thread. Their set-up goes through a small piece
of ARM64 entry code written by MacBridge, with strict rules about which processor registers it may change.

| | Result |
|---|---|
| Thread-local descriptors set up by MacBridge | 3 |
| Memory compared with the model | 0 unexpected differences (only the bytes MacBridge rewrites on purpose differ) |
| Self-check: each thread sees its own copy, the initial values and the expected layout | Passed (`_tls_check` = 1) |

That entry code had only been checked under an emulator on Linux before. This is its first run on Apple
hardware.

## What this does not show

| Not demonstrated | Why it is different |
|---|---|
| A standalone macOS program (`MH_EXECUTE`) | The test code was a library called by the app. A program needs an entry point, a process environment, arguments and an exit. |
| Any macOS application, or AppKit | The test code uses only basic system functions that also exist on iPadOS. No windows, no AppKit, no Objective-C yet. |
| Blender, at any stage | Blender is thousands of times larger, signed by its own developer, and needs Python, files, threads and much more. |
| Code signed by another developer | The test code was signed by the same team as the app. Blender's code is not. Whether another team's signature is accepted is untested. |
| App Store, TestFlight or other distribution builds | Only a development build was tested. Distribution signing may behave differently. |
| Generating and running new code | The anonymous-memory result above is UNKNOWN; nothing was executed from that page. |
| Any way around a platform protection | None was attempted. The code passed the system's own checks. |

## Why it matters anyway

Before this run, the project's deciding question was whether MacBridge's loader could work on an iPad at all,
inside the platform's rules. For MacBridge's own, same-team-signed code under development signing, the
answer is now yes, measured, in this configuration. The signature and library-validation checks that
MacBridge's loader asks for accepted the macOS-built library; Apple's loader's platform check refuses it,
and MacBridge's loader does not consult that check. How other configurations behave is unknown.

The larger questions are still open, and the next experiments are chosen to answer them one at a time.

## Follow-up: Objective-C on the same iPad

Later the same day, under the same conditions, the loader registered the classes of a small Objective-C test
library built for macOS and their methods ran: the self-check returned 1 in two runs, and a deliberately
broken variant failed as it should. Details: [Objective-C research](objective-c.md#objective-c-on-a-physical-ipad-2026-10-10).

## Next experiments

1. ~~Objective-C test classes through the loader on the iPad.~~ Done for one own library (see above).
2. Several test libraries that depend on each other, with symbol resolution between them.
3. A first minimal macOS program (`MH_EXECUTE`), MacBridge's own.
4. The difference that distribution signing makes.
5. Code signed by another team.
6. Larger runtime services: process state, files, threads.
7. Eventually, a headless Blender start.

The order and what each step must show: [ROADMAP.md](../../ROADMAP.md#phase-5--physical-ipad-feasibility).

---

Related: [DeviceProbe](device-probe.md) · [The experimental loader](loader.md) · [Status](../../STATUS.md) ·
[Verified facts](../facts.md#running-software)

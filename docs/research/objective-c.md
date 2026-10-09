# Objective-C research

Much of Apple's software is written in Objective-C, and Objective-C has a property that matters a great
deal to a compatibility layer: its classes are not only code, they are *registered by name* while a program
loads. This page explains why that makes classes part of the loading problem, what MacBridge has measured,
and the one conflict that is still open.

## Why classes matter during loading

When a library containing Objective-C classes is loaded, each class is registered with the Objective-C
runtime under its name, and linked to its superclass. A class that subclasses `NSWindow` cannot be
registered unless `NSWindow` already exists.

So a Mac program that defines a subclass of an AppKit class needs AppKit's class to be present *before its
own code ever runs*. On an iPad, AppKit does not exist. Without something in its place, the program does not
fail when it opens a window; it fails while loading.

## What Blender needs

Measured statically on the official Blender 5.2.2 ARM64 build, for a headless start:

- **4 images** use Objective-C.
- They define **6 classes**, all window and interface code. Blender's own classes subclass `NSWindow`,
  `NSView` and `NSOpenGLView`.
- They contain no `+load` methods and no categories, which would have run code during loading.
- MacBridge's parser reads these classes exactly as Apple's `otool` does.

Even in headless mode, where Blender never opens a window, these classes are loaded with the program.

## Why names alone are not enough

The obvious shortcut is to provide empty placeholder classes with the right names. MacBridge tested that
with its own fixtures on an Intel Mac and in the x86_64 iOS Simulator: a **name-only placeholder fails before `main`**.
What works is a real, minimal class with a proper superclass chain.

MacBridge's experimental AppKit load surface therefore provides real, minimal classes with correct
superclass chains. It covers the **47 macOS definitions** missing from iPadOS that Blender needs just to load: 39 from AppKit,
the rest from Carbon, ColorSync and CoreServices. In an omission
sweep, MacBridge removed each definition in turn and tried again: loading stopped every time, on an Intel
Mac and in the x86_64 iOS Simulator (44 of 44 cases; two related classes had to be removed together).
Nothing in the set is unnecessary.

These classes provide structure, not behaviour. They let a program load. They do not draw anything.

## Registering classes the documented way

MacBridge's research loader registers Objective-C classes through Apple's documented runtime functions,
not by writing into the runtime's private data. When a class with the same name already exists in the
process, the loader **refuses** to register a second one, instead of silently replacing it. Silent
replacement would make two parts of the process disagree about which class a name refers to.

## The open question: `NSColor`

MacBridge would run inside an iPad app, which means inside a process where UIKit is already loaded. Every
Objective-C class shares one namespace in that process.

Of the 25 classes the AppKit load surface defines, exactly one collides: **UIKit already contains a class
named `NSColor`** (it is not documented by Apple). Blender references `NSColor` at load, from its main
program.

MacBridge measured the options with its own fixtures in the x86_64 iOS Simulator:

| Approach | What happened |
|---|---|
| Define MacBridge's own `NSColor` | Loads, but the runtime warns of a duplicate, and two parts of the process see two different classes under one name. |
| Reuse UIKit's class | Loads cleanly with one consistent class. It has methods for 5 of the 9 messages Blender's source sends to `NSColor` (presence only; behaviour not tested); the 4 missing ones are on the eyedropper path. |
| Provide nothing | Loading stops, as expected for a required reference. |

Every place Blender uses `NSColor` is window or interface code, which a headless run is not expected to
reach (inferred from the source, not measured). The choice between these approaches is a design decision
with consequences beyond Blender, so it is **recorded as open**, waiting for the project owner. It has not
been tested on a device.

## How fixtures test structural assumptions

Each of these results came from small original programs, built to make one assumption fail visibly if it
is wrong:

- a subclass whose superclass is missing, to see where loading stops;
- a name-only placeholder against a real class with a superclass chain;
- a stand-in library that defines, re-exports or omits `NSColor`, loaded next to UIKit;
- one omission per definition, to show that each of the 47 is required.

None of these programs is Blender, and none of them ran on an iPad. They establish the *structure* a
loader must provide. Whether Blender then behaves correctly is a separate question that only execution can
answer.

---

Related: [Technical concepts](../concepts.md#objective-c) · [Blender research](blender.md) ·
[Architecture](../architecture.md#objective-c-registration-and-the-appkit-load-surface)

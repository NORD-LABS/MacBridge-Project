# How MacBridge works, in plain language

This page is for anyone curious about the project, with no programming background needed. It explains
the few ideas you need to follow MacBridge's progress. Technical readers may prefer
[Technical concepts](concepts.md).

## Two environments on related hardware

A Mac runs macOS. An iPad runs iPadOS. Recent models of both use Apple Silicon processors, which speak the
same machine language, called ARM64.

It is tempting to conclude that Mac software should therefore run on an iPad. It does not, because an
application is not only written for a processor. It is written for an *environment*: a particular operating
system, with particular services, and particular rules.

## What an application really is

When you download a Mac app, the important part is a file of compiled instructions. Those instructions are
the part the processor understands, and that part would indeed work on an iPad's processor.

But almost every useful thing an app does, it asks the operating system to do. Opening a file, drawing a
button, playing a sound, starting a thread: each is a request to a *system library*, a shared piece of
software that comes with the operating system. An app is instructions *plus* a long list of these
expectations.

Many of the libraries a Mac app expects exist on iPadOS too, sometimes with the same names. Some do not
exist at all. The most important missing one is AppKit, the library that gives Mac apps their windows,
menus and buttons. iPadOS has its own equivalent, UIKit, which works differently.

## Preparing a program to run

Before a program's first instruction runs, the operating system prepares it. A component called the
*loader* reads the file, places it in memory, finds every library it needs, connects the two, and runs any
setup code. Only then does the app itself start.

On a Mac, macOS's loader does this. Apple's loader also checks which system a program was made for. In
Apple's iPad simulator, it looks at a Mac library, sees that it was made for macOS, and refuses it before
anything runs. That refusal is a deliberate check, and MacBridge does not try to get around it.

So MacBridge would need its own loader, one that prepares a Mac program inside the MacBridge app. That
loader exists today as research code that works with small test programs on a Mac.

## A compatibility layer

A compatibility layer sits between a program and an environment it was not written for. When the program
makes a request the environment cannot answer directly, the layer answers it, either by passing it on to
something equivalent or by providing its own version.

For MacBridge, that would mean:

- passing requests that iPadOS can handle to iPadOS;
- answering requests for things iPadOS does not have, such as parts of AppKit, with MacBridge's own code;
- and keeping a careful record of every request that cannot be answered.

MacBridge has worked this out on paper for Blender: for every one of the 1,453 system functions and objects
a background start of Blender asks for, there is a recorded answer about who would provide it.

## The rules of the iPad

iPadOS is stricter than macOS, on purpose. Every app runs in a *sandbox*, a fenced-off area where it can
only see its own files. Every piece of code that runs must carry a *signature* the system accepts. An app
cannot start other programs as separate processes.

These rules protect people, and MacBridge works within them. It never disables, weakens or works around
them. If the honest answer turns out to be that the rules do not allow a Mac app to run this way, that
answer is the result.

## Why so much testing on a Mac?

Because the Mac is where things can be checked safely and quickly. But a result on a Mac only proves
something about a Mac. The same goes for Apple's iPad *simulator*, which runs on the Mac and does not
enforce all of the iPad's rules.

That is why every result MacBridge publishes says *where* it was measured, and why the project's most
important upcoming experiment, [DeviceProbe](research/device-probe.md), has to run on a real iPad.

## What would count as a breakthrough

Not a screenshot of Blender on an iPad. The first real breakthrough would be much smaller: **a tiny,
original Mac test program, running on a physical iPad through MacBridge, with its output recorded.** That
would show the core idea can work within the iPad's rules. Everything after it, including Blender, would
still have to be shown step by step.

---

**Where next:** [Status](../STATUS.md) · [FAQ](faq.md) · [Glossary](glossary.md)

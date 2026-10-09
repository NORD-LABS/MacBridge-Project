# Technical concepts

This page is for developers who know how to program but have not spent time inside Apple's executable
formats. Each concept gets a definition, the reason it matters to MacBridge, and, where it helps, a small
example. Short definitions are in the [glossary](glossary.md); the research pages go deeper.

**Contents:** [The processor](#the-processor) · [The file](#the-file) · [Loading](#loading) ·
[Before main](#before-main) · [The system libraries](#the-system-libraries) ·
[The platform's rules](#the-platforms-rules)

---

## The processor

### ARM64

ARM64 (AArch64) is the instruction set of every Apple Silicon Mac and of the iPads MacBridge targets.

**Why it matters.** It removes one whole problem. A Mac app built for ARM64 contains instructions an
Apple Silicon iPad's processor can execute directly, so MacBridge does not need an emulator or a
translator like Rosetta. When the same small C program is compiled for macOS and for iOS, the instruction
sequence comes out the same. What differs is everything around the instructions, which is what the rest
of this page is about.

**What it does not solve.** Sharing an instruction set is necessary, not sufficient. A program is
instructions *plus* a long list of expectations about the system it runs on.

### The ABI

The Application Binary Interface is the contract between pieces of compiled code: which registers carry
arguments, which ones a function must leave untouched, how structures are laid out.

**Why it matters.** Most of the ABI is shared between macOS and iPadOS on ARM64, but a loader has to honour
the special cases. One example MacBridge has worked through is thread-local variables (below), whose entry
code may only change a handful of registers. Getting that wrong would corrupt a program in ways that only
show up later, on another thread.

---

## The file

### Mach-O

Mach-O is the file format for programs and libraries on macOS and iPadOS. A Mach-O file has a header, a
list of *load commands*, and segments of code and data.

**Why it matters.** Mach-O is MacBridge's starting point. The inspector reads it on the Mac and on the iPad,
and every later step depends on reading it correctly.

### Universal binaries

A universal ("fat") binary holds several Mach-O files for different architectures in one file, such as
ARM64 and x86_64.

**Why it matters.** MacBridge has to pick the ARM64 slice. Blender's official Apple Silicon build is ARM64
only, so this is simple for Blender, but the inspector handles the general case.

### Load commands

Load commands are the table of contents of a Mach-O file. They declare the segments to map, the libraries
to link, the platform and minimum OS version, the entry point, the code signature, and where the fixup
information is.

**Why it matters.** One load command, the build-version command, declares which platform a binary was
built for. Apple's loader checks it and refuses a mismatch *before any of the program's code runs*:
measured in the iOS Simulator, a macOS library is rejected with "incompatible platform". MacBridge cannot
simply hand a Mac binary to the iPad's loader.

```
LC_BUILD_VERSION   platform macOS   minos 11.2
LC_LOAD_DYLIB      /System/Library/Frameworks/AppKit.framework/Versions/C/AppKit
LC_DYLD_INFO_ONLY  rebase / bind / lazy-bind / export information
LC_CODE_SIGNATURE  offset and size of the signature
```
<sub>An illustrative excerpt of the kind of load commands an ARM64 macOS program carries.</sub>

---

## Loading

### Dynamic linking and dyld

Programs do not contain the system's code. They name the libraries they need, and at launch the *dynamic
loader*, Apple's `dyld`, finds those libraries, maps them into memory, connects them, and prepares
everything before `main` runs.

**Why it matters.** On iPadOS, `dyld` serves iPadOS programs. A macOS program arriving through MacBridge
would need the same preparation from MacBridge itself: that is the role of MacBridge's research loader.
Read more in [The experimental loader](research/loader.md).

### Install names

Each library declares an *install name*: the path that identifies it, for example AppKit's framework path.
A program records the install names of everything it links.

**Why it matters.** Many macOS install names do not exist on iPadOS, and some exist under a different
path. MacBridge maps every install name Blender's headless start needs to one of four answers: an iPadOS
library at the same path, an iPadOS library at another path, a stand-in MacBridge would provide, or a
recorded conflict. For Blender 5.2.2 that is 26 system libraries, all strongly linked, so none can simply
be skipped.

### Imports, exports and binding

A library *exports* symbols; a program *imports* them. *Binding* writes the address of each imported symbol
into the program's memory so its calls and references reach the right place.

**Why it matters.** Imports are the most precise description of what a program expects from the system.
MacBridge's symbol provider registry assigns each of the 1,453 symbols a headless Blender start imports to
a provider. A symbol that exists on iPadOS under the same name is counted as present, and that is all it
is: [the same name does not guarantee the same behaviour](evidence.md#rules).

### Weak imports

A weak import may be missing. If no library provides it, its address becomes zero and the launch
continues.

**Why it matters.** Weak imports let a program run on older systems that lack a newer function. For a
compatibility layer they mark the places where a missing definition is survivable, provided the program
checks before calling.

### Rebasing

Programs are linked as if they would load at a fixed address, then loaded somewhere else. *Rebasing* adds
the difference to every internal pointer.

**Why it matters.** Rebases are the simplest fixups, and a good first test of a loader: after rebasing,
every pointer in memory must be exactly right. In MacBridge's host experiments, memory after fixups matched
the analysis model byte for byte.

### Bind opcodes and chained fixups

Apple binaries encode their fixups in one of two formats. The older one is a compact list of *opcodes*. The
newer one, *chained fixups*, threads the information through the pointers themselves.

**Why it matters.** A loader has to support whichever format the program uses. MacBridge first expected
Blender's ARM64 build to use chained fixups. Reading the actual build showed that **every image uses bind
opcodes**, and the work was reprioritised. MacBridge's opcode decoder agrees with LLVM's `llvm-objdump` on
all 195 of Blender's images that carry fixups, 1,201,316 fixups in total.

---

## Before main

### Initializers

Libraries can run code automatically when they load, before the program's `main`. C++ static
constructors and Objective-C `+load` methods are common sources.

**Why it matters.** A program can fail before its own code starts, inside an initializer. Blender's headless
start has 6,211 static initializers across 30 images, and their order matters. MacBridge's model of that
order was checked against Apple's loader with its own fixtures. Running Blender's initializers is a later
step, because it requires execution.

### Thread-local storage

Thread-local variables have one copy per thread. On Apple platforms a variable is accessed through a
small piece of entry code that the loader connects; on first use in a thread it allocates that thread's
copy from a template.

**Why it matters.** Ten of Blender's headless images use thread-local variables, 94 of them in total, and
Blender is heavily multithreaded. The entry code has a strict rule: on ARM64 it may change only a few
registers and must preserve all the vector registers. MacBridge's ARM64 version of this entry code passed
that contract on four threads, but only under an emulator on Linux; it has not run on Apple hardware.

---

## The system libraries

### libSystem

libSystem is the base of every Apple program: the C library, threads, memory, files, time.

**Why it matters.** Even a five-symbol C program brings dozens of system libraries into memory at startup.
Of the 649 libSystem names Blender imports, 648 are exported by iOS's libSystem. That says they exist; it
does not say they behave the same for a program built for macOS.

### Foundation

Foundation provides strings, collections, dates, files, bundles and process information. It exists on
both platforms.

**Why it matters.** Foundation is shared, but parts of it describe *the current process*: its bundle, its
arguments, its working directory. A program loaded by MacBridge into MacBridge's own process would see
MacBridge's answers unless MacBridge provides its own. These "process-state" questions are one of the two
currently blocked rows in Blender's preflight.

### Objective-C

Objective-C is the language of much of Apple's frameworks. Its runtime keeps a table of classes by name
and dispatches method calls at run time.

**Why it matters.** Classes are not just code; they are registered, by name, while a program loads. A Mac
program that subclasses an AppKit class needs that class to exist before it can even load. See
[Objective-C research](research/objective-c.md).

### AppKit

AppKit is the macOS framework for windows, menus and events. It does not exist on iPadOS.

**Why it matters.** Even started without a window, Blender links AppKit and defines subclasses of
`NSWindow`, `NSView` and `NSOpenGLView`. To load at all, it needs 47 definitions that iPadOS lacks, 39 of them from AppKit. MacBridge
has an experimental shim that provides exactly those, as structure only: it lets a program load, it does
not implement windows.

---

## The platform's rules

### Code signing

Every piece of code that runs on an iPad must be signed in a way the system accepts. On macOS the rules
are more flexible.

**Why it matters.** This is one of the central unknowns. An iPad app can run code that is signed into the
app. Whether, and how, code that originated as a Mac program could be legitimately signed and mapped
inside MacBridge's process is exactly what [DeviceProbe](research/device-probe.md) is meant to begin
measuring. MacBridge does not bypass, disable or weaken code signing, and will record a block if that is
the answer.

### Executable memory

Memory can be readable, writable, executable, or a combination. Modern systems restrict which memory may
become executable.

**Why it matters.** A loader must map a program's code as executable. iPadOS allows that for code signed
into the app; general "just-in-time" executable memory is documented by Apple only for alternative browser
engines. This is the decisive unknown in Blender's preflight.

### Entitlements

Entitlements are signed permissions. Some capabilities, such as a larger memory limit on some iPad
models, are available only through an entitlement Apple provides.

**Why it matters.** MacBridge uses only entitlements obtainable through Apple's normal developer process.
It never forges or misuses one.

### The iPadOS sandbox

Every iPadOS app runs in a sandbox: it can see its own files, not the whole system, and it cannot start
other programs as separate processes.

**Why it matters.** A Mac program expects to be a process of its own, with its own files around it.
On an iPad, a program loaded by MacBridge would have to live inside MacBridge's own process, and see a
file layout MacBridge prepares for it. That is why MacBridge is designed as a userspace runtime inside one
ordinary app, not as a launcher.

---

Next: [Architecture](architecture.md) shows how these pieces fit together in MacBridge, and what exists of
each.

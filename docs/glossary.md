# Glossary

Short definitions of the terms used across MacBridge's documentation. For the longer version, with why each
idea matters to the project, see [Technical concepts](concepts.md).

### ABI

Application Binary Interface. The rules compiled code follows to work with other compiled code: how arguments are passed, which registers must be preserved, how data is laid out in memory.

### AppKit

Apple's framework for windows, menus, controls and events on macOS. It does not exist on iPadOS, which uses UIKit instead.

### Apple Silicon

Apple's own ARM64 processors. In this documentation the term mostly means the M-series chips used in current Macs and in iPad Air and iPad Pro models.

### ARM64

The 64-bit ARM instruction set (also called AArch64). Apple Silicon Macs and iPads both execute it.

### Bind

A fixup that writes the address of a symbol from another library into a program's memory.

### Chained fixups

A newer, compact encoding of fixups used by many recent Apple binaries. Blender 5.2.2 does not use it; its images use bind opcodes.

### Code signing

A cryptographic signature over a program's code. Apple platforms check it before code may run; iPadOS is far stricter than macOS about whose signatures it accepts.

### Compatibility layer

Software that lets a program written for one environment run in another by providing the services it expects. MacBridge is research into whether such a layer is possible on a stock iPad.

### dyld

Apple's dynamic loader: the system component that loads a program and its libraries, applies fixups and runs initializers before the program's own code starts.

### Dylib

A dynamic library on Apple platforms: code loaded alongside a program rather than built into it.

### Dynamic loader

See [dyld](#dyld). MacBridge has its own experimental loader for research.

### Entitlements

Signed permissions attached to an app, such as access to a capability the sandbox otherwise denies. They are granted through Apple's signing process and cannot be added by the app itself.

### Export

A symbol a library makes available to others.

### Fixture

A small program written for a test. MacBridge's fixtures are original C, C++ and Objective-C code, each designed so that one result depends on one specific loader step.

### Fixup

An adjustment made to a program's memory when it is loaded, because addresses are not known until then. Rebases and binds are both fixups.

### Foundation

Apple's framework of basic types and services (strings, collections, files, dates). It exists on both macOS and iPadOS.

### Framework

A bundle that packages a dynamic library with its headers and resources.

### Headless

Running without a user interface. For Blender, `--background` mode: start, run Python, render, save, exit.

### Host execution

Running an experiment on the development Mac itself. It shows that MacBridge's code does what it should, not what an iPad would allow.

### Import

A symbol a program needs from another library.

### Initializer

Code a library runs automatically when it is loaded, before the program's `main`.

### Install name

The path a library declares as its identity, such as `/System/Library/Frameworks/AppKit.framework/Versions/C/AppKit`. Programs record it to find the library again at launch.

### Mach-O

The executable file format used by macOS and iPadOS for programs and libraries.

### Metal

Apple's GPU programming interface, available on both macOS and iPadOS.

### Objective-C runtime

The library that keeps track of Objective-C classes and dispatches method calls while a program runs.

### Physical-device validation

A result measured on a real iPad. In MacBridge it is the only kind of result that can answer the central question.

### Preflight

MacBridge's per-capability readiness table for a headless Blender start. Each row has its own status and evidence; there is deliberately no overall score.

### Rebase

A fixup that adjusts a pointer inside a program by the distance between where it was linked and where it was actually loaded.

### Sandbox

The set of restrictions an app runs under. On iPadOS every app is sandboxed: it can only reach its own files and the capabilities its entitlements grant.

### Simulator

Apple's iOS Simulator, which runs iPadOS frameworks on the Mac. It uses the Mac's kernel and does not enforce device code signing, so its results are not device results.

### Static analysis

Learning about a program by reading its files without running it.

### Thread-local storage

Variables that have a separate copy for each thread. On Apple platforms the loader sets them up through a small piece of entry code with strict rules about which registers it may change.

### UIKit

Apple's framework for the user interface on iPadOS and iOS.

### Weak import

An import that is allowed to be missing. If no library provides it, its address is set to zero instead of stopping the launch.

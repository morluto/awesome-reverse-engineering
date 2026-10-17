# Awesome Reverse Engineering [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> **Featured: [REA](https://github.com/morluto/rea)** — Agent-oriented reverse-engineering tools, from application behavior to native binaries. By the creators of awesome-reverse-engineering.

[![REA — Reverse Engineer Anything](.github/rea-social-preview.png)](https://github.com/morluto/rea)

A curated starting point for understanding binaries, applications, firmware, file formats, and protocols.

Find a tool by the work you need to do. Each entry describes its purpose; commercial tools are marked **commercial**. This is an initial selection, open to additions and corrections.

## Start here

| Your task | Start with |
| --- | --- |
| Learn assembly and reversing fundamentals | [Learning](#learning) |
| Identify an executable and its capabilities | [File identification and triage](#file-identification-and-triage) |
| Read native code or step through it | [Native analysis](#native-analysis) and [Debuggers](#debuggers) |
| Trace calls or instrument a running program | [Dynamic instrumentation and tracing](#dynamic-instrumentation-and-tracing) |
| Examine a suspicious file, process, or memory image | [Malware analysis](#malware-analysis) |
| Inspect an APK, .NET assembly, or Java program | [Android and managed code](#android-and-managed-code) |
| Inspect an iOS app, macOS binary, or Apple firmware | [iOS and macOS](#ios-and-macos) |
| Unpack a Python, Go, Unity, Godot, or obfuscated .NET program | [Language runtimes and packagers](#language-runtimes-and-packagers) |
| Understand browser behavior or an undocumented protocol | [Web and protocols](#web-and-protocols) |
| Extract firmware or inspect a binary format | [Firmware and hardware](#firmware-and-hardware) and [File formats](#file-formats) |
| Compare builds or automate an investigation | [Diffing and analysis frameworks](#diffing-and-analysis-frameworks) and [AI-assisted analysis](#ai-assisted-analysis) |

## Contents

- [Learning](#learning)
  - [Books](#books)
- [File identification and triage](#file-identification-and-triage)
- [Native analysis](#native-analysis)
- [Debuggers](#debuggers)
- [Dynamic instrumentation and tracing](#dynamic-instrumentation-and-tracing)
- [Malware analysis](#malware-analysis)
- [Android and managed code](#android-and-managed-code)
- [iOS and macOS](#ios-and-macos)
- [Language runtimes and packagers](#language-runtimes-and-packagers)
- [Web and protocols](#web-and-protocols)
- [Firmware and hardware](#firmware-and-hardware)
- [File formats](#file-formats)
- [Diffing and analysis frameworks](#diffing-and-analysis-frameworks)
- [AI-assisted analysis](#ai-assisted-analysis)
- [Practice and communities](#practice-and-communities)
- [Related lists](#related-lists)
- [Contributing and maintenance](#contributing-and-maintenance)
- [License](#license)

## Learning

![An open technical manual with circuit diagrams and an orange bookmark](.github/section-art/learning.png)

- [Azeria Labs](https://azeria-labs.com/writing-arm-assembly-part-1/) - ARM assembly tutorials with exercises for learning registers, memory, and calling conventions.
- [Compiler Explorer](https://godbolt.org/) - Compiles code in the browser with many compilers and shows the generated assembly, for seeing how source constructs and optimization levels translate to machine code.
- [Corkami](https://github.com/corkami/pics) - Visual references and posters explaining binary formats and file structures, including executable-format layouts.
- [Nightmare](https://guyinatuxedo.github.io/) - Course built from annotated CTF challenges, progressing from assembly and reversing basics to binary exploitation.
- [OpenSecurityTraining2](https://ost2.fyi/) - Structured courses in assembly, architecture, debugging, and reverse engineering.
- [pwn.college](https://pwn.college/) - Free courses with hands-on challenges in Linux, assembly, reverse engineering, and binary exploitation, run in a browser-accessible environment.
- [Reverse Engineering for Beginners](https://beginners.re/) - Free book connecting compiled C and C++ examples to assembly across several architectures.
- [RPISEC Modern Binary Exploitation](https://github.com/RPISEC/MBE) - Course materials and labs covering reverse engineering, memory corruption, and exploitation; no commits since December 2021, so labs may need older toolchains.

### Books

<!-- TODO: section art for this heading. Add .github/section-art/books.png (320x213, 8-bit palette PNG in the style of the existing illustrations) and reference it here with alt text. -->

- [Hacking the Xbox](https://www.bunniestudios.com/blog/2013/releasing-free-pdf-of-hacking-the-xbox-in-honor-of-aaron-swartz/) - Introduction to hardware reverse engineering through the original Xbox's security design; free PDF edition released by the author.
- [Practical Binary Analysis](https://nostarch.com/binaryanalysis) - Covers ELF and PE internals, disassembly, binary instrumentation, taint analysis, and symbolic execution, with tools built in the exercises.
- [Practical Malware Analysis](https://nostarch.com/malware) - Hands-on introduction to static and dynamic Windows malware analysis with lab exercises; published in 2012, so some tooling chapters are dated.
- [The Ghidra Book](https://nostarch.com/ghidra-book-2e) - Guide to Ghidra's disassembler, decompiler, scripting, and extension APIs; the 2026 second edition covers BSim and PyGhidra.

## File identification and triage

![Unknown files sorted by their format markers in an inspection tray](.github/section-art/file-triage.png)

- [capa](https://github.com/mandiant/capa) - Identifies capabilities in executable files using rules over static or dynamic analysis results.
- [checksec](https://github.com/slimm609/checksec) - Checks ELF security properties such as PIE, RELRO, stack canaries, and non-executable stacks; mitigation flags are not a vulnerability verdict.
- [Detect It Easy](https://github.com/horsicq/Detect-It-Easy) - Identifies executable formats, compilers, packers, and other file characteristics.
- [FLOSS](https://github.com/mandiant/flare-floss) - Recovers obfuscated strings, including strings constructed on the stack.
- [hexvero](https://github.com/maximilianfeix/hexvero) - Statically triages Electron archives and JavaScript bundles for IPC channels, preload bridges, and window settings, plus ELF/Mach-O/PE imports and hardening; its CLI, MCP server, and local web UI require Node.js 22.12+, and pattern-based JavaScript analysis can miss indirect code.
- [LIEF](https://github.com/lief-project/LIEF) - Parses and modifies executable formats such as PE, ELF, and Mach-O from code.
- [Malcat](https://malcat.fr/) - Hex editor and disassembler for triaging unknown files, with 50+ format parsers, embedded-file extraction, YARA scanning, and Python scripting. **Commercial**, with a free Lite edition for non-professional use.
- [PE-bear](https://github.com/hasherezade/pe-bear) - Graphical PE viewer and editor for a quick first look at headers, sections, imports, and resources, including malformed files.
- [pestudio](https://www.winitor.com/) - Flags suspicious imports, strings, resources, and other indicators in Windows executables for initial assessment. **Commercial**, with a free basic edition for private use.

## Native analysis

![A binary file inspected through a magnifying glass](.github/section-art/binary-analysis.png)

- [Binary Ninja](https://binary.ninja/) - Interactive disassembler and decompiler with intermediate representations and scripting APIs. **Commercial**, with a free edition.
- [Cutter](https://github.com/rizinorg/cutter) - Graphical reverse-engineering interface built on Rizin.
- [Decompiler Explorer](https://dogbolt.org/) - Web service that runs an uploaded binary through several decompilers and shows their output side by side.
- [Ghidra](https://github.com/NationalSecurityAgency/ghidra) - Disassembly, decompilation, scripting, and headless analysis for native binaries.
- [IDA](https://hex-rays.com/ida-pro) - Interactive disassembler and decompiler with processor modules and a plugin ecosystem. **Commercial**, with a free edition.
- [radare2](https://github.com/radareorg/radare2) - Command-line toolkit for disassembly, binary inspection, debugging, and scripting.
- [RetDec](https://github.com/avast/retdec) - Retargetable LLVM-based decompiler for ELF, PE, Mach-O, and other formats; in limited maintenance mode, with little new development.
- [Rizin](https://github.com/rizinorg/rizin) - Reverse-engineering framework with command-line analysis and reusable libraries.
- [Rubber Room](https://binarybacktrace.com/tools/rubber_room) - Browser PE workbench with x86-64 disassembly, partial Win32 API emulation and experimental C-like pseudocode that may omit program logic; alpha.

## Debuggers

![A debugger tracing execution to an orange breakpoint](.github/section-art/debugging.png)

- [Cheat Engine](https://github.com/cheat-engine/cheat-engine) - Memory scanner, debugger, and disassembler for finding and changing values in running processes, mainly used for game and application modding.
- [GDB](https://www.sourceware.org/gdb/) - Native debugger with scripting and remote-debugging support.
- [GEF](https://github.com/hugsy/gef) - Single-file GDB extension that adds context views, heap inspection, and commands for exploit development and binary analysis.
- [LLDB](https://lldb.llvm.org/) - LLVM debugger for native programs, including macOS and iOS development workflows.
- [pwndbg](https://github.com/pwndbg/pwndbg) - Debugger extensions for inspecting memory, assembly, and runtime state during binary analysis.
- [rr](https://github.com/rr-debugger/rr) - Records and replays Linux process execution for repeatable debugging.
- [WinDbg](https://learn.microsoft.com/en-us/windows-hardware/drivers/debugger/) - Microsoft debugger for Windows user-mode and kernel debugging, crash dump analysis, and Time Travel Debugging; version 1.2610.1001.0 and later include the official [WinDbg MCP](https://learn.microsoft.com/en-us/windows-hardware/drivers/debuggercmds/set-up-windbg-mcp) server.
- [x64dbg](https://github.com/x64dbg/x64dbg) - Windows user-mode debugger for inspecting native executables and libraries.

## Dynamic instrumentation and tracing

<!-- TODO: section art for this heading. Add .github/section-art/instrumentation.png (320x213, 8-bit palette PNG in the style of the existing illustrations) and reference it here with alt text. -->

- [DynamoRIO](https://github.com/DynamoRIO/dynamorio) - Dynamic binary instrumentation platform for building tools that observe or modify instructions at runtime, with bundled tracing and memory-checking tools.
- [Frida](https://github.com/frida/frida) - Injects scripts into running processes to trace calls, inspect data, and change behavior.
- [Intel Pin](https://www.intel.com/content/www/us/en/developer/articles/tool/pin-a-dynamic-binary-instrumentation-tool.html) - Dynamic binary instrumentation framework for writing analysis tools for x86 and x86-64 programs on Linux and Windows; closed source, free for any use.
- [QBDI](https://github.com/QBDI/QBDI) - LLVM-based dynamic binary instrumentation framework for x86, x86-64, ARM, and AArch64, with C, C++, and Python APIs and Frida integration.
- [strace](https://github.com/strace/strace) - Linux system-call tracer for inspecting process I/O, signals, syscall arguments, and return values.
- [Sysinternals Suite](https://learn.microsoft.com/en-us/sysinternals/) - Microsoft utilities, including Process Monitor, Process Explorer, and Autoruns, for observing process, file, registry, and network activity on Windows.

## Malware analysis

<!-- TODO: section art for this heading. Add .github/section-art/malware-analysis.png (320x213, 8-bit palette PNG in the style of the existing illustrations) and reference it here with alt text. -->

Run samples only in isolated, disposable environments, and follow your organization's handling procedures.

- [CAPE Sandbox](https://github.com/kevoreilly/CAPEv2) - Automated sandbox derived from Cuckoo that runs samples in virtual machines and records behavior, unpacked payloads, and malware configurations.
- [FLARE-VM](https://github.com/mandiant/flare-vm) - Installation scripts that turn a Windows virtual machine into a malware-analysis and reverse-engineering workstation.
- [oletools](https://github.com/decalage2/oletools) - Python tools for inspecting Office, OLE, and RTF files and extracting macros, embedded objects, and other document artifacts.
- [PE-sieve](https://github.com/hasherezade/pe-sieve) - Scans a running process for injected or modified code, such as hollowed modules, hooks, and shellcode, and dumps what it finds.
- [REMnux](https://remnux.org/) - Linux toolkit for analyzing malicious executables, documents, scripts, and network traffic, available as a virtual machine, container, or installer.
- [Speakeasy](https://github.com/mandiant/speakeasy) - Windows emulation framework for PE files, drivers, and shellcode that produces API reports within a modeled runtime.
- [Volatility 3](https://github.com/volatilityfoundation/volatility3) - Memory forensics framework for extracting processes, modules, network connections, and other artifacts from memory images.
- [YARA](https://github.com/VirusTotal/yara) - Identifies and classifies files with rules over strings, byte patterns, and file properties; in maintenance mode, with YARA-X as its successor.
- [YARA-X](https://github.com/VirusTotal/yara-x) - Rust-based rule-scanning engine with CLI and language bindings; check its documented differences before migrating YARA rules.

## Android and managed code

![A browser and phone exchanging packets](.github/section-art/apps-protocols.png)

- [Androguard](https://github.com/androguard/androguard) - Python tooling for analyzing Android applications, bytecode, and call relationships.
- [Apktool](https://github.com/iBotPeaches/Apktool) - Decodes Android resources and Smali code, and rebuilds APKs after edits.
- [AsmResolver](https://github.com/Washi1337/AsmResolver) - Library for reading, modifying, and rebuilding native and managed PE files, including .NET metadata and application bundles.
- [dnSpyEx](https://github.com/dnSpyEx/dnSpy) - .NET debugger and assembly editor maintained as a continuation of dnSpy.
- [ILSpy](https://github.com/icsharpcode/ILSpy) - .NET assembly browser and decompiler with GUI and command-line interfaces.
- [JADX](https://github.com/skylot/jadx) - Android DEX decompiler with code navigation and search in a graphical interface or CLI.
- [JEB](https://www.pnfsoftware.com/jeb/) - Android decompiler and analysis platform with edition-dependent native analysis and official MCP capabilities that vary by version; **commercial**.
- [MobSF](https://github.com/MobSF/Mobile-Security-Framework-MobSF) - Automated static and dynamic analysis of Android, iOS, and Windows mobile apps, with a web interface and REST API.
- [OWASP MASTG](https://mas.owasp.org/MASTG/) - Mobile security testing guidance with Android and iOS reverse-engineering techniques.
- [Recaf](https://github.com/Col-E/Recaf) - Java bytecode analysis and editing environment.
- [Vineflower](https://github.com/Vineflower/vineflower) - Java decompiler focused on modern language features and readable output; requires Java 17 or newer to run current releases.

## iOS and macOS

<!-- TODO: section art for this heading. Add .github/section-art/ios-macos.png (320x213, 8-bit palette PNG in the style of the existing illustrations) and reference it here with alt text. -->

- [class-dump](https://github.com/nygard/class-dump) - Generates Objective-C headers from Mach-O binaries; unmaintained since 2019 and without Swift support, so `ipsw class-dump` is a maintained alternative.
- [Hopper](https://www.hopperapp.com/) - macOS disassembler and decompiler with Objective-C and Swift support, LLDB and GDB debugging, and scripting. **Commercial**, with a free demo.
- [ipsw](https://github.com/blacktop/ipsw) - Command-line toolkit for downloading and examining iOS and macOS firmware, dyld shared caches, kernelcaches, and Mach-O binaries.
- [objection](https://github.com/sensepost/objection) - Frida-based toolkit for exploring iOS and Android apps at runtime, including class inspection, method hooking, and certificate-pinning bypass.
- [pymobiledevice3](https://github.com/doronz88/pymobiledevice3) - CLI and Python API for iOS device services, including logs, crash reports, packet capture, and developer tooling with version-dependent tunnel requirements.

## Language runtimes and packagers

<!-- TODO: section art for this heading. Add .github/section-art/language-runtimes.png (320x213, 8-bit palette PNG in the style of the existing illustrations) and reference it here with alt text. -->

- [AssetRipper](https://github.com/AssetRipper/AssetRipper) - Unity asset-analysis and export tool with version-dependent support and additional paid Premium features.
- [Blutter](https://github.com/worawit/blutter) - Flutter AOT analysis tool for recent Android arm64 libapp.so files, producing annotated assembly, object-pool dumps, and Frida templates.
- [Cpp2IL](https://github.com/SamboyCoding/Cpp2IL) - Recovers types, methods, and IL from Unity IL2CPP builds into .NET assemblies and other outputs; described by its author as work in progress.
- [de4dot](https://github.com/de4dot/de4dot) - .NET deobfuscator and unpacker for assemblies protected by common obfuscators; archived in 2020 and no longer updated.
- [GDRE Tools](https://github.com/GDRETools/gdsdecomp) - Recovers Godot projects from exported games, including PCK extraction, GDScript decompilation, and resource conversion.
- [GoReSym](https://github.com/mandiant/GoReSym) - Recovers function names, types, and build metadata from Go binaries, including stripped ones.
- [Hermit](https://github.com/xV4L3x/hermit) - Interactive toolkit for inspecting, disassembling, decompiling, and structurally patching React Native Hermes bytecode; supports HBC 94, 95, and 96, with HBC 98 unsupported.
- [Il2CppDumper](https://github.com/Perfare/Il2CppDumper) - Restores Unity IL2CPP type and method metadata for use in IDA, Ghidra, and other tools; no commits since July 2024, with Cpp2IL as a maintained alternative.
- [pycdc](https://github.com/zrax/pycdc) - Disassembles and decompiles Python bytecode from `.pyc` files; decompilation of recent Python versions can be incomplete.
- [pyinstxtractor](https://github.com/extremecoders-re/pyinstxtractor) - Extracts the contents of PyInstaller executables, including the bytecode needed for decompilation; the [pyinstxtractor-ng](https://github.com/pyinstxtractor/pyinstxtractor-ng) fork uses xdis so the host Python need not match the build version and supports PyInstaller archive decryption when the embedded key can be recovered, but neither tool decompiles bytecode.

## Web and protocols

![A browser displaying a network packet trace](.github/section-art/web-protocols.png)

- [Burp Suite](https://portswigger.net/burp) - Intercepting proxy and toolkit for inspecting, replaying, and modifying HTTP and WebSocket traffic. **Commercial**, with a free Community Edition.
- [Chrome DevTools](https://developer.chrome.com/docs/devtools/) - Browser tools for stepping through JavaScript, inspecting network requests, and examining runtime state.
- [HTTP Toolkit](https://httptoolkit.com/) - Intercepts and inspects HTTP(S) traffic from browsers, desktop applications, Android devices, and containers with automated interception setup. **Commercial**, with a free open-source edition.
- [mitmproxy](https://github.com/mitmproxy/mitmproxy) - Intercepts, inspects, and modifies HTTP traffic with interactive tools and Python scripts.
- [Protobuf Decoder](https://github.com/pawitp/protobuf-decoder) - Web application that decodes Protobuf messages without a schema and shows field numbers, wire types, and possible value interpretations.
- [Scapy](https://github.com/secdev/scapy) - Python packet framework for dissecting and constructing protocols, reading PCAPs, and scripting network experiments.
- [WABT](https://github.com/WebAssembly/wabt) - WebAssembly utilities for converting, inspecting, validating, and decompiling modules.
- [wasm-tools](https://github.com/bytecodealliance/wasm-tools) - Bytecode Alliance tools for inspecting, validating, and transforming WebAssembly modules, components, and WIT interfaces.
- [webcrack](https://github.com/j4k0xb/webcrack) - Deobfuscates JavaScript and unpacks common bundler output to make code easier to inspect.
- [Wireshark](https://www.wireshark.org/) - Captures and dissects network traffic for protocol investigation.

## Firmware and hardware

![A microcontroller board with cyan traces and an orange debug connector](.github/section-art/firmware-hardware.png)

- [Binwalk](https://github.com/ReFirmLabs/binwalk) - Identifies embedded files and extracts content from firmware images.
- [EMBA](https://github.com/e-m-b-a/emba) - Firmware security analyzer that extracts images, runs static and emulation-based checks, and produces reports and SBOMs.
- [Facedancer](https://github.com/greatscottgadgets/facedancer) - Python USB device-emulation and proxy framework for compatible hardware on GNU/Linux; 3.x does not support legacy scripts and backend capabilities vary.
- [FirmAE](https://github.com/pr0v3rbs/FirmAE) - Emulates Linux-based router and IP camera firmware for dynamic analysis, using heuristics that make full-system emulation succeed more often.
- [flashrom](https://www.flashrom.org/) - Reads, writes, and verifies flash chips through supported programmers, for dumping or restoring firmware from hardware.
- [Glasgow Interface Explorer](https://github.com/GlasgowEmbedded/glasgow) - Programmable hardware interface explorer with applets for probing and interacting with digital buses; requires Glasgow hardware.
- [OFRAK](https://github.com/redballoonsecurity/ofrak) - Framework for unpacking, analyzing, modifying, and repacking binary artifacts.
- [OpenOCD](https://openocd.org/) - Connects to hardware debug interfaces for on-chip debugging and flash access.
- [Packetry](https://github.com/greatscottgadgets/packetry) - USB 2.0 protocol analyzer for Cynthion captures and offline PCAP files using the LINKTYPE_USB_2_0 format.
- [QEMU](https://www.qemu.org/) - Machine emulator for running firmware and programs built for other architectures, with a GDB stub for debugging.
- [Renode](https://github.com/renode/renode) - Embedded-system simulator with scriptable platform and peripheral models for repeatable firmware debugging and observation.
- [sigrok](https://sigrok.org/) - Signal analysis tools and protocol decoders for logic analyzers and related hardware.
- [UEFITool](https://github.com/LongSoft/UEFITool) - Parses UEFI firmware structures and extracts or replaces modules.
- [unblob](https://github.com/onekey-sec/unblob) - Extracts nested archives, compressed data, and filesystem images from firmware and other files.
- [usb-rea](https://github.com/emirmrkaljevic/usb-rea) - Infers the protocol of a vendor-specific USB device from usbmon or USBPcap captures of labelled actions (value fields, counters, checksums, multi-packet commands), with frame-number evidence, and generates a pyusb driver and a Wireshark Lua dissector; tested on synthetic and documented protocols, not yet on many real devices.

## File formats

![A structured file separated into data layers](.github/section-art/file-formats.png)

- [010 Editor](https://www.sweetscape.com/010editor/) - Hex editor with binary templates for inspecting structured files. **Commercial**.
- [Construct](https://github.com/construct/construct) - Declarative Python library for parsing and building binary formats with composable schemas and validation.
- [CyberChef](https://github.com/gchq/CyberChef) - Browser-based workbench for decoding, decompressing, and transforming data with exportable recipes.
- [Hex Harbinger](https://binarybacktrace.com/tools/hex_harbinger) - Browser hex editor that overlays structure templates for PE, ELF, Mach-O and ZIP files and highlights the parsed fields; alpha.
- [ImHex](https://github.com/WerWolv/ImHex) - Hex editor with a pattern language for describing and exploring binary structures.
- [Kaitai Struct](https://kaitai.io/) - Describes binary formats declaratively and generates parsers in multiple languages.
- [Struct Smith](https://binarybacktrace.com/tools/struct_smith) - Browser editor for Spec binary-format schemas, with a live parse tree, byte highlighting and diagnostics; alpha, with a 64 MiB input limit.

## Diffing and analysis frameworks

![Two binary files compared with a changed block highlighted](.github/section-art/diffing.png)

- [angr](https://github.com/angr/angr) - Python framework for symbolic execution and program analysis; [angr-management](https://github.com/angr/angr-management) is its official GUI front end, not a separate analysis engine.
- [BinDiff](https://github.com/google/bindiff) - Compares disassembled binaries to identify similar functions and changes between builds; inputs come from the [BinExport](https://github.com/google/binexport) exporters for IDA Pro, Ghidra, and Binary Ninja; the current IDA plugin source requires IDA Pro 9.4+, while the 2024 release documents IDA SDK 8.0+ for building that plugin.
- [Capstone](https://github.com/capstone-engine/capstone) - Multi-architecture disassembly library for building analysis tools.
- [Diaphora](https://github.com/joxeankoret/diaphora) - Binary diffing plugin for comparing functions and transferring analysis in IDA.
- [ghidriff](https://github.com/clearbluejar/ghidriff) - Ghidra-based command-line binary diffing engine with JSON, Markdown, and optional HTML reports; requires compatible Ghidra, PyGhidra, and JDK versions.
- [Miasm](https://github.com/cea-sec/miasm) - Python reverse-engineering framework with an intermediate representation, emulation, symbolic execution, and assemblers and disassemblers for several architectures.
- [Qiling](https://github.com/qilingframework/qiling) - Emulates binaries with operating-system services for scripted runtime analysis.
- [Triton](https://github.com/JonathanSalwan/Triton) - Dynamic binary analysis library with symbolic execution, taint analysis, and AST representations of instruction semantics, usable from C++ or Python.
- [Unicorn](https://github.com/unicorn-engine/unicorn) - CPU emulation library for executing and instrumenting machine code across architectures.

## AI-assisted analysis

![A robot assistant examining a binary file](.github/section-art/ai-analysis.png)

Agent integrations expose existing analysis tools or coordinate an investigation. Check the upstream documentation for required software and supported clients; confirm conclusions against the underlying code and runtime evidence.

- [Binary Ninja MCP Server](https://docs.binary.ninja/guide/mcp.html) - Built-in Binary Ninja server that exposes functions, symbols, strings, disassembly, IL, and decompiled code to MCP clients; the headless variant requires a Commercial or Ultimate license.
- [Chrome DevTools MCP](https://github.com/ChromeDevTools/chrome-devtools-mcp) - Official MCP server for inspecting Chrome network activity, runtime state, console output, and performance traces; requires Node.js LTS and Chrome.
- [Gepetto](https://github.com/JusticeRage/Gepetto) - IDA plugin that asks language models to explain decompiled functions and rename their variables; requires IDA 7.6 or later and access to a supported model provider.
- [Ghidra MCP Server](https://github.com/bethington/ghidra-mcp) - Connects AI clients to Ghidra analysis through MCP.
- [GhidraMCP](https://github.com/LaurieWired/GhidraMCP) - Ghidra plugin and MCP server for decompiling, listing, and renaming functions and data; the original project from which Ghidra MCP Server was derived.
- [Hex-Rays IDA MCP](https://github.com/HexRaysSA/ida-mcp) - Official IDA MCP server for agent access to binary analysis; requires IDA 9.4+ with idalib, Python 3.11+, and uv, with IDA licensing separate from the server.
- [IDA Pro MCP](https://github.com/mrexodia/ida-pro-mcp) - Exposes IDA analysis and scripting capabilities to MCP clients; requires a compatible IDA installation.
- [JADX-AI-MCP](https://github.com/zinja-coder/jadx-ai-mcp) - Connects AI clients to JADX for Android application analysis.
- [radare2 MCP](https://github.com/radareorg/radare2-mcp) - Provides an MCP interface to radare2 for agent-driven binary analysis.
- [RES](https://github.com/alextnetto/res) - Experimental agent skill for documenting a SaaS web app's screens, business rules, data model, API shapes, and design tokens through the browser, with sandbox and change-ledger guidance; requires a browser-driving agent and Node.js 22+.
- [WinDbg MCP](https://learn.microsoft.com/en-us/windows-hardware/drivers/debuggercmds/set-up-windbg-mcp) - Official MCP server built into WinDbg 1.2610.1001.0 and later; supported clients are VS Code with GitHub Copilot and GitHub Copilot CLI, with one active MCP client per WinDbg session.

## Practice and communities

![Interlocking challenge tiles beside community chat bubbles](.github/section-art/practice.png)

- [crackmes.one](https://crackmes.one/) - Practice binaries organized by platform, architecture, and difficulty.
- [FLARE-On](https://flare-on.com/) - Annual reverse-engineering challenge series with previous challenges and solutions.
- [Microcorruption](https://microcorruption.com/) - Browser-based embedded security CTF in which you reverse and exploit firmware for simulated MSP430 lock devices with a built-in debugger.
- [OALabs](https://www.youtube.com/@OALABS) - Video tutorials on malware reverse engineering, unpacking, and analysis tooling.
- [picoCTF](https://picoctf.org/) - Free CTF platform from Carnegie Mellon University with beginner-friendly reversing, forensics, and binary exploitation challenges, plus a year-round practice gym.
- [r/ReverseEngineering](https://www.reddit.com/r/ReverseEngineering/) - Subreddit for sharing reverse-engineering articles, tools, and research.
- [Reverse Engineering Stack Exchange](https://reverseengineering.stackexchange.com/) - Questions and answers about tools, assembly, executable formats, and analysis techniques.
- [Root Me](https://www.root-me.org/) - Challenge platform whose categories include binary cracking, app-system exploitation, and forensics.

## Related lists

![Reference catalogs connected by a chain link](.github/section-art/related-lists.png)

See the [list structure and maintenance review](docs/list-review.md) for a dated comparison of 21 general and specialist collections. Recent activity and popularity are assessed separately there.

- [Awesome AI Reverse Engineering](https://github.com/DiscoverBox/awesome-ai-reverse) - AI integrations organized by analysis ecosystem, with English and Chinese editions.
- [Awesome Embedded Security](https://github.com/hexsecs/awesome-embedded-security) - Firmware and hardware tools, learning resources, and repository-health workflows.
- [Awesome Game File Format Reversing](https://github.com/VelocityRa/awesome-game-file-format-reversing) - Game formats, engines, asset tools, and specialist references.
- [Awesome REA](https://github.com/kaixinbaba/awesome-rea) - Independent directory of open-source reconstructions, reimplementations, compatibility projects, and REA resources, with dated source reviews, license notes, and known limits.
- [Awesome REA (reacher-z)](https://github.com/reacher-z/Awesome-REA) - Bilingual catalog of reverse-engineering tools, reconstruction projects, case studies, and research, with a searchable website and a separately labeled automated repository index.
- [Awesome Reverse Engineering and Malware Analysis](https://github.com/ZX41R/awesome-reverse-engineering-and-malware-analysis) - Topic pages spanning reversing, malware analysis, and related research.
- [Awesome Reversing by Reversing.ID](https://github.com/ReversingID/Awesome-Reversing) - Separate catalogs for software, hardware, formats, and databases.
- [Awesome Web Reversing](https://github.com/TheQmaks/awesome-web-reversing) - Web investigation workflows and a machine-readable tool catalog.

## Contributing and maintenance

![A maintenance checklist beside a wrench](.github/section-art/contributing.png)

Read [CONTRIBUTING.md](CONTRIBUTING.md) to suggest a resource or fix an entry. Prefer canonical project links and descriptions that explain when a resource is useful.

The [priority-candidate source review](docs/priority-candidates.md) records dated support claims, required environments, and four [reproducible examples](examples/resource-intake/README.md); documented support and reproduced behavior are recorded separately.

Links are checked on pull requests, pushes to the default branch, and weekly by [GitHub Actions](.github/workflows/links.yml). A passing link check confirms availability, not tool quality or maintenance; review archived projects, compatibility changes, and replacements when updating entries.

## License

![A shared document with an open padlock](.github/section-art/license.png)

[CC0 1.0](LICENSE). Listed projects retain their own licenses.

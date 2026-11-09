# Bounded resource examples

These self-authored fixtures demonstrate Construct, Scapy, YARA-X, Vineflower, Malduck, hermes-dec, MemProcFS, boofuzz, Keystone, esptool, and Z3 in CI, plus a local PyLingual check. They are small selection examples, not upstream test suites or evidence of full platform/version support.

Use Python 3.11 with `venv`/`pip` support, JDK 17, Node.js, and an Internet connection for the pinned packages, JAR, and Hermes compilers. From the repository root:

```bash
resource_examples_dir="$(mktemp -d)"
python3.11 -m venv "$resource_examples_dir/venv"
"$resource_examples_dir/venv/bin/python" -m pip install -r examples/resource-intake/requirements.txt
"$resource_examples_dir/venv/bin/python" examples/resource-intake/verify.py --output "$resource_examples_dir/results"
```

The runner downloads [Vineflower 1.12.0](https://github.com/Vineflower/vineflower/releases/tag/1.12.0) and two `hermes-compiler` npm tarballs, and checks each SHA-256 before executing anything from them. An existing JAR can be supplied with `--vineflower-jar /path/to/vineflower-1.12.0.jar`; the same digest check still applies. Failed assertions or commands fail the run; a successful run writes `results.json` and retains generated artifacts in a unique directory under the selected output path.

The Hermes fixture additionally needs Node.js (CI uses Node.js 22). Its pinned compilers provide Linux x86-64, universal macOS, and Windows x86-64 binaries; native Windows/macOS execution is not part of this repository's verification.

MemProcFS runs only on Linux x86-64, where it also needs the system `libusb-1.0` library (`sudo apt-get install libusb-1.0-0` on Debian/Ubuntu). Its pinned wheels are installed only on that host, and on other hosts the runner records MemProcFS as `skipped`.

The Keystone check and its explicit Keystone/Capstone pins are exercised only on Linux x86-64; Capstone may also be installed elsewhere as another package's dependency. Keystone 0.9.2 has no wheel for ARM hosts, where pip would build it from source with CMake and a C++ compiler; on other hosts the runner records Keystone as `skipped`.

On Windows, use this PowerShell block with Python 3.11 and JDK 17 or newer (`java` and `javac` on `PATH`). The verifier checks both Java versions before running the fixtures. Use `python` in place of `py -3.11` if that is your Python 3.11 launcher.

```powershell
$resourceExamplesDir = Join-Path ([System.IO.Path]::GetTempPath()) ("resource-examples-" + [guid]::NewGuid())
New-Item -ItemType Directory -Path $resourceExamplesDir | Out-Null
py -3.11 -m venv (Join-Path $resourceExamplesDir "venv")
$resourcePython = Join-Path $resourceExamplesDir "venv\Scripts\python.exe"
& $resourcePython -m pip install -r examples/resource-intake/requirements.txt
& $resourcePython examples/resource-intake/verify.py --output $resourceExamplesDir
```

| Resource / pinned version | Input and independent expected result | Scope |
| --- | --- | --- |
| Construct 2.10.70 | Golden bytes `534d4b310500017472616365`: `SMK1`, little-endian length 5, type 1, payload `trace`; parse/build and reject bad magic, truncation, or trailing bytes | One binary schema on this Python host |
| Scapy 2.8.0 | Known Ethernet/IP/UDP fields and `trace` payload; independent IP/UDP checksum checks; PCAP write/read | Offline packets only, no transmission or live capture |
| YARA-X 1.21.0 | Self-authored rule matches the golden bytes and not `negative sample`; unescaped `{` in a regex produces `CompileError` | Python API and this documented regex difference, not all YARA rules/modules |
| Vineflower 1.12.0 | Java 17 record and switch expression; compile → decompile → rebuild; main prints `25`, five branch vectors match explicit expected values | This fixture only, no obfuscation or other Java target versions |
| Malduck 4.4.1 | A [self-authored extractor](malduck_modules/duckcfg/__init__.py) and [YARA rule](malduck_modules/duckcfg/duckcfg.yar); a sample with marker `DKCFG1`, an 8-byte key, and a config encrypted by an independent RC4 implementation yields two C2 URLs, campaign `trace-7`, and sleep `300`; wrong-key and no-marker samples yield no config | Extractor framework, procmem reads, and RC4 only; no real malware family |
| hermes-dec 0.1.8 | [`hbc_fixture.js`](hbc_fixture.js) compiled by `hermes-compiler` 250829098.0.19 (HBC 98) and 260318099.0.4 (HBC 99) at `-g0` and `-g1`; header version, disassembly, and pseudo-code landmarks (function names, strings, `<Mod>`, constant `7`) | See the limits below |
| MemProcFS 5.19.0 | A 16 MiB raw image with a self-built x64 page table; with `-dtb 0x10000` the [probe](memprocfs_probe.py) shows one `unknown_process`, reads `MPFS-PHYS-MARK-1` at physical `0x1000` and through `/memory.pmem`, and translates `0x140001678` to physical `0x345678` where it reads `MPFS-VIRT-MARK-2` | Physical-memory, page-table, and virtual-file-system API on Linux x86-64 only; no Windows OS analysis |
| boofuzz 0.4.2 | A made-up TRC1 protocol (`TRC1`, kind, big-endian length, payload, big-endian CRC-32) described with `Size` and `Checksum` blocks; the default frame matches bytes built with `struct` and `zlib`, and a localhost server receives all 575 payload mutations with a correct length and CRC, replying to each | One-field-at-a-time fuzzing (`max_depth=1`) against a localhost server only; see the limits below |
| Keystone 0.9.2 (with Capstone 5.0.9) | x86-64 `push rbp; mov rbp, rsp; mov eax, dword ptr [rbx + rcx*4 + 8]; xor eax, eax; pop rbp; ret` and ARM64 `mov x0, #1; add x1, x2, x3; ldr x0, [x1, #8]; b #0x1010; ret` at base `0x1000` assemble to bytes encoded by hand from the Intel SDM and Arm ARM (`554889e58b448b0831c05dc3`, `200080d24100038b200440f901000014c0035fd6`); Capstone disassembles them back to the same text, which reassembles to the same bytes; `b #0x1010` at `0x2000` becomes the backward branch `04fcff17` | Two short sequences on two ISAs, Linux x86-64 only; see the limits below |
| esptool 5.6.0 | A 128-byte ESP32 application image built by hand from the [5.6.0 documented layout](https://raw.githubusercontent.com/espressif/esptool/e970488de2c8f1906ca9b08de681b3f9dc58b2d5/docs/en/advanced-topics/firmware-image-format.rst): entry `0x40080400`, a 16-byte DRAM segment at `0x3ffb0000` and a 32-byte IRAM segment at `0x40080400`, checksum `0xf3` (`0xEF` XOR the segment data) and an appended SHA-256 `f8d0bbc1…c9cb`; `image-info` reports the header, both segments at file offsets `0x18` and `0x30`, and a valid checksum and hash, with no device connected. A synthetic variant with chip ID 9 is detected as ESP32-S3 (header identification only); flipping one data bit gives checksum `0xf2` and hash `b1f33ee1…4147`, both reported as invalid | Offline `image-info` on one ESP32 application layout; no serial port, flashing, or bootloader images; see the limits below |
| Z3 (z3-solver 5.3.1.0) | A synthetic 16-bit serial check written as a decompiler would show it (`((x * 0x9E37) ^ (x >> 5)) + rotl(x, 3)` with unsigned arithmetic) and target `0x002a`; brute-forcing all 65,536 inputs in plain Python finds exactly `0x1bb9`, `0x9cff`, and `0xb62c`, and Z3's bit-vector solver, asked again with each found serial blocked, returns the same three and then `unsat` | Python API, one 16-bit constraint; no SMT-LIB files, tactics, timeouts, or `unknown` results; see the limits below |

The branch oracle for `Probe.java` is:

```text
-1:-1
0:11
1:22
2:22
9:-1
```

The hermes-dec check also records three limits:

- `hbc-file-parser` warns that HBC 98 and 99 are not formally supported.
- With `-g1` location info, `hbc-file-parser` prints the header and then raises a `TypeError` in `debug_info_parser.py`; `-g0` files parse cleanly. The disassembler and decompiler succeed at both levels.
- The original fixture prints `even:negative:25` under Node.js; executing the pseudo-code prints `even:negative:21`, because register variables are shared across functions instead of being local to each call.

The boofuzz check also records three limits:

- Replies to fuzzed messages are read only with `receive_data_after_fuzz=True`; by default `last_recv` stays empty.
- `String` mutations are text: byte patterns such as `\xde\xad\xbe\xef` are sent UTF-8 encoded, and `max_len` counts characters, so a 48-character limit produced a 96-byte payload.
- Without a process monitor or restart callback, a target that stops listening ends the run after 17 of 575 cases with only an info message ("Ending fuzzing"); no test case is marked failed and `fuzz()` returns normally.

The Keystone check also records two limits:

- A branch to an absolute target is encoded as an offset from the address passed to `asm()`, so the same text gives different bytes at another base. A RIP-relative memory operand such as `[rip + 8]` instead keeps its literal displacement bytes at both bases; moving those bytes changes the address they access.
- An unknown mnemonic fails with `KS_ERR_ASM_MNEMONICFAIL`, but an ARM64 immediate that one `MOV` cannot encode (`mov x0, #0x12345678`) fails with errno 561, which the 0.9.2 Python binding has no constant for and reports only as "Unknown error".

The esptool check also records two limits:

- In 5.6.0, `image-info` reports checksum/hash mismatches as `invalid` but still exits 0, so a script must read those lines rather than the exit status. A file cut off inside a segment exits 2 (`End of file reading segment 0x3ffb0000, length 16 (actual length 8)`).
- `--chip esp32s3` makes `image-info` parse an ESP32 image as ESP32-S3 without a warning: it still prints `Chip ID: 0 (ESP32)` and a valid checksum, but labels the segments with the ESP32-S3 memory map. Without `--chip`, the chip comes from the image header.

The Z3 check also records two limits, both described in the [5.3.1 Python API](https://raw.githubusercontent.com/Z3Prover/z3/ac9156f97cb44e56472e1c841f7a2beb1e976b24/src/api/python/z3/z3.py) but easy to miss when translating decompiled code:

- `>>` on a bit-vector is an arithmetic (signed) shift; C's unsigned `>>` is `LShR`. Written with `>>`, the same check returns only `0x1bb9`, silently missing the two serials whose top bit is set, without an error. The two shifts agree whenever the top bit is clear.
- `model.eval(y, model_completion=True)` gives an unconstrained variable the value 0 and adds it to the model, so afterwards `model[y]` is 0 and `model.decls()` lists `y` as if the solver had chosen it.

Without `-dtb`, MemProcFS rejects a raw image that contains no identifiable operating system (`Unable to locate valid DTB`). The Linux `memprocfs` wheel does not include `leechcore.so`; the runner uses the one from `leechcorepyc` by starting the probe with `LD_LIBRARY_PATH` pointing at its directory.

The [dated local result](verified.json) records host/tool versions, input hashes, artifact digests, and the tested scope; it was produced in a Linux x86_64 container. CI repeats the examples and uploads current results through the [resource-example workflow](../../.github/workflows/resource-examples.yml). The current job uses Linux x86-64, Python 3.11, Java 17, Node.js 22, and `libusb-1.0`; it makes no Windows, macOS, hardware, or other-version claim.

## Local check: PyLingual

PyLingual needs about 1.2 GB of models per target Python version, so it is not part of the CI job. [`pylingual/fixture.py`](pylingual/fixture.py) is compiled with checked-hash invalidation for CPython 3.11.15, 3.12.13, and 3.13.14 (through exact-version `uv` requests), decompiled with PyLingual v0.1.0 (commit `11a1516`), and its functions are loaded one at a time and compared with the original, so a function that does not compile cannot hide the others. [`pinned_config.yaml`](pylingual/pinned_config.yaml) pins the segmentation and statement models to the Hugging Face revisions observed on 2026-10-19 and still current on 2026-10-21. PyLingual loads tokenizers without a revision argument, so the config cannot pin them; [the report](pylingual/verified.json), which the runner generates, records the tokenizer revisions the Hugging Face cache resolved, the PyLingual commit and package versions, and input hashes.

```bash
git clone https://github.com/syssec-utd/pylingual && git -C pylingual checkout 11a1516d84a6c2aa71ec23fbd11e4b99dc8c4a86
(cd pylingual && uv sync --frozen)
python3 examples/resource-intake/pylingual/run.py --pylingual pylingual/.venv/bin/pylingual --output "$(mktemp -d)"
```

The runner records the resolved compiler versions, disables the optional shared Redis translation cache, and saves per-target stdout/stderr logs for model-download or decompilation failures. PyLingual itself needs Python 3.12 or newer. Hosts using a SOCKS proxy may also need the optional `socksio` transport in the PyLingual environment; this is a transport requirement, not a model or decompiler result. On all three target versions, `classify`, `checksum`, `squares`, and `label` behave like the original. `parse_port` (a `try`/`except` followed by a chained comparison) fails on every version, and PyLingual flags it in both its report and the output file: on 3.11 it does not compile (`Compilation Error`), so the decompiled file as a whole cannot be imported; on 3.12 and 3.13 the file imports, but `parse_port` returns `-2` for `"8080"` instead of `8080` (`Different control flow`). The same results were produced at commit `509ea92` on 2026-10-19, and repeated runs produced identical output.

See the [candidate review](../../docs/priority-candidates.md) for primary sources, documented requirements, and the nineteen entries without execution verification.

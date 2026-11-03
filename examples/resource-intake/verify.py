"""Reproduce eleven narrow resource examples with independent expected outputs."""
import argparse
import ctypes.util
from datetime import datetime, timezone
import hashlib
from importlib.metadata import PackageNotFoundError, version
import csv
import io
import json
import os
from pathlib import Path
import platform
import re
import socket
import struct
import subprocess
import sys
import tarfile
import tempfile
import threading
import zlib
from urllib.request import urlopen


SOURCE = Path(__file__).resolve().parent
JAR_URL = "https://github.com/Vineflower/vineflower/releases/download/1.12.0/vineflower-1.12.0.jar"
JAR_SHA256 = "1dfcfe974395734fa467ce620661c7623d05ba83670de0529b1fbd63ff548b9d"
CFR_URL = "https://github.com/leibnitz27/cfr/releases/download/0.152/cfr-0.152.jar"
CFR_SHA256 = "f686e8f3ded377d7bc87d216a90e9e9512df4156e75b06c655a16648ae8765b2"
# Shapes.java: text block, areas 3*2*2, -1 (r == 0), 3*3, 2*5, then label(0, 1, 5, -3, 6).
SHAPES_OUTPUT = "shapes|  v1|12,-1,9,10,zero,one1,one5,neg,many,"
GOLDEN = bytes.fromhex("534d4b310500017472616365")
EXPECTED_BRANCHES = "-1:-1\n0:11\n1:22\n2:22\n9:-1"
HERMESC = {
    98: ("https://registry.npmjs.org/hermes-compiler/-/hermes-compiler-250829098.0.19.tgz",
         "839af099f0926b5ebbd738ba54764a3f40e35dfc3aac91babf56f8eb7c69280e"),
    99: ("https://registry.npmjs.org/hermes-compiler/-/hermes-compiler-260318099.0.4.tgz",
         "613b6230cf796bd1b6a8248e2cf8fb2799a5be92d23d49e96ee0b68dc2bfdcf2"),
}
HBC_ORIGINAL_OUTPUT = "even:negative:25"
HBC_PSEUDOCODE_OUTPUT = "even:negative:21"


DUCK_KEY = b"duck-key"
DUCK_PLAIN = b"c2=http://192.0.2.10/gate;c2=http://198.51.100.7/gate;campaign=trace-7;sleep=300"
DUCK_CONFIG = {"family": "duckcfg", "urls": ["http://192.0.2.10/gate", "http://198.51.100.7/gate"], "campaign": "trace-7", "sleep": 300}
TRC1_CASES = 575
MEMPROCFS_PACKAGES = {"memprocfs": "5.19.0", "leechcorepyc": "2.23.3"}
PML4, PDPT, PD, PT, PAGE = 0x10000, 0x11000, 0x12000, 0x13000, 0x345000
FIXTURE_VA = 0x140001678
KEYSTONE_PACKAGES = {"keystone-engine": "0.9.2", "capstone": "5.0.9"}
ASM_BASE = 0x1000
# Expected bytes are encoded by hand from the Intel SDM and Arm ARM opcode tables, not by either library.
X64_SOURCE = "push rbp; mov rbp, rsp; mov eax, dword ptr [rbx + rcx*4 + 8]; xor eax, eax; pop rbp; ret"
X64_BYTES = "554889e58b448b0831c05dc3"
A64_SOURCE = "mov x0, #1; add x1, x2, x3; ldr x0, [x1, #8]; b #0x1010; ret"
A64_BYTES = "200080d24100038b200440f901000014c0035fd6"
# The same `b #0x1010` assembled at 0x2000 is a backward branch: imm26 = (0x1010 - 0x2000) / 4.
A64_BACKWARD_BRANCH = "04fcff17"
ESP_ENTRY = 0x40080400
ESP_SEGMENTS = [(0x3FFB0000, b"ESPT-DRAM-MARK01"), (0x40080400, bytes(range(32)))]
# 0xEF XOR every segment data byte; SHA-256 of the 96 bytes before the appended digest.
ESP_CHECKSUM = 0xF3
ESP_DIGEST = "f8d0bbc1a5404fa6754dc071f077ffd0b7d12fdda1887b9d236ff9b53bfbc9cb"
# The same image with bit 0 of the first DRAM data byte flipped.
ESP_CORRUPT_CHECKSUM = 0xF2
ESP_CORRUPT_DIGEST = "b1f33ee18559e6060ca9a6acd628f0ab432abd84afd68f55c42bda4a3cc74147"

def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def checksum(data):
    """Independent RFC 1071-style checksum for the small packet fixture."""
    if len(data) % 2:
        data += b"\x00"
    total = sum(struct.unpack(f"!{len(data) // 2}H", data))
    while total >> 16:
        total = (total & 0xFFFF) + (total >> 16)
    return (~total) & 0xFFFF


def run(*args, env=None):
    completed = subprocess.run(args, text=True, capture_output=True, check=True, env=env)
    return completed.stdout.strip()


def hermesc(work, bytecode_version):
    hosts = {"Linux": "linux64-bin", "Darwin": "osx-bin", "Windows": "win64-bin"}
    system = platform.system()
    if system not in hosts or (system != "Darwin" and platform.machine().lower() not in ("x86_64", "amd64")):
        raise SystemExit("The pinned Hermes compilers require Linux/Windows x86-64 or macOS x86-64/arm64.")
    url, digest = HERMESC[bytecode_version]
    with urlopen(url, timeout=120) as response:
        archive = response.read()
    assert hashlib.sha256(archive).hexdigest() == digest, f"hermes-compiler {bytecode_version} digest mismatch"
    prefix = Path("package/hermesc") / hosts[system]
    directory = work / f"hermesc-{bytecode_version}"
    directory.mkdir()
    target = directory / ("hermesc.exe" if system == "Windows" else "hermesc")
    with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
        # Windows needs the runtime DLLs beside hermesc.exe, not just the executable.
        for member in tar.getmembers():
            if member.isfile() and Path(member.name).parent == prefix:
                (directory / Path(member.name).name).write_bytes(tar.extractfile(member).read())
    target.chmod(0o755)
    return target


def verify_hermes_dec(work):
    tools = Path(sys.executable).parent
    suffix = ".exe" if platform.system() == "Windows" else ""
    shim = "globalThis.print = console.log; new Function(require('fs').readFileSync(process.argv[1], 'utf8'))();"
    assert run("node", "-e", shim, str(SOURCE / "hbc_fixture.js")) == HBC_ORIGINAL_OUTPUT
    digests = {}
    for bytecode_version in HERMESC:
        compiler = hermesc(work, bytecode_version)
        bare, hbc = [work / f"fixture-{bytecode_version}-{level}.hbc" for level in ("g0", "g1")]
        for level, output in (("-g0", bare), ("-g1", hbc)):
            run(str(compiler), "-emit-binary", level, "-out", str(output), str(SOURCE / "hbc_fixture.js"))
            assert output.read_bytes()[8] == bytecode_version, "Unexpected HBC header version"
        parsed = subprocess.run([str(tools / ("hbc-file-parser" + suffix)), str(bare)], text=True, capture_output=True, check=True)
        assert f"| Version                      | {bytecode_version}" in parsed.stdout
        assert "not formally supported" in parsed.stderr
        # With backtrace location info (-g1), the header prints but debug-info parsing raises a TypeError.
        parsed = subprocess.run([str(tools / ("hbc-file-parser" + suffix)), str(hbc)], text=True, capture_output=True)
        assert parsed.returncode == 1 and f"| Version                      | {bytecode_version}" in parsed.stdout
        assert "debug_info_parser.py" in parsed.stderr and "TypeError" in parsed.stderr
        for binary in (bare, hbc):
            hasm, pseudo = binary.with_suffix(".hasm"), binary.with_suffix(".js")
            run(str(tools / ("hbc-disassembler" + suffix)), str(binary), str(hasm))
            run(str(tools / ("hbc-decompiler" + suffix)), str(binary), str(pseudo))
            listing, code = hasm.read_text(), pseudo.read_text()
            for needle in ('Function #1 "classify"', 'Function #2 "scaled"', "<Mod>", "'hbc-fixture-marker'"):
                assert needle in listing, (binary.name, needle)
            for needle in ("// Original name: classify", "// Original name: scaled", "'negative'", "'zero'", "'even'", "'odd'", "r0 = 7;"):
                assert needle in code, (binary.name, needle)
            # The pseudo-code shares register variables across functions, so running it does not reproduce the original.
            assert run("node", "-e", shim, str(pseudo)) == HBC_PSEUDOCODE_OUTPUT, binary.name
        digests[bytecode_version] = {"g0": sha256(bare), "g1": sha256(hbc)}
    return digests


def require_java(executable):
    try:
        completed = subprocess.run([executable, "-version"], text=True, capture_output=True, check=True)
    except FileNotFoundError as exc:
        raise SystemExit(
            f"{executable} was not found. Install JDK 17 or newer and retry."
        ) from exc
    except subprocess.CalledProcessError as exc:
        raise SystemExit(f"Cannot query {executable} version. Install JDK 17 or newer and retry.") from exc
    output = completed.stdout + completed.stderr
    match = re.search(r'\b(?:javac|(?:openjdk|java)(?:\s+version)?)\s+"?(\d+)(?:\.(\d+))?', output)
    major = int(match[2] if match and match[1] == "1" and match[2] else match[1]) if match else 0
    if major < 17:
        raise SystemExit(f"{executable} requires JDK 17 or newer; found {output.strip() or 'an unknown version'}.")

def rc4(key, data):
    """Independent RC4 used only to build the Malduck fixture."""
    state, j = list(range(256)), 0
    for i in range(256):
        j = (j + state[i] + key[i % len(key)]) & 0xFF
        state[i], state[j] = state[j], state[i]
    i = j = 0
    out = bytearray()
    for byte in data:
        i = (i + 1) & 0xFF
        j = (j + state[i]) & 0xFF
        state[i], state[j] = state[j], state[i]
        out.append(byte ^ state[(state[i] + state[j]) & 0xFF])
    return bytes(out)

def duck_sample(key=DUCK_KEY, marker=b"DKCFG1"):
    return b"\x00" * 64 + marker + DUCK_KEY + struct.pack("<H", len(DUCK_PLAIN)) + rc4(key, DUCK_PLAIN) + b"\x00" * 32

def verify_malduck(work):
    from malduck.extractor import ExtractManager, ExtractorModules

    modules = ExtractorModules(str(SOURCE / "malduck_modules"))
    results = {}
    for name, data in {"good": duck_sample(), "wrong-key": duck_sample(key=b"bad-key!"), "no-marker": duck_sample(marker=b"XXXXXX")}.items():
        path = work / f"duckcfg-{name}.bin"
        path.write_bytes(data)
        manager = ExtractManager(modules)
        results[name] = (manager.push_file(str(path)), manager.config)
    assert results["good"] == ("duckcfg", [DUCK_CONFIG]), results["good"]
    assert results["wrong-key"] == (None, []) and results["no-marker"] == (None, [])
    return sha256(work / "duckcfg-good.bin")

def trc1_frame(payload=b"trace"):
    """TRC1: magic, kind, big-endian payload length, payload, big-endian CRC-32 of the payload (built with struct and zlib)."""
    return b"TRC1\x01" + struct.pack(">H", len(payload)) + payload + struct.pack(">I", zlib.crc32(payload))


def trc1_valid(frame):
    length = struct.unpack(">H", frame[5:7])[0] if len(frame) >= 7 else -1
    payload = frame[7:-4]
    return frame[:5] == b"TRC1\x01" and len(payload) == length and frame[-4:] == struct.pack(">I", zlib.crc32(payload))


def recv_exactly(conn, size):
    """Read size bytes, or fewer only if the peer disconnects first."""
    data = b""
    while len(data) < size:
        chunk = conn.recv(size - len(data))
        if not chunk:
            break
        data += chunk
    return data


class Trc1Server(threading.Thread):
    """Localhost TRC1 server: replies OK plus the CRC to valid frames, or stops listening on a payload over crash_over bytes."""

    def __init__(self, crash_over=None):
        super().__init__(daemon=True)
        self.crash_over, self.frames, self.replies, self.crashed = crash_over, [], [], False
        self.stopping = threading.Event()
        self.sock = socket.create_server(("127.0.0.1", 0))
        self.sock.settimeout(0.1)  # lets run() notice stop() between connections

    def stop(self):
        self.stopping.set()
        self.join(timeout=5)
        self.sock.close()

    def run(self):
        while not (self.crashed or self.stopping.is_set()):
            try:
                conn, _ = self.sock.accept()
            except socket.timeout:
                continue
            except OSError:
                return
            with conn:
                conn.settimeout(5)
                frame = recv_exactly(conn, 7)
                if len(frame) == 7:
                    frame += recv_exactly(conn, struct.unpack(">H", frame[5:7])[0] + 4)
                # A frame cut short by a disconnect is recorded as received and fails trc1_valid.
                self.frames.append(frame)
                if self.crash_over is not None and len(frame) - 11 > self.crash_over:
                    self.crashed = True
                    self.sock.close()
                    return
                reply = b"OK" + frame[-4:] if trc1_valid(frame) else b"BAD"
                self.replies.append(reply)
                conn.sendall(reply)


def fuzz_trc1(work, crash_over=None, **options):
    from boofuzz import Block, Byte, Checksum, FuzzLoggerCsv, Request, Session, Size, Static, String, Target, TCPSocketConnection

    request = Request("trc1", children=(
        Static(name="magic", default_value=b"TRC1"),
        Byte(name="kind", default_value=1, fuzzable=False),
        Size(name="length", block_name="body", length=2, endian=">", fuzzable=False),
        Block(name="body", children=(String(name="payload", default_value="trace", max_len=48),)),
        Checksum(name="crc", block_name="body", algorithm="crc32", endian=">", fuzzable=False),
    ))
    server = Trc1Server(crash_over)
    server.start()
    sent, received, log = [], [], io.StringIO()

    def record(target, fuzz_data_logger, session, *args, **kwargs):
        sent.append(session.last_send)
        received.append(session.last_recv)

    try:
        session = Session(
            target=Target(connection=TCPSocketConnection("127.0.0.1", server.sock.getsockname()[1], recv_timeout=2)),
            web_port=None, fuzz_loggers=[FuzzLoggerCsv(file_handle=log)], db_filename=str(work / f"boofuzz-{len(list(work.glob('boofuzz-*')))}.db"),
            sleep_time=0, restart_sleep_time=0, post_test_case_callbacks=[record], **options,
        )
        session.connect(request)
        session.fuzz(max_depth=1)
    finally:
        server.stop()
    rows = list(csv.reader(io.StringIO(log.getvalue())))
    return request.render(), server, sent, received, rows


def verify_boofuzz(work):
    rendered, server, sent, received, _ = fuzz_trc1(work, receive_data_after_fuzz=True)
    assert rendered == trc1_frame(), rendered.hex()
    assert len(server.frames) == TRC1_CASES and sent == server.frames and received == server.replies
    assert all(trc1_valid(frame) for frame in server.frames), "a fuzzed frame has a wrong length or CRC"
    # String mutations are text: b"\xde\xad\xbe\xef" patterns are sent UTF-8 encoded, and max_len counts characters.
    longest = max(server.frames, key=len)
    assert len(longest) - 11 == 96 and longest[7:15] == "\xde\xad\xbe\xef".encode()
    # By default, replies to fuzzed messages are not read.
    _, _, _, default_received, _ = fuzz_trc1(work, index_end=5)
    assert default_received == [b""] * 5, default_received
    # Without a restart method or monitor, a target that stops listening ends the run early with only an info message.
    _, crashed, _, _, rows = fuzz_trc1(work, crash_over=40, restart_threshold=1)
    kinds = [row[1] for row in rows]
    assert crashed.crashed and len(crashed.frames) < TRC1_CASES and "fail" not in kinds and "error" not in kinds
    assert any("Ending fuzzing" in row[-1] for row in rows)
    return {"cases": TRC1_CASES, "frames_before_target_stopped": len(crashed.frames), "default_frame": rendered.hex()}


def memprocfs_host():
    # The pinned wheels are Linux x86-64 and Windows x64; only Linux x86-64 is exercised here.
    return platform.system() == "Linux" and platform.machine() == "x86_64"


def keystone_host():
    # Keystone 0.9.2 has no ARM-host wheels (pip would build it from source); only Linux x86-64 is exercised here.
    return platform.system() == "Linux" and platform.machine() == "x86_64"


def required_packages():
    packages = {"construct": "2.10.70", "scapy": "2.8.0", "yara-x": "1.21.0", "hermes-dec": "0.1.8", "malduck": "4.4.1", "boofuzz": "0.4.2", "esptool": "5.6.0"}
    if memprocfs_host():
        packages.update(MEMPROCFS_PACKAGES)
    if keystone_host():
        packages.update(KEYSTONE_PACKAGES)
    return packages


def memprocfs_env(leechcore_dir):
    """Prepend leechcore.so's directory, keeping any library path the host already needs."""
    existing = os.environ.get("LD_LIBRARY_PATH")
    return dict(os.environ, LD_LIBRARY_PATH=os.pathsep.join([str(leechcore_dir), existing] if existing else [str(leechcore_dir)]))


def memprocfs_image(path):
    image = bytearray(16 * 1024 * 1024)
    indexes = [(FIXTURE_VA >> shift) & 0x1FF for shift in (39, 30, 21, 12)]
    for table, entry, index in zip((PML4, PDPT, PD, PT), (PDPT, PD, PT, PAGE), indexes):
        image[table + index * 8:table + index * 8 + 8] = struct.pack("<Q", entry | 0x7)
    image[0x1000:0x1010] = b"MPFS-PHYS-MARK-1"
    image[PAGE + 0x678:PAGE + 0x688] = b"MPFS-VIRT-MARK-2"
    path.write_bytes(image)


def verify_memprocfs(work):
    if not ctypes.util.find_library("usb-1.0"):
        raise SystemExit("MemProcFS needs the libusb-1.0 system library; install it (for example `sudo apt-get install libusb-1.0-0`) and retry.")
    import leechcorepyc

    image = work / "memprocfs.raw"
    memprocfs_image(image)
    # The memprocfs wheel does not bundle leechcore.so; leechcorepyc provides it.
    env = memprocfs_env(Path(leechcorepyc.__file__).parent)
    output = run(sys.executable, str(SOURCE / "memprocfs_probe.py"), str(image), hex(PML4), hex(FIXTURE_VA), env=env)
    observed = json.loads(output.splitlines()[-1])
    assert bytes.fromhex(observed["physical"]) == b"MPFS-PHYS-MARK-1" == bytes.fromhex(observed["pmem_file"])
    assert observed["processes"] == [[1, "unknown_process", PML4]], observed["processes"]
    assert bytes.fromhex(observed["virtual"]) == b"MPFS-VIRT-MARK-2" and observed["virt2phys"] == PAGE + 0x678
    assert "memory.pmem" in observed["root"]
    return sha256(image)


def verify_keystone():
    import capstone
    import keystone

    cases = [
        (keystone.KS_ARCH_X86, keystone.KS_MODE_64, capstone.CS_ARCH_X86, capstone.CS_MODE_64, X64_SOURCE, X64_BYTES),
        (keystone.KS_ARCH_ARM64, keystone.KS_MODE_LITTLE_ENDIAN, capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM, A64_SOURCE, A64_BYTES),
    ]
    for ks_arch, ks_mode, cs_arch, cs_mode, source, expected in cases:
        assembler = keystone.Ks(ks_arch, ks_mode)
        encoding, count = assembler.asm(source, ASM_BASE)
        assert bytes(encoding).hex() == expected and count == source.count(";") + 1, (source, bytes(encoding).hex(), count)
        text = "; ".join(f"{insn.mnemonic} {insn.op_str}".strip() for insn in capstone.Cs(cs_arch, cs_mode).disasm(bytes.fromhex(expected), ASM_BASE))
        assert text == source, text
        assert bytes(assembler.asm(text, ASM_BASE)[0]).hex() == expected

    x64 = keystone.Ks(keystone.KS_ARCH_X86, keystone.KS_MODE_64)
    # RIP operands contain a literal displacement; changing the base does not relocate it.
    for base in (0x1000, 0x2000):
        assert bytes(x64.asm("mov eax, dword ptr [rip + 8]", base)[0]).hex() == "8b0508000000"
    arm64 = keystone.Ks(keystone.KS_ARCH_ARM64, keystone.KS_MODE_LITTLE_ENDIAN)
    # Relative branches are encoded against the address passed to asm().
    assert bytes(arm64.asm("b #0x1010", 0x2000)[0]).hex() == A64_BACKWARD_BRANCH
    try:
        keystone.Ks(keystone.KS_ARCH_X86, keystone.KS_MODE_64).asm("foo eax")
    except keystone.KsError as exc:
        assert exc.errno == keystone.KS_ERR_ASM_MNEMONICFAIL, exc.errno
    else:
        raise AssertionError("Unknown mnemonic unexpectedly assembled")
    # An immediate that one MOV cannot encode fails with errno 561, which the 0.9.2 binding reports as "Unknown error".
    try:
        arm64.asm("mov x0, #0x12345678")
    except keystone.KsError as exc:
        assert exc.errno == 561 and str(exc) == "Unknown error", (exc.errno, str(exc))
    else:
        raise AssertionError("Unencodable immediate unexpectedly assembled")


def esp_image(chip_id=0):
    """Self-authored ESP32 application image: 8-byte header, 16-byte extended header, two segments, checksum, SHA-256."""
    image = bytearray(struct.pack("<BBBBI", 0xE9, len(ESP_SEGMENTS), 2, 0x20, ESP_ENTRY))  # DIO, 4MB at 40m
    image += struct.pack("<B3sHBHH4sB", 0xEE, bytes(3), chip_id, 0, 0, 0xFFFF, bytes(4), 1)  # WP pin disabled, hash appended
    total = 0xEF
    for address, data in ESP_SEGMENTS:
        image += struct.pack("<II", address, len(data)) + data
        for byte in data:
            total ^= byte
    image += bytes(15 - len(image) % 16) + bytes([total])
    return bytes(image + hashlib.sha256(image).digest())


def image_info(path, *chip):
    """Run the documented CLI offline; image-info opens no serial port."""
    completed = subprocess.run([sys.executable, "-m", "esptool", *chip, "image-info", str(path)], text=True, capture_output=True)
    return completed.returncode, completed.stdout + completed.stderr


def verify_esptool(work):
    app = work / "esp32-app.bin"
    app.write_bytes(esp_image())
    assert hashlib.sha256(app.read_bytes()[:-32]).hexdigest() == ESP_DIGEST and app.read_bytes()[95] == ESP_CHECKSUM
    code, out = image_info(app)
    assert code == 0, out
    for line in ("Detected image type: ESP32", "Entry point: 0x40080400", "Segments: 2", "Flash size: 4MB", "Flash mode: DIO", "Chip ID: 0 (ESP32)",
                 f"Checksum: {ESP_CHECKSUM:#x} (valid)", f"Validation hash: {ESP_DIGEST} (valid)"):
        assert line in out, (line, out)
    rows = re.findall(r"^\s*(\d+)\s+(0x[0-9a-f]+)\s+(0x[0-9a-f]+)\s+(0x[0-9a-f]+)\s+(.+?)\s*$", out, re.M)
    assert [row[:4] for row in rows] == [("0", "0x00010", "0x3ffb0000", "0x00000018"), ("1", "0x00020", "0x40080400", "0x00000030")], rows
    assert "DRAM" in rows[0][4] and "IRAM" in rows[1][4], rows

    s3 = work / "esp32s3-app.bin"
    s3.write_bytes(esp_image(chip_id=9))
    code, out = image_info(s3)
    assert code == 0 and "Detected image type: ESP32-S3" in out and "Chip ID: 9 (ESP32-S3)" in out, out

    # A corrupted image is reported as invalid, but the command still exits 0.
    corrupt = bytearray(app.read_bytes())
    corrupt[32] ^= 1
    bad = work / "esp32-corrupt.bin"
    bad.write_bytes(corrupt)
    code, out = image_info(bad)
    assert code == 0, out
    assert f"Checksum: {ESP_CHECKSUM:#x} (invalid - calculated {ESP_CORRUPT_CHECKSUM:#x})" in out and f"Validation hash: {ESP_CORRUPT_DIGEST} (invalid)" in out, out

    truncated = work / "esp32-truncated.bin"
    truncated.write_bytes(app.read_bytes()[:40])
    code, out = image_info(truncated)
    assert code == 2 and "End of file reading segment 0x3ffb0000, length 16 (actual length 8)" in out, (code, out)

    # --chip overrides the header's chip ID without a warning; the memory map follows --chip.
    code, out = image_info(app, "--chip", "esp32s3")
    assert code == 0 and "ESP32-S3 Image Header" in out and "Chip ID: 0 (ESP32)" in out and "warn" not in out.lower(), out
    assert f"Checksum: {ESP_CHECKSUM:#x} (valid)" in out and f"Validation hash: {ESP_DIGEST} (valid)" in out, out
    forced = re.findall(r"^\s*\d+\s+0x[0-9a-f]+\s+0x[0-9a-f]+\s+0x[0-9a-f]+\s+(.+?)\s*$", out, re.M)
    assert forced == ["MEM_INTERNAL", "MEM_INTERNAL"], forced
    return sha256(app)


def verify_cfr(work, cfr_jar):
    """Compile -> decompile -> rebuild Shapes.java with CFR, with and without --sealed true."""
    if cfr_jar is None:
        cfr_jar = work / "cfr-0.152.jar"
        with urlopen(CFR_URL, timeout=60) as response:
            cfr_jar.write_bytes(response.read())
    assert sha256(cfr_jar) == CFR_SHA256, "CFR artifact digest mismatch"
    original = work / "cfr-original"
    original.mkdir()
    run("javac", "--release", "17", "-d", str(original), str(SOURCE / "Shapes.java"), str(SOURCE / "SealedProbe.java"))
    assert run("java", "-cp", str(original), "Shapes") == SHAPES_OUTPUT
    assert run("java", "-cp", str(original), "SealedProbe") == "true:3"

    sealed = {}
    for name, flags in (("default", []), ("sealed", ["--sealed", "true"])):
        decompiled, rebuilt = work / f"cfr-{name}-src", work / f"cfr-{name}-rebuilt"
        decompiled.mkdir()
        rebuilt.mkdir()
        run("java", "-jar", str(cfr_jar), str(original / "Shapes.class"), "--outputdir", str(decompiled), *flags)
        source = (decompiled / "Shapes.java").read_text()
        run("javac", "--release", "17", "-d", str(rebuilt), str(decompiled / "Shapes.java"), str(SOURCE / "SealedProbe.java"))
        assert run("java", "-cp", str(rebuilt), "Shapes") == SHAPES_OUTPUT
        sealed[name] = run("java", "-cp", str(rebuilt), "SealedProbe")
        if name == "default":
            # For Java 17 class files CFR 0.152 treats sealed as experimental and leaves it off unless asked.
            assert "permits" not in source and "Uses 'sealed' constructs - enablewith --sealed true" in source, source
        else:
            assert "sealed interface Shape" in source and "permits Circle, Square, Rect" in source, source
    assert sealed == {"default": "false:0", "sealed": "true:3"}, sealed
    return {"artifact": {"url": CFR_URL, "sha256": CFR_SHA256}, "output": SHAPES_OUTPUT, "rebuilt_is_sealed": sealed}


def verify(work, jar, cfr_jar=None):
    for package, expected in required_packages().items():
        try:
            installed = version(package)
        except PackageNotFoundError as exc:
            raise SystemExit(
                f'Missing Python dependency: {package}. Install with `"{sys.executable}" -m pip install -r "{SOURCE / "requirements.txt"}"`.'
            ) from exc
        if installed != expected:
            raise SystemExit(f"Expected {package}=={expected}, found {installed}. Install the pinned requirements from {SOURCE / 'requirements.txt'}.")

    require_java("javac")
    require_java("java")
    try:
        run("node", "--version")
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        raise SystemExit("Node.js is required for the Hermes fixture; install Node.js 22 LTS and retry.") from exc

    from construct import Byte, Bytes, Const, ConstructError, Int16ul, Struct, Terminated
    from scapy.all import Ether, IP, Raw, UDP, rdpcap, wrpcap
    import yara_x

    schema = Struct(
        "magic" / Const(b"SMK1"), "length" / Int16ul, "kind" / Byte,
        "payload" / Bytes(lambda ctx: ctx.length), Terminated,
    )
    parsed = schema.parse(GOLDEN)
    assert parsed.length == 5 and parsed.kind == 1 and parsed.payload == b"trace"
    assert schema.build(dict(length=5, kind=1, payload=b"trace")) == GOLDEN
    for bad in (GOLDEN[:-1], GOLDEN + b"\x00", b"WRNG" + GOLDEN[4:]):
        try:
            schema.parse(bad)
        except ConstructError:
            continue
        raise AssertionError("Malformed fixture accepted")

    packet = (
        Ether(src="02:00:00:00:00:01", dst="02:00:00:00:00:02")
        / IP(src="192.0.2.1", dst="192.0.2.2")
        / UDP(sport=1234, dport=4321) / Raw(b"trace")
    )
    wire = bytes(packet)
    assert len(wire) == 47 and wire[:14] == bytes.fromhex("0200000000020200000000010800")
    assert checksum(wire[14:34]) == 0
    pseudo_header = bytes.fromhex("c0000201c0000202") + struct.pack("!BBH", 0, 17, 13)
    assert checksum(pseudo_header + wire[34:]) == 0
    assert Ether(wire)[UDP].dport == 4321 and bytes(Ether(wire)[Raw]) == b"trace"
    pcap = work / "trace.pcap"
    wrpcap(str(pcap), [packet])
    packets = rdpcap(str(pcap))
    assert len(packets) == 1 and packets[0][IP].src == "192.0.2.1"
    assert bytes(packets[0][Raw]) == b"trace"

    compiler = yara_x.Compiler()
    compiler.add_source('rule Fixture { strings: $a = "trace" condition: $a and uint16(0) == 0x4d53 }')
    scanner = yara_x.Scanner(compiler.build())
    assert [r.identifier for r in scanner.scan(GOLDEN).matching_rules] == ["Fixture"]
    assert list(scanner.scan(b"negative sample").matching_rules) == []
    bad_compiler = yara_x.Compiler()
    try:
        bad_compiler.add_source("rule Bad { strings: $a = /abc{/ condition: $a }")
    except Exception as exc:
        assert type(exc).__name__ == "CompileError", type(exc).__name__
    else:
        raise AssertionError("Unescaped brace unexpectedly compiled")

    if jar is None:
        jar = work / "vineflower-1.12.0.jar"
        with urlopen(JAR_URL, timeout=60) as response:
            jar.write_bytes(response.read())
    assert sha256(jar) == JAR_SHA256, "Vineflower artifact digest mismatch"
    original, decompiled, rebuilt = [work / name for name in ("original", "decompiled", "rebuilt")]
    for directory in (original, decompiled, rebuilt):
        directory.mkdir()
    run("javac", "--release", "17", "-d", str(original), str(SOURCE / "BranchDemo.java"), str(SOURCE / "Probe.java"))
    run("java", "-jar", str(jar), str(original), str(decompiled))
    run("javac", "--release", "17", "-d", str(rebuilt), str(decompiled / "BranchDemo.java"), str(SOURCE / "Probe.java"))
    for classes in (original, rebuilt):
        assert run("java", "-cp", str(classes), "BranchDemo") == "25"
        assert run("java", "-cp", str(classes), "Probe") == EXPECTED_BRANCHES
    cfr_summary = verify_cfr(work, cfr_jar)

    duck_digest = verify_malduck(work)
    hbc_digests = verify_hermes_dec(work)
    boofuzz_summary = verify_boofuzz(work)
    esp_digest = verify_esptool(work)
    keystone_result = {"name": "Keystone", "version": "0.9.2", "result": "skipped", "scope": "This check runs on Linux x86-64 only"}
    if keystone_host():
        verify_keystone()
        keystone_result.update(result="passed", scope="x86-64 and ARM64: hand-encoded bytes, Capstone 5.0.9 disassembly and reassembly, base-relative branch versus literal RIP displacement, mnemonic error code; an unencodable ARM64 immediate reports errno 561 as \"Unknown error\"")
    memprocfs = {"name": "MemProcFS", "version": "5.19.0", "result": "skipped", "scope": "This check runs on Linux x86-64 only"}
    image_digest = None
    if memprocfs_host():
        image_digest = verify_memprocfs(work)
        memprocfs.update(result="passed", scope="Self-authored raw image: physical read, user-supplied DTB fallback process, virtual read, virt2phys, /memory.pmem; no Windows OS analysis")

    return {
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "host": {"platform": platform.platform(), "python": platform.python_version(), "javac": run("javac", "-version"), "node": run("node", "--version")},
        "results": [
            {"name": "Construct", "version": "2.10.70", "result": "passed", "scope": "Golden bytes, parse/build, wrong magic, truncation, trailing-data rejection"},
            {"name": "Scapy", "version": "2.8.0", "result": "passed", "scope": "Offline packet/PCAP round trip and independent IP/UDP checksums; no traffic sent"},
            {"name": "YARA-X", "version": "1.21.0", "result": "passed", "scope": "Python API positive/negative matching and strict-regex CompileError"},
            {"name": "Vineflower", "version": "1.12.0", "result": "passed", "scope": "Java 17 record/switch expression, rebuild, main output and five branch vectors"},
            {"name": "CFR", "version": "0.152", "result": "passed", "scope": "Synthetic Java 17 sealed interface, records, instanceof patterns, switch yield and text block: rebuilt output matches; by default the rebuilt interface is no longer sealed, and --sealed true restores it"},
            {"name": "Malduck", "version": "4.4.1", "result": "passed", "scope": "Self-authored YARA-triggered extractor and RC4 config; wrong-key and no-marker samples yield no config"},
            {"name": "hermes-dec", "version": "0.1.8", "result": "passed", "scope": "HBC 98/99 at -g0/-g1: header, disassembly and pseudo-code landmarks; -g1 debug-info parsing raises TypeError; executing the pseudo-code prints 21, not 25"},
            {"name": "boofuzz", "version": "0.4.2", "result": "passed", "scope": "Localhost TRC1 protocol: default frame, 575 payload mutations with correct length/CRC, sent and replied frames match; replies unread by default, UTF-8 string mutations, and a stopped target ends the run without a failure"},
            memprocfs,
            keystone_result,
            {"name": "esptool", "version": "5.6.0", "result": "passed", "scope": "Offline image-info on a synthetic ESP32 image: header, segments, checksum and SHA-256; chip ID 9 is auto-detected as ESP32-S3; checksum/hash mismatches exit 0, a truncated segment exits 2, and --chip overrides the header chip ID without a warning while the checksum and hash stay valid"},
        ],
        "inputs": [{"path": name, "sha256": sha256(SOURCE / name)} for name in ("BranchDemo.java", "Probe.java", "Shapes.java", "SealedProbe.java", "hbc_fixture.js", "malduck_modules/duckcfg/__init__.py", "malduck_modules/duckcfg/duckcfg.yar", "memprocfs_probe.py", "verify.py", "requirements.txt")],
        "golden_hex": GOLDEN.hex(),
        "vineflower_artifact": {"url": JAR_URL, "sha256": JAR_SHA256},
        "cfr": cfr_summary,
        "expected_main": "25", "expected_branches": EXPECTED_BRANCHES.splitlines(),
        "malduck": {"sample_sha256": duck_digest, "expected_config": DUCK_CONFIG},
        "hermes_dec": {"compilers": {str(v): {"url": u, "sha256": d} for v, (u, d) in HERMESC.items()},
                       "hbc_sha256": {str(v): d for v, d in hbc_digests.items()},
                       "original_output": HBC_ORIGINAL_OUTPUT, "pseudocode_output": HBC_PSEUDOCODE_OUTPUT},
        "boofuzz": boofuzz_summary,
        "memprocfs": {"image_sha256": image_digest, "dtb": hex(PML4), "virtual_address": hex(FIXTURE_VA), "physical_address": hex(PAGE + 0x678)},
        "keystone": {"base": hex(ASM_BASE), "x64": {"source": X64_SOURCE, "bytes": X64_BYTES},
                     "arm64": {"source": A64_SOURCE, "bytes": A64_BYTES, "backward_branch_at_0x2000": A64_BACKWARD_BRANCH}},
        "esptool": {"image_sha256": esp_digest, "entry": hex(ESP_ENTRY), "checksum": hex(ESP_CHECKSUM), "validation_hash": ESP_DIGEST,
                    "corrupt_checksum": hex(ESP_CORRUPT_CHECKSUM), "corrupt_validation_hash": ESP_CORRUPT_DIGEST},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="Directory for results and generated example artifacts")
    parser.add_argument("--vineflower-jar", type=Path, help="Optional existing 1.12.0 JAR; its digest is still checked")
    parser.add_argument("--cfr-jar", type=Path, help="Optional existing CFR 0.152 JAR; its digest is still checked")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    jar = args.vineflower_jar.resolve() if args.vineflower_jar else None
    work = Path(tempfile.mkdtemp(prefix="run-", dir=args.output))
    report = verify(work, jar, args.cfr_jar.resolve() if args.cfr_jar else None)
    (args.output / "results.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()

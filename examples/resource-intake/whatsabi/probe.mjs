import { whatsabi } from "@shazow/whatsabi";

// Hand-built jump table. Selectors are keccak256("foo()") and keccak256("bar(uint256)"), first 4 bytes.
// The PUSH1 targets are not JUMPDESTs, so this is selector recovery only.
const dispatcher =
  "0x63c29855788114600e57630423a1328114601657600080fd5b5b";
// PUSH4 that is not followed by the JUMPI table pattern.
const lone = "0x63deadbeef00";

const selectors = whatsabi.selectorsFromBytecode(dispatcher);
const abi = whatsabi.abiFromBytecode(dispatcher);
const loneSelectors = whatsabi.selectorsFromBytecode(lone);

if (JSON.stringify(selectors) !== JSON.stringify(["0xc2985578", "0x0423a132"])) {
  throw new Error("dispatcher selectors " + JSON.stringify(selectors));
}
if (abi.length !== 0) {
  throw new Error("expected no ABI without valid JUMPDESTs " + JSON.stringify(abi));
}
if (loneSelectors.length !== 0) {
  throw new Error("lone PUSH4 was treated as a selector " + JSON.stringify(loneSelectors));
}

process.stdout.write(JSON.stringify({
  selectors,
  abi,
  lone_push4: loneSelectors,
}) + "\n");

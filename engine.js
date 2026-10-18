// Base Math engine - convert a whole number between bases, show two's complement, and count what digits hold.
// Mirrored by oracle.py; keep the op order identical.
// Bases run 2 to 36 with digits 0-9 then a-z. Converted numbers are whole, up to 64 typed digits.

var DIGITS = "0123456789abcdefghijklmnopqrstuvwxyz";

function _base(b, label) {
  if (typeof b !== "number" || !isFinite(b) || Math.floor(b) !== b || b < 2 || b > 36) {
    throw new Error(label + " must be a whole number from 2 to 36");
  }
  return b;
}

function _toBig(text, base) {
  if (typeof text !== "string") throw new Error("enter a number to convert");
  var t = text.replace(/\s+/g, "").toLowerCase();
  if (t.length === 0) throw new Error("enter a number to convert");
  if (t.length > 64) throw new Error("the number can have at most 64 digits");
  var v = 0n, B = BigInt(base);
  for (var i = 0; i < t.length; i++) {
    var d = DIGITS.indexOf(t.charAt(i));
    if (d < 0 || d >= base) throw new Error("'" + t.charAt(i) + "' is not a digit in base " + base);
    v = v * B + BigInt(d);
  }
  return { text: t, value: v };
}

function _fromBig(v, base) {
  if (v === 0n) return "0";
  var B = BigInt(base), s = "";
  while (v > 0n) { s = DIGITS.charAt(Number(v % B)) + s; v = v / B; }
  return s;
}

// The convert truth: the same number written in another base.
function convertTruth(text, fromBase, toBase) {
  var f = _base(fromBase, "from base"), t = _base(toBase, "to base");
  var p = _toBig(text, f);
  return p.text + " in base " + f + " is " + _fromBig(p.value, t) + " in base " + t + ".";
}

// The twos truth: how a whole number is stored in a fixed number of bits.
function twosTruth(value, bits) {
  if (typeof value !== "number" || !isFinite(value) || Math.floor(value) !== value || Math.abs(value) > 1e12) {
    throw new Error("value must be a whole number");
  }
  if (bits !== 4 && bits !== 8 && bits !== 16 && bits !== 32) throw new Error("bit width must be 4, 8, 16 or 32");
  var v = BigInt(value), span = 1n << BigInt(bits), half = span >> 1n;
  if (v < -half || v >= half) {
    return String(value) + " does not fit in " + bits + " bits, which hold " + (-half).toString() + " to " + (half - 1n).toString() + ".";
  }
  var u = v < 0n ? span + v : v;
  var bin = _fromBig(u, 2), hex = _fromBig(u, 16);
  while (bin.length < bits) bin = "0" + bin;
  while (hex.length < bits / 4) hex = "0" + hex;
  return String(value) + " fits in " + bits + " bits as " + bin + " (hex " + hex + "). Read as an unsigned number, that pattern is " + u.toString() + ".";
}

// The capacity truth: the range a number of digits can hold in a base.
function capacityTruth(digits, base) {
  if (typeof digits !== "number" || !isFinite(digits) || Math.floor(digits) !== digits || digits < 1 || digits > 64) {
    throw new Error("digits must be a whole number from 1 to 64");
  }
  var b = _base(base, "base");
  var n = BigInt(b) ** BigInt(digits);
  return digits + (digits === 1 ? " digit" : " digits") + " in base " + b + (digits === 1 ? " holds" : " hold") + " 0 to " + (n - 1n).toString() + ", which is " + n.toString() + " values.";
}

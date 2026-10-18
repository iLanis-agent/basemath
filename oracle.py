#!/usr/bin/env python3
# Base Math oracle - mirrors engine.js.
import json, math, re

DIGITS = "0123456789abcdefghijklmnopqrstuvwxyz"

def _base(b, label):
    if isinstance(b, bool) or not isinstance(b, (int, float)) or not math.isfinite(b) or math.floor(b) != b or b < 2 or b > 36:
        raise ValueError(f"{label} must be a whole number from 2 to 36")
    return int(b)

def _to_big(text, base):
    if not isinstance(text, str):
        raise ValueError("enter a number to convert")
    t = re.sub(r"\s+", "", text).lower()
    if len(t) == 0:
        raise ValueError("enter a number to convert")
    if len(t) > 64:
        raise ValueError("the number can have at most 64 digits")
    v = 0
    for ch in t:
        d = DIGITS.find(ch)
        if d < 0 or d >= base:
            raise ValueError(f"'{ch}' is not a digit in base {base}")
        v = v * base + d
    return t, v

def _from_big(v, base):
    if v == 0:
        return "0"
    s = ""
    while v > 0:
        s = DIGITS[v % base] + s
        v //= base
    return s

def convert_truth(text, from_base, to_base):
    f = _base(from_base, "from base"); t = _base(to_base, "to base")
    txt, v = _to_big(text, f)
    return f"{txt} in base {f} is {_from_big(v, t)} in base {t}."

def twos_truth(value, bits):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or math.floor(value) != value or abs(value) > 1e12:
        raise ValueError("value must be a whole number")
    if bits not in (4, 8, 16, 32):
        raise ValueError("bit width must be 4, 8, 16 or 32")
    v = int(value); span = 1 << bits; half = span >> 1
    if v < -half or v >= half:
        return f"{v} does not fit in {bits} bits, which hold {-half} to {half - 1}."
    u = span + v if v < 0 else v
    bn = _from_big(u, 2).rjust(bits, "0"); hx = _from_big(u, 16).rjust(bits // 4, "0")
    return f"{v} fits in {bits} bits as {bn} (hex {hx}). Read as an unsigned number, that pattern is {u}."

def capacity_truth(digits, base):
    if isinstance(digits, bool) or not isinstance(digits, (int, float)) or not math.isfinite(digits) or math.floor(digits) != digits or digits < 1 or digits > 64:
        raise ValueError("digits must be a whole number from 1 to 64")
    digits = int(digits)
    b = _base(base, "base")
    n = b ** digits
    return f"{digits} {'digit' if digits == 1 else 'digits'} in base {b} {'holds' if digits == 1 else 'hold'} 0 to {n - 1}, which is {n} values."

FNS = {"convertTruth": convert_truth, "twosTruth": twos_truth, "capacityTruth": capacity_truth}
CASES = [
    ("convertTruth", ["ff", 16, 10]), ("convertTruth", ["255", 10, 2]), ("convertTruth", ["11111111", 2, 16]), ("convertTruth", ["0", 10, 2]),
    ("convertTruth", ["zz", 36, 10]), ("convertTruth", ["FF", 16, 8]), ("convertTruth", ["007", 10, 10]), ("convertTruth", [" 1 0 1 ", 2, 10]),
    ("convertTruth", ["1" * 64, 2, 16]), ("convertTruth", ["z" * 64, 36, 10]), ("convertTruth", ["100", 36, 2]), ("convertTruth", ["777", 8, 16]),
    ("convertTruth", ["12", 2, 10]), ("convertTruth", ["g", 16, 10]), ("convertTruth", ["-5", 10, 2]), ("convertTruth", ["", 10, 2]), ("convertTruth", ["1" * 65, 2, 10]),
    ("convertTruth", ["10", 1, 10]), ("convertTruth", ["10", 10, 37]), ("convertTruth", ["10", 10.5, 2]), ("convertTruth", [None, 10, 2]),
    ("twosTruth", [-5, 8]), ("twosTruth", [5, 8]), ("twosTruth", [0, 8]), ("twosTruth", [127, 8]), ("twosTruth", [128, 8]), ("twosTruth", [-128, 8]), ("twosTruth", [-129, 8]),
    ("twosTruth", [-1, 32]), ("twosTruth", [2147483647, 32]), ("twosTruth", [2147483648, 32]), ("twosTruth", [-2147483648, 32]), ("twosTruth", [-1, 4]), ("twosTruth", [7, 4]), ("twosTruth", [8, 4]),
    ("twosTruth", [-300, 16]), ("twosTruth", [1.5, 8]), ("twosTruth", [5, 7]), ("twosTruth", [10**13, 32]),
    ("capacityTruth", [8, 2]), ("capacityTruth", [1, 10]), ("capacityTruth", [2, 16]), ("capacityTruth", [64, 2]), ("capacityTruth", [64, 36]), ("capacityTruth", [4, 10]),
    ("capacityTruth", [1, 2]), ("capacityTruth", [0, 2]), ("capacityTruth", [65, 2]), ("capacityTruth", [8, 1]), ("capacityTruth", [8, 37]), ("capacityTruth", [2.5, 10]),
]

out = []
for fn, args in CASES:
    try:
        exp = FNS[fn](*args)
    except ValueError as e:
        exp = "ERR:" + str(e)
    out.append({"fn": fn, "args": args, "expected": exp})
with open("expected.json", "w") as f:
    json.dump(out, f, indent=1)
    f.write("\n")
print(len(out), "cases")

# Base Math

Number base arithmetic. 255 and ff are the same number wearing different digits.

## What it computes

- **The convert truth** - a whole number written in another base, 2 to 36, digits 0-9 then a-z, up to 64 digits. Exact, with big integers.
- **The twos truth** - how a whole number is stored in 4, 8, 16 or 32 bits in two's complement: the bit pattern, its hex, its unsigned reading, or the range that width holds when it does not fit.
- **The capacity truth** - the range and count of values that 1 to 64 digits hold in a base.

## Boundary

Arithmetic only. Base Math does not know which base, width or signed format a language, file or device uses. Check those where they apply.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic.
- `oracle.py` - the Python mirror that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json` (51 cases).
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/basemath/
Repo: https://github.com/iLanis-agent/basemath

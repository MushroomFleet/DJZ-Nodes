# StringPainter

This custom node generates hexadecimal string values based on a seed value. It can operate in either increment mode (using the provided seed directly) or random mode (generating random hex values). The node is useful for creating unique identifiers or hash-like strings for painting or procedural generation purposes.

## Input Parameters

- **seed** (Required)
  - Default: 0
  - Range: 0 to 0xFFFFFFFF (4294967295)
  - The base value used to generate the hex string
  - In increment mode, this value is directly converted to hex
  - In random mode, this value is ignored and a random value is generated instead

- **bits** (Required)
  - Options: "16", "32"
  - Default: "16"
  - Determines the length of the output hex string:
    - 16-bit: Produces a 4-character hex string (0000-FFFF)
    - 32-bit: Produces an 8-character hex string (00000000-FFFFFFFF)

- **mode** (Required)
  - Options: "increment", "random"
  - Default: "increment"
  - Determines how the hex string is generated:
    - `increment`: Uses the provided seed value directly
    - `random`: Generates a random value between 0 and 0xFFFFFFFF

## Output

1. **STRING**
   - A hexadecimal string representation
   - Length depends on the bits parameter:
     - 16-bit: 4 characters (e.g., "3039")
     - 32-bit: 8 characters (e.g., "00003039")
   - Always uses uppercase letters for hex digits A-F

## Usage Examples

1. **16-bit Increment Mode**
   - Set bits to "16"
   - Set mode to "increment"
   - Set seed to 12345
   - Output: "3039" (12345 in hex, truncated to 16 bits)

2. **32-bit Increment Mode**
   - Set bits to "32"
   - Set mode to "increment"
   - Set seed to 12345
   - Output: "00003039" (12345 in hex, padded to 32 bits)

3. **Random Mode**
   - Set mode to "random"
   - The seed value is ignored
   - Each execution generates a new random hex string
   - Length depends on the bits setting (4 or 8 characters)

## Notes

- The node always outputs uppercase hexadecimal values
- In 16-bit mode, values are padded with leading zeros to ensure 4 characters
- In 32-bit mode, values are padded with leading zeros to ensure 8 characters
- Random mode generates completely random values each time, regardless of the seed input
- The node is part of the "painting" category, suggesting its use in procedural generation workflows

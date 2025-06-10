# StringPainterV2

An enhanced version of the StringPainter node that generates hexadecimal string values. This version adds support for generating multiple hex strings at once, custom random ranges, and tracks the seeds used for generation. It maintains the core functionality of operating in either increment or random mode while adding new features for more complex use cases.

## Input Parameters

### Required Parameters

- **seed** (Required)
  - Default: 0
  - Range: 0 to 0xFFFFFFFF (4294967295)
  - The base value used to generate hex strings
  - In increment mode, this value is used as the starting point
  - In random mode, this value is ignored

- **bits** (Required)
  - Options: "16", "32"
  - Default: "16"
  - Determines the length of the output hex strings:
    - 16-bit: Produces 4-character hex strings (0000-FFFF)
    - 32-bit: Produces 8-character hex strings (00000000-FFFFFFFF)

- **mode** (Required)
  - Options: "increment", "random"
  - Default: "increment"
  - Determines how hex strings are generated:
    - `increment`: Uses the seed value and increments for each subsequent value
    - `random`: Generates random values within the specified range

- **count** (Required)
  - Default: 1
  - Range: 1 to 100
  - Number of hex strings to generate
  - Multiple values are returned as a comma-separated string

### Optional Parameters

- **random_min** (Optional)
  - Default: 0
  - Range: 0 to 0xFFFFFFFF
  - Minimum value for random number generation
  - Only used when mode is "random"

- **random_max** (Optional)
  - Default: 0xFFFFFFFF
  - Range: 0 to 0xFFFFFFFF
  - Maximum value for random number generation
  - Must be greater than random_min
  - Only used when mode is "random"

## Outputs

1. **hex_string** (STRING)
   - Comma-separated list of hexadecimal strings
   - Each string's length depends on the bits parameter:
     - 16-bit: 4 characters (e.g., "3039")
     - 32-bit: 8 characters (e.g., "00003039")
   - Always uses uppercase letters for hex digits A-F

2. **used_seed** (INT)
   - Comma-separated list of seeds used to generate each hex string
   - Useful for tracking or reproducing specific results
   - In increment mode, shows the sequence of seeds used
   - In random mode, shows the actual random values generated

## Usage Examples

1. **Single 16-bit Value (Increment Mode)**
   - Set bits to "16"
   - Set mode to "increment"
   - Set seed to 12345
   - Set count to 1
   - Output hex_string: "3039"
   - Output used_seed: "12345"

2. **Multiple 32-bit Values (Increment Mode)**
   - Set bits to "32"
   - Set mode to "increment"
   - Set seed to 12345
   - Set count to 3
   - Output hex_string: "00003039,0000303A,0000303B"
   - Output used_seed: "12345,12346,12347"

3. **Custom Range Random Values**
   - Set mode to "random"
   - Set count to 5
   - Set random_min to 1000
   - Set random_max to 9999
   - Outputs 5 random hex values within the specified range
   - Also outputs the actual random seeds used

## Notes

- The node includes robust error handling for all inputs
- In increment mode, the seed automatically wraps around at 0xFFFFFFFF
- Custom random ranges must be valid (min < max) or an error is returned
- The node maintains state between calls in increment mode
- Error messages are returned as hex_string when invalid inputs are provided
- The node is part of the "painting" category, suitable for procedural generation workflows

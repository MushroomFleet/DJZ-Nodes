# Sequential Number Generator

The Sequential Number Generator is a utility node that generates sequential integer numbers within a defined range. It's designed to work with ComfyUI's seed system, allowing for controlled sequential number generation that can be used in various workflows.

## Parameters

### Required Parameters

1. **start** (INT)
   - The starting value of the sequence range
   - Default value: 0
   - Minimum value: -2147483648
   - Maximum value: 2147483647

2. **end** (INT)
   - The ending value of the sequence range
   - Default value: 1
   - Minimum value: -2147483648
   - Maximum value: 2147483647

3. **seed** (INT)
   - The seed value that determines the current position in the sequence
   - Default value: 0
   - Minimum value: 0
   - Maximum value: 18446744073709551615 (0xffffffffffffffff)

## Outputs

The node returns two values:
1. **value**: The current number in the sequence
2. **next**: The next number that will be generated in the sequence

## Usage

1. Set the desired range using the start and end parameters
2. Provide a seed value to determine the current position in the sequence
3. The node will output both the current value and the next value in the sequence

## Examples

### Basic Counter
- start: 0
- end: 9
- seed: 0

Result:
- value: 0
- next: 1

### Custom Range
- start: 100
- end: 105
- seed: 2

Result:
- value: 102
- next: 103

## Notes

- The sequence wraps around when it reaches the end value
  - For example, with range 1-3:
    - If current value is 3, next value will be 1
- The start value must be less than or equal to the end value
- The seed value maps to a position within the specified range
- The sequence is deterministic based on the seed value
- Useful for:
  - Creating numbered sequences
  - Implementing counters
  - Generating sequential batch numbers
  - Cycling through a range of values

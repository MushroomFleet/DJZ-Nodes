# BatchRangeSwap Node

The BatchRangeSwap node is designed for manipulating image sequences by replacing a range of frames in a target sequence with a provided set of swap frames. This node is particularly useful for video editing and frame sequence manipulation tasks within ComfyUI.

## Parameters

### Required Inputs

1. **target_sequence** (IMAGE)
   - The main sequence of images that will be modified
   - Must be a batch of multiple images (batch size > 1)
   - This is your base sequence where frames will be swapped

2. **swap_frames** (IMAGE)
   - The batch of frames that will replace frames in the target sequence
   - Must be a valid batch of images
   - These frames will be used to replace frames in the specified range

3. **start_frame** (INT)
   - The starting frame index where swapping will begin
   - Default value: 0
   - Minimum value: 0
   - Maximum value: 999
   - Step size: 1

4. **end_frame** (INT)
   - The ending frame index where swapping will end
   - Default value: 1
   - Minimum value: 0
   - Maximum value: 999
   - Step size: 1
   - Must be greater than or equal to start_frame

## Usage

The node operates by:
1. Taking a target sequence of images
2. Identifying the range between start_frame and end_frame
3. Replacing frames in this range with frames from swap_frames
4. Preserving all frames outside the specified range

### Example

If you have:
- A target sequence of 10 frames
- 3 swap frames
- start_frame = 2
- end_frame = 5

The result will be:
- Frames 0-1 from the target sequence (unchanged)
- Frames 2-4 replaced with the 3 swap frames
- Frame 5 from the target sequence remains unchanged (since only 3 swap frames were provided)
- Frames 6-9 from the target sequence (unchanged)

## Output

The node outputs a single IMAGE type, which is the modified sequence containing:
- Original frames before the swap range
- Newly swapped frames
- Original frames after the swap range

## Notes

- The node will print a warning if either the target_sequence or swap_frames inputs are not proper batches of images
- If there are fewer swap frames than the specified range, the node will:
  - Swap as many frames as possible
  - Print a warning indicating how many frames were actually swapped
  - Leave remaining frames in the range unchanged
- Frame indices are automatically clamped to valid ranges to prevent errors
- The original sequence length is preserved (unlike BatchRangeInsert)
- If the selected frame range is empty (start_frame equals end_frame), the original sequence is returned unchanged with a warning
- The node creates a clone of the target sequence before making modifications, preserving the original data

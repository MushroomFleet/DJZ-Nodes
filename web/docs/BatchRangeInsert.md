# BatchRangeInsert Node

The BatchRangeInsert node is designed for manipulating image sequences by inserting a batch of frames into a target sequence at a specified range. This node is particularly useful for video editing and frame sequence manipulation tasks within ComfyUI.

## Parameters

### Required Inputs

1. **target_sequence** (IMAGE)
   - The main sequence of images that will be modified
   - Must be a batch of multiple images (batch size > 1)
   - This is your base sequence where new frames will be inserted

2. **insert_frames** (IMAGE)
   - The batch of frames that will be inserted into the target sequence
   - Must be a valid batch of images
   - These frames will replace the specified range in the target sequence

3. **start_frame** (INT)
   - The starting frame index where insertion will begin
   - Default value: 0
   - Minimum value: 0
   - Maximum value: 999
   - Step size: 1

4. **end_frame** (INT)
   - The ending frame index where insertion will end
   - Default value: 1
   - Minimum value: 0
   - Maximum value: 999
   - Step size: 1
   - Must be greater than or equal to start_frame

## Usage

The node operates by:
1. Taking a target sequence of images
2. Removing frames between start_frame and end_frame (inclusive)
3. Inserting the provided insert_frames at the start_frame position
4. Preserving all frames before start_frame and after end_frame

### Example

If you have:
- A target sequence of 10 frames
- 3 insert frames
- start_frame = 2
- end_frame = 4

The result will be:
- Frames 0-1 from the target sequence
- The 3 insert frames
- Frames 5-9 from the target sequence

## Output

The node outputs a single IMAGE type, which is the modified sequence containing:
- Original frames before the insertion point
- Newly inserted frames
- Original frames after the insertion point

## Notes

- The node will print a warning if either the target_sequence or insert_frames inputs are not proper batches of images
- The final sequence length will be: original_length - (end_frame - start_frame) + insert_frames_length
- Frame indices are automatically clamped to valid ranges to prevent errors
- The node preserves the original image dimensions and channel count

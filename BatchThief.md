# Batch Thief Node

The Batch Thief node is designed to extract a specific range of frames from a batch of images. This node is particularly useful when you need to isolate or work with a subset of frames from a larger batch sequence.

## Parameters

### Required Inputs

1. **images** (IMAGE)
   - Input batch of images to extract frames from
   - Must be a batch containing multiple images

2. **start_frame** (INT)
   - The starting frame index to extract from the batch
   - Default value: 0
   - Minimum value: 0
   - Maximum value: 999
   - Step size: 1

3. **end_frame** (INT)
   - The ending frame index (exclusive) for extraction
   - Default value: 1
   - Minimum value: 0
   - Maximum value: 999
   - Step size: 1

## Usage

The node works by selecting a range of frames from the input batch, starting from `start_frame` up to (but not including) `end_frame`. For example:
- If you set `start_frame = 0` and `end_frame = 5`, it will extract the first 5 frames from the batch
- If you set `start_frame = 10` and `end_frame = 15`, it will extract frames 10 through 14

## Important Notes

1. The node requires a batch of multiple images to function properly. If a single image is provided, a warning will be displayed.
2. Frame indices are automatically adjusted to valid ranges:
   - If `start_frame` is less than 0, it will be set to 0
   - If `end_frame` exceeds the batch size, it will be capped at the batch size
   - If `start_frame` is greater than or equal to `end_frame`, an empty batch warning will be displayed
3. The node is categorized under "image/batch" in the ComfyUI interface

## Output

- Returns a tensor of type IMAGE containing the selected frames
- If an invalid range is selected (start_frame >= end_frame), returns a single empty frame to maintain tensor structure

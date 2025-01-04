# DJZ Datamosh V2

A ComfyUI custom node that creates datamoshing effects by analyzing and manipulating motion between frames in an image sequence. This node offers three different modes of operation for creating various datamoshing effects.

## Parameters

### Required Inputs

- **images**: An image sequence input (batch of images) with at least 2 frames.
- **mode**: Select from three processing modes:
  - `glide`: Generates a sequence by propagating motion detected between the first two frames
  - `copy`: Preserves the original frames without modification
  - `movement`: Calculates and applies motion shifts between all consecutive frames
- **block_size**: Size of blocks used for motion analysis (4-64, default: 16)
  - Larger blocks result in more chunky, visible distortion effects
  - Smaller blocks create more subtle, detailed motion tracking
- **max_shift**: Maximum pixel distance blocks can move (1-32, default: 8)
  - Higher values allow for more extreme motion distortion
  - Lower values keep the effect more constrained
- **shift_range**: Step size for motion search (1-4, default: 2)
  - Lower values provide more precise motion tracking but slower processing
  - Higher values are faster but may miss subtle movements
- **sequence_length**: Number of frames to generate in glide mode (1-300, default: 30)
  - Only used when mode is set to "glide"
  - Determines how many frames are created by propagating the initial motion

## Usage

1. Connect a sequence of images (minimum 2 frames) to the "images" input
2. Select the desired processing mode:
   - Use `glide` to create a smooth transition sequence from two frames
   - Use `movement` to process the entire sequence with frame-to-frame motion tracking
   - Use `copy` to pass through the original frames unchanged
3. Adjust block_size and max_shift to control the intensity and granularity of the datamosh effect
4. For glide mode, set sequence_length to determine how many frames to generate

## Mode Details

### Glide Mode
- Analyzes motion between first two frames only
- Generates new frames by repeatedly applying the detected motion
- Useful for creating smooth transitions or extending motion from a brief sequence

### Movement Mode
- Processes entire sequence frame by frame
- Each frame is modified based on motion detected from previous frame
- Creates continuous datamoshing effect throughout the sequence

### Copy Mode
- Passes through original frames unchanged
- Useful for debugging or comparing with processed versions

## Technical Details

The node uses block-matching techniques to detect motion between frames:
- Divides frames into blocks of specified size
- Searches for best matching blocks within max_shift distance
- Applies found motion vectors to create distortion effects
- Uses wrapped coordinates to handle edge cases

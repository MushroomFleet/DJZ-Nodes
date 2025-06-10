# Djz Datamosh V3

A ComfyUI custom node that creates datamoshing effects using video compression artifacts. This node uses FFmpeg for video processing and implements two different datamoshing techniques by manipulating video frame types (I-frames and P-frames).

## Parameters

### Required Inputs

- **images**: An image sequence input (batch of images) with at least 2 frames.
- **mode**: Select from two processing modes:
  - `iframe_removal`: Removes I-frames (keyframes) in the specified range to create datamoshing effects
  - `delta_repeat`: Repeats P-frames (delta frames) to create stuttering motion effects
- **start_frame**: Starting frame index for applying the effect (0-999, default: 0)
  - Determines where in the sequence the datamoshing effect begins
  - Frames before this index remain unaffected
- **end_frame**: Ending frame index for applying the effect (-1-999, default: -1)
  - Determines where in the sequence the datamoshing effect ends
  - Use -1 to process until the last frame
  - Frames after this index remain unaffected
- **delta_frames**: Number of P-frames to collect and repeat (1-30, default: 5)
  - Only used in `delta_repeat` mode
  - Higher values create longer motion loops
  - Must be less than the number of frames in the processing range

## Usage

1. Connect a sequence of images (minimum 2 frames) to the "images" input
2. Select the desired processing mode:
   - Use `iframe_removal` for classic datamoshing effects where motion bleeds across scenes
   - Use `delta_repeat` for stuttering, repeating motion effects
3. Set the frame range using start_frame and end_frame to control where the effect is applied
4. For delta_repeat mode, adjust delta_frames to control the length of motion loops

## Mode Details

### iframe_removal Mode
- Removes I-frames (keyframes) within the specified frame range
- Creates the classic datamoshing effect where motion from one scene bleeds into another
- Particularly effective when there are scene changes in the sequence
- Preserves P-frames which contain motion information

### delta_repeat Mode
- Collects a specified number of P-frames and repeats them
- Creates a stuttering, looping motion effect
- More predictable than iframe_removal mode
- Useful for creating rhythmic, glitch-like animations

## Technical Details

The node processes images through several stages:
1. Converts input frames to an AVI file using FFmpeg
2. Manipulates the video frame data based on the selected mode:
   - Identifies and removes I-frames for iframe_removal mode
   - Collects and repeats P-frames for delta_repeat mode
3. Converts the processed video back to frames using FFmpeg
4. Handles video compression artifacts and frame type markers (0x0001B0 for I-frames, 0x0001B6 for P-frames)

## Requirements

- Requires FFmpeg to be installed and accessible in the system path
- Input images should have consistent dimensions
- Sufficient disk space for temporary video files during processing

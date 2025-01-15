# Jitter Effect Node

A ComfyUI node that applies realistic camera shake/jitter effects to image sequences. This node is particularly useful for creating dynamic motion effects, simulating handheld camera movement, or adding organic instability to animations.

## Parameters

### Required Inputs

- **images**: The input batch of images to process
- **x_amplitude** (Default: 3, Range: 0-50)
  - Controls the maximum horizontal displacement in pixels
  - Higher values create more dramatic left-right movement
  - Use lower values (1-5) for subtle shake effects

- **y_amplitude** (Default: 3, Range: 0-50)
  - Controls the maximum vertical displacement in pixels
  - Higher values create more dramatic up-down movement
  - Works in conjunction with x_amplitude for 2D motion

- **rotation_angle** (Default: 0.0, Range: 0.0-5.0)
  - Maximum rotation angle in degrees
  - Adds rotational shake to the movement
  - Small values (0.1-1.0) work best for realistic camera shake

- **frame_coherence** (Default: 0.5, Range: 0.0-1.0)
  - Controls how smooth the jitter movement is between frames
  - 0.0: Completely random movement each frame
  - 1.0: Maximum smoothing between frames
  - Higher values prevent jarring transitions

- **border_mode** (Default: "REPLICATE")
  - Determines how edges are handled when the image is shifted
  - Options:
    - REPLICATE: Extends edge pixels (best for most cases)
    - REFLECT: Mirrors the image at the edges
    - CONSTANT: Fills with black

- **seed** (Default: 0, Range: 0-2147483647)
  - Random seed for reproducible results
  - Same seed will generate the same jitter pattern

## How It Works

The Jitter Effect node applies a combination of translation and rotation to each frame:

1. Generates random offsets for x, y, and rotation based on the amplitude parameters
2. Uses frame coherence to smooth movement between frames
3. Applies the transformation using OpenCV's warpAffine
4. Handles all color channels independently for accurate color preservation

## Usage Tips

1. **For Realistic Camera Shake:**
   - Use small amplitudes (2-5 pixels)
   - Set rotation_angle to 0.1-0.3
   - Use frame_coherence around 0.7-0.8

2. **For Glitch Effects:**
   - Use higher amplitudes (10+)
   - Lower frame_coherence (0.1-0.3)
   - Experiment with different border modes

3. **For Subtle Movement:**
   - Keep x_amplitude and y_amplitude at 1-2
   - Set rotation_angle to 0
   - Use high frame_coherence (0.9)

## Technical Details

- Processes images as numpy arrays for efficient batch processing
- Maintains input image dimensions and color channels
- GPU-compatible through PyTorch tensor conversion
- Implements smooth transitions using linear interpolation between frames

## Output

Returns the processed images with the applied jitter effect, maintaining the same format and dimensions as the input.

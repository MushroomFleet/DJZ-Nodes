# VideoInterlaced Node

A ComfyUI custom node that simulates interlaced video upscaling, similar to the technique used in converting 720p to 1080i video formats. This node applies field-based processing to create an authentic interlaced video effect while upscaling the input frames.

## Overview

The VideoInterlaced node performs interlaced upscaling by:
1. Upscaling the input frame using bilinear interpolation
2. Separating the frame into even and odd fields
3. Applying motion compensation between fields
4. Combining the fields to create the final interlaced output

The default configuration upscales the input by 1.5x (e.g., 720p to 1080i), maintaining the aspect ratio while adding the interlacing effect.

## Parameters

### Required Inputs

- **images** (IMAGE)
  - Input image or batch of images to process
  - Accepts any valid ComfyUI image tensor

- **input_height** (INT)
  - Original frame height in pixels
  - Default: 720
  - Range: 480-4320
  - Step: 1

- **input_width** (INT)
  - Original frame width in pixels
  - Default: 1280
  - Range: 640-7680
  - Step: 1

- **field_order** (COMBO)
  - Determines which field (even or odd lines) comes first
  - Options:
    - "top_first": Even lines are processed first (default)
    - "bottom_first": Odd lines are processed first
  - Affects the interlacing pattern and motion appearance

- **blend_factor** (FLOAT)
  - Controls the amount of motion compensation blending between fields
  - Default: 0.25
  - Range: 0.0-0.5
  - Step: 0.05
  - Higher values create more temporal blending between fields
  - Lower values maintain sharper field separation

## Output

- Returns an upscaled, interlaced version of the input image(s)
- Output dimensions will be 1.5x the input dimensions
- Maintains the original aspect ratio
- Preserves the input color channels

## Usage Tips

1. For authentic interlaced video effects:
   - Use the default 720p to 1080i conversion settings
   - Keep the blend_factor around 0.25 for natural motion appearance

2. For different resolutions:
   - Adjust input_height and input_width to match your source material
   - The output will automatically scale to 1.5x these dimensions

3. Field order selection:
   - Use "top_first" for most modern video formats
   - Switch to "bottom_first" if you notice motion artifacts

4. Motion compensation:
   - Increase blend_factor for smoother motion but reduced sharpness
   - Decrease blend_factor for sharper fields but more visible interlacing

## Technical Details

The node uses PyTorch for processing and supports both CPU and CUDA acceleration. It performs:
- Bilinear upscaling of the input frame
- Field separation using masks
- Motion compensation through field shifting and blending
- Field recombination for the final output

The output is automatically clamped to the valid range [0, 1] to prevent artifacts.

# Image Interleaved Upscaler

A custom node for ComfyUI that provides high-quality image upscaling using an interleaved field technique, similar to traditional interlaced video processing but optimized for image enhancement.

## Description

The Image Interleaved Upscaler applies a sophisticated upscaling method that processes images by separating them into alternating fields (similar to interlaced video), upscaling them independently, and then recombining them with optional blending and enhancement features. This approach can help preserve detail and reduce artifacts commonly seen in traditional upscaling methods.

## Parameters

### Required Inputs

- **image**: The input image to be upscaled
- **input_width** (Default: 1280, Range: 640-7680)
  - The target width for the input image
  - Helps maintain proper aspect ratio during upscaling
  
- **input_height** (Default: 720, Range: 480-4320)
  - The target height for the input image
  - Works in conjunction with input_width for aspect ratio maintenance

- **scale_factor** (Default: 1.5, Range: 1.0-4.0)
  - Determines how much to upscale the image
  - A value of 1.0 means no scaling, 2.0 means double the size, etc.

- **field_order** (Options: "top_first", "bottom_first", Default: "top_first")
  - Determines which field is processed first in the interleaving
  - Can affect the appearance of fine details

- **blend_factor** (Default: 0.25, Range: 0.0-1.0)
  - Controls how much the fields blend into each other
  - Higher values create smoother transitions but might reduce sharpness
  - 0.0 means no blending, 1.0 means maximum blending

- **interpolation_mode** (Options: "bilinear", "bicubic", "nearest", Default: "bilinear")
  - The algorithm used for the initial upscaling
  - "bilinear": Good balance of quality and speed
  - "bicubic": Higher quality but slower
  - "nearest": Fastest but lowest quality, good for pixel art

- **field_strength** (Default: 1.0, Range: 0.0-2.0)
  - Controls the intensity of the field effect
  - Higher values emphasize the interleaving effect
  - Lower values create a more subtle effect

- **edge_enhancement** (Default: 0.0, Range: 0.0-1.0)
  - Applies additional sharpening to edges using a Sobel operator
  - Higher values create sharper edges but may introduce artifacts
  - 0.0 means no enhancement

## Usage Tips

1. **For General Upscaling:**
   - Start with default settings
   - Use "bilinear" interpolation mode
   - Keep blend_factor around 0.25
   - Keep edge_enhancement at 0.0

2. **For Maximum Detail:**
   - Use "bicubic" interpolation
   - Lower the blend_factor to 0.1-0.15
   - Increase field_strength to 1.2-1.5
   - Add slight edge_enhancement (0.2-0.3)

3. **For Smoother Results:**
   - Increase blend_factor to 0.4-0.5
   - Keep field_strength at 1.0 or slightly lower
   - Use "bilinear" interpolation

4. **For Artistic Effects:**
   - Experiment with high field_strength (1.5-2.0)
   - Try different field_order settings
   - Combine with higher edge_enhancement values

## Technical Details

The node uses a sophisticated process that:
1. Upscales the input image to the target size
2. Separates the image into alternating fields
3. Processes each field independently
4. Applies optional edge enhancement using Sobel operators
5. Blends the fields back together with controllable intensity

The result is output as a single upscaled image that maintains good detail while minimizing common upscaling artifacts.

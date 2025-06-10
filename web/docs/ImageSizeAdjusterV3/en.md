# Image Size Adjuster V3

An enhanced version of the Image Size Adjuster that adds support for Mochi1 video model alongside standard image models. This version is optimized for both image and video workflows, with special handling for different aspect ratios and orientations.

## Input Parameters

### Required Parameters

- **image**: The input image to be resized
- **model_type**: Choose between four AI model types:
  - `SD`: Targets 512x512 (262,144 pixels)
  - `SDXL`: Targets 1024x1024 (1,048,576 pixels)
  - `Cascade`: Targets 2048x2048 (4,194,304 pixels)
  - `Mochi1`: Video-optimized with fixed dimensions:
    - Landscape: 848x480 (16:9)
    - Portrait: 480x848 (9:16)
- **downscale_factor**: The number that both width and height should be divisible by
  - Default: 8 (optimized for video workflows)
  - Range: 1-128
  - Used to ensure dimensions are optimal for the model's tiling system
- **rounding_method**: How dimensions are rounded to meet the downscale factor:
  - `up`: Always rounds up to the next multiple
  - `down`: Always rounds down to the previous multiple
  - `nearest`: Rounds to the closest multiple
- **preserve_original**: Option to keep one of the original dimensions:
  - `none`: Adjust both dimensions
  - `width`: Keep original width if it's divisible by downscale_factor
  - `height`: Keep original height if it's divisible by downscale_factor
- **force_square**: When enabled, outputs a square image with equal width and height

### Optional Parameters

- **scaling_factor**: Multiplier for the target pixel count
  - Default: 1.0
  - Range: 0.1-10.0
  - Allows fine-tuning of the overall image size
  - Note: Does not affect Mochi1 model type
- **max_width**: Maximum allowed width
  - Default: 2048
  - Range: 64-8192
  - For Mochi1: Automatically limited to model constraints
- **max_height**: Maximum allowed height
  - Default: 2048
  - Range: 64-8192
  - For Mochi1: Automatically limited to model constraints

## Outputs

- **adjusted_width**: The final calculated width
- **adjusted_height**: The final calculated height
- **applied_scale**: The actual scaling factor applied to the image
- **original_width**: The input image's width (for reference)
- **original_height**: The input image's height (for reference)

## How It Works

### Standard Models (SD, SDXL, Cascade)
1. Calculates target pixel count based on model type and scaling factor
2. Determines initial dimensions based on aspect ratio and force_square setting
3. Applies preservation of original dimensions if requested
4. Rounds dimensions according to the chosen rounding method
5. Applies size limits to ensure dimensions stay within bounds

### Mochi1 Model
1. Determines orientation (landscape/portrait) based on aspect ratio
2. Automatically selects appropriate fixed dimensions:
   - Landscape: 848x480
   - Portrait: 480x848
3. Maintains strict 16:9 or 9:16 aspect ratio
4. Applies rounding and size limits while preserving the model's constraints

## Use Cases

- Video frame preparation for Mochi1 model
- Standard image preparation for various AI models
- Maintaining specific aspect ratios for video workflows
- Automatic orientation detection and adjustment
- Precise dimension control while respecting model constraints
- Batch processing with consistent sizing across multiple models

## Key Differences from V2

1. Added Mochi1 video model support with fixed aspect ratios
2. Default downscale factor changed to 8 (better for video)
3. Automatic orientation detection for Mochi1
4. Smart constraints based on model type
5. Enhanced aspect ratio handling for video formats

# Image Size Adjuster V2

An advanced node for adjusting image dimensions with precise control over scaling behavior. This node builds upon the original Image Size Adjuster with additional features for fine-tuning the output dimensions while maintaining optimal compatibility with different AI models.

## Input Parameters

### Required Parameters

- **image**: The input image to be resized
- **model_type**: Choose between three AI model types:
  - `SD`: Targets 512x512 (262,144 pixels)
  - `SDXL`: Targets 1024x1024 (1,048,576 pixels)
  - `Cascade`: Targets 2048x2048 (4,194,304 pixels)
- **downscale_factor**: The number that both width and height should be divisible by
  - Default: 64
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
- **max_width**: Maximum allowed width
  - Default: 2048
  - Range: 64-8192
  - Ensures width doesn't exceed this value
- **max_height**: Maximum allowed height
  - Default: 2048
  - Range: 64-8192
  - Ensures height doesn't exceed this value

## Outputs

- **adjusted_width**: The final calculated width
- **adjusted_height**: The final calculated height
- **applied_scale**: The actual scaling factor applied to the image
- **original_width**: The input image's width (for reference)
- **original_height**: The input image's height (for reference)

## How It Works

1. Calculates target pixel count based on model type and scaling factor
2. Determines initial dimensions based on aspect ratio and force_square setting
3. Applies preservation of original dimensions if requested
4. Rounds dimensions according to the chosen rounding method
5. Applies size limits to ensure dimensions stay within bounds
6. Calculates the actual scale applied for reference

## Use Cases

- Precise control over image dimensions for AI model input
- Maintaining specific dimensions while adjusting others
- Creating square images while maintaining optimal pixel count
- Scaling images with exact control over rounding behavior
- Ensuring images stay within maximum size limits
- Tracking actual scaling applied to images

# Image Size Adjuster

This node automatically adjusts image dimensions to be optimal for different AI model types (SD 1.5, SDXL, or Cascade) while maintaining the original aspect ratio and ensuring dimensions are properly divisible for tiling.

## Input Parameters

- **image**: The input image to be resized
- **model_type**: Choose between three AI model types:
  - `SD`: Targets 512x512 (262,144 pixels)
  - `SDXL`: Targets 1024x1024 (1,048,576 pixels)
  - `Cascade`: Targets 2048x2048 (4,194,304 pixels)
- **downscale_factor**: The number that both width and height should be divisible by
  - Default: 64
  - Range: 1-128
  - Used to ensure dimensions are optimal for the model's tiling system

## Outputs

- **adjusted_width**: The calculated optimal width for the selected model
- **adjusted_height**: The calculated optimal height for the selected model

## How It Works

1. The node first determines the target total pixel count based on the selected model type
2. It preserves the aspect ratio of your input image while scaling to match the target pixel count
3. Both dimensions are then adjusted to be divisible by the downscale_factor
4. The final dimensions maintain a similar total pixel count to the model's target while keeping your image's proportions

## Use Cases

- Preparing images for specific AI models while maintaining composition
- Ensuring dimensions are optimal for tiling/processing
- Automatically calculating proper dimensions for different model types without manual math

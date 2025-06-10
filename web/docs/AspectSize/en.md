# AspectSize Node

The AspectSize node is a utility for calculating optimal image dimensions while maintaining a desired aspect ratio. It's particularly useful when working with different AI models (SD, SDXL, or Cascade) that have specific optimal resolutions.

## Parameters

### Required Inputs

- **model_type** (Selection)
  - Options: "SD", "SDXL", "Cascade"
  - Determines the base resolution:
    - SD: 512x512 base
    - SDXL: 1024x1024 base
    - Cascade: 2048x2048 base

- **aspect_ratio_width** (Integer)
  - Default: 1
  - The width component of your desired aspect ratio
  - Example: For 16:9, set this to 16

- **aspect_ratio_height** (Integer)
  - Default: 1
  - The height component of your desired aspect ratio
  - Example: For 16:9, set this to 9

## Outputs

- **Width** (Integer)
  - The calculated optimal width that maintains the aspect ratio
  - Always divisible by 16 (for model compatibility)

- **Height** (Integer)
  - The calculated optimal height that maintains the aspect ratio
  - Always divisible by 16 (for model compatibility)

## How It Works

1. The node takes your desired aspect ratio and model type
2. Calculates dimensions that maintain the total pixel count of the base resolution
3. Adjusts the dimensions to be divisible by 16 (required for stable diffusion models)
4. Returns the optimal width and height values

## Common Use Cases

1. **Widescreen Images**
   - Set aspect_ratio_width to 16 and aspect_ratio_height to 9 for standard widescreen
   - Works well for landscape compositions

2. **Portrait Mode**
   - Set aspect_ratio_width to 9 and aspect_ratio_height to 16 for vertical compositions
   - Ideal for character portraits or phone wallpapers

3. **Square Images**
   - Set both values to 1 for perfect squares
   - Useful for social media profile pictures or album covers

## Notes

- The node ensures that the output dimensions are always divisible by 16, which is required for compatibility with AI image generation models
- The total pixel count is preserved as much as possible while maintaining the aspect ratio
- The calculations automatically adjust based on the selected model type's base resolution

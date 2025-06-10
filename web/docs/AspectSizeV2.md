# Aspect Size V2 Node

The Aspect Size V2 node is an enhanced version of the AspectSize node, providing more flexible control over image dimensions while maintaining aspect ratios. It adds customizable downscaling options, making it more versatile for different AI model requirements.

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

- **downscale_factor** (Integer)
  - Default: 64
  - Range: 1-128
  - Controls the divisibility of the output dimensions
  - Higher values result in dimensions that are multiples of larger numbers
  - Useful for ensuring compatibility with different model architectures

## Outputs

- **Width** (Integer)
  - The calculated optimal width that maintains the aspect ratio
  - Will be divisible by the chosen downscale_factor

- **Height** (Integer)
  - The calculated optimal height that maintains the aspect ratio
  - Will be divisible by the chosen downscale_factor

## Key Differences from AspectSize V1

1. **Configurable Downscale Factor**
   - V1 used a fixed value of 16
   - V2 allows values from 1 to 128
   - Provides more control over final dimensions

2. **Enhanced Compatibility**
   - More flexible for different model architectures
   - Better support for custom training setups
   - Allows fine-tuning of output dimensions

## Common Use Cases

1. **Standard AI Model Generation**
   - Use downscale_factor of 64 for most stable diffusion models
   - Maintains compatibility while offering good size control

2. **Custom Model Requirements**
   - Adjust downscale_factor based on specific model architecture
   - Useful for models with unique dimensional requirements

3. **Memory Optimization**
   - Higher downscale_factor values can help reduce memory usage
   - Useful when working with limited GPU memory

## Notes

- The node preserves the total pixel count of the base resolution while maintaining aspect ratio
- The downscale_factor affects both width and height equally
- Higher downscale_factor values result in more constrained dimension options
- Lower downscale_factor values offer more precise dimension control but may not be compatible with all models

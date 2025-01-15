# Image Interleaved Upscaler V2

A ComfyUI custom node that combines GAN-based upscaling with interlacing effects for enhanced image quality. This node applies sophisticated field-based processing to create smoother, more detailed upscaled images.

## Features

- Combines traditional upscaling with interlaced field processing
- Supports any ComfyUI-compatible upscaling model
- Tile-based processing for handling large images
- Optional edge enhancement
- Memory-efficient processing with automatic tiling adjustments

## Parameters

### Required Parameters

- **image**: The input image to be processed
- **upscale_model**: The upscaling model to use (any ComfyUI-compatible upscaler)
- **field_order**: Determines the interlacing pattern
  - `top_first`: Process top scanlines first (default)
  - `bottom_first`: Process bottom scanlines first
- **blend_factor**: Controls the blending between adjacent scanlines
  - Range: 0.0 to 1.0 (default: 0.25)
  - Higher values create smoother transitions between fields
  - Lower values maintain sharper field separation
- **field_strength**: Controls the intensity of the interlacing effect
  - Range: 0.0 to 2.0 (default: 1.0)
  - Higher values increase the prominence of the interlacing effect
  - Lower values create more subtle field differences

### Optional Parameters

- **tile_size**: Size of processing tiles for large images
  - Range: 128 to 1024 (default: 512)
  - Larger values use more VRAM but may be faster
  - Automatically reduces if out of memory
- **tile_overlap**: Overlap between processing tiles
  - Range: 16 to 256 (default: 32)
  - Higher values reduce visible seams but increase processing time
- **edge_enhancement**: Additional edge sharpening strength
  - Range: 0.0 to 1.0 (default: 0.0)
  - Uses Sobel operator for edge detection
  - Higher values create sharper, more defined edges

## How It Works

1. The node first upscales the entire image using the provided upscaling model
2. It then applies an interlacing effect by:
   - Separating the image into even and odd fields
   - Processing each field with the specified field order
   - Blending adjacent scanlines based on the blend factor
   - Applying field strength modulation
3. Optional edge enhancement is applied using Sobel edge detection
4. The final image is processed in tiles to manage memory usage

## Usage Tips

- For vintage or retro-style effects:
  - Use higher field_strength (1.5-2.0)
  - Set blend_factor lower (0.1-0.2)
  - Enable edge_enhancement (0.3-0.5)

- For smoother, modern upscaling:
  - Use moderate field_strength (0.5-1.0)
  - Set blend_factor higher (0.3-0.5)
  - Keep edge_enhancement low or disabled

- For large images:
  - Adjust tile_size based on your GPU VRAM
  - Increase tile_overlap if you notice seams
  - The node will automatically adjust if it runs out of memory

## Memory Management

The node includes automatic memory management features:
- Dynamically adjusts tile size if out of memory
- Cleans up GPU memory after processing
- Moves models between CPU and GPU as needed

## Output

Returns a single upscaled image tensor in BHWC format (Batch, Height, Width, Channels), compatible with other ComfyUI nodes in the image processing pipeline.

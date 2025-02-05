# VideoInterlaceGAN V3

A ComfyUI custom node for high-quality video frame upscaling that combines interlaced processing with GAN-based upscaling models. This node provides advanced temporal compensation and edge enhancement features for superior video quality.

## Features

- GAN-based upscaling with external model support
- Interlaced field processing with customizable field order
- Temporal compensation for improved frame consistency
- Edge enhancement capabilities
- Tiled processing for handling large frames
- Memory-efficient operation with automatic OOM handling

## Parameters

### Required Parameters

- **images**: Input video frames in tensor format (IMAGE)
- **upscale_model**: External upscaling model to use for processing (UPSCALE_MODEL)
- **field_order**: Field interlacing order
  - `top_first`: Process top field first (default)
  - `bottom_first`: Process bottom field first
- **blend_factor**: Controls the strength of field blending
  - Range: 0.0 to 1.0 (default: 0.25)
  - Higher values create smoother transitions between fields
- **temporal_radius**: Number of neighboring frames to consider for temporal compensation
  - Range: 1 to 3 (default: 1)
  - Higher values provide more temporal consistency but may reduce detail

### Optional Parameters

- **tile_size**: Size of processing tiles for memory efficiency
  - Range: 128 to 1024 (default: 512)
  - Smaller values use less memory but may be slower
- **tile_overlap**: Overlap between processing tiles to prevent artifacts
  - Range: 16 to 256 (default: 32)
  - Higher values reduce tile boundary artifacts
- **enhance_edges**: Strength of edge enhancement
  - Range: 0.0 to 1.0 (default: 0.0)
  - Higher values increase perceived sharpness

## Technical Details

### Processing Pipeline

1. **Temporal Compensation**
   - Analyzes neighboring frames within the specified temporal radius
   - Applies weighted averaging for consistent motion
   - Handles edge cases at sequence boundaries

2. **Interlaced Processing**
   - Upscales full frame using the provided GAN model
   - Separates fields based on specified field order
   - Applies field blending for smoother transitions

3. **Edge Enhancement**
   - Uses Sobel operator for edge detection
   - Applies controllable edge enhancement
   - Preserves natural image appearance

4. **Memory Management**
   - Implements tiled processing for large frames
   - Automatically handles out-of-memory situations
   - Efficiently manages GPU resources

## Usage Tips

1. **Optimal Field Order**
   - Use `top_first` for most modern video sources
   - Try `bottom_first` if you notice field artifacts

2. **Memory Optimization**
   - Reduce `tile_size` if encountering memory issues
   - Increase `tile_overlap` if seeing tile boundary artifacts

3. **Quality Tuning**
   - Adjust `blend_factor` for optimal field transition smoothness
   - Use `enhance_edges` sparingly to avoid over-sharpening
   - Increase `temporal_radius` for smoother motion at the cost of processing time

## Category
image/upscaling

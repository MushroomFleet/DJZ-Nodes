# VideoInterlaceFastV4 Node

A high-performance ComfyUI custom node designed for video frame upscaling with multiple optimization modes. This node provides various speed/quality tradeoffs and optional enhancements for different use cases.

## Features

- Multiple upscaling modes from fastest to highest quality
- GPU-accelerated processing with CUDA support
- Batch processing capability
- Optional motion compensation
- Edge enhancement in quality mode
- Flexible precision control (full/half)

## Parameters

### Required Parameters

- **images**: Input image tensor (IMAGE type)
- **mode**: Upscaling mode selection (default: "balanced")
  - `fastest`: Pure bilinear upscaling - maximum speed, lower quality
  - `fast`: Lanczos upscaling without motion compensation
  - `balanced`: Lanczos with basic motion compensation
  - `quality`: Full feature set with edge enhancement
- **input_height**: Input frame height (default: 720, range: 480-4320)
- **input_width**: Input frame width (default: 1280, range: 640-7680)
- **scale_factor**: Upscaling multiplier (default: 1.5, range: 1.0-4.0)

### Optional Parameters

- **enable_motion_comp**: Enable/disable motion compensation (default: True)
  - Helps reduce temporal artifacts between frames
  - Available in balanced and quality modes
- **batch_size**: Number of frames to process simultaneously (default: 4, range: 1-16)
  - Higher values may increase speed but require more VRAM
- **precision**: Processing precision mode (default: "half")
  - `half`: Uses FP16 on GPU for faster processing
  - `full`: Uses FP32 for higher precision

## Mode Details

1. **Fastest Mode**
   - Uses pure bilinear upscaling
   - Best for real-time applications
   - Minimal VRAM usage
   - Suitable for preview or when speed is critical

2. **Fast Mode**
   - Implements Lanczos upscaling
   - Better quality than bilinear
   - No motion compensation
   - Good balance of speed and quality for static content

3. **Balanced Mode**
   - Lanczos upscaling with optional motion compensation
   - Reduces temporal artifacts
   - Recommended for most use cases
   - Good trade-off between quality and performance

4. **Quality Mode**
   - Full feature set enabled
   - Enhanced motion compensation
   - Edge enhancement for sharper details
   - Best for final renders where quality is priority

## Technical Notes

- Automatically uses CUDA acceleration when available
- Implements efficient batch processing for better performance
- Handles both single frames and batched inputs
- Automatically manages precision based on hardware capabilities
- Includes edge case handling for various input formats
- Preserves color accuracy with proper normalization

## Usage Tips

1. Start with "balanced" mode for most use cases
2. Use "fastest" mode for preview or real-time applications
3. Enable motion compensation when processing video sequences
4. Adjust batch size based on available VRAM
5. Use "quality" mode for final renders where processing time isn't critical
6. Consider using half precision on GPU for better performance

## Performance Considerations

- Higher batch sizes generally improve throughput but require more VRAM
- Motion compensation adds processing overhead but improves temporal consistency
- Quality mode is significantly more resource-intensive than other modes
- GPU processing with half precision can provide significant speed improvements

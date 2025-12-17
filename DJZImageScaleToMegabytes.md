# DJZ Scale to Megabytes

A ComfyUI custom node that intelligently scales images to a target file size in megabytes, perfect for API integrations with file size limits.

## Overview

This node is derived from `DJZImageScaleToTotalPixels` and provides a different scaling approach: instead of scaling to a specific pixel count, it scales images to achieve a target file size. This is particularly useful when working with APIs that have upload size restrictions (e.g., 5MB limits).

## Features

- **File Size Target**: Specify target size in megabytes instead of dimensions
- **Batch Processing**: Option to apply size limit to entire batch or per-image
- **Aspect Ratio Preservation**: Maintains original image proportions
- **Dimension Divisibility**: Ensures output dimensions are divisible by a specified factor
- **Multiple Resize Methods**: Supports various upscaling/downscaling algorithms
- **API-Friendly**: Designed for workflows with file size constraints

## Parameters

### Required Inputs

- **image** (`IMAGE`): Input image or batch of images
- **upscale_method** (dropdown): Resize algorithm
  - `nearest-exact`: Fastest, lowest quality
  - `bilinear`: Good balance of speed and quality
  - `area`: Best for downscaling
  - `bicubic`: Higher quality, slower
  - `lanczos`: Highest quality, slowest
- **total_megabytes** (`FLOAT`): Target file size in MB
  - Default: `4.99` (useful for 5MB API limits)
  - Range: `0.01` to `100.0` MB
  - Step: `0.01`
- **divisible_by** (`INT`): Ensures dimensions are multiples of this value
  - Default: `64` (common for AI models)
  - Range: `1` to `512`
  - Useful for models requiring specific dimension alignment
- **batch** (`BOOLEAN`): Batch processing mode
  - `False` (default): Each image scaled to target size individually
  - `True`: Total batch size equals target (size divided among images)

## How It Works

### File Size Estimation

The node estimates PNG file sizes using:
1. Uncompressed size = width × height × channels
2. Compressed estimate = uncompressed × 0.6 (assumes ~40% compression)

This conservative estimate ensures images stay under limits while minimizing unnecessary downsizing.

### Scaling Algorithm

1. Calculate current estimated file size
2. Determine scale factor: `√(target_bytes / current_bytes)`
3. Apply scale factor to dimensions
4. Round dimensions to nearest `divisible_by` multiple
5. Enforce minimum dimensions (`divisible_by` × 1)
6. Perform resize operation

### Batch Mode Behavior

**Batch = False** (Default)
```
3 images × 4.99 MB target = each image ~4.99 MB
Total batch size: ~15 MB
```

**Batch = True**
```
3 images × 4.99 MB target = ~1.66 MB per image
Total batch size: ~4.99 MB
```

## Use Cases

### 1. API Upload Limits
```
API has 5MB limit → Set total_megabytes = 4.99
Guarantees successful uploads with minimal quality loss
```

### 2. Batch Processing Mixed Aspect Ratios
```
Process multiple images with different dimensions
All scaled to consistent file size
Aspect ratios preserved
```

### 3. Storage Optimization
```
Reduce storage footprint while maintaining quality
Predictable file sizes for database planning
```

### 4. Model Input Requirements
```
Ensure dimensions divisible by 64 for VAE compatibility
Maintain file size constraints simultaneously
```

## Installation

1. Place `DJZImageScaleToMegabytes.py` in your ComfyUI custom nodes directory:
   ```
   ComfyUI/custom_nodes/DJZImageScaleToMegabytes.py
   ```

2. Restart ComfyUI

3. Node appears as "DJZ Scale to Megabytes" in the `image/upscaling` category

## Example Workflows

### Example 1: API Upload with 5MB Limit
```
Input: 4096×4096 image (~15MB estimated)
Settings:
  - total_megabytes: 4.99
  - divisible_by: 8
  - batch: False
  - upscale_method: lanczos

Output: 2560×2560 image (~4.95MB)
Result: Successfully uploads to API
```

### Example 2: Batch Processing for Web Gallery
```
Input: 10 mixed-resolution images
Settings:
  - total_megabytes: 2.0
  - divisible_by: 1
  - batch: False
  - upscale_method: area

Output: 10 images, each ~2MB
Result: Consistent file sizes for web optimization
```

### Example 3: Batch Limit for Email Attachment
```
Input: 5 vacation photos
Settings:
  - total_megabytes: 9.9 (10MB email limit)
  - divisible_by: 1
  - batch: True
  - upscale_method: bicubic

Output: 5 images totaling ~9.9MB
Result: Entire batch fits in single email
```

## Technical Notes

### Compression Assumptions

- The node estimates PNG compression at ~40% efficiency
- Actual compression varies by image content:
  - Simple graphics: 70-90% compression (smaller files)
  - Detailed photos: 20-40% compression (larger files)
- The 0.6 multiplier (60% retained) is conservative to prevent overshooting limits

### Dimension Rounding

- Dimensions always rounded to `divisible_by` multiples
- Ensures compatibility with models requiring specific alignments
- May result in slightly different file sizes than target
- Minimum dimensions enforced: `divisible_by × 1`

### Performance

- Scales linearly with image resolution and batch size
- `lanczos` method: highest quality, ~2-3× slower
- `area` method: best for downscaling, fast
- `nearest-exact`: fastest, use for quick previews

## Comparison with DJZImageScaleToTotalPixels

| Feature | ScaleToTotalPixels | ScaleToMegabytes |
|---------|-------------------|------------------|
| Control by | Megapixels (resolution) | Megabytes (file size) |
| Use case | Dimension constraints | File size constraints |
| Batch mode | No | Yes |
| API-friendly | Indirect | Direct |
| Best for | Resolution requirements | Upload/storage limits |

## Troubleshooting

**Images still too large**
- Decrease `total_megabytes` by 10-20%
- Some images compress less than estimated

**Images too small/low quality**
- Increase `total_megabytes`
- Check if `batch: True` is unintentionally enabled

**Dimension errors in downstream nodes**
- Adjust `divisible_by` to match model requirements
- Common values: 1, 8, 64, 128

**Unexpected batch sizes**
- Verify `batch` parameter setting
- Remember: `True` splits target across all images

## Credits

Based on the original `DJZImageScaleToTotalPixels` node.

Developed for ComfyUI workflows requiring file size management alongside dimension control.

## License

Use freely in your ComfyUI workflows. Attribution appreciated but not required.

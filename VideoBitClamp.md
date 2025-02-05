# VideoBitClamp (Video Bit Depth Clamper)

A sophisticated ComfyUI node for simulating lower bit depth color palettes in videos and images while maintaining quality through various dithering methods and enhancement options.

## Description

VideoBitClamp reduces the color bit depth of images or video frames while providing fine control over the process through dithering, color space conversion, and various quality preservation techniques. It's particularly useful for creating retro-style visuals or optimizing color palettes while maintaining visual quality.

## Parameters

### Required Inputs

- **images**: The input images/frames to process (IMAGE type)
- **bit_depth**: Target bit depth for color quantization
  - `8bit`: 2 bits per channel (8 levels per channel)
  - `16bit`: 3 bits per channel (16 levels per channel)
  - `32bit`: 4 bits per channel (32 levels per channel)
  - `64bit`: 5 bits per channel (64 levels per channel)
  - `128bit`: 6 bits per channel (128 levels per channel)
- **dithering**: Method used to reduce color banding
  - `none`: Direct color quantization
  - `ordered`: Bayer matrix dithering for uniform pattern
  - `floyd-steinberg`: Error diffusion dithering for natural look
- **color_space**: Color space for processing
  - `RGB`: Standard RGB color space
  - `YUV`: Processes luminance and chrominance separately
- **preservation**: Blend factor with original image (0.0 to 1.0)
  - 0.0: Full bit depth reduction effect
  - 1.0: Preserves original image entirely

### Optional Inputs

- **gamma**: Gamma correction value (1.0 to 3.0)
  - Default: 2.2
  - Affects how brightness is preserved during quantization
- **noise_reduction**: Pre-processing noise reduction (0.0 to 1.0)
  - Default: 0.0
  - Higher values smooth the image before processing
- **temporal_coherence**: Frame-to-frame consistency (0.0 to 1.0)
  - Default: 0.0
  - Reduces flickering in video sequences

## Features Explained

### 1. Bit Depth Reduction

The node offers various bit depth options that affect color quantization:
- Lower bit depths (8bit/16bit) create more pronounced retro effects
- Higher bit depths (64bit/128bit) offer subtle color palette optimization
- Each step doubles the available colors per channel

### 2. Dithering Methods

Three dithering options are available to handle color banding:

1. **No Dithering**
   - Direct color quantization
   - Creates sharp color transitions
   - Useful for pixel art style effects

2. **Ordered Dithering**
   - Uses 4x4 Bayer matrix
   - Creates uniform, pattern-based dithering
   - Good for retro computer graphics look

3. **Floyd-Steinberg Dithering**
   - Error diffusion algorithm
   - Creates natural-looking gradients
   - Best for preserving image detail

### 3. Color Space Processing

Two color space options affect how the image is processed:

1. **RGB Mode**
   - Processes all color channels equally
   - Better for preserving vibrant colors
   - Recommended for most uses

2. **YUV Mode**
   - Separates luminance from color information
   - Better preserves perceived brightness
   - Useful for vintage video effects

### 4. Advanced Features

1. **Noise Reduction**
   - Bilateral filtering preserves edges
   - Reduces artifacts in compressed images
   - Applies before bit depth reduction

2. **Temporal Coherence**
   - Considers adjacent frames in video
   - Reduces color flickering
   - Weighted frame blending

3. **Gamma Correction**
   - Preserves perceived brightness
   - Compensates for display characteristics
   - Affects quantization behavior

## Usage Tips

1. **For Retro Effects**
   - Use 8bit or 16bit depth
   - Try ordered dithering
   - Consider YUV color space
   - Keep preservation at 0.0

2. **For Quality Optimization**
   - Use 32bit or higher
   - Use floyd-steinberg dithering
   - Stay in RGB color space
   - Adjust preservation as needed

3. **For Video Processing**
   - Enable temporal coherence
   - Consider noise reduction
   - Use floyd-steinberg dithering
   - Adjust based on source quality

4. **For Best Results**
   - Start with higher bit depths
   - Test different dithering methods
   - Use preservation for subtle effects
   - Enable temporal coherence for video

## Technical Details

- Processes images in batch mode
- CUDA-accelerated when available
- Maintains original image dimensions
- Preserves alpha channel if present
- Handles edge cases and color space conversion
- Provides detailed processing logs

## Output

Returns processed images with the same dimensions as input, with colors quantized to the specified bit depth and optional enhancements applied.

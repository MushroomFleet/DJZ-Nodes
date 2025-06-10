# DjzDatamoshV8 (Djz Pixel Sort V8 Advanced)

A sophisticated pixel sorting node for ComfyUI that provides advanced control over image glitch aesthetics through various sorting methods and masking capabilities.

## Description

DjzDatamoshV8 is an advanced pixel sorting node that can create unique glitch art effects by reorganizing pixels based on different properties like luminance, hue, saturation, or edge detection (laplacian). The node supports masked operations and multiple sorting passes for complex effects.

## Parameters

### Required Inputs

- **images**: The input images to apply the pixel sorting effect to (IMAGE type)
- **mask**: A mask to control where the sorting effect is applied (MASK type)
  - White areas (1.0) = Apply sorting
  - Black areas (0.0) = Keep original pixels
- **sort_mode**: The method used to determine pixel sorting order
  - `luminance`: Sorts based on pixel brightness
  - `hue`: Sorts based on color hue values
  - `saturation`: Sorts based on color intensity
  - `laplacian`: Sorts based on edge detection values
- **threshold**: Controls segment creation (0.0 to 1.0)
  - Lower values create more segments
  - Higher values create fewer, larger segments
  - Default: 0.5
- **rotation**: Controls the direction of the sorting effect (-180° to 180°)
  - -90° (default): Vertical sorting
  - 0°: Horizontal sorting
  - 90°: Vertical sorting (reverse direction)
  - 180°: Horizontal sorting (reverse direction)
- **multi_pass**: Boolean toggle for applying all sorting modes sequentially
  - When enabled, applies all sorting modes in order: luminance → hue → saturation → laplacian
  - Creates more complex and intense effects
- **seed**: Random seed for reproducible results (0 to 4294967295)
  - Default: 42

## Sorting Modes Explained

1. **Luminance Mode**
   - Sorts pixels based on their brightness
   - Uses standard RGB to luminance conversion (0.2126R + 0.7152G + 0.0722B)
   - Good for creating clean, contrast-based sorting effects

2. **Hue Mode**
   - Sorts pixels based on their color angle in HSV color space
   - Creates rainbow-like sorting patterns
   - Effective for images with varied colors

3. **Saturation Mode**
   - Sorts based on color intensity
   - Separates vivid colors from muted ones
   - Useful for emphasizing or de-emphasizing colorful areas

4. **Laplacian Mode**
   - Sorts based on edge detection
   - Emphasizes areas of high contrast
   - Creates effects that follow image contours

## Usage Tips

1. **Basic Usage**
   - Start with `luminance` mode and threshold = 0.5
   - Adjust threshold to control segment size
   - Use rotation to change sorting direction

2. **Masking**
   - Use masks to apply effects selectively
   - Combine with other mask generators for precise control
   - Useful for preserving important image features

3. **Advanced Effects**
   - Enable multi_pass for complex glitch effects
   - Combine with other image effects
   - Experiment with different sort modes for varied results

4. **Optimization**
   - Lower threshold values create more segments but increase processing time
   - Multi_pass mode takes longer to process
   - Use seed parameter for reproducible results

## Technical Details

- Processes images in BHWC format (Batch, Height, Width, Channels)
- Supports batch processing
- Uses stable sorting algorithm for consistent results
- Implements efficient numpy operations for performance
- Handles edge cases and prevents division by zero
- Preserves image quality through proper normalization

## Output

Returns processed images with the same dimensions as input, maintaining the original aspect ratio and color depth.

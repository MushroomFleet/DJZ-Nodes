# DjzDatamoshV7 (Djz Pixel Sort V7 Advanced)

A sophisticated pixel sorting node that creates artistic datamosh-like effects by sorting pixels based on various image properties. This node offers multiple sorting modes and customizable parameters for creating unique visual effects.

## Parameters

### images
- Type: IMAGE
- Description: The input batch of images to apply the pixel sorting effect to.
- Format: Expects images in BHWC (Batch, Height, Width, Channels) format.

### sort_mode
- Type: Dropdown ["luminance", "hue", "saturation", "laplacian"]
- Description: Determines how pixels are sorted within segments:
  - `luminance`: Sorts based on pixel brightness
  - `hue`: Sorts based on color angles
  - `saturation`: Sorts based on color intensity
  - `laplacian`: Sorts based on edge detection strength

### threshold
- Type: FLOAT
- Default: 0.5
- Range: 0.0 to 1.0
- Step: 0.05
- Description: Controls the creation of sorted segments:
  - Lower values create fewer, longer sorted segments
  - Higher values create more, shorter sorted segments
  - Effect varies by sort mode:
    - luminance: threshold on brightness
    - hue: threshold on color angles
    - saturation: threshold on color intensity
    - laplacian: threshold on edge strength

### rotation
- Type: INT
- Default: -90
- Range: -180 to 180
- Step: 90
- Description: Angle to rotate the sorting direction. Use this to change the orientation of the sorting effect.

### multi_pass
- Type: BOOLEAN
- Default: false
- Description: When enabled, applies all sorting modes sequentially in a fixed order (luminance → hue → saturation → laplacian). When disabled, only uses the selected sort_mode.

### seed
- Type: INT
- Default: 42
- Range: 0 to 4294967295 (0xFFFFFFFF)
- Step: 1
- Description: Random seed for reproducible results.

## Usage Tips

1. **Sort Mode Selection**:
   - `luminance`: Best for creating effects based on image brightness
   - `hue`: Effective for sorting based on color, creating rainbow-like effects
   - `saturation`: Useful for separating vibrant areas from muted ones
   - `laplacian`: Great for edge-based effects, highlighting image contours

2. **Threshold Adjustment**:
   - Start with 0.5 and adjust based on desired segment size
   - Lower values (0.1-0.3) create longer, more dramatic sorting effects
   - Higher values (0.7-0.9) create more subtle, granular effects

3. **Rotation Usage**:
   - -90° (default): Vertical sorting
   - 0°: Horizontal sorting
   - 90°: Inverse vertical sorting
   - 180°: Inverse horizontal sorting

4. **Multi-pass Mode**:
   - Enable for more complex, layered effects
   - Useful when single-mode sorting doesn't provide enough distortion
   - May increase processing time

## Output

Returns the processed image(s) with the pixel sorting effect applied. The output maintains the same dimensions and format as the input.

## Error Handling

- Automatically handles invalid inputs by returning the original image
- Maintains batch processing capability
- Provides console feedback for debugging

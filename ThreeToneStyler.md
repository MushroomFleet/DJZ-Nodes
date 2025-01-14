# Three Tone Styler

A ComfyUI custom node that creates stylized images using three-tone color relationships based on color theory principles. This node allows you to transform images by applying carefully selected color combinations while preserving the original image's structure through luminance mapping.

## Description

The Three Tone Styler node processes images by separating them into three distinct tonal regions (shadows, midtones, and highlights) and applies colors based on established color theory relationships. This can create striking artistic effects while maintaining the image's core details.

## Parameters

### Required Parameters

- **images**: The input image(s) to process
- **base_color**: Hex color code (e.g., "#0000FF") that serves as the primary color for the effect
- **color_relationship**: Determines how additional colors are generated relative to the base color
  - `Primaries`: Uses primary color relationships (120° apart on the color wheel)
  - `Secondaries`: Uses secondary color relationships
  - `Complementary`: Uses the base color and its complement (180° opposite)
  - `Split Complementary`: Uses colors on either side of the complement
  - `Triadic`: Uses three colors equally spaced around the color wheel
  - `Analogous`: Uses adjacent colors on the color wheel
- **tone_mapping**: Determines which tonal region receives the base color
  - `Highlights`: Base color applied to bright areas
  - `Midtones`: Base color applied to middle values
  - `Shadows`: Base color applied to dark areas
- **contrast**: (0.1 to 2.0) Adjusts the contrast between tonal regions
- **threshold_low**: (0.0 to 1.0) Sets the boundary between shadows and midtones
- **threshold_high**: (0.0 to 1.0) Sets the boundary between midtones and highlights

### Optional Parameters

- **smoothing**: (0.0 to 1.0) Controls the smoothness of transitions between tonal regions
- **saturation**: (0.0 to 2.0) Adjusts the color intensity of the effect
- **preserve_luminance**: When enabled, maintains the original image's brightness values

## Usage Tips

1. **Color Selection**:
   - Start with a base color that matches your artistic vision
   - Experiment with different color relationships to achieve various moods:
     - Use `Complementary` for high contrast, dramatic effects
     - Use `Analogous` for more subtle, harmonious results
     - Use `Triadic` for vibrant, balanced compositions

2. **Tonal Control**:
   - Adjust `threshold_low` and `threshold_high` to control the size of each tonal region
   - Use `contrast` to enhance or soften the separation between tones
   - Enable `preserve_luminance` to maintain the original image's light and dark areas

3. **Fine-Tuning**:
   - Use `smoothing` to reduce harsh transitions between colors
   - Adjust `saturation` to control the intensity of the applied colors
   - Try different `tone_mapping` options to vary which tonal region receives the base color

## Technical Details

The node processes images using the following steps:
1. Converts the input image to luminance values
2. Applies contrast adjustment
3. Creates three masks based on luminance thresholds
4. Generates additional colors based on color theory relationships
5. Applies colors to each tonal region
6. Optionally preserves original luminance and adjusts saturation

## Example Applications

- Creating stylized portraits with dramatic color schemes
- Developing unique artistic interpretations of photographs
- Generating mood-specific variations of images
- Exploring color theory relationships in a practical context

## Output

The node outputs a processed image that maintains the original's structure while applying the three-tone color effect. The result is a single IMAGE type that can be further processed by other nodes in your ComfyUI workflow.

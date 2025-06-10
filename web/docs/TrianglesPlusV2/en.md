# TrianglesPlus V2 Node

## Overview
TrianglesPlusV2 is an enhanced version of the TrianglesPlus node that generates abstract art using triangles. This version adds significant customization options including color palettes, size presets, and density controls.

## Parameters

### Required Parameters
- **width** (INT)
  - Default: 1024
  - Minimum: 64
  - Maximum: 4096
  - Description: The width of the generated image in pixels.

- **height** (INT)
  - Default: 1024
  - Minimum: 64
  - Maximum: 4096
  - Description: The height of the generated image in pixels.

- **seed** (INT)
  - Default: 0
  - Minimum: 0
  - Maximum: 4294967295
  - Description: Random seed for reproducible generation.

- **background_color** (STRING)
  - Default: "#000000"
  - Description: Hex color code for the background (e.g., "#FF0000" for red)

- **color_palette** (COMBO)
  - Options:
    - "kandinsky": Bright, artistic colors inspired by the artist
    - "warm": Orange and yellow tones
    - "cool": Blue and green tones
    - "monochrome": Grayscale variations
    - "vibrant": Bold, saturated colors
  - Description: Predefined color schemes for the triangles

- **size_preset** (COMBO)
  - Options:
    - "small": 0.5x multiplier
    - "medium": 1.0x multiplier
    - "large": 2.0x multiplier
  - Description: Controls the size of the generated triangles

- **count_preset** (COMBO)
  - Options:
    - "sparse": 4 triangles
    - "medium": 7 triangles
    - "dense": 12 triangles
  - Description: Determines the number of triangles in the composition

## Color Palettes
1. **kandinsky**
   - Colors: #69D2E7, #A7DBD8, #E0E4CC, #F38630, #FA6900, #FF4E50, #F9D423
   - Style: Artistic, balanced mix of warm and cool tones

2. **warm**
   - Colors: #FF4E50, #FC913A, #F9D423, #EDE574, #E1F5C4
   - Style: Warm, sunset-like colors

3. **cool**
   - Colors: #69D2E7, #A7DBD8, #E0E4CC, #B2C2C1, #8AB8B2
   - Style: Cool, calming ocean-like tones

4. **monochrome**
   - Colors: #FFFFFF, #D9D9D9, #BFBFBF, #8C8C8C, #404040
   - Style: Grayscale variations

5. **vibrant**
   - Colors: #FF1E1E, #FF9900, #FFFF00, #00FF00, #0000FF, #9900FF
   - Style: Bold, rainbow-like colors

## Output
- Returns an IMAGE type that can be used with other ComfyUI nodes
- The output is a tensor in the format (B,H,W,C) where:
  - B: Batch size (always 1)
  - H: Height of the image
  - W: Width of the image
  - C: Color channels (RGB)

## Usage Tips
- Experiment with different color palettes and background colors for varied effects
- Use the size presets to control the scale of the geometric elements
- Adjust the count preset to create either minimal or complex compositions
- Try different seeds with the same settings to generate variations while maintaining the same style

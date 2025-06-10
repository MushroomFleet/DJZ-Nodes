# Video Ring Painter Node

A ComfyUI node that creates customizable ring-shaped highlights around masked areas in images or video frames. This node is useful for creating attention-drawing effects, highlighting specific regions, or creating decorative borders around subjects.

## Inputs

### Required Inputs
- **images**: Batch of input images
- **mask**: Input mask defining the area to create rings around

## Parameters

### Ring Properties
- **stroke_width** (0 - 999, default: 20)
  - Controls the thickness of the ring
  - Measured in pixels
  - Higher values create thicker rings
  - Value of 0 creates no ring

- **stroke_blur** (0 - 100, default: 6)
  - Controls the softness of the ring edges
  - Higher values create softer, more diffused edges
  - Value of 0 creates sharp edges
  - Useful for creating natural-looking transitions

### Color Settings
- **highlight_color** (String, default: "#FF0000")
  - Color of the ring highlight
  - Accepts two formats:
    - Hex color codes (e.g., "#FF0000" for red)
    - RGB values as comma-separated floats (e.g., "1.0,0.0,0.0" for red)

- **background_color** (String, default: "#000000")
  - Color of the area outside the ring
  - Accepts same formats as highlight_color
  - Usually set to black (#000000) for transparency

- **highlight_opacity** (0.0 - 1.0, default: 0.8)
  - Controls the transparency of the ring
  - 1.0 is fully opaque
  - 0.0 is fully transparent
  - Useful for subtle effects or overlays

## Outputs

The node returns two outputs:

1. **preview** (IMAGE)
   - Colored visualization of the ring effect
   - Useful for previewing the effect in the workflow
   - Shows the ring with applied colors and opacity

2. **ring_mask** (MASK)
   - Grayscale mask of the ring shape
   - Useful for further processing or compositing
   - Values range from 0 (transparent) to 1 (opaque)

## Technical Details

### Mask Processing
- Uses morphological operations (dilation/erosion) to create ring shapes
- Applies Gaussian blur for edge softening
- Handles both single frames and batched inputs
- Automatically scales mask values to appropriate range

### Color Processing
- Supports both hex color codes and normalized RGB values
- Converts all colors to normalized RGB (0-1 range) internally
- Applies colors with proper alpha compositing
- Handles invalid color inputs gracefully with fallback to black

## Usage Tips

1. For Sharp Highlight Rings:
   - Use higher stroke_width values (40-100)
   - Keep stroke_blur low (0-2)
   - Set highlight_opacity to 1.0
   - Use bright highlight_color

2. For Subtle Glows:
   - Use moderate stroke_width (10-30)
   - Increase stroke_blur (10-20)
   - Lower highlight_opacity (0.3-0.6)
   - Use softer highlight colors

3. For Animated Effects:
   - Feed animated masks as input
   - Ring will automatically follow mask changes
   - Useful for tracking or emphasis effects

4. For Complex Compositing:
   - Use the ring_mask output
   - Combine with other effects
   - Create custom color gradients
   - Layer multiple rings with different settings

## Common Applications

1. Subject Highlighting:
   - Highlight main subjects in videos
   - Create attention-drawing effects
   - Emphasize specific areas

2. Transition Effects:
   - Create ring wipes
   - Generate reveal effects
   - Build focus transitions

3. UI Elements:
   - Create interactive highlights
   - Build selection indicators
   - Design animated borders

4. Creative Effects:
   - Generate decorative frames
   - Create energy effects
   - Design abstract animations

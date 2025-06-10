# Fish Eye Effect Node

A ComfyUI node that applies a realistic fisheye lens effect to images or image sequences. This effect simulates the characteristic distortion of wide-angle and fisheye lenses, with precise control over various lens characteristics.

## Parameters

### Distortion Strength (0.0 - 1.0)
Controls the intensity of the lens distortion. Now with finer control for subtle effects.
- Default: 0.2 (reduced from 0.5 for more subtle default effect)
- Step size: 0.005 for precise adjustments
- Lower values (0.05-0.15) for gentle wide-angle effects
- Higher values for traditional fisheye looks

### Barrel vs Pincushion (-1.0 - 1.0)
Controls the type of lens distortion.
- Default: 0.0 (balanced)
- Negative values create pincushion distortion (edges pull inward)
- Positive values create barrel distortion (edges push outward)
- Allows blending between distortion types

### Radial Falloff (1.0 - 4.0)
Controls how quickly the distortion increases from center to edge.
- Default: 2.0
- Lower values (1.0-2.0) for more linear distortion
- Higher values (2.0-4.0) for more pronounced edge effects
- Affects the overall character of the lens distortion

### Edge Softness (0.0 - 1.0)
Controls how smoothly the distortion transitions at the edges.
- Default: 0.1 (reduced for more precise control)
- Lower values for defined edges
- Higher values for smoother transitions

### Zoom (0.5 - 2.0)
Adjusts the overall zoom level of the effect.
- Default: 1.0
- Values below 1.0 zoom out, showing more of the scene
- Values above 1.0 zoom in, cropping the edges

### Spherical Aberration (-0.5 - 0.5)
Simulates the optical imperfection where rays entering through different parts of the lens focus at slightly different distances.
- Default: 0.0
- Negative values create inward aberration
- Positive values create outward aberration

### Chromatic Aberration (0.0 - 0.02)
Simulates color fringing commonly seen in wide-angle lenses, where different wavelengths of light focus at slightly different positions.
- Default: 0.0
- Higher values increase the separation between color channels
- Adds realism to the lens effect

## Usage Tips

1. For a subtle wide-angle effect:
   - Distortion_strength: 0.05-0.15
   - Barrel_vs_pincushion: 0.2-0.4
   - Radial_falloff: 1.5-2.0
   - Edge_softness: 0.1
   - Minimal chromatic aberration (0.001)

2. For a classic fisheye look:
   - Distortion_strength: 0.3-0.4
   - Barrel_vs_pincushion: 0.6-0.8
   - Radial_falloff: 2.0-2.5
   - Edge_softness: 0.15-0.2
   - Consider chromatic aberration (0.003-0.005)

3. For a professional wide-angle lens:
   - Distortion_strength: 0.1-0.2
   - Barrel_vs_pincushion: 0.0-0.2
   - Radial_falloff: 1.8-2.2
   - Edge_softness: 0.05-0.1
   - Minimal spherical aberration (0.05)

4. For vintage lens simulation:
   - Distortion_strength: 0.15-0.25
   - Barrel_vs_pincushion: 0.3-0.5
   - Radial_falloff: 2.2-2.8
   - Add both spherical (0.1) and chromatic aberration (0.004)
   - Edge_softness: 0.2

## Technical Details

The effect is implemented using:
- Polar coordinate transformation for accurate lens distortion
- Blend between barrel and pincushion distortion types
- Configurable radial falloff for precise distortion control
- Non-linear distortion with customizable smoothing
- High-quality interpolation using scipy's map_coordinates
- Optional per-channel sampling for chromatic aberration
- Efficient batch processing for image sequences

## Advanced Usage

1. Combining Parameters:
   - Barrel_vs_pincushion and radial_falloff work together to shape the distortion
   - Higher radial_falloff values amplify the barrel/pincushion effect
   - Edge_softness can help blend strong distortions more naturally

2. Fine-Tuning Tips:
   - Start with low distortion_strength and adjust in small increments
   - Use barrel_vs_pincushion to find the right distortion character
   - Adjust radial_falloff to control how the distortion spreads
   - Fine-tune edge_softness last to polish the look

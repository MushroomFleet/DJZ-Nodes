# Noise Factory V3

A powerful ComfyUI custom node for generating various types of colorful noise patterns with image blending capabilities. This node can create complex, procedural noise patterns that can be used standalone or blended with existing images.

## Features

- 8 different noise pattern types
- Adjustable parameters for fine control
- Optional image blending
- Customizable dimensions
- Seed control for reproducibility

## Noise Types

1. **Plasma**
   - Creates smooth, plasma-like patterns with interference effects
   - Produces organic, flowing color transitions

2. **RGB Turbulence**
   - Generates turbulent noise patterns with separate RGB channels
   - Creates chaotic, swirling color effects

3. **Prismatic**
   - Produces spectral color patterns
   - Creates rainbow-like gradients based on noise values

4. **HSV Noise**
   - Generates noise in HSV color space
   - Offers natural color transitions with controllable saturation

5. **Perlin RGB**
   - Classic Perlin noise with separate RGB channels
   - Creates smooth, natural-looking noise patterns

6. **Polychromatic Cellular**
   - Generates Voronoi-like cellular patterns
   - Creates organic, cell-like structures with color interpolation

7. **Rainbow Fractal**
   - Produces fractal patterns with rainbow color mapping
   - Creates complex, self-similar structures with vibrant colors

8. **Color Wavelet**
   - Generates wavelet-based noise with phase-shifted color channels
   - Creates intricate patterns with wave-like characteristics

## Parameters

### Required Parameters

- **width** (default: 512)
  - Width of the output image
  - Range: 64 to 4096 pixels

- **height** (default: 512)
  - Height of the output image
  - Range: 64 to 4096 pixels

- **noise_type** (default: "Plasma")
  - Type of noise pattern to generate
  - Choose from the 8 available noise types

- **scale** (default: 1.0)
  - Controls the scale/zoom level of the noise pattern
  - Range: 0.1 to 10.0
  - Lower values create larger patterns, higher values create more detailed patterns

- **octaves** (default: 4)
  - Number of noise layers to combine
  - Range: 1 to 8
  - Higher values add more detail but increase computation time

- **persistence** (default: 0.5)
  - Controls how much each octave contributes to the final pattern
  - Range: 0.0 to 1.0
  - Higher values create more detailed, rougher patterns

- **saturation** (default: 1.0)
  - Controls color saturation of the generated pattern
  - Range: 0.0 to 2.0
  - Higher values create more vibrant colors

- **noise_strength** (default: 1.0)
  - Controls the blend strength when combining with an input image
  - Range: 0.0 to 1.0
  - 1.0 = full noise pattern, 0.0 = full input image

### Optional Parameters

- **seed** (default: -1)
  - Seed for random number generation
  - Range: -1 to 0xffffffff
  - Use -1 for random seed, or specify a value for reproducible results

- **image**
  - Optional input image to blend with the noise pattern
  - If provided, the noise pattern will be blended with this image based on noise_strength

## Output

- Returns a single IMAGE output that can be used with other ComfyUI nodes
- Output is always in RGB format
- Values are normalized between 0 and 1

## Usage Tips

1. For pure noise generation:
   - Simply connect the width/height inputs and adjust parameters
   - Experiment with different noise types for varied effects

2. For image blending:
   - Connect an input image
   - Use noise_strength to control blend amount
   - Try different noise types to create unique effects

3. For reproducible results:
   - Set a specific seed value
   - Keep all other parameters the same

4. For optimal performance:
   - Start with lower octave values (1-4)
   - Increase octaves gradually if more detail is needed
   - Consider lower resolutions for previewing effects

# NoiseFactory V2

NoiseFactory V2 is an advanced ComfyUI node that generates various types of colorful noise patterns with turbulence control. It offers multiple noise generation algorithms, each producing unique visual effects that can be used in various image generation workflows.

## Features

- 8 different noise pattern types
- Turbulence control for added complexity
- RGB color balance adjustment
- Customizable scale, frequency, and octaves
- Seed control for reproducible results

## Noise Types

1. **Plasma**: Creates smooth, plasma-like patterns with interference effects
2. **RGB Turbulence**: Generates turbulent noise patterns with separate RGB channels
3. **Prismatic**: Produces rainbow-like prismatic effects
4. **HSV Noise**: Creates noise in HSV color space with saturation control
5. **Perlin RGB**: Implements Perlin noise separately for each RGB channel
6. **Polychromatic Cellular**: Generates Voronoi-like cellular patterns with color
7. **Rainbow Fractal**: Creates fractal patterns with rainbow color mapping
8. **Color Wavelet**: Produces wavelet-based patterns with phase-shifted colors

## Parameters

### Required Parameters

- **width** (default: 512, range: 64-4096)
  - Width of the generated noise image in pixels

- **height** (default: 512, range: 64-4096)
  - Height of the generated noise image in pixels

- **noise_type** (default: "RGB Turbulence")
  - The type of noise pattern to generate
  - Choose from the 8 available noise types listed above

- **scale** (default: 1.0, range: 0.1-10.0)
  - Controls the overall scale of the noise pattern
  - Higher values create larger patterns, lower values create finer details

- **octaves** (default: 4, range: 1-8)
  - Number of noise layers to combine
  - More octaves create more detailed patterns but increase generation time

- **persistence** (default: 0.5, range: 0.0-1.0)
  - Controls how much each octave contributes to the final pattern
  - Higher values create more prominent detail layers

- **turbulence** (default: 0.5, range: 0.0-2.0)
  - Amount of turbulent distortion applied to the noise
  - Higher values create more chaotic and distorted patterns

- **frequency** (default: 1.0, range: 0.1-5.0)
  - Base frequency of the noise pattern
  - Higher values create more rapid variations

- **saturation** (default: 1.0, range: 0.0-2.0)
  - Controls color saturation in the generated pattern
  - Values above 1.0 increase saturation, below 1.0 decrease it

- **red_balance** (default: 1.0, range: 0.0-2.0)
  - Multiplier for the red channel intensity

- **green_balance** (default: 1.0, range: 0.0-2.0)
  - Multiplier for the green channel intensity

- **blue_balance** (default: 1.0, range: 0.0-2.0)
  - Multiplier for the blue channel intensity

### Optional Parameters

- **seed** (default: -1, range: -1 to 0xffffffff)
  - Random seed for reproducible patterns
  - Use -1 for random results each time
  - Any other value will produce consistent results

## Output

The node outputs an IMAGE type that can be used with other ComfyUI nodes. The output is always in RGB format with values normalized between 0 and 1.

## Usage Tips

1. **For Organic Patterns**:
   - Use "Plasma" or "RGB Turbulence" with higher turbulence values
   - Increase octaves for more detail
   - Adjust persistence for varying detail prominence

2. **For Abstract Patterns**:
   - Try "Rainbow Fractal" or "Prismatic" types
   - Experiment with different scale and frequency values
   - Use color balance to adjust the final look

3. **For Textural Effects**:
   - "Perlin RGB" or "Color Wavelet" work well
   - Lower scale values create finer textures
   - Adjust turbulence for varying levels of distortion

4. **For Cellular Patterns**:
   - Use "Polychromatic Cellular" type
   - Adjust scale to control cell size
   - Turbulence adds organic distortion to cells

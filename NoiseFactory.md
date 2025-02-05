# NoiseFactory Node

The NoiseFactory node is a powerful ComfyUI custom node that generates various types of colorful noise patterns. It provides multiple noise generation algorithms that can create unique and visually interesting patterns for creative applications.

## Features

- 8 different noise pattern types
- Adjustable parameters for fine-tuning
- High-resolution support (up to 4096x4096)
- Seed control for reproducible results

## Parameters

### Required Parameters

1. **width** (Integer)
   - Default: 512
   - Range: 64 to 4096
   - The width of the generated noise pattern in pixels

2. **height** (Integer)
   - Default: 512
   - Range: 64 to 4096
   - The height of the generated noise pattern in pixels

3. **noise_type** (Dropdown)
   - Available options:
     - Plasma: Creates organic, flowing plasma-like patterns
     - RGB Turbulence: Generates turbulent noise with separate RGB channels
     - Prismatic: Produces spectral color patterns
     - HSV Noise: Creates noise in HSV color space
     - Perlin RGB: Classic Perlin noise with RGB channels
     - Polychromatic Cellular: Cellular/Voronoi-style noise with color
     - Rainbow Fractal: Fractal patterns with rainbow coloring
     - Color Wavelet: Wavelet-based noise with color phase shifts

4. **scale** (Float)
   - Default: 1.0
   - Range: 0.1 to 10.0
   - Controls the zoom level of the noise pattern
   - Lower values create larger patterns, higher values create more detailed patterns

5. **octaves** (Integer)
   - Default: 4
   - Range: 1 to 8
   - Determines the level of detail in the noise
   - Higher values add more layers of detail but increase computation time

6. **persistence** (Float)
   - Default: 0.5
   - Range: 0.0 to 1.0
   - Controls how much each octave contributes to the final pattern
   - Higher values create more dramatic variations

7. **saturation** (Float)
   - Default: 1.0
   - Range: 0.0 to 2.0
   - Affects the color intensity of the generated pattern
   - Primarily used in HSV Noise type, but can influence other patterns

### Optional Parameters

8. **seed** (Integer)
   - Default: -1 (random)
   - Range: -1 to 4294967295 (0xffffffff)
   - Controls the randomization of the pattern
   - Use -1 for random results, or set a specific value for reproducible patterns

## Noise Type Descriptions

### Plasma
Creates smooth, organic patterns reminiscent of plasma effects. Excellent for creating flowing, natural-looking backgrounds or textures.

### RGB Turbulence
Generates turbulent noise patterns with independent RGB channels. Creates chaotic, colorful patterns with strong color separation.

### Prismatic
Produces spectral color patterns based on noise values. Creates rainbow-like effects with smooth transitions between colors.

### HSV Noise
Generates noise in HSV color space, allowing for more natural color variations. Great for creating atmospheric or gradient-like effects.

### Perlin RGB
Classic Perlin noise applied to separate RGB channels. Creates coherent noise patterns with subtle color variations.

### Polychromatic Cellular
Creates Voronoi-like cellular patterns with random color assignments. Excellent for creating organic, cell-like structures.

### Rainbow Fractal
Generates fractal patterns with rainbow color mapping. Creates complex, self-similar patterns with vibrant colors.

### Color Wavelet
Uses wavelet-like functions with phase shifts for each color channel. Creates intricate patterns with wave-like color variations.

## Usage Tips

1. Start with the default parameters and adjust them gradually to understand their effects.
2. The scale parameter is crucial for controlling the overall size of patterns - start with 1.0 and adjust as needed.
3. Increase octaves for more detail, but be aware it will increase generation time.
4. Use the seed parameter when you need to reproduce specific patterns.
5. Different noise types may respond differently to parameter changes - experiment to find the best combinations.

## Output

The node outputs an IMAGE type that can be used with other ComfyUI nodes in your workflow. The output is always in RGB format with values normalized between 0 and 1.

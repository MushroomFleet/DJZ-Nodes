# VideoNoiseFactory

A ComfyUI custom node that generates animated noise patterns with film grain effects. This node combines advanced noise generation techniques with customizable film grain effects to create dynamic, animated textures.

## Description

VideoNoiseFactory generates animated noise patterns that can be used for various purposes such as:
- Creating dynamic backgrounds
- Generating texture animations
- Simulating film grain and video effects
- Producing abstract animated patterns

## Noise Types

The node supports 8 different noise pattern types:

1. **Plasma** - Creates flowing, plasma-like patterns with smooth color transitions
2. **RGB Turbulence** - Generates turbulent noise patterns with separate RGB channels
3. **Prismatic** - Produces rainbow-like prismatic effects with smooth transitions
4. **HSV Noise** - Creates noise in HSV color space for unique color variations
5. **Perlin RGB** - Uses Perlin noise separately for each RGB channel
6. **Polychromatic Cellular** - Generates Voronoi-like cellular patterns with color
7. **Rainbow Fractal** - Creates fractal patterns with rainbow color variations
8. **Color Wavelet** - Produces wave-like patterns with color phase shifts

## Parameters

### Basic Settings
- **width** (64-4096, default: 512) - Output width in pixels
- **height** (64-4096, default: 512) - Output height in pixels
- **num_frames** (1-1000, default: 24) - Number of frames to generate

### Noise Pattern Parameters
- **noise_type** - Select from the 8 available noise types
- **noise_scale** (0.1-10.0, default: 1.0) - Scale of the noise pattern
- **octaves** (1-8, default: 4) - Number of noise layers to combine
- **persistence** (0.0-1.0, default: 0.5) - How much each octave contributes
- **turbulence** (0.0-2.0, default: 0.5) - Amount of turbulent distortion
- **frequency** (0.1-5.0, default: 1.0) - Base frequency of the noise
- **saturation** (0.0-2.0, default: 1.0) - Color saturation level

### Film Grain Parameters
- **grain_preset** - Choose from predefined grain patterns:
  - custom: Use custom grain expression
  - subtle: Light, subtle grain
  - vintage: Classic film grain look
  - unstable_signal: Fluctuating grain pattern
  - dip: Periodic intensity changes
  - ebb: Flowing grain pattern
  - flow: Smooth, animated grain
- **grain_expression** - Custom mathematical expression for grain pattern
- **base_intensity** (0.0-1.0, default: 0.1) - Base intensity of the grain
- **time_scale** (0.1-10.0, default: 1.0) - Speed of grain animation
- **grain_scale** (0.0-1.0, default: 0.2) - Scale of grain texture

### Color Balance
- **red_balance** (0.0-2.0, default: 1.0) - Red channel intensity
- **green_balance** (0.0-2.0, default: 1.0) - Green channel intensity
- **blue_balance** (0.0-2.0, default: 1.0) - Blue channel intensity

### Seeds
- **noise_seed** (0-4294967295) - Seed for noise pattern generation
- **grain_seed** (0-4294967295) - Seed for grain pattern generation

## Film Grain Presets

The node includes several predefined grain patterns:

- **subtle**: Light grain with subtle animation
- **vintage**: Classic film look with organic variation
- **unstable_signal**: More dramatic, fluctuating grain
- **dip**: Periodic intensity changes
- **ebb**: Flowing grain pattern
- **flow**: Smooth, animated grain

## Custom Grain Expressions

You can create custom grain patterns using mathematical expressions. Available functions:
- sin, cos, exp, abs, pow
- normal(mu, sigma) - Normal distribution
- uniform(a, b) - Uniform distribution
- Variables: t (time), pi, e

Example expression:
```
0.08 * normal(0.5, 0.15) * (1 + 0.2 * sin(t/25))
```

## Output

The node outputs an IMAGE type that can be used with other ComfyUI nodes. The output is a sequence of frames that can be used for animation or video effects.

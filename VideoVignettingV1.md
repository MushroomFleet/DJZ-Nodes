# Video Vignetting v1 Node

A ComfyUI node that simulates realistic vignetting effects commonly found in photography and cinematography. This node can create both mechanical vignetting (caused by lens design) and chemical vignetting (caused by film properties), with options for temporal variation over video sequences.

## Vignette Types

- **Mechanical**: Simulates the natural light falloff caused by lens design and physical aperture
- **Chemical**: Recreates the irregular darkening patterns caused by chemical film processes
- **Both**: Combines both mechanical and chemical effects for maximum realism
- **None**: Disables vignetting effects

## Parameters

### Mechanical Vignetting Parameters

- **mechanical_intensity** (0.0 - 1.0, default: 0.5)
  - Controls the strength of the mechanical vignette effect
  - Higher values create darker edges
  - Lower values maintain more edge brightness

- **mechanical_feather** (0.1 - 1.0, default: 0.3)
  - Controls how gradually the mechanical vignette transitions
  - Higher values create softer transitions
  - Lower values create more defined edges

### Chemical Vignetting Parameters

- **chemical_intensity** (0.0 - 1.0, default: 0.4)
  - Controls the strength of the chemical vignette effect
  - Higher values create more pronounced darkening
  - Affects the overall density of the chemical pattern

- **chemical_irregularity** (0.0 - 1.0, default: 0.2)
  - Controls the randomness of the chemical vignette pattern
  - Higher values create more organic, irregular patterns
  - Lower values maintain more uniform darkening

### Temporal Variation

- **temporal_variance** (None/Sine/Random/Pulse/Custom)
  - None: No variation over time
  - Sine: Smooth sinusoidal variation
  - Random: Random fluctuations frame to frame
  - Pulse: Binary on/off variation
  - Custom: User-defined mathematical expression

- **variance_speed** (0.1 - 5.0, default: 1.0)
  - Controls how quickly the temporal variation changes
  - Higher values create faster variations
  - Lower values create slower, more gradual changes

- **variance_amplitude** (0.0 - 1.0, default: 0.2)
  - Controls how much the effect varies over time
  - Higher values create more dramatic variations
  - Lower values maintain more consistent effects

### Custom Animation

- **custom_expression** (String, default: "sin(t * 0.1) * 0.2")
  - Mathematical expression for custom temporal variation
  - Uses 't' as the time variable
  - Supports mathematical functions:
    - sin, cos, tan: Trigonometric functions
    - exp: Exponential function
    - log: Natural logarithm
    - pi: Mathematical constant π

## Technical Details

### Mechanical Vignetting Implementation
- Uses radial gradient calculation from image center
- Applies sigmoid-based feathering for natural transitions
- Scales with image dimensions for consistent look

### Chemical Vignetting Implementation
- Combines multiple octaves of Perlin-like noise
- Creates organic, film-like irregularities
- Scales noise patterns with image size

### Temporal Variation System
- Frame-based timing system
- Multiple variation patterns available
- Safe evaluation of custom expressions
- Smooth interpolation between states

## Usage Tips

1. For Classic Lens Vignetting:
   - Use "Mechanical" type
   - Set moderate mechanical_intensity (0.3-0.5)
   - Use higher mechanical_feather for natural look
   - Keep temporal variation off

2. For Vintage Film Look:
   - Use "Chemical" type
   - Increase chemical_irregularity
   - Add slight temporal variation with "Random"
   - Keep variance_amplitude low (0.1-0.2)

3. For Dynamic Effects:
   - Use "Both" type
   - Enable temporal variation
   - Experiment with custom expressions
   - Example expressions:
     - "sin(t) * 0.3": Simple oscillation
     - "sin(t) * sin(t * 2) * 0.2": Complex pattern
     - "exp(-t % 1) * 0.3": Decay pattern

4. For Maximum Realism:
   - Combine mechanical and chemical effects
   - Use subtle irregularity (0.1-0.3)
   - Add very slight temporal variation
   - Keep amplitudes moderate

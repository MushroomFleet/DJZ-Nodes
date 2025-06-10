# Film Gate Weave Node

A ComfyUI node that simulates the characteristic weaving motion of film as it passes through a projector gate. This effect recreates the subtle (or pronounced) horizontal and vertical movement that occurs due to mechanical imperfections in film projection systems.

## Presets

The node includes several carefully tuned presets for common film weave patterns:

- **none**: No weave effect (stable image)
- **subtle**: Minimal movement, suitable for well-maintained projectors
- **moderate**: Medium movement, typical of standard projection
- **heavy**: Pronounced movement, simulating worn equipment
- **custom**: Full control over weave parameters and motion pattern

## Parameters

### Motion Controls

- **amplitude_x** (0.0 - 20.0, default: 3.0)
  - Controls the amount of horizontal movement
  - Higher values create more side-to-side motion
  - Lower values restrict horizontal movement

- **amplitude_y** (0.0 - 20.0, default: 1.0)
  - Controls the amount of vertical movement
  - Higher values create more up-and-down motion
  - Typically kept lower than amplitude_x for realism

- **frequency** (0.1 - 5.0, default: 1.0)
  - Controls how quickly the weave pattern repeats
  - Higher values create more rapid movement
  - Lower values create slower, more gradual movement

- **phase_shift** (0.0 - 2π, default: 0.0)
  - Offsets the starting point of the weave pattern
  - Useful for creating variation between sequences
  - Measured in radians

### Custom Animation

- **custom_expression** (String, default: "sin(t * 0.1) * 5")
  - Mathematical expression for custom weave patterns
  - Uses 't' as the time variable (0 to 2π)
  - Supports mathematical functions:
    - sin: Sine function
    - cos: Cosine function
    - tan: Tangent function
    - pi: Mathematical constant π

## Preset Details

### Subtle Preset
- Minimal horizontal weave (2.0 amplitude)
- Very slight vertical movement (0.5 amplitude)
- Slower frequency (0.8)
- Simple sinusoidal motion
- Suitable for most vintage film looks

### Moderate Preset
- Medium horizontal weave (4.0 amplitude)
- Light vertical movement (1.0 amplitude)
- Standard frequency (1.2)
- Combined sine/cosine motion
- Good for typical projection effects

### Heavy Preset
- Strong horizontal weave (8.0 amplitude)
- Noticeable vertical movement (2.0 amplitude)
- Faster frequency (1.5)
- Complex motion pattern
- Simulates poorly maintained equipment

## Technical Details

The node implements sophisticated techniques to create realistic film weave:

1. **Motion Generation**
   - Time-based animation system
   - Separate X and Y displacement calculations
   - Smooth interpolation between frames
   - Phase-shifted vertical movement

2. **Image Transformation**
   - 2D mesh grid displacement
   - Bilinear interpolation for smooth movement
   - Edge handling to prevent artifacts
   - Proper scaling with image dimensions

3. **Expression Evaluation**
   - Safe mathematical expression parsing
   - Support for common trigonometric functions
   - Time normalization for consistent motion
   - Error handling for invalid expressions

## Usage Tips

1. For Modern Film Look:
   - Use "subtle" preset
   - Reduce amplitude_x to 1.0-2.0
   - Keep amplitude_y below 0.5
   - Use slower frequency (0.5-0.8)

2. For Vintage Projection:
   - Start with "moderate" preset
   - Increase amplitude_x slightly
   - Add custom expression for variation
   - Example: "sin(t * 1.2) * 4 + sin(t * 0.4) * 2"

3. For Damaged Film Effect:
   - Use "heavy" preset
   - Increase both amplitudes
   - Add faster frequency
   - Combine with other film damage effects

4. For Custom Patterns:
   - Start with basic sinusoidal motion
   - Add complexity gradually
   - Combine multiple frequencies
   - Example expressions:
     - Simple: "sin(t) * 5"
     - Complex: "sin(t * 1.5) * 4 + cos(t * 0.7) * 2"
     - Random: "sin(t) * (3 + sin(t * 2) * 2)"

## Common Applications

1. Film Restoration:
   - Simulate original projection characteristics
   - Add period-appropriate movement
   - Maintain subtle, consistent motion

2. Vintage Effects:
   - Combine with grain and scratches
   - Use moderate weave settings
   - Match movement to film era

3. Creative Effects:
   - Experiment with custom expressions
   - Create rhythmic motion patterns
   - Synchronize with audio or scene cuts

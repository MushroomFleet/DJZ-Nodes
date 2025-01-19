# Video Chromatic Aberration Node

A ComfyUI node that simulates chromatic aberration effects commonly seen in photography and cinematography. This node can create both static and animated color fringing effects by independently controlling the offset of red and blue color channels.

## Animation Presets

- **none**: Static chromatic aberration effect
- **custom**: User-defined mathematical expression for animation
- **pulse**: Pulsating intensity effect
- **broken_lighting**: Irregular, flickering effect
- **wave**: Smooth, wave-like variation
- **random_jitter**: Random fluctuations in intensity
- **strobe**: Alternating strong/weak effect

## Parameters

### Channel Offsets

- **red_offset_x** (-50.0 - 50.0, default: 5.0)
  - Horizontal offset for red channel
  - Positive values shift right
  - Negative values shift left

- **red_offset_y** (-50.0 - 50.0, default: 0.0)
  - Vertical offset for red channel
  - Positive values shift down
  - Negative values shift up

- **blue_offset_x** (-50.0 - 50.0, default: -5.0)
  - Horizontal offset for blue channel
  - Positive values shift right
  - Negative values shift left

- **blue_offset_y** (-50.0 - 50.0, default: 0.0)
  - Vertical offset for blue channel
  - Positive values shift down
  - Negative values shift up

### Animation Controls

- **animation_speed** (0.1 - 10.0, default: 1.0)
  - Controls how quickly the animation cycles
  - Higher values create faster variations
  - Lower values create slower changes

- **effect_intensity** (0.0 - 5.0, default: 1.0)
  - Overall strength of the effect
  - Multiplier for animation amplitude
  - Values above 1.0 create exaggerated effects

- **chromatic_blur** (0.0 - 10.0, default: 0.0)
  - Adds blur to offset channels
  - Creates softer color transitions
  - Higher values increase blur radius

### Custom Animation

- **custom_expression** (String, default: "sin(t * 2 * pi) * intensity")
  - Mathematical expression for custom animation
  - Uses variables:
    - t: Time variable (0 to 2π)
    - intensity: Effect intensity value
    - pi: Mathematical constant π
  - Supports functions:
    - sin, cos, tan: Trigonometric functions
    - abs: Absolute value
    - pow: Power function

## Preset Details

### Pulse
- Rhythmic intensity variation
- Smooth transitions
- Good for heartbeat-like effects
- Based on absolute sine function

### Broken Lighting
- Random variations
- Irregular timing
- Simulates electrical interference
- Combines sine and random functions

### Wave
- Smooth, continuous variation
- Predictable pattern
- Good for subtle animation
- Based on sine function

### Random Jitter
- Small random variations
- Continuous updates
- Good for unstable effects
- Uses random number generation

### Strobe
- Sharp intensity changes
- Binary states (strong/weak)
- Good for dramatic effects
- Based on threshold sine function

## Technical Details

### Channel Processing
- Independent RGB channel control
- Affine transformation for offsets
- Border reflection handling
- Optional Gaussian blur

### Animation System
- Time-based animation
- Safe expression evaluation
- Multiple preset patterns
- Smooth frame interpolation

### Image Processing
- Proper color space handling
- Edge artifact prevention
- Channel recombination
- Intensity normalization

## Usage Tips

1. For Lens Distortion Look:
   - Use static (none) preset
   - Opposite red/blue horizontal offsets
   - Minimal vertical offset
   - Example settings:
     - red_offset_x: 5.0
     - blue_offset_x: -5.0
     - effect_intensity: 1.0

2. For Digital Glitch Effect:
   - Use random_jitter preset
   - Higher effect_intensity
   - Add some vertical offset
   - Example settings:
     - effect_intensity: 2.0-3.0
     - animation_speed: 2.0-4.0
     - chromatic_blur: 0.5-1.0

3. For Vintage Film Look:
   - Use wave preset
   - Subtle offsets
   - Add chromatic blur
   - Example settings:
     - effect_intensity: 0.5-1.0
     - chromatic_blur: 1.0-2.0
     - animation_speed: 0.5-0.8

4. For Custom Animation:
   - Start with basic sine wave
   - Add complexity gradually
   - Example expressions:
     - "sin(t) * intensity"
     - "sin(t) * cos(t * 2) * intensity"
     - "abs(sin(t * 3)) * intensity"

## Common Applications

1. Film Emulation:
   - Simulate lens characteristics
   - Add period-appropriate effects
   - Create vintage aesthetics

2. Music Videos:
   - Create rhythmic effects
   - Sync with beat
   - Dynamic color separation

3. Glitch Art:
   - Create digital artifacts
   - Random distortions
   - Technical malfunction simulation

4. Artistic Effects:
   - Creative color separation
   - Dynamic visual interest
   - Emphasis on movement

## Technical Considerations

1. Performance Impact:
   - Higher chromatic_blur values increase processing time
   - Complex custom expressions may impact performance
   - Animation requires frame-by-frame processing

2. Quality Control:
   - Monitor edge artifacts
   - Check for color accuracy
   - Verify animation smoothness

3. Resolution Handling:
   - Effects scale with image resolution
   - Adjust offsets for different resolutions
   - Consider final output format

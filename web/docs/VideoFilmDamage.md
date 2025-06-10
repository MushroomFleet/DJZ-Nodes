# Film Damage Effect Node

A ComfyUI node that simulates various types of film damage and aging effects commonly seen in vintage footage. This node can create realistic scratches, dust, chemical deterioration, and other artifacts that mimic the appearance of damaged or aged film material.

## Presets

The node comes with several built-in presets for quick application of film damage effects:

- **none**: No damage effects applied
- **light**: Subtle aging effects suitable for slightly worn footage
- **medium**: Balanced damage effects for typical vintage look
- **heavy**: Significant damage effects for well-worn footage
- **severe**: Extreme damage effects for heavily deteriorated film
- **custom**: Fully customizable parameters for precise control

## Parameters

### Main Parameters

- **damage_preset** (none/light/medium/heavy/severe/custom)
  - Predefined combinations of damage effects
  - Select "custom" to manually adjust all parameters

- **time_variance** (0.0 - 1.0, default: 0.5)
  - Controls how much the damage effects vary over time
  - Higher values create more dynamic, changing damage patterns
  - Lower values maintain more consistent damage effects

### Scratch Effects

- **scratch_density** (0.0 - 1.0, default: 0.3)
  - Controls the amount of vertical scratches
  - Higher values create more scratches
  - Scales with image size for consistent appearance

- **scratch_width_scale** (0.1 - 5.0, default: 1.0)
  - Multiplier for scratch thickness
  - Higher values create wider scratches
  - Values below 1.0 create finer scratches

### Dust and Hair Effects

- **dust_amount** (0.0 - 1.0, default: 0.2)
  - Controls the quantity of dust particles and hair-like artifacts
  - Affects both small dust spots and longer hair-like marks
  - Scales with image size

- **dust_size_scale** (0.1 - 5.0, default: 1.0)
  - Multiplier for dust particle size
  - Higher values create larger dust particles
  - Also affects the thickness of hair-like artifacts

### Chemical Deterioration

- **deterioration_strength** (0.0 - 1.0, default: 0.25)
  - Controls the intensity of chemical deterioration effects
  - Simulates color fading and emulsion damage
  - Creates organic-looking patterns of degradation

### Custom Animation

- **custom_expression** (String, default: "sin(t * 0.1) * 0.5 + 0.5")
  - Mathematical expression for custom time-based variation
  - Uses 't' as the time variable (0.0 to 1.0)
  - Supports basic mathematical functions (sin, cos, tan, exp, sqrt)
  - Result should stay within 0.0 to 1.0 range for best results

## Technical Details

The node implements several sophisticated techniques to create realistic film damage:

1. **Scratch Generation**
   - Vertical-oriented damage patterns
   - Variable length and intensity
   - Scale-aware implementation for consistent look at different resolutions

2. **Dust and Hair Simulation**
   - Multiple particle types (dust spots and hair-like artifacts)
   - Random distribution with natural clustering
   - Size scaling based on image dimensions

3. **Chemical Deterioration**
   - Perlin-like noise patterns for organic appearance
   - Channel-specific degradation
   - Gaussian blurring for natural edge transitions

4. **Temporal Variation**
   - Time-based modulation of effect intensities
   - Customizable through mathematical expressions
   - Smooth transitions between frames

## Usage Tips

1. For Classic Film Look:
   - Start with "medium" preset
   - Adjust scratch_density and dust_amount to taste
   - Keep deterioration_strength relatively low

2. For Heavily Damaged Look:
   - Use "heavy" or "severe" preset as base
   - Increase scratch_width_scale for more visible scratches
   - Increase deterioration_strength for more color damage

3. For Custom Animation:
   - Switch to "custom" preset
   - Experiment with custom_expression for unique patterns
   - Example expressions:
     - "sin(t * 3.14 * 2)": Simple oscillation
     - "t": Linear progression
     - "cos(t * 4) * 0.25 + 0.5": Faster, dampened oscillation

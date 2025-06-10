# Halation & Bloom Effect Node

A ComfyUI node that simulates halation and bloom effects commonly seen in film photography and cinematography. This node can create both the color-specific halation effect (where bright areas bleed into darker areas with color shifts) and general bloom effects (uniform glow around bright areas).

## Effect Modes

- **Halation**: Simulates film halation, where bright areas create color-specific blooming
- **Bloom**: Creates a uniform glow around bright areas
- **Both**: Combines both halation and bloom effects for maximum impact

## Parameters

### Main Controls

- **intensity** (0.0 - 5.0, default: 1.0)
  - Controls the overall strength of the effect
  - Higher values create stronger glows
  - Values above 1.0 create exaggerated effects

- **threshold** (0.0 - 1.0, default: 0.6)
  - Brightness level where the effect begins
  - Higher values affect only the brightest areas
  - Lower values affect more of the image

- **radius** (1 - 100, default: 15)
  - Controls the size of the glow effect
  - Higher values create larger, softer glows
  - Lower values create tighter, more focused effects

### Color Controls

- **red_offset** (0.5 - 2.0, default: 1.2)
  - Controls the spread of the red channel in halation
  - Higher values create more red bleed
  - Simulates the characteristic red halation of film

- **chromatic_aberration** (0.0 - 2.0, default: 0.5)
  - Creates color separation around bright areas
  - Higher values increase color fringing
  - Adds to the photographic realism

### Animation Controls

- **temporal_variation** (0.0 - 1.0, default: 0.2)
  - Controls how much the effect varies over time
  - Creates subtle animation in the glow
  - Higher values create more dynamic changes

## Technical Details

### Halation Implementation
- Channel-specific Gaussian blur
- Different spread rates for R/G/B channels
- Luminance-based masking
- Red channel emphasis for film-like look

### Bloom Implementation
- Uniform multi-channel blur
- Threshold-based bright area isolation
- Intensity-controlled additive blending
- Temporal smoothing

### Color Processing
- LAB color space for luminance detection
- RGB channel separation for chromatic effects
- Proper color space handling for accurate results
- Smooth blending between effects

### Animation System
- Sine-based temporal variation
- Frame-aware parameter modulation
- Smooth transitions between states
- Maintains consistent look across sequences

## Usage Tips

1. For Classic Film Halation:
   - Use "Halation" mode
   - Set intensity around 1.0-1.5
   - Keep threshold high (0.7-0.8)
   - Increase red_offset slightly
   - Use moderate radius (10-20)

2. For Modern Anamorphic Look:
   - Use "Both" mode
   - Higher intensity (1.5-2.0)
   - Lower threshold (0.4-0.5)
   - Increase chromatic_aberration
   - Larger radius (25-40)

3. For Subtle Enhancement:
   - Use "Bloom" mode
   - Low intensity (0.3-0.7)
   - High threshold (0.8-0.9)
   - Small radius (5-10)
   - Minimal temporal_variation

4. For Dream Sequence:
   - Use "Both" mode
   - High intensity (2.0-3.0)
   - Low threshold (0.3-0.4)
   - Large radius (40-60)
   - Increase temporal_variation

## Common Applications

1. Film Emulation:
   - Simulate specific film stock characteristics
   - Recreate vintage lens effects
   - Add period-appropriate glow

2. Music Videos:
   - Create dreamy, ethereal looks
   - Enhance bright highlights
   - Add dynamic light effects

3. Fantasy Sequences:
   - Ethereal glow effects
   - Soft, dreamy highlights
   - Temporal animation for magical effects

4. Beauty Shots:
   - Soft, flattering glow
   - Reduced harsh highlights
   - Enhanced skin tones through red halation

## Technical Considerations

1. Performance Impact:
   - Larger radius values increase processing time
   - Both mode requires more computation
   - Temporal variation adds minimal overhead

2. Resolution Handling:
   - Effects scale with image resolution
   - Adjust radius for different resolutions
   - Consider final output size when setting parameters

3. Color Management:
   - Works in linear color space
   - Preserves color accuracy
   - Handles high dynamic range properly

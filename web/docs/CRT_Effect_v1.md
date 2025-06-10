# CRT Effect v1 Node

A ComfyUI node that simulates the distinctive visual characteristics of CRT (Cathode Ray Tube) displays. This node can recreate various types of CRT screens, from classic arcade monitors to vintage television sets, with customizable parameters for authentic retro effects.

## Presets

The node includes several carefully tuned presets that emulate different types of CRT displays:

- **Custom**: Full manual control over all parameters
- **Arcade**: High contrast, sharp scanlines, moderate curvature (classic arcade cabinet look)
- **Consumer TV**: Softer image, more pronounced curvature, higher chromatic effects
- **Professional Monitor**: Minimal distortion, sharp image, subtle scanlines
- **Black & White TV**: Monochrome output with vintage TV characteristics

## Parameters

### Display Structure

- **scanline_intensity** (0.0 - 1.0, default: 0.3)
  - Controls the darkness of scanlines
  - Higher values create more pronounced scan lines
  - Lower values create a more subtle effect

- **scanline_spacing** (1 - 10, default: 2)
  - Controls the distance between scanlines
  - Lower values create denser scanlines
  - Higher values create more spaced out lines

### Screen Effects

- **phosphor_blur** (0.0 - 2.0, default: 0.5)
  - Simulates phosphor persistence blur
  - Higher values create softer images
  - Lower values maintain sharper details

- **bloom_intensity** (0.0 - 1.0, default: 0.2)
  - Controls the glow around bright areas
  - Higher values create more pronounced blooming
  - Simulates light scatter in CRT phosphors

- **bloom_spread** (3 - 51, default: 15)
  - Controls how far the bloom effect extends
  - Must be an odd number
  - Higher values create wider glows

### Screen Geometry

- **curvature** (0.0 - 0.5, default: 0.1)
  - Simulates CRT screen curvature
  - Higher values create more pronounced bulging
  - Affects both horizontal and vertical curves

- **vignette_intensity** (0.0 - 1.0, default: 0.2)
  - Darkening effect around screen edges
  - Higher values create stronger edge darkening
  - Simulates natural light falloff

### Image Adjustments

- **brightness** (0.5 - 2.0, default: 1.0)
  - Overall screen brightness
  - Values above 1.0 increase brightness
  - Values below 1.0 decrease brightness

- **contrast** (0.5 - 2.0, default: 1.0)
  - Image contrast adjustment
  - Higher values increase contrast
  - Lower values decrease contrast

### Color Effects

- **rgb_offset** (0.0 - 5.0, default: 0.5)
  - Simulates RGB phosphor misalignment
  - Creates chromatic separation
  - Higher values increase color fringing
  - Set to 0 for no color separation

## Preset Details

### Arcade Monitor
- Sharp, high-contrast image
- Prominent scanlines
- Moderate bloom
- Slight curvature
- Enhanced brightness and contrast

### Consumer TV
- Softer image quality
- More pronounced color fringing
- Significant curvature
- Stronger vignetting
- Wider scanline spacing

### Professional Monitor
- Minimal distortion
- Sharp image quality
- Subtle scanlines
- Very slight curvature
- Accurate color reproduction

### Black & White TV
- Monochrome conversion
- Strong phosphor blur
- Pronounced curvature
- Heavy vignetting
- Wide scanline spacing

## Technical Details

The node implements several sophisticated techniques to create authentic CRT effects:

1. **Scanline Generation**
   - Mathematically accurate scanline patterns
   - Variable intensity and spacing
   - Proper scaling with image size

2. **Phosphor Simulation**
   - Gaussian blur for phosphor persistence
   - Multi-pass bloom for light scatter
   - RGB channel separation for color CRTs

3. **Screen Geometry**
   - 2D displacement mapping for screen curvature
   - Radial vignette calculation
   - Proper aspect ratio preservation

4. **Color Processing**
   - RGB channel offsetting for chromatic effects
   - Brightness/contrast adjustment
   - Special handling for B&W mode

## Usage Tips

1. For Classic Gaming Look:
   - Use "Arcade" preset as base
   - Increase scanline_intensity slightly
   - Maintain moderate curvature
   - Enhance contrast slightly

2. For Vintage TV Effect:
   - Start with "Consumer TV" preset
   - Increase phosphor_blur
   - Add more rgb_offset
   - Enhance vignette_intensity

3. For Clean Professional Look:
   - Use "Professional Monitor" preset
   - Reduce all distortion effects
   - Maintain subtle scanlines
   - Keep minimal curvature

4. For Custom Effects:
   - Start with closest preset
   - Adjust parameters incrementally
   - Consider interaction between effects
   - Balance between authenticity and clarity

# Fish Eye Effects V2

A powerful and versatile lens effect node for ComfyUI that simulates various camera lens characteristics, from ultra-wide fisheye to telephoto effects. This node provides realistic lens distortion, depth of field effects, chromatic aberration, and vignetting.

## Features

- Multiple lens presets simulating real focal lengths
- Switchable between regular lens distortion and fisheye projection
- Customizable distortion strength
- Depth-based focus effects
- Chromatic aberration simulation
- Bokeh blur for depth of field effects
- Adjustable vignette strength

## Lens Presets

The node includes several presets that simulate common camera focal lengths:

- **14MM Ultra Wide**: Extreme wide-angle with strong distortion and vignetting
- **24MM Wide**: Wide-angle with moderate distortion
- **35MM Standard**: Standard wide-angle with subtle distortion
- **50MM Normal**: Minimal distortion, closest to human vision
- **85MM Portrait**: Very subtle distortion, ideal for portraits
- **100MM Telephoto**: Minimal distortion with slight compression
- **200MM Super Telephoto**: Nearly distortion-free with subtle effects
- **Custom**: Fully customizable settings

## Parameters

### Main Controls

- **Lens Preset**: Choose from the predefined focal length presets
- **Fisheye Mode**: Toggle between regular lens distortion and fisheye projection
  - When OFF: Uses polynomial distortion typical of regular lenses
  - When ON: Uses equidistant projection typical of fisheye lenses

### Advanced Parameters

- **Custom Distortion** (-1.0 to 1.0)
  - Adds or subtracts distortion from the preset value
  - Negative values create barrel distortion
  - Positive values create pincushion distortion
  - Default: 0.0

- **Focus Distance** (0.1 to 10.0)
  - Controls the focal plane distance
  - Lower values focus closer to the camera
  - Higher values focus further away
  - Default: 1.0

- **Vignette Strength** (0.0 to 1.0)
  - Controls the darkness of the corners
  - Adds to the preset's built-in vignette
  - Higher values create stronger darkening
  - Default: 0.0

- **Chromatic Aberration** (0.0 to 0.02)
  - Simulates color fringing effects
  - Creates RGB channel separation
  - Higher values increase the effect
  - Default: 0.0

- **Bokeh Blur** (0.0 to 1.0)
  - Creates depth-of-field blur
  - Works in conjunction with Focus Distance
  - Higher values increase blur strength
  - Default: 0.0

## Usage Tips

1. Start with a lens preset that matches your desired look
2. Adjust the custom distortion to fine-tune the lens effect
3. Use focus distance and bokeh blur together for depth effects
4. Add chromatic aberration sparingly for vintage or artistic effects
5. Fine-tune vignette strength to enhance the mood or draw attention to the center

## Technical Details

- Input: Accepts standard ComfyUI image tensors
- Output: Returns processed image with applied lens effects
- Processing: Maintains original image dimensions and aspect ratio
- Color: Preserves color channels while applying effects

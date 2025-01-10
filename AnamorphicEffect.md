# Anamorphic Lens Effect Node

A ComfyUI custom node that simulates the distinctive characteristics of anamorphic lenses, commonly used in cinematic filmmaking. This node applies various effects including oval bokeh, horizontal lens flares, and aspect ratio adjustments to create that signature anamorphic look.

## Features

- Anamorphic squeeze ratio adjustment
- Horizontal lens flares with customizable properties
- Oval/elliptical bokeh simulation
- Horizontal chromatic aberration
- Real-time preview with slider controls

## Parameters

### Aspect and Squeeze
- **squeeze_ratio** (default: 1.33, range: 1.0-2.0)
  - Controls the horizontal squeeze factor of the image
  - Higher values create a wider aspect ratio when unsqueezed
  - Classic anamorphic lenses typically use 1.33x (2:1) or 2.0x (2.39:1)

### Lens Flare Controls
- **flare_intensity** (default: 0.3, range: 0.0-1.0)
  - Controls the brightness of the horizontal lens flares
  - Higher values create more pronounced flares
  
- **flare_length** (default: 0.5, range: 0.1-1.0)
  - Determines how far the lens flares stretch horizontally
  - Higher values create longer, more dramatic streaks
  
- **flare_color** (default: 0.7, range: 0.0-1.0)
  - Adjusts the color temperature of the flares
  - Lower values create cooler, bluer flares
  - Higher values create warmer, more golden flares

### Bokeh Controls
- **bokeh_amount** (default: 0.0, range: 0.0-1.0)
  - Controls the strength of the bokeh blur effect
  - Higher values create more pronounced background blur
  
- **bokeh_elliptical** (default: 0.5, range: 0.0-1.0)
  - Adjusts how oval-shaped the bokeh becomes
  - Higher values create more horizontally stretched bokeh
  - Lower values maintain more circular bokeh

### Chromatic Aberration
- **chromatic_aberration** (default: 0.0, range: 0.0-1.0)
  - Controls the amount of horizontal color separation
  - Creates the characteristic blue/red fringing along high-contrast edges
  - Higher values increase the separation distance between colors

## Usage Tips

1. **For Classic Anamorphic Look:**
   - Set squeeze_ratio to 1.33 or 2.0
   - Use moderate flare_intensity (0.2-0.4)
   - Add slight chromatic_aberration (0.1-0.2)

2. **For Dramatic Lens Flares:**
   - Increase flare_intensity above 0.5
   - Adjust flare_length to taste
   - Experiment with flare_color for different moods

3. **For Bokeh Control:**
   - Start with bokeh_amount around 0.3-0.5
   - Adjust bokeh_elliptical to match your squeeze_ratio
   - Higher squeeze ratios typically look better with more elliptical bokeh

## Technical Details

- The node processes images using GPU acceleration when available
- All effects are applied in a physically-inspired order:
  1. Anamorphic squeeze
  2. Oval bokeh simulation
  3. Lens flare generation
  4. Chromatic aberration
- All parameters use normalized ranges (0-1) for intuitive control
- Real-time preview updates as parameters are adjusted

## Example Workflow

1. Connect your image source to the node's input
2. Adjust squeeze_ratio based on your desired aspect ratio
3. Fine-tune lens flares and bokeh to match your creative vision
4. Add subtle chromatic aberration for enhanced realism
5. Connect the output to your next processing node or final output

This node is perfect for creating cinematic looks, music videos, or any content where you want to achieve that distinctive anamorphic aesthetic without the need for expensive specialty lenses.

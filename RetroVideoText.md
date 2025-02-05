# RetroVideoText Node

A ComfyUI custom node that adds retro-style text overlays to images with various CRT and vintage video effects.

## Description

RetroVideoText allows you to add text to your images with classic CRT monitor and retro video effects, including:
- Customizable text with multiple font options
- Glowing text effects
- CRT scanlines
- Chromatic aberration
- Multiple color presets reminiscent of vintage displays

## Parameters

### Required Parameters

- **images**: The input image(s) to process
- **text**: The text to display (default: "SYSTEM LOADING...")
- **font**: Choice of font to use. Can use either:
  - "default" system font
  - Any .TTF font file placed in the `/TTF/` directory
- **position**: Text position on the image
  - "top"
  - "center"
  - "bottom" (default)
- **font_size**: Size of the text (8-256 pixels, default: 32)
- **text_color**: Color preset for the text
  - "green" (default) - Classic terminal green
  - "amber" - Vintage monitor amber
  - "white" - Standard white
  - "cyan" - Electric blue
  - "magenta" - Neon purple
- **glow_radius**: Size of the text glow effect (0-20 pixels, default: 3)
- **glow_intensity**: Strength of the glow effect (0.0-1.0, default: 0.5)
- **scanline_spacing**: Distance between CRT scanlines (1-20 pixels, default: 3)
- **scanline_alpha**: Opacity of the scanlines (0.0-1.0, default: 0.3)
- **chromatic_aberration**: Amount of RGB color separation (0-10 pixels, default: 2)

## Usage Tips

1. **Font Selection**:
   - Place any custom TTF fonts in the `/TTF/` directory to make them available
   - The node will automatically detect and list available fonts
   - Falls back to system fonts if custom fonts fail to load

2. **Text Effects**:
   - Combine glow and chromatic aberration for authentic CRT look
   - Adjust scanline spacing and alpha for different monitor styles
   - Use different color presets to match various vintage displays

3. **Positioning**:
   - Text is automatically centered horizontally
   - Vertical position can be adjusted using the position parameter
   - Maintains proper spacing from edges

## Examples

### Classic Terminal Look
```
- text: "SYSTEM READY"
- text_color: "green"
- glow_radius: 3
- glow_intensity: 0.5
- scanline_spacing: 3
- position: "bottom"
```

### Vintage Amber Display
```
- text: "LOADING..."
- text_color: "amber"
- glow_radius: 4
- glow_intensity: 0.7
- chromatic_aberration: 2
- position: "center"
```

### High-Tech Cyan
```
- text: "INITIALIZING"
- text_color: "cyan"
- glow_radius: 5
- glow_intensity: 0.8
- scanline_spacing: 2
- chromatic_aberration: 3
- position: "top"
```

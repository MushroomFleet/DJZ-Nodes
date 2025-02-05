# 🖥️ Screensaver Generator

The Screensaver Generator node creates classic screensaver-style animations, offering various nostalgic presets like pipes, starfield, matrix rain, bouncing shapes, and plasma effects. Each animation can be customized with different color schemes and parameters.

## Input Parameters

### Required

- **width** (64 - 4096, default: 512)
  - The width of the generated animation in pixels
  - Values are rounded to multiples of 64

- **height** (64 - 4096, default: 512)
  - The height of the generated animation in pixels
  - Values are rounded to multiples of 64

- **fps** (1 - 60, default: 30)
  - Frames per second for the animation
  - Higher values create smoother motion

- **max_frames** (1 - 9999, default: 60)
  - Total number of frames to generate
  - Longer sequences require more processing time

- **preset** (dropdown selection)
  - `pipes`: 3D-style flowing pipes reminiscent of Windows 95
  - `starfield`: Space travel simulation with moving stars
  - `matrix`: Digital rain effect inspired by The Matrix
  - `bounce`: Colorful shapes bouncing around the screen
  - `plasma`: Psychedelic flowing plasma patterns

- **color_scheme** (dropdown selection)
  - `classic`: Traditional blue and cyan colors
  - `rainbow`: Full spectrum of bright colors
  - `neon`: Vibrant cyberpunk-style colors
  - `monochrome`: Single-color variations (green)

- **speed** (0.1 - 5.0, default: 1.0)
  - Controls the animation speed
  - Higher values create faster movement

## Preset Details

### Pipes
- Generates flowing 3D-style pipes that grow and branch
- Colors change as new pipes are created
- Speed affects pipe growth rate

### Starfield
- Simulates space travel through a star field
- Stars closer to viewer appear larger
- Speed affects travel velocity
- Color scheme affects star colors at different depths

### Matrix
- Creates falling digital characters
- Green-tinted by default (regardless of color scheme)
- Speed affects character fall rate
- Characters fade out as they fall

### Bounce
- Generates bouncing geometric shapes
- Shapes bounce off screen edges
- Speed affects bounce velocity
- Colors based on selected color scheme

### Plasma
- Creates flowing plasma-style patterns
- Continuous color transitions
- Speed affects pattern flow rate
- Color scheme determines pattern palette

## Color Schemes

### Classic
- Primary: Blue (0, 0, 255)
- Secondary: Cyan (0, 255, 255)
- Tertiary: Green (0, 255, 0)

### Rainbow
- Full spectrum of colors
- 12 evenly spaced hues
- Maximum saturation and brightness

### Neon
- Magenta (255, 0, 255)
- Cyan (0, 255, 255)
- Yellow (255, 255, 0)

### Monochrome
- Bright Green (0, 255, 0)
- Medium Green (0, 192, 0)
- Dark Green (0, 128, 0)

## Usage Tips

1. **For Smooth Animations**:
   - Use higher FPS (30-60)
   - Keep speed around 1.0
   - Generate enough frames for your sequence

2. **For Retro Look**:
   - Use lower resolutions (512x512 or less)
   - Choose classic or monochrome color schemes
   - Moderate speed (0.5-1.0)

3. **For Modern Effects**:
   - Use higher resolutions (1024x1024+)
   - Choose rainbow or neon color schemes
   - Experiment with higher speeds

4. **For Performance**:
   - Lower resolution for faster generation
   - Reduce max_frames for quicker results
   - Balance FPS with sequence length

## Output

- Returns a batch of image frames as a tensor
- Each frame maintains the specified width and height
- RGB format with values normalized to 0-1 range

## Note

The generated animations are deterministic within each run but use random elements for initialization. This means running the node multiple times with the same parameters may produce slightly different variations of the same effect. The processing time increases with resolution, number of frames, and complexity of the chosen preset.

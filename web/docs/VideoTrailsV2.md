# Video Trails Effect V2

The Video Trails Effect V2 is an enhanced version of the original Video Trails node, featuring improved motion detection, color bleeding effects, and exponential decay for more natural-looking trails. This version processes motion detection per color channel, allowing for more authentic color separation effects.

## Input Parameters

### Required

- **images**: The input batch of images/frames to process

- **trail_strength** (0.1 - 0.99, default: 0.85)
  - Controls the intensity of the trailing effect
  - Higher values create more pronounced, longer-lasting trails
  - Lower values produce subtler, quicker-fading trails

- **decay_rate** (0.01 - 0.5, default: 0.15)
  - Controls how quickly trails fade using exponential decay
  - Higher values cause faster trail dissipation
  - Lower values make trails persist longer

- **color_bleed** (0.0 - 1.0, default: 0.3)
  - Controls the amount of color channel separation in the trails
  - 0.0 disables color bleeding completely
  - Higher values create more pronounced RGB channel separation
  - Creates a chromatic aberration-like effect in the trails

- **blur_amount** (0.0 - 2.0, default: 0.5)
  - Controls the Gaussian blur applied to the trails
  - 0.0 creates sharp, defined trails
  - Higher values produce smoother, more diffused trails
  - Values above 1.0 create very soft, dreamy effects

- **threshold** (0.01 - 0.5, default: 0.1)
  - Sets the sensitivity of motion detection
  - Lower values detect subtle movements
  - Higher values only respond to more significant motion

## Key Improvements Over V1

1. **Per-Channel Motion Detection**
   - Processes each RGB channel separately
   - Creates more nuanced and colorful trail effects
   - Better preserves color information in motion

2. **Color Bleeding Effect**
   - Adds controllable RGB channel separation
   - Creates artistic chromatic aberration effects
   - Enhances the visual appeal of trails

3. **Exponential Decay**
   - More natural-looking trail fadeout
   - Smoother transition between frames
   - Better control over trail persistence

4. **Enhanced Blur**
   - Uses Gaussian blur for smoother results
   - Adjustable kernel size based on blur strength
   - Creates more professional-looking effects

## Usage Tips

1. **For Classic Trail Effects**:
   - Set color_bleed to 0
   - Use moderate trail_strength (0.7-0.8)
   - Keep blur_amount low (0.2-0.3)

2. **For Psychedelic Effects**:
   - Increase color_bleed (0.5-0.8)
   - Use high trail_strength (0.9+)
   - Set moderate blur_amount (0.5-0.7)

3. **For Subtle, Professional Effects**:
   - Use low color_bleed (0.1-0.2)
   - Set higher threshold (0.2-0.3)
   - Use moderate blur_amount (0.4-0.6)

4. **For Dream-like Sequences**:
   - Set high blur_amount (1.0-1.5)
   - Use low decay_rate (0.05-0.1)
   - Set moderate color_bleed (0.3-0.4)

## Output

- Returns the processed image batch with enhanced motion trails applied
- Maintains the same dimensions and format as the input
- Each frame contains accumulated trails with color bleeding and blur effects

## Note

This version offers more creative possibilities than the original, particularly for artistic and experimental video effects. The color bleeding feature can create striking visual effects when combined with the right amount of blur and trail strength. As with V1, the first frame won't show trails as it needs at least two frames to detect motion. The exponential decay provides a more natural-looking fadeout compared to the linear decay in V1.

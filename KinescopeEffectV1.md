# KinescopeEffectV1

A ComfyUI node that simulates the distinctive visual characteristics of kinescope recordings and early television broadcasts. This effect recreates the nostalgic look of footage that was recorded by filming a TV or monitor screen, including various analog artifacts and imperfections.

## Description

The Kinescope Effect node applies multiple processing layers to create an authentic vintage television appearance, including film grain, phosphor persistence, scanlines, and edge bleeding effects. This can be particularly useful for:

- Creating retro-style animations
- Adding vintage television aesthetics to modern footage
- Simulating early broadcast television looks
- Creating nostalgic visual effects

## Parameters

### Basic Settings

- **black_and_white** (Boolean, default: True)
  - Converts the image to black and white, simulating early television broadcasts
  - When set to False, maintains original colors

- **contrast** (Float, default: 1.2)
  - Range: 0.1 to 3.0
  - Adjusts the contrast of the image
  - Higher values increase the difference between light and dark areas

- **brightness** (Float, default: 1.1)
  - Range: 0.1 to 3.0
  - Controls the overall brightness of the image
  - Values above 1.0 increase brightness, below 1.0 decrease it

### Analog Effects

- **film_grain** (Float, default: 35.0)
  - Range: 0.0 to 100.0
  - Adds random noise to simulate film grain
  - Higher values create more pronounced grain effect
  - Effect is multiplied by the number of generations

- **phosphor_persistence** (Float, default: 0.3)
  - Range: 0.0 to 1.0
  - Simulates the ghosting effect of phosphor displays
  - Higher values create more noticeable image persistence

- **scanline_intensity** (Float, default: 0.15)
  - Range: 0.0 to 1.0
  - Controls the visibility of horizontal scanlines
  - Higher values create more pronounced scanlines

- **edge_bleeding** (Float, default: 1.5)
  - Range: 0.0 to 5.0
  - Simulates color/light bleeding around edges
  - Higher values increase the bleeding effect radius

### Blur Settings

- **vertical_blur** (Integer, default: 1)
  - Range: 1 to 21 (odd numbers only)
  - Applies vertical blur to simulate vertical resolution loss
  - Higher values create more vertical smearing

- **horizontal_blur** (Integer, default: 1)
  - Range: 1 to 21 (odd numbers only)
  - Applies horizontal blur to simulate horizontal resolution loss
  - Higher values create more horizontal smearing

### Advanced Settings

- **generations** (Integer, default: 1)
  - Range: 1 to 5
  - Simulates multiple generations of recording
  - Each generation multiplies the film grain effect
  - Higher values create more degraded looking output

## Usage Tips

1. For authentic early television look:
   - Enable black_and_white
   - Use moderate phosphor_persistence (0.2-0.4)
   - Set scanline_intensity to 0.15-0.25

2. For color TV from the 1960s-70s:
   - Disable black_and_white
   - Increase edge_bleeding to 2.0-3.0
   - Use higher film_grain (40-60)

3. For degraded footage look:
   - Increase generations to 2 or 3
   - Increase film_grain
   - Add more blur in both directions

4. For subtle vintage effect:
   - Keep generations at 1
   - Use minimal scanline_intensity (0.1)
   - Keep phosphor_persistence low (0.1-0.2)

## Input/Output

- Input: Accepts a batch of images (IMAGE type)
- Output: Returns processed images with kinescope effect applied (IMAGE type)

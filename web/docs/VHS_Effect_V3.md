# VHS Effect v3

A ComfyUI custom node that simulates authentic VHS (Video Home System) tape effects and artifacts on images. This node provides extensive control over various VHS-style distortions and effects, allowing you to create realistic retro video aesthetics.

## Features

- Multiple VHS tape speed modes (SP, LP, EP)
- Horizontal noise line generation
- Shifting distortion bands
- Color bleeding/ghosting effects
- Adjustable sharpening
- Composite video artifacts simulation

## Parameters

### Base VHS Settings

- **tape_speed**: Selects the VHS tape recording speed mode
  - `SP` (Standard Play): Highest quality, least artifacts
  - `LP` (Long Play): Medium quality, moderate artifacts
  - `EP` (Extended Play): Lowest quality, most pronounced artifacts

- **composite_preemphasis**: Controls the emphasis of composite video signal simulation
  - Range: 0.0 to 8.0
  - Default: 4.0
  - Higher values increase the intensity of composite video artifacts

### Noise Line Effects

- **noise_line_intensity**: Controls the brightness of horizontal noise lines
  - Range: 0.0 to 1.0
  - Default: 0.8
  - Higher values create more visible noise lines

- **noise_line_thickness**: Sets the vertical thickness of noise lines
  - Range: 1 to 10 pixels
  - Default: 2
  - Higher values create thicker noise lines

- **noise_line_count**: Determines the number of noise lines per frame
  - Range: 0 to 5
  - Default: 1
  - Higher values add more noise lines to the image

### Distortion Effects

- **distortion_bands**: Sets the number of horizontal shifting distortion bands
  - Range: 0 to 10
  - Default: 3
  - Higher values create more bands of horizontal displacement

- **max_band_offset**: Controls the maximum pixel displacement of distortion bands
  - Range: 0 to 30 pixels
  - Default: 10
  - Higher values allow for more extreme horizontal shifts

### Color Effects

- **color_bleed_strength**: Controls the intensity of color bleeding/ghosting
  - Range: 0.0 to 1.0
  - Default: 0.3
  - Higher values create more pronounced color separation

- **color_bleed_offset**: Sets the pixel distance of color channel separation
  - Range: 1 to 5 pixels
  - Default: 2
  - Higher values increase the distance between color channels

### Enhancement

- **sharpen_amount**: Controls the final image sharpening
  - Range: 1.0 to 3.0
  - Default: 1.5
  - Values above 1.0 increase image sharpness

## Usage Tips

1. For authentic VHS artifacts:
   - Use `LP` or `EP` tape speeds for more pronounced effects
   - Keep color_bleed_strength between 0.2-0.4
   - Use 1-2 noise lines with moderate intensity

2. For subtle vintage effects:
   - Use `SP` tape speed
   - Keep color_bleed_strength low (0.1-0.2)
   - Use minimal noise lines and distortion bands

3. For extreme degradation:
   - Use `EP` tape speed
   - Increase noise_line_count and distortion_bands
   - Use higher color_bleed_strength and offset values

## Technical Details

The node processes images through multiple stages:
1. Applies tape speed-based blur
2. Generates random horizontal noise lines
3. Creates shifting distortion bands
4. Simulates color bleeding/ghosting
5. Applies final sharpening

All effects are applied while maintaining the original image dimensions and color space.

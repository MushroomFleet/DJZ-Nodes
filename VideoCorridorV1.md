# 🌀 Infinite Corridor Generator (VideoCorridorV1)

This node generates dynamic infinite corridor video sequences with perspective effects, creating immersive tunnel-like animations. It offers various customization options for colors, patterns, and lighting effects.

## Parameters

### Basic Settings

#### Width
- **Type:** Integer
- **Default:** 512
- **Range:** 128 to 4096
- **Step:** 64
- **Description:** The width of the output video in pixels.

#### Height
- **Type:** Integer
- **Default:** 512
- **Range:** 128 to 4096
- **Step:** 64
- **Description:** The height of the output video in pixels.

#### FPS
- **Type:** Integer
- **Default:** 30
- **Range:** 1 to 60
- **Step:** 1
- **Description:** Frames per second for the output video.

#### Max Frames
- **Type:** Integer
- **Default:** 300
- **Range:** 1 to 9999
- **Step:** 1
- **Description:** Total number of frames to generate.

### Corridor Properties

#### Corridor Depth
- **Type:** Float
- **Default:** 2.0
- **Range:** 0.5 to 5.0
- **Step:** 0.1
- **Description:** Controls how deep the corridor appears. Higher values create a longer-looking corridor.

#### Movement Speed
- **Type:** Float
- **Default:** 0.05
- **Range:** 0.01 to 0.2
- **Step:** 0.01
- **Description:** Controls how fast the camera appears to move through the corridor.

#### Perspective Strength
- **Type:** Float
- **Default:** 1.0
- **Range:** 0.5 to 2.0
- **Step:** 0.1
- **Description:** Controls the intensity of the perspective effect. Higher values create more dramatic perspective distortion.

### Visual Style Options

#### Color Scheme
- **Type:** Dropdown
- **Options:**
  - `neon`: Bright, vibrant neon colors
  - `classic`: Traditional RGB color progression
  - `rainbow`: Full spectrum of colors
  - `monochrome`: Grayscale variations
  - `sunset`: Warm orange and purple tones
  - `cyberpunk`: High-contrast futuristic colors

#### Wall Pattern
- **Type:** Dropdown
- **Options:**
  - `solid`: Simple solid color walls
  - `gradient`: Smooth gradient from wall color to white
  - `grid`: Grid pattern overlay on walls
  - `diagonal`: Diagonal line pattern overlay

#### Lighting Mode
- **Type:** Dropdown
- **Options:**
  - `dynamic`: Light intensity varies with depth
  - `static`: Consistent lighting throughout
  - `pulsing`: Rhythmic light intensity changes
  - `ambient`: Soft, diffused lighting effect

## Usage Tips

1. **For Smooth Animation:**
   - Keep the movement speed between 0.03 and 0.08
   - Use at least 30 FPS for fluid motion

2. **For Best Visual Impact:**
   - Combine complementary color schemes with appropriate lighting modes
   - Use the grid or diagonal patterns with dynamic lighting for added depth perception

3. **Performance Considerations:**
   - Higher resolutions and frame counts will increase generation time
   - Consider reducing max_frames for quick previews

## Color Scheme Details

- **Neon:** (255,0,255), (0,255,255), (255,255,0), etc.
- **Classic:** Standard RGB progression
- **Rainbow:** Full HSV color wheel conversion
- **Monochrome:** Grayscale values from 255 to 60
- **Sunset:** Warm oranges to cool purples
- **Cyberpunk:** High-contrast neon combinations

## Technical Notes

- The corridor is generated using perspective transformation
- Wall patterns are applied using OpenCV polygon filling and line drawing
- Lighting effects are calculated per-frame and can be influenced by depth
- The animation loops seamlessly when max_frames is set appropriately for the movement speed

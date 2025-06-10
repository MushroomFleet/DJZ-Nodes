# 🎲 Video Cube Generator (VideoCubeV1)

This node generates 3D rotating cube animations with customizable parameters, offering various rendering styles, color schemes, and lighting effects. It creates dynamic animations of a cube that can rotate around all three axes.

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
- **Default:** 120
- **Range:** 1 to 9999
- **Step:** 1
- **Description:** Total number of frames to generate.

### Cube Properties

#### Cube Size
- **Type:** Float
- **Default:** 1.0
- **Range:** 0.1 to 5.0
- **Step:** 0.1
- **Description:** Controls the size of the cube relative to the viewport.

#### Distance
- **Type:** Float
- **Default:** 5.0
- **Range:** 2.0 to 20.0
- **Step:** 0.5
- **Description:** Distance of the cube from the camera. Higher values make the cube appear smaller.

#### FOV (Field of View)
- **Type:** Float
- **Default:** 75.0
- **Range:** 30.0 to 120.0
- **Step:** 5.0
- **Description:** Camera field of view in degrees. Higher values create more perspective distortion.

### Rotation Settings

#### Rotation X
- **Type:** Float
- **Default:** 0.02
- **Range:** -0.1 to 0.1
- **Step:** 0.01
- **Description:** Speed of rotation around the X axis (pitch). Positive values rotate upward.

#### Rotation Y
- **Type:** Float
- **Default:** 0.03
- **Range:** -0.1 to 0.1
- **Step:** 0.01
- **Description:** Speed of rotation around the Y axis (yaw). Positive values rotate rightward.

#### Rotation Z
- **Type:** Float
- **Default:** 0.01
- **Range:** -0.1 to 0.1
- **Step:** 0.01
- **Description:** Speed of rotation around the Z axis (roll). Positive values rotate clockwise.

### Visual Style Options

#### Color Scheme
- **Type:** Dropdown
- **Options:**
  - `rainbow`: Full spectrum of colors with 80% saturation
  - `monochrome`: Grayscale variations from white to dark gray
  - `neon`: Bright, vibrant neon colors
  - `pastel`: Soft, light colors
  - `cyberpunk`: High-contrast futuristic colors

#### Render Style
- **Type:** Dropdown
- **Options:**
  - `wireframe`: Shows only the edges of the cube
  - `solid`: Renders filled faces with lighting
  - `points`: Displays vertices as colored points

#### Lighting Mode
- **Type:** Dropdown
- **Options:**
  - `basic`: Simple diffuse lighting
  - `ambient`: Soft lighting with ambient component
  - `dynamic`: Advanced lighting with specular highlights
  - `none`: No lighting effects applied

## Usage Tips

1. **For Smooth Rotation:**
   - Keep rotation values between -0.05 and 0.05
   - Use different values for each axis to create interesting patterns
   - Higher FPS values will create smoother animations

2. **For Best Visual Impact:**
   - Combine appropriate lighting modes with render styles
   - Use `solid` render style with `dynamic` lighting for realistic 3D appearance
   - `wireframe` style works well with `neon` or `cyberpunk` color schemes

3. **Performance Considerations:**
   - Higher resolutions and frame counts will increase generation time
   - Complex lighting calculations (dynamic mode) may impact performance
   - Consider using simpler render styles for quick previews

## Technical Details

- Uses perspective projection for 3D to 2D conversion
- Implements painter's algorithm for face rendering
- Supports diffuse and specular lighting calculations
- Automatically handles face culling and depth sorting
- Uses normalized light direction for consistent lighting across cube faces

## Color Scheme Details

- **Rainbow:** HSV-based colors with 80% saturation
- **Monochrome:** Grayscale values from 255 to 60
- **Neon:** Bright, saturated complementary colors
- **Pastel:** Soft, desaturated colors
- **Cyberpunk:** High-contrast neon combinations

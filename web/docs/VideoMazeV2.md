# 🌀 Video Maze Generator V2

An enhanced version of the Video Maze Generator that adds deterministic maze generation and additional control parameters.

## Key Improvements Over V1
- Deterministic maze generation using ComfyUI's standard seed parameter
- Customizable wall thickness
- Adjustable camera height for different perspectives
- Fog distance control for atmospheric effects
- Enhanced ceiling and floor color options
- Improved collision detection and movement

## Parameters

### Basic Settings
- `width`: Output width in pixels (128-4096, default: 512)
- `height`: Output height in pixels (128-4096, default: 512)
- `fps`: Frames per second (1-60, default: 30)
- `max_frames`: Maximum number of frames to generate (1-9999, default: 300)
- `seed`: Random seed for deterministic maze generation (0-18446744073709551615, default: 0)

### Maze Configuration
- `maze_size`: Size of the maze grid (15-100, default: 30)
- `wall_height`: Height of maze walls (0.5-3.0, default: 1.2)
- `wall_thickness`: Thickness of walls in pixels (1-5, default: 1)

### Camera Settings
- `camera_height`: Vertical camera position (0.1-1.0, default: 0.5)
- `camera_pitch`: Camera tilt angle in degrees (-45.0 to 45.0, default: 0.0)
- `fog_distance`: Distance at which fog effect starts (5.0-50.0, default: 20.0)
- `fov`: Field of view in degrees (30.0-120.0, default: 75.0)
- `movement_speed`: Camera movement speed (0.01-0.2, default: 0.05)
- `rotation_speed`: Camera rotation speed (0.01-0.15, default: 0.03)

### Visual Settings
- `color_scheme`: Color palette selection
  - `neon`: Bright, vibrant colors
  - `classic`: Traditional RGB-based colors
  - `rainbow`: Full spectrum colors
  - `monochrome`: Grayscale variations
  - `sunset`: Warm, atmospheric colors
  - `cyberpunk`: High-contrast futuristic colors

- `wall_pattern`: Wall texture pattern
  - `solid`: Simple solid walls
  - `gradient`: Vertical gradient effect
  - `brick`: Animated brick pattern
  - `circuit`: Moving circuit board pattern

- `lighting_mode`: Lighting effect type
  - `dynamic`: Distance-based lighting
  - `static`: Constant lighting
  - `pulsing`: Animated pulsing effect
  - `ambient`: Soft ambient lighting

- `render_quality`: Ray casting quality
  - `standard`: Basic quality (faster)
  - `high`: Improved quality
  - `ultra`: Maximum quality (slower)

- `ceiling_color`: Hex color code for ceiling (default: "#000000")
- `floor_color`: Hex color code for floor (default: "#000000")

## Output
- Returns a tensor of image frames in the standard ComfyUI format
- Compatible with video generation workflows
- Can be used with RepeatDecorator and LoopDecorator for endless animations

## Tips
- Use higher `render_quality` for final renders and lower for previews
- Adjust `fog_distance` to control the atmosphere and visibility
- Experiment with different `wall_pattern` and `lighting_mode` combinations
- Use consistent `seed` values to generate the same maze layout repeatedly
- Adjust `camera_height` and `camera_pitch` for different perspectives
- Use hex color codes (e.g., "#FF0000" for red) to customize ceiling and floor colors

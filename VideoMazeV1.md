# 🌀 Video Maze Generator (VideoMazeV1)

A ComfyUI custom node that generates infinite 3D maze video sequences with enhanced visuals and dynamic effects.

## Description

The Video Maze Generator creates animated sequences of a first-person perspective journey through a procedurally generated 3D maze. It features dynamic lighting, various wall patterns, and multiple color schemes to create engaging visual effects.

## Parameters

### Basic Settings
- **width**: Output frame width (128-4096 pixels, default: 512)
- **height**: Output frame height (128-4096 pixels, default: 512)
- **fps**: Frames per second (1-60 fps, default: 30)
- **max_frames**: Total number of frames to generate (1-9999, default: 300)

### Maze Configuration
- **maze_size**: Size of the maze grid (15-100, default: 30)
  - Larger values create more complex mazes
  - Affects performance and generation time
- **wall_height**: Height of maze walls (0.5-3.0, default: 1.2)
  - Controls the perceived height of walls relative to viewport
- **fov**: Field of view angle (30.0-120.0 degrees, default: 75.0)
  - Wider angles create more distortion at edges
  - Narrower angles create a more tunnel-like view

### Movement Settings
- **movement_speed**: Forward movement speed (0.01-0.2, default: 0.05)
  - Higher values create faster forward motion
- **rotation_speed**: Turning speed (0.01-0.15, default: 0.03)
  - Controls how quickly the view rotates

### Visual Options

#### Color Schemes
- **neon**: Bright, high-contrast neon colors
- **classic**: Traditional RGB color progression
- **rainbow**: Full spectrum color rotation
- **monochrome**: Grayscale gradient
- **sunset**: Warm orange to purple gradient
- **cyberpunk**: Vibrant tech-inspired colors

#### Wall Patterns
- **solid**: Simple solid colored walls
- **gradient**: Smooth gradient from base color to white
- **brick**: Repeating brick-like pattern
- **circuit**: Animated circuit-board style pattern

#### Lighting Modes
- **dynamic**: Distance-based lighting falloff
- **static**: Consistent lighting throughout
- **pulsing**: Rhythmic light intensity changes
- **ambient**: Soft, ambient lighting with subtle highlights

#### Render Quality
- **standard**: Basic rendering, best performance
- **high**: Improved anti-aliasing and detail
- **ultra**: Maximum quality with finest detail

## Technical Details

- Output Type: IMAGE (tensor of frames)
- Category: Video/Animation
- Compatible Decorators: RepeatDecorator, LoopDecorator

## Features

### Advanced Maze Generation
- Procedurally generated mazes with varying complexity
- Occasional wider passages for variety
- Smart collision detection with wall sliding

### Enhanced Visuals
- Dynamic lighting effects based on distance and mode
- Multiple wall pattern options with animation
- Ceiling and floor rendering
- Quality-based ray casting for different performance levels

## Usage

1. Add the node to your ComfyUI workflow
2. Configure the basic parameters (width, height, fps)
3. Adjust maze and movement settings to your preference
4. Select visual options (color scheme, wall pattern, lighting)
5. Choose render quality based on your performance needs
6. Connect the output to your workflow

The node outputs a tensor of image frames that can be further processed or saved as a video sequence.

## Performance Notes

- Higher maze_size values will increase generation time
- Ultra render quality may impact performance on larger resolutions
- Complex wall patterns and dynamic lighting may affect frame generation speed

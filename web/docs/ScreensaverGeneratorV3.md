# 🖥️ Screensaver Generator V3

An advanced ComfyUI node for generating animated screensaver-style effects with support for external presets and multiple color schemes. This node creates dynamic, customizable animations that can be used for various creative purposes.

## Overview

The ScreensaverGeneratorV3 is a flexible framework for creating animated screensaver effects. It supports:
- External preset loading from .scg files
- Multiple color schemes
- Customizable animation parameters
- Batch frame generation
- Dynamic parameter visibility based on selected preset

## Base Parameters

1. **preset** (COMBO)
   - List of available screensaver presets
   - Loaded dynamically from the ScreenGen directory
   - Controls which animation style will be generated

2. **width** (INT)
   - Width of the generated frames
   - Range: 64 to 4096
   - Default: 512
   - Step: 64

3. **height** (INT)
   - Height of the generated frames
   - Range: 64 to 4096
   - Default: 512
   - Step: 64

4. **fps** (INT)
   - Frames per second for the animation
   - Range: 1 to 60
   - Default: 30
   - Step: 1

5. **max_frames** (INT)
   - Total number of frames to generate
   - Range: 1 to 9999
   - Default: 60
   - Step: 1

6. **color_scheme** (COMBO)
   - Available options:
     - classic: Blue and cyan color palette
     - rainbow: Full spectrum color transitions
     - neon: Bright, vibrant colors
     - monochrome: Single color variations
   - Controls the color palette used in the animation

7. **speed** (FLOAT)
   - Animation speed multiplier
   - Range: 0.1 to 5.0
   - Default: 1.0
   - Step: 0.1

## Preset System

### How Presets Work
- Presets are loaded from .scg files in the ScreenGen directory
- Each preset defines its own set of parameters and rendering logic
- Preset parameters are dynamically added to the node's interface
- Parameters are prefixed with the preset name for clarity

### Creating Custom Presets
Presets must be defined in .scg files with:
1. A class ending in 'Screensaver'
2. Required attributes:
   - name: Preset identifier
   - parameters: Parameter definitions
   - render: Frame generation method

## Color Management

The node includes a sophisticated color palette system:

### Built-in Color Schemes
- **classic**: Traditional blue and cyan combination
- **rainbow**: Full spectrum color transitions
- **neon**: Bright, vibrant neon colors
- **monochrome**: Single color variations

### Color Palette Features
- Automatic palette generation
- Palette caching for performance
- Smooth color transitions
- RGB color space support

## Technical Details

### Output
- Returns: IMAGE tensor
- Format: Batch of frames (B, H, W, C)
- Value range: 0.0 to 1.0 (normalized)
- Channel order: RGB

### Error Handling
The node implements comprehensive error handling for:
- Preset loading failures
- Parameter validation
- Frame generation issues
- Color palette errors

### Performance Considerations
- Efficient frame batch generation
- Color palette caching
- State management for animations
- Memory-optimized frame handling

## Usage Tips

1. **Preset Selection**
   - Browse available presets in the dropdown
   - Parameters update automatically based on selection
   - Each preset offers unique animation styles

2. **Animation Tuning**
   - Adjust speed for faster/slower animations
   - Modify max_frames based on needed duration
   - FPS affects smoothness vs. generation time

3. **Color Customization**
   - Try different color schemes for varied effects
   - Color schemes affect the mood of animations
   - Some presets may work better with specific schemes

4. **Resolution Control**
   - Higher resolutions need more processing time
   - Match resolution to intended use case
   - Keep width/height reasonable for performance

## Integration Notes

- Compatible with video workflow nodes
- Supports animation decorators (RepeatDecorator, LoopDecorator)
- Can be used in batch processing pipelines
- Outputs standard tensor format for compatibility

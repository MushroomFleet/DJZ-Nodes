# Screensaver Generator V2

A ComfyUI custom node that generates retro-style screensaver animations with customizable parameters and external preset support.

## Description

The Screensaver Generator V2 is an enhanced version of the screensaver generator that allows for dynamic loading of external screensaver presets. It creates animated sequences that can be used as transitions, backgrounds, or creative effects in your image generation pipeline.

## Base Parameters

- **preset**: Select from available screensaver patterns loaded from the ScreenGen directory
- **width**: Output frame width (64-4096 pixels, default: 512)
- **height**: Output frame height (64-4096 pixels, default: 512)
- **fps**: Frames per second (1-60 fps, default: 30)
- **max_frames**: Total number of frames to generate (1-9999, default: 60)
- **color_scheme**: Visual style of the screensaver. Options:
  - `classic`: Blue and cyan color scheme
  - `rainbow`: Full spectrum color rotation
  - `neon`: High contrast neon colors
  - `monochrome`: Green-only gradient
- **speed**: Animation speed multiplier (0.1-5.0, default: 1.0)

## Preset System

The node dynamically loads screensaver presets from `.scg` files in the ScreenGen directory. Each preset can define its own additional parameters that will appear in the node interface when that preset is selected.

### Preset Parameters
When you select a specific preset, additional parameters unique to that preset will become visible in the node interface. These parameters are defined by the preset file and allow for customization of the specific screensaver pattern.

## Usage

1. Add the node to your ComfyUI workflow
2. Select a preset from the dropdown menu
3. Adjust the base parameters (width, height, fps, etc.)
4. Configure any preset-specific parameters that appear
5. Connect the output to your workflow

The node outputs a tensor of image frames that can be further processed or saved as a video sequence.

## Technical Details

- Output Type: IMAGE (tensor of frames)
- Category: Video
- Compatible Decorators: RepeatDecorator, LoopDecorator

## Installation

The node requires the ScreenGen directory to be present in the same folder as the node file. Ensure all preset `.scg` files are placed in the ScreenGen directory for proper loading.

## Error Handling

- If the ScreenGen directory is not found, a warning message will be displayed
- Invalid preset files will be skipped with an error message
- The node validates all inputs before processing to ensure parameter compatibility

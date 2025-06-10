# VideoTimecode Node

A ComfyUI custom node that adds professional timecode overlays to image sequences. This node is particularly useful for video post-processing workflows where frame timing information needs to be visible.

## Features

- Adds frame-accurate timecode overlay to image sequences
- Customizable font selection with TTF support
- Adjustable positioning and styling
- Support for forward and reverse counting
- Configurable background opacity for better readability
- Multiple color presets for timecode display

## Parameters

### Required Parameters

- **images**: Input batch of images to process (IMAGE type)
- **fps**: Frame rate of the sequence
  - Default: 30.0
  - Range: 1.0 to 120.0
  - Step: 0.1
- **start_time**: Initial timecode in format "HH:MM:SS:FF"
  - Default: "00:00:00:00"
  - Format: Hours:Minutes:Seconds:Frames
- **font**: Font selection for timecode display
  - Options: "default" or any .TTF file in the TTF directory
  - Automatically detects and lists available TTF fonts
- **font_size**: Size of the timecode text
  - Default: 32
  - Range: 8 to 256 pixels
- **position**: Vertical placement of the timecode
  - Options: "top" or "bottom"
  - Default: "bottom"
- **text_color**: Color of the timecode text
  - Options: white, black, red, green, blue, yellow
  - Default: white
- **background_opacity**: Opacity of the background box behind the timecode
  - Default: 0.5
  - Range: 0.0 (fully transparent) to 1.0 (fully opaque)
  - Step: 0.1
- **reverse_count**: Direction of timecode counting
  - Default: false
  - When true, counts backward from start_time
  - When false, counts forward from start_time

## Usage

1. Connect your image sequence to the "images" input
2. Set your desired frame rate (fps)
3. Configure the start timecode in "HH:MM:SS:FF" format
4. Adjust visual parameters (font, size, position, colors) as needed
5. Enable reverse_count if you need a countdown timer effect

## Technical Details

- The node automatically handles batch processing of image sequences
- Timecode is frame-accurate and synchronized with the specified fps
- Supports high-resolution images with proper scaling
- Includes fallback font handling for robustness
- Background box ensures timecode readability over any image content
- Uses efficient image processing with PIL and numpy for optimal performance

## Font Support

The node supports custom TTF fonts placed in the `/TTF/` directory. If no custom font is specified or available, it will attempt to use the following fallback fonts in order:
1. System default font
2. Arial
3. DejaVuSans
4. System-specific fonts (Windows/Mac)
5. Built-in default font as last resort

## Output

Returns a processed IMAGE with the same dimensions as the input, with the timecode overlay added according to the specified parameters.

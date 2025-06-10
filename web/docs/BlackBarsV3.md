# Black Bars V3

A ComfyUI custom node that applies industry-standard letterboxing/pillarboxing with intelligent aspect ratio detection and padding options. This node is designed to help you achieve professional-grade video and image formatting by adding black bars (letterboxing/pillarboxing) while preserving your entire image.

## Key Features

- Preserves the entire image by using padding instead of cropping
- Automatic aspect ratio detection
- Support for standard industry aspect ratios
- Optional safe area guides
- Professional-grade padding calculations

## Parameters

### 1. Images (required)
- Input images to be processed
- Accepts standard ComfyUI image tensor format

### 2. Target Ratio (required)
Available options:
- `auto`: Automatically detects and matches the closest standard aspect ratio
- `2.39:1 (Anamorphic)`: Standard anamorphic widescreen format
- `2.35:1 (CinemaScope)`: Classic CinemaScope format
- `1.85:1 (Theatrical)`: Common theatrical release format
- `16:9 (HD)`: Standard HD video format
- `4:3 (Classic)`: Traditional TV/monitor format
- `1:1 (Square)`: Square format for social media
- `9:16 (Vertical)`: Vertical video format (e.g., mobile/stories)

### 3. Safe Area (boolean)
- Default: False
- When enabled, displays industry-standard safe area guides:
  - 90% Action Safe Area
  - 80% Title Safe Area
- Useful for ensuring critical content remains visible across different displays

### 4. Show Guides (boolean)
- Default: False
- When enabled, shows the same guides as Safe Area
- Can be used for composition and content placement

## Technical Details

### Supported Common Resolutions
The node automatically recognizes these standard resolutions:
- 1920x1080 (16:9)
- 3840x2160 (16:9)
- 1280x720 (16:9)
- 720x480 (4:3)
- 720x576 (4:3)
- 1080x1920 (9:16)
- 1080x1080 (1:1)

### Aspect Ratio Precision
The node supports these precise aspect ratios:
- 2.39:1 (Anamorphic)
- 2.35:1 (CinemaScope)
- 1.85:1 (Theatrical)
- 16:9 (≈1.78:1)
- 3:2 (1.5:1)
- 4:3 (≈1.33:1)
- 1:1
- 9:16 (0.5625:1)

## Usage Tips

1. **Automatic Mode**
   - Start with `auto` target ratio to let the node detect the closest standard aspect ratio
   - Useful when working with content from various sources

2. **Safe Areas**
   - Enable `safe_area` when creating content for broadcast or professional video
   - Ensures text and important elements remain visible across different displays

3. **Composition**
   - Use `show_guides` during composition to ensure proper content placement
   - Helps maintain professional standards for content positioning

4. **Preservation**
   - Unlike previous versions, V3 always preserves your entire image
   - Adds black bars (padding) instead of cropping

## Technical Implementation

- Uses PyTorch for efficient tensor operations
- Implements precise padding calculations to maintain aspect ratio accuracy
- Supports batch processing for multiple images
- GPU-accelerated when CUDA is available

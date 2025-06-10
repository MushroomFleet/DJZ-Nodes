# Black Bars V2

A ComfyUI custom node that provides industry-standard letterboxing and pillarboxing capabilities with automatic aspect ratio detection and professional safe area guides.

## Description

BlackBarsV2 allows you to convert images to standard aspect ratios using either black bars (letterbox/pillarbox) or center cropping. It supports common cinematic and broadcast aspect ratios with optional safe area guides for professional content creation.

## Parameters

### Mode
- **letterbox**: Adds black bars to the top and bottom to achieve the target aspect ratio
- **pillarbox**: Adds black bars to the sides to achieve the target aspect ratio
- **center_crop**: Crops the image from the center to achieve the target ratio without adding black bars

### Target Ratio
- **auto**: Automatically detects and matches the closest standard aspect ratio
- **2.39:1 (Anamorphic)**: Ultra-widescreen format commonly used in modern films
- **2.35:1 (CinemaScope)**: Classic widescreen cinematic format
- **1.85:1 (Theatrical)**: Standard theatrical widescreen format
- **16:9 (HD)**: Standard HD video format
- **4:3 (Classic)**: Traditional TV and early film format
- **1:1 (Square)**: Square format for social media
- **9:16 (Vertical)**: Vertical video format for mobile devices

### Safe Area Options

#### Safe Area (Boolean)
When enabled, displays industry-standard safe area guides:
- 90% Action Safe Area: Ensures important action stays within viewable areas across different displays
- 80% Title Safe Area: Ensures text and graphics remain readable across all display types

#### Show Guides (Boolean)
When enabled, displays visual guides showing:
- Crop boundaries
- Safe area markers
- Aspect ratio alignment guides

## Common Use Cases

1. **Film Production**
   - Converting footage to cinema-standard 2.39:1 or 2.35:1
   - Adding professional safe area guides for post-production

2. **Broadcast Content**
   - Converting between 16:9 and 4:3 formats
   - Ensuring content meets broadcast safe area requirements

3. **Social Media**
   - Converting horizontal content to vertical (9:16) for Stories/Reels
   - Creating square (1:1) format for profile posts

4. **Multi-Platform Content**
   - Using auto-detection to standardize mixed aspect ratio content
   - Batch processing with consistent safe areas across all outputs

## Technical Details

The node supports common standard resolutions including:
- 1920x1080 (FHD)
- 3840x2160 (4K UHD)
- 1280x720 (HD)
- 720x480 (SD)
- 720x576 (PAL)
- 1080x1920 (Vertical FHD)
- 1080x1080 (Square HD)

For non-standard input resolutions, the node automatically calculates and matches to the closest standard aspect ratio when in auto mode.

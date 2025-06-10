# Non-Square Pixels v1

A ComfyUI node that simulates non-square pixels, replicating the appearance of classic video formats like PAL and NTSC. This effect is particularly useful for creating authentic retro video looks or matching modern footage with historical aspect ratios.

## Overview

In the early days of television and video, pixels weren't always perfectly square. Different broadcast standards (PAL and NTSC) used slightly rectangular pixels to accommodate technical limitations. This node allows you to simulate these historical formats or create custom non-square pixel effects.

## Parameters

### Images
- **Type:** IMAGE
- **Description:** The input image or batch of images to process.

### Preset
- **Type:** Dropdown
- **Options:**
  - `CUSTOM`: Use a custom pixel aspect ratio
  - `PAL (4:3)`: Standard PAL format (1.0667:1 pixel aspect ratio)
  - `PAL WIDESCREEN (16:9)`: Widescreen PAL format (~1.4223:1 pixel aspect ratio)
  - `NTSC (4:3)`: Standard NTSC format (0.9091:1 pixel aspect ratio)
  - `NTSC WIDESCREEN (16:9)`: Widescreen NTSC format (~1.2121:1 pixel aspect ratio)
- **Default:** CUSTOM

### Custom Pixel Aspect Ratio
- **Type:** Float
- **Range:** 0.5 to 2.0
- **Step:** 0.0001
- **Default:** 1.0667 (PAL 4:3)
- **Description:** When "CUSTOM" preset is selected, this value determines the pixel aspect ratio. Values greater than 1 make pixels wider, values less than 1 make pixels taller.

### Preserve Original Size
- **Type:** Dropdown
- **Options:**
  - `enable`: Output image will maintain the same dimensions as input
  - `disable`: Output image dimensions will change based on the pixel aspect ratio
- **Default:** enable
- **Description:** Determines whether the output image should maintain its original dimensions or be stretched according to the pixel aspect ratio.

## Common Use Cases

1. **Vintage Television Look**
   - Use `PAL (4:3)` or `NTSC (4:3)` presets to simulate classic TV footage
   - Enable size preservation to maintain image dimensions

2. **Historical Video Matching**
   - Choose the preset matching your target format (PAL/NTSC)
   - Disable size preservation if you need accurate aspect ratio output

3. **Widescreen Retro Effect**
   - Use `PAL WIDESCREEN (16:9)` or `NTSC WIDESCREEN (16:9)` for modern aspect ratio with retro feel
   - Particularly effective for creating vintage-style cinematic looks

4. **Custom Stylization**
   - Select `CUSTOM` preset
   - Experiment with different pixel aspect ratios for creative effects
   - Values > 1 create horizontally stretched pixels
   - Values < 1 create vertically stretched pixels

## Technical Details

The node uses bilinear interpolation for resizing operations to maintain smooth transitions between pixels. The transformation process involves:

1. Converting the input image to the target pixel aspect ratio
2. Optionally rescaling back to original dimensions if preservation is enabled
3. Maintaining proper color and brightness values throughout the process

## Notes

- When preservation is disabled, the output image width will change based on the pixel aspect ratio
- The effect is resolution-independent and works with any input image size
- For authentic retro looks, consider combining with other effects like scanlines or color bleeding

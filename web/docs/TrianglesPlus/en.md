# TrianglesPlus Node

## Overview
The TrianglesPlus node is a custom ComfyUI node that generates abstract art using triangular shapes. It creates unique, geometric compositions by placing multiple colored triangles in different regions of the canvas.

## Parameters

### Required Parameters
- **width** (INT)
  - Default: 1024
  - Minimum: 64
  - Maximum: 4096
  - Description: The width of the generated image in pixels.

- **height** (INT)
  - Default: 1024
  - Minimum: 64
  - Maximum: 4096
  - Description: The height of the generated image in pixels.

- **seed** (INT)
  - Default: 0
  - Minimum: 0
  - Maximum: 4294967295
  - Description: Random seed for reproducible generation. Using the same seed will produce identical results.

## Output
- Returns an IMAGE type that can be used with other ComfyUI nodes
- The output is a tensor in the format (B,H,W,C) where:
  - B: Batch size (always 1)
  - H: Height of the image
  - W: Width of the image
  - C: Color channels (RGB)

## How It Works
1. The node creates a blank canvas with the specified dimensions
2. It generates 7 different triangles, each with:
   - Random positions based on specific regions of the canvas
   - Unique random colors
3. The triangles are strategically placed to create an abstract composition:
   - Two triangles in the top region
   - Two triangles in the bottom region
   - One triangle in the middle region
   - Two triangles on the sides
4. The final image is converted to the appropriate format for ComfyUI

## Usage Tips
- Experiment with different seeds to generate various compositions
- Adjust width and height to create different aspect ratios
- The node works well as a starting point for further image processing or as a background generator

# Dinsky Plus V2 Generator Node

The Dinsky Plus V2 Generator is a node that creates Kandinsky-style abstract art by generating shapes based on coordinate pairs. It offers various customization options including different color palettes, shape types, and weighting systems to create unique abstract compositions.

## Parameters

### Required Inputs

1. **width** (INT)
   - Width of the output image
   - Default: 1024
   - Range: 64 to 4096 pixels

2. **height** (INT)
   - Height of the output image
   - Default: 1024
   - Range: 64 to 4096 pixels

3. **seed** (INT)
   - Random seed for reproducible generation
   - Default: 0
   - Range: 0 to 2^32 - 1

4. **x_coords** (STRING)
   - Comma-separated list of X coordinates
   - Default: "100,200,300,400,500"
   - Example: "100,200,300" creates points at x=100, x=200, and x=300

5. **y_coords** (STRING)
   - Comma-separated list of Y coordinates
   - Default: "100,200,300,400,500"
   - Example: "100,200,300" creates points at y=100, y=200, and y=300

6. **shape_radius** (INT)
   - Radius of shapes (particularly circles)
   - Default: 50
   - Range: 1 to 500 pixels

7. **line_width** (INT)
   - Width of lines when drawing line shapes
   - Default: 5
   - Range: 1 to 50 pixels

8. **color_palette** (COMBO)
   - Choice of predefined color schemes
   - Options:
     - "kandinsky": Blues, oranges, and yellows (#69D2E7, #A7DBD8, #E0E4CC, #F38630, #FA6900, #FF4E50, #F9D423)
     - "warm": Red to yellow spectrum (#FF4E50, #FC913A, #F9D423, #EDE574, #E1F5C4)
     - "cool": Blues and greens (#69D2E7, #A7DBD8, #E0E4CC, #B2C2C1, #8AB8B2)
     - "monochrome": Grayscale (#FFFFFF, #D9D9D9, #BFBFBF, #8C8C8C, #404040)
     - "vibrant": Full spectrum (#FF1E1E, #FF9900, #FFFF00, #00FF00, #0000FF, #9900FF)

9. **circle_weight** (FLOAT)
   - Probability weight for generating circles
   - Default: 1.0
   - Range: 0.0 to 10.0
   - Step: 0.1

10. **rectangle_weight** (FLOAT)
    - Probability weight for generating rectangles
    - Default: 1.0
    - Range: 0.0 to 10.0
    - Step: 0.1

11. **line_weight** (FLOAT)
    - Probability weight for generating lines
    - Default: 1.0
    - Range: 0.0 to 10.0
    - Step: 0.1

## Shape Generation System

The node uses a weighted probability system to determine which shapes to draw:

1. **Circles**: Drawn centered on coordinate points with the specified radius
2. **Rectangles**: Drawn between consecutive coordinate pairs
3. **Lines**: Drawn connecting consecutive coordinate pairs

The weights determine the relative probability of each shape type being chosen. For example:
- Equal weights (1.0, 1.0, 1.0): Each shape has a 33.33% chance
- Weights (2.0, 1.0, 1.0): Circles have 50% chance, rectangles and lines 25% each
- Setting any weight to 0 removes that shape from consideration

## Coordinate System

- Coordinates are provided as comma-separated strings
- If parsing fails or insufficient coordinates are provided, default coordinates are used
- The system automatically pairs X and Y coordinates
- Minimum of 2 coordinate pairs are required (defaults are added if fewer are provided)
- Coordinates exceeding canvas dimensions are automatically clamped to valid ranges

## Output

- Returns a single IMAGE tensor
- Format: BCHW (Batch, Channel, Height, Width)
- RGB color space
- Pixel values normalized to 0-1 range
- White background

## Important Notes

1. The node is categorized under "DJZ-Nodes" in the ComfyUI interface
2. Shape generation is deterministic for a given seed value
3. The canvas starts with a white background
4. Shapes are drawn in the order of the provided coordinates
5. Each shape uses a randomly selected color from the chosen palette

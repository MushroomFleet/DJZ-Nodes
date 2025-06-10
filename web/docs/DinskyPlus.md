# Dinsky Plus Generator Node

## Overview
The Dinsky Plus Generator creates Kandinsky-style abstract art by randomly placing geometric shapes on a canvas. It generates unique compositions using circles, rectangles, and lines with customizable colors and dimensions.

## Input Parameters

### width
- **Type**: Integer
- **Default**: 1024
- **Range**: 64 to 4096
- **Description**: The width of the generated image in pixels
- **Usage**: Controls the horizontal size of the canvas

### height
- **Type**: Integer
- **Default**: 1024
- **Range**: 64 to 4096
- **Description**: The height of the generated image in pixels
- **Usage**: Controls the vertical size of the canvas

### seed
- **Type**: Integer
- **Default**: 0
- **Range**: 0 to 4294967295
- **Description**: Random seed for reproducible generation
- **Usage**: Using the same seed will generate the same composition

### num_shapes
- **Type**: Integer
- **Default**: 100
- **Range**: 1 to 1000
- **Description**: Number of shapes to generate
- **Usage**: Higher values create denser compositions

### min_size
- **Type**: Integer
- **Default**: 10
- **Range**: 1 to 500
- **Description**: Minimum size for shapes in pixels
- **Usage**: Affects the smallest possible:
  - Circle radius
  - Rectangle width/height
  - Line length

### max_size
- **Type**: Integer
- **Default**: 100
- **Range**: 1 to 1000
- **Description**: Maximum size for shapes in pixels
- **Usage**: Affects the largest possible:
  - Circle radius
  - Rectangle width/height
  - Line length

### color_palette
- **Type**: Dropdown selection
- **Options**:
  - `kandinsky`: Blues, greens, oranges, and yellows
  - `warm`: Reds, oranges, and yellows
  - `cool`: Blues, greens, and grays
  - `monochrome`: Grayscale from white to dark gray
  - `vibrant`: Bright primary and secondary colors
- **Description**: Color scheme for the generated shapes
- **Usage**: Select different palettes to achieve various artistic styles

### circle_weight
- **Type**: Float
- **Default**: 1.0
- **Range**: 0.0 to 10.0
- **Step**: 0.1
- **Description**: Relative probability of generating circles
- **Usage**: Higher values increase the proportion of circles in the composition

### rectangle_weight
- **Type**: Float
- **Default**: 1.0
- **Range**: 0.0 to 10.0
- **Step**: 0.1
- **Description**: Relative probability of generating rectangles
- **Usage**: Higher values increase the proportion of rectangles in the composition

### line_weight
- **Type**: Float
- **Default**: 1.0
- **Range**: 0.0 to 10.0
- **Step**: 0.1
- **Description**: Relative probability of generating lines
- **Usage**: Higher values increase the proportion of lines in the composition

## Output

### IMAGE
- **Type**: Tensor (B,H,W,C format)
- **Description**: Generated abstract art composition
- **Usage**: Can be connected to any node that accepts image input

## Example Usage
1. Add the Dinsky Plus Generator node to your workflow
2. Set desired canvas dimensions (width and height)
3. Adjust shape generation parameters:
   - Use num_shapes to control composition density
   - Set min_size and max_size for shape variety
   - Adjust shape weights to favor certain geometric elements
4. Choose a color palette that matches your desired style
5. Use different seeds to generate variations
6. Connect the output to an image preview or processing node

## Notes
- Shape weights are relative to each other and automatically normalized
- Line width scales with min_size parameter
- Shapes are randomly positioned within canvas bounds
- All shapes are filled with no outlines
- The output is always in RGB format

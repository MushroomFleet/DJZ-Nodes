# Fractal Art Generator Node

The Fractal Art Generator is a powerful node that creates various types of fractal art, including the classic Mandelbrot set, Julia sets, Burning Ship fractal, Tricorn, and Newton fractals. It offers extensive customization options for creating unique mathematical art pieces.

## Parameters

### Required Parameters

- **width**: The width of the output image in pixels.
  - Default: 1024
  - Minimum: 64
  - Maximum: 4096

- **height**: The height of the output image in pixels.
  - Default: 1024
  - Minimum: 64
  - Maximum: 4096

- **max_iterations**: The maximum number of iterations for calculating each pixel.
  - Default: 500
  - Minimum: 50
  - Maximum: 2000
  - Higher values provide more detail but increase generation time

- **preset**: The type of fractal to generate. Options:
  - `Custom`: Use custom coordinates and zoom level
  - `Classic Mandelbrot`: The standard Mandelbrot set
  - `Julia Set`: A classic Julia set with parameter c = -0.4 + 0.6i
  - `Burning Ship`: The Burning Ship fractal
  - `Tricorn`: The Tricorn fractal (also known as the Mandelbar set)
  - `Newton`: Newton fractal based on cube roots of unity

- **zoom_level**: Controls how far in or out the view is zoomed.
  - Default: 1.0
  - Minimum: 0.1
  - Maximum: 100.0
  - Step: 0.1

### Optional Parameters

- **x_center**: The x-coordinate of the center point to view.
  - Default: -0.75
  - Range: -2.0 to 2.0
  - Step: 0.0001

- **y_center**: The y-coordinate of the center point to view.
  - Default: 0.0
  - Range: -2.0 to 2.0
  - Step: 0.0001

## Fractal Types Explained

### Classic Mandelbrot
- The standard Mandelbrot set, showing the characteristic cardioid and period bulbs
- Default view centered at (-0.5, 0.0) with zoom 0.8

### Julia Set
- A classic Julia set with fixed parameter c = -0.4 + 0.6i
- Creates intricate, symmetrical patterns
- Default view centered at (0.0, 0.0) with zoom 0.8

### Burning Ship
- A variation where the real and imaginary parts are made positive before squaring
- Creates a distinctive "burning ship" shape
- Default view centered at (-0.4, -0.6) with zoom 0.6

### Tricorn
- Also known as the Mandelbar set
- Uses complex conjugate in the iteration
- Default view centered at (0.0, 0.0) with zoom 0.8

### Newton
- Based on Newton's method for finding cube roots of unity
- Creates distinctive basins of attraction
- Default view centered at (0.0, 0.0) with zoom 0.7

## Output

- Returns a single IMAGE output
- The image is rendered in grayscale:
  - Black represents points inside the set
  - White represents points that escape quickly
  - Grayscale values represent intermediate escape times

## Use Cases

- Creating mathematical art
- Exploring fractal mathematics visually
- Generating unique abstract backgrounds
- Educational visualization of complex dynamics
- Creating high-resolution fractal wallpapers

## Tips for Best Results

1. **Resolution**: Higher width/height values create more detailed images but take longer to generate
2. **Iterations**: Increase max_iterations when zooming in to maintain detail
3. **Exploration**: Use Custom preset with x_center and y_center to explore specific areas
4. **Detail Level**: Higher zoom_level values require higher max_iterations for good detail
5. **Performance**: Start with lower resolution and iterations for quick previews, then increase for final renders

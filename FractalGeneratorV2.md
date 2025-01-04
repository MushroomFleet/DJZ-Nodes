# FractalGeneratorV2 (Fractal Art Generator V2)

An advanced ComfyUI node for generating high-quality fractal art. This node supports multiple fractal types, color schemes, and offers extensive customization options for creating unique fractal imagery.

## Parameters

### Basic Settings

#### width
- Type: INT
- Default: 1024
- Range: 64 to 4096
- Description: The width of the output image in pixels.

#### height
- Type: INT
- Default: 1024
- Range: 64 to 4096
- Description: The height of the output image in pixels.

#### max_iterations
- Type: INT
- Default: 500
- Range: 50 to 2000
- Description: Maximum number of iterations for calculating fractal values. Higher values provide more detail but increase computation time.

### Fractal Configuration

#### preset
- Type: Dropdown
- Options: ["Custom", "Classic Mandelbrot", "Julia Set", "Burning Ship", "Tricorn", "Newton"]
- Default: "Classic Mandelbrot"
- Description: Predefined fractal types with optimized parameters:
  - `Custom`: Use custom coordinates and parameters
  - `Classic Mandelbrot`: Traditional Mandelbrot set
  - `Julia Set`: Julia set with interesting variations
  - `Burning Ship`: Modified Mandelbrot with absolute values
  - `Tricorn`: Also known as the Mandelbar set
  - `Newton`: Newton fractal based on complex roots

#### zoom_level
- Type: FLOAT
- Default: 1.0
- Range: 0.1 to 100.0
- Step: 0.1
- Description: Controls the magnification level of the fractal. Higher values zoom in closer.

### Color Settings

#### color_preset
- Type: Dropdown
- Options: ["Classic White-Grey", "Electric Blue", "Fire", "Rainbow", "Deep Space", "Ocean", "Forest", "Psychedelic"]
- Default: "Classic White-Grey"
- Description: Predefined color schemes:
  - `Classic White-Grey`: Traditional monochrome coloring
  - `Electric Blue`: Bright electric blue with white highlights
  - `Fire`: Warm gradient from deep red through orange to yellow
  - `Rainbow`: Full spectrum with high saturation
  - `Deep Space`: Space theme with stars and nebula colors
  - `Ocean`: Ocean colors from deep blue to white foam
  - `Forest`: Natural greens and browns
  - `Psychedelic`: Ultra-vibrant cycling colors

#### color_cycles
- Type: FLOAT
- Default: 1.0
- Range: 0.1 to 10.0
- Step: 0.1
- Description: Controls how many times the color pattern repeats. Higher values create more color bands.

### Advanced Parameters

#### power
- Type: FLOAT
- Default: 2.0
- Range: 2.0 to 5.0
- Step: 0.1
- Description: Exponent used in fractal calculations. Higher values create more complex patterns.

#### escape_radius
- Type: FLOAT
- Default: 2.0
- Range: 1.0 to 10.0
- Step: 0.1
- Description: Threshold for determining if a point escapes the set. Affects detail and coloring.

#### smooth_coloring
- Type: BOOLEAN
- Default: true
- Description: Enables smooth color transitions between iteration bands when true.

### Optional Parameters

#### x_center
- Type: FLOAT
- Default: -0.75
- Range: -2.0 to 2.0
- Step: 0.0001
- Description: X-coordinate for the center of the view. Used in Custom preset mode.

#### y_center
- Type: FLOAT
- Default: 0.0
- Range: -2.0 to 2.0
- Step: 0.0001
- Description: Y-coordinate for the center of the view. Used in Custom preset mode.

## Usage Tips

1. **Choosing a Preset**:
   - Start with "Classic Mandelbrot" to explore the basic fractal
   - Try "Julia Set" for more varied and symmetric patterns
   - "Burning Ship" and "Tricorn" offer unique variations
   - "Newton" creates distinct boundary patterns

2. **Color Customization**:
   - Use "Classic White-Grey" for traditional visualization
   - "Deep Space" and "Ocean" work well for artistic renders
   - "Psychedelic" and "Rainbow" create vibrant, dynamic images
   - Adjust color_cycles to control pattern density

3. **Detail Control**:
   - Increase max_iterations for more detailed boundaries
   - Use smooth_coloring for better gradient transitions
   - Adjust escape_radius to modify boundary thickness
   - Higher power values create more intricate patterns

4. **Exploration**:
   - Use zoom_level to focus on interesting areas
   - In Custom mode, adjust x_center and y_center to navigate
   - Combine different presets with color schemes for unique results

## Output

Returns a single IMAGE tensor in BCHW format, suitable for further processing in ComfyUI workflows.

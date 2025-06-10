# FractalGeneratorV3 (Fractal Gen Cuda)

A CUDA-accelerated ComfyUI node for generating high-quality fractal art. This version leverages GPU acceleration for faster processing while maintaining all the features of the standard fractal generator.

## Performance Note

This node automatically utilizes CUDA acceleration when a compatible NVIDIA GPU is available, falling back to CPU processing if CUDA is not available. The CUDA implementation can provide significant performance improvements, especially for:
- High-resolution outputs (2048x2048 and above)
- High iteration counts (1000+)
- Complex fractal types (Newton, high-power calculations)

## Parameters

### Basic Settings

#### width
- Type: INT
- Default: 1024
- Range: 64 to 4096
- Description: The width of the output image in pixels. Higher resolutions benefit more from CUDA acceleration.

#### height
- Type: INT
- Default: 1024
- Range: 64 to 4096
- Description: The height of the output image in pixels. Higher resolutions benefit more from CUDA acceleration.

#### max_iterations
- Type: INT
- Default: 500
- Range: 50 to 2000
- Description: Maximum number of iterations for calculating fractal values. CUDA acceleration allows for higher iteration counts with less performance impact.

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

1. **CUDA Optimization**:
   - For best performance, use higher resolution outputs and iteration counts
   - Complex fractals like Newton and high-power calculations benefit most from GPU acceleration
   - The node automatically handles GPU memory management

2. **High-Resolution Rendering**:
   - Take advantage of CUDA acceleration to generate larger images
   - Consider using higher iteration counts for more detail
   - Smooth coloring has minimal performance impact with CUDA

3. **Preset Selection**:
   - All presets are optimized for GPU computation
   - Newton fractals particularly benefit from CUDA acceleration
   - Custom mode allows for exploration without performance penalty

4. **Color and Detail**:
   - All color presets are computed efficiently on GPU
   - Smooth coloring is optimized for CUDA processing
   - Higher power values and escape radius calculations are accelerated

## Output

Returns a single IMAGE tensor in BCHW format, suitable for further processing in ComfyUI workflows. The output maintains full precision regardless of computation method (GPU or CPU).

## System Requirements

- NVIDIA GPU with CUDA support for GPU acceleration
- Automatically falls back to CPU processing if CUDA is unavailable
- Compatible with all CUDA-capable GPUs

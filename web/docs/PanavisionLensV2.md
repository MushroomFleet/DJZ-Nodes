# Panavision Lens Effect v2

An enhanced ComfyUI custom node that provides sophisticated simulation of Panavision anamorphic lens characteristics, including advanced bokeh modeling, multi-layer flares, chromatic effects, and film-like color science.

## Features

- Advanced anamorphic lens simulation
- Sophisticated bokeh system with rotation and elongation controls
- Multi-layer lens flare system with position control
- Professional color science with highlight retention and shadow rolloff
- Zone-based color temperature adjustments
- Chromatic aberration and barrel distortion effects
- Real-time processing with GPU acceleration

## Parameters

### Lens Format

- **aspect_ratio** (1.85 - 2.76, default: 2.39)
  - Controls the final aspect ratio of the output image
  - Common values: 2.39:1 (standard anamorphic), 1.85:1 (wide-screen)

- **anamorphic_squeeze** (1.0 - 2.4, default: 2.0)
  - Controls the horizontal compression factor
  - Higher values create more pronounced anamorphic characteristics
  - 2.0 represents classic anamorphic squeeze ratio

### Bokeh Characteristics

- **bokeh_intensity** (0.0 - 1.0, default: 0.5)
  - Controls the strength of the bokeh effect
  - Higher values create more pronounced background blur

- **bokeh_threshold** (0.5 - 1.0, default: 0.8)
  - Sets the brightness threshold for bokeh effect activation
  - Higher values limit the effect to brighter areas

- **bokeh_elongation** (1.0 - 3.0, default: 2.0)
  - Controls the horizontal stretching of bokeh shapes
  - Higher values create more oval-shaped bokeh

- **bokeh_rotation** (-45.0 - 45.0, default: 0.0)
  - Adjusts the rotation angle of bokeh shapes
  - Useful for creating diagonal bokeh effects

### Lens Flare System

- **primary_flare_intensity** (0.0 - 1.0, default: 0.4)
  - Controls the strength of the main lens flare
  - Creates warm-toned central flare elements

- **secondary_flare_intensity** (0.0 - 1.0, default: 0.2)
  - Controls the strength of additional flare elements
  - Creates cooler-toned complementary flares

- **flare_position_y** (-1.0 - 1.0, default: 0.0)
  - Adjusts the vertical position of the flare system
  - Negative values move flares up, positive values move them down

- **flare_stretch** (0.5 - 2.0, default: 1.0)
  - Controls the horizontal spread of flare elements
  - Higher values create more elongated flare patterns

### Color Science

- **highlight_retention** (0.0 - 1.0, default: 0.8)
  - Controls highlight roll-off characteristics
  - Higher values preserve more detail in bright areas

- **shadow_rolloff** (0.0 - 1.0, default: 0.3)
  - Controls the transition into shadow areas
  - Higher values create more gradual shadow falloff

- **blacks_crush** (0.0 - 0.5, default: 0.1)
  - Adjusts the depth of black levels
  - Higher values create more dramatic contrast

### Color Temperature

- **highlight_warmth** (-0.5 - 0.5, default: 0.2)
  - Adjusts color temperature in highlight areas
  - Positive values add warmth, negative values add coolness

- **midtone_warmth** (-0.5 - 0.5, default: 0.1)
  - Adjusts color temperature in midtone areas
  - Enables separate control of midtone color balance

- **shadow_coolness** (-0.5 - 0.5, default: 0.15)
  - Adjusts color temperature in shadow areas
  - Positive values add coolness to shadows

### Aberration and Distortion

- **chromatic_aberration** (0.0 - 1.0, default: 0.0)
  - Controls color fringing effect
  - Higher values create more pronounced color separation

- **barrel_distortion** (-0.5 - 0.5, default: 0.0)
  - Controls lens geometric distortion
  - Positive values create barrel effect, negative values create pincushion effect

## Usage

1. Connect an image output to the "images" input of the node
2. Adjust lens format parameters to set the basic anamorphic look
3. Fine-tune bokeh parameters for desired background blur characteristics
4. Adjust flare system parameters to create characteristic lens flares
5. Use color science controls to achieve desired tonal balance
6. Fine-tune color temperature across different tonal ranges
7. Add technical effects like chromatic aberration and barrel distortion as needed

## Technical Details

- Processes images in batches (B, H, W, C format)
- Utilizes GPU acceleration when available
- Implements sophisticated edge-aware processing
- Preserves color ratios during tonal adjustments
- Applies effects in optimal order for quality results

## Tips for Best Results

- Start with aspect ratio and squeeze settings to establish the basic anamorphic look
- Use bokeh rotation to match the natural angle of bright background elements
- Adjust flare position to complement the composition of your image
- Use highlight retention to prevent clipping in bright areas
- Apply chromatic aberration subtly for a more natural look
- Balance color temperature adjustments across tonal ranges for cohesive results
- Use barrel distortion sparingly to maintain natural perspective

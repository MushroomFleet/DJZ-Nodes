# Video Interlaced Upscaler V2

A ComfyUI custom node for applying interlaced upscaling effects to video frames with advanced control over field handling, interpolation, and motion compensation.

## Description

The Video Interlaced Upscaler V2 node provides sophisticated control over interlaced video processing, allowing users to simulate and manipulate interlaced video effects while upscaling frames. It's particularly useful for creating retro video effects, enhancing video quality, or achieving specific artistic looks.

## Parameters

### Required Parameters

- **images**: Input video frames to process
- **input_height** (default: 720, range: 480-4320)
  - The height of the input frames in pixels
  - Determines the base resolution before upscaling

- **input_width** (default: 1280, range: 640-7680)
  - The width of the input frames in pixels
  - Determines the base resolution before upscaling

- **field_order** (default: "top_first")
  - Options: "top_first", "bottom_first"
  - Determines which field (even or odd lines) is processed first
  - Affects the visual appearance of motion and interlacing artifacts

- **scale_factor** (default: 1.5, range: 1.0-4.0)
  - The factor by which to upscale the input frames
  - Higher values result in larger output resolution

- **blend_factor** (default: 0.25, range: 0.0-1.0)
  - Controls how much adjacent fields blend together
  - Higher values create smoother transitions between fields
  - Lower values maintain more distinct field separation

- **motion_compensation** (default: "basic")
  - Options: "none", "basic", "advanced"
  - none: No motion compensation applied
  - basic: Simple field-based motion smoothing
  - advanced: Temporal-aware motion compensation using adjacent frames

- **interpolation_mode** (default: "bilinear")
  - Options: "bilinear", "bicubic", "nearest"
  - Determines the algorithm used for scaling
  - bilinear: Smooth, balanced quality
  - bicubic: Higher quality but may introduce slight ringing
  - nearest: Sharp, pixelated look

- **deinterlace_method** (default: "blend")
  - Options: "blend", "bob", "weave"
  - blend: Smoothly combines fields
  - bob: Line doubling with field separation
  - weave: Interleaves fields with additional processing

### Optional Parameters

- **field_strength** (default: 1.0, range: 0.0-2.0)
  - Controls the intensity of the field separation effect
  - Higher values emphasize the interlaced look
  - Lower values create a more subtle effect

- **temporal_radius** (default: 1, range: 1-3)
  - Number of adjacent frames to consider for motion compensation
  - Only affects advanced motion compensation
  - Higher values can improve motion smoothness but may introduce artifacts

- **edge_enhancement** (default: 0.0, range: 0.0-1.0)
  - Applies additional sharpening to edges
  - Higher values create more defined edges
  - Can help combat blur from upscaling

## Usage Tips

1. **For Retro Video Effects:**
   - Use "top_first" field order
   - Set blend_factor to low values (0.1-0.2)
   - Choose "bob" deinterlace method
   - Enable edge enhancement (0.3-0.5)

2. **For Quality Upscaling:**
   - Use "advanced" motion compensation
   - Set blend_factor to medium values (0.3-0.4)
   - Choose "blend" deinterlace method
   - Use "bicubic" interpolation

3. **For Artistic Effects:**
   - Experiment with field_strength values
   - Try different combinations of deinterlace methods
   - Adjust temporal_radius for motion effects
   - Mix with edge enhancement for unique looks

## Output

The node outputs processed frames with:
- Applied interlacing effects
- Upscaled dimensions based on scale_factor
- Enhanced edges (if enabled)
- Motion compensation (if enabled)

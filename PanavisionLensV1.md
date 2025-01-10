# Panavision Lens Effect v1

A ComfyUI custom node that simulates the distinctive characteristics of Panavision anamorphic lenses, including oval bokeh, characteristic lens flares, unique color rendering, and aspect ratio adjustments.

## Features

- Anamorphic aspect ratio control
- Horizontal squeeze simulation
- Oval-shaped bokeh effects
- Dual-color horizontal lens flares
- Characteristic color temperature adjustments
- Real-time processing of images

## Parameters

### Aspect Ratio and Format

- **aspect_ratio** (1.85 - 2.76, default: 2.39)
  - Controls the final aspect ratio of the output image
  - Common values: 2.39:1 (standard anamorphic), 1.85:1 (wide-screen)

- **horizontal_squeeze** (1.0 - 2.0, default: 1.5)
  - Simulates the anamorphic lens squeeze factor
  - Higher values create more pronounced horizontal stretching
  - 1.5 is typical for classic Panavision lenses

### Bokeh Effects

- **bokeh_intensity** (0.0 - 1.0, default: 0.5)
  - Controls the strength of the oval bokeh effect
  - Higher values create more pronounced background blur

- **bokeh_threshold** (0.5 - 1.0, default: 0.8)
  - Sets the brightness threshold for bokeh effect application
  - Affects which bright areas trigger the oval bokeh

### Lens Flares

- **flare_intensity** (0.0 - 1.0, default: 0.4)
  - Controls the overall strength of lens flares
  - Higher values create more pronounced flare effects

- **blue_flare** (0.0 - 1.0, default: 0.7)
  - Adjusts the intensity of the blue component in lens flares
  - Creates the characteristic cool streak in the flare

- **orange_flare** (0.0 - 1.0, default: 0.6)
  - Adjusts the intensity of the orange component in lens flares
  - Creates the warm complementary streak in the flare

### Color Rendering

- **highlight_warmth** (0.0 - 1.0, default: 0.2)
  - Controls the warm color bias in highlight areas
  - Higher values add more orange tones to bright areas

- **shadow_coolness** (0.0 - 1.0, default: 0.15)
  - Controls the cool color bias in shadow areas
  - Higher values add more blue tones to darker areas

## Usage

1. Connect an image output to the "images" input of the node
2. Adjust the aspect ratio and horizontal squeeze to achieve desired anamorphic look
3. Fine-tune bokeh effects for background blur characteristics
4. Adjust flare parameters to create characteristic lens flares
5. Fine-tune color rendering using highlight warmth and shadow coolness
6. The processed image will maintain the input batch size with applied effects

## Technical Details

- Processes images in batches (B, H, W, C format)
- Automatically uses GPU acceleration when available
- Maintains image quality through bilinear interpolation
- All effects are applied non-destructively and can be adjusted in real-time

## Tips

- For classic Panavision look, start with 2.39:1 aspect ratio and 1.5x squeeze
- Bokeh effects are most noticeable in scenes with bright background points of light
- Flare effects work best with strong light sources in the frame
- Color temperature adjustments can be used subtly for natural-looking results

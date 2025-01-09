# VHS Effect v1

A ComfyUI custom node that simulates the visual characteristics and artifacts of VHS (Video Home System) tape recordings. This effect applies various distortions and noise patterns typical of VHS media, including luminance compression, chrominance bleeding, tracking errors, and analog noise.

## Parameters

### Luma (Brightness) Controls
- **luma_compression_rate** (Default: 1.0, Range: 0.1-10.0)
  - Controls the compression of brightness information
  - Higher values create more pronounced horizontal compression artifacts
  - Values closer to 1.0 maintain more original image clarity

- **luma_noise_sigma** (Default: 30.0, Range: 0.0-100.0)
  - Controls the intensity of brightness noise
  - Higher values create more grainy/static effects in the brightness channel
  - Set to 0 for no brightness noise

- **luma_noise_mean** (Default: 0.0, Range: -50.0-50.0)
  - Adjusts the overall brightness offset of the noise
  - Positive values make noise brighter, negative values make it darker
  - 0.0 maintains neutral noise brightness

### Chroma (Color) Controls
- **chroma_compression_rate** (Default: 1.0, Range: 0.1-10.0)
  - Controls the compression of color information
  - Higher values increase color bleeding and artifacts
  - Values closer to 1.0 maintain more original color accuracy

- **chroma_noise_intensity** (Default: 10.0, Range: 0.0-50.0)
  - Controls the intensity of color noise
  - Higher values create more color distortion and bleeding
  - Set to 0 for no color noise

### Blur and Distortion
- **vertical_blur** (Default: 1, Range: 1-21, Step: 2)
  - Controls vertical smearing of the image
  - Higher values create more vertical blur
  - Must be an odd number (automatically adjusted if even)

- **horizontal_blur** (Default: 1, Range: 1-21, Step: 2)
  - Controls horizontal smearing of the image
  - Higher values create more horizontal blur
  - Must be an odd number (automatically adjusted if even)

- **border_size** (Default: 1.7, Range: 0.0-10.0)
  - Controls the size of the black border on the right edge
  - Simulates the edge distortion common in VHS playback
  - Higher values create a larger black border

### Effect Intensity
- **generations** (Default: 3, Range: 1-10)
  - Simulates the degradation from multiple VHS copies
  - Higher values increase overall noise and distortion
  - Each "generation" multiplies the noise effects

## Input
- **images**: Accepts a batch of images to process

## Output
- Returns processed images with VHS effects applied

## Effect Details

The node applies several authentic VHS-style effects:
1. Separate processing of luminance (brightness) and chrominance (color) channels
2. Simulated tracking errors and wave distortions
3. Color bleeding and chroma noise
4. Horizontal compression artifacts
5. Edge distortion and black borders
6. Generation loss simulation
7. Analog-style noise and grain

## Usage Tips

1. For authentic VHS looks:
   - Keep compression rates between 1.0-3.0
   - Use moderate noise values (10-30)
   - Set generations to 2-4

2. For extreme degradation:
   - Increase compression rates above 5.0
   - Use high noise values (50+)
   - Set generations to 7-10

3. For subtle effects:
   - Keep compression rates close to 1.0
   - Use low noise values (5-15)
   - Set generations to 1-2

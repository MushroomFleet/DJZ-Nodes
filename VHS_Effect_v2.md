# VHS Effect v2

A ComfyUI custom node that simulates authentic VHS (Video Home System) tape effects and artifacts. This node processes images to recreate the characteristic visual qualities of VHS recordings, including noise, color bleeding, signal degradation, and tape speed effects.

## Features

- Converts images to YIQ color space for authentic analog video processing
- Simulates various VHS recording speeds (SP, LP, EP)
- Adds realistic video noise and chroma artifacts
- Simulates color bleeding effects
- Includes signal ringing artifacts
- Adjustable output sharpening
- Supports batch processing

## Parameters

### Composite Pre-emphasis
- **Range**: 0.0 to 8.0
- **Default**: 0.0
- **Description**: Controls the emphasis of the composite video signal. Higher values increase contrast and can lead to more pronounced artifacts.

### VHS Output Sharpening
- **Range**: 1.0 to 5.0
- **Default**: 1.5
- **Description**: Post-processing sharpening applied to the final image. Values above 1.0 increase image sharpness to compensate for VHS blur.

### Color Bleeding
- **Range**: 0.0 to 10.0
- **Default**: 0.0
- **Description**: Simulates color bleeding artifacts common in VHS tapes. Higher values create more pronounced color smearing effects.

### Video Noise
- **Range**: 0.0 to 4200.0
- **Default**: 2.0
- **Description**: Adds random noise to the luminance (brightness) channel. Higher values create more visible static and noise.

### Chroma Noise
- **Range**: 0.0 to 16384.0
- **Default**: 0.0
- **Description**: Adds noise specifically to the color channels. Creates color distortion and artifacts typical of worn VHS tapes.

### Chroma Phase Noise
- **Range**: 0.0 to 50.0
- **Default**: 0.0
- **Description**: Simulates phase errors in the color signal. Creates rainbow-like color shifts and distortions.

### Enable Ringing
- **Type**: Boolean
- **Default**: True
- **Description**: Toggles signal ringing artifacts that appear as echo-like effects around sharp edges.

### Ringing Power
- **Range**: 2 to 7
- **Default**: 2
- **Description**: Controls the intensity of the ringing effect when enabled. Higher values create more pronounced ringing artifacts.

### Tape Speed
- **Options**: SP, LP, EP
- **Default**: SP
- **Description**: Simulates different VHS recording speeds:
  - **SP (Standard Play)**: Highest quality, least degradation
  - **LP (Long Play)**: Medium quality, moderate degradation
  - **EP (Extended Play)**: Lowest quality, most degradation

## Usage Tips

1. For authentic VHS looks:
   - Start with SP tape speed for cleaner looks or EP for more degraded effects
   - Add moderate video noise (2.0-10.0)
   - Enable ringing with power 2-3
   - Add slight color bleeding (0.5-2.0)

2. For worn tape effects:
   - Increase chroma noise and phase noise
   - Use EP tape speed
   - Increase color bleeding
   - Add higher video noise values

3. For subtle VHS effects:
   - Use SP tape speed
   - Keep video noise low (1.0-5.0)
   - Disable ringing or use minimum power
   - Use minimal color bleeding

## Technical Details

The node processes images through several steps:
1. Converts RGB to YIQ color space for authentic analog processing
2. Applies various effects in the correct signal chain order
3. Processes each effect with consideration for VHS signal characteristics
4. Converts back to RGB color space for final output

The implementation includes authentic signal processing techniques used in real VHS systems, including:
- YIQ color space transformation
- Gaussian-filtered noise for realistic static
- Signal ringing simulation using FFT
- Color bleeding simulation using linear filtering

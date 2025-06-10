# Databending Effect v1

The Databending Effect v1 node is a creative image manipulation tool that applies audio-style effects to images through databending techniques. It works by converting image data into audio-like signals, applying audio effects, and converting the result back into image data, creating unique and glitch-like visual effects.

## Input Parameters

### Required

- **images**: The input batch of images to process
- **effect_type**: Choose from the following effects:
  - `echo`: Creates a delayed copy of the image data
  - `reverb`: Adds multiple decaying reflections to the image
  - `distortion`: Applies non-linear distortion to the image data
  - `bitcrush`: Reduces the bit depth of the image data
  - `tremolo`: Applies amplitude modulation
  - `phaser`: Creates sweeping filter effects
  - `chorus`: Adds slightly delayed and modulated copies

### Effect Parameters

- **echo_delay** (0.1 - 1.0, default: 0.3)
  - Controls the delay time for the echo effect
  - Higher values create more separated echoes
  
- **echo_decay** (0.0 - 0.9, default: 0.1)
  - Controls how quickly the echo fades out
  - Higher values make echoes persist longer

- **distortion_intensity** (0.1 - 1.0, default: 0.5)
  - Controls the amount of distortion applied
  - Higher values create more extreme distortion

- **modulation_rate** (0.1 - 10.0, default: 1.0)
  - Controls the speed of modulation effects (tremolo, phaser, chorus)
  - Higher values create faster modulation

- **modulation_depth** (0.1 - 2.0, default: 0.5)
  - Controls the intensity of modulation effects
  - Higher values create more pronounced modulation

## Usage Tips

1. **Echo Effect**: Best for creating ghost-like trailing effects. Use longer delays with moderate decay for distinct copies, or shorter delays with higher decay for a smearing effect.

2. **Reverb Effect**: Creates a diffused, dreamy version of the image. Works well with architectural or landscape images.

3. **Distortion Effect**: Adds aggressive artifacts and color shifts. Start with lower intensity values and increase for more extreme effects.

4. **Bitcrush Effect**: Creates pixelated and color-reduced effects. Effective for creating retro or low-fi aesthetics.

5. **Tremolo Effect**: Creates rhythmic brightness variations. Most noticeable with moderate to high modulation rates.

6. **Phaser Effect**: Produces sweeping color shifts. Works well with images that have large areas of similar colors.

7. **Chorus Effect**: Adds subtle doubling and movement to the image. Best used with moderate depth settings for subtle effects.

## Output

- Returns the processed image batch with the selected databending effect applied.
- Output images maintain the same dimensions and format as the input.

## Note

The effects are applied by treating image data as audio signals, which can produce unpredictable and creative results. Each effect may work differently depending on the image content and colors. Experimentation is encouraged to find the most interesting combinations of effects and parameters for your specific images.

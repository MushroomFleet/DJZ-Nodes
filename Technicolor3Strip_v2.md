# Technicolor 3-Strip v2

An advanced implementation of the classic Technicolor three-strip color process, featuring enhanced color controls and film characteristic simulations. This node provides a comprehensive suite of tools to achieve the rich, vibrant look of classic Hollywood films while offering fine-grained control over various aspects of the image processing.

## Parameters

### Color Channel Controls
- **red_strength** (default: 1.5, range: 0.1-3.0)
  - Controls the intensity of the red channel
  - Higher values create more pronounced reds, characteristic of classic Technicolor films
  
- **green_strength** (default: 1.3, range: 0.1-3.0)
  - Adjusts the intensity of the green channel
  - Fine-tune for natural foliage and skin tones
  
- **blue_strength** (default: 1.2, range: 0.1-3.0)
  - Controls the intensity of the blue channel
  - Affects sky tones and shadow characteristics

### Cross-processing
- **cross_process_amount** (default: 0.1, range: 0.0-0.5)
  - Controls color bleeding between channels
  - Simulates the imperfect color separation of the original process
  - Use sparingly for subtle color mixing effects

### Enhanced Color Controls
- **color_saturation** (default: 1.4, range: 0.0-3.0)
  - Overall color intensity adjustment
  - Higher values create more vivid colors
  - Values below 1.0 reduce color intensity

- **color_temperature** (default: 1.0, range: 0.5-2.0)
  - Adjusts the overall warmth or coolness of the image
  - Values > 1.0 create warmer tones
  - Values < 1.0 create cooler tones

- **color_vibrance** (default: 1.2, range: 0.5-2.0)
  - Intelligent saturation enhancement
  - Boosts muted colors while preventing already-saturated colors from clipping
  - Helps achieve rich colors without oversaturation

### Contrast and Tone Controls
- **contrast** (default: 1.2, range: 0.5-2.0)
  - Controls overall image contrast
  - Higher values increase tonal separation
  - Lower values create a flatter look

- **brightness** (default: 1.0, range: 0.5-1.5)
  - Adjusts overall image brightness
  - Fine-tune to balance the image's exposure

- **shadow_tone** (default: 0.9, range: 0.5-1.5)
  - Controls the density and detail in shadow areas
  - Higher values lift shadows
  - Lower values deepen shadows

- **highlight_tone** (default: 0.95, range: 0.5-1.5)
  - Manages highlight detail retention
  - Higher values preserve more highlight detail
  - Lower values allow highlights to bloom

### Film Characteristics
- **grain_amount** (default: 0.1, range: 0.0-1.0)
  - Adds simulated film grain
  - Higher values create more pronounced grain
  - Adds organic texture to the image

- **sharpness** (default: 1.1, range: 0.0-2.0)
  - Controls image definition
  - Higher values increase perceived sharpness
  - Lower values create a softer look

- **halation** (default: 0.2, range: 0.0-1.0)
  - Simulates light bleeding in film emulsion
  - Creates subtle glow around bright areas
  - Adds to the classic film look

## Usage Tips

1. **Basic Setup**
   - Start with default values for a balanced look
   - Adjust color channel strengths first to set the basic color balance
   - Fine-tune cross-processing for subtle color mixing

2. **Color Refinement**
   - Use color_temperature to set the overall mood
   - Adjust color_vibrance before color_saturation for more natural results
   - Balance shadow_tone and highlight_tone to control dynamic range

3. **Film Look**
   - Add grain last, after other adjustments are finalized
   - Use halation subtly for authentic film characteristics
   - Balance sharpness with grain for a cohesive look

4. **Common Combinations**
   - For a classic Technicolor look: Increase red_strength and color_saturation
   - For a vintage feel: Add grain and halation, reduce sharpness slightly
   - For high contrast look: Increase contrast and reduce shadow_tone

## Technical Details

The node processes images through multiple stages:
1. Channel separation and individual color processing
2. Cross-process simulation
3. Advanced color grading (temperature, vibrance, saturation)
4. Tone control and contrast adjustment
5. Film characteristic simulation (grain, halation, sharpness)

This version offers significant improvements over v1:
- More sophisticated color processing
- Advanced film characteristic simulation
- Finer control over image tonality
- Enhanced highlight and shadow management
- Additional creative controls for achieving specific looks

The node supports batch processing and maintains original image dimensions and aspect ratios.

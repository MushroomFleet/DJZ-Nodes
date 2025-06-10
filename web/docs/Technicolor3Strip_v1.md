# Technicolor 3-Strip v1

This custom node emulates the classic Technicolor three-strip color process, a pioneering color film process used from the 1930s to the 1950s. It simulates the rich, vibrant color palette characteristic of classic Hollywood films by independently processing red, green, and blue color channels.

## Parameters

### Color Channel Strengths
- **red_strength** (default: 1.5, range: 0.1-3.0)
  - Controls the intensity of the red channel
  - Higher values create more pronounced reds, typical of Technicolor's famous "ruby slippers" effect
  
- **green_strength** (default: 1.3, range: 0.1-3.0)
  - Adjusts the intensity of the green channel
  - Affects the rendering of foliage and helps balance the overall color palette
  
- **blue_strength** (default: 1.2, range: 0.1-3.0)
  - Manages the intensity of the blue channel
  - Influences sky tones and cool colors in the image

### Color Processing
- **cross_process_amount** (default: 0.1, range: 0.0-0.5)
  - Controls the amount of color bleeding between channels
  - Simulates the subtle color mixing that occurred in the original Technicolor process
  - Higher values create more pronounced color cross-contamination effects

- **saturation_boost** (default: 1.2, range: 0.5-2.0)
  - Enhances the overall color saturation
  - Values above 1.0 increase color intensity, while values below 1.0 reduce it
  - Helps achieve the vivid, saturated look of Technicolor films

### Image Enhancement
- **contrast_boost** (default: 1.1, range: 0.5-2.0)
  - Adjusts the overall contrast of the image
  - Higher values create more dramatic contrast typical of classic film
  - Helps achieve the punchy look of Technicolor movies

### Tone Protection
- **shadow_preservation** (default: 0.8, range: 0.0-1.0)
  - Controls how much detail is preserved in darker areas
  - Higher values retain more shadow detail
  - Helps prevent shadows from becoming too crushed or blocked up

- **highlight_protection** (default: 0.9, range: 0.0-1.0)
  - Manages the preservation of highlight details
  - Higher values prevent highlights from blowing out
  - Helps maintain detail in bright areas while still allowing for the characteristic Technicolor look

## Usage Tips

1. Start with the default values, which are calibrated to provide a balanced Technicolor look
2. Adjust the color strengths first to get the basic color balance you want
3. Use cross_process_amount sparingly - a little goes a long way
4. Fine-tune the saturation and contrast to taste
5. Use shadow_preservation and highlight_protection to recover any lost detail in the extremes

## Technical Details

The node processes images through several stages:
1. Separates the image into individual color channels
2. Applies independent strength adjustments to each channel
3. Implements cross-processing between channels
4. Enhances contrast and saturation
5. Applies shadow and highlight protection
6. Recombines the channels into the final image

This node works with batches of images and preserves the original image dimensions and aspect ratios.

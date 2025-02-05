# Classic Film Effect Node

A ComfyUI node that simulates the characteristics and imperfections of classic film stocks, providing a realistic analog film look to digital images.

## Description

The Classic Film Effect node applies various film stock simulations to your images, replicating the unique characteristics of popular film stocks like Kodachrome, Portra, and Tri-X. It simulates not only the color and tone response of these films but also their physical characteristics like grain, halation, and common analog artifacts.

## Features

- 9 authentic film stock simulations
- Adjustable grain, vignette, and halation effects
- Film degradation effects (dust and scratches)
- Frame jitter simulation
- High-precision color processing
- Resolution-independent effects

## Film Stocks

1. **Kodachrome 64**
   - Warm color temperature (6500K)
   - Slightly enhanced contrast and saturation
   - Fine grain structure
   - Known for vibrant yet natural colors

2. **Portra 400** (Default)
   - Natural color temperature (5900K)
   - Very subtle contrast enhancement
   - Moderate grain
   - Excellent skin tones and neutral color balance

3. **Velvia 50**
   - Daylight balanced (5500K)
   - Enhanced contrast and saturation
   - Very fine grain
   - Known for vibrant landscape photography

4. **Tri-X 400**
   - Classic black and white film
   - Higher contrast
   - Pronounced grain structure
   - Excellent shadow detail

5. **HP5 Plus**
   - Traditional black and white film
   - Moderate contrast
   - Fine grain structure
   - Wide exposure latitude

6. **Ektachrome E100**
   - Slightly warm color temperature (6200K)
   - Neutral contrast
   - Fine grain
   - Natural color reproduction

7. **Pro 400H**
   - Neutral color temperature (5800K)
   - Very subtle contrast
   - Moderate grain
   - Excellent highlight handling

8. **Delta 3200**
   - High-speed black and white film
   - Enhanced contrast
   - Very pronounced grain
   - Excellent low-light performance

9. **Cinestill 800T**
   - Tungsten-balanced (3200K)
   - Moderate contrast
   - Notable grain structure
   - Characteristic halation effect

## Parameters

### Required Inputs

- **images**: The input images to process
- **film_stock**: Choice of film simulation (default: "portra400")
- **grain_intensity**: Controls the strength of film grain (0.0 - 1.0, default: 0.04)
  - Lower values (0.01-0.05) for subtle grain
  - Higher values (0.05-0.1) for more pronounced grain
  - Values above 0.1 for artistic effect

- **vignette_strength**: Controls the darkening of image corners (0.0 - 1.0, default: 0.1)
  - 0.0: No vignette
  - 0.1-0.2: Subtle natural vignette
  - Above 0.3: More dramatic effect

- **scratch_probability**: Controls the likelihood of film scratches (0.0 - 1.0, default: 0.02)
  - 0.0: No scratches
  - 0.01-0.03: Occasional scratches
  - Above 0.05: Heavy wear effect

- **dust_density**: Controls the amount of dust particles (0.0 - 0.1, default: 0.001)
  - 0.0: No dust
  - 0.001-0.002: Light dust
  - Above 0.005: Heavy dust effect

- **halation_strength**: Controls the glow around bright areas (0.0 - 1.0, default: 0.05)
  - 0.0: No halation
  - 0.05-0.1: Subtle glow
  - Above 0.2: Strong bloom effect

- **enable_jitter**: Toggles slight frame movement simulation (default: True)
  - True: Enables subtle frame movement
  - False: Disables movement

- **seed**: Random seed for consistent results (default: 0)
  - Any integer value
  - Same seed produces same grain/dust/scratch patterns

## Usage Tips

1. **For Natural Film Look:**
   - Use Portra 400 or Pro 400H
   - Keep grain_intensity around 0.04
   - Set vignette_strength to 0.1
   - Use minimal dust_density (0.001) and scratch_probability (0.02)

2. **For Vintage Look:**
   - Use Kodachrome 64 or Ektachrome E100
   - Increase grain_intensity to 0.06-0.08
   - Set vignette_strength to 0.2
   - Increase dust_density to 0.002-0.003

3. **For Classic Black & White:**
   - Use Tri-X 400 or HP5 Plus
   - Adjust grain_intensity based on preference (0.04-0.08)
   - Consider higher contrast through tone curve adjustments

4. **For Cinematic Look:**
   - Use Cinestill 800T
   - Enable halation (0.1-0.15 strength)
   - Moderate grain (0.05-0.07)
   - Subtle vignette (0.15-0.2)

## Examples

The node works best when:
- Used as a final processing step
- Applied to well-exposed images
- Combined with appropriate film stock for the subject matter:
  - Portra 400 for portraits
  - Velvia 50 for landscapes
  - Tri-X 400 for street photography
  - Cinestill 800T for night scenes

## Technical Notes

- All effects scale appropriately with image resolution
- Maintains high color fidelity through floating-point processing
- Grain, dust, and scratches are resolution-independent
- Preserves image dynamic range through careful tone mapping

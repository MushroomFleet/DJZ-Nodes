# Lens Leaks & Flares Node

A ComfyUI node that simulates realistic lens leaks and lens flares effects commonly seen in photography and cinematography. This node can create both light leak effects and dynamic lens flares with customizable parameters for maximum creative control.

## Modes

### Lens Leaks Mode
Creates random light leaks that simulate light entering through small gaps or imperfections in the lens housing. These effects can add warmth, atmosphere, and a vintage feel to your images.

### Lens Flares Mode
Simulates the optical artifact that occurs when light is scattered or flared in a lens system, creating a characteristic pattern of artifacts and glowing effects.

## Parameters

### Common Parameters
- **intensity** (0.0 - 1.0, default: 0.5)
  - Controls the strength of the overall effect
  - Higher values create more pronounced effects
  - Lower values create subtle effects

- **chromatic_aberration** (0.0 - 1.0, default: 0.2)
  - Simulates color fringing and color separation
  - Creates RGB color shifts around bright areas
  - Higher values increase the separation distance

- **bloom_radius** (10 - 200, default: 50)
  - Controls the size of the glow around bright areas
  - Larger values create softer, more diffused glows
  - Smaller values create tighter, more focused glows

### Lens Leaks Specific Parameters
- **leak_color** (warm/cool/rainbow)
  - warm: Creates orange-tinted leaks for a vintage feel
  - cool: Creates blue-tinted leaks for a modern look
  - rainbow: Creates multi-colored leaks with varying hues

- **num_leaks** (1 - 10, default: 3)
  - Controls how many individual light leaks appear
  - Each leak is randomly positioned

- **leak_size** (0.1 - 1.0, default: 0.3)
  - Controls the size of each individual leak
  - Expressed as a fraction of the image size

### Lens Flares Specific Parameters
- **flare_position** (0.0 - 1.0, default: 0.5)
  - Controls the horizontal position of the lens flare
  - 0.0 is left edge, 1.0 is right edge
  - Creates realistic flare positioning

## Technical Details

The node processes images using a combination of techniques:
- Radial gradients for leak and flare generation
- Gaussian blur for bloom effects
- Channel splitting for chromatic aberration
- HSV color space manipulation for rainbow effects

All effects are applied in a physically-inspired way, simulating real optical phenomena that occur in camera lenses.

## Usage Tips

1. For vintage photography looks:
   - Use lens leaks mode
   - Set leak_color to "warm"
   - Use moderate intensity (0.3-0.6)
   - Add slight chromatic aberration

2. For modern cinematic flares:
   - Use lens flares mode
   - Position flares intentionally
   - Use larger bloom radius
   - Add moderate chromatic aberration

3. For psychedelic effects:
   - Use lens leaks mode
   - Set leak_color to "rainbow"
   - Use higher number of leaks
   - Increase intensity and leak size

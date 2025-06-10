# Cathode Ray Effect Node

This node simulates the visual characteristics of a CRT (Cathode Ray Tube) display, creating authentic retro screen effects. It combines multiple effects including screen curvature, scanlines, glow, color bleeding, and noise to create a convincing CRT monitor appearance.

## Parameters

### Preset
- **Type:** Dropdown
- **Options:** static, fluctuating, degraded, custom
- **Default:** static
- **Description:**
  - `static`: Maintains consistent effect intensity
  - `fluctuating`: Creates a subtle pulsing effect
  - `degraded`: Gradually reduces effect intensity over time
  - `custom`: Uses a custom mathematical expression for time-based variation

### Custom Expression
- **Type:** String
- **Default:** `sin(t/10) * 0.1 + 0.2`
- **Description:** A mathematical expression that controls effect intensity over time when using the "custom" preset. The variable `t` represents the current frame index.

### Screen Curvature
- **Type:** Float
- **Range:** 0.0 to 1.0
- **Default:** 0.2
- **Description:** Controls the amount of screen bulging/curvature typical of CRT displays. Higher values create more pronounced curved edges.

### Scanline Intensity
- **Type:** Float
- **Range:** 0.0 to 1.0
- **Default:** 0.3
- **Description:** Controls the visibility of horizontal scanlines. Higher values create more pronounced dark lines between scan rows.

### Glow Amount
- **Type:** Float
- **Range:** 0.0 to 1.0
- **Default:** 0.2
- **Description:** Controls the amount of bloom/glow around bright areas, simulating the phosphor glow of CRT displays.

### Color Bleeding
- **Type:** Float
- **Range:** 0.0 to 1.0
- **Default:** 0.15
- **Description:** Simulates color fringing and bleeding between adjacent pixels, typical of CRT displays. Higher values create more pronounced color separation.

### Noise Amount
- **Type:** Float
- **Range:** 0.0 to 0.5
- **Default:** 0.05
- **Description:** Adds random noise to simulate screen interference and grain. Higher values create more visible noise.

## Usage Tips

1. For a classic CRT look, start with the "static" preset and adjust the scanline intensity and screen curvature.
2. Use the "fluctuating" preset to create a more dynamic, living CRT effect.
3. The "degraded" preset is useful for creating worn-out or failing CRT monitor effects.
4. When using custom expressions, you can use any Python math functions (sin, cos, etc.) and the variable 't' which represents the current frame number.

## Custom Expression Examples

- `sin(t/10) * 0.1 + 0.2`: Creates a smooth, sinusoidal variation
- `random() * 0.3 + 0.7`: Creates random fluctuations
- `max(0.2, 1 - t/100)`: Creates a gradual decay effect

## Technical Details

The node applies effects in the following order:
1. Screen curvature (barrel distortion)
2. Phosphor glow (gaussian blur)
3. Color bleeding (channel-specific vertical blur)
4. Noise addition
5. Scanline overlay

Each effect's intensity can be modulated by the chosen preset or custom expression, allowing for dynamic variations over time.

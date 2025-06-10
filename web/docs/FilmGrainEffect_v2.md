# Film Grain Effect V2 (video)

This node applies a customizable film grain effect to a batch of images, with support for both preset patterns and custom mathematical expressions.

## Input Parameters

- **images**: A batch of input images to process
- **preset**: Choose from predefined grain patterns or select "custom" to use your own expression
  - custom: Use your own mathematical expression
  - subtle: Light grain effect with gentle temporal variation
  - vintage: Classic film grain with periodic intensity changes
  - unstable_signal: Dynamic grain pattern with multiple frequency components
  - dip: Periodic intensity dips
  - ebb: Smooth oscillating grain pattern
  - flow: Flowing grain pattern with dual frequency modulation
- **expression_input**: Mathematical expression for custom grain pattern (used when preset is "custom")
  - Available functions: sin, cos, exp, abs, pow
  - Constants: pi, e
  - Random distributions: normal(mean, std), uniform(min, max)
  - Time variable: t (scaled by time_scale)
- **base_intensity**: Overall strength of the grain effect (0.0 to 1.0)
- **time_scale**: Controls the speed of temporal variations (0.1 to 10.0)
- **noise_scale**: Controls the scale/contrast of the noise pattern (0.0 to 1.0)
- **seed**: Random seed for reproducible results

## Expression Examples

The following preset expressions can be used as references for creating custom patterns:

```python
# Subtle grain
0.08 * normal(0.5, 0.15) * (1 + 0.2 * sin(t/25))

# Vintage film
0.15 * normal(0.5, 0.25) * (1 + 0.3 * sin(t/12)) + 0.05 * exp(-(t % 40)/10)

# Unstable signal
0.15 * normal(0.5, 0.3) * (1 + 0.5 * sin(t/5)) + 0.1 * sin(t/3) * exp(-t/100 % 20) + 0.05 * uniform(-1, 1) * sin(t/7)**2
```

## Expression Guidelines

1. Use `t` as the time variable (frame number × time_scale)
2. Combine random distributions (normal, uniform) with periodic functions (sin, cos)
3. Use modulo (%) for repeating patterns
4. Keep final values reasonable (typically between 0 and 1)
5. Test with different time_scale values to adjust temporal variation speed

## Output

- Returns the processed images with film grain effect applied
- Output maintains the same dimensions and format as input
- Values are automatically clipped to valid range (0 to 1)

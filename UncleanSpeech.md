# UncleanSpeech Node

## Description
The UncleanSpeech node is a powerful audio processing tool designed to emulate various audio systems and environments. It applies a chain of audio effects including compression, equalization, distortion, noise generation, and reverb to transform clean audio into stylized or degraded versions.

## Features
- Preset system for saving and loading effect configurations
- Comprehensive audio effect chain
- Support for multi-channel audio
- Automatic audio normalization
- Detailed logging system for troubleshooting

## Parameters

### Basic Input
- **audio**: Input audio signal (required)
- **preset**: Select from available preset configurations (if any exist in the presets folder)

### Compression
- **compression_ratio** (1.0 - 20.0, default: 1.0)
  - Controls the intensity of dynamic range compression
  - Higher values result in more aggressive compression
  - 1.0 means no compression

- **compression_threshold** (-60.0 - 0.0 dB, default: -20.0)
  - Sets the threshold level where compression begins
  - Signals above this threshold will be compressed
  - Lower values affect more of the audio signal

### Equalization
- **low_cut** (20.0 - 2000.0 Hz, default: 20.0)
  - Sets the low-frequency cutoff point
  - Frequencies below this value are attenuated
  - Higher values remove more low frequencies

- **high_cut** (1000.0 - 20000.0 Hz, default: 20000.0)
  - Sets the high-frequency cutoff point
  - Frequencies above this value are attenuated
  - Lower values remove more high frequencies

### Distortion
- **distortion_amount** (0.0 - 1.0, default: 0.0)
  - Controls the amount of harmonic distortion
  - Uses soft clipping algorithm
  - Higher values create more aggressive distortion
  - 0.0 means no distortion

### Noise
- **noise_level** (0.0 - 1.0, default: 0.0)
  - Controls the amplitude of added noise
  - 0.0 means no noise, 1.0 is maximum noise

- **noise_color** (Options: "white", "pink", "brown")
  - White: Equal energy per frequency
  - Pink: Energy decreases by 3dB per octave
  - Brown: Energy decreases by 6dB per octave

### Reverb
- **reverb_amount** (0.0 - 1.0, default: 0.0)
  - Controls the wet/dry mix of the reverb effect
  - 0.0 is dry (no reverb), 1.0 is fully wet

- **room_size** (0.1 - 1.0, default: 0.5)
  - Controls the simulated room size for reverb
  - Affects the length and density of reverb reflections
  - Larger values create longer reverb tails

## Using Presets
The node supports preset configurations stored in .preset files. These should be placed in the 'presets' directory within the node's folder. Presets are JSON files that can store combinations of effect parameters for quick recall.

## Example Use Cases
1. **Lo-fi Effect**: Use high compression ratio, add noise, and cut high frequencies
2. **Telephone Effect**: Set narrow EQ band, add distortion and noise
3. **Room Simulation**: Use reverb with appropriate room size
4. **Vintage Recording**: Combine noise, compression, and EQ to emulate old recording equipment

## Technical Details
- Supports multi-channel audio processing
- Automatically handles various input tensor shapes
- Includes comprehensive error handling and logging
- Normalizes output to prevent clipping
- Preserves input sample rate

## Output
Returns processed audio with the same number of channels and sample rate as the input, but with applied effects chain.

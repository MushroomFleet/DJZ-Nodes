# VoiceEffects2 - Voice Effects Processor 2

## Overview
The **VoiceEffects2** custom node processes audio by applying a variety of voice effects. It uses an external preset file from the `voice-effects/` folder to determine which effects to apply. This preset acts as a whitelist, ensuring only the desired effects are executed. The node is designed for audio manipulation within the custom nodes ecosystem.

## Features
- **Dynamic Preset Loading:** Loads a preset file (e.g., `ethereal.py`, `robot.py`, etc.) from the `voice-effects/` folder to control the effects pipeline.
- **Multi-Effect Processing:** Supports a range of effects including reverb, frequency filtering, vibrato, formant shifting, echo, and distortion.
- **Robust Logging:** Logs each processing step to both standard error and a dedicated log file (`voice_effects2.log`), facilitating debugging and troubleshooting.

## Inputs
- **audio:**  
  A dictionary containing the audio data.  
  **Required Keys:**
  - `waveform`: The audio waveform provided either as a PyTorch tensor or a NumPy array.
  - `sample_rate` (optional): The sample rate for the audio. If not provided, it defaults to 44100 Hz.
  
- **effect_presets:**  
  A string corresponding to a filename (from the `voice-effects/` folder) that defines the set of effects to be applied. This is selected via a dropdown in the user interface.

## Outputs
Returns a dictionary containing:
- `waveform`: The processed audio as a PyTorch tensor.
- `sample_rate`: The sample rate used during processing.
- `path`: Currently set to `None`, reserved for potential file path outputs in future use cases.

## Processing Pipeline
1. **Input Validation and Conversion:**  
   - Verifies that the `audio` input is a dictionary and contains a valid `waveform`.
   - Converts the waveform to a consistent NumPy array format.

2. **Preset File Loading:**  
   - Constructs the full path to the preset file using the selected `effect_presets` value.
   - Reads and executes the preset code within an environment where an instance of `EffectsExecutor` is available.

3. **Channel-wise Processing:**  
   - Iterates over each batch and audio channel.
   - Applies the effects as defined in the preset file.

4. **Normalization:**  
   - Normalizes the processed audio based on the maximum absolute amplitude.

5. **Tensor Conversion:**  
   - Converts the processed NumPy array back into a PyTorch tensor for standardized output.

## Detailed Functions and Parameters

### EffectsExecutor Class
The internal `EffectsExecutor` class is responsible for applying individual audio effects. Its key methods include:

- **apply_reverb / add_reverb**  
  *Parameters:*  
  - `room_size`: Determines the length of the impulse response, affecting the reverb duration.  
  - `damping`: Controls the decay rate of the reverb effect.  
  *Description:*  
  Applies a convolution-based reverb effect to simulate acoustic environments.

- **apply_frequency_filter**  
  *Parameters:*  
  - `cutoff_freq`: The cutoff frequency for the filter.  
  - `filter_type`: Type of filter to apply; supported types are `lowpass`, `highpass`, and `bandpass`.  
  *Description:*  
  Utilizes a Butterworth filter to selectively reduce or enhance parts of the frequency spectrum.

- **add_vibrato**  
  *Parameters:*  
  - `freq`: Frequency of the vibrato modulation.  
  - `depth`: Intensity of the vibrato effect.  
  *Description:*  
  Introduces a periodic shift in the audio signal, creating a vibrato effect.

- **change_formants**  
  *Parameters:*  
  - `shift_factor`: A multiplier used to alter the formant frequencies.  
  *Description:*  
  Adjusts the spectral envelope of the audio via an STFT-based method and interpolation, thereby modifying perceived voice character.

- **add_echo**  
  *Parameters:*  
  - `delay_time`: The delay before the echo effect is applied, in seconds.  
  - `decay`: The amplitude decay factor for the echoed signal.  
  *Description:*  
  Produces an echo by adding a delayed and decayed copy of the original audio signal.

- **add_distortion**  
  *Parameters:*  
  - `gain`: The amplification factor applied to the original audio.  
  - `threshold`: Maximum threshold value; signals are clipped to this value to achieve distortion.  
  *Description:*  
  Distorts the audio by amplifying and clipping the signal, then normalizes it to prevent clipping artifacts.

## Usage Example
Below is an example demonstrating how to utilize the **VoiceEffects2** node:

```python
import torch
from VoiceEffects2 import VoiceEffects2

# Create a sample audio input (1 second of random noise at 44100 Hz)
audio_input = {
    "waveform": torch.randn(1, 1, 44100),
    "sample_rate": 44100
}

# Choose a preset from the 'voice-effects' folder
preset_filename = "ethereal.py"

# Initialize the node and process the audio
voice_effect_node = VoiceEffects2()
result = voice_effect_node.process(audio_input, preset_filename)

# The result is a dictionary with the processed waveform, sample rate, and a file path placeholder
print(result)
```

## Troubleshooting
- **Preset File Missing:**  
  Ensure that the preset file specified in `effect_presets` exists in the `voice-effects/` folder.
- **Logging:**  
  Review the `voice_effects2.log` file for detailed information on processing steps and error messages.
- **Input Issues:**  
  Verify that the `audio` dictionary has a valid `waveform` and (optionally) a proper `sample_rate`.

## Dependencies
- **External Libraries:**  
  - numpy  
  - torch  
  - scipy  
  - librosa
- **Standard Libraries:**  
  - os, glob, sys

## License & Credits
Include your license information and any necessary credits or attributions here.

---

This document details the functionality, usage, and inner workings of the VoiceEffects2 custom node. It is intended to guide users in integrating and troubleshooting the node effectively.

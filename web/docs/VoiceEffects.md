# VoiceEffects Node Documentation

## Overview

The **VoiceEffects** node is designed to process an audio input by applying a suite of voice effects. It supports multiple audio effects ranging from reverb to distortion, making it a versatile tool for audio processing tasks. The node accepts a dictionary containing the audio waveform and optional sample rate, processes it using various effects, and outputs the modified audio.

## Node Structure

### Class Attributes and Initialization

- **Type & Output Type**:  
  - `type`: "VoiceEffects"  
  - `output_type`: "AUDIO"  
  Indicates the node's role and the type of output it produces.
- **Output Dimensions**:  
  - `output_dims`: 1  
  Specifies the dimensionality of the output.
- **Category, Name & Description**:  
  - `category`: "Audio"  
  - `name`: "Voice Effects Processor"  
  - `description`: "Applies various voice effects including reverb, filtering, vibrato, formant shifting, echo, and distortion"  
  Provides details for UI display and user understanding.
- **Logging**:  
  The node creates a log file (`voice_effects.log`) in the same directory to record processing steps and errors during execution.

### Core Functions

#### 1. log(message)
- **Purpose**:  
  Logs messages both to the standard error stream and to a log file, aiding in debugging and tracking the internal processing workflow.
- **Usage**:  
  Invoked internally at various steps to log the status and any errors.

#### 2. INPUT_TYPES (classmethod)
- **Purpose**:  
  Defines the input parameters required by the node. This specification allows the node to integrate seamlessly within the system’s UI and parameter management.
- **Parameters**:
  - **audio**:  
    - Type: "AUDIO"  
    - Must be a dictionary containing a key `"waveform"`. Optionally, it may include `"sample_rate"` (default is 44100 Hz).
  
  - **Reverb Parameters**:
    - **room_size**:  
      - Type: FLOAT  
      - Description: Controls the reverb length, scaled to the sample rate.  
      - Range: 0.0 to 1.0, Default: 0.1
    - **damping**:  
      - Type: FLOAT  
      - Description: Determines how quickly the reverb decays.  
      - Range: 0.0 to 1.0, Default: 0.1
  
  - **Frequency Filter Parameters**:
    - **cutoff_freq**:  
      - Type: FLOAT  
      - Description: Sets the cutoff frequency for filtering.  
      - Range: 300 Hz to 5000 Hz, Default: 300
    - **filter_type**:  
      - Type: List (options: "lowpass", "highpass", "bandpass")  
      - Description: Specifies the type of frequency filter.
  
  - **Vibrato Parameters**:
    - **vibrato_freq**:  
      - Type: FLOAT  
      - Description: Frequency of modulation for the vibrato effect.  
      - Range: 1.0 to 10.0 Hz, Default: 1.0
    - **vibrato_depth**:  
      - Type: FLOAT  
      - Description: Depth or intensity of the vibrato effect.  
      - Range: 0.0 to 1.0, Default: 0.1
  
  - **Formant Shifting**:
    - **shift_factor**:  
      - Type: FLOAT  
      - Description: Controls the scaling factor for formant frequency shifting.  
      - Range: 0.5 to 2.0, Default: 0.5

  - **Echo Parameters**:
    - **delay_time**:  
      - Type: FLOAT  
      - Description: Delay before the echo starts, in seconds.  
      - Range: 0.1 to 1.0, Default: 0.1
    - **decay**:  
      - Type: FLOAT  
      - Description: Decay factor for the echo effect.  
      - Range: 0.1 to 1.0, Default: 0.3

  - **Distortion Parameters**:
    - **gain**:  
      - Type: FLOAT  
      - Description: Amplification factor applied before the distortion effect.  
      - Range: 1.0 to 5.0, Default: 1.0
    - **threshold**:  
      - Type: FLOAT  
      - Description: Clipping threshold for distortion.  
      - Range: 0.1 to 1.0, Default: 0.1

#### 3. process(...)
- **Purpose**:  
  Implements the audio processing pipeline by applying a series of effects sequentially.
- **Processing Steps**:
  1. **Input Validation**:  
     Checks that the audio input is a dictionary and contains the required `"waveform"` key.
  2. **Audio Data Conversion**:  
     Converts the received waveform into a NumPy array or Torch tensor with the expected shape `[batch, channels, samples]`.
  3. **Effect Applications**:  
     Sequentially applies the following effects:
     - **Reverb**: Uses an exponentially decaying impulse response.
     - **Frequency Filter**: Applies a Butterworth filter based on the chosen type (lowpass, highpass, bandpass).
     - **Vibrato**: Introduces a modulation-based delay to create a vibrato effect.
     - **Formant Shifting**: Alters the audio’s timbre via STFT and magnitude interpolation.
     - **Echo**: Adds a delayed version of the signal modulated by a decay factor.
     - **Distortion**: Applies gain and clips the signal to generate distortion.
  4. **Normalization and Output**:  
     Normalizes the final processed audio and converts it back to a Torch tensor, ensuring compatibility with subsequent nodes.

## How to Use the VoiceEffects Node

1. **Prepare the Input**:
   - Ensure that the audio input is provided as a dictionary with a key `"waveform"`.
   - Optionally include `"sample_rate"`; if omitted, a default of 44100 Hz is used.

2. **Adjust Parameters as Needed**:
   - **Reverb**:  
     Modify `room_size` and `damping` to control the character and length of the reverb.
   - **Frequency Filter**:  
     Set `cutoff_freq` and choose a `filter_type` to target specific frequency ranges.
   - **Vibrato**:  
     Adjust `vibrato_freq` and `vibrato_depth` to add a modulating effect to the audio.
   - **Formant Shifting**:  
     Change `shift_factor` to adjust the vocal quality.
   - **Echo**:  
     Use `delay_time` and `decay` to configure how pronounced the echo is.
   - **Distortion**:  
     Tweak `gain` and `threshold` to achieve the desired level of distortion effect.

3. **Execution Process**:
   - On execution, the node processes the input audio by applying each effect in the above-described sequence.
   - Processing steps are logged for monitoring and debugging via `voice_effects.log`.

## Logging and Debugging

- The node logs all processing activities and any potential errors to both STDERR and a dedicated log file (`voice_effects.log`).
- These logs assist in troubleshooting and provide insight into the processing stages.

## Final Output

- The processed audio is returned as a dictionary containing:
  - `"waveform"`: The processed audio tensor.
  - `"sample_rate"`: The sample rate used for processing.
  - `"path"`: A placeholder for the audio file path (if applicable).

This documentation should serve as a comprehensive guide to understanding and utilizing the VoiceEffects node in your audio processing pipeline.

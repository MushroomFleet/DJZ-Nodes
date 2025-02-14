import numpy as np
import torch
import scipy.signal as signal
import librosa
import os
import glob
import sys

class VoiceEffects2:
    def __init__(self):
        self.type = "VoiceEffects2"
        self.output_type = "AUDIO"
        self.output_dims = 1
        self.compatible_decorators = []
        self.required_extensions = []
        self.category = "Audio"
        self.name = "Voice Effects Processor 2"
        self.description = ("Applies voice effects based on an external preset file "
                            "located in the voice-effects/ folder. The preset file, chosen "
                            "via the dropdown 'effect_presets', acts as a whitelist for "
                            "the effects to apply.")
        # Setup logging file in the same directory
        self.log_file = os.path.join(os.path.dirname(__file__), 'voice_effects2.log')

    def log(self, message):
        """Log message to file and stderr"""
        print(message, file=sys.stderr)
        try:
            with open(self.log_file, 'a') as f:
                f.write(message + '\n')
        except Exception as e:
            print("Logging error:", e, file=sys.stderr)

    @classmethod
    def INPUT_TYPES(cls):
        import os, glob
        current_dir = os.path.dirname(__file__)
        preset_folder = os.path.join(current_dir, "voice-effects")
        files = []
        if os.path.isdir(preset_folder):
            files = [os.path.basename(p) for p in glob.glob(os.path.join(preset_folder, "*.py"))]
        return {
            "required": {
                "audio": ("AUDIO",),
                "effect_presets": (files,)
            }
        }

    RETURN_TYPES = ("AUDIO",)
    RETURN_NAMES = ("audio",)
    FUNCTION = "process"

    class EffectsExecutor:
        def __init__(self, data, sample_rate, log_func):
            self.data = data  # numpy array for a single audio channel
            self.sample_rate = sample_rate
            self.log = log_func

        def apply_reverb(self, room_size, damping):
            self.log("Applying Reverb")
            reverb_len = int(self.sample_rate * room_size)
            impulse = np.exp(-damping * np.linspace(0, reverb_len, reverb_len))
            if len(impulse) < len(self.data):
                impulse = np.pad(impulse, (0, len(self.data) - len(impulse)), mode='constant')
            reverb_signal = signal.convolve(self.data, impulse, mode='same')
            self.data = 0.6 * self.data + 0.4 * reverb_signal

        def add_reverb(self, room_size, damping):
            self.apply_reverb(room_size, damping)

        def apply_frequency_filter(self, cutoff_freq, filter_type):
            self.log("Applying Frequency Filter")
            nyquist = self.sample_rate / 2
            normalized_cutoff = cutoff_freq / nyquist
            order = 4
            if filter_type == "lowpass":
                b, a = signal.butter(order, normalized_cutoff, btype="low")
            elif filter_type == "highpass":
                b, a = signal.butter(order, normalized_cutoff, btype="high")
            elif filter_type == "bandpass":
                b, a = signal.butter(order, [normalized_cutoff * 0.5, normalized_cutoff], btype="band")
            else:
                self.log(f"Unknown filter type: {filter_type}. Skipping filter.")
                return
            self.data = signal.filtfilt(b, a, self.data)

        def add_vibrato(self, freq, depth):
            self.log("Adding Vibrato")
            t = np.arange(len(self.data)) / self.sample_rate
            mod = depth * np.sin(2 * np.pi * freq * t)
            delay_samples = (mod * self.sample_rate).astype(int)
            vibrato_signal = np.zeros_like(self.data)
            for i in range(len(self.data)):
                index = i - delay_samples[i]
                if 0 <= index < len(self.data):
                    vibrato_signal[i] = self.data[index]
            self.data = vibrato_signal

        def change_formants(self, shift_factor):
            self.log("Changing Formants")
            D = librosa.stft(self.data)
            D_mag, D_phase = librosa.magphase(D)
            num_bins, num_frames = D_mag.shape
            new_bins = int(num_bins * shift_factor)
            new_D_mag = np.zeros((new_bins, num_frames))
            for i in range(num_frames):
                new_D_mag[:, i] = np.interp(np.linspace(0, num_bins, new_bins),
                                             np.arange(num_bins),
                                             D_mag[:, i])
            if D_phase.shape[0] > new_bins:
                new_D_phase = D_phase[:new_bins, :]
            else:
                pad_width = new_bins - D_phase.shape[0]
                new_D_phase = np.pad(D_phase, ((0, pad_width), (0, 0)), mode='constant')
            D_modified = new_D_mag * new_D_phase
            self.data = librosa.istft(D_modified, length=len(self.data))

        def add_echo(self, delay_time, decay):
            self.log("Adding Echo")
            delay_samples = int(self.sample_rate * delay_time)
            echo_signal = np.zeros_like(self.data)
            if delay_samples < len(self.data):
                echo_signal[delay_samples:] = self.data[:-delay_samples] * decay
            self.data = self.data + echo_signal

        def add_distortion(self, gain, threshold):
            self.log("Applying Distortion")
            distorted = self.data * gain
            distorted = np.clip(distorted, -threshold, threshold)
            max_val = np.max(np.abs(distorted))
            if max_val > 0:
                distorted = distorted / max_val
            self.data = distorted

    def process(self, audio, effect_presets):
        self.log("Starting VoiceEffects2 processing...")

        # Validate input audio dictionary
        if not isinstance(audio, dict):
            self.log("Error: Input audio is not a dictionary")
            raise ValueError("Input audio must be a dictionary")
        if "waveform" not in audio:
            self.log("Error: Input audio missing 'waveform' key")
            raise ValueError("Input audio must contain 'waveform' key")
        if audio["waveform"] is None:
            self.log("Error: Input audio waveform is None")
            raise ValueError("Input audio waveform cannot be None")

        sample_rate = audio.get("sample_rate", 44100)
        self.log(f"Using sample rate: {sample_rate}")

        # Convert waveform to numpy array with shape [batch, channels, samples]
        waveform = audio["waveform"]
        if isinstance(waveform, torch.Tensor):
            if waveform.dim() == 1:
                waveform = waveform.view(1, 1, -1)
            elif waveform.dim() == 2:
                if waveform.shape[0] <= 8:
                    waveform = waveform.unsqueeze(0)
                else:
                    waveform = waveform.unsqueeze(1)
            elif waveform.dim() == 3 and waveform.shape[1] > waveform.shape[2]:
                waveform = waveform.transpose(1, 2)
            audio_data = waveform.cpu().numpy()
        else:
            audio_data = np.array(waveform)
            if audio_data.ndim == 1:
                audio_data = audio_data.reshape(1, 1, -1)
            elif audio_data.ndim == 2:
                if audio_data.shape[0] <= 8:
                    audio_data = np.expand_dims(audio_data, 0)
                else:
                    audio_data = np.expand_dims(audio_data, 1)
            elif audio_data.ndim == 3 and audio_data.shape[1] > audio_data.shape[2]:
                audio_data = np.transpose(audio_data, (0, 2, 1))
        self.log(f"Audio data shape after conversion: {audio_data.shape}")

        # Copy audio data for processing
        processed = audio_data.copy()
        batch_size = processed.shape[0]

        # Build the path for the selected preset file from voice-effects/ folder
        current_dir = os.path.dirname(__file__)
        preset_path = os.path.join(current_dir, "voice-effects", effect_presets)
        if not os.path.isfile(preset_path):
            self.log(f"Error: Preset file {preset_path} does not exist")
            raise ValueError(f"Preset file {effect_presets} not found")
        try:
            with open(preset_path, 'r') as f:
                preset_code = f.read()
        except Exception as e:
            self.log(f"Error reading preset file: {str(e)}")
            raise e

        # Process each channel in each batch using the preset
        for b in range(batch_size):
            for c in range(processed[b].shape[0]):
                self.log(f"Processing batch {b} channel {c}, original shape: {processed[b][c].shape}")
                channel_data = processed[b][c].copy()
                executor = self.EffectsExecutor(channel_data, sample_rate, self.log)
                # Execute the preset code in an environment where "effects" is the executor.
                exec(preset_code, {"effects": executor, "np": np, "signal": signal, "librosa": librosa})
                processed[b][c] = executor.data
                self.log(f"Finished processing batch {b} channel {c}")

        # Normalize processed audio
        max_val = np.max(np.abs(processed))
        self.log(f"Maximum absolute value before normalization: {max_val}")
        if max_val > 0:
            processed = processed / max_val
        else:
            self.log("Warning: Maximum value is 0; skipping normalization")

        # Convert processed data to torch tensor
        try:
            processed_tensor = torch.from_numpy(processed).float()
            self.log(f"Converted processed audio to tensor with shape {processed_tensor.shape}")
        except Exception as e:
            self.log(f"Error converting to tensor: {str(e)}")
            raise ValueError("Tensor conversion failed")

        if processed_tensor.dim() == 2:
            processed_tensor = processed_tensor.unsqueeze(1)
        elif processed_tensor.dim() == 3 and processed_tensor.shape[1] > processed_tensor.shape[2]:
            processed_tensor = processed_tensor.transpose(1, 2)
        processed_tensor = processed_tensor.contiguous().detach()

        result = {
            "waveform": processed_tensor,
            "sample_rate": sample_rate,
            "path": None
        }
        self.log("VoiceEffects2 processing complete. Returning final output.")
        return (result,)

NODE_CLASS_MAPPINGS = {
    "VoiceEffects2": VoiceEffects2
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "VoiceEffects2": "🎤 Voice Effects 2"
}

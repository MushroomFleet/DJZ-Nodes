import numpy as np
import torch
import scipy.signal as signal
import librosa
import json
import os
import glob
import sys

class VoiceEffects:
    def __init__(self):
        self.type = "VoiceEffects"
        self.output_type = "AUDIO"
        self.output_dims = 1
        self.compatible_decorators = []
        self.required_extensions = []
        self.category = "Audio"
        self.name = "Voice Effects Processor"
        self.description = "Applies various voice effects including reverb, filtering, vibrato, formant shifting, echo, and distortion"
        # Setup logging file in same directory
        self.log_file = os.path.join(os.path.dirname(__file__), 'voice_effects.log')

    def log(self, message):
        """Log message to file and stderr"""
        print(message, file=sys.stderr)
        with open(self.log_file, 'a') as f:
            f.write(message + '\n')

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "audio": ("AUDIO",),
                # Reverb parameters
                "room_size": ("FLOAT", {
                    "default": 0.1,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.1
                }),
                "damping": ("FLOAT", {
                    "default": 0.1,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.1
                }),
                # Frequency filter parameters
                "cutoff_freq": ("FLOAT", {
                    "default": 300,
                    "min": 300,
                    "max": 5000,
                    "step": 100
                }),
                "filter_type": (["lowpass", "highpass", "bandpass"],),
                # Vibrato parameters
                "vibrato_freq": ("FLOAT", {
                    "default": 1.0,
                    "min": 1.0,
                    "max": 10.0,
                    "step": 0.5
                }),
                "vibrato_depth": ("FLOAT", {
                    "default": 0.1,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.1
                }),
                # Formant shifting
                "shift_factor": ("FLOAT", {
                    "default": 0.5,
                    "min": 0.5,
                    "max": 2.0,
                    "step": 0.1
                }),
                # Echo parameters
                "delay_time": ("FLOAT", {
                    "default": 0.1,
                    "min": 0.1,
                    "max": 1.0,
                    "step": 0.1
                }),
                "decay": ("FLOAT", {
                    "default": 0.3,
                    "min": 0.1,
                    "max": 1.0,
                    "step": 0.1
                }),
                # Distortion parameters
                "gain": ("FLOAT", {
                    "default": 1.0,
                    "min": 1.0,
                    "max": 5.0,
                    "step": 0.1
                }),
                "threshold": ("FLOAT", {
                    "default": 0.1,
                    "min": 0.1,
                    "max": 1.0,
                    "step": 0.1
                })
            }
        }

    RETURN_TYPES = ("AUDIO",)
    RETURN_NAMES = ("audio",)
    FUNCTION = "process"

    def process(self, audio, room_size, damping, cutoff_freq, filter_type,
                vibrato_freq, vibrato_depth, shift_factor,
                delay_time, decay, gain, threshold):
        """Process audio by applying various voice effects"""
        self.log("Starting voice effects processing...")

        # Validate input audio
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

        # Process waveform, converting to numpy array with proper shape [batch, channels, samples]
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

        # Process each effect on each batch and channel
        processed = audio_data.copy()

        # Define effect functions
        def apply_reverb(x):
            self.log("Applying Reverb")
            reverb_len = int(sample_rate * room_size)
            impulse = np.exp(-damping * np.linspace(0, reverb_len, reverb_len))
            # Pad impulse if shorter than signal length
            if len(impulse) < len(x):
                impulse = np.pad(impulse, (0, len(x) - len(impulse)), mode='constant')
            reverb_signal = signal.convolve(x, impulse, mode='same')
            return 0.6 * x + 0.4 * reverb_signal

        def apply_frequency_filter(x):
            self.log("Applying Frequency Filter")
            nyquist = sample_rate / 2
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
                return x
            return signal.filtfilt(b, a, x)

        def add_vibrato(x):
            self.log("Adding Vibrato")
            t = np.arange(len(x)) / sample_rate
            mod = vibrato_depth * np.sin(2 * np.pi * vibrato_freq * t)
            delay_samples = (mod * sample_rate).astype(int)
            vibrato_signal = np.zeros_like(x)
            for i in range(len(x)):
                index = i - delay_samples[i]
                if 0 <= index < len(x):
                    vibrato_signal[i] = x[index]
            return vibrato_signal

        def change_formants(x):
            self.log("Changing Formants")
            # Use librosa's STFT, interpolate magnitude, then invert
            D = librosa.stft(x)
            D_mag, D_phase = librosa.magphase(D)
            # Stretch magnitude horizontally by shift_factor
            num_bins, num_frames = D_mag.shape
            new_bins = int(num_bins * shift_factor)
            new_D_mag = np.zeros((new_bins, num_frames))
            for i in range(num_frames):
                new_D_mag[:, i] = np.interp(np.linspace(0, num_bins, new_bins),
                                             np.arange(num_bins),
                                             D_mag[:, i])
            # Resize phase to match new magnitude shape
            # For simplicity, trim or pad phase to new_bins
            if D_phase.shape[0] > new_bins:
                new_D_phase = D_phase[:new_bins, :]
            else:
                pad_width = new_bins - D_phase.shape[0]
                new_D_phase = np.pad(D_phase, ((0, pad_width), (0, 0)), mode='constant')
            D_modified = new_D_mag * new_D_phase
            return librosa.istft(D_modified, length=len(x))

        def add_echo(x):
            self.log("Adding Echo")
            delay_samples = int(sample_rate * delay_time)
            echo_signal = np.zeros_like(x)
            if delay_samples < len(x):
                echo_signal[delay_samples:] = x[:-delay_samples] * decay
            return x + echo_signal

        def add_distortion(x):
            self.log("Applying Distortion")
            distorted = x * gain
            distorted = np.clip(distorted, -threshold, threshold)
            max_val = np.max(np.abs(distorted))
            if max_val > 0:
                distorted = distorted / max_val
            return distorted

        # Apply each effect on every channel of every batch
        batch_size = processed.shape[0]
        for b in range(batch_size):
            for c in range(processed[b].shape[0]):
                channel_audio = processed[b][c].copy()
                self.log(f"Processing batch {b} channel {c}, original shape: {channel_audio.shape}")
                # Apply effects sequentially
                channel_audio = apply_reverb(channel_audio)
                channel_audio = apply_frequency_filter(channel_audio)
                channel_audio = add_vibrato(channel_audio)
                channel_audio = change_formants(channel_audio)
                channel_audio = add_echo(channel_audio)
                channel_audio = add_distortion(channel_audio)
                processed[b][c] = channel_audio
                self.log(f"Finished processing batch {b} channel {c}")

        # Normalize processed audio
        max_val = np.max(np.abs(processed))
        self.log(f"Maximum absolute value before normalization: {max_val}")
        if max_val > 0:
            processed = processed / max_val
        else:
            self.log("Warning: Maximum value is 0; skipping normalization")

        # Convert to torch tensor
        try:
            processed_tensor = torch.from_numpy(processed).float()
            self.log(f"Converted processed audio to tensor with shape {processed_tensor.shape}")
        except Exception as e:
            self.log(f"Error converting to tensor: {str(e)}")
            raise ValueError("Tensor conversion failed")

        # Ensure tensor has [batch, channels, samples] shape formatting for ComfyUI
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
        self.log("Voice effects processing complete. Returning final output.")
        return (result,)

NODE_CLASS_MAPPINGS = {
    "VoiceEffects": VoiceEffects
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "VoiceEffects": "🎤 Voice Effects"
}

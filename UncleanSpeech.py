import numpy as np
import torch
import scipy.signal as signal
import json
import os
import glob
import types
import sys

class PresetLoader:
    @staticmethod
    def load_preset_file(file_path):
        """Load a .preset file containing audio effect parameters"""
        try:
            with open(file_path, 'r') as f:
                preset = json.load(f)
            return preset
        except Exception as e:
            print(f"Error loading preset {file_path}: {str(e)}")
            return None

class UncleanSpeech:
    def __init__(self):
        self.type = "UncleanSpeech"
        self.output_type = "AUDIO"
        self.output_dims = 1
        self.compatible_decorators = []
        self.required_extensions = []
        self.category = "Audio"
        self.name = "Unclean Speech Processor"
        self.description = "Applies various audio effects to emulate different audio systems and environments"
        self.presets = {}
        self.load_presets()
        
        # Setup logging
        self.log_file = os.path.join(os.path.dirname(__file__), 'unclean_speech.log')
        
    def log(self, message):
        """Log message to file and console"""
        print(message, file=sys.stderr)
        with open(self.log_file, 'a') as f:
            f.write(message + '\n')
        
    def load_presets(self):
        """Load all .preset files from the PRESETS directory"""
        # Get the directory where the node file is located
        node_dir = os.path.dirname(os.path.abspath(__file__))
        # Look for a 'presets' folder (case-insensitive)
        preset_dir = os.path.join(node_dir, 'presets')
        if not os.path.exists(preset_dir):
            os.makedirs(preset_dir)
            print(f"Created presets directory at: {preset_dir}")
            
        preset_files = glob.glob(os.path.join(preset_dir, '*.preset'))
        
        for preset_file in preset_files:
            try:
                preset = PresetLoader.load_preset_file(preset_file)
                if preset is not None:
                    preset_name = os.path.splitext(os.path.basename(preset_file))[0]
                    self.presets[preset_name] = preset
                    print(f"Successfully loaded preset: {preset_name}")
            except Exception as e:
                print(f"Error loading preset {preset_file}: {str(e)}")
                
        if not preset_files:
            print(f"No preset files found in: {preset_dir}")

    @classmethod
    def INPUT_TYPES(cls):
        """Define input parameters for the node"""
        # Load available presets
        preset_dir = os.path.join(os.path.dirname(__file__), 'PRESETS')
        preset_files = glob.glob(os.path.join(preset_dir, '*.preset'))
        preset_names = [os.path.splitext(os.path.basename(f))[0] for f in preset_files]
        
        if not preset_names:
            preset_names = ["none"]
            
        return {
            "required": {
                "audio": ("AUDIO",),
                "preset": (preset_names,),
                # Basic Effects
                "compression_ratio": ("FLOAT", {
                    "default": 1.0,
                    "min": 1.0,
                    "max": 20.0,
                    "step": 0.1
                }),
                "compression_threshold": ("FLOAT", {
                    "default": -20.0,
                    "min": -60.0,
                    "max": 0.0,
                    "step": 0.1
                }),
                # EQ Parameters
                "low_cut": ("FLOAT", {
                    "default": 20.0,
                    "min": 20.0,
                    "max": 2000.0,
                    "step": 1.0
                }),
                "high_cut": ("FLOAT", {
                    "default": 20000.0,
                    "min": 1000.0,
                    "max": 20000.0,
                    "step": 1.0
                }),
                # Distortion
                "distortion_amount": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01
                }),
                # Noise
                "noise_level": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01
                }),
                "noise_color": (["white", "pink", "brown"],),
                # Reverb
                "reverb_amount": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01
                }),
                "room_size": ("FLOAT", {
                    "default": 0.5,
                    "min": 0.1,
                    "max": 1.0,
                    "step": 0.01
                })
            }
        }

    RETURN_TYPES = ("AUDIO", )
    RETURN_NAMES = ("audio", )
    FUNCTION = "process"

    def apply_compression(self, audio, ratio, threshold):
        """Apply compression effect to audio"""
        try:
            # Convert threshold from dB to linear
            threshold_linear = 10 ** (threshold / 20.0)
            
            # Calculate gain reduction
            gain_reduction = np.where(
                np.abs(audio) > threshold_linear,
                (np.abs(audio) / threshold_linear) ** (1/ratio - 1),
                1.0
            )
            
            return audio * gain_reduction
        except Exception as e:
            self.log(f"Error in compression: {str(e)}")
            raise

    def apply_eq(self, audio, sample_rate, low_cut, high_cut):
        """Apply EQ filtering"""
        try:
            nyquist = sample_rate / 2
            low_cut_norm = low_cut / nyquist
            high_cut_norm = high_cut / nyquist
            
            # Design and apply bandpass filter
            b, a = signal.butter(4, [low_cut_norm, high_cut_norm], btype='band')
            return signal.filtfilt(b, a, audio)
        except Exception as e:
            self.log(f"Error in EQ: {str(e)}")
            raise

    def apply_distortion(self, audio, amount):
        """Apply distortion effect"""
        try:
            if amount == 0:
                return audio
                
            # Soft clipping distortion
            return np.tanh(audio * (1 + amount * 10)) / (1 + amount)
        except Exception as e:
            self.log(f"Error in distortion: {str(e)}")
            raise

    def generate_noise(self, samples, noise_type, level):
        """Generate various types of noise"""
        try:
            if level == 0:
                return np.zeros(samples)
                
            # Generate base noise
            noise = np.random.normal(0, 1, samples)
            
            if noise_type == "pink":
                # Generate pink noise using 1/f filter
                f = np.fft.fftfreq(len(noise))
                f[0] = float('inf')  # Avoid divide by zero
                pink_filter = 1 / np.sqrt(np.abs(f))
                noise_fft = np.fft.fft(noise)
                noise = np.real(np.fft.ifft(noise_fft * pink_filter))
            elif noise_type == "brown":
                # Generate brown noise using cumulative sum
                noise = np.cumsum(noise)
                    
            # Normalize noise
            noise = noise - np.mean(noise)
            if np.max(np.abs(noise)) > 0:  # Avoid division by zero
                noise = noise / np.max(np.abs(noise))
                
            return noise * level
        except Exception as e:
            self.log(f"Error in noise generation: {str(e)}")
            raise

    def apply_reverb(self, audio, sample_rate, amount, room_size):
        """Apply simple reverb effect to a single channel"""
        try:
            if amount == 0:
                return audio
                
            # Create simple impulse response
            delay_samples = int(room_size * sample_rate * 0.1)  # 100ms max delay
            ir = np.zeros(delay_samples)
            num_reflections = 8
            for i in range(num_reflections):
                pos = int((i / num_reflections) * delay_samples)
                ir[pos] = 0.7 ** i
            
            # Normalize IR
            if np.sum(ir) > 0:  # Avoid division by zero
                ir = ir / np.sum(ir)
            
            # Apply convolution reverb
            wet = signal.convolve(audio, ir, mode='same')
            return (1 - amount) * audio + amount * wet
        except Exception as e:
            self.log(f"Error in reverb: {str(e)}")
            raise

    def process(self, audio, preset, compression_ratio, compression_threshold, 
               low_cut, high_cut, distortion_amount, noise_level, noise_color,
               reverb_amount, room_size):
        """Process audio with all effects"""
        from tqdm import tqdm
        print(f"\nApplying {preset} preset to audio...")
        
        # Validate input audio with detailed logging
        self.log("\nValidating input audio...")
        
        if not isinstance(audio, dict):
            self.log("Error: Input audio is not a dictionary")
            raise ValueError("Input audio must be a dictionary")
            
        self.log(f"Input audio keys: {list(audio.keys())}")
        
        if 'waveform' not in audio:
            self.log("Error: Input audio missing 'waveform' key")
            raise ValueError("Input audio must contain 'waveform' key")
            
        if audio['waveform'] is None:
            self.log("Error: Input audio waveform is None")
            raise ValueError("Input audio waveform cannot be None")
            
        sample_rate = audio.get('sample_rate', 44100)
        self.log(f"Using sample rate: {sample_rate}")
        
        # Get waveform and ensure it's the right shape
        self.log("\nProcessing waveform...")
        waveform = audio['waveform']
        
        if waveform is None:
            self.log("Error: Waveform is None")
            raise ValueError("Input audio waveform is None")
            
        self.log(f"Waveform type: {type(waveform)}")
        if isinstance(waveform, torch.Tensor):
            self.log(f"Tensor shape: {waveform.shape}, dimensions: {waveform.dim()}")
            self.log("Converting tensor to numpy array")
            # Ensure tensor has correct shape [batch, channels, samples]
            if waveform.dim() == 1:  # [samples]
                waveform = waveform.view(1, 1, -1)  # Add batch and channel dimensions
            elif waveform.dim() == 2:  # [channels, samples] or [batch, samples]
                if waveform.shape[0] <= 8:  # Assume it's [channels, samples] if first dim is small
                    waveform = waveform.unsqueeze(0)  # Add batch dimension
                else:  # Assume it's [batch, samples]
                    waveform = waveform.unsqueeze(1)  # Add channel dimension
            elif waveform.dim() == 3:
                # Already has batch dimension, ensure [batch, channels, samples] order
                if waveform.shape[1] > waveform.shape[2]:
                    waveform = waveform.transpose(1, 2)
            # Validate shape
            if waveform.dim() != 3:
                raise ValueError(f"Expected 3D tensor after reshaping, got {waveform.dim()}D")
            self.log(f"Tensor shape after reshaping: {waveform.shape} [batch, channels, samples]")
            
            # Convert to numpy while maintaining shape
            audio_data = waveform.cpu().numpy()
            self.log(f"Audio data shape after conversion: {audio_data.shape}")
        else:
            self.log("Converting non-tensor waveform to numpy array")
            audio_data = np.array(waveform)
            # Ensure we have [batch, channels, samples] shape
            if audio_data.ndim == 1:  # [samples]
                audio_data = audio_data.reshape(1, 1, -1)  # Add batch and channel dimensions
            elif audio_data.ndim == 2:  # [channels, samples] or [batch, samples]
                if audio_data.shape[0] <= 8:  # Assume it's [channels, samples] if first dim is small
                    audio_data = np.expand_dims(audio_data, 0)  # Add batch dimension
                else:  # Assume it's [batch, samples]
                    audio_data = np.expand_dims(audio_data, 1)  # Add channel dimension
            elif audio_data.ndim == 3 and audio_data.shape[1] > audio_data.shape[2]:
                audio_data = np.transpose(audio_data, (0, 2, 1))  # Fix channel/sample order if needed
            
        self.log(f"Audio data shape after conversion and reshaping: {audio_data.shape}")
            
        # Convert to numpy if needed and validate
        if isinstance(audio_data, torch.Tensor):
            self.log("Converting remaining tensor to numpy")
            audio_data = audio_data.numpy()
            
        if audio_data is None or audio_data.size == 0:
            self.log("Error: Audio data is None or empty after conversion")
            raise ValueError("Failed to convert audio data to numpy array")
            
        self.log(f"Audio data type: {type(audio_data)}, shape: {audio_data.shape}")
        
        # Ensure audio_data has the right shape
        if len(audio_data.shape) < 2:
            self.log(f"Reshaping audio data from {audio_data.shape} to (1, -1)")
            audio_data = audio_data.reshape(1, -1)
            self.log(f"New audio data shape: {audio_data.shape}")
        
        try:
            # Load preset if specified
            self.log(f"\nLoading preset: {preset}")
            if preset in self.presets:
                preset_data = self.presets[preset]
                self.log(f"Found preset data: {preset_data}")
                
                # Override parameters with preset values
                original_params = {
                    'compression_ratio': compression_ratio,
                    'compression_threshold': compression_threshold,
                    'low_cut': low_cut,
                    'high_cut': high_cut,
                    'distortion_amount': distortion_amount,
                    'noise_level': noise_level,
                    'noise_color': noise_color,
                    'reverb_amount': reverb_amount,
                    'room_size': room_size
                }
                
                # Update parameters and log changes
                compression_ratio = preset_data.get('compression_ratio', compression_ratio)
                compression_threshold = preset_data.get('compression_threshold', compression_threshold)
                low_cut = preset_data.get('low_cut', low_cut)
                high_cut = preset_data.get('high_cut', high_cut)
                distortion_amount = preset_data.get('distortion_amount', distortion_amount)
                noise_level = preset_data.get('noise_level', noise_level)
                noise_color = preset_data.get('noise_color', noise_color)
                reverb_amount = preset_data.get('reverb_amount', reverb_amount)
                room_size = preset_data.get('room_size', room_size)
                
                # Log parameter changes
                new_params = {
                    'compression_ratio': compression_ratio,
                    'compression_threshold': compression_threshold,
                    'low_cut': low_cut,
                    'high_cut': high_cut,
                    'distortion_amount': distortion_amount,
                    'noise_level': noise_level,
                    'noise_color': noise_color,
                    'reverb_amount': reverb_amount,
                    'room_size': room_size
                }
                
                for param_name in original_params:
                    if original_params[param_name] != new_params[param_name]:
                        self.log(f"Parameter {param_name} changed from {original_params[param_name]} to {new_params[param_name]}")
            else:
                self.log(f"No preset found for {preset}, using default parameters")
            
            # Define effects chain
            effects = [
                ("Compression", lambda x: self.apply_compression(x, compression_ratio, compression_threshold)),
                ("EQ", lambda x: self.apply_eq(x, sample_rate, low_cut, high_cut)),
                ("Distortion", lambda x: self.apply_distortion(x, distortion_amount)),
                ("Noise", lambda x: x + self.generate_noise(x.shape[-1], noise_color, noise_level)),
                ("Reverb", lambda x: self.apply_reverb(x, sample_rate, reverb_amount, room_size))
            ]
            
            # Apply effects chain with progress bar
            processed = audio_data.copy()
            with tqdm(effects, desc="Applying effects", unit="effect") as pbar:
                for effect_name, effect_func in pbar:
                    pbar.set_description(f"Applying {effect_name}")
                    self.log(f"Applying effect: {effect_name}")
                    self.log(f"Audio shape before {effect_name}: {processed.shape}")
                    
                    # Process each batch and channel separately
                    batch_size = processed.shape[0]
                    processed_batches = []
                    for batch_idx in range(batch_size):
                        batch_audio = processed[batch_idx]  # [channels, samples]
                        # Process each channel
                        processed_channels = []
                        for channel_idx in range(batch_audio.shape[0]):
                            channel_audio = batch_audio[channel_idx]  # [samples]
                            # Ensure channel_audio is 1D
                            channel_audio = channel_audio.reshape(-1)
                            processed_channel = effect_func(channel_audio)
                            # Ensure processed_channel is 1D
                            processed_channel = np.asarray(processed_channel).reshape(-1)
                            processed_channels.append(processed_channel)
                        processed_batch = np.stack(processed_channels)  # [channels, samples]
                        processed_batches.append(processed_batch)
                    processed = np.stack(processed_batches)  # [batch, channels, samples]
                    self.log(f"Processed shape: {processed.shape}")
                    
                    # Validate after each effect
                    if processed is None:
                        self.log(f"Error: {effect_name} effect returned None")
                        raise ValueError(f"Effect {effect_name} returned None")
                        
                    self.log(f"Audio shape after {effect_name}: {processed.shape}")
            
            # Normalize output
            self.log("\nNormalizing output...")
            max_val = np.max(np.abs(processed))
            self.log(f"Maximum absolute value: {max_val}")
            
            if max_val > 0:
                self.log("Normalizing audio")
                processed = processed / max_val
            else:
                self.log("Warning: Maximum value is 0, skipping normalization")
            
            # Convert to tensor
            self.log("\nConverting to tensor...")
            try:
                processed = torch.from_numpy(processed).float()
                self.log(f"Tensor conversion successful. Shape: {processed.shape}, dtype: {processed.dtype}")
            except Exception as e:
                self.log(f"Error during tensor conversion: {str(e)}")
                raise ValueError(f"Failed to convert processed audio to tensor: {str(e)}")
            
            # Validate processed audio before returning
            if processed is None or processed.size == 0:
                self.log("Error: Processed audio is invalid after tensor conversion")
                raise ValueError("Final processed audio is invalid")
            
            self.log("\nPreparing final output...")
            try:
                # Ensure tensor is in the correct format for ComfyUI: [batch, channels, samples]
                processed = processed.cpu()
                # Ensure correct dimensions and order
                if processed.dim() == 2:  # [batch, samples]
                    processed = processed.unsqueeze(1)  # Add channel dimension
                elif processed.dim() == 3:
                    if processed.shape[1] > processed.shape[2]:
                        processed = processed.transpose(1, 2)
                # Make contiguous and detach from computation graph
                processed_with_batch = processed.contiguous().detach()
                self.log(f"Final tensor shape: {processed_with_batch.shape}, device: {processed_with_batch.device}, contiguous: {processed_with_batch.is_contiguous()}")
                result = {
                    "waveform": processed_with_batch,
                    "sample_rate": sample_rate,
                    "path": None  # Include path field even if not used
                }
                
                # Final validation
                if result["waveform"] is None:
                    self.log("Error: Final waveform is None")
                    raise ValueError("Failed to create output waveform tensor")
                    
                self.log("Successfully created final output")
                # Return tuple to match RETURN_TYPES
                return (result,)
                
            except Exception as e:
                self.log(f"Error preparing final output: {str(e)}")
                raise ValueError(f"Failed to prepare final output: {str(e)}")
            
        except Exception as e:
            self.log(f"Error processing audio: {str(e)}")
            raise  # Re-raise the exception after logging

NODE_CLASS_MAPPINGS = {
    "UncleanSpeech": UncleanSpeech
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "UncleanSpeech": "🎙️ Unclean Speech"
}

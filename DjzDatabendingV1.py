import numpy as np
import torch
import cv2
from PIL import Image
import io
import scipy.signal as signal
import tempfile
import os

class DjzDatabendingV1:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),  # Batch of images input
                "effect_type": (["echo", "reverb", "distortion", "bitcrush", "tremolo", "phaser", "chorus"],),
                "echo_delay": ("FLOAT", {
                    "default": 0.3,
                    "min": 0.1,
                    "max": 1.0,
                    "step": 0.1,
                }),
                "echo_decay": ("FLOAT", {
                    "default": 0.1,
                    "min": 0.0,
                    "max": 0.9,
                    "step": 0.1,
                }),
                "distortion_intensity": ("FLOAT", {
                    "default": 0.5,
                    "min": 0.1,
                    "max": 1.0,
                    "step": 0.1,
                }),
                "modulation_rate": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.1,
                    "max": 10.0,
                    "step": 0.1,
                }),
                "modulation_depth": ("FLOAT", {
                    "default": 0.5,
                    "min": 0.1,
                    "max": 2.0,
                    "step": 0.1,
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "apply_databending"
    CATEGORY = "image/effects"

    def apply_echo(self, audio_data, delay, decay, sample_rate=44100):
        """Apply echo effect to audio data"""
        print(f"Applying echo effect (delay: {delay}, decay: {decay})")
        delay_samples = int(delay * sample_rate)
        echo_filter = np.zeros(delay_samples + 1)
        echo_filter[0] = 1
        echo_filter[-1] = decay
        return signal.convolve(audio_data, echo_filter, mode='same')
        
    def apply_reverb(self, audio_data, depth, decay, sample_rate=44100):
        """Apply reverb effect to audio data"""
        print(f"Applying reverb effect (depth: {depth}, decay: {decay})")
        num_reflections = int(depth * sample_rate)
        decay_curve = np.exp(-decay * np.arange(num_reflections))
        impulse = np.random.rand(num_reflections) * decay_curve
        return signal.convolve(audio_data, impulse, mode='same')
    
    def apply_distortion(self, audio_data, intensity):
        """Apply distortion effect to audio data"""
        print(f"Applying distortion effect (intensity: {intensity})")
        return np.clip(audio_data * (1 + intensity), -1, 1)
    
    def apply_bitcrush(self, audio_data, depth):
        """Apply bit crushing effect to audio data"""
        print(f"Applying bitcrush effect (depth: {depth})")
        bits = int(16 * (1 - depth))  # Convert depth to bits (1-16)
        steps = 2**bits
        return np.round(audio_data * steps) / steps
        
    def apply_tremolo(self, audio_data, rate, depth, sample_rate=44100):
        """Apply tremolo effect to audio data"""
        print(f"Applying tremolo effect (rate: {rate}, depth: {depth})")
        t = np.arange(len(audio_data)) / sample_rate
        mod = depth * np.sin(2 * np.pi * rate * t) + (1 - depth)
        return audio_data * mod
        
    def apply_phaser(self, audio_data, rate, depth, sample_rate=44100):
        """Apply phaser effect to audio data"""
        print(f"Applying phaser effect (rate: {rate}, depth: {depth})")
        t = np.arange(len(audio_data)) / sample_rate
        lfo = (np.sin(2 * np.pi * rate * t) + 1) * depth
        allpass = np.exp(-2j * np.pi * lfo / sample_rate)
        return np.real(audio_data * allpass)
        
    def apply_chorus(self, audio_data, rate, depth, sample_rate=44100):
        """Apply chorus effect to audio data"""
        print(f"Applying chorus effect (rate: {rate}, depth: {depth})")
        t = np.arange(len(audio_data)) / sample_rate
        mod = depth * np.sin(2 * np.pi * rate * t)
        indices = np.arange(len(audio_data)) + (mod * sample_rate).astype(int)
        indices = np.clip(indices, 0, len(audio_data) - 1)
        return 0.5 * (audio_data + audio_data[indices])

    def process_single_image(self, image, effect_type, params):
        """Process a single image with databending effects"""
        print(f"Processing image with {effect_type} effect...")
        
        # Create temporary BMP file
        with tempfile.NamedTemporaryFile(suffix='.bmp', delete=False) as tmp_bmp:
            bmp_path = tmp_bmp.name
            Image.fromarray((image * 255).astype(np.uint8)).save(bmp_path, 'BMP')
        
        print("Converting to raw audio data...")
        # Read BMP header
        with open(bmp_path, 'rb') as f:
            header = f.read(54)  # BMP header size
            audio_data = np.frombuffer(f.read(), dtype=np.uint8).astype(np.float32) / 255.0

        print("Applying audio effect...")
        # Apply selected effect
        if effect_type == "echo":
            processed_audio = self.apply_echo(audio_data, params['delay'], params['decay'])
        elif effect_type == "reverb":
            processed_audio = self.apply_reverb(audio_data, params['depth'], params['decay'])
        elif effect_type == "distortion":
            processed_audio = self.apply_distortion(audio_data, params['intensity'])
        elif effect_type == "bitcrush":
            processed_audio = self.apply_bitcrush(audio_data, params['depth'])
        elif effect_type == "tremolo":
            processed_audio = self.apply_tremolo(audio_data, params['rate'], params['depth'])
        elif effect_type == "phaser":
            processed_audio = self.apply_phaser(audio_data, params['rate'], params['depth'])
        elif effect_type == "chorus":
            processed_audio = self.apply_chorus(audio_data, params['rate'], params['depth'])

        print("Converting back to image...")
        # Convert back to image data
        processed_data = (processed_audio * 255).astype(np.uint8)
        
        # Create new image with original header
        with tempfile.NamedTemporaryFile(suffix='.bmp', delete=False) as tmp_out:
            tmp_out.write(header)
            tmp_out.write(processed_data.tobytes())
            
        # Read processed image
        processed_image = np.array(Image.open(tmp_out.name)).astype(np.float32) / 255.0
        
        # Cleanup temporary files
        os.unlink(bmp_path)
        os.unlink(tmp_out.name)
        
        return processed_image

    def apply_databending(self, images, effect_type, echo_delay, echo_decay, distortion_intensity, modulation_rate, modulation_depth):
        """Process batch of images with databending effects"""
        print(f"\nStarting databending process with {effect_type} effect...")
        
        # Convert from torch tensor to numpy array
        batch_numpy = images.cpu().numpy()
        batch_size = batch_numpy.shape[0]
        
        # Prepare parameters
        params = {
            'delay': echo_delay,
            'decay': echo_decay,
            'intensity': distortion_intensity,
            'rate': modulation_rate,
            'depth': modulation_depth
        }
        
        # Process each image in the batch
        processed_batch = np.zeros_like(batch_numpy)
        for i in range(batch_size):
            print(f"\nProcessing image {i+1}/{batch_size}")
            processed_batch[i] = self.process_single_image(batch_numpy[i], effect_type, params)
        
        print("\nDatabending process complete!")
        return (torch.from_numpy(processed_batch).to(images.device),)

NODE_CLASS_MAPPINGS = {
    "DjzDatabendingV1": DjzDatabendingV1
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DjzDatabendingV1": "Databending Effect v1"
}
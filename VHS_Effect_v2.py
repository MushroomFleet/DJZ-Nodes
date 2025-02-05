import numpy as np
import torch
import cv2
from scipy.signal import lfilter
from enum import Enum
import math
import os

class VHSSpeed(Enum):
    VHS_SP = (2400000.0, 320000.0, 9)
    VHS_LP = (1900000.0, 300000.0, 12)
    VHS_EP = (1400000.0, 280000.0, 14)
    
    def __init__(self, luma_cut, chroma_cut, chroma_delay):
        self.luma_cut = luma_cut
        self.chroma_cut = chroma_cut
        self.chroma_delay = chroma_delay

class VHS_Effect_v2:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),
                "composite_preemphasis": ("FLOAT", {
                    "default": 4.0,
                    "min": 0.0,
                    "max": 8.0,
                    "step": 0.1
                }),
                "vhs_out_sharpen": ("FLOAT", {
                    "default": 2.5,
                    "min": 1.0,
                    "max": 5.0,
                    "step": 0.1
                }),
                "color_bleeding": ("FLOAT", {
                    "default": 5.0,
                    "min": 0.0,
                    "max": 10.0,
                    "step": 0.1
                }),
                "video_noise": ("FLOAT", {
                    "default": 1000.0,
                    "min": 0.0,
                    "max": 4200.0,
                    "step": 1.0
                }),
                "chroma_noise": ("FLOAT", {
                    "default": 5000.0,
                    "min": 0.0,
                    "max": 16384.0,
                    "step": 1.0
                }),
                "chroma_phase_noise": ("FLOAT", {
                    "default": 25.0,
                    "min": 0.0,
                    "max": 50.0,
                    "step": 1.0
                }),
                "enable_ringing": ("BOOLEAN", {"default": True}),
                "ringing_power": ("INT", {
                    "default": 2,
                    "min": 2,
                    "max": 7,
                    "step": 1
                }),
                "tape_speed": (["SP", "LP", "EP"],),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "apply_vhs_effect"
    CATEGORY = "image/effects"

    def __init__(self):
        # Find the ringPattern.npy file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ring_pattern_path = os.path.join(current_dir, 'ringPattern.npy')
        
        try:
            self.ring_pattern = np.load(ring_pattern_path)
            print(f"Loaded ring pattern from: {ring_pattern_path}")
        except Exception as e:
            print(f"Could not load ringPattern.npy: {e}")
            print("Using fallback pattern")
            self.ring_pattern = self.generate_ring_pattern()
        
        self.ntsc_rate = 315000000.00 / 88 * 4

    def generate_ring_pattern(self, size=720):
        x = np.linspace(0, 2*np.pi, size)
        pattern = np.sin(x * 4) * np.exp(-x/4)
        pattern = (pattern - pattern.min()) / (pattern.max() - pattern.min())
        pattern += 0.3 * np.sin(x * 8) * np.exp(-x/2)
        pattern = (pattern - pattern.min()) / (pattern.max() - pattern.min())
        return pattern.astype(np.float32)

    def bgr2yiq(self, bgrimg):
        bgrimg_float = bgrimg.astype(np.float32)
        planar = np.transpose(bgrimg_float, (2, 0, 1))
        b, g, r = planar
        
        # Standard YIQ conversion matrix
        Y = 0.299 * r + 0.587 * g + 0.114 * b
        I = 0.596 * r - 0.274 * g - 0.322 * b
        Q = 0.211 * r - 0.523 * g + 0.312 * b
        
        return np.stack([Y, I, Q], axis=0)

    def yiq2bgr(self, yiq):
        Y, I, Q = [ch.astype(np.float32) for ch in yiq]
        
        # Standard YIQ to RGB conversion matrix
        r = Y + 0.956 * I + 0.619 * Q
        g = Y - 0.272 * I - 0.647 * Q
        b = Y - 1.105 * I + 1.702 * Q
        
        rgb = np.stack([b, g, r], axis=2)
        return np.clip(rgb, 0, 255).astype(np.uint8)

    def apply_vhs_noise(self, yiq, noise_amount):
        Y, I, Q = yiq
        if noise_amount > 0:
            noise = np.random.normal(0, noise_amount/100, Y.shape).astype(np.float32)
            kernel_size = 3
            noise = cv2.GaussianBlur(noise, (kernel_size, kernel_size), 0)
            Y = Y + noise
        return np.stack([Y, I, Q])

    def apply_chroma_noise(self, yiq, noise_amount, phase_noise):
        Y, I, Q = [ch.astype(np.float32) for ch in yiq]
        
        if noise_amount > 0:
            noise_i = np.random.normal(0, noise_amount/100, I.shape).astype(np.float32)
            noise_q = np.random.normal(0, noise_amount/100, Q.shape).astype(np.float32)
            kernel_size = 3
            noise_i = cv2.GaussianBlur(noise_i, (kernel_size, kernel_size), 0)
            noise_q = cv2.GaussianBlur(noise_q, (kernel_size, kernel_size), 0)
            I += noise_i
            Q += noise_q
        
        if phase_noise > 0:
            angle = np.random.normal(0, phase_noise/10, I.shape) * np.pi / 180
            i_new = I * np.cos(angle) - Q * np.sin(angle)
            q_new = I * np.sin(angle) + Q * np.cos(angle)
            I, Q = i_new, q_new
        
        return np.stack([Y, I, Q])

    def apply_color_bleeding(self, yiq, amount):
        Y, I, Q = [ch.astype(np.float32) for ch in yiq]
        
        if amount > 0:
            kernel_size = int(amount * 2) + 1
            kernel = np.ones(kernel_size) / kernel_size
            
            I = lfilter(kernel, 1, I)
            Q = lfilter(kernel, 1, Q)
            
            if kernel_size > 1:
                I = cv2.GaussianBlur(I, (1, kernel_size), 0)
                Q = cv2.GaussianBlur(Q, (1, kernel_size), 0)
        
        return np.stack([Y, I, Q])

    def apply_tape_speed_effects(self, yiq, speed):
        Y, I, Q = [ch.astype(np.float32) for ch in yiq]
        
        kernel_size = {
            VHSSpeed.VHS_SP: 3,
            VHSSpeed.VHS_LP: 5,
            VHSSpeed.VHS_EP: 7
        }[speed]
        
        if kernel_size > 1:
            Y = cv2.GaussianBlur(Y, (kernel_size, 1), 0)
            I = cv2.GaussianBlur(I, (kernel_size, 1), 0)
            Q = cv2.GaussianBlur(Q, (kernel_size, 1), 0)
        
        return np.stack([Y, I, Q])

    def apply_ringing(self, yiq, power):
        Y, I, Q = [ch.astype(np.float32) for ch in yiq]
        rows, cols = Y.shape
        
        for idx, channel in enumerate([Y, I, Q]):
            dft = cv2.dft(channel, flags=cv2.DFT_COMPLEX_OUTPUT)
            dft_shift = np.fft.fftshift(dft)
            
            mask = np.reshape(self.ring_pattern ** power, (1, -1))
            mask = cv2.resize(mask, (cols, 1))
            mask = np.repeat(mask, rows, axis=0)
            
            dft_shift *= mask[:, :, np.newaxis]
            img_back = cv2.idft(np.fft.ifftshift(dft_shift), flags=cv2.DFT_SCALE)
            if idx == 0:
                Y = img_back[:, :, 0]
            elif idx == 1:
                I = img_back[:, :, 0]
            else:
                Q = img_back[:, :, 0]
        
        return np.stack([Y, I, Q])

    def process_frame(self, frame, params):
        frame = frame.astype(np.float32)
        yiq = self.bgr2yiq(frame)
        
        if params["enable_ringing"]:
            yiq = self.apply_ringing(yiq, params["ringing_power"])
        
        yiq = self.apply_vhs_noise(yiq, params["video_noise"])
        yiq = self.apply_chroma_noise(yiq, params["chroma_noise"], params["chroma_phase_noise"])
        yiq = self.apply_color_bleeding(yiq, params["color_bleeding"])
        yiq = self.apply_tape_speed_effects(yiq, params["tape_speed"])
        
        result = self.yiq2bgr(yiq)
        
        if params["vhs_out_sharpen"] > 1.0:
            result = result.astype(np.float32)
            kernel_size = (3, 3)
            sigma = 1.0
            alpha = params["vhs_out_sharpen"]
            beta = -(alpha - 1.0)
            
            blurred = cv2.GaussianBlur(result, kernel_size, sigma)
            result = cv2.addWeighted(result, alpha, blurred, beta, 0)
        
        return np.clip(result, 0, 255).astype(np.uint8)

    def apply_vhs_effect(self, images, composite_preemphasis, vhs_out_sharpen, 
                        color_bleeding, video_noise, chroma_noise, chroma_phase_noise,
                        enable_ringing, ringing_power, tape_speed):
        
        batch_numpy = images.cpu().numpy()
        batch_size, height, width, channels = batch_numpy.shape
        
        params = {
            "composite_preemphasis": composite_preemphasis,
            "vhs_out_sharpen": vhs_out_sharpen,
            "color_bleeding": color_bleeding,
            "video_noise": video_noise,
            "chroma_noise": chroma_noise,
            "chroma_phase_noise": chroma_phase_noise,
            "enable_ringing": enable_ringing,
            "ringing_power": ringing_power,
            "tape_speed": getattr(VHSSpeed, f"VHS_{tape_speed}")
        }
        
        processed_batch = np.zeros_like(batch_numpy)
        for i in range(batch_size):
            frame = (batch_numpy[i] * 255).astype(np.uint8)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            
            frame = self.process_frame(frame, params)
            
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            processed_batch[i] = frame.astype(np.float32) / 255.0
        
        return (torch.from_numpy(processed_batch).to(images.device),)

NODE_CLASS_MAPPINGS = {
    "VHS_Effect_v2": VHS_Effect_v2
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "VHS_Effect_v2": "VHS Effect v2"
}
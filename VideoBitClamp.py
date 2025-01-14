import torch
import torch.nn.functional as F
from typing import Tuple, List
import numpy as np

class VideoBitClamp:
    """
    ComfyUI custom node for applying bit depth clamping effects to video frames.
    Simulates lower bit depth color palettes while maintaining smooth gradients
    and offering various dithering options.
    """
    
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "bit_depth": (["8bit", "16bit", "32bit", "64bit", "128bit"], {
                    "default": "8bit"
                }),
                "dithering": (["none", "ordered", "floyd-steinberg"], {
                    "default": "none"
                }),
                "color_space": (["RGB", "YUV"], {
                    "default": "RGB"
                }),
                "preservation": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.05,
                    "display": "slider"
                }),
            },
            "optional": {
                "gamma": ("FLOAT", {
                    "default": 2.2,
                    "min": 1.0,
                    "max": 3.0,
                    "step": 0.1,
                    "display": "slider"
                }),
                "noise_reduction": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.1,
                    "display": "slider"
                }),
                "temporal_coherence": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.1,
                    "display": "slider"
                })
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "apply_bit_clamp"
    CATEGORY = "image/effects"

    def apply_noise_reduction(self, frame: torch.Tensor, strength: float) -> torch.Tensor:
        """
        Applies bilateral filtering for noise reduction while preserving edges.
        """
        if strength == 0:
            return frame
            
        # Convert to YUV for better noise reduction
        rgb_weights = torch.tensor([0.299, 0.587, 0.114], device=self.device)
        yuv_frame = torch.zeros_like(frame)
        
        # Only process Y channel
        y = torch.sum(frame * rgb_weights, dim=-1, keepdim=True)
        
        # Apply bilateral filtering
        sigma_space = strength * 5.0
        sigma_color = strength * 0.1
        
        # Simple bilateral filter implementation
        radius = int(sigma_space * 2)
        filtered = F.avg_pool2d(
            y.permute(2, 0, 1).unsqueeze(0),
            kernel_size=radius*2+1,
            stride=1,
            padding=radius
        ).squeeze(0).permute(1, 2, 0)
        
        # Blend with original based on strength
        return torch.lerp(frame, filtered.repeat(1, 1, 3), strength)

    def apply_ordered_dither(self, frame: torch.Tensor) -> torch.Tensor:
        """
        Applies ordered dithering using a Bayer matrix.
        """
        # 4x4 Bayer matrix
        bayer = torch.tensor([
            [ 0, 8, 2, 10],
            [12, 4, 14, 6],
            [ 3, 11, 1, 9],
            [15, 7, 13, 5]
        ], device=self.device) / 16.0
        
        # Tile the bayer matrix to match frame dimensions
        h, w = frame.shape[:2]
        bayer_tiled = bayer.repeat(
            (h + 3) // 4,
            (w + 3) // 4
        )[:h, :w].unsqueeze(-1)
        
        # Apply dithering
        return (frame + bayer_tiled / (2 * frame.shape[-1])).clamp(0, 1)

    def apply_floyd_steinberg(self, frame: torch.Tensor, levels: int) -> torch.Tensor:
        """
        Applies Floyd-Steinberg dithering.
        """
        result = frame.clone()
        h, w = frame.shape[:2]
        
        for y in range(h-1):
            for x in range(1, w-1):
                old_pixel = result[y, x].clone()
                new_pixel = torch.round(old_pixel * (levels - 1)) / (levels - 1)
                result[y, x] = new_pixel
                
                error = old_pixel - new_pixel
                
                # Distribute error to neighboring pixels
                result[y, x+1] += error * 7/16
                result[y+1, x-1] += error * 3/16
                result[y+1, x] += error * 5/16
                result[y+1, x+1] += error * 1/16
                
        return result.clamp(0, 1)

    def apply_bit_depth(self,
                       frame: torch.Tensor,
                       bit_depth: str,
                       dithering: str,
                       gamma: float) -> torch.Tensor:
        """
        Applies bit depth reduction with optional dithering.
        """
        # Convert bit depth string to actual bits per channel
        bits_map = {
            "8bit": 2,    # 2 bits per channel = 8 levels per channel
            "16bit": 3,   # 3 bits per channel = 16 levels per channel
            "32bit": 4,   # 4 bits per channel = 32 levels per channel
            "64bit": 5,   # 5 bits per channel = 64 levels per channel
            "128bit": 6   # 6 bits per channel = 128 levels per channel
        }
        bits = bits_map[bit_depth]
        levels = 2 ** bits  # This gives us the number of levels per channel
        
        # Apply gamma correction
        frame_gamma = frame.pow(gamma)
        
        if dithering == "none":
            # Direct quantization for each color channel
            frame_gamma = torch.floor(frame_gamma * (levels - 1)) / (levels - 1)
        elif dithering == "ordered":
            frame_gamma = self.apply_ordered_dither(frame_gamma)
        elif dithering == "floyd-steinberg":
            frame_gamma = self.apply_floyd_steinberg(frame_gamma, levels)
        
        # Quantize to target bit depth (for dithered versions)
        if dithering != "none":
            frame_gamma = torch.round(frame_gamma * (levels - 1)) / (levels - 1)
        
        # Reverse gamma correction
        return frame_gamma.pow(1/gamma)

    def convert_color_space(self, frame: torch.Tensor, to_yuv: bool) -> torch.Tensor:
        """
        Converts between RGB and YUV color spaces.
        """
        if to_yuv:
            # RGB to YUV conversion matrix
            matrix = torch.tensor([
                [ 0.299,  0.587,  0.114],
                [-0.147, -0.289,  0.436],
                [ 0.615, -0.515, -0.100]
            ], device=self.device)
        else:
            # YUV to RGB conversion matrix
            matrix = torch.tensor([
                [1.000,  0.000,  1.140],
                [1.000, -0.395, -0.581],
                [1.000,  2.032,  0.000]
            ], device=self.device)
        
        return torch.matmul(frame, matrix.T)

    def apply_temporal_coherence(self,
                               current_frame: torch.Tensor,
                               prev_frame: torch.Tensor,
                               next_frame: torch.Tensor,
                               strength: float) -> torch.Tensor:
        """
        Reduces temporal color banding by considering adjacent frames.
        """
        if strength == 0 or (prev_frame is None and next_frame is None):
            return current_frame
            
        weights = torch.tensor([0.25, 0.5, 0.25]) * strength
        
        result = current_frame * weights[1]
        if prev_frame is not None:
            result += prev_frame * weights[0]
        if next_frame is not None:
            result += next_frame * weights[2]
            
        return result + current_frame * (1 - strength)

    def apply_bit_clamp(self,
                       images: torch.Tensor,
                       bit_depth: str,
                       dithering: str,
                       color_space: str,
                       preservation: float,
                       gamma: float = 2.2,
                       noise_reduction: float = 0.0,
                       temporal_coherence: float = 0.0) -> Tuple[torch.Tensor]:
        """
        Applies bit depth clamping effect to a batch of images.
        """
        print(f"\nInitializing VideoBitClamp processing...")
        print(f"Settings: {bit_depth}, Dithering: {dithering}, Color Space: {color_space}")
        
        # Ensure input is on correct device
        if not isinstance(images, torch.Tensor):
            print("Converting input to tensor...")
            images = torch.tensor(images, device=self.device)
        else:
            images = images.to(self.device)
        
        batch_size = images.shape[0]
        print(f"Processing {batch_size} frames...")
        output = torch.zeros_like(images)
        
        for i in range(batch_size):
            print(f"\nProcessing frame {i+1}/{batch_size}")
            frame = images[i]
            
            # Apply noise reduction if enabled
            if noise_reduction > 0:
                print(f"  Applying noise reduction (strength: {noise_reduction:.2f})...")
                frame = self.apply_noise_reduction(frame, noise_reduction)
            
            # Convert to YUV if selected
            if color_space == "YUV":
                print("  Converting to YUV color space...")
                frame = self.convert_color_space(frame, to_yuv=True)
            
            # Apply temporal coherence if enabled
            if temporal_coherence > 0:
                print(f"  Applying temporal coherence (strength: {temporal_coherence:.2f})...")
                prev_frame = images[i-1] if i > 0 else None
                next_frame = images[i+1] if i < batch_size-1 else None
                frame = self.apply_temporal_coherence(
                    frame, prev_frame, next_frame, temporal_coherence
                )
            
            # Apply bit depth clamping
            print(f"  Applying {bit_depth} clamping with {dithering} dithering...")
            frame_clamped = self.apply_bit_depth(frame, bit_depth, dithering, gamma)
            
            # Blend with original based on preservation factor
            if preservation > 0:
                print(f"  Blending with original (preservation: {preservation:.2f})...")
                frame_final = torch.lerp(frame_clamped, frame, preservation)
            else:
                frame_final = frame_clamped
            
            # Convert back to RGB if necessary
            if color_space == "YUV":
                print("  Converting back to RGB color space...")
                frame_final = self.convert_color_space(frame_final, to_yuv=False)
            
            output[i] = frame_final
            print(f"  Frame {i+1} complete ({((i+1)/batch_size*100):.1f}% of total)")
            
        print("\nProcessing complete!")
        
        return (torch.clamp(output, 0, 1),)

NODE_CLASS_MAPPINGS = {
    "VideoBitClamp": VideoBitClamp
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "VideoBitClamp": "Video Bit Depth Clamper"
}
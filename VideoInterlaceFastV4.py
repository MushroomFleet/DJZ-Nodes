import torch
import torch.nn.functional as F
import cv2
import numpy as np
from typing import Tuple, List, Optional, Union
from enum import Enum

class UpscaleMode(str, Enum):
    FASTEST = "fastest"          # Pure bilinear
    FAST = "fast"               # Lanczos without motion comp
    BALANCED = "balanced"       # Interlaced + basic motion
    QUALITY = "quality"         # Full features

class VideoInterlaceFastV4:
    """
    Optimized ComfyUI custom node for fast video frame upscaling.
    Supports multiple speed/quality modes and optional enhancements.
    """
    
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.use_half = self.device == "cuda"  # Enable fp16 on GPU
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "mode": (["fastest", "fast", "balanced", "quality"], {
                    "default": "balanced"
                }),
                "input_height": ("INT", {
                    "default": 720,
                    "min": 480,
                    "max": 4320,
                    "step": 1,
                }),
                "input_width": ("INT", {
                    "default": 1280,
                    "min": 640,
                    "max": 7680,
                    "step": 1,
                }),
                "scale_factor": ("FLOAT", {
                    "default": 1.5,
                    "min": 1.0,
                    "max": 4.0,
                    "step": 0.1,
                }),
            },
            "optional": {
                "enable_motion_comp": ("BOOLEAN", {
                    "default": True,
                }),
                "batch_size": ("INT", {
                    "default": 4,
                    "min": 1,
                    "max": 16,
                    "step": 1,
                }),
                "precision": (["full", "half"], {
                    "default": "half"
                }),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "upscale"
    CATEGORY = "image/upscaling"

    def fastest_upscale(self, frame: torch.Tensor, scale_factor: Union[float, Tuple[float, float]]) -> torch.Tensor:
        """Pure bilinear upscaling - fastest possible method"""
        # Ensure frame is in correct format (B,H,W,C)
        if len(frame.shape) == 3:  # Single frame
            frame = frame.unsqueeze(0)
            
        # Handle scale factor
        if isinstance(scale_factor, tuple):
            scale_h, scale_w = scale_factor
        else:
            scale_h = scale_w = scale_factor
            
        return F.interpolate(
            frame.permute(0, 3, 1, 2),  # B,H,W,C -> B,C,H,W
            scale_factor=(scale_h, scale_w),
            mode='bilinear',
            align_corners=False
        ).permute(0, 2, 3, 1)  # B,C,H,W -> B,H,W,C

    def lanczos_upscale(self, frame: torch.Tensor, target_size: Tuple[int, int]) -> torch.Tensor:
        """Fast Lanczos upscaling using OpenCV"""
        # Convert to float32 before numpy conversion
        frame = frame.float()
        
        # Convert to numpy and ensure proper range [0, 1]
        frame_np = frame.cpu().numpy()
        frame_np = np.clip(frame_np, 0, 1)
        
        # Handle different input formats
        if len(frame_np.shape) == 4:  # Batch of images (B,H,W,C)
            B, H, W, C = frame_np.shape
            output = []
            for i in range(B):
                # Process each frame
                img = frame_np[i]  # (H,W,C)
                # Convert to uint8 for OpenCV
                img_uint8 = (img * 255).astype(np.uint8)
                upscaled = cv2.resize(
                    img_uint8, 
                    (int(target_size[1]), int(target_size[0])), 
                    interpolation=cv2.INTER_LANCZOS4
                )
                # Convert back to float32 [0, 1]
                upscaled = upscaled.astype(np.float32) / 255.0
                output.append(upscaled)
            upscaled = np.stack(output)
        else:  # Single image (H,W,C)
            # Convert to uint8 for OpenCV
            frame_uint8 = (frame_np * 255).astype(np.uint8)
            upscaled = cv2.resize(
                frame_uint8, 
                (int(target_size[1]), int(target_size[0])), 
                interpolation=cv2.INTER_LANCZOS4
            )
            # Convert back to float32 [0, 1]
            upscaled = upscaled.astype(np.float32) / 255.0
            
        # Back to tensor
        return torch.from_numpy(upscaled).to(self.device)

    def apply_fast_motion_compensation(self, 
                                     frames: torch.Tensor,
                                     blend_factor: float = 0.2) -> torch.Tensor:
        """Simplified motion compensation for speed"""
        batch_size = frames.shape[0]
        compensated = frames.clone()
        
        for i in range(1, batch_size - 1):
            # Simple temporal blending
            compensated[i] = (
                frames[i] * (1 - blend_factor) +
                (frames[i-1] + frames[i+1]) * (blend_factor / 2)
            )
        
        return compensated

    def process_batch(self,
                     frames: torch.Tensor,
                     target_size: Tuple[int, int],
                     mode: str,
                     enable_motion_comp: bool) -> torch.Tensor:
        """Process a batch of frames according to selected mode"""
        # Ensure frames are in correct format (B,H,W,C)
        if len(frames.shape) == 3:  # Single frame
            frames = frames.unsqueeze(0)
        elif len(frames.shape) == 4 and frames.shape[-1] != 3:  # Wrong channel dimension
            frames = frames.movedim(1, -1)
            
        if mode == UpscaleMode.FASTEST:
            # Calculate scale factors for height and width
            scale_h = target_size[0] / frames.shape[1]
            scale_w = target_size[1] / frames.shape[2]
            return self.fastest_upscale(frames, (scale_h, scale_w))
            
        elif mode == UpscaleMode.FAST:
            # Lanczos without motion compensation
            return self.lanczos_upscale(frames, target_size)
            
        elif mode == UpscaleMode.BALANCED:
            # Lanczos with optional basic motion compensation
            if enable_motion_comp:
                frames = self.apply_fast_motion_compensation(frames)
            return self.lanczos_upscale(frames, target_size)
            
        else:  # QUALITY mode
            # Full processing with all features enabled
            if enable_motion_comp:
                frames = self.apply_fast_motion_compensation(frames, blend_factor=0.3)
            upscaled = self.lanczos_upscale(frames, target_size)
            # Add edge enhancement for quality mode
            upscaled = self.enhance_edges(upscaled)
            return upscaled

    def enhance_edges(self, frames: torch.Tensor, strength: float = 0.3) -> torch.Tensor:
        """Fast edge enhancement using Sobel operator"""
        # Simple Sobel edge detection
        sobel_x = torch.tensor([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], 
                             device=self.device).float()
        sobel_y = sobel_x.t()
        
        if len(frames.shape) == 4:  # Batch of frames
            frames_gray = frames.mean(dim=1, keepdim=True)
        else:  # Single frame
            frames_gray = frames.mean(dim=0, keepdim=True)
            
        # Apply Sobel
        edges_x = F.conv2d(frames_gray, sobel_x.view(1, 1, 3, 3), padding=1)
        edges_y = F.conv2d(frames_gray, sobel_y.view(1, 1, 3, 3), padding=1)
        edges = torch.sqrt(edges_x.pow(2) + edges_y.pow(2))
        
        # Enhance original frames
        return frames + edges * strength

    def upscale(self,
                images: torch.Tensor,
                mode: str,
                input_height: int,
                input_width: int,
                scale_factor: float,
                enable_motion_comp: bool = True,
                batch_size: int = 4,
                precision: str = "half") -> Tuple[torch.Tensor]:
        """
        Main upscaling function with batched processing
        """
        # Setup
        if precision == "half" and self.use_half:
            images = images.half()
        
        target_height = int(input_height * scale_factor)
        target_width = int(input_width * scale_factor)
        target_size = (target_height, target_width)
        
        # Ensure images are in correct format
        if not isinstance(images, torch.Tensor):
            images = torch.tensor(images, device=self.device)
        
        # Process in batches
        batches = torch.split(images, batch_size)
        outputs = []
        
        for batch in batches:
            # Move batch to device and ensure float32 for processing
            batch = batch.to(self.device).float()
            if len(batch.shape) == 3:
                batch = batch.unsqueeze(0)
                
            # Process according to mode
            upscaled = self.process_batch(
                batch, 
                target_size, 
                mode,
                enable_motion_comp
            )
            
            outputs.append(upscaled.cpu())  # Move back to CPU to save memory
            
        # Combine batches
        output = torch.cat(outputs, dim=0)
        
        # Convert back to half precision if needed
        if precision == "half" and self.use_half:
            output = output.half()
            
        return (torch.clamp(output, 0, 1),)

NODE_CLASS_MAPPINGS = {
    "VideoInterlaceFastV4": VideoInterlaceFastV4
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "VideoInterlaceFastV4": "Fast Video Upscaler V4"
}
import torch
import torch.nn.functional as F
from typing import Tuple, List
import numpy as np

class VideoInterlacedV2:
    """
    Enhanced ComfyUI custom node for interlaced upscaling of video frames.
    Provides additional controls for field handling, interpolation methods,
    and motion compensation.
    """
    
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "input_height": ("INT", {
                    "default": 720,
                    "min": 480,
                    "max": 4320,
                    "step": 1,
                    "display": "number"
                }),
                "input_width": ("INT", {
                    "default": 1280,
                    "min": 640,
                    "max": 7680,
                    "step": 1,
                    "display": "number"
                }),
                "field_order": (["top_first", "bottom_first"], {
                    "default": "top_first"
                }),
                "scale_factor": ("FLOAT", {
                    "default": 1.5,
                    "min": 1.0,
                    "max": 4.0,
                    "step": 0.1,
                    "display": "slider"
                }),
                "blend_factor": ("FLOAT", {
                    "default": 0.25,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.05,
                    "display": "slider"
                }),
                "motion_compensation": (["none", "basic", "advanced"], {
                    "default": "basic"
                }),
                "interpolation_mode": (["bilinear", "bicubic", "nearest"], {
                    "default": "bilinear"
                }),
                "deinterlace_method": (["blend", "bob", "weave"], {
                    "default": "blend"
                }),
            },
            "optional": {
                "field_strength": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 2.0,
                    "step": 0.1,
                    "display": "slider"
                }),
                "temporal_radius": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 3,
                    "step": 1,
                    "display": "number"
                }),
                "edge_enhancement": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.1,
                    "display": "slider"
                })
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "apply_interlacing"
    CATEGORY = "image/upscaling"

    def apply_edge_enhancement(self, frame: torch.Tensor, strength: float) -> torch.Tensor:
        """
        Applies edge enhancement to the frame using a Sobel operator.
        """
        if strength == 0:
            return frame
            
        # Sobel operators
        sobel_x = torch.tensor([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], device=self.device).float()
        sobel_y = torch.tensor([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], device=self.device).float()
        
        # Expand dimensions for conv2d
        frame_gray = frame.mean(dim=-1, keepdim=True)
        frame_gray = frame_gray.permute(2, 0, 1).unsqueeze(0)
        
        # Apply Sobel operators
        edges_x = F.conv2d(frame_gray, sobel_x.view(1, 1, 3, 3), padding=1)
        edges_y = F.conv2d(frame_gray, sobel_y.view(1, 1, 3, 3), padding=1)
        edges = torch.sqrt(edges_x.pow(2) + edges_y.pow(2))
        
        # Normalize and apply strength
        edges = edges / edges.max() * strength
        
        # Add enhanced edges to original frame
        enhanced = frame + edges.squeeze(0).permute(1, 2, 0).repeat(1, 1, frame.shape[-1])
        return torch.clamp(enhanced, 0, 1)

    def apply_advanced_motion_compensation(self,
                                        frame: torch.Tensor,
                                        prev_frame: torch.Tensor,
                                        next_frame: torch.Tensor,
                                        temporal_radius: int) -> torch.Tensor:
        """
        Applies advanced motion compensation using temporal information.
        """
        if temporal_radius <= 1 or prev_frame is None or next_frame is None:
            return frame
            
        # Calculate motion vectors (simplified optical flow estimation)
        flow_prev = frame - prev_frame
        flow_next = next_frame - frame
        
        # Weight based on temporal distance
        weights = torch.softmax(torch.tensor([1.0, 2.0, 1.0]), dim=0)
        
        # Combine frames with weighted average
        compensated = (
            weights[0] * prev_frame +
            weights[1] * frame +
            weights[2] * next_frame
        )
        
        return compensated

    def create_interlaced_frame(self,
                              frame: torch.Tensor,
                              prev_frame: torch.Tensor = None,
                              next_frame: torch.Tensor = None,
                              target_height: int = None,
                              target_width: int = None,
                              field_order: str = "top_first",
                              blend_factor: float = 0.25,
                              motion_compensation: str = "basic",
                              interpolation_mode: str = "bilinear",
                              deinterlace_method: str = "blend",
                              field_strength: float = 1.0,
                              temporal_radius: int = 1,
                              edge_enhancement: float = 0.0) -> torch.Tensor:
        """
        Creates an interlaced frame with enhanced options for field handling and processing.
        """
        # Initial upscale
        upscaled = F.interpolate(
            frame.unsqueeze(0).permute(0, 3, 1, 2),
            size=(target_height, target_width),
            mode=interpolation_mode,
            align_corners=False if interpolation_mode != 'nearest' else None
        ).permute(0, 2, 3, 1).squeeze(0)
        
        # Create field masks
        even_mask = torch.zeros((target_height, 1, 1), device=self.device)
        odd_mask = torch.zeros((target_height, 1, 1), device=self.device)
        
        if field_order == "top_first":
            even_mask[::2] = 1.0
            odd_mask[1::2] = 1.0
        else:
            even_mask[1::2] = 1.0
            odd_mask[::2] = 1.0
        
        # Apply field strength
        even_mask *= field_strength
        odd_mask *= field_strength
        
        # Separate fields
        even_field = upscaled * even_mask
        odd_field = upscaled * odd_mask
        
        # Apply motion compensation based on selected method
        if motion_compensation != "none":
            if motion_compensation == "advanced" and prev_frame is not None and next_frame is not None:
                upscaled = self.apply_advanced_motion_compensation(
                    upscaled, prev_frame, next_frame, temporal_radius
                )
            else:  # Basic motion compensation
                shifted_even = torch.roll(even_field, shifts=1, dims=0)
                shifted_odd = torch.roll(odd_field, shifts=-1, dims=0)
                
                even_field = (1 - blend_factor) * even_field + blend_factor * shifted_odd
                odd_field = (1 - blend_factor) * odd_field + blend_factor * shifted_even
        
        # Apply deinterlacing method
        if deinterlace_method == "blend":
            interlaced = even_field + odd_field
        elif deinterlace_method == "bob":
            interlaced = torch.where(even_mask > 0, even_field, odd_field)
        else:  # weave
            interlaced = even_field + odd_field
            interlaced = F.interpolate(
                interlaced.unsqueeze(0).permute(0, 3, 1, 2),
                size=(target_height, target_width),
                mode=interpolation_mode,
                align_corners=False if interpolation_mode != 'nearest' else None
            ).permute(0, 2, 3, 1).squeeze(0)
        
        # Apply edge enhancement if enabled
        if edge_enhancement > 0:
            interlaced = self.apply_edge_enhancement(interlaced, edge_enhancement)
        
        return interlaced

    def apply_interlacing(self,
                         images: torch.Tensor,
                         input_height: int,
                         input_width: int,
                         field_order: str,
                         scale_factor: float,
                         blend_factor: float,
                         motion_compensation: str,
                         interpolation_mode: str,
                         deinterlace_method: str,
                         field_strength: float = 1.0,
                         temporal_radius: int = 1,
                         edge_enhancement: float = 0.0) -> Tuple[torch.Tensor]:
        """
        Apply enhanced interlaced upscaling to a batch of images.
        """
        # Ensure input is on correct device
        if not isinstance(images, torch.Tensor):
            images = torch.tensor(images, device=self.device)
        else:
            images = images.to(self.device)
        
        # Calculate target dimensions
        target_height = int(input_height * scale_factor)
        target_width = int(input_width * scale_factor)
        
        # Process batch
        batch_size = images.shape[0]
        output = torch.zeros((batch_size, target_height, target_width, images.shape[3]),
                           device=self.device)
        
        for i in range(batch_size):
            # Get adjacent frames for motion compensation
            prev_frame = images[i-1] if i > 0 else None
            next_frame = images[i+1] if i < batch_size-1 else None
            
            output[i] = self.create_interlaced_frame(
                images[i],
                prev_frame,
                next_frame,
                target_height,
                target_width,
                field_order,
                blend_factor,
                motion_compensation,
                interpolation_mode,
                deinterlace_method,
                field_strength,
                temporal_radius,
                edge_enhancement
            )
        
        return (torch.clamp(output, 0, 1),)

NODE_CLASS_MAPPINGS = {
    "VideoInterlacedV2": VideoInterlacedV2
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "VideoInterlacedV2": "Video Interlaced Upscaler V2"
}
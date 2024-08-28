import os
import numpy as np
import torch
from PIL import Image
import folder_paths

class FFXFADEORAMA:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image1": ("IMAGE",),
                "image2": ("IMAGE",),
                "num_frames": ("INT", {"default": 30, "min": 2, "max": 120, "step": 1}),
                "transition_type": ([
                    "fade", "glitchA", "glitchB", "wipeR", "wipeL",
                    "smoothright", "smoothleft",
                    "openglitchdoors", "closeglitchdoors", "openchanneldoors",
                    "rgbbandright", "rgbdoubleright", "rgbdoubleleft", "rgbdoubleleft2",
                    "fadeblack", "fadewhite"
                ], {"default": "fade"}),
                "filename_prefix": ("STRING", {"default": "FFXFADE", "tooltip": "The prefix for the output files."})
            },
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"}
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "create_crossfade_sequence"
    OUTPUT_NODE = True
    CATEGORY = "image/animation"

    def create_crossfade_sequence(self, image1, image2, num_frames, transition_type, filename_prefix, prompt=None, extra_pnginfo=None):
        if image1.shape != image2.shape:
            raise ValueError("Input images must have the same dimensions")

        sequence = self.generate_transition(image1, image2, num_frames, transition_type)

        results = []
        for i in range(num_frames):
            frame = sequence[i]
            result = self.save_image(frame, f"{filename_prefix}_{i:05d}", prompt, extra_pnginfo)
            results.extend(result)

        return (sequence, {"ui": {"images": results}})

    def generate_transition(self, image1, image2, num_frames, transition_type):
        b, c, h, w = image1.shape
        t = torch.linspace(0, 1, num_frames).view(num_frames, 1, 1, 1)
        
        if transition_type == "fade":
            return image1 * (1 - t) + image2 * t
        
        elif transition_type in ["glitchA", "glitchB", "wipeR", "wipeL"]:
            if transition_type == "glitchA":
                mask = (torch.linspace(0, 1, w) < t).float().view(num_frames, 1, 1, w)
            elif transition_type == "glitchB":
                mask = (torch.linspace(0, 1, w) > (1 - t)).float().view(num_frames, 1, 1, w)
            elif transition_type == "wipeR":
                mask = (torch.linspace(0, 1, h) < t).float().view(num_frames, 1, h, 1)
            else:  # wipeL
                mask = (torch.linspace(0, 1, h) > (1 - t)).float().view(num_frames, 1, h, 1)
            return image1 * (1 - mask) + image2 * mask
        
        elif transition_type in ["smoothright", "smoothleft"]:
            y = torch.linspace(0, 1, h).view(1, 1, h, 1)
            if transition_type == "smoothright":
                mask = 0.5 * (1 - torch.cos(np.pi * y))
            else:
                mask = 0.5 * (1 - torch.cos(np.pi * (1 - y)))
            mask = (mask < t).float()
            return image1 * (1 - mask) + image2 * mask
        
        elif transition_type in ["openglitchdoors", "closeglitchdoors", "openchanneldoors"]:
            y, x = torch.meshgrid(torch.linspace(-1, 1, h), torch.linspace(-1, 1, w))
            if transition_type == "openglitchdoors":
                mask = torch.max(torch.abs(x), torch.abs(y)).unsqueeze(0).unsqueeze(0)
            else:
                mask = (x.pow(2) + y.pow(2)).sqrt().unsqueeze(0).unsqueeze(0)
            
            if transition_type == "closeglitchdoors":
                mask = (mask > (1 - t)).float()
            else:  # openglitchdoors or openchanneldoors
                mask = (mask < t).float()
            return image1 * (1 - mask) + image2 * mask
        
        elif transition_type in ["rgbbandright", "rgbdoubleright", "rgbdoubleleft", "rgbdoubleleft2"]:
            y, x = torch.meshgrid(torch.linspace(0, 1, h), torch.linspace(0, 1, w))
            if transition_type == "rgbbandright":
                mask = (x + y < 2 * t).float().view(num_frames, 1, h, w)
            elif transition_type == "rgbdoubleright":
                mask = (x - y > 1 - 2 * t).float().view(num_frames, 1, h, w)
            elif transition_type == "rgbdoubleleft":
                mask = (y - x > 1 - 2 * t).float().view(num_frames, 1, h, w)
            else:  # rgbdoubleleft2
                mask = (x + y > 2 - 2 * t).float().view(num_frames, 1, h, w)
            return image1 * (1 - mask) + image2 * mask
        
        elif transition_type in ["fadeblack", "fadewhite"]:
            black_or_white = torch.ones_like(image1) if transition_type == "fadewhite" else torch.zeros_like(image1)
            first_half = image1 * (1 - 2 * t) + black_or_white * 2 * t
            second_half = black_or_white * (2 - 2 * t) + image2 * (2 * t - 1)
            return torch.where(t < 0.5, first_half, second_half)
        
        else:
            raise ValueError(f"Unsupported transition type: {transition_type}")

    def save_image(self, image, filename_prefix, prompt=None, extra_pnginfo=None):
        full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(filename_prefix, self.output_dir, image.shape[1], image.shape[0])
        
        results = []
        i = 255. * image.cpu().numpy()
        img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
        
        file = f"{filename}_{counter:05}.png"
        img.save(os.path.join(full_output_folder, file))
        results.append({
            "filename": file,
            "subfolder": subfolder,
            "type": self.type
        })
        
        return results
"""
@author: DJZ-Nodes
Dataset Wordcloud Generator - A node that generates wordcloud visualizations from prompt datasets
"""

import os
import torch
import numpy as np
from PIL import Image
from wordcloud import WordCloud
import matplotlib.pyplot as plt

class DatasetWordcloud:
    """A ComfyUI node that generates wordcloud visualizations from prompt datasets"""
    COLOR_PALETTES = {
        "kandinsky": ['#69D2E7', '#A7DBD8', '#E0E4CC', '#F38630', '#FA6900', '#FF4E50', '#F9D423'],
        "warm": ['#FF4E50', '#FC913A', '#F9D423', '#EDE574', '#E1F5C4'],
        "cool": ['#69D2E7', '#A7DBD8', '#E0E4CC', '#B2C2C1', '#8AB8B2'],
        "monochrome": ['#FFFFFF', '#D9D9D9', '#BFBFBF', '#8C8C8C', '#404040'],
        "vibrant": ['#FF1E1E', '#FF9900', '#FFFF00', '#00FF00', '#0000FF', '#9900FF']
    }

    @classmethod
    def INPUT_TYPES(cls):
        # Get the list of text files in the 'prompts' folder
        prompts_folder = os.path.join(os.path.dirname(__file__), 'prompts')
        text_files = [f for f in os.listdir(prompts_folder) if f.endswith('.txt')]
        
        return {
            "required": {
                "text_file": (text_files,),
                "width": ("INT", {"default": 800, "min": 64, "max": 4096}),
                "height": ("INT", {"default": 400, "min": 64, "max": 4096}),
                "color_palette": (list(cls.COLOR_PALETTES.keys()),),
                "background_color": ("STRING", {"default": "white"})
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate_wordcloud"
    CATEGORY = "DJZ-Nodes"

    def generate_wordcloud(self, text_file, width, height, color_palette, background_color):
        # Get the full path to the text file
        prompts_folder = os.path.join(os.path.dirname(__file__), 'prompts')
        file_path = os.path.join(prompts_folder, text_file)

        # Read the entire content of the file
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()

        # Get colors for selected palette
        colors = self.COLOR_PALETTES[color_palette]

        # Create a WordCloud object with the specified settings
        wordcloud = WordCloud(
            width=width,
            height=height,
            background_color=background_color,
            colormap=None,  # We'll use our own color function
            color_func=lambda *args, **kwargs: np.random.choice(colors),
            prefer_horizontal=0.7
        ).generate(text)

        # Convert the wordcloud to an image
        plt.figure(figsize=(width/100, height/100), dpi=100)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        
        # Save to a temporary buffer
        plt.savefig('temp_wordcloud.png', bbox_inches='tight', pad_inches=0, 
                   facecolor=background_color)
        plt.close()

        # Load the saved image and convert to tensor
        image = Image.open('temp_wordcloud.png')
        
        # Resize to requested dimensions if needed
        if image.size != (width, height):
            image = image.resize((width, height))

        # Convert to RGB if not already
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Convert to numpy array and normalize to 0-1 range
        image_np = np.array(image).astype(np.float32) / 255.0
        
        # Convert to PyTorch tensor
        image_tensor = torch.from_numpy(image_np)
        
        # Ensure shape is (B,H,W,C)
        if len(image_tensor.shape) == 3:
            image_tensor = image_tensor.unsqueeze(0)

        # Clean up temporary file
        if os.path.exists('temp_wordcloud.png'):
            os.remove('temp_wordcloud.png')
        
        return (image_tensor,)

# Node registration for ComfyUI
NODE_CLASS_MAPPINGS = {
    "DatasetWordcloud": DatasetWordcloud
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DatasetWordcloud": "Dataset Wordcloud"
}

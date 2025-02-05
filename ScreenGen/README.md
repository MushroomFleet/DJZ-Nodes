# ScreenGen - Screensaver Generator Presets

This directory contains the screensaver preset files for the ScreensaverGeneratorV2 node. Each preset is a Python file with the `.scg` extension that defines a screensaver effect.

## Creating a New Preset

To create a new screensaver preset:

1. Create a new file with the `.scg` extension in this directory
2. Define a class that ends with 'Screensaver' (e.g., `MyCustomScreensaver`)
3. Implement the required methods and properties:

```python
import cv2
import numpy as np

class MyCustomScreensaver:
    def __init__(self):
        self.name = "My Custom"  # Name shown in the preset dropdown
        self.description = "Description of your screensaver"
        
        # Define parameters that will be exposed in the UI
        self.parameters = {
            "param_name": {
                "type": "INT",  # INT, FLOAT, or STRING
                "default": 10,
                "min": 1,
                "max": 100,
                "step": 1
            }
            # Add more parameters as needed
        }
    
    def init_state(self):
        """Return initial state for the screensaver"""
        return {
            # Add any state variables needed
        }
    
    def render(self, width, height, frame, colors, speed, state, params):
        """Render a frame of the screensaver
        
        Args:
            width (int): Frame width
            height (int): Frame height
            frame (int): Current frame number
            colors (list): List of (R,G,B) tuples for the color palette
            speed (float): Global speed multiplier
            state (dict): State from previous frame (or None for first frame)
            params (dict): Current parameter values
            
        Returns:
            tuple: (frame_image, new_state)
            - frame_image: numpy array of shape (height, width, 3)
            - new_state: Updated state dict for next frame
        """
        if not state:
            state = self.init_state()
            
        # Create frame image
        img = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Render your effect here using the parameters
        # ...
        
        return img, state
```

## Parameter Types

The following parameter types are supported:

- `INT`: Integer values with min/max/step
- `FLOAT`: Float values with min/max/step
- `STRING` with choices: Dropdown selection from a list of options

Example parameter definitions:

```python
self.parameters = {
    # Integer parameter
    "count": {
        "type": "INT",
        "default": 10,
        "min": 1,
        "max": 100,
        "step": 1
    },
    
    # Float parameter
    "speed": {
        "type": "FLOAT",
        "default": 1.0,
        "min": 0.1,
        "max": 5.0,
        "step": 0.1
    },
    
    # Choice parameter
    "mode": {
        "type": "STRING",
        "default": "mode1",
        "choices": ["mode1", "mode2", "mode3"]
    }
}
```

## Tips

1. Use descriptive parameter names that reflect their purpose
2. Set reasonable min/max/default values
3. Keep the step size appropriate for the parameter range
4. Use the state dict to maintain continuity between frames
5. Utilize the color palette provided in the colors parameter
6. Scale effects based on the global speed parameter
7. Handle the case when state is None (first frame)
8. Ensure all numpy arrays use uint8 dtype for images

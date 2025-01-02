"""
Sequential Number Generator Node for ComfyUI
Generates sequential integer numbers within a defined range.
Uses ComfyUI's seed logic for counter control.
"""

class SequentialNumberGenerator:
    """
    A custom node for ComfyUI that generates sequential integer numbers within a specified range.
    The numbers cycle through the range in order, resetting back to the start when reaching the end.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "start": ("INT", {"default": 0, "min": -2147483648, "max": 2147483647}),
                "end": ("INT", {"default": 1, "min": -2147483648, "max": 2147483647}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            },
        }

    RETURN_TYPES = ("INT", "INT",)  # Returns (current_value, next_value)
    RETURN_NAMES = ("value", "next")
    FUNCTION = "generate"
    CATEGORY = "number operations"
    
    def generate(self, start, end, seed):
        # Validate the range
        if start > end:
            raise ValueError(f"Start value ({start}) must be less than or equal to end value ({end})")
            
        # Calculate the range size
        range_size = end - start + 1
        
        # Map the seed to a valid value in our range
        current = start + (seed % range_size)
        
        # Calculate the next value
        next_value = current + 1
        if next_value > end:
            next_value = start
            
        return (current, next_value)

# Define the node class mapping
NODE_CLASS_MAPPINGS = {
    "SequentialNumberGenerator": SequentialNumberGenerator
}

# Define how you want the node to be displayed in the UI
NODE_DISPLAY_NAME_MAPPINGS = {
    "SequentialNumberGenerator": "Sequential Number Generator"
}

# This line is optional but recommended to prevent execution if the file is imported
if __name__ == "__main__":
    pass
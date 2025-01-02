"""
Sequential Number Generator Node for ComfyUI
Generates sequential integer numbers within a specified range.
"""

class SequentialNumberGenerator:
    """
    A custom node for ComfyUI that generates sequential integer numbers within a specified range.
    The numbers cycle through the range in order, resetting back to the start when reaching the end.
    """
    
    def __init__(self):
        self.execution_count = 0
        self.current_range = None
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "start": ("INT", {"default": 0, "min": -2147483648, "max": 2147483647}),
                "end": ("INT", {"default": 1, "min": -2147483648, "max": 2147483647}),
            },
        }

    RETURN_TYPES = ("INT",)
    FUNCTION = "generate"
    CATEGORY = "number operations"
    
    def IS_CHANGED(self, start, end):
        range_id = f"{start}-{end}"
        if self.current_range != range_id:
            self.current_range = range_id
            self.execution_count = 0
        return self.execution_count

    def generate(self, start, end):
        # Calculate the range size
        range_size = end - start + 1
        
        # Calculate the current position in the sequence
        current_position = self.execution_count % range_size
        
        # Calculate the actual number based on the position
        result = start + current_position
        
        # Increment the execution count
        self.execution_count += 1
        
        return (result,)

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
import random

class StringPainterV2:
    """
    A node for generating hex strings based on a seed value.
    Supports 16-bit and 32-bit hex strings in increment and random modes.
    Now also outputs the seed used for each generation.
    """

    def __init__(self):
        self.seed = 0
        self.bits = 16
        self.mode = "increment"
        self.custom_random_range = (0, 0xFFFFFFFF)

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xFFFFFFFF}),
                "bits": (["16", "32"], {"default": "16"}),
                "mode": (["increment", "random"], {"default": "increment"}),
                "count": ("INT", {"default": 1, "min": 1, "max": 100})
            },
            "optional": {
                "random_min": ("INT", {"default": 0, "min": 0, "max": 0xFFFFFFFF}),
                "random_max": ("INT", {"default": 0xFFFFFFFF, "min": 0, "max": 0xFFFFFFFF})
            }
        }

    RETURN_TYPES = ("STRING", "INT")
    RETURN_NAMES = ("hex_string", "used_seed")
    FUNCTION = "generate_hex"
    CATEGORY = "painting"

    def generate_hex(self, seed, bits, mode, count, random_min=None, random_max=None):
        """
        Generate hex string(s) based on input parameters.
        Returns both the generated hex string(s) and the seed(s) used.
        """
        try:
            self.seed = self._validate_int(seed, "seed", 0, 0xFFFFFFFF)
            self.bits = self._validate_int(bits, "bits", 16, 32)
            self.mode = self._validate_str(mode, "mode", ["increment", "random"])
            count = self._validate_int(count, "count", 1, 100)
            
            if random_min is not None and random_max is not None:
                self.custom_random_range = (
                    self._validate_int(random_min, "random_min", 0, 0xFFFFFFFF),
                    self._validate_int(random_max, "random_max", 0, 0xFFFFFFFF)
                )
                if self.custom_random_range[0] >= self.custom_random_range[1]:
                    raise ValueError("random_min must be less than random_max")
            
            hex_strings = []
            used_seeds = []
            for _ in range(count):
                hex_string, used_seed = self._generate_single_hex()
                hex_strings.append(hex_string)
                used_seeds.append(used_seed)
            
            return (",".join(hex_strings), ",".join(map(str, used_seeds)))
        
        except ValueError as e:
            return (f"Error: {str(e)}", str(self.seed))

    def _generate_single_hex(self):
        """Generate a single hex string and return it along with the seed used."""
        if self.mode == "random":
            used_seed = random.randint(*self.custom_random_range)
        else:
            used_seed = self.seed
            self.seed = (self.seed + 1) & 0xFFFFFFFF  # Increment and wrap around

        hex_string = self._seed_to_hex(used_seed)
        return hex_string, used_seed

    def _seed_to_hex(self, seed):
        """Convert seed to hex string using bitwise operations."""
        mask = (1 << self.bits) - 1
        hex_value = seed & mask
        return f"{hex_value:0{self.bits//4}X}"

    @staticmethod
    def _validate_int(value, name, min_value, max_value):
        """Validate integer inputs."""
        try:
            value = int(value)
            if not (min_value <= value <= max_value):
                raise ValueError(f"{name} must be between {min_value} and {max_value}")
            return value
        except ValueError:
            raise ValueError(f"Invalid {name}: must be an integer")

    @staticmethod
    def _validate_str(value, name, valid_options):
        """Validate string inputs."""
        if value not in valid_options:
            raise ValueError(f"Invalid {name}: must be one of {', '.join(valid_options)}")
        return value

# Example usage and testing
if __name__ == "__main__":
    painter = StringPainterV2()
    
    # Test with default parameters
    hex_result, seed_result = painter.generate_hex(12345, "16", "increment", 1)
    print(f"Default (16-bit, increment): Hex: {hex_result}, Seed: {seed_result}")
    
    # Test with 32-bit and random mode
    hex_result, seed_result = painter.generate_hex(0, "32", "random", 5, 1000, 9999)
    print(f"32-bit, random mode, 5 values, custom range:")
    print(f"Hex: {hex_result}")
    print(f"Seeds: {seed_result}")
    
    # Test error handling
    hex_result, seed_result = painter.generate_hex(-1, "16", "invalid", 1)
    print(f"Error handling test: {hex_result}, Seed: {seed_result}")
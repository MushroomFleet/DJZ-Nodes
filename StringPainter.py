import random

class StringPainter:
    def __init__(self):
        self.seed = 0
        self.bits = 16
        self.mode = "increment"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xFFFFFFFF}),
                "bits": (["16", "32"], {"default": "16"}),
                "mode": (["increment", "random"], {"default": "increment"})
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate_hex"
    CATEGORY = "painting"

    def generate_hex(self, seed, bits, mode):
        self.seed = seed
        self.bits = int(bits)
        self.mode = mode

        if self.mode == "random":
            seed = random.randint(0, 0xFFFFFFFF)

        hex_string = self.seed_to_hex(seed, self.bits)
        return (hex_string,)

    def seed_to_hex(self, seed, bits):
        max_value = 2**bits - 1
        hex_value = seed & max_value
        if bits == 16:
            return f"{hex_value:04X}"
        elif bits == 32:
            return f"{hex_value:08X}"
        else:
            raise ValueError("Unsupported bit size")

# Example usage (not part of the node class, but useful for testing)
if __name__ == "__main__":
    painter = StringPainter()
    
    # Test with 16-bit increment mode
    result = painter.generate_hex(12345, "16", "increment")
    print(f"16-bit increment mode, seed 12345: {result[0]}")
    
    # Test with 32-bit increment mode
    result = painter.generate_hex(12345, "32", "increment")
    print(f"32-bit increment mode, seed 12345: {result[0]}")
    
    # Test with 16-bit random mode
    result = painter.generate_hex(0, "16", "random")
    print(f"16-bit random mode: {result[0]}")
    
    # Test with 32-bit random mode
    result = painter.generate_hex(0, "32", "random")
    print(f"32-bit random mode: {result[0]}")
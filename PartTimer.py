import time
from typing import Any, Dict, Tuple

# Wildcard trick is taken from pythongossss's
class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False

any_typ = AnyType("*")

class PartTimer:
    """
    A ComfyUI node that acts as a stopwatch to measure execution time
    between START and STOP signals in a workflow.
    
    Features a customizable label parameter for easy identification
    when using multiple timers in complex workflows.
    
    Uses the AnyType wildcard trick to accept any input type,
    allowing seamless integration into any workflow without type conflicts.
    """
    
    def __init__(self):
        self.start_time = None
        self.node_id = id(self)  # Unique identifier for this instance
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "label": ("STRING", {
                    "default": "Timer",
                    "multiline": False,
                    "placeholder": "Timer label for console output"
                }),
            },
            "optional": {
                "START": (any_typ,),
                "STOP": (any_typ,),
            }
        }
    
    RETURN_TYPES = (any_typ, any_typ)
    RETURN_NAMES = ("start_passthrough", "stop_passthrough")
    FUNCTION = "measure_time"
    CATEGORY = "utils/timing"
    OUTPUT_NODE = True
    
    def measure_time(self, label: str = "Timer", START: Any = None, STOP: Any = None) -> Tuple[Any, Any]:
        """
        Measures time between START and STOP inputs and prints result to console.
        
        Args:
            label: Custom label for this timer instance
            START: Any input that triggers the start of timing (optional)
            STOP: Any input that triggers the stop of timing (optional)
            
        Returns:
            Tuple of (START, STOP) passed through for chaining
        """
        current_time = time.time()
        
        # If this is the first time we're seeing START input, record start time
        if START is not None and self.start_time is None:
            self.start_time = current_time
            print(f"[{label}] Stopwatch STARTED at {time.strftime('%H:%M:%S', time.localtime(current_time))}")
        
        # If we have a STOP input and we've already started timing
        if STOP is not None and self.start_time is not None:
            elapsed_seconds = current_time - self.start_time
            
            # Convert to HHMMSS format
            hours = int(elapsed_seconds // 3600)
            minutes = int((elapsed_seconds % 3600) // 60)
            seconds = int(elapsed_seconds % 60)
            
            time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            
            print(f"[{label}] Stopwatch STOPPED")
            print(f"[{label}] Elapsed Time: {time_str}")
            print(f"[{label}] Total Seconds: {elapsed_seconds:.2f}")
            
            # Reset for potential future measurements
            self.start_time = None
        
        return (START, STOP)

# Node registration for ComfyUI
NODE_CLASS_MAPPINGS = {
    "PartTimer": PartTimer
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PartTimer": "Part Timer (Stopwatch)"
}
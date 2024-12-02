import os
from pathlib import Path
import folder_paths

class SaveText:
    OUTPUT_NODE = True
    RETURN_TYPES = ("STRING", "STRING")  # Returns text and filepath
    RETURN_NAMES = ("text", "file_path")
    FUNCTION = "write_text"
    CATEGORY = "file"  # Add this to organize the node in ComfyUI's menu
    
    @classmethod
    def IS_CHANGED(self, **kwargs):
        return float("nan")

    @classmethod
    def INPUT_TYPES(s):
        # Get valid directories from ComfyUI's folder_paths
        valid_paths = [folder_paths.get_output_directory(), 
                      folder_paths.get_input_directory(), 
                      folder_paths.get_temp_directory()]
        
        return {
            "required": {
                "root_dir": (valid_paths, {}),
                "file": ("STRING", {"default": "file.txt"}),
                "append": (["append", "overwrite", "new only"], {}),
                "insert": ("BOOLEAN", {
                    "default": True, 
                    "label_on": "new line", 
                    "label_off": "none",
                    "pysssss.binding": [{
                        "source": "append",
                        "callback": [{
                            "type": "if",
                            "condition": [{
                                "left": "$source.value",
                                "op": "eq",
                                "right": '"append"'
                            }],
                            "true": [{
                                "type": "set",
                                "target": "$this.disabled",
                                "value": False
                            }],
                            "false": [{
                                "type": "set",
                                "target": "$this.disabled",
                                "value": True
                            }],
                        }]
                    }]
                }),
                "text": ("STRING", {"forceInput": True, "multiline": True})
            },
        }

    def write_text(self, root_dir, file, append, insert, text):
        # Create full path
        full_path = Path(root_dir) / file
        
        # Create parent directories if they don't exist
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Determine write mode and handle file operations
        if append == "append":
            mode = 'a'
            newline = '\n' if insert else ''
            content = f"{newline}{text}"
        else:
            mode = 'x' if append == "new only" else 'w'
            content = text
            
        try:
            with open(full_path, mode, encoding='utf-8') as f:
                f.write(content)
        except FileExistsError:
            if append == "new only":
                raise Exception(f"File {full_path} already exists and 'new only' mode was selected")
            
        return (text, str(full_path))  # Modified to match RETURN_TYPES
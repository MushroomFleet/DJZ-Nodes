import os
import hashlib

class CaptionsToPromptList:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "directory_path": ("STRING", {"default": "/path/to/dataset"}),
            },
            "optional": {
                "reload": ("BOOLEAN", {"default": False, "label_on": "if file changed", "label_off": "if value changed"}),
            }
        }
    
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("combined_captions", "output_filename")
    FUNCTION = "process_captions"
    CATEGORY = "custom/text"

    def IS_CHANGED(self, directory_path, reload=False):
        if not reload:
            return directory_path
        else:
            md5 = hashlib.md5()
            for dirpath, dirnames, filenames in os.walk(directory_path):
                for filename in sorted(filenames):
                    if filename.endswith(".txt"):
                        file_path = os.path.join(dirpath, filename)
                        md5.update(filename.encode('utf-8'))
                        with open(file_path, 'rb') as f:
                            while True:
                                chunk = f.read(4096)
                                if not chunk:
                                    break
                                md5.update(chunk)
            return md5.hexdigest()

    def process_captions(self, directory_path, reload=False):
        all_captions = []

        for dirpath, dirnames, filenames in os.walk(directory_path):
            for filename in filenames:
                if filename.endswith(".txt"):
                    file_path = os.path.join(dirpath, filename)
                    try:
                        with open(file_path, "r", encoding="utf-8") as infile:
                            captions = infile.read().splitlines()
                            all_captions.extend(captions)
                        print(f"Processed {file_path}")
                    except Exception as e:
                        print(f"Error processing {file_path}: {str(e)}")
                elif not filename.endswith(".png"):
                    print(f"Ignoring file {filename}")

        # Join all captions into a single string, separated by newlines
        result = "\n".join(all_captions)
        
        # Get the final directory name and append .txt
        output_filename = os.path.basename(os.path.normpath(directory_path)) + ".txt"
        
        return (result, output_filename)
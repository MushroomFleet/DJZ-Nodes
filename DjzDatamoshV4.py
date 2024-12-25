import torch
import numpy as np
import subprocess
import os
import tempfile
import json
from PIL import Image
import folder_paths

class DjzDatamoshV4:
    def __init__(self):
        self.type = "DjzDatamoshV4"
        self.output_node = True
        
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "target_images": ("IMAGE",),
                "source_images": ("IMAGE",),
                "mode": (["extract_and_transfer", "extract_only", "transfer_only"],),
                "vector_file": ("STRING", {
                    "default": "vectors.json",
                    "multiline": False
                }),
                "method": (["add", "replace"],),
                "gop_period": ("INT", {
                    "default": 1000,
                    "min": 1,
                    "max": 10000,
                    "step": 1
                })
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "style_transfer"
    CATEGORY = "image/effects"

    def batch_to_mpg(self, images, output_path, temp_dir, fps=30):
        """Convert image batch to MPG format for vector extraction"""
        frame_pattern = os.path.join(temp_dir, 'frame_%04d.png')
        
        # Save frames
        for i in range(len(images)):
            img_np = (images[i].cpu().numpy() * 255).astype(np.uint8)
            Image.fromarray(img_np).save(frame_pattern % i)
        
        # Convert to MPG using ffgac with specific settings
        subprocess.call(
            f'ffgac -i "{frame_pattern}" -an -mpv_flags +nopimb+forcemv '
            f'-qscale:v 0 -g 1000 -vcodec mpeg2video -f rawvideo -y "{output_path}"',
            shell=True
        )
        
        # Clean up frame files
        for i in range(len(images)):
            os.remove(frame_pattern % i)

    def get_vectors(self, input_video, temp_dir):
        """Extract motion vectors using ffgac and ffedit"""
        try:
            # Create temporary files
            temp_mpg = os.path.join(temp_dir, 'temp.mpg')
            temp_json = os.path.join(temp_dir, 'temp.json')
            
            # Extract video data using ffgac
            subprocess.call(
                f'ffgac -i "{input_video}" -an -mpv_flags +nopimb+forcemv -qscale:v 0 '
                f'-g 1000 -vcodec mpeg2video -f rawvideo -y "{temp_mpg}"',
                shell=True
            )
            
            # Extract motion vectors using ffedit
            subprocess.call(f'ffedit -i "{temp_mpg}" -f mv:0 -e "{temp_json}"', shell=True)
            
            # Read the extracted data
            with open(temp_json, 'r') as f:
                raw_data = json.load(f)
            
            # Clean up temporary files
            os.remove(temp_mpg)
            os.remove(temp_json)
            
            # Get vectors from each frame
            frames = raw_data['streams'][0]['frames']
            vectors = []
            
            for frame in frames:
                try:
                    vectors.append(frame['mv']['forward'])
                except:
                    vectors.append([])
            
            return vectors
            
        except Exception as e:
            print(f"Error extracting vectors: {e}")
            return None

    def apply_vectors(self, vectors, input_video, output_video, method='add', temp_dir=None):
        """Apply motion vectors using ffedit"""
        try:
            if not vectors:
                print("No vectors to apply")
                return False
                
            # Create temporary files
            temp_mpg = os.path.join(temp_dir, 'temp.mpg')
            script_path = os.path.join(temp_dir, 'apply_vectors.js')
            
            # Convert input to MPG
            subprocess.call(
                f'ffgac -i "{input_video}" -an -mpv_flags +nopimb+forcemv -qscale:v 0 '
                f'-g 1000 -vcodec mpeg2video -f rawvideo -y "{temp_mpg}"',
                shell=True
            )
            
            # Create JavaScript for vector application with export keyword
            to_add = '+' if method == 'add' else ''
            script_contents = f'''
            var vectors = {json.dumps(vectors)};
            var n_frames = 0;

            export function glitch_frame(frame) {{
                let fwd_mvs = frame["mv"]["forward"];
                if (!fwd_mvs || !vectors[n_frames]) {{
                    n_frames++;
                    return;
                }}

                for ( let i = 0; i < fwd_mvs.length; i++ ) {{
                    let row = fwd_mvs[i];
                    for ( let j = 0; j < row.length; j++ ) {{
                        let mv = row[j];
                        try {{
                            mv[0] {to_add}= vectors[n_frames][i][j][0];
                            mv[1] {to_add}= vectors[n_frames][i][j][1];
                        }} catch {{}}
                    }}
                }}

                n_frames++;
            }}
            '''
            
            # Write JavaScript file
            with open(script_path, 'w') as f:
                f.write(script_contents)
            
            # Apply vectors using ffedit
            subprocess.call(f'ffedit -i "{temp_mpg}" -f mv -s "{script_path}" -o "{output_video}"', shell=True)
            
            # Clean up temp files
            os.remove(temp_mpg)
            os.remove(script_path)
            
            return True
            
        except Exception as e:
            print(f"Error applying vectors: {e}")
            return False

    def video_to_frames(self, video_path, temp_dir):
        """Convert video back to image frames"""
        frames_pattern = os.path.join(temp_dir, 'output_%04d.png')
        subprocess.call([
            'ffmpeg',
            '-y',
            '-i', video_path,
            frames_pattern
        ])
        
        frames = []
        frame_idx = 1
        while True:
            frame_path = frames_pattern % frame_idx
            if not os.path.exists(frame_path):
                break
                
            img = Image.open(frame_path)
            frame_np = np.array(img).astype(np.float32) / 255.0
            frames.append(torch.from_numpy(frame_np))
            
            os.remove(frame_path)
            frame_idx += 1
            
        return torch.stack(frames) if frames else None

    def style_transfer(self, target_images, source_images, mode, vector_file, method, gop_period):
        print(f"Starting DjzDatamoshV4 in {mode} mode")
        print(f"Source images shape: {source_images.shape}")
        print(f"Target images shape: {target_images.shape}")
        
        temp_dir = folder_paths.get_temp_directory()
        output_dir = os.path.join(folder_paths.base_path, "custom_nodes", "motion_vectors")
        os.makedirs(output_dir, exist_ok=True)
        
        source_mpg = None
        target_mpg = None
        output_video = None
        vectors = []
        
        try:
            if mode in ["extract_only", "extract_and_transfer"]:
                # Convert source images to MPG
                source_mpg = os.path.join(temp_dir, 'source.mpg')
                self.batch_to_mpg(source_images, source_mpg, temp_dir)
                print("Converted source images to MPG")
                
                # Extract vectors
                print("Extracting motion vectors...")
                vectors = self.get_vectors(source_mpg, temp_dir)
                if vectors:
                    print(f"Extracted motion vectors from {len(vectors)} frames")
                    vector_file_path = os.path.join(output_dir, vector_file)
                    with open(vector_file_path, 'w') as f:
                        json.dump(vectors, f)
                    print(f"Saved vectors to {vector_file_path}")
                else:
                    print("Failed to extract motion vectors")
                    if mode == "extract_only":
                        return (source_images,)
                        
            if mode in ["transfer_only", "extract_and_transfer"]:
                # Load vectors if needed
                if mode == "transfer_only":
                    vector_file_path = os.path.join(output_dir, vector_file)
                    try:
                        with open(vector_file_path, 'r') as f:
                            vectors = json.load(f)
                        print(f"Loaded vectors from {len(vectors)} frames")
                    except FileNotFoundError:
                        print(f"Vector file {vector_file_path} not found")
                        return (target_images,)
                
                # Convert target images and apply vectors
                target_mpg = os.path.join(temp_dir, 'target.mpg')
                output_video = os.path.join(temp_dir, 'output.mpg')
                
                self.batch_to_mpg(target_images, target_mpg, temp_dir)
                print("Converted target images to MPG")
                
                print("Applying motion vectors...")
                if self.apply_vectors(vectors, target_mpg, output_video, method, temp_dir):
                    # Convert result back to frames
                    result = self.video_to_frames(output_video, temp_dir)
                    if result is not None:
                        print(f"Processing complete. Output shape: {result.shape}")
                        return (result,)
                
            print("Processing failed")
            return (target_images,)
            
        except Exception as e:
            print(f"Error during processing: {str(e)}")
            import traceback
            traceback.print_exc()
            return (target_images,)
            
        finally:
            # Clean up temporary files
            for file in [f for f in [source_mpg, target_mpg, output_video] if f is not None]:
                if os.path.exists(file):
                    try:
                        os.remove(file)
                    except Exception as e:
                        print(f"Error cleaning up {file}: {str(e)}")

# Register the node with ComfyUI
NODE_CLASS_MAPPINGS = {
    "DjzDatamoshV4": DjzDatamoshV4
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DjzDatamoshV4": "Djz Datamosh V4 (Style Transfer)"
}
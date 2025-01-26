import numpy as np
import torch
import cv2
import moderngl
from PIL import Image
import os

class GSL_Filter_V1:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),  # Batch of images input
                "effect_preset": (["custom", "grayscale", "edge_detection", "gaussian_blur", "pixelate", "wave_distortion", "chromatic_aberration"],),
                "intensity": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 5.0,
                    "step": 0.1
                }),
                "blur_radius": ("FLOAT", {
                    "default": 2.0,
                    "min": 0.1,
                    "max": 10.0,
                    "step": 0.1
                }),
                "edge_threshold": ("FLOAT", {
                    "default": 0.1,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01
                }),
                "pixelate_factor": ("INT", {
                    "default": 4,
                    "min": 1,
                    "max": 64,
                    "step": 1
                }),
                "wave_amplitude": ("FLOAT", {
                    "default": 0.1,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01
                }),
                "wave_frequency": ("FLOAT", {
                    "default": 5.0,
                    "min": 0.1,
                    "max": 50.0,
                    "step": 0.1
                }),
                "chromatic_shift": ("FLOAT", {
                    "default": 0.01,
                    "min": 0.0,
                    "max": 0.1,
                    "step": 0.001
                })
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "apply_gsl_filter"
    CATEGORY = "image/effects"

    def __init__(self):
        self.ctx = moderngl.create_standalone_context()
        self.setup_shaders()

    def setup_shaders(self):
        # Basic vertex shader
        vertex_shader = '''
            #version 330
            in vec2 position;
            in vec2 texcoord;
            out vec2 uv;
            void main() {
                gl_Position = vec4(position, 0.0, 1.0);
                uv = texcoord;
            }
        '''

        # Fragment shader with multiple effects
        fragment_shader = '''
            #version 330
            uniform sampler2D image;
            uniform int effect_type;
            uniform float intensity;
            uniform float blur_radius;
            uniform float edge_threshold;
            uniform int pixelate_factor;
            uniform float wave_amplitude;
            uniform float wave_frequency;
            uniform float chromatic_shift;
            uniform vec2 resolution;
            
            in vec2 uv;
            out vec4 fragColor;

            vec4 apply_grayscale() {
                vec4 color = texture(image, uv);
                float gray = dot(color.rgb, vec3(0.299, 0.587, 0.114));
                return mix(color, vec4(gray), intensity);
            }

            vec4 apply_edge_detection() {
                vec2 pixel = 1.0 / resolution;
                vec4 h = (
                    texture(image, uv + pixel * vec2(-1, 0)) * -1.0 +
                    texture(image, uv + pixel * vec2(1, 0)) * 1.0
                );
                vec4 v = (
                    texture(image, uv + pixel * vec2(0, -1)) * -1.0 +
                    texture(image, uv + pixel * vec2(0, 1)) * 1.0
                );
                float edge = length(h.rgb) + length(v.rgb);
                return vec4(vec3(edge > edge_threshold ? 1.0 : 0.0), 1.0);
            }

            vec4 apply_gaussian_blur() {
                vec4 color = vec4(0.0);
                vec2 pixel = 1.0 / resolution;
                float total_weight = 0.0;
                
                for(float x = -blur_radius; x <= blur_radius; x++) {
                    for(float y = -blur_radius; y <= blur_radius; y++) {
                        vec2 offset = vec2(x, y) * pixel;
                        float weight = exp(-(x*x + y*y) / (2.0 * blur_radius * blur_radius));
                        color += texture(image, uv + offset) * weight;
                        total_weight += weight;
                    }
                }
                
                return color / total_weight;
            }

            vec4 apply_pixelate() {
                vec2 pixel = vec2(pixelate_factor) / resolution;
                vec2 coord = floor(uv / pixel) * pixel;
                return texture(image, coord);
            }

            vec4 apply_wave_distortion() {
                vec2 offset = vec2(
                    sin(uv.y * wave_frequency) * wave_amplitude,
                    sin(uv.x * wave_frequency) * wave_amplitude
                );
                return texture(image, uv + offset);
            }

            vec4 apply_chromatic_aberration() {
                vec4 color;
                color.r = texture(image, uv + vec2(chromatic_shift, 0.0)).r;
                color.g = texture(image, uv).g;
                color.b = texture(image, uv - vec2(chromatic_shift, 0.0)).b;
                color.a = 1.0;
                return color;
            }

            void main() {
                switch(effect_type) {
                    case 0: fragColor = texture(image, uv); break;  // custom/bypass
                    case 1: fragColor = apply_grayscale(); break;
                    case 2: fragColor = apply_edge_detection(); break;
                    case 3: fragColor = apply_gaussian_blur(); break;
                    case 4: fragColor = apply_pixelate(); break;
                    case 5: fragColor = apply_wave_distortion(); break;
                    case 6: fragColor = apply_chromatic_aberration(); break;
                    default: fragColor = texture(image, uv);
                }
            }
        '''

        # Create shader program
        self.program = self.ctx.program(
            vertex_shader=vertex_shader,
            fragment_shader=fragment_shader
        )

        # Set up vertex data for a fullscreen quad
        vertices = np.array([
            # positions   texture coords
            -1.0, -1.0,   0.0, 0.0,
             1.0, -1.0,   1.0, 0.0,
             1.0,  1.0,   1.0, 1.0,
            -1.0,  1.0,   0.0, 1.0,
        ], dtype='f4')
        
        indices = np.array([0, 1, 2, 0, 2, 3], dtype='i4')
        
        self.vbo = self.ctx.buffer(vertices.tobytes())
        self.ibo = self.ctx.buffer(indices.tobytes())
        self.vao = self.ctx.vertex_array(
            self.program,
            [
                (self.vbo, '2f 2f', 'position', 'texcoord'),
            ],
            self.ibo
        )

    def process_image(self, image, effect_type, params):
        # Convert image to texture
        texture = self.ctx.texture(image.shape[:2][::-1], 4, image.tobytes())
        texture.use(0)

        # Create framebuffer
        fbo = self.ctx.framebuffer(
            color_attachments=[self.ctx.texture(image.shape[:2][::-1], 4)]
        )
        fbo.use()

        # Set uniforms
        self.program['image'] = 0
        self.program['effect_type'] = effect_type
        self.program['resolution'] = image.shape[:2][::-1]
        
        for param_name, value in params.items():
            if param_name in self.program:
                self.program[param_name] = value

        # Render
        self.vao.render()

        # Read result
        data = fbo.read(components=4)
        result = np.frombuffer(data, dtype=np.uint8).reshape(image.shape)

        # Clean up
        fbo.release()
        texture.release()

        return result

    def apply_gsl_filter(self, images, effect_preset, intensity, blur_radius, 
                        edge_threshold, pixelate_factor, wave_amplitude, 
                        wave_frequency, chromatic_shift):
        
        # Convert from torch tensor to numpy array
        batch_numpy = images.cpu().numpy()
        batch_size, height, width, channels = batch_numpy.shape
        
        # Map preset to effect type
        effect_map = {
            "custom": 0,
            "grayscale": 1,
            "edge_detection": 2,
            "gaussian_blur": 3,
            "pixelate": 4,
            "wave_distortion": 5,
            "chromatic_aberration": 6
        }
        effect_type = effect_map[effect_preset]
        
        # Prepare parameters
        params = {
            "intensity": intensity,
            "blur_radius": blur_radius,
            "edge_threshold": edge_threshold,
            "pixelate_factor": pixelate_factor,
            "wave_amplitude": wave_amplitude,
            "wave_frequency": wave_frequency,
            "chromatic_shift": chromatic_shift
        }
        
        # Process each image in the batch
        processed_batch = np.zeros_like(batch_numpy)
        for i in range(batch_size):
            print(f"Processing image {i+1}/{batch_size} with {effect_preset} effect...")
            
            # Convert to RGBA for processing
            frame = (batch_numpy[i] * 255).astype(np.uint8)
            if frame.shape[2] == 3:
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2RGBA)
            
            # Apply GSL effect
            processed = self.process_image(frame, effect_type, params)
            
            # Convert back to RGB and normalize
            if processed.shape[2] == 4:
                processed = cv2.cvtColor(processed, cv2.COLOR_RGBA2RGB)
            processed_batch[i] = processed.astype(np.float32) / 255.0
            
            print(f"Image {i+1} processed successfully")
        
        print("Batch processing complete!")
        
        # Convert back to torch tensor
        return (torch.from_numpy(processed_batch).to(images.device),)

    def __del__(self):
        # Clean up OpenGL resources
        if hasattr(self, 'ctx'):
            self.ctx.release()

NODE_CLASS_MAPPINGS = {
    "GSL_Filter_V1": GSL_Filter_V1
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GSL_Filter_V1": "GSL Filter v1"
}
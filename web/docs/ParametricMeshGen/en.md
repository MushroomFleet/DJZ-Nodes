# Parametric Mesh Generator

The Parametric Mesh Generator is a ComfyUI node that creates 3D parametric meshes and generates their preview images. This node is particularly useful for creating 3D geometric shapes that can be exported as OBJ files for use in 3D applications.

## Parameters

### Required Parameters

- **resolution** (Integer)
  - Default: 30
  - Range: 10 to 100
  - Controls the mesh density/detail level
  - Higher values create smoother surfaces but increase processing time

- **scale** (Float)
  - Default: 1.0
  - Range: 0.1 to 10.0
  - Controls the overall size of the generated mesh
  - Larger values create bigger meshes

- **amplitude** (Float)
  - Default: 0.5
  - Range: 0.0 to 2.0
  - Controls the intensity of surface deformation
  - Higher values create more pronounced surface variations

- **frequency** (Float)
  - Default: 1.0
  - Range: 0.1 to 5.0
  - Controls how often the surface deformation pattern repeats
  - Higher values create more frequent surface variations

- **phase** (Float)
  - Default: 0.0
  - Range: -3.14159 to 3.14159 (negative Pi to Pi)
  - Controls the offset of the surface deformation pattern
  - Useful for creating different variations of the same basic shape

## Outputs

1. **preview_image** (IMAGE)
   - A 3D preview render of the generated mesh
   - Shows the mesh from a 45-degree angle with cyan surface color and black edges

2. **obj_path** (STRING)
   - File path to the exported OBJ file
   - The file is saved in the ComfyUI output/OBJ directory
   - Each generated file has a unique timestamp in its name

## Usage

1. Add the node to your ComfyUI workflow
2. Adjust the parameters to create the desired shape:
   - Start with default values and adjust gradually
   - Use resolution carefully as higher values impact performance
   - Combine scale and amplitude to control the overall shape
   - Use frequency and phase to fine-tune surface details
3. The node will automatically generate both a preview image and an OBJ file
4. The OBJ file can be imported into most 3D software for further use

## Technical Details

- The node generates a parametric surface using trigonometric functions
- The mesh is created using a grid of vertices connected by triangular faces
- Preview images are generated using matplotlib with a 3D projection
- OBJ files are saved with proper vertex and face information for 3D software compatibility

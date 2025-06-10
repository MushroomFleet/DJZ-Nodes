# Parametric Mesh Generator V2

An enhanced version of the Parametric Mesh Generator that creates 3D parametric meshes with advanced controls. This node offers multiple surface types, complex deformations, and improved visualization options.

## Parameters

### Surface Configuration

- **surface_type** (Dropdown)
  - Options: SPHERE, TORUS, KLEIN_BOTTLE, MOBIUS
  - Default: SPHERE
  - Determines the base geometric shape of the mesh

- **resolution** (Integer)
  - Default: 30
  - Range: 10 to 200
  - Controls the mesh density/detail level
  - Higher values create smoother surfaces but increase processing time

- **scale** (Float)
  - Default: 1.0
  - Range: 0.1 to 10.0
  - Controls the overall size of the generated mesh

### Primary Wave Deformation

- **amplitude** (Float)
  - Default: 0.5
  - Range: 0.0 to 2.0
  - Controls the intensity of primary surface deformation

- **frequency** (Float)
  - Default: 1.0
  - Range: 0.1 to 5.0
  - Controls how often the primary deformation pattern repeats

- **phase** (Float)
  - Default: 0.0
  - Range: -3.14159 to 3.14159 (negative Pi to Pi)
  - Controls the offset of the primary deformation pattern

### Secondary Wave Deformation

- **secondary_amplitude** (Float)
  - Default: 0.0
  - Range: 0.0 to 2.0
  - Controls the intensity of secondary surface deformation
  - Allows for more complex surface patterns

- **secondary_frequency** (Float)
  - Default: 2.0
  - Range: 0.1 to 5.0
  - Controls how often the secondary deformation pattern repeats

- **secondary_phase** (Float)
  - Default: 0.0
  - Range: -3.14159 to 3.14159 (negative Pi to Pi)
  - Controls the offset of the secondary deformation pattern

### Surface Properties

- **smoothness** (Integer)
  - Default: 1
  - Range: 0 to 3
  - Controls the smoothing groups in the OBJ file
  - 0 disables smoothing, higher values create smoother surfaces

- **twist** (Float)
  - Default: 0.0
  - Range: -2.0 to 2.0
  - Applies a twisting deformation to the surface
  - Positive values twist clockwise, negative counterclockwise

### Preview Settings

- **preview_elevation** (Integer)
  - Default: 30
  - Range: 0 to 90
  - Controls the vertical viewing angle in the preview

- **preview_azimuth** (Integer)
  - Default: 45
  - Range: 0 to 360
  - Controls the horizontal viewing angle in the preview

- **mesh_color** (Dropdown)
  - Options: CYAN, RED, GREEN, BLUE, PURPLE, ORANGE
  - Default: CYAN
  - Sets the color of the mesh in the preview

- **edge_visibility** (Float)
  - Default: 0.3
  - Range: 0.0 to 1.0
  - Controls the visibility of mesh edges in the preview
  - 0.0 hides edges, 1.0 shows full edge lines

## Outputs

1. **preview_image** (IMAGE)
   - A 3D preview render of the generated mesh
   - Shows the mesh from customizable angles with selected color and edge visibility

2. **obj_path** (STRING)
   - File path to the exported OBJ file
   - The file is saved in the ComfyUI output/OBJ directory
   - Filename includes the surface type and timestamp

## Surface Types

### SPHERE
- Basic spherical surface that can be deformed with waves
- Ideal for creating planet-like objects or organic shapes

### TORUS
- Donut-shaped surface with major and minor radii
- Great for creating ring-like structures or twisted loops

### KLEIN_BOTTLE
- Non-orientable surface that passes through itself
- Useful for creating mathematical art or abstract shapes

### MOBIUS
- Single-sided surface with a half twist
- Perfect for creating infinite loop animations or mathematical demonstrations

## Usage Tips

1. Start with the desired surface type and adjust basic parameters:
   - Use resolution carefully as it significantly impacts performance
   - Adjust scale to get the right overall size

2. Add primary deformation:
   - Use amplitude for basic surface variation
   - Adjust frequency to control pattern density
   - Fine-tune with phase for pattern positioning

3. Layer secondary deformation:
   - Start with low secondary_amplitude
   - Use different frequency than primary for interesting patterns
   - Adjust phase to align patterns as needed

4. Fine-tune surface properties:
   - Use smoothness to control surface interpolation
   - Experiment with twist for unique variations

5. Perfect the preview:
   - Adjust elevation and azimuth for the best view
   - Choose a color that highlights surface details
   - Fine-tune edge_visibility for clear structure

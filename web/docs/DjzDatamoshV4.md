# DjzDatamoshV4 Node

## Description
The DjzDatamoshV4 node is an advanced image effects node that performs motion vector-based style transfer between images. It can extract motion vectors from a source sequence of images and apply them to a target sequence, creating unique datamoshing effects. This node is particularly useful for creating artistic glitch effects and style transfers between different image sequences.

## Parameters

### Required Inputs

1. **target_images** (IMAGE)
   - The sequence of images that will receive the motion vector effects
   - These are the base images that will be modified

2. **source_images** (IMAGE)
   - The sequence of images to extract motion vectors from
   - These images define the movement patterns that will be applied

3. **mode** (Dropdown)
   - Options:
     - `extract_and_transfer`: Extract vectors from source and apply to target
     - `extract_only`: Only extract vectors from source images
     - `transfer_only`: Only apply previously saved vectors to target images
   - Controls the operation mode of the node

4. **vector_file** (STRING)
   - Default: "vectors.json"
   - The filename to save or load motion vectors
   - Used for storing extracted vectors or loading previously saved ones

5. **method** (Dropdown)
   - Options:
     - `add`: Add the motion vectors to existing motion
     - `replace`: Replace existing motion with new vectors
   - Determines how motion vectors are applied to the target images

6. **gop_period** (INTEGER)
   - Default: 1000
   - Range: 1-10000
   - Step: 1
   - Controls the Group of Pictures (GOP) period for MPEG encoding
   - Higher values create longer segments of related frames

## Output
- Returns a modified IMAGE sequence with the applied motion vector effects

## Usage

### Basic Workflow
1. Connect a sequence of source images (for motion vector extraction)
2. Connect a sequence of target images (to receive the effects)
3. Choose the desired operation mode
4. Set the vector file name if you want to save/load vectors
5. Select the application method (add/replace)
6. Adjust the GOP period if needed

### Mode-Specific Usage

#### Extract and Transfer Mode
- Extracts motion vectors from source images and immediately applies them to target images
- Best for direct style transfer between two image sequences

#### Extract Only Mode
- Only extracts and saves motion vectors from source images
- Useful when you want to save motion patterns for later use

#### Transfer Only Mode
- Applies previously saved motion vectors to target images
- Requires an existing vector file from a previous extraction

## Notes
- The node requires external tools (ffgac and ffedit) for motion vector processing
- Vector files are saved in the 'custom_nodes/motion_vectors' directory
- Processing may take some time depending on the number and size of images
- If processing fails, the node returns the unmodified target images

# DjzDatamoshV5 Node

## Description
The DjzDatamoshV5 node is an image effects node that creates unique datamoshing effects by sorting and reordering frames based on their file sizes. Unlike previous versions that use motion vectors, this node analyzes the compressed size of each frame to create interesting visual transitions. This approach can create distinctive glitch-like effects by grouping visually similar frames together.

## Parameters

### Required Inputs

1. **images** (IMAGE)
   - The sequence of images to process
   - Requires at least 2 images in the sequence
   - Input shape should be [batch_size, height, width, channels]

2. **reverse_sort** (BOOLEAN)
   - Default: True
   - When True: Sorts frames from largest to smallest file size
   - When False: Sorts frames from smallest to largest file size
   - Controls the ordering direction of the sorted frames

3. **start_frame** (INTEGER)
   - Default: 0
   - Range: 0-999
   - Step: 1
   - Defines the first frame to include in the sorting process
   - Frames before this index maintain their original order

4. **end_frame** (INTEGER)
   - Default: -1 (processes until the last frame)
   - Range: -1 to 999
   - Step: 1
   - Defines the last frame to include in the sorting process
   - Use -1 to process until the end of the sequence
   - Frames after this index maintain their original order

## Output
- Returns a modified IMAGE sequence with frames reordered based on their file sizes
- Output maintains the same dimensions as the input

## Usage

### Basic Operation
1. Connect a sequence of images to the node
2. Choose whether to sort by largest or smallest file size using reverse_sort
3. Optionally set start_frame and end_frame to limit the range of sorted frames
4. The node will process the frames and return the reordered sequence

### Advanced Usage
- Use start_frame and end_frame to create partial effects:
  - Sort only the middle section of your sequence
  - Keep intros and outros intact while sorting the main content
  - Create gradual transitions between ordered and sorted sections

### Tips for Best Results
- Sequences with varying visual complexity will produce more dramatic effects
- Longer sequences provide more opportunities for interesting sorting patterns
- Experiment with reverse_sort to find the most visually appealing arrangement
- Use partial sorting (with start_frame and end_frame) to maintain some temporal coherence

## Technical Process
1. Converts input frames to PNG format
2. Calculates file size for each frame
3. Sorts frames within the specified range based on file size
4. Maintains original order for frames outside the specified range
5. Reconstructs video from the reordered frames
6. Converts back to tensor format for output

## Notes
- Requires at least 2 input images to function
- Processing time increases with the number of input frames
- File sizes can vary based on image content complexity
- Returns unmodified input if any processing step fails

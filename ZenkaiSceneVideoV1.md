# Zenkai Scene Video V1

This node is designed to load video files from selected folders within the `/scenevideo/` directory.

## Overview

The Zenkai Scene Video V1 node provides a convenient way to load videos from organized scene folders. It combines folder selection functionality with video loading capabilities, allowing you to easily manage and access different video scenes in your workflow.

## Inputs

- **folder**: Select a folder from the `/scenevideo/` directory containing video files
- **mode**: Choose how to select videos from the folder:
  - `single_video`: Use the index parameter to select a specific video
  - `incremental_video`: Increment through videos using the index parameter
  - `random`: Use seed to randomly select a video
- **seed**: Random seed for selecting videos in random mode
- **index**: Video index for selection in single_video or incremental_video modes
- **skip_frames**: Number of frames to skip from the beginning of the video
- **max_frames**: Maximum number of frames to load (0 = all remaining)
- **memory_limit_mb**: Memory limit for video loading in MB (0 = auto)
- **force_rate**: Force a specific frame rate (0 = use source frame rate)
- **label**: Label for the video batch
- **pattern**: File pattern to filter video files (e.g. `*.mp4`)

### Optional Inputs

- **meta_batch**: Video batch manager for frame batching
- **vae**: VAE model for encoding video frames

## Outputs

- **frames**: Tensor containing the loaded video frames
- **frame_count**: Number of frames loaded
- **audio**: Audio data from the video if available
- **video_info**: Information about the video such as dimensions, frame rate, etc.
- **filename_text**: Filename of the loaded video

## Usage

1. Create a folder structure under the `/scenevideo/` directory:
   ```
   /scenevideo/
     /scene1/
       video1.mp4
       video2.mp4
     /scene2/
       video3.mp4
       ...
   ```

2. Use the node to select a scene folder and load videos from it.

3. The node will automatically detect all folders in the `/scenevideo/` directory and provide them as dropdown options.

4. Videos will be selected based on the chosen mode (single, incremental, or random) and the index/seed parameters.

## Example

To load video frames from a specific scene folder:
1. Select the desired folder from the dropdown
2. Choose the selection mode (e.g., "random")
3. Set the seed value if using random mode
4. Adjust other parameters as needed (skip_frames, max_frames, etc.)
5. Connect the outputs to downstream nodes in your workflow

## Notes

- The `/scenevideo/` directory is automatically created when the node is initialized
- If no folders exist in `/scenevideo/`, a "none" option will be displayed
- When using the meta_batch input, frames will be loaded in batches according to the batch manager settings

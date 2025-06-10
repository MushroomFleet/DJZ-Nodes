# LoadVideoDirectory

This custom node allows you to load video frames from a directory containing video files. It supports multiple video formats (mp4, avi, mov, mkv) and provides various modes for video selection and frame extraction.

## Input Parameters

- **mode** (Required)
  - Options: "single_video", "incremental_video", "random"
  - Determines how videos are selected from the directory:
    - `single_video`: Loads frames from a specific video using the index parameter
    - `incremental_video`: Loads frames sequentially through the video directory
    - `random`: Randomly selects a video based on the seed parameter

- **seed** (Required)
  - Default: 0
  - Range: 0 to 0xffffffffffffffff
  - Used as the random seed when mode is set to "random"
  - Determines which video is selected in random mode

- **index** (Required)
  - Default: 0
  - Range: 0 to 150000
  - Step: 1
  - Specifies which video to load when using "single_video" mode
  - Acts as a starting point for "incremental_video" mode

- **skip_frames** (Required)
  - Default: 0
  - Range: 0 to 999999
  - Step: 1
  - Number of frames to skip from the start of the video

- **max_frames** (Required)
  - Default: 0
  - Range: 0 to 999999
  - Step: 1
  - Maximum number of frames to load
  - If set to 0, loads all frames after skip_frames

- **label** (Required)
  - Default: 'Video Batch 001'
  - A label for the batch of frames being loaded
  - Useful for organization and tracking

- **path** (Required)
  - Default: ''
  - The directory path containing the video files
  - Must be a valid directory path

- **pattern** (Required)
  - Default: '*'
  - File pattern for matching video files in the directory
  - Supports glob patterns (e.g., '*.mp4', 'video_*.avi')

## Outputs

1. **frames** (IMAGE)
   - A tensor containing the loaded video frames
   - Format: [batch, height, width, channels]
   - Normalized RGB values (0-1 range)

2. **filename_text** (STRING)
   - The filename of the currently loaded video

## Usage Examples

1. **Loading a Specific Video**
   - Set mode to "single_video"
   - Specify the video index
   - Useful when you want to process a particular video repeatedly

2. **Sequential Processing**
   - Set mode to "incremental_video"
   - The node will process videos in alphabetical order
   - Good for batch processing multiple videos

3. **Random Video Selection**
   - Set mode to "random"
   - Set a seed value for reproducible randomization
   - Useful for training or creating variations

## Notes

- The node automatically converts video frames from BGR to RGB color space
- Frames are normalized to the 0-1 range for compatibility with other nodes
- Invalid video files or frames are automatically skipped
- The node supports recursive directory searching when using patterns
- Memory usage depends on the number of frames being loaded

# Load Video Batch Frame

A versatile node for loading individual frames from video files in a directory. This node supports multiple video formats and various loading modes, making it ideal for video-based workflows in ComfyUI.

## Supported Video Formats

- `.mp4`
- `.avi`
- `.mov`
- `.mkv`

## Input Parameters

- **mode**: Select how video frames are loaded:
  - `single_video`: Load a specific frame from a specific video using index
  - `incremental_video`: Load frames sequentially across videos
  - `random`: Load a random frame based on seed value
- **seed**: Random seed for the random mode
  - Default: 0
  - Range: 0 to 18446744073709551615
- **index**: The index of the video in the directory listing
  - Default: 0
  - Range: 0-150000
  - Used to select which video to load from
- **frame**: The frame number to extract from the video
  - Default: 0
  - Range: 0-999999
  - Note: If frame number exceeds video length, last frame is used
- **label**: A label for the batch (for organization)
  - Default: 'Video Batch 001'
- **path**: Directory path containing the video files
  - Must be a valid directory path
- **pattern**: File matching pattern
  - Default: '*'
  - Supports glob patterns (e.g., '*.mp4', 'video_*')

## Outputs

- **frame**: The loaded video frame as an IMAGE tensor
  - Format: RGB
  - Normalized to 0-1 range
  - Shape: [batch, height, width, channels]
- **filename_text**: The filename of the source video

## How It Works

### Single Video Mode
1. Loads the video at the specified index in the directory
2. Extracts the requested frame number
3. Returns the frame and filename

### Incremental Video Mode
1. Keeps track of current position in the video list
2. Loads frames sequentially across videos
3. Wraps back to start when reaching the end

### Random Mode
1. Uses the provided seed for randomization
2. Selects a random video from the directory
3. Loads the specified frame from the random video

## Frame Processing

1. Video frames are loaded using OpenCV
2. Converted from BGR to RGB color space
3. Normalized to 0-1 range
4. Converted to PyTorch tensor
5. Reshaped to match ComfyUI's expected format

## Error Handling

- Validates directory path existence
- Handles invalid video files
- Manages frame number overflow
- Returns None for invalid video/frame combinations

## Use Cases

- Training data preparation from videos
- Frame extraction for video editing
- Random frame sampling for AI training
- Sequential video processing
- Batch processing of multiple video files

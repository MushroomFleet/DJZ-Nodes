# LoadVideoDirectoryV2

A powerful and flexible ComfyUI custom node for loading video files from a directory with advanced batch processing capabilities, memory management, and audio support.

## Features

- Multiple video loading modes (single, incremental, random)
- Batch processing support
- Automatic memory management
- Audio extraction capabilities
- Frame skipping and limiting
- Customizable frame rate control
- Support for multiple video formats (mp4, avi, mov, mkv)

## Parameters

### Required Parameters

- **mode** (single_video/incremental_video/random)
  - `single_video`: Loads a specific video using the index parameter
  - `incremental_video`: Cycles through videos incrementally based on index
  - `random`: Selects a random video using the seed parameter

- **seed** (default: 0)
  - Used for random video selection when mode is set to "random"
  - Range: 0 to 0xffffffffffffffff

- **index** (default: 0)
  - Video selection index for single_video mode
  - Base index for incremental mode
  - Range: 0 to 150000

- **skip_frames** (default: 0)
  - Number of frames to skip from the start of the video
  - Range: 0 to 999999

- **max_frames** (default: 0)
  - Maximum number of frames to load
  - Set to 0 for all frames
  - Range: 0 to 999999

- **memory_limit_mb** (default: 0)
  - Memory limit in megabytes for frame loading
  - Set to 0 for automatic memory management
  - Range: 0 to 128000MB (128GB)

- **force_rate** (default: 0)
  - Override the video's original frame rate
  - Set to 0 to use the video's native frame rate
  - Range: 0 to 60 fps

- **label** (default: 'Video Batch 001')
  - Custom label for the batch process
  - Used for organization and identification

- **path**
  - Directory path containing the video files
  - Must be a valid existing directory

- **pattern** (default: '*')
  - File matching pattern for video selection
  - Supports glob patterns (e.g., '*.mp4', 'video_*')

### Optional Parameters

- **meta_batch** (VHS_BatchManager)
  - Batch processing manager for coordinated video loading
  - Handles frame distribution across multiple processes

- **vae** (VAE)
  - VAE model for potential preprocessing
  - Optional parameter for integration with other nodes

## Outputs

1. **frames** (IMAGE)
   - Tensor containing the loaded video frames
   - Format: [frames, height, width, channels]

2. **frame_count** (INT)
   - Number of frames successfully loaded

3. **audio** (AUDIO)
   - Audio data extracted from the video
   - Includes waveform, sample rate, and timing information

4. **video_info** (VHS_VIDEOINFO)
   - Comprehensive video metadata including:
     - Source FPS, frame count, duration
     - Source dimensions (width, height)
     - Loaded frame information
     - Processing parameters

5. **filename_text** (STRING)
   - Name of the currently processed video file

## Technical Details

### Memory Management
- Automatic memory limit calculation based on available system memory
- Manual memory limit option for controlled resource usage
- Frame batch loading to prevent memory overflow

### Audio Processing
- Audio extraction at 44.1kHz sample rate
- Stereo channel support
- Synchronized with frame timing
- FFmpeg-based extraction for reliability

### Video Processing
- OpenCV-based frame extraction
- RGB color space conversion
- Float32 precision (0-1 range)
- Efficient frame generator implementation

## Usage Tips

1. For large videos, use `memory_limit_mb` to prevent out-of-memory errors
2. Use `skip_frames` and `max_frames` to process specific sections of videos
3. The `pattern` parameter can help filter specific video files in the directory
4. `force_rate` can be useful for maintaining consistent frame timing across different videos
5. Use incremental mode with meta_batch for efficient batch processing of multiple videos

## Error Handling

The node includes comprehensive error handling for:
- Invalid paths or patterns
- Memory limitations
- Video loading failures
- Audio extraction issues
- Frame reading errors

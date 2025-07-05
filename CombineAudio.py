import os
import sys
import math
import time
from pydub import AudioSegment

class CombineAudio:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "audio1": ("AUDIO",),
                "audio2": ("AUDIO",),
                "volume1": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 2.0,
                    "step": 0.1
                }),
                "volume2": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 2.0,
                    "step": 0.1
                }),
            },
        }

    RETURN_TYPES = ("AUDIO",)
    FUNCTION = "combine_audio"
    CATEGORY = "audio"

    def combine_audio(self, audio1, audio2, volume1=1.0, volume2=1.0):
        try:
            # Enhanced input format detection with detailed logging
            print(f"Audio1 type: {type(audio1)}", file=sys.stderr)
            print(f"Audio2 type: {type(audio2)}", file=sys.stderr)
            
            # Process audio1
            if isinstance(audio1, dict):
                print(f"Audio1 dict keys: {list(audio1.keys())}", file=sys.stderr)
                if 'file' in audio1:
                    audio1_file = audio1['file']
                elif 'filename' in audio1:  # Alternative key name
                    audio1_file = audio1['filename']
                elif 'path' in audio1:  # Another alternative key name
                    audio1_file = audio1['path']
                else:
                    print(f"Audio1 contents: {audio1}", file=sys.stderr)
                    raise ValueError("Could not find file path in audio1")
            elif hasattr(audio1, 'file'):
                audio1_file = audio1.file
            elif hasattr(audio1, 'filename'):  # Alternative attribute name
                audio1_file = audio1.filename
            elif hasattr(audio1, 'path'):  # Another alternative attribute name
                audio1_file = audio1.path
            else:
                print(f"Audio1 dir attributes: {dir(audio1)}", file=sys.stderr)
                raise ValueError("Could not extract file path from audio1")
                
            # Process audio2
            if isinstance(audio2, dict):
                print(f"Audio2 dict keys: {list(audio2.keys())}", file=sys.stderr)
                if 'file' in audio2:
                    audio2_file = audio2['file']
                elif 'filename' in audio2:  # Alternative key name
                    audio2_file = audio2['filename']
                elif 'path' in audio2:  # Another alternative key name
                    audio2_file = audio2['path']
                else:
                    print(f"Audio2 contents: {audio2}", file=sys.stderr)
                    # Try to use the same file as audio1 for testing if we can't find audio2
                    print(f"WARNING: Using audio1 file as fallback for audio2", file=sys.stderr)
                    audio2_file = audio1_file
            elif hasattr(audio2, 'file'):
                audio2_file = audio2.file
            elif hasattr(audio2, 'filename'):  # Alternative attribute name
                audio2_file = audio2.filename
            elif hasattr(audio2, 'path'):  # Another alternative attribute name
                audio2_file = audio2.path
            else:
                print(f"Audio2 dir attributes: {dir(audio2)}", file=sys.stderr)
                # Try to use the same file as audio1 for testing if we can't find audio2
                print(f"WARNING: Using audio1 file as fallback for audio2", file=sys.stderr)
                audio2_file = audio1_file
                
            # Load the audio files and print debug info
            print(f"Loading audio1 from: {audio1_file}", file=sys.stderr)
            sound1 = AudioSegment.from_file(audio1_file)
            print(f"Loading audio2 from: {audio2_file}", file=sys.stderr)
            sound2 = AudioSegment.from_file(audio2_file)
            
            # Print debug info about the loaded audio
            print(f"Audio1 format - Channels: {sound1.channels}, Sample rate: {sound1.frame_rate}, Duration: {len(sound1)}ms", file=sys.stderr)
            print(f"Audio2 format - Channels: {sound2.channels}, Sample rate: {sound2.frame_rate}, Duration: {len(sound2)}ms", file=sys.stderr)
            
            # Convert both audio tracks to a consistent format for reliable mixing
            # Use standard CD quality parameters
            target_sample_rate = 44100  # Standard sample rate
            target_channels = 2  # Stereo
            
            # Normalize audio1 format
            if sound1.frame_rate != target_sample_rate or sound1.channels != target_channels:
                print(f"Converting audio1 to {target_channels} channels at {target_sample_rate}Hz", file=sys.stderr)
                sound1 = sound1.set_frame_rate(target_sample_rate)
                sound1 = sound1.set_channels(target_channels)
            
            # Normalize audio2 format
            if sound2.frame_rate != target_sample_rate or sound2.channels != target_channels:
                print(f"Converting audio2 to {target_channels} channels at {target_sample_rate}Hz", file=sys.stderr)
                sound2 = sound2.set_frame_rate(target_sample_rate)
                sound2 = sound2.set_channels(target_channels)
            
            # Apply volume adjustments (pydub uses dB, so we convert from linear scale)
            # Debug the original levels
            print(f"Original audio1 RMS level: {sound1.dBFS} dBFS", file=sys.stderr)
            print(f"Original audio2 RMS level: {sound2.dBFS} dBFS", file=sys.stderr)
            
            # Using the formula: dB = 20 * log10(volume)
            if volume1 > 0:  # Avoid log(0) error
                db_change1 = 20 * math.log10(float(volume1))
                print(f"Applying {db_change1} dB gain to audio1 (volume factor: {volume1})", file=sys.stderr)
                sound1 = sound1.apply_gain(db_change1)  # Use apply_gain method for clearer intention
            elif volume1 == 0:  # Handle zero volume case
                print(f"Muting audio1 (volume: {volume1})", file=sys.stderr)
                sound1 = sound1.apply_gain(-100)  # Apply extreme attenuation
                
            if volume2 > 0:  # Avoid log(0) error
                db_change2 = 20 * math.log10(float(volume2))
                print(f"Applying {db_change2} dB gain to audio2 (volume factor: {volume2})", file=sys.stderr)
                sound2 = sound2.apply_gain(db_change2)  # Use apply_gain method for clearer intention
            elif volume2 == 0:  # Handle zero volume case
                print(f"Muting audio2 (volume: {volume2})", file=sys.stderr)
                sound2 = sound2.apply_gain(-100)  # Apply extreme attenuation
                
            # Debug the adjusted levels
            print(f"Adjusted audio1 RMS level: {sound1.dBFS} dBFS", file=sys.stderr)
            print(f"Adjusted audio2 RMS level: {sound2.dBFS} dBFS", file=sys.stderr)
            
            # Trim audio2 to match audio1's length (audio1 determines the output length)
            if len(sound1) < len(sound2):
                # Trim audio2 to match audio1's length
                print(f"Trimming audio2 from {len(sound2)}ms to match audio1 length: {len(sound1)}ms", file=sys.stderr)
                sound2 = sound2[:len(sound1)]
            else:
                # If audio1 is longer than audio2, pad audio2 with silence
                diff = len(sound1) - len(sound2)
                print(f"Padding audio2 with {diff}ms of silence to match audio1 length", file=sys.stderr)
                silence = AudioSegment.silent(duration=diff, frame_rate=sound2.frame_rate)
                silence = silence.set_channels(sound2.channels)
                sound2 = sound2 + silence
            
            # Use pydub's standard overlay to mix the tracks
            # This ensures the user's volume settings are directly respected
            print(f"Mixing audio tracks using standard overlay with user-defined volume levels", file=sys.stderr)
            combined = sound1.overlay(sound2, position=0)
            
            # Critical: Verify combined length matches audio1 length EXACTLY
            print(f"Before length check - Audio1: {len(sound1)}ms, Combined: {len(combined)}ms", file=sys.stderr)
            
            # Force the combined length to match audio1's length exactly
            if len(combined) != len(sound1):
                print(f"WARNING: Combined length {len(combined)}ms differs from audio1 length {len(sound1)}ms - forcing correction", file=sys.stderr)
                if len(combined) > len(sound1):
                    # Trim if somehow longer
                    combined = combined[:len(sound1)]
                else:
                    # Pad if somehow shorter
                    diff = len(sound1) - len(combined)
                    silence = AudioSegment.silent(duration=diff, frame_rate=combined.frame_rate)
                    silence = silence.set_channels(combined.channels)
                    combined = combined + silence
                    
            # Verify the combined audio matches audio1 length
            print(f"After correction - Audio1: {len(sound1)}ms, Combined: {len(combined)}ms", file=sys.stderr)
            print(f"Combined audio RMS level: {combined.dBFS} dBFS", file=sys.stderr)
            
            # Use timestamp to create unique filename preventing any caching issues
            timestamp = int(time.time())
            final_output_path = os.path.join(os.path.dirname(audio1_file), f"combined_audio_{timestamp}.wav")
            
            print(f"Exporting to unique path: {final_output_path}", file=sys.stderr)
            
            # Export the combined audio directly as WAV
            # This avoids any potential issues with MP4 containers not respecting duration
            combined.export(final_output_path, format="wav")
            
            # Verify the file exists and has the right length
            try:
                verify_audio = AudioSegment.from_file(final_output_path)
                print(f"Verified output file length: {len(verify_audio)}ms (Expected: {len(sound1)}ms)", file=sys.stderr)
                
                if abs(len(verify_audio) - len(sound1)) > 50:  # Allow small tolerance of 50ms
                    print(f"WARNING: Output length doesn't match expected. Using direct trimming.", file=sys.stderr)
                    # Load, trim/pad and re-save if needed
                    if len(verify_audio) > len(sound1):
                        verify_audio = verify_audio[:len(sound1)]
                    else:
                        pad = AudioSegment.silent(duration=len(sound1) - len(verify_audio), frame_rate=verify_audio.frame_rate)
                        verify_audio = verify_audio + pad
                    
                    verify_audio.export(final_output_path, format="wav")
            except Exception as e:
                print(f"Error during verification: {str(e)}", file=sys.stderr)
            
            # Create new audio output with the structure expected by ComfyUI
            print(f"Creating audio output structure matching input format", file=sys.stderr)
            
            # Determine the appropriate output format based on input format
            # Prefer dictionary format as it's more common in ComfyUI
            if isinstance(audio1, dict):
                reference_audio = audio1
                is_dict = True
            elif isinstance(audio2, dict):
                reference_audio = audio2
                is_dict = True
            else:
                reference_audio = audio1
                is_dict = False
                
            if is_dict:
                # Handle dictionary-style audio objects (default for ComfyUI)
                print(f"Using dictionary format for output", file=sys.stderr)
                combined_audio = {}
                
                # Copy structure from reference but update key fields
                for key in reference_audio:
                    if key != 'file' and key != 'filename' and key != 'path':
                        combined_audio[key] = reference_audio[key]
                
                # Set the output file path - make sure we use the most recent final_output_path
                print(f"Setting output file path to: {final_output_path}", file=sys.stderr)
                combined_audio['file'] = final_output_path
                
                # Check if path exists to confirm it's correct
                if not os.path.exists(final_output_path):
                    print(f"WARNING: Output file path doesn't exist: {final_output_path}", file=sys.stderr)
                
                # Use audio1's duration for the output (since we're trimming audio2 to match audio1)
                if isinstance(audio1, dict) and 'duration' in audio1:
                    combined_audio['duration'] = audio1['duration']
                else:
                    combined_audio['duration'] = len(sound1) / 1000.0  # Convert ms to seconds
                
                print(f"Setting output duration to audio1's duration: {combined_audio['duration']}s", file=sys.stderr)
                    
                # Set start time to 0
                combined_audio['start_time'] = 0.0
            else:
                # Handle object-style audio objects (legacy support)
                print(f"Using object format for output", file=sys.stderr)
                try:
                    # Try to create an instance of the same class
                    # Use audio1's duration for consistency
                    duration = getattr(audio1, 'duration', len(sound1) / 1000.0) if hasattr(audio1, 'duration') else len(sound1) / 1000.0
                    print(f"Setting output duration to audio1's duration: {duration}s", file=sys.stderr)
                    
                    combined_audio = reference_audio.__class__(
                        file=final_output_path,
                        start_time=0.0,
                        duration=duration
                    )
                except Exception as e:
                    # Fallback to dictionary format if object creation fails
                    print(f"Failed to create object format output: {e}, falling back to dict", file=sys.stderr)
                    # IMPORTANT: Always use audio1's duration, not the combined duration
                    audio1_duration_seconds = len(sound1) / 1000.0
                    print(f"Using audio1 duration for fallback output: {audio1_duration_seconds}s", file=sys.stderr)
                    combined_audio = {
                        'file': final_output_path,
                        'start_time': 0.0,
                        'duration': audio1_duration_seconds  # Use audio1's duration explicitly
                    }
            
            # Final verification of output structure
            if isinstance(combined_audio, dict) and 'file' in combined_audio and 'duration' in combined_audio:
                print(f"FINAL OUTPUT CHECK - File: {combined_audio['file']}, Duration: {combined_audio['duration']}s", file=sys.stderr)
                
                # One last check to make sure the duration is correct
                try:
                    # If file exists, check its actual duration
                    if os.path.exists(combined_audio['file']):
                        check_audio = AudioSegment.from_file(combined_audio['file'])
                        actual_duration = len(check_audio) / 1000.0
                        print(f"Actual file duration: {actual_duration}s, Expected: {combined_audio['duration']}s", file=sys.stderr)
                        
                        # If there's still a major discrepancy, set correct metadata
                        if abs(actual_duration - combined_audio['duration']) > 0.5:  # More than half second difference
                            print(f"WARNING: Duration mismatch in output metadata vs actual file.", file=sys.stderr)
                            # Force the duration in the output metadata to match audio1
                            audio1_duration_seconds = len(sound1) / 1000.0
                            combined_audio['duration'] = audio1_duration_seconds
                except Exception as final_check_error:
                    print(f"Warning during final check: {str(final_check_error)}", file=sys.stderr)
                
            return (combined_audio,)
            
        except Exception as e:
            print(f"Error combining audio: {str(e)}", file=sys.stderr)
            # Return original audio for debugging purposes
            return (audio1,)

NODE_CLASS_MAPPINGS = {
    "CombineAudio": CombineAudio
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CombineAudio": "Combine Audio Tracks"
}

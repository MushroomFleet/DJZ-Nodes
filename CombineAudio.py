import os
import sys
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
            # Load the audio files using pydub
            sound1 = AudioSegment.from_file(audio1.file)
            sound2 = AudioSegment.from_file(audio2.file)
            
            # Apply volume adjustments (pydub uses dB, so we convert from linear scale)
            if volume1 != 1.0:
                sound1 = sound1 + (20 * float(volume1))  # Convert to dB
            if volume2 != 1.0:
                sound2 = sound2 + (20 * float(volume2))  # Convert to dB
            
            # Match lengths by padding the shorter audio with silence that matches its audio parameters
            if len(sound1) > len(sound2):
                diff = len(sound1) - len(sound2)
                silence = AudioSegment.silent(duration=diff, frame_rate=sound2.frame_rate)
                silence = silence.set_channels(sound2.channels)
                sound2 = sound2 + silence
            else:
                diff = len(sound2) - len(sound1)
                silence = AudioSegment.silent(duration=diff, frame_rate=sound1.frame_rate)
                silence = silence.set_channels(sound1.channels)
                sound1 = sound1 + silence
            
            # Combine audio (overlay maintains both tracks)
            combined = sound1.overlay(sound2)
            
            # Export the combined audio
            output_path = os.path.join(os.path.dirname(audio1.file), "combined_audio.mp4")
            combined.export(output_path, format="mp4")
            
            print(f"Successfully created combined audio at: {output_path}", file=sys.stderr)
            
            # Create new LazyAudioMap with the combined audio
            combined_audio = audio1.__class__(
                file=output_path,
                start_time=0.0,
                duration=max(audio1.duration, audio2.duration) if hasattr(audio1, 'duration') and hasattr(audio2, 'duration') else len(combined) / 1000.0
            )
            
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

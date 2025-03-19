import torch
from pathlib import Path
import os
import numpy as np
import tempfile
import wave
import subprocess  # Added for ffmpeg
import sys
import logging

class SpeechToText:
    def __init__(self):
        self.local_model = None
        
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model_size": (["tiny", "base", "small", "medium", "large-v2"], {"default": "base"}),
            },
            "optional": {
                "AUDIO": ("AUDIO",),
                "audio_path": ("STRING", {"default": None, "forceInput": True}),
                "video_path": ("STRING", {"default": None, "forceInput": True}),
            }
        }
    
    RETURN_TYPES = ("STRING", "STRING", "STRING",)
    RETURN_NAMES = ("transcript", "detected_language","language_name",)
    FUNCTION = "transcribe_audio"
    CATEGORY = "Bjornulf"

    def tensor_to_wav(self, audio_tensor, sample_rate):
        """Convert audio tensor to temporary WAV file"""
        audio_data = audio_tensor.squeeze().numpy()
        
        if audio_data.ndim == 2:
            audio_data = np.mean(audio_data, axis=0)
        elif audio_data.ndim > 2:
            raise ValueError(f"Unsupported audio tensor shape: {audio_data.shape}")

        temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
        
        with wave.open(temp_file.name, 'wb') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            audio_data = (audio_data * 32767).astype(np.int16)
            wav_file.writeframes(audio_data.tobytes())
        
        return temp_file.name

    def load_local_model(self, model_size):
        import faster_whisper
        
        try:
            if self.local_model is None:
                print(f"Loading local Whisper model ({model_size})...")
                self.local_model = faster_whisper.WhisperModel(model_size, device="cpu", compute_type="int8")
                print("Local model loaded successfully!")
            return True, None
        except Exception as e:
            return False, f"Error loading model: {str(e)}"

    def transcribe_local(self, audio_path, model_size):
        success, message = self.load_local_model(model_size)
        if not success:
            return False, message, None

        try:
            print("Starting local transcription...")
            segments, info = self.local_model.transcribe(str(audio_path), beam_size=5)
            text = " ".join([segment.text for segment in segments]).strip()
            detected_language = info.language
            print("Local transcription completed successfully!")
            return True, text, detected_language
        except Exception as e:
            return False, f"Error during local transcription: {str(e)}", None

    def transcribe_audio(self, model_size, AUDIO=None, audio_path=None, video_path=None):
        # Check Python version and warn if 3.12 or higher
        if sys.version_info > (3, 12):
            logging.warning("⚠️⚠️⚠️ Warning: You are using Python {}.{} or higher. This may cause compatibility issues with some dependencies (e.g., faster_whisper). Consider using Python 3.11 or 3.12 instead. ⚠️⚠️⚠️".format(sys.version_info.major, sys.version_info.minor))
        import faster_whisper
        transcript = "No valid audio input provided"
        detected_language = ""
        temp_wav_path = None
        temp_audio_path = None
        
        try:
            # Check video input first
            if video_path and os.path.exists(video_path):
                try:
                    # Create temp file for extracted audio
                    temp_audio = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
                    temp_audio.close()
                    temp_audio_path = temp_audio.name
                    
                    # FFmpeg command to extract audio
                    command = [
                        'ffmpeg',
                        '-i', video_path,
                        '-vn',
                        '-acodec', 'pcm_s16le',
                        '-ar', '16000',
                        '-ac', '1',
                        '-y',
                        temp_audio_path
                    ]
                    subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    audio_to_process = temp_audio_path
                except subprocess.CalledProcessError as e:
                    return (f"FFmpeg error: {e.stderr.decode()}", "", "")
                except Exception as e:
                    return (f"Error extracting audio: {str(e)}", "", "")
            elif AUDIO is not None:
                waveform = AUDIO['waveform']
                sample_rate = AUDIO['sample_rate']
                temp_wav_path = self.tensor_to_wav(waveform, sample_rate)
                audio_to_process = temp_wav_path
            elif audio_path and os.path.exists(audio_path):
                audio_to_process = audio_path
            else:
                return ("No valid audio input provided", "", "")

            if audio_to_process:
                success, result, lang = self.transcribe_local(audio_to_process, model_size)
                transcript = result if success else f"Local transcription failed: {result}"
                detected_language = lang if success else ""

        finally:
            # Cleanup temporary files
            if temp_wav_path and os.path.exists(temp_wav_path):
                os.unlink(temp_wav_path)
            if temp_audio_path and os.path.exists(temp_audio_path):
                os.unlink(temp_audio_path)

        language_map = {
            "ar": "Arabic", "cs": "Czech", "de": "German", "en": "English",
            "es": "Spanish", "fr": "French", "hi": "Hindi", "hu": "Hungarian",
            "it": "Italian", "ja": "Japanese", "ko": "Korean", "nl": "Dutch",
            "pl": "Polish", "pt": "Portuguese", "ru": "Russian", "tr": "Turkish",
            "zh-cn": "Chinese"
        }
        detected_language_name = language_map.get(detected_language, "Unknown")
        
        return (transcript, detected_language, detected_language_name)
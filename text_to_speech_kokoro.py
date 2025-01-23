import os
import requests
import random

VOICE_OPTIONS = {
    "af_bella": "Bella (American Female) - af_bella",
    "af_nicole": "Nicole (American Female) - af_nicole",
    "af_sarah": "Sarah (American Female) - af_sarah",
    "af_sky": "Sky (American Female) - af_sky",
    "af": "Default (American Female) - af",
    "am_adam": "Adam (American Male) - am_adam",
    "am_michael": "Michael (American Male) - am_michael",
    "bf_emma": "Emma (British Female) - bf_emma",
    "bf_isabella": "Isabella (British Female) - bf_isabella",
    "bm_george": "George (British Male) - bm_george",
    "bm_lewis": "Lewis (British Male) - bm_lewis"
}

# Create a reversed mapping for display to value
VOICE_DISPLAY_TO_VALUE = {v: k for k, v in VOICE_OPTIONS.items()}

LANGUAGE_OPTIONS = {
    "en-us": "English (US)",
    "en-gb": "English (UK)",
    "fr-fr": "French",
    "ja": "Japanese",
    "ko": "Korean",
    "cmn": "Chinese (Mandarin)"
}

def download_if_not_exists(url, dest_path):
    """Download a file from a URL if it doesn't already exist."""
    if not os.path.exists(dest_path):
        print(f"Downloading {os.path.basename(dest_path)}...")
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(dest_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded {os.path.basename(dest_path)}")

class KokoroTTS:
    BASE_DIR = "Bjornulf/Kokoro"
    MODEL_FILE = os.path.join(BASE_DIR, "kokoro-v0_19.onnx")
    VOICES_FILE = os.path.join(BASE_DIR, "voices.bin")

    VOICE_LANGUAGES = {
        'af': 'en-us', 'am': 'en-us', 'bf': 'en-gb', 'bm': 'en-gb'
    }

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True}),
                "voice": (list(VOICE_OPTIONS.values()), {"default": "Default (American Female) - af"}),
                "language": (list(LANGUAGE_OPTIONS.keys()), {"default": "en-us"}),
                "speed": ("FLOAT", {"default": 1.0, "min": 0.5, "max": 2.0, "step": 0.1}),
                "autoplay": ("BOOLEAN", {"default": True}),
                "save_audio": ("BOOLEAN", {"default": True}),
                "overwrite": ("BOOLEAN", {"default": False}),
                "seed": ("INT", {"default": 0}),
            }
        }

    RETURN_TYPES = ("AUDIO",)
    FUNCTION = "generate_audio"
    CATEGORY = "Bjornulf/Kokoro"

    def generate_audio(self, text: str, voice: str, language: str, speed: float,
                      autoplay: bool, save_audio: bool, 
                      overwrite: bool, seed: int):
        random.seed(seed)

        config = {
            "model_path": self.MODEL_FILE,
            "voices_path": self.VOICES_FILE,
            "speed": speed,
            "language": language
        }

        download_if_not_exists(
            "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files/kokoro-v0_19.onnx",
            config["model_path"]
        )
        download_if_not_exists(
            "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files/voices.bin",
            config["voices_path"]
        )

        try:
            from kokoro_onnx import Kokoro
            import soundfile as sf
            import torch
            import numpy as np
            from pydub import AudioSegment
            from pydub.playback import play

            voice_id = VOICE_DISPLAY_TO_VALUE[voice]
            kokoro = Kokoro(config["model_path"], config["voices_path"])

            # Check if file exists and overwrite is False
            sanitized_text = ''.join(c if c.isalnum() else '_' for c in text[:50])
            save_path = os.path.join("Bjornulf_TTS_Kokoro", voice_id, f"{sanitized_text}.wav")
            full_path = os.path.abspath(save_path)

            if os.path.exists(full_path) and not overwrite:
                print(f"File exists: {full_path}. Loading existing audio.")
                samples, sample_rate = sf.read(full_path)
                if autoplay:
                    audio_segment = AudioSegment.from_file(full_path)
                    play(audio_segment)
            else:
                # Generate new audio
                samples, sample_rate = kokoro.create(
                    text,
                    voice=voice_id,
                    speed=config["speed"],
                    lang=language
                )

                if save_audio:
                    os.makedirs(os.path.dirname(full_path), exist_ok=True)
                    sf.write(full_path, samples, sample_rate)

                if autoplay:
                    try:
                        audio_segment = AudioSegment(
                            samples.tobytes(), 
                            frame_rate=sample_rate,
                            sample_width=samples.dtype.itemsize, 
                            channels=1
                        )
                        play(audio_segment)
                    except Exception as e:
                        print(f"Autoplay error: {e}")

            audio_tensor = torch.from_numpy(samples).unsqueeze(0)
            audio_output = {"waveform": audio_tensor.unsqueeze(0), "sample_rate": sample_rate}
            return (audio_output,)

        except Exception as e:
            print(f"Error in Kokoro TTS: {e}")
            return ({"waveform": torch.zeros(1, 1, 1), "sample_rate": 22050},)
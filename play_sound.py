import os
import io
import sys
from pydub import AudioSegment
from pydub.playback import play
import torch
import numpy as np
from scipy.io import wavfile

class Everything(str):
    def __ne__(self, __value: object) -> bool:
        return False

class PlayAudio:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "anything": (Everything("*"), {"forceInput": True}),
            },
            "optional": {
                "AUDIO": ("AUDIO", {"forceInput": True}),
                "audio_path": ("STRING", {"default": ""})
            }
        }

    RETURN_TYPES = (Everything("*"),)
    RETURN_NAMES = ("anything",)
    FUNCTION = "execute"
    CATEGORY = "audio"
    
    def play_audio(self, anything, AUDIO=None, audio_path=None):
        # print(f"Debug - Entering play_audio: AUDIO={AUDIO}, audio_path={audio_path}")
        try:
            # Case 1: AUDIO input is provided
            if AUDIO is not None:
                # print(f"Debug - Processing AUDIO input: type={type(AUDIO)}")
                if isinstance(AUDIO, dict) and 'waveform' in AUDIO:
                    waveform = AUDIO['waveform']
                    sample_rate = AUDIO.get('sample_rate', 44100)
                    
                    if isinstance(waveform, torch.Tensor):
                        waveform = waveform.cpu().numpy()
                    
                    if waveform.dtype.kind == 'f':
                        waveform = (waveform * 32767).astype(np.int16)
                    
                    temp_wav = io.BytesIO()
                    wavfile.write(temp_wav, sample_rate, waveform)
                    temp_wav.seek(0)
                    sound = AudioSegment.from_wav(temp_wav)
                
                elif isinstance(AUDIO, AudioSegment):
                    sound = AUDIO
                else:
                    raise ValueError(f"Unsupported AUDIO type: {type(AUDIO)}")
            
            # Case 2: audio_path is provided
            elif audio_path and os.path.exists(audio_path):
                # print(f"Debug - Loading audio from path: {audio_path}")
                sound = AudioSegment.from_file(audio_path)
            
            # Case 3: Default to bell sound
            else:
                audio_file = os.path.join(os.path.dirname(__file__), 'bell.m4a')
                # print(f"Debug - Attempting default bell sound: {audio_file}")
                if not os.path.exists(audio_file):
                    raise FileNotFoundError(f"Default bell.m4a not found at {audio_file}")
                sound = AudioSegment.from_file(audio_file, format="m4a")

            # Play the sound
            # print("Debug - Playing sound...")
            if sys.platform.startswith('win'):
                wav_io = io.BytesIO()
                sound.export(wav_io, format='wav')
                wav_data = wav_io.getvalue()
                import winsound
                winsound.PlaySound(wav_data, winsound.SND_MEMORY)
            else:
                play(sound)
            # print("Debug - Sound played successfully")
                
        except Exception as e:
            # print(f"Audio playback error: {e}")
            import traceback
            print(traceback.format_exc())

    def execute(self, anything, AUDIO=None, audio_path=None):
        # print(f"Debug - Execute: anything={anything}, AUDIO={AUDIO}, audio_path={audio_path}")
        self.play_audio(anything, AUDIO, audio_path)
        return (anything,)
    
    @classmethod
    def IS_CHANGED(cls, anything, AUDIO=None, audio_path=None, *args):
        return float("NaN")
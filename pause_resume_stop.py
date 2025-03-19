import time
from aiohttp import web
from server import PromptServer
# import logging
from pydub import AudioSegment
from pydub.playback import play
import os
import io
import sys
import random
# from comfy_execution.graph import ExecutionBlocker

class Everything(str):
    def __ne__(self, __value: object) -> bool:
        return False

class PauseResume:
    is_paused = True
    should_stop = False

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input": (Everything("*"), {"forceInput": True}),
                "seed": ("INT", {"default": 1}),
            }
        }

    RETURN_TYPES = (Everything("*"),)
    RETURN_NAMES = ("output",)
    FUNCTION = "loop_resume_or_stop"
    CATEGORY = "Bjornulf"
    
    def play_audio(self):
        # Check if the operating system is Windows
        if sys.platform.startswith('win'):
            try:
                # Load the audio file into memory
                audio_file = os.path.join(os.path.dirname(__file__), 'bell.m4a')
                
                # Load the audio segment without writing to any temp files
                sound = AudioSegment.from_file(audio_file, format="m4a")
                
                # Export the AudioSegment to a WAV file in memory
                wav_io = io.BytesIO()
                sound.export(wav_io, format='wav')
                wav_data = wav_io.getvalue()
                
                # Play the WAV data using winsound
                import winsound
                winsound.PlaySound(wav_data, winsound.SND_MEMORY)
            except Exception as e:
                print(f"An error occurred: {e}")
        else:
            audio_file = os.path.join(os.path.dirname(__file__), 'bell.m4a')
            sound = AudioSegment.from_file(audio_file, format="m4a")
            play(sound)

    def loop_resume_or_stop(self, input, seed):
        random.seed(seed)
        self.play_audio()
        self.input = input
        while PauseResume.is_paused and not PauseResume.should_stop:
            # logging.info(f"PauseResume.is_paused: {PauseResume.is_paused}, PauseResume.should_stop: {PauseResume.should_stop}")
            time.sleep(1)  # Sleep to prevent busy waiting
        
        if PauseResume.should_stop:
            PauseResume.should_stop = False  # Reset for next run
            PauseResume.is_paused = True
            raise Exception("Workflow stopped by user")
            # return (ExecutionBlocker("Workflow stopped by user"),)  # Return ExecutionBlocker to stop gracefully, but error on next node.
        
        PauseResume.is_paused = True
        PauseResume.should_stop = False
        return (self.input,)

@PromptServer.instance.routes.get("/bjornulf_resume")
async def resume_node(request):
    # logging.info("Resume node called")
    PauseResume.is_paused = False
    return web.Response(text="Node resumed")

@PromptServer.instance.routes.get("/bjornulf_stop")
async def stop_node(request):
    # logging.info("Stop node called")
    PauseResume.should_stop = True
    PauseResume.is_paused = False  # Ensure the loop exits
    return web.Response(text="Workflow stopped")
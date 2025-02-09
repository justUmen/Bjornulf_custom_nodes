import time
from aiohttp import web
from server import PromptServer
# import logging
from pydub import AudioSegment
from pydub.playback import play
import os
import sys
import io
import random

class Everything(str):
    def __ne__(self, __value: object) -> bool:
        return False

class PickInput:
    is_paused = True
    should_stop = False
    selected_input = None

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "number_of_inputs": ("INT", {"default": 2, "min": 1, "max": 10, "step": 1}),
                "seed": ("INT", {"default": 1}),
            },
            "hidden": {
                **{f"input_{i}": (Everything("*"), {"forceInput": "True"}) for i in range(1, 11)}
            }
        }

    RETURN_TYPES = (Everything("*"),)
    RETURN_NAMES = ("output",)
    FUNCTION = "pick_input"
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

    def pick_input(self, seed, **kwargs):
        random.seed(seed)
        # logging.info(f"Selected input at the start: {PickInput.selected_input}")
        self.play_audio()
        
        while PickInput.is_paused and not PickInput.should_stop:
            # logging.info(f"PickInput.is_paused: {PickInput.is_paused}, PickInput.should_stop: {PickInput.should_stop}")
            time.sleep(1)  # Sleep to prevent busy waiting
        
        if PickInput.should_stop:
            PickInput.should_stop = False  # Reset for next run
            PickInput.is_paused = True
            raise Exception("Workflow stopped by user")
        
        PickInput.is_paused = True
        PickInput.should_stop = False
        
        # Check if the selected input exists in kwargs
        if PickInput.selected_input not in kwargs:
            # logging.error(f"Selected input '{PickInput.selected_input}' not found in kwargs")
            # logging.info(f"Available kwargs: {list(kwargs.keys())}")
            return (None,)  # or handle this error as appropriate
        
        selected_value = kwargs.get(PickInput.selected_input)
        # logging.info(f"Value of selected input '{PickInput.selected_input}': {selected_value}")
        
        # Store the value in self.target if needed
        self.target = selected_value
        
        return (selected_value,)

    def create_select_handler(self, index):
        async def select_input(request):
            self.selected_input = index
            self.is_waiting = False
            return web.Response(text=f"Input {index + 1} selected")
        return select_input

@PromptServer.instance.routes.get("/bjornulf_stop_pick")
async def stop_node_pick(request):
    # logging.info("Stop node pick called")
    PickInput.should_stop = True
    PickInput.is_paused = False  # Ensure the loop exits
    return web.Response(text="Workflow stopped")

@PromptServer.instance.routes.get("/bjornulf_select_input_1")
async def bjornulf_select_input_1(request):
    # logging.info("Resume node called")
    PickInput.is_paused = False
    PickInput.selected_input="input_1"
    return web.Response(text="Node resumed")

@PromptServer.instance.routes.get("/bjornulf_select_input_2")
async def bjornulf_select_input_2(request):
    # logging.info("Resume node called")
    PickInput.is_paused = False
    PickInput.selected_input="input_2"
    return web.Response(text="Node resumed")

@PromptServer.instance.routes.get("/bjornulf_select_input_3")
async def bjornulf_select_input_3(request):
    # logging.info("Resume node called")
    PickInput.is_paused = False
    PickInput.selected_input="input_3"
    return web.Response(text="Node resumed")

@PromptServer.instance.routes.get("/bjornulf_select_input_4")
async def bjornulf_select_input_4(request):
    # logging.info("Resume node called")
    PickInput.is_paused = False
    PickInput.selected_input="input_4"
    return web.Response(text="Node resumed")

@PromptServer.instance.routes.get("/bjornulf_select_input_5")
async def bjornulf_select_input_5(request):
    # logging.info("Resume node called")
    PickInput.is_paused = False
    PickInput.selected_input="input_5"
    return web.Response(text="Node resumed")

@PromptServer.instance.routes.get("/bjornulf_select_input_6")
async def bjornulf_select_input_6(request):
    # logging.info("Resume node called")
    PickInput.is_paused = False
    PickInput.selected_input="input_6"
    return web.Response(text="Node resumed")

@PromptServer.instance.routes.get("/bjornulf_select_input_7")
async def bjornulf_select_input_7(request):
    # logging.info("Resume node called")
    PickInput.is_paused = False
    PickInput.selected_input="input_7"
    return web.Response(text="Node resumed")

@PromptServer.instance.routes.get("/bjornulf_select_input_8")
async def bjornulf_select_input_8(request):
    # logging.info("Resume node called")
    PickInput.is_paused = False
    PickInput.selected_input="input_8"
    return web.Response(text="Node resumed")

@PromptServer.instance.routes.get("/bjornulf_select_input_9")
async def bjornulf_select_input_9(request):
    # logging.info("Resume node called")
    PickInput.is_paused = False
    PickInput.selected_input="input_9"
    return web.Response(text="Node resumed")

@PromptServer.instance.routes.get("/bjornulf_select_input_10")
async def bjornulf_select_input_10(request):
    # logging.info("Resume node called")
    PickInput.is_paused = False
    PickInput.selected_input="input_10"
    return web.Response(text="Node resumed")
import random
import json
import os
from aiohttp import web
from server import PromptServer

class ModelClipVaeSelector:
    def __init__(self):
        self._counter = -1
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "number_of_inputs": ("INT", {"default": 2, "min": 2, "max": 10, "step": 1}),
                "selected_number": ("INT", {"default": 0, "min": 0, "max": 10, "step": 1}),  # 0 for random, >0 for specific selection
                "model_1": ("MODEL", {"forceInput": True}),
                "clip_1": ("CLIP", {"forceInput": True}),
                "vae_1": ("VAE", {"forceInput": True}),
                "model_2": ("MODEL", {"forceInput": True}),
                "clip_2": ("CLIP", {"forceInput": True}),
                "vae_2": ("VAE", {"forceInput": True}),
                "RANDOM": ("BOOLEAN", {"default": False}),  # Force random selection
                "LOOP": ("BOOLEAN", {"default": False}),  # Return all as list
                "LOOP_SEQUENTIAL": ("BOOLEAN", {"default": False}),  # Sequential looping
                "jump": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1}),  # Jump size for sequential loop
                "seed": ("INT", {
                    "default": 0,
                    "min": -1,
                    "max": 0x7FFFFFFFFFFFFFFF
                }),
            },
            "hidden": {
                **{f"model_{i}": ("MODEL", {"forceInput": True}) for i in range(3, 11)},
                **{f"clip_{i}": ("CLIP", {"forceInput": True}) for i in range(3, 11)},
                **{f"vae_{i}": ("VAE", {"forceInput": True}) for i in range(3, 11)},
            }
        }

    RETURN_TYPES = ("MODEL", "CLIP", "VAE", "INT")  # Added INT for current selection
    RETURN_NAMES = ("model", "clip", "vae", "current_selection")
    OUTPUT_IS_LIST = (True, True, True, False)  # Allow lists for model/clip/vae outputs
    FUNCTION = "select_models"
    CATEGORY = "Bjornulf"

    def select_models(self, number_of_inputs, selected_number, RANDOM, LOOP, LOOP_SEQUENTIAL, jump, **kwargs):
        if LOOP:
            # Return all models as lists
            models = [kwargs[f"model_{i}"] for i in range(1, number_of_inputs + 1)]
            clips = [kwargs[f"clip_{i}"] for i in range(1, number_of_inputs + 1)]
            vaes = [kwargs[f"vae_{i}"] for i in range(1, number_of_inputs + 1)]
            return (models, clips, vaes, 0)
            
        if LOOP_SEQUENTIAL:
            counter_file = os.path.join("Bjornulf", "model_selector_counter.txt")
            os.makedirs(os.path.dirname(counter_file), exist_ok=True)

            try:
                with open(counter_file, 'r') as f:
                    current_index = int(f.read().strip())
            except (FileNotFoundError, ValueError):
                current_index = -jump

            next_index = current_index + jump
            
            if next_index >= number_of_inputs:
                with open(counter_file, 'w') as f:
                    f.write(str(-jump))
                raise ValueError(f"Counter has reached the last model (total models: {number_of_inputs}). Counter has been reset.")

            with open(counter_file, 'w') as f:
                f.write(str(next_index))

            selected_index = next_index + 1  # Convert to 1-based indexing
        else:
            # Handle RANDOM or specific selection
            if RANDOM or selected_number == 0:
                random.seed(kwargs.get('seed', 0))
                selected_index = random.randint(1, number_of_inputs)
            else:
                selected_index = max(1, min(selected_number, number_of_inputs))
        
        selected_model = kwargs[f"model_{selected_index}"]
        selected_clip = kwargs[f"clip_{selected_index}"]
        selected_vae = kwargs[f"vae_{selected_index}"]
        
        return ([selected_model], [selected_clip], [selected_vae], selected_index)

    @classmethod
    def IS_CHANGED(cls, number_of_inputs, selected_number, RANDOM, LOOP, LOOP_SEQUENTIAL, jump, **kwargs):
        return float("NaN") if LOOP_SEQUENTIAL else (number_of_inputs, selected_number, RANDOM, LOOP, LOOP_SEQUENTIAL, jump, kwargs.get('seed', 0))

# Add routes for counter management
@PromptServer.instance.routes.post("/reset_model_selector_counter")
async def reset_model_selector_counter(request):
    counter_file = os.path.join("Bjornulf", "model_selector_counter.txt")
    try:
        os.remove(counter_file)
        return web.json_response({"success": True}, status=200)
    except FileNotFoundError:
        return web.json_response({"success": True}, status=200)
    except Exception as e:
        return web.json_response({"success": False, "error": str(e)}, status=500)

@PromptServer.instance.routes.post("/get_model_selector_counter")
async def get_model_selector_counter(request):
    counter_file = os.path.join("Bjornulf", "model_selector_counter.txt")
    try:
        with open(counter_file, 'r') as f:
            current_index = int(f.read().strip())
        return web.json_response({"success": True, "value": current_index + 1}, status=200)
    except (FileNotFoundError, ValueError):
        return web.json_response({"success": True, "value": 0}, status=200)
    except Exception as e:
        return web.json_response({"success": False, "error": str(e)}, status=500)
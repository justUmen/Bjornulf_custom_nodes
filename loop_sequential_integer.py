import os
from aiohttp import web
from server import PromptServer
import logging

class LoopIntegerSequential:
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "from_this": ("INT", {"default": 1, "min": 1, "max": 50000, "step": 1}),
                "to_that": ("INT", {"default": 10, "min": 1, "max": 50000, "step": 1}),
                "jump": ("INT", {"default": 1, "min": 1, "max": 1000, "step": 1}),
            },
        }

    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("int_value", "remaining_cycles")
    FUNCTION = "get_next_value"
    CATEGORY = "Bjornulf"

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")  # This ensures the node always runs

    def get_next_value(self, from_this, to_that, jump):
        counter_file = os.path.join("Bjornulf", "counter_integer.txt")
        os.makedirs(os.path.dirname(counter_file), exist_ok=True)

        try:
            with open(counter_file, 'r') as f:
                current_value = int(f.read().strip())
        except (FileNotFoundError, ValueError):
            current_value = from_this - jump  # Start with from_this on first run

        next_value = current_value + jump

        # Block execution if we exceed to_that
        if next_value > to_that:
            raise ValueError(f"Counter has reached its limit of {to_that}, Reset Counter to continue.")

        # Save the new value
        with open(counter_file, 'w') as f:
            f.write(str(next_value))

        # Calculate how many times it can run before reaching the limit
        if jump != 0:
            remaining_cycles = max(0, (to_that - next_value) // jump + 1)
        else:
            remaining_cycles = 0  # Avoid division by zero

        return (next_value, remaining_cycles - 1) # Subtract 1 to account for the current run

# Server routes
@PromptServer.instance.routes.post("/get_counter_value")
async def get_counter_value(request):
    # logging.info("Get counter value called")
    counter_file = os.path.join("Bjornulf", "counter_integer.txt")
    try:
        with open(counter_file, 'r') as f:
            current_index = int(f.read().strip())
        return web.json_response({"success": True, "value": current_index + 1}, status=200)
    except (FileNotFoundError, ValueError):
        return web.json_response({"success": True, "value": 0}, status=200)
    except Exception as e:
        return web.json_response({"success": False, "error": str(e)}, status=500)

@PromptServer.instance.routes.post("/reset_counter")
async def reset_counter(request):
    # logging.info("Reset counter called")
    counter_file = os.path.join("Bjornulf", "counter_integer.txt")
    try:
        os.remove(counter_file)
        return web.json_response({"success": True}, status=200)
    except FileNotFoundError:
        return web.json_response({"success": True}, status=200)  # File doesn't exist, consider it reset
    except Exception as e:
        return web.json_response({"success": False, "error": str(e)}, status=500)
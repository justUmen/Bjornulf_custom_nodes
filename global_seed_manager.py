
from server import PromptServer
import os
from aiohttp import web
import random

class GlobalSeedManager:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"seed": ( "INT", {
            "default": 0,
            "min": 0,
            "max": 4294967294
        })}}

    RETURN_TYPES = ("INT", "STRING", "INT", "STRING")
    RETURN_NAMES = ("new_seed_INT", "new_seed_STRING", "previous_seed_INT", "all_seeds_LIST")
    FUNCTION = "generate_seed"
    CATEGORY = "Bjornulf"

    def generate_seed(self, seed: int):
        # Generate new random seed
        new_seed = random.randint(0, 2**31 - 1)
        seed_str = str(new_seed)
        
        # Define file path
        file_path = "Bjornulf/random_seeds.txt"
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Read previous seeds from file
        try:
            with open(file_path, 'r') as f:
                existing_seeds = f.read().strip()
                seed_list = existing_seeds.split(';') if existing_seeds else []
                prev_seed = int(seed_list[-1]) if seed_list else -1
        except (FileNotFoundError, ValueError, IndexError):
            prev_seed = -1
            seed_list = []
        
        # Add new seed to list
        seed_list.append(str(new_seed))
        
        # Write all seeds to file
        with open(file_path, 'w') as f:
            f.write(';'.join(seed_list))
        
        # Create string of all seeds
        all_seeds_str = ';'.join(seed_list)
        
        return new_seed, seed_str, prev_seed, all_seeds_str

# Define the API endpoint to delete the seeds file
@PromptServer.instance.routes.post("/delete_random_seeds")
async def delete_random_seeds(request):
    file_path = "Bjornulf/random_seeds.txt"
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return web.json_response({"success": True})
        else:
            return web.json_response({"success": False, "error": "File not found"})
    except Exception as e:
        return web.json_response({"success": False, "error": str(e)})
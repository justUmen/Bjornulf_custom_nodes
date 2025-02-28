import os
import numpy as np
from PIL import Image, ImageSequence, ImageOps
import torch

from aiohttp import web
from server import PromptServer
class LoadImagesFromSelectedFolder:
    @classmethod
    def INPUT_TYPES(cls):
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        comfyui_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
        output_dir = os.path.join(comfyui_root, 'output')
        
        def count_images(folder_path):
            # Count the number of image files in the folder
            return len([f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))])
        
        folders = []
        for root, dirs, files in os.walk(output_dir):
            rel_path = os.path.relpath(root, output_dir)
            if rel_path == '.':
                continue
            image_count = count_images(root)
            if image_count > 0:
                folder_name = f"{rel_path} ({image_count} images)"
                folders.append((folder_name, rel_path))
        
        # Sort folders alphabetically, case-insensitive
        folders.sort(key=lambda x: x[0].lower())

        return {
            "required": {
                "selected_folder": ([folder[0] for folder in folders],),
            }
        }
    
    RETURN_TYPES = ("IMAGE", "IMAGE", "IMAGE", "IMAGE")
    RETURN_NAMES = ("Images resolution 1", "Images resolution 2", "Images resolution 3", "Images resolution 4")
    FUNCTION = "load_images_from_selected_folder"
    CATEGORY = "Bjornulf"

    def load_images_from_selected_folder(self, selected_folder):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        comfyui_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
        output_dir = os.path.join(comfyui_root, 'output')
        folder_path = os.path.join(output_dir, selected_folder.split(" (")[0])
        
        images_by_resolution = {}

        # Check if the folder exists and contains images
        if not os.path.exists(folder_path):
            print(f"Folder {folder_path} does not exist.")
            return (None, None, None)

        image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
        if not image_files:
            print(f"No images found in folder {folder_path}.")
            return (None, None, None)

        for image_file in image_files:
            image_path = os.path.join(folder_path, image_file)
            img = Image.open(image_path)
            
            for i in ImageSequence.Iterator(img):
                i = ImageOps.exif_transpose(i)

                if i.mode == 'I':
                    i = i.point(lambda i: i * (1 / 255))
                image = i.convert("RGB")
                
                resolution = image.size
                
                image = np.array(image).astype(np.float32) / 255.0
                image = torch.from_numpy(image)[None,]
                
                if resolution not in images_by_resolution:
                    images_by_resolution[resolution] = []
                
                images_by_resolution[resolution].append(image)

        # Sort resolutions by total pixel count (width * height)
        sorted_resolutions = sorted(images_by_resolution.keys(), key=lambda r: r[0] * r[1], reverse=True)

        outputs = []
        for i in range(4):  # Return up to 4 different resolutions
            if i < len(sorted_resolutions):
                resolution = sorted_resolutions[i]
                output_image = torch.cat(images_by_resolution[resolution], dim=0)
                outputs.append(output_image)
            else:
                # Create a placeholder tensor filled with 11111111111111111111111
                H, W, C = 64, 64, 3 
                placeholder_image = torch.ones((1, H, W, C), dtype=torch.float32)
                outputs.append(placeholder_image)

        return tuple(outputs)

# Define the API endpoint to get the list of image folders
@PromptServer.instance.routes.get("/get_image_folders")
async def get_image_folders(request):
    # Get the ComfyUI output directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    comfyui_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
    output_dir = os.path.join(comfyui_root, 'output')
    
    # Collect folders with images
    folders = []
    for root, dirs, files in os.walk(output_dir):
        rel_path = os.path.relpath(root, output_dir)
        if rel_path == '.':
            continue  # Skip the root output directory itself
        # Count image files in the folder
        image_count = len([f for f in os.listdir(root) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))])
        if image_count > 0:
            folder_name = f"{rel_path} ({image_count} images)"
            folders.append(folder_name)
    
    # Sort the list alphabetically (case-insensitive)
    folders.sort(key=lambda x: x.lower())
    
    # Return the folder list as JSON
    return web.json_response({"success": True, "folders": folders})
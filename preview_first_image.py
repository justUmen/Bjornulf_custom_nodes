import random
import os
import numpy as np
import torch
from nodes import SaveImage
import folder_paths
from PIL import Image
import cv2

class PreviewFirstImage(SaveImage):
    def __init__(self):
        super().__init__()
        self.output_dir = folder_paths.get_temp_directory()
        self.type = "temp"
        self.prefix_append = "_preview_" + ''.join(random.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(5))
        self.compress_level = 1

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "images": ("IMAGE",),
                "path": ("STRING", {"default": ""})
            },
            "hidden": {
                "prompt": "PROMPT",
                "extra_pnginfo": "EXTRA_PNGINFO"
            },
        }

    RETURN_TYPES = ()
    FUNCTION = "preview_image"
    OUTPUT_NODE = True
    CATEGORY = "image"

    def preview_image(self, images=None, path="", prompt=None, extra_pnginfo=None):
        if images is None and not path:
            return {}

        output_images = None

        # Handle image tensor input - always take first image from batch
        if images is not None and images.nelement() > 0:
            # Ensure we're working with the first image in the batch
            first_image = images[0:1]  # Maintains batch dimension
            return super().save_images(images=first_image, prompt=prompt, extra_pnginfo=extra_pnginfo)

        # Handle path input
        if path and os.path.exists(path):
            try:
                if path.lower().endswith(('.mp4', '.avi', '.mov', '.wmv', '.webm', '.mkv')):  # Video file
                    cap = cv2.VideoCapture(path)
                    ret, frame = cap.read()
                    cap.release()
                    
                    if not ret:
                        return {}
                        
                    # Convert BGR to RGB and normalize
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame = frame.astype(np.float32) / 255.0
                    output_images = torch.from_numpy(frame).unsqueeze(0)
                    
                else:  # Image file
                    image = Image.open(path).convert('RGB')
                    image_np = np.array(image).astype(np.float32) / 255.0
                    output_images = torch.from_numpy(image_np).unsqueeze(0)
                
                return super().save_images(images=output_images, prompt=prompt, extra_pnginfo=extra_pnginfo)
                
            except Exception as e:
                print(f"Error processing file {path}: {str(e)}")
                return {}
        
        return {}
import random
import os
import hashlib
# import logging
import numpy as np
import torch
from nodes import SaveImage
import folder_paths
from PIL import Image
from server import PromptServer
from aiohttp import web

# Configure logging
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger("ImageNote")

class ImageNote(SaveImage):
    def __init__(self):
        self.output_dir = folder_paths.get_temp_directory()
        self.type = "temp"
        self.prefix_append = "_temp_" + ''.join(random.choice("abcdefghijklmnopqrstupvxyz") for _ in range(5))
        self.compress_level = 1
        self.note_dir = os.path.join("ComfyUI", "Bjornulf", "imageNote")
        os.makedirs(self.note_dir, exist_ok=True)

        # Store last image path and hash to prevent unnecessary reloading
        self.last_image_path = None
        self.last_image_hash = None
        self.last_output_images = None

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": {
                "images": ("IMAGE", ),
                "image_path": ("STRING", {"default": ""}),
                "note_text": ("STRING", {"default": "", "multiline": True})
            },
            "hidden": {
                "prompt": "PROMPT",
                "extra_pnginfo": "EXTRA_PNGINFO"
            },
        }
    
    FUNCTION = "process_image"
    OUTPUT_NODE = True
    CATEGORY = "Bjornulf"

    def compute_md5(self, image):
        image_bytes = image.tobytes() if isinstance(image, Image.Image) else image
        return hashlib.md5(image_bytes).hexdigest()

    def process_image(self, images=None, image_path="", note_text="", prompt=None, extra_pnginfo=None):
        output_images = None
        output_note_text = ""

        # If images are given, process them
        if images is not None and len(images) > 0:
            output_images = images
            image_np = (images[0].numpy() * 255).astype(np.uint8)
            image = Image.fromarray(image_np)
            image_hash = self.compute_md5(image)

            note_path = os.path.join(self.note_dir, f"{image_hash}.txt")
            if os.path.exists(note_path):
                with open(note_path, "r", encoding="utf-8") as f:
                    output_note_text = f.read()
            elif note_text:
                with open(note_path, "w", encoding="utf-8") as f:
                    f.write(note_text)
                    output_note_text = note_text

        # If image_path is empty, do nothing
        elif not image_path:
            # logger.debug("No image path provided, skipping processing.")
            return None, ""

        # Process image from path only if it has changed
        elif os.path.isfile(image_path):
            if image_path == self.last_image_path:
                # logger.debug("Image path has not changed, skipping reload.")
                return super().save_images(images=self.last_output_images, prompt=prompt, extra_pnginfo=extra_pnginfo)

            image = Image.open(image_path).convert("RGB")
            image_hash = self.compute_md5(image)

            if image_hash == self.last_image_hash:
                # logger.debug("Image content has not changed, skipping reload.")
                return super().save_images(images=self.last_output_images, prompt=prompt, extra_pnginfo=extra_pnginfo)

            note_path = os.path.join(self.note_dir, f"{image_hash}.txt")
            if os.path.exists(note_path):
                with open(note_path, "r", encoding="utf-8") as f:
                    output_note_text = f.read()
            elif note_text:
                with open(note_path, "w", encoding="utf-8") as f:
                    f.write(note_text)
                    output_note_text = note_text

            image_np = np.array(image).astype(np.float32) / 255.0
            output_images = torch.from_numpy(image_np).unsqueeze(0)

            # Update stored values
            self.last_image_path = image_path
            self.last_image_hash = image_hash
            self.last_output_images = output_images

        return super().save_images(images=output_images, prompt=prompt, extra_pnginfo=extra_pnginfo)

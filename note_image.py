import os
import hashlib
import numpy as np
from nodes import SaveImage
import random
from PIL import Image, ImageOps, ImageSequence
import torch
import folder_paths
import node_helpers
from aiohttp import web

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
class ImageNoteLoadImage:
    @classmethod
    def INPUT_TYPES(s):
        base_input_dir = folder_paths.get_input_directory() # Get base input directory
        input_dir = os.path.join(base_input_dir, "Bjornulf", "imagenote_images") # Specify subdirectory

        # Create the directory if it doesn't exist
        if not os.path.exists(input_dir):
            os.makedirs(input_dir, exist_ok=True) # Create directory and parents if needed

        # Filter for image files only
        valid_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')
        files = [f for f in os.listdir(input_dir) if 
                os.path.isfile(os.path.join(input_dir, f)) and 
                f.lower().endswith(valid_extensions)]

        if not files:
            # Provide a default option if no files are found
            files = ["none"]

        return {"required":
                    {
                        "image": (sorted(files), {"image_upload": True}),
                        # "note": ("STRING", {"default": ""}),  # Added multiline option FAILURE
                        "note": ("STRING", {"multiline": True, "lines": 10})
                    }
                }

    RETURN_TYPES = ("IMAGE", "MASK", "STRING", "STRING")  # Added note to return types
    RETURN_NAMES = ("image", "mask", "image_path", "note")  # Added note to return names
    FUNCTION = "load_image_alpha"
    CATEGORY = "Bjornulf"

    def load_image_alpha(self, image, note):  # Added note parameter
        image_path = folder_paths.get_annotated_filepath(image)

        img = node_helpers.pillow(Image.open, image_path)

        output_images = []
        output_masks = []
        w, h = None, None

        excluded_formats = ['MPO']

        for i in ImageSequence.Iterator(img):
            i = node_helpers.pillow(ImageOps.exif_transpose, i)

            if i.mode == 'I':
                i = i.point(lambda i: i * (1 / 255))
            image_converted = i.convert("RGBA")  # Renamed to avoid shadowing

            if len(output_images) == 0:
                w = image_converted.size[0]
                h = image_converted.size[1]

            if image_converted.size[0] != w or image_converted.size[1] != h:
                continue

            image_np = np.array(image_converted).astype(np.float32) / 255.0  # Renamed to avoid shadowing
            image_tensor = torch.from_numpy(image_np)[None,]  # Renamed to avoid shadowing
            if 'A' in i.getbands():
                mask = np.array(i.getchannel('A')).astype(np.float32) / 255.0
                mask = 1. - torch.from_numpy(mask)
            else:
                mask = torch.zeros((64, 64), dtype=torch.float32, device="cpu")
            output_images.append(image_tensor)  # Renamed to avoid shadowing
            output_masks.append(mask.unsqueeze(0))

        if len(output_images) > 1 and img.format not in excluded_formats:
            output_image = torch.cat(output_images, dim=0)
            output_mask = torch.cat(output_masks, dim=0)
        else:
            output_image = output_images[0]
            output_mask = output_masks[0]

        return (output_image, output_mask, image_path, note)  # Added note to return tuple

    @classmethod
    def IS_CHANGED(s, image, note):  # Added note to IS_CHANGED
        image_path = folder_paths.get_annotated_filepath(image)
        m = hashlib.sha256()
        with open(image_path, 'rb') as f:
            m.update(f.read())
        return m.digest().hex() + str(note) # Include note in hash

    @classmethod
    def VALIDATE_INPUTS(s, image):
        if not folder_paths.exists_annotated_filepath(image):
            return "Invalid image file: {}".format(image)

        return True
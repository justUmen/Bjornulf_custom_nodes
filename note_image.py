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

class ImageNote:
    def __init__(self):
        # Directory to store notes, created if it doesn’t exist
        self.note_dir = os.path.join("ComfyUI", "Bjornulf", "imageNote")
        os.makedirs(self.note_dir, exist_ok=True)

    @classmethod
    def INPUT_TYPES(cls):
        """Define the input types for the node."""
        return {
            "optional": {
                "images": ("IMAGE", ),
                "image_path": ("STRING", {"default": ""}),
                "note": ("STRING", {"default": ""}),
                "note_2": ("STRING", {"default": ""}),
                "note_3": ("STRING", {"default": ""})
            },
            "hidden": {
                "prompt": "PROMPT",
                "extra_pnginfo": "EXTRA_PNGINFO"
            },
        }
    
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("image_path", "note")
    FUNCTION = "process_image"
    OUTPUT_NODE = True
    CATEGORY = "Bjornulf"

    def compute_md5(self, image):
        """Compute MD5 hash of an image for note association."""
        if isinstance(image, Image.Image):
            image_bytes = image.tobytes()
        elif isinstance(image, torch.Tensor):
            image_bytes = (image.numpy() * 255).astype(np.uint8).tobytes()
        else:
            image_bytes = image
        return hashlib.md5(image_bytes).hexdigest()

    def process_image(self, images=None, image_path="", note="", note_2="", note_3="", prompt=None, extra_pnginfo=None):
        """Process the image and associate all notes."""
        output_note = ""
        ui_images = []

        input_dir = folder_paths.get_input_directory()
        output_dir = folder_paths.get_output_directory()
        temp_dir = folder_paths.get_temp_directory()

        # Collect all non-empty notes
        all_notes = [n for n in [note, note_2, note_3] if n]

        # Case 1: Image provided via file path
        if image_path and os.path.isfile(image_path):
            image = Image.open(image_path).convert("RGB")
            image_hash = self.compute_md5(image)

            # Determine image reference for UI
            if image_path.startswith(input_dir):
                type_ = "input"
                filename = os.path.relpath(image_path, input_dir)
            elif image_path.startswith(output_dir):
                type_ = "output"
                filename = os.path.relpath(image_path, output_dir)
            else:
                temp_filename = f"{image_hash}.png"
                temp_path = os.path.join(temp_dir, temp_filename)
                if not os.path.exists(temp_path):
                    image.save(temp_path)
                type_ = "temp"
                filename = temp_filename

            # Handle notes: append new notes and read all
            note_path = os.path.join(self.note_dir, f"{image_hash}.txt")
            if all_notes:
                with open(note_path, "a", encoding="utf-8") as f:
                    for n in all_notes:
                        f.write(n + "\n")
            if os.path.exists(note_path):
                with open(note_path, "r", encoding="utf-8") as f:
                    output_note = f.read().rstrip()  # Remove trailing newline

            ui_images = [{"filename": filename, "subfolder": "", "type": type_}]
            result = (image_path, output_note)

        # Case 2: Image provided as tensor
        elif images is not None and len(images) > 0:
            image_np = (images[0].numpy() * 255).astype(np.uint8)
            image = Image.fromarray(image_np)
            image_hash = self.compute_md5(image)

            temp_filename = f"{image_hash}.png"
            temp_path = os.path.join(temp_dir, temp_filename)
            if not os.path.exists(temp_path):
                image.save(temp_path)

            # Handle notes: append new notes and read all
            note_path = os.path.join(self.note_dir, f"{image_hash}.txt")
            if all_notes:
                with open(note_path, "a", encoding="utf-8") as f:
                    for n in all_notes:
                        f.write(n + "\n")
            if os.path.exists(note_path):
                with open(note_path, "r", encoding="utf-8") as f:
                    output_note = f.read().rstrip()

            ui_images = [{"filename": temp_filename, "subfolder": "", "type": "temp"}]
            result = (temp_path, output_note)

        # Case 3: No image provided
        else:
            result = ("", "")

        return {"ui": {"images": ui_images}, "result": result}

class ImageNoteLoadImage:
    def __init__(self):
        self.note_dir = os.path.join("ComfyUI", "Bjornulf", "imageNote")
        os.makedirs(self.note_dir, exist_ok=True)

    @classmethod
    def INPUT_TYPES(s):
        base_input_dir = folder_paths.get_input_directory()
        input_dir = os.path.join(base_input_dir, "Bjornulf", "imagenote_images")
        if not os.path.exists(input_dir):
            os.makedirs(input_dir, exist_ok=True)
        valid_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')
        files = [f for f in os.listdir(input_dir) if 
                 os.path.isfile(os.path.join(input_dir, f)) and 
                 f.lower().endswith(valid_extensions)]
        if not files:
            files = ["none"]
        return {
            "required": {
                "image": (sorted(files), {"image_upload": True}),
                "note": ("STRING", {"default": ""}),
                "note_2": ("STRING", {"default": ""}),
                "note_3": ("STRING", {"default": ""})
            }
        }

    RETURN_TYPES = ("IMAGE", "MASK", "STRING", "STRING")
    RETURN_NAMES = ("image", "mask", "image_path", "note")
    FUNCTION = "load_image_alpha"
    CATEGORY = "Bjornulf"

    def compute_md5(self, image):
        """Compute MD5 hash of an image for note association."""
        if isinstance(image, Image.Image):
            image_bytes = image.tobytes()
        elif isinstance(image, torch.Tensor):
            image_bytes = (image.numpy() * 255).astype(np.uint8).tobytes()
        else:
            image_bytes = image
        return hashlib.md5(image_bytes).hexdigest()

    def load_image_alpha(self, image, note="", note_2="", note_3=""):
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
            image_converted = i.convert("RGBA")
            if len(output_images) == 0:
                w = image_converted.size[0]
                h = image_converted.size[1]
            if image_converted.size[0] != w or image_converted.size[1] != h:
                continue
            image_np = np.array(image_converted).astype(np.float32) / 255.0
            image_tensor = torch.from_numpy(image_np)[None,]
            if 'A' in i.getbands():
                mask = np.array(i.getchannel('A')).astype(np.float32) / 255.0
                mask = 1. - torch.from_numpy(mask)
            else:
                mask = torch.zeros((64, 64), dtype=torch.float32, device="cpu")
            output_images.append(image_tensor)
            output_masks.append(mask.unsqueeze(0))

        if len(output_images) > 1 and img.format not in excluded_formats:
            output_image = torch.cat(output_images, dim=0)
            output_mask = torch.cat(output_masks, dim=0)
        else:
            output_image = output_images[0]
            output_mask = output_masks[0]

        # Compute hash from the first image
        first_image = output_image[0] if output_image.dim() == 4 else output_image
        image_hash = self.compute_md5(first_image)

        # Handle notes: append new notes and read all
        all_notes = [n for n in [note, note_2, note_3] if n]
        note_path = os.path.join(self.note_dir, f"{image_hash}.txt")
        if all_notes:
            with open(note_path, "a", encoding="utf-8") as f:
                for n in all_notes:
                    f.write(n + "\n")
        output_note = ""
        if os.path.exists(note_path):
            with open(note_path, "r", encoding="utf-8") as f:
                output_note = f.read().rstrip()

        return (output_image, output_mask, image_path, output_note)

    @classmethod
    def IS_CHANGED(s, image, note, note_2, note_3):
        image_path = folder_paths.get_annotated_filepath(image)
        m = hashlib.sha256()
        with open(image_path, 'rb') as f:
            m.update(f.read())
        return m.digest().hex() + str(note) + str(note_2) + str(note_3)

    @classmethod
    def VALIDATE_INPUTS(s, image):
        if not folder_paths.exists_annotated_filepath(image):
            return "Invalid image file: {}".format(image)
        return True
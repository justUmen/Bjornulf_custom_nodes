import os
import numpy as np
from PIL import Image
import json
from PIL.PngImagePlugin import PngInfo
import torch

class SaveTmpImage:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE", {"forceInput": True}),
            },
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
        }

    FUNCTION = "save_image"
    RETURN_TYPES = ()
    OUTPUT_NODE = True
    CATEGORY = "Bjornulf"

    def save_image(self, image, prompt=None, extra_pnginfo=None):
        # Ensure the output directory exists
        os.makedirs("./output", exist_ok=True)

        # Convert the image from ComfyUI format to PIL Image
        i = 255. * image.cpu().numpy()
        # Reshape the image if it's not in the expected format, remove any leading dimensions of size 1
        if i.ndim > 3:
            i = np.squeeze(i)
        # Ensure the image is 3D (height, width, channels)
        if i.ndim == 2:
            i = i[:, :, np.newaxis]  # Add a channel dimension if it's missing

        img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))

        # Prepare metadata
        metadata = PngInfo()
        if prompt is not None:
            metadata.add_text("prompt", json.dumps(prompt))
        if extra_pnginfo is not None:
            for k, v in extra_pnginfo.items():
                metadata.add_text(k, json.dumps(v))

        # Save the image with metadata, overwriting if it exists
        filename = "./output/tmp_api.png"
        img.save(filename, format="PNG", pnginfo=metadata)

        print(f"Temporary image saved as: {filename}")

        return {"ui": {"images": [{"filename": filename, "type": "output"}]}}
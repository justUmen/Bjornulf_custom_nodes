import os
import requests
from PIL import Image
import numpy as np
import torch
import base64

class APIGenerateGPT4o:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_key": ("STRING", {
                    "multiline": False,
                    "default": ""  # User provides their OpenAI API key
                }),
                "prompt": ("STRING", {
                    "multiline": True,
                    "default": "A cute baby sea otter"
                }),
                "size": (["1024x1024", "1536x1024", "1024x1536", "auto"], {
                    "default": "1536x1024"
                }),
            },
            "optional": {
                "background": (["auto", "transparent", "opaque"], {
                    "default": "auto"
                }),
                "moderation": (["auto", "low"], {
                    "default": "auto"
                }),
                "output_format": (["png", "jpeg", "webp"], {
                    "default": "png"
                }),
                "quality": (["auto", "high", "medium", "low"], {
                    "default": "auto"
                }),
                "n": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 1
                }),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate"
    CATEGORY = "OpenAI API"

    def get_next_number(self):
        """Get the next available number for naming saved image files."""
        save_dir = "output/API/OpenAI_GPT4o"
        os.makedirs(save_dir, exist_ok=True)
        files = [f for f in os.listdir(save_dir) if f.endswith('.png')]
        if not files:
            return 1
        numbers = [int(f.split('.')[0]) for f in files]
        return max(numbers) + 1

    def generate(self, api_key, prompt, size, background="auto", moderation="auto", output_format="png", quality="auto", n=1):
        """Generate an image using the OpenAI gpt-image-1 model and return it as a tensor."""
        # API headers
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        # API payload
        payload = {
            "model": "gpt-image-1",
            "prompt": prompt,
            "n": n,
            "size": size,
            "background": background,
            "moderation": moderation,
            "output_format": output_format,
            "quality": quality
        }

        # Send request to OpenAI API
        response = requests.post(
            "https://api.openai.com/v1/images/generations",
            headers=headers,
            json=payload
        )
        if response.status_code != 200:
            raise Exception(f"API request failed: {response.text}")

        # Parse response and extract base64 image data
        data = response.json()
        b64_data = data["data"][0]["b64_json"]
        
        # Decode base64 data into image bytes
        image_bytes = base64.b64decode(b64_data)

        # Save the image with an incrementing filename
        next_num = self.get_next_number()
        filename = f"{next_num:03d}.png"
        filepath = os.path.join("output/API/OpenAI_GPT4o", filename)
        with open(filepath, "wb") as f:
            f.write(image_bytes)

        # Load and process the image
        img = Image.open(filepath)
        if img.mode != "RGB":
            img = img.convert("RGB")
        
        # Convert to tensor for ComfyUI
        img_tensor = torch.from_numpy(np.array(img).astype(np.float32) / 255.0)
        img_tensor = img_tensor.unsqueeze(0)

        return (img_tensor,)
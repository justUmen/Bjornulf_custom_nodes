import numpy as np
import torch
from PIL import Image

class ResizeImage:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE", {}),
                "width": ("INT", {"default": 256}),
                "height": ("INT", {"default": 256}),
            },
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
        }

    FUNCTION = "resize_image"
    RETURN_TYPES = ("IMAGE",)
    OUTPUT_NODE = True
    CATEGORY = "Bjornulf"

    def resize_image(self, image, width=256, height=256, prompt=None, extra_pnginfo=None):
        # Ensure the input image is on CPU and convert to numpy array
        image_np = image.cpu().numpy()
        
        # Get original dimensions
        if image_np.ndim == 4:
            orig_height, orig_width = image_np.shape[1:3]
        else:
            orig_height, orig_width = image_np.shape[:2]
        
        # Calculate new dimensions maintaining aspect ratio if needed
        aspect_ratio = orig_width / orig_height
        
        if width == 0 and height == 0:
            # If both are 0, use original dimensions
            new_width, new_height = orig_width, orig_height
        elif width == 0:
            # If width is 0, calculate it based on height
            new_height = height
            new_width = int(height * aspect_ratio)
        elif height == 0:
            # If height is 0, calculate it based on width
            new_width = width
            new_height = int(width / aspect_ratio)
        else:
            # Use provided dimensions
            new_width, new_height = width, height

        # Check if the image is in the format [batch, height, width, channel]
        if image_np.ndim == 4:
            # If so, we'll process each image in the batch
            resized_images = []
            for img in image_np:
                # Convert to PIL Image
                pil_img = Image.fromarray((img * 255).astype(np.uint8))
                # Resize
                resized_pil = pil_img.resize((new_width, new_height), Image.LANCZOS)
                # Convert back to numpy and normalize
                resized_np = np.array(resized_pil).astype(np.float32) / 255.0
                resized_images.append(resized_np)
            
            # Stack the resized images back into a batch
            resized_batch = np.stack(resized_images)
            # Convert to torch tensor
            resized_tensor = torch.from_numpy(resized_batch)
        else:
            # If it's a single image, process it directly
            # Convert to PIL Image
            pil_img = Image.fromarray((image_np * 255).astype(np.uint8))
            # Resize
            resized_pil = pil_img.resize((new_width, new_height), Image.LANCZOS)
            # Convert back to numpy and normalize
            resized_np = np.array(resized_pil).astype(np.float32) / 255.0
            # Add batch dimension if it was originally present
            if image.dim() == 4:
                resized_np = np.expand_dims(resized_np, axis=0)
            # Convert to torch tensor
            resized_tensor = torch.from_numpy(resized_np)

        # Update metadata if needed
        if extra_pnginfo is not None:
            extra_pnginfo["resized_width"] = new_width
            extra_pnginfo["resized_height"] = new_height

        return (resized_tensor, prompt, extra_pnginfo)
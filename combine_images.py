import torch
import numpy as np
# import logging

class CombineImages:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "number_of_images": ("INT", {"default": 2, "min": 1, "max": 50, "step": 1}),
                "all_in_one": ("BOOLEAN", {"default": False}),
                "image_1": ("IMAGE",),
            },
            "hidden": {
                **{f"image_{i}": ("IMAGE",) for i in range(2, 51)}
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "all_in_one_images"
    OUTPUT_NODE = True
    CATEGORY = "Bjornulf"

    def all_in_one_images(self, number_of_images, all_in_one, ** kwargs):
        images = [kwargs[f"image_{i}"] for i in range(1, number_of_images + 1) if f"image_{i}" in kwargs]
        
        # for i, img in enumerate(images):
        #     logging.info(f"Image {i+1} shape: {img.shape}, dtype: {img.dtype}, min: {img.min()}, max: {img.max()}")
        
        if all_in_one:
            # Check if all images have the same shape
            shapes = [img.shape for img in images]
            if len(set(shapes)) > 1:
                raise ValueError("All images must have the same resolution to use all_in_one. "
                                 f"Found different shapes: {shapes}")
            
            # Convert images to float32 and scale to 0-1 range if necessary
            processed_images = []
            for img in images:
                if isinstance(img, np.ndarray):
                    if img.dtype == np.uint8:
                        img = img.astype(np.float32) / 255.0
                    elif img.dtype == np.bool_:
                        img = img.astype(np.float32)
                elif isinstance(img, torch.Tensor):
                    if img.dtype == torch.uint8:
                        img = img.float() / 255.0
                    elif img.dtype == torch.bool:
                        img = img.float()
                
                # Ensure the image is 3D (height, width, channels)
                if img.ndim == 4:
                    img = img.squeeze(0)
                
                processed_images.append(img)
            
            # Stack all images along a new dimension
            if isinstance(processed_images[0], np.ndarray):
                all_in_oned = np.stack(processed_images)
                all_in_oned = torch.from_numpy(all_in_oned)
            else:
                all_in_oned = torch.stack(processed_images)
            
            # Ensure the output is in the format expected by the preview node
            # (batch, height, width, channels)
            if all_in_oned.ndim == 3:
                all_in_oned = all_in_oned.unsqueeze(0)
            if all_in_oned.shape[-1] != 3 and all_in_oned.shape[-1] != 4:
                all_in_oned = all_in_oned.permute(0, 2, 3, 1)
            
            return (all_in_oned,)
        else:
            # Return a single tuple containing all images (original behavior)
            return (images,)

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")

    @classmethod
    def VALIDATE_INPUTS(cls, ** kwargs):
        if kwargs['all_in_one']:
            cls.OUTPUT_IS_LIST = (False,)
        else:
            cls.OUTPUT_IS_LIST = (True,)
        return True

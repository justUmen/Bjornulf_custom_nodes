import torch
import numpy as np

class CombineImages:
    SPECIAL_PREFIX = "ImSpEcIaL"  # The special text prefix to look for

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

    def all_in_one_images(self, number_of_images, all_in_one, **kwargs):
        # Retrieve all inputs based on number_of_images
        inputs = [kwargs.get(f"image_{i}", None) for i in range(1, number_of_images + 1)]

        # Check for special text input with "ImSpEcIaL" prefix
        for i, inp in enumerate(inputs):
            if isinstance(inp, str):
                if inp.startswith(self.SPECIAL_PREFIX):
                    # Extract the text after the prefix (for logging or future use)
                    text_after_prefix = inp[len(self.SPECIAL_PREFIX):].lstrip()
                    # Return a dummy image as a placeholder
                    # Note: Adjust this to return an actual image if necessary
                    dummy_image = torch.zeros((1, 256, 256, 3), dtype=torch.float32)
                    return (dummy_image,)
                else:
                    # Ignore non-special text inputs (e.g., empty strings or other text)
                    inputs[i] = None

        # Filter out None values (ignored inputs) and non-image inputs
        images = []
        for inp in inputs:
            if inp is not None and not isinstance(inp, str):
                images.append(inp)

        # Check if there are any valid images
        if not images:
            raise ValueError("No valid image inputs provided after filtering non-image inputs.")

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
            # Return a single tuple containing all valid images
            return (images,)

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")

    @classmethod
    def VALIDATE_INPUTS(cls, **kwargs):
        if kwargs['all_in_one']:
            cls.OUTPUT_IS_LIST = (False,)
        else:
            cls.OUTPUT_IS_LIST = (True,)
        return True
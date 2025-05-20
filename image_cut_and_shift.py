import torch
import numpy as np
from PIL import Image

class HorizontalCutAndShift:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),                  # Input image tensor
                "X": ("INT", {"default": 0, "min": 0, "max": 4096}),  # Cut position
                "Y": ("INT", {"default": 0, "min": 0, "max": 4096}),  # Upward shift for bottom
                "Z": ("INT", {"default": 0, "min": 0, "max": 4096}),  # Downward shift for top
                "fill_color": (["black", "white"],),  # New option for fill color
            }
        }

    RETURN_TYPES = ("IMAGE",)  # Output is an image tensor
    FUNCTION = "process"       # Processing function name
    CATEGORY = "image"         # Node category in ComfyUI

    def process(self, image, X, Y, Z, fill_color):
        # Get image dimensions: batch size, height, width, channels
        batch, H, W, channels = image.shape

        # Initialize output tensor based on the selected fill color
        if fill_color == "black":
            output = torch.zeros_like(image)  # Zeros for black
        elif fill_color == "white":
            output = torch.ones_like(image)   # Ones for white
        else:
            raise ValueError("Invalid fill_color: must be 'black' or 'white'")

        # Process the bottom part: shift upward by Y pixels
        bottom_dest_start = max(X - Y, 0)
        bottom_dest_end = min(H - 1 - Y, H - 1)
        if bottom_dest_start <= bottom_dest_end:
            num_rows_bottom = bottom_dest_end - bottom_dest_start + 1
            bottom_src_start = bottom_dest_start + Y
            bottom_src_end = bottom_src_start + num_rows_bottom - 1
            if bottom_src_start < X:
                offset = X - bottom_src_start
                bottom_dest_start += offset
                bottom_src_start = X
                num_rows_bottom -= offset
            if bottom_src_end >= H:
                excess = bottom_src_end - (H - 1)
                num_rows_bottom -= excess
                bottom_dest_end = bottom_dest_start + num_rows_bottom - 1
            if num_rows_bottom > 0:
                output[:, bottom_dest_start:bottom_dest_end + 1, :, :] = \
                    image[:, bottom_src_start:bottom_src_end + 1, :, :]

        # Process the top part: shift downward by Z pixels
        top_dest_start = max(Z, 0)
        top_dest_end = min(X - 1 + Z, H - 1)
        if top_dest_start <= top_dest_end:
            num_rows_top = top_dest_end - top_dest_start + 1
            top_src_start = top_dest_start - Z
            top_src_end = top_src_start + num_rows_top - 1
            if top_src_end >= X:
                excess = top_src_end - (X - 1)
                num_rows_top -= excess
                top_dest_end = top_dest_start + num_rows_top - 1
            if num_rows_top > 0:
                output[:, top_dest_start:top_dest_end + 1, :, :] = \
                    image[:, top_src_start:top_src_end + 1, :, :]

        return (output,)  # Return the output tensor as a tuple
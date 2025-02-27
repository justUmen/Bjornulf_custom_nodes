import torch
import numpy as np
from PIL import Image
import io

class ImageDetails:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image_input": ("IMAGE",),
            },
        }

    RETURN_TYPES = ("INT", "INT", "BOOL", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("WIDTH", "HEIGHT", "HAS_TRANSPARENCY", "ORIENTATION", "TYPE", "ALL")
    FUNCTION = "show_image_details"
    OUTPUT_NODE = True
    CATEGORY = "Bjornulf"

    def show_image_details(self, image_input):
        if isinstance(image_input, torch.Tensor):
            is_tensor = True
            input_type = "tensor"
            # Ensure the tensor is on CPU and convert to numpy
            image_input = image_input.cpu().numpy()
        elif isinstance(image_input, (bytes, bytearray)):
            is_tensor = False
            input_type = "bytes"
            image_input = [image_input]  # Wrap single bytes object in a list
        else:
            is_tensor = False
            input_type = "bytes"
        
        all_widths, all_heights, all_transparencies, all_details, all_orientations = [], [], [], [], []

        if is_tensor:
            # Handle tensor images
            if len(image_input.shape) == 5:  # (batch, 1, channels, height, width)
                image_input = np.squeeze(image_input, axis=1)
            
            batch_size = image_input.shape[0]
            for i in range(batch_size):
                image = image_input[i]
                
                # Ensure the image is in HxWxC format
                if image.shape[0] == 3 or image.shape[0] == 4:  # If it's in CxHxW format
                    image = np.transpose(image, (1, 2, 0))  # Change to HxWxC
                
                # Normalize to 0-255 range if necessary
                if image.max() <= 1:
                    image = (image * 255).astype('uint8')
                else:
                    image = image.astype('uint8')
                
                pil_image = Image.fromarray(image)
                self.process_image(pil_image, input_type, all_widths, all_heights, all_transparencies, all_details, all_orientations)
        else:
            # Handle bytes-like objects
            batch_size = len(image_input)
            for i in range(batch_size):
                pil_image = Image.open(io.BytesIO(image_input[i]))
                self.process_image(pil_image, input_type, all_widths, all_heights, all_transparencies, all_details, all_orientations)

        # Combine all details into a single string
        combined_details = "\n".join(all_details)

        # Return the details of the first image, plus the combined details string
        return (all_widths[0], all_heights[0], all_transparencies[0], all_orientations[0], 
                input_type, combined_details)

    def process_image(self, pil_image, input_type, all_widths, all_heights, all_transparencies, all_details, all_orientations):
        # Get image details
        width, height = pil_image.size
        has_transparency = pil_image.mode in ('RGBA', 'LA') or \
                           (pil_image.mode == 'P' and 'transparency' in pil_image.info)

        # Determine orientation
        if width > height:
            orientation = "landscape"
        elif height > width:
            orientation = "portrait"
        else:
            orientation = "square"

        # Prepare the ALL string
        details = f"\nType: {input_type}"
        details += f"\nWidth: {width}"
        details += f"\nHeight: {height}"
        details += f"\nNumber of Pixels: {width * height}"
        details += f"\nLoaded with transparency: {has_transparency}"
        details += f"\nImage Mode: {pil_image.mode}"
        details += f"\nOrientation: {orientation}\n"

        all_widths.append(width)
        all_heights.append(height)
        all_transparencies.append(has_transparency)
        all_details.append(details)
        all_orientations.append(orientation)

import torch
import os
import shutil
from PIL import Image
import numpy as np

class VideoPingPong:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("IMAGES",)
    FUNCTION = "pingpong_images"
    CATEGORY = "Bjornulf"

    def pingpong_images(self, images):
        # Create a clean folder to store the images
        temp_dir = "temp_pingpong"
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.makedirs(temp_dir)

        try:
            # Save each image in the temporary directory
            num_images = images.shape[0]
            for i in range(num_images):
                img_tensor = images[i]
                img_pil = Image.fromarray((img_tensor.cpu().numpy() * 255).astype('uint8'))
                img_path = os.path.join(temp_dir, f"image_{i:04d}.png")
                img_pil.save(img_path)

            # Create the pingpong sequence
            pingpong_list = list(range(num_images)) + list(range(num_images - 2, 0, -1))

            # Process images in batches
            batch_size = 10
            pingpong_tensors = []
            
            for i in range(0, len(pingpong_list), batch_size):
                batch = pingpong_list[i:i+batch_size]
                batch_tensors = []
                
                for j in batch:
                    img_path = os.path.join(temp_dir, f"image_{j:04d}.png")
                    img_pil = Image.open(img_path)
                    img_np = np.array(img_pil).astype(np.float32) / 255.0
                    img_tensor = torch.from_numpy(img_np)
                    batch_tensors.append(img_tensor)
                    
                    # Close the image to free up memory
                    img_pil.close()
                
                # Stack the batch tensors
                batch_tensor = torch.stack(batch_tensors)
                pingpong_tensors.append(batch_tensor)
                
                # Clear unnecessary variables
                del batch_tensors
                torch.cuda.empty_cache()

            # Concatenate all batches
            pingpong_tensor = torch.cat(pingpong_tensors, dim=0)

        finally:
            # Clean up the temporary directory
            shutil.rmtree(temp_dir)

        return (pingpong_tensor,)
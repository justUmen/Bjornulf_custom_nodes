import numpy as np
import scipy.ndimage as ndi
import torch

class LargestMaskOnly:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mask": ("MASK",),
            }
        }
    
    RETURN_TYPES = ("MASK",)
    FUNCTION = "process"
    CATEGORY = "mask"

    def process(self, mask):
        # Convert mask to numpy array
        mask_np = mask.cpu().numpy()
        
        # Print debug info about mask
        print(f"Mask shape: {mask_np.shape}")
        print(f"Mask dtype: {mask_np.dtype}")
        print(f"Mask min: {mask_np.min()}, max: {mask_np.max()}")
        
        # Ensure binary mask (0 and 1)
        binary_mask = (mask_np > 0.5).astype(np.uint8)
        
        # Use scipy's label function instead of OpenCV
        labeled_array, num_features = ndi.label(binary_mask)
        print(f"Found {num_features} connected components")
        
        if num_features <= 1:  # No components or just one
            return (mask,)
        
        # Find sizes of all labeled regions
        sizes = np.bincount(labeled_array.ravel())
        # Skip background (label 0)
        if len(sizes) > 1:
            sizes = sizes[1:]
            # Find the label of the largest component (add 1 because we skipped background)
            largest_label = np.argmax(sizes) + 1
            # Create a mask with only the largest component
            largest_mask = (labeled_array == largest_label).astype(np.float32)
        else:
            # Fallback if something went wrong with the labeling
            largest_mask = binary_mask.astype(np.float32)
        
        # Convert back to tensor and return
        result = torch.from_numpy(largest_mask)
        return (result,)

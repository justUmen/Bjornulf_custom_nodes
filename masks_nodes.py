import numpy as np
import scipy.ndimage as ndi
import torch

class BodyPartSelectorMask:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "mask": ("MASK",),
                "selection": (["head", "hands", "feet"],),
            }
        }
    
    RETURN_TYPES = ("MASK",)
    FUNCTION = "process"
    CATEGORY = "Bjornulf"

    def process_single(self, mask_np, selection):
        """
        Process a single 2D mask to select head, hands, or feet based on position.
        
        Args:
            mask_np: 2D numpy array (H, W)
            selection: str, one of "head", "hands", "feet"
        
        Returns:
            2D numpy array with selected shapes
        """
        # Convert to binary mask
        binary_mask = (mask_np > 0.5).astype(np.uint8)
        
        # Label connected components
        labeled_array, num_features = ndi.label(binary_mask)
        if num_features < 5:
            raise ValueError(f"Expected at least 5 components, found {num_features}")
        
        # Compute sizes of all components (excluding background)
        sizes = np.bincount(labeled_array.ravel())[1:]
        # Select the five largest components
        largest_indices = np.argsort(sizes)[-5:][::-1]  # Top 5 in descending order
        largest_labels = largest_indices + 1  # Map to label numbers (1-based)
        
        # Compute centroids for the five largest components
        centroids = []
        for label in largest_labels:
            positions = np.argwhere(labeled_array == label)
            if len(positions) > 0:
                centroid_row = positions[:, 0].mean()  # Average row
                centroid_col = positions[:, 1].mean()  # Average column
                centroids.append((label, centroid_row, centroid_col))
        
        # Sort by centroid row (ascending, since row 0 is top)
        centroids.sort(key=lambda x: x[1])
        
        # Assign components based on vertical position
        head_label = centroids[0][0]          # Smallest row (top)
        hand_labels = [centroids[1][0], centroids[2][0]]  # Middle two
        feet_labels = [centroids[3][0], centroids[4][0]]  # Largest rows (bottom)
        
        # Select labels based on user input
        if selection == "head":
            selected_labels = [head_label]
        elif selection == "hands":
            selected_labels = hand_labels
        elif selection == "feet":
            selected_labels = feet_labels
        else:
            raise ValueError("Selection must be 'head', 'hands', or 'feet'")
        
        # Create new mask with selected components
        new_mask = np.isin(labeled_array, selected_labels).astype(np.float32)
        return new_mask

    def process(self, mask, selection):
        """
        Process the input mask(s) and return a new mask with selected parts.
        
        Args:
            mask: torch tensor, either 2D (H, W) or 3D (N, H, W)
            selection: str, one of "head", "hands", "feet"
        
        Returns:
            Tuple containing the output mask tensor
        """
        mask_np = mask.cpu().numpy()
        
        if mask_np.ndim == 2:
            # Single mask
            result = self.process_single(mask_np, selection)
            result = result[None, ...]  # Add batch dimension: (1, H, W)
        elif mask_np.ndim == 3:
            # Batched masks
            results = [self.process_single(mask_np[i], selection) 
                      for i in range(mask_np.shape[0])]
            result = np.stack(results, axis=0)  # Stack to (N, H, W)
        else:
            raise ValueError("Mask must be 2D (H, W) or 3D (N, H, W)")
        
        return (torch.from_numpy(result),)
class LargestMaskOnly:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "mask": ("MASK",),
                "num_masks": ("INT", {"default": 1, "min": 1, "max": 10}),
            }
        }
    
    RETURN_TYPES = ("MASK",)
    FUNCTION = "process"
    CATEGORY = "Bjornulf"

    def process_single(self, mask_np, num_masks):
        """Process a single mask to keep the top num_masks largest components."""
        # Convert to binary mask
        binary_mask = (mask_np > 0.5).astype(np.uint8)
        # Label connected components
        labeled_array, num_features = ndi.label(binary_mask)
        
        if num_features > 0:
            # Get sizes of all components, excluding background (label 0)
            sizes = np.bincount(labeled_array.ravel())[1:]
            # Determine how many components to keep
            k = min(num_masks, num_features)
            if k > 0:
                # Get indices of the top k largest components (descending order)
                top_indices = np.argsort(sizes)[::-1][:k]
                # Map indices to labels (add 1 since sizes[1:] starts at label 1)
                top_labels = top_indices + 1
                # Create mask with only the top k components
                largest_mask = np.isin(labeled_array, top_labels).astype(np.float32)
            else:
                largest_mask = np.zeros_like(binary_mask, dtype=np.float32)
        else:
            # No components found, return an empty mask
            largest_mask = np.zeros_like(binary_mask, dtype=np.float32)
        
        return largest_mask

    def process(self, mask, num_masks):
        """Process the input mask(s) and return the top num_masks largest components."""
        # Convert mask to numpy array
        mask_np = mask.cpu().numpy()
        
        if mask_np.ndim == 2:
            # Single mask: process and add batch dimension
            result = self.process_single(mask_np, num_masks)
            result = result[None, ...]  # Shape becomes (1, H, W)
        elif mask_np.ndim == 3:
            # Batched masks: process each mask independently
            results = [self.process_single(mask_np[i], num_masks) for i in range(mask_np.shape[0])]
            result = np.stack(results, axis=0)  # Shape remains (N, H, W)
        else:
            raise ValueError("Invalid mask shape: expected 2D (H, W) or 3D (N, H, W)")
        
        # Convert back to torch tensor and return as a tuple
        return (torch.from_numpy(result),)

class BoundingRectangleMask:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "mask": ("MASK",),
                "up": ("INT", {"default": 0, "min": -10000, "max": 10000}),
                "down": ("INT", {"default": 0, "min": -10000, "max": 10000}),
                "right": ("INT", {"default": 0, "min": -10000, "max": 10000}),
                "left": ("INT", {"default": 0, "min": -10000, "max": 10000}),
            }
        }
    
    RETURN_TYPES = ("MASK",)
    FUNCTION = "process"
    CATEGORY = "Bjornulf"

    def process_single(self, mask_np, up, down, right, left):
        active = mask_np > 0.5
        if not np.any(active):
            return np.zeros_like(mask_np, dtype=np.float32)
        
        rows_with_active = np.any(active, axis=1)
        cols_with_active = np.any(active, axis=0)
        min_row = np.where(rows_with_active)[0][0]
        max_row = np.where(rows_with_active)[0][-1]
        min_col = np.where(cols_with_active)[0][0]
        max_col = np.where(cols_with_active)[0][-1]
        
        min_row_adj = min_row - up
        max_row_adj = max_row + down
        min_col_adj = min_col - left
        max_col_adj = max_col + right
        
        H, W = mask_np.shape
        min_row_adj = max(0, min_row_adj)
        max_row_adj = min(H - 1, max_row_adj)
        min_col_adj = max(0, min_col_adj)
        max_col_adj = min(W - 1, max_col_adj)
        
        if min_row_adj > max_row_adj or min_col_adj > max_col_adj:
            return np.zeros_like(mask_np, dtype=np.float32)
        
        new_mask = np.zeros_like(mask_np, dtype=np.float32)
        new_mask[min_row_adj:max_row_adj + 1, min_col_adj:max_col_adj + 1] = 1.0
        return new_mask

    def process(self, mask, up, down, right, left):
        mask_np = mask.cpu().numpy()
        
        if mask_np.ndim == 2:
            result = self.process_single(mask_np, up, down, right, left)
            result = result[None, ...]
        elif mask_np.ndim == 3:
            results = [self.process_single(mask_np[i], up, down, right, left) 
                      for i in range(mask_np.shape[0])]
            result = np.stack(results, axis=0)
        else:
            raise ValueError("Mask must be 2D (H, W) or 3D (N, H, W)")
        
        return (torch.from_numpy(result),)
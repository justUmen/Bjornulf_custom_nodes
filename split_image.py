import torch

class SplitImageGrid:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "rows": ("INT", {"default": 1, "min": 1, "max": 9}),
                "columns": ("INT", {"default": 1, "min": 1, "max": 9}),
                "MODIFIED_part_index": ("INT", {"default": 1, "min": 1, "max": 9}),
            }
        }

    RETURN_TYPES = ["IMAGE"] * 9 + ["INT", "INT", "IMAGE", "INT"]
    RETURN_NAMES = [f"part_{i}" for i in range(1, 10)] + ["rows", "columns", "MODIFIED_part", "MODIFIED_part_index"]
    FUNCTION = "split"
    CATEGORY = "image"

    def split(self, image, rows, columns, MODIFIED_part_index):
        # Get image dimensions
        B, H, W, C = image.shape
        # Removed check: if H % rows != 0 or W % columns != 0:
        #     raise ValueError("Image dimensions must be divisible by rows and columns")
        
        # Calculate base part dimensions
        part_height = H // rows
        part_width = W // columns
        O = 2  # Overlap of 2 pixels
        parts = []
        
        # Split image with overlap
        for r in range(rows):
            for c in range(columns):
                # Define slicing indices with overlap
                h_start = max(0, r * part_height - O)  # Extend O pixels up, but not beyond top
                h_end = min(H, (r + 1) * part_height + O)  # Extend O pixels down, not beyond bottom
                w_start = max(0, c * part_width - O)  # Extend O pixels left, not beyond left edge
                w_end = min(W, (c + 1) * part_width + O)  # Extend O pixels right, not beyond right edge
                part = image[:, h_start:h_end, w_start:w_end, :]
                parts.append(part)
        
        # Pad unused parts with None
        while len(parts) < 9:
            parts.append(None)
        
        # Adjust MODIFIED_part_index to 0-based and validate
        MODIFIED_index = MODIFIED_part_index - 1
        if MODIFIED_index < 0 or MODIFIED_index >= rows * columns:
            raise ValueError(f"MODIFIED_part_index {MODIFIED_part_index} is out of range for {rows}x{columns} grid")
        MODIFIED_part = parts[MODIFIED_index]
        
        return tuple(parts + [rows, columns, MODIFIED_part, MODIFIED_part_index])

class ReassembleImageGrid:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "original": ("IMAGE",),
                "rows": ("INT", {"default": 1, "min": 1, "max": 10}),
                "columns": ("INT", {"default": 1, "min": 1, "max": 10}),
            },
            "optional": {
                "part_1": ("IMAGE",),
                "part_2": ("IMAGE",),
                "part_3": ("IMAGE",),
                "part_4": ("IMAGE",),
                "part_5": ("IMAGE",),
                "part_6": ("IMAGE",),
                "part_7": ("IMAGE",),
                "part_8": ("IMAGE",),
                "part_9": ("IMAGE",),
                "MODIFIED_part": ("IMAGE",),
                "MODIFIED_part_index": ("INT", {"default": 0, "min": 0, "max": 9}),
                "reference_video_part_index": ("INT", {"default": 0, "min": 0, "max": 9}),
                "auto_resize": ("BOOLEAN", {"default": True}),  # Add option to enable/disable auto-resizing
            }
        }

    RETURN_TYPES = ["IMAGE"]
    RETURN_NAMES = ["image"]
    FUNCTION = "reassemble"
    CATEGORY = "image"

    def repeat_frames(self, tensor, k):
        """Repeat the tensor k times along the batch dimension."""
        return tensor.repeat(k, 1, 1, 1) if k > 1 else tensor

    def adjust_frame_count_with_repeat(self, tensor, B_ref, B_original):
        """Adjust frame count, considering repetition if B_ref ≈ k * B_original."""
        if B_original == 0:
            raise ValueError("Original frame count is zero")
        k = round(B_ref / B_original)
        if k > 0 and abs(B_ref - k * B_original) <= 1:
            repeated = self.repeat_frames(tensor, k)
            if repeated.shape[0] > B_ref:
                repeated = repeated[:B_ref]
            elif repeated.shape[0] < B_ref:
                pad_size = B_ref - repeated.shape[0]
                last_frame = repeated[-1:].repeat(pad_size, 1, 1, 1)
                repeated = torch.cat([repeated, last_frame], dim=0)
            return repeated
        else:
            return self.adjust_frame_count(tensor, B_ref)

    def adjust_frame_count(self, tensor, target_B):
        """Adjust the frame count of a tensor to match target_B by repeating or skipping frames."""
        B = tensor.shape[0]
        if B == target_B:
            return tensor
        indices = torch.linspace(0, B - 1, steps=target_B).round().long()
        indices = indices.clamp(0, B - 1)
        return tensor[indices]
    
    def resize_tensor(self, tensor, target_height, target_width):
        """Resize tensor to target dimensions using interpolation."""
        import torch.nn.functional as F
        B, H, W, C = tensor.shape
        
        # PyTorch's F.interpolate expects [B, C, H, W] format
        # So we need to permute, resize, then permute back
        tensor_BCHW = tensor.permute(0, 3, 1, 2)  # [B, H, W, C] -> [B, C, H, W]
        
        # Resize using bilinear interpolation
        resized = F.interpolate(
            tensor_BCHW, 
            size=(target_height, target_width), 
            mode='bilinear', 
            align_corners=False
        )
        
        # Convert back to [B, H, W, C] format
        return resized.permute(0, 2, 3, 1)  # [B, C, H, W] -> [B, H, W, C]

    def reassemble(self, original, rows, columns, part_1=None, part_2=None, part_3=None, 
                   part_4=None, part_5=None, part_6=None, part_7=None, part_8=None, 
                   part_9=None, MODIFIED_part=None, MODIFIED_part_index=0, 
                   reference_video_part_index=0, auto_resize=True):
        # Get original dimensions
        B, H, W, C = original.shape
        
        # Calculate part dimensions
        part_height = H // rows
        part_width = W // columns
        O = 2  # Overlap pixels, matching SplitImageGrid
        parts = [part_1, part_2, part_3, part_4, part_5, part_6, part_7, part_8, part_9]

        # Override with MODIFIED_part if provided
        if MODIFIED_part is not None and MODIFIED_part_index > 0:
            index = MODIFIED_part_index - 1
            if index < 0 or index >= 9:
                raise ValueError(f"Invalid MODIFIED_part_index: {MODIFIED_part_index}")
            parts[index] = MODIFIED_part

        # Handle reference part logic
        if reference_video_part_index > 0:
            ref_index = reference_video_part_index - 1
            if parts[ref_index] is None:
                raise ValueError(f"Reference part {reference_video_part_index} is not provided")
            B_ref = parts[ref_index].shape[0]
            original = self.adjust_frame_count_with_repeat(original, B_ref, B)
            for i in range(9):
                if parts[i] is not None and i != ref_index:
                    parts[i] = self.adjust_frame_count_with_repeat(parts[i], B_ref, B)
                elif i == ref_index:
                    parts[i] = parts[i]
        else:
            B_ref = B

        # Clone original to avoid modifying it
        reassembled = original.clone()

        # Reassemble the parts into the grid
        for i, part in enumerate(parts, start=1):
            if part is not None:
                # Determine part position
                row = (i - 1) // columns
                col = (i - 1) % columns
                # Calculate cropping offsets based on position
                crop_top = O if row > 0 else 0
                crop_left = O if col > 0 else 0
                
                # Get the cropped part
                cropped_part = part[:, crop_top:, crop_left:, :]
                
                # Check if resize is needed and enabled
                if auto_resize and (cropped_part.shape[1] != part_height or cropped_part.shape[2] != part_width):
                    print(f"Resizing part {i} from {cropped_part.shape[1:3]} to ({part_height}, {part_width})")
                    cropped_part = self.resize_tensor(cropped_part, part_height, part_width)
                elif not auto_resize and (cropped_part.shape[1] != part_height or cropped_part.shape[2] != part_width):
                    # If auto-resize is disabled, still throw the error
                    raise ValueError(f"Cropped part {i} has incorrect shape. Expected ({part_height}, {part_width}, {C}), got {cropped_part.shape[1:]}")
                
                # Validate frame count
                if cropped_part.shape[0] != B_ref:
                    raise ValueError(f"Cropped part {i} has incorrect frame count. Expected {B_ref}, got {cropped_part.shape[0]}")
                
                # Place cropped part into reassembled image
                h_start = row * part_height
                h_end = h_start + part_height
                w_start = col * part_width
                w_end = w_start + part_width
                reassembled[:, h_start:h_end, w_start:w_end, :] = cropped_part

        return (reassembled,)
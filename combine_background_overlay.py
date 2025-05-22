import torch
import numpy as np
from PIL import Image

class CombineBackgroundOverlay:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "background": ("IMAGE",),
                "overlay": ("IMAGE",),
                "mask": ("MASK",),
                "horizontal_position": ("FLOAT", {"default": 50, "min": -50, "max": 150, "step": 0.1}),
                "vertical_position": ("FLOAT", {"default": 50, "min": -50, "max": 150, "step": 0.1}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "combine_background_overlay"
    CATEGORY = "Bjornulf"

    def combine_background_overlay(self, background, overlay, mask, horizontal_position, vertical_position):
        results = []

        # Use the first background image for all overlays
        bg = background[0].cpu().numpy()
        bg = np.clip(bg * 255, 0, 255).astype(np.uint8)
        
        # Check if background has alpha channel (4 channels)
        if bg.shape[2] == 4:
            bg_img = Image.fromarray(bg, 'RGBA')
            bg_has_alpha = True
        else:
            bg_img = Image.fromarray(bg, 'RGB')
            bg_has_alpha = False

        # Process each overlay image with the same background
        for i in range(overlay.shape[0]):
            # Get overlay and corresponding mask
            ov = overlay[i].cpu().numpy()
            ov = np.clip(ov * 255, 0, 255).astype(np.uint8)
            
            # Use corresponding mask or repeat last mask if fewer masks
            mask_idx = min(i, mask.shape[0] - 1)
            m = mask[mask_idx].cpu().numpy()
            m = np.clip(m * 255, 0, 255).astype(np.uint8)

            # Ensure overlay has correct shape (height, width, 3)
            if len(ov.shape) == 2:
                ov = np.stack([ov, ov, ov], axis=2)
            elif ov.shape[2] != 3:
                ov = ov[:, :, :3]

            # Create PIL Image for overlay
            ov_img = Image.fromarray(ov, 'RGB')
            
            # Ensure mask has correct shape and create alpha channel
            if len(m.shape) == 2:
                alpha = Image.fromarray(m, 'L')
            else:
                # If mask has multiple channels, use the first one
                alpha = Image.fromarray(m[:, :, 0] if len(m.shape) > 2 else m, 'L')
            
            # Resize alpha to match overlay if needed
            if alpha.size != ov_img.size:
                alpha = alpha.resize(ov_img.size, Image.LANCZOS)
            
            # Combine RGB overlay with alpha mask
            ov_img.putalpha(alpha)

            # Calculate positions
            x = int((horizontal_position / 100) * bg_img.width - (horizontal_position / 100) * ov_img.width)
            y = int((vertical_position / 100) * bg_img.height - (vertical_position / 100) * ov_img.height)

            # Start with a fresh copy of the background for each overlay
            if bg_has_alpha:
                result = bg_img.copy()
            else:
                # Convert to RGBA for compositing
                result = Image.new('RGBA', bg_img.size, (0, 0, 0, 0))
                result.paste(bg_img, (0, 0))

            # Paste the overlay with alpha blending
            if x + ov_img.width > 0 and y + ov_img.height > 0 and x < result.width and y < result.height:
                # Create a temporary image for positioning
                temp = Image.new('RGBA', result.size, (0, 0, 0, 0))
                temp.paste(ov_img, (x, y), ov_img)
                
                # Composite the overlay onto the result
                result = Image.alpha_composite(result.convert('RGBA'), temp)

            # Convert back to numpy array and then to torch tensor
            result_np = np.array(result)
            
            # Determine output format based on background
            if bg_has_alpha:
                # Keep RGBA format if background had alpha
                if result_np.shape[2] == 4:
                    result_tensor = torch.from_numpy(result_np).float() / 255.0
                else:
                    # Add alpha channel if somehow lost
                    alpha_channel = np.ones((result_np.shape[0], result_np.shape[1], 1), dtype=np.uint8) * 255
                    result_np = np.concatenate([result_np, alpha_channel], axis=2)
                    result_tensor = torch.from_numpy(result_np).float() / 255.0
            else:
                # Convert RGBA to RGB if background was RGB
                if result_np.shape[2] == 4:
                    # Alpha blend with white background
                    alpha = result_np[:, :, 3:4] / 255.0
                    rgb = result_np[:, :, :3]
                    white_bg = np.ones_like(rgb) * 255
                    result_np = (rgb * alpha + white_bg * (1 - alpha)).astype(np.uint8)
                
                result_tensor = torch.from_numpy(result_np).float() / 255.0

            results.append(result_tensor)

        # Stack all results into a single tensor
        final_result = torch.stack(results)

        return (final_result,)
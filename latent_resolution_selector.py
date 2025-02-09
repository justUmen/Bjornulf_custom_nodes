import torch
import numpy as np
from nodes import EmptyLatentImage

class LatentResolutionSelector:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "resolution_preset": ([
                    # SD 1.5 Resolutions - Square
                    "SD1.5 - Square - 512x512 (1:1)", 
                    "SD1.5 - Square - 640x640 (1:1)", 
                    "SD1.5 - Square - 768x768 (1:1)",
                    
                    # SD 1.5 Resolutions - Landscape
                    "SD1.5 - Landscape - 640x480 (4:3)", 
                    "SD1.5 - Landscape - 768x512 (3:2)", 
                    "SD1.5 - Landscape - 704x384 (16:9)", 
                    "SD1.5 - Landscape - 768x384 (2:1)",
                    
                    # SD 1.5 Resolutions - Portrait
                    "SD1.5 - Portrait - 480x640 (3:4)", 
                    "SD1.5 - Portrait - 512x768 (2:3)",
                    "SD1.5 - Portrait - 384x704 (9:16)", 
                    "SD1.5 - Portrait - 384x768 (1:2)",
                    
                    # SDXL Resolutions - Square
                    "SDXL - Square - 1024x1024 (1:1)", 
                    "SDXL - Square - 1280x1280 (1:1)",
                    
                    # SDXL Resolutions - Landscape
                    "SDXL - Landscape - 1024x768 (4:3)", 
                    "SDXL - Landscape - 1152x864 (4:3)", 
                    "SDXL - Landscape - 1280x960 (4:3)",
                    "SDXL - Landscape - 1152x768 (3:2)", 
                    "SDXL - Landscape - 1344x896 (3:2)",
                    "SDXL - Landscape - 1344x768 (16:9)", 
                    "SDXL - Landscape - 1344x576 (21:9)",
                    
                    # SDXL Resolutions - Portrait
                    "SDXL - Portrait - 768x1024 (3:4)", 
                    "SDXL - Portrait - 864x1152 (3:4)", 
                    "SDXL - Portrait - 960x1280 (3:4)",
                    "SDXL - Portrait - 768x1152 (2:3)", 
                    "SDXL - Portrait - 896x1344 (2:3)",
                    "SDXL - Portrait - 768x1344 (9:16)",
                    
                    # FLUX High Resolutions - Square
                    "FLUX - Square - 1536x1536 (1:1)", 
                    "FLUX - Square - 1920x1920 (1:1)",
                    
                    # FLUX High Resolutions - Landscape
                    "FLUX - Landscape - 1536x1152 (4:3)", 
                    "FLUX - Landscape - 1920x1440 (4:3)",
                    "FLUX - Landscape - 1536x1024 (3:2)", 
                    "FLUX - Landscape - 1856x1088 (~16:9)", 
                    "FLUX - Landscape - 1920x1280 (3:2)",
                    "FLUX - Landscape - 1920x1080 (16:9)", 
                    "FLUX - Landscape - 1920x816 (21:9)",
                    
                    # FLUX High Resolutions - Portrait
                    "FLUX - Portrait - 1152x1536 (3:4)", 
                    "FLUX - Portrait - 1440x1920 (3:4)",
                    "FLUX - Portrait - 1024x1536 (2:3)", 
                    "FLUX - Portrait - 1088x1856 (~16:9)", 
                    "FLUX - Portrait - 1280x1920 (2:3)",
                    "FLUX - Portrait - 1080x1920 (9:16)", 
                    "FLUX - Portrait - 816x1920 (21:9)"
                ],),
                "batch_size": ("INT", {"default": 1, "min": 1, "max": 64})
            }
        }

    RETURN_TYPES = ("LATENT",)
    FUNCTION = "generate_latent"
    CATEGORY = "Bjornulf"

    def generate_latent(self, resolution_preset, batch_size=1):
        # Extract dimensions from the preset string
        resolution = resolution_preset.split(' - ')[2].split(' ')[0]
        width, height = map(int, resolution.split('x'))
        
        # Create empty latent image with the selected dimensions
        latent = EmptyLatentImage().generate(width, height, batch_size)[0]
        
        return (latent,)
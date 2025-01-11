import os
import comfy.sd
import comfy.utils

class LoaderLoraWithPath:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": ("MODEL",),
                "clip": ("CLIP",),
                "lora_path": ("STRING", {"default": ""}),
                "strength_model": ("FLOAT", {"default": 1.0, "min": -100.0, "max": 100.0, "step": 0.01}),
                "strength_clip": ("FLOAT", {"default": 1.0, "min": -100.0, "max": 100.0, "step": 0.01}),
            }
        }
    
    RETURN_TYPES = ("MODEL", "CLIP")
    FUNCTION = "load_lora"  # Added this line
    CATEGORY = "Bjornulf"

    def load_lora(self, model, clip, lora_path, strength_model, strength_clip):
        try:
            # Check if path exists
            if not os.path.isfile(lora_path):
                print(f"Error: Lora file not found at path: {lora_path}")
                return (model, clip)

            # Load the Lora file
            try:
                lora = comfy.utils.load_torch_file(lora_path)
            except Exception as e:
                print(f"Error loading Lora file: {str(e)}")
                return (model, clip)

            # Apply the Lora
            model_lora, clip_lora = comfy.sd.load_lora_for_models(
                model, 
                clip, 
                lora, 
                strength_model, 
                strength_clip
            )
            
            return (model_lora, clip_lora)
            
        except Exception as e:
            print(f"Error in load_lora: {str(e)}")
            return (model, clip)
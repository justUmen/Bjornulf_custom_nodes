import os
import comfy.sd
import comfy.utils

class LoaderLoraWithPath:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": ("MODEL",),
                "lora_path": ("STRING", {"default": ""}),
                "strength_model": ("FLOAT", {"default": 1.0, "min": -100.0, "max": 100.0, "step": 0.01}),
                "strength_clip": ("FLOAT", {"default": 1.0, "min": -100.0, "max": 100.0, "step": 0.01}),
            },
            "optional": {
                "clip": ("CLIP",),
            }
        }
    
    RETURN_TYPES = ("MODEL", "CLIP", "STRING")
    FUNCTION = "load_lora"
    CATEGORY = "Bjornulf"

    def load_lora(self, model, lora_path, strength_model, strength_clip, clip=None):
        try:
            if not os.path.isfile(lora_path):
                print(f"Error: Lora file not found at path: {lora_path}")
                return (model, clip if clip is not None else None, lora_path if lora_path is not None else None)

            lora = comfy.utils.load_torch_file(lora_path)

            if clip is not None:
                model_lora, clip_lora = comfy.sd.load_lora_for_models(
                    model, clip, lora, strength_model, strength_clip
                )
                return (model_lora, clip_lora, lora_path if lora_path is not None else None)
            else:
                model_lora = model.clone()
                # Assuming ModelPatcher with diffusion_model
                state_dict = model_lora.model.diffusion_model.state_dict()
                for key in lora:
                    if 'unet' in key:  # Filter for UNet keys; adjust as needed
                        if key in state_dict:
                            state_dict[key] += strength_model * lora[key]
                model_lora.model.diffusion_model.load_state_dict(state_dict)
                return (model_lora, None, lora_path if lora_path is not None else None)

        except Exception as e:
            print(f"Error in load_lora: {str(e)}")
            return (model, clip if clip is not None else None)
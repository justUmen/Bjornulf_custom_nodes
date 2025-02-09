import os
import random
from folder_paths import get_filename_list, get_full_path
import comfy.sd
import comfy.utils

class AllLoraSelector:
    @classmethod
    def INPUT_TYPES(cls):
        lora_list = get_filename_list("loras")
        optional_inputs = {}
        
        # Add a default value if lora_list is empty
        if not lora_list:
            lora_list = ["none"]
            
        for i in range(1, 21):
            optional_inputs[f"lora_{i}"] = (lora_list, {"default": lora_list[0]})
            optional_inputs[f"strength_model_{i}"] = ("FLOAT", {"default": 1.0, "min": -100.0, "max": 100.0, "step": 0.01})
            optional_inputs[f"strength_clip_{i}"] = ("FLOAT", {"default": 1.0, "min": -100.0, "max": 100.0, "step": 0.01})

        return {
            "required": {
                "number_of_loras": ("INT", {"default": 3, "min": 1, "max": 20, "step": 1}),
                "model": ("MODEL",),
                "clip": ("CLIP",),
            },
            "optional": optional_inputs
        }

    RETURN_TYPES = ("MODEL", "CLIP", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("model", "clip", "lora_paths", "lora_names", "lora_folders")
    FUNCTION = "apply_all_loras"
    CATEGORY = "Bjornulf"

    def apply_all_loras(self, number_of_loras, model, clip, **kwargs):
        available_loras = []
        strengths_model = []
        strengths_clip = []
        
        # Collect LoRAs and their strengths
        for i in range(1, number_of_loras + 1):
            lora_key = f"lora_{i}"
            strength_model_key = f"strength_model_{i}"
            strength_clip_key = f"strength_clip_{i}"
            
            if lora_key in kwargs and kwargs[lora_key] and kwargs[lora_key] != "none":
                available_loras.append(kwargs[lora_key])
                strengths_model.append(kwargs.get(strength_model_key, 1.0))
                strengths_clip.append(kwargs.get(strength_clip_key, 1.0))
        
        if not available_loras:
            return (model, clip, "", "", "")

        # Initialize lists for collecting metadata
        lora_paths = []
        lora_names = []
        lora_folders = []
        
        # Create a copy of the initial model and clip
        result_model = model.clone()
        result_clip = clip.clone()
        
        # Apply each LoRA sequentially
        for selected_lora, strength_model, strength_clip in zip(available_loras, strengths_model, strengths_clip):
            # Get LoRA metadata
            lora_name = os.path.splitext(os.path.basename(selected_lora))[0]
            lora_path = get_full_path("loras", selected_lora)
            lora_folder = os.path.basename(os.path.dirname(lora_path))
            
            # Load and apply LoRA
            lora = comfy.utils.load_torch_file(lora_path, safe_load=True)
            model_lora, clip_lora = comfy.sd.load_lora_for_models(
                result_model, result_clip, lora, strength_model, strength_clip
            )
            
            # Update results
            result_model = model_lora
            if clip_lora is not None:
                result_clip = clip_lora
            
            # Collect metadata
            lora_paths.append(lora_path)
            lora_names.append(lora_name)
            lora_folders.append(lora_folder)
        
        return (
            result_model, 
            result_clip, 
            ",".join(lora_paths), 
            ",".join(lora_names), 
            ",".join(lora_folders)
        )
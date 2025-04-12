import os
from folder_paths import get_filename_list, get_full_path_or_raise
from comfy_extras.nodes_upscale_model import UpscaleModelLoader


class LoopUpscaleModelSelector:
    @classmethod
    def INPUT_TYPES(cls):
        model_list = get_filename_list("upscale_models")
        # if not model_list:
        # raise ValueError("No checkpoint models found in the upscale_models directory")

        optional_inputs = {}

        # Safely get default model for each input
        for i in range(1, 11):
            # If model_list is empty, use an empty default
            if not model_list:
                optional_inputs[f"model_{i}"] = (model_list, {})
            else:
                # Use modulo to wrap around to the start of the list if we exceed its length
                default_index = (i - 1) % len(model_list)
                optional_inputs[f"model_{i}"] = (
                    model_list,
                    {"default": model_list[default_index]},
                )

        return {
            "required": {
                "number_of_models": (
                    "INT",
                    {"default": 3, "min": 1, "max": 20, "step": 1},
                ),
            },
            "optional": optional_inputs,
        }

    RETURN_TYPES = ("UPSCALE_MODEL", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("model", "model_path", "model_name", "model_folder")
    FUNCTION = "select_upscale_models"
    CATEGORY = "Bjornulf"
    OUTPUT_IS_LIST = (True, True, True, True)

    def select_upscale_models(self, number_of_models, **kwargs):
        # Collect available models from kwargs
        available_models = [
            kwargs[f"model_{i}"]
            for i in range(1, number_of_models + 1)
            if f"model_{i}" in kwargs and kwargs[f"model_{i}"]
        ]

        # Raise an error if no models are available
        if not available_models:
            raise ValueError(
                "No upscale models selected. Please ensure at least one model is selected."
            )

        models = []
        model_paths = []
        model_names = []
        model_folders = []

        model_loader = UpscaleModelLoader()

        for selected_model in available_models:
            # Get the model name (without folders or extensions)
            model_name = os.path.splitext(os.path.basename(selected_model))[0]

            # Get the full path to the selected model
            model_path = get_full_path_or_raise("upscale_models", selected_model)

            # Get the folder name where the model is located
            model_folder = os.path.basename(os.path.dirname(model_path))

            # Load the model using ComfyUI's UpscaleModelLoader class
            model = model_loader.load_model(selected_model)[0]

            models.append(model)
            model_paths.append(model_path)
            model_names.append(model_name)
            model_folders.append(model_folder)

        return (models, model_paths, model_names, model_folders)

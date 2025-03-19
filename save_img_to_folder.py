import os
import folder_paths
from nodes import SaveImage

class SaveImageToFolder(SaveImage):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE", ),
                "folder_name": ("STRING", {"default": "my_folder"}),
            },
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
        }

    FUNCTION = "save_images"
    CATEGORY = "Bjornulf"
    OUTPUT_NODE = True

    def save_images(self, images, folder_name, prompt=None, extra_pnginfo=None):
        # Create the custom folder within the output directory
        custom_folder = os.path.join(folder_paths.get_output_directory(), folder_name)
        os.makedirs(custom_folder, exist_ok=True)
        
        # Call the parent's save_images with filename_prefix set to "folder_name/"
        # This will make the parent class save to the custom folder
        if images is None:
            return (None,)
        else:
            return super().save_images(
                images=images,
                filename_prefix=f"{folder_name}/_",
                prompt=prompt,
                extra_pnginfo=extra_pnginfo
            )
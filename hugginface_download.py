import os
import folder_paths
from huggingface_hub import hf_hub_download

class HuggingFaceDownloader:
    """Custom node for downloading models from Hugging Face within ComfyUI"""
    
    MODELS_DIR = {
        "models/vae": "vae",
        "models/unet": "unet",
        "models/clip": "clip",
        "models/lora": "loras",
        "models/controlnet": "controlnet",
        "models/upscale": "upscale_models",
        "models/embeddings": "embeddings"
    }

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "hf_token": ("STRING", {"multiline": False, "default": ""}),
                "repo_id": ("STRING", {"multiline": False, "default": "Kijai/HunyuanVideo_comfy"}),
                "filename": ("STRING", {"multiline": False, "default": "hunyuan_video_vae_bf16.safetensors"}),
                "model_type": (list(cls.MODELS_DIR.keys()),),
            },
            "optional": {
                "custom_path": ("STRING", {"multiline": False, "default": ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("status",)
    FUNCTION = "download_model"
    CATEGORY = "Bjornulf"

    def download_model(self, hf_token, repo_id, filename, model_type, custom_path=None):
        download_dir = "Unknown"
        try:
            os.environ["HF_TOKEN"] = hf_token
            
            if custom_path:
                download_dir = custom_path
            else:
                folder_key = self.MODELS_DIR[model_type]
                download_dir = folder_paths.get_folder_paths(folder_key)[0]
            
            os.makedirs(download_dir, exist_ok=True)
            
            hf_hub_download(
                repo_id=repo_id,
                filename=filename,
                token=hf_token,
                local_dir=download_dir
            )
            
            return (f"Successfully downloaded {filename} to {download_dir}",)
            
        except IndexError:
            return (f"No directory found for model type: {model_type}. Check folder_paths configuration.",)
        except Exception as e:
            return (f"Error downloading model: {str(e)}, {filename} to {download_dir}",)

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("nan")
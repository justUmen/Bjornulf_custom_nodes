import os
import folder_paths
from huggingface_hub import hf_hub_download
from huggingface_hub.utils import EntryNotFoundError

class HuggingFaceDownloader:
    """Custom node for downloading models from Hugging Face within ComfyUI"""
    
    # Mapping of model types to their directory names
    MODELS_DIR = {
        "models/vae": "vae",
        "models/unet": "unet",
        "models/clip": "clip",
        "models/text_encoders": "text_encoders",
        "models/diffusion_models": "diffusion_models",
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
            # Set the Hugging Face token
            os.environ["HF_TOKEN"] = hf_token
            
            # Determine the download directory
            if custom_path:
                download_dir = custom_path
            else:
                folder_key = self.MODELS_DIR[model_type]
                download_dir = folder_paths.get_folder_paths(folder_key)[0]
            
            # Create the download directory if it doesn’t exist
            os.makedirs(download_dir, exist_ok=True)
            
            # Progress callback to show download progress
            def progress_callback(downloaded, total):
                if total > 0:
                    progress = (downloaded / total) * 100
                    print(f"\rDownloading {filename}: {progress:.2f}%", end="")
                if downloaded == total:
                    print("\nDownload complete.")
            
            # First attempt: try downloading the file directly from the repository
            try:
                hf_hub_download(
                    repo_id=repo_id,
                    filename=filename,
                    subfolder=None,
                    token=hf_token,
                    local_dir=download_dir,
                    callbacks=[progress_callback]
                )
                source = "directly"
            except EntryNotFoundError:
                # Second attempt: try downloading from split_files/<model_type>
                subfolder = f"split_files/{self.MODELS_DIR[model_type]}"
                hf_hub_download(
                    repo_id=repo_id,
                    filename=filename,
                    subfolder=subfolder,
                    token=hf_token,
                    local_dir=download_dir,
                    callbacks=[progress_callback]
                )
                source = f"subfolder {subfolder}"
            
            # Return success message with the source of the file
            return (f"Successfully downloaded {filename} from {repo_id} ({source}) to {download_dir}",)
            
        except IndexError:
            return (f"No directory found for model type: {model_type}. Check folder_paths configuration.",)
        except EntryNotFoundError:
            return (f"Error: {filename} not found in {repo_id} or {repo_id}/split_files/{self.MODELS_DIR[model_type]}",)
        except Exception as e:
            return (f"Error downloading model: {str(e)}, {filename} to {download_dir}",)

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("nan")
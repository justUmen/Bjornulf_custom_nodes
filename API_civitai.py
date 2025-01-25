import os
import time
import requests
from PIL import Image, ImageSequence, ImageOps
import numpy as np
import torch
from io import BytesIO
import json
import threading
import random
import importlib
import folder_paths
import node_helpers
import hashlib
from folder_paths import get_filename_list, get_full_path, models_dir
import nodes
            
# Register the new checkpoint folder
bjornulf_checkpoint_path = os.path.join(folder_paths.models_dir, "checkpoints", "Bjornulf_civitAI")
os.makedirs(bjornulf_checkpoint_path, exist_ok=True)

# Convert tuple to list, append new path, and convert back to tuple
checkpoint_folders = list(folder_paths.folder_names_and_paths["checkpoints"])
checkpoint_folders.append(bjornulf_checkpoint_path)
folder_paths.folder_names_and_paths["checkpoints"] = tuple(checkpoint_folders)

# Prepare Models
custom_nodes_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
civitai_base_path = os.path.join(custom_nodes_dir, "ComfyUI", "custom_nodes", "Bjornulf_custom_nodes", "civitai")
parsed_models_path = civitai_base_path

# Define image folders
image_folders = {
    "sdxl_1.0": os.path.join(civitai_base_path, "sdxl_1.0"),
    "sd_1.5": os.path.join(civitai_base_path, "sd_1.5"),
    "pony": os.path.join(civitai_base_path, "pony"),
    "flux.1_d": os.path.join(civitai_base_path, "flux.1_d"),
    "flux.1_s": os.path.join(civitai_base_path, "flux.1_s"),
    "lora_sdxl_1.0": os.path.join(civitai_base_path, "lora_sdxl_1.0"),
    "lora_sd_1.5": os.path.join(civitai_base_path, "lora_sd_1.5"),
    "lora_pony": os.path.join(civitai_base_path, "lora_pony"),
    "lora_flux.1_d": os.path.join(civitai_base_path, "lora_flux.1_d"),
    "lora_hunyuan_video": os.path.join(civitai_base_path, "lora_hunyuan_video"),
    "NSFW_lora_hunyuan_video": os.path.join(civitai_base_path, "NSFW_lora_hunyuan_video")
}

# Add folder paths for each image folder
for folder_name, folder_path in image_folders.items():
    folder_paths.add_model_folder_path(folder_name, folder_path)
    
    # Create target paths in input directory
    target_path = os.path.join('input', folder_name)
    
    # Create link if it doesn't exist
    if not os.path.exists(target_path):
        try:
            if os.name == 'nt':  # Windows
                os.system(f'mklink /J "{target_path}" "{folder_path}"')
            else:  # Unix-like
                os.symlink(folder_path, target_path)
            print(f"Successfully created link from {folder_path} to {target_path}")
        except OSError as e:
            print(f"Failed to create link: {e}")

# Prepare Loras
# lora_images_path = os.path.join(custom_nodes_dir, "ComfyUI", "custom_nodes", "Bjornulf_custom_nodes", "civitai", "lora_images")
# folder_paths.add_model_folder_path("lora_images", lora_images_path)
# target_lora_path = os.path.join('input', 'lora_images')
# # Create link if it doesn't exist
# if not os.path.exists(target_lora_path):
#     try:
#         if os.name == 'nt':  # Windows
#             os.system(f'mklink /J "{target_lora_path}" "{lora_images_path}"')
#         else:  # Unix-like
#             os.symlink(lora_images_path, target_lora_path)
#         print(f"Successfully created link from {lora_images_path} to {target_lora_path}")
#     except OSError as e:
#         print(f"Failed to create link: {e}")

def get_civitai():
    import civitai
    importlib.reload(civitai)
    return civitai

# Check if the environment variable exists
if "CIVITAI_API_TOKEN" not in os.environ:
    os.environ["CIVITAI_API_TOKEN"] = "d5fc336223a367e6b503a14a10569825"
else:
    print("CIVITAI_API_TOKEN already exists in the environment.")
import civitai

class APIGenerateCivitAI:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_token": ("STRING", {
                    "multiline": False,
                    "default": "",
                    "placeholder": "Enter your CivitAI API token here"
                }),
                "model_urn": ("STRING", {
                    "multiline": False,
                    "default": "urn:air:sdxl:checkpoint:civitai:133005@782002"
                }),
                "prompt": ("STRING", {
                    "multiline": True,
                    "default": "RAW photo, face portrait photo of 26 y.o woman"
                }),
                "negative_prompt": ("STRING", {
                    "multiline": True,
                    "default": "(deformed iris, deformed pupils, semi-realistic, cgi, 3d, render, sketch, cartoon, drawing, anime)"
                }),
                "width": ("INT", {
                    "default": 1024,
                    "min": 128,
                    "max": 1024,
                    "step": 64
                }),
                "height": ("INT", {
                    "default": 768,
                    "min": 128,
                    "max": 1024,
                    "step": 64
                }),
                "steps": ("INT", {
                    "default": 20,
                    "min": 1,
                    "max": 50,
                    "step": 1
                }),
                "cfg_scale": ("FLOAT", {
                    "default": 7.0,
                    "min": 1.0,
                    "max": 30.0,
                    "step": 0.1
                }),
                "seed": ("INT", {
                    "default": -1,
                    "min": -1,
                    "max": 0x7FFFFFFFFFFFFFFF
                }),
                "number_of_images": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 10,
                    "step": 1
                }),
                "timeout": ("INT", {
                    "default": 300,
                    "min": 60,
                    "max": 1800,
                    "step": 60,
                    "display": "Timeout (seconds)"
                }),
            },
            "optional":{
                "add_LORA": ("add_LORA", {"forceInput": True}),
            }
        }

    RETURN_TYPES = ("IMAGE", "STRING",)
    RETURN_NAMES = ("image", "generation_info",)
    FUNCTION = "generate"
    CATEGORY = "Civitai"

    def __init__(self):
        self.output_dir = "output/API/CivitAI"
        self.metadata_dir = "output/API/CivitAI/metadata"
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.metadata_dir, exist_ok=True)
        self._interrupt_event = threading.Event()
        

    def get_next_number(self):
        """Get the next available number for file naming"""
        files = [f for f in os.listdir(self.output_dir) if f.endswith('.png')]
        if not files:
            return 1
        numbers = [int(f.split('.')[0]) for f in files]
        return max(numbers) + 1

    def check_job_status(self, job_token, job_id, timeout=9999):
        """Check job status with timeout"""
        start_time = time.time()
        while time.time() - start_time < timeout and not self._interrupt_event.is_set():
            try:
                response = civitai.jobs.get(token=job_token)
                job_status = response['jobs'][0]
                
                if job_status.get('status') == 'failed':
                    raise Exception(f"Job failed: {job_status.get('error', 'Unknown error')}")
                
                if job_status['result'].get('available'):
                    return job_status['result'].get('blobUrl')
                
                print(f"Job Status: {job_status['status']}")
                time.sleep(2)
                
            except Exception as e:
                print(f"Error checking job status: {str(e)}")
                time.sleep(2)
            
            # Check for interruption
            if self._interrupt_event.is_set():
                raise InterruptedError("Generation interrupted by user")
        
        if self._interrupt_event.is_set():
            raise InterruptedError("Generation interrupted by user")
        raise TimeoutError(f"Job timed out after {timeout} seconds")

    def save_image_and_metadata(self, img, generation_info, number):
        """Save both image and its metadata"""
        # Save image
        filename = f"{number:04d}.png"
        filepath = os.path.join(self.output_dir, filename)
        img.save(filepath)

        # Save metadata
        metadata_filename = f"{number:04d}_metadata.json"
        metadata_filepath = os.path.join(self.metadata_dir, metadata_filename)
        with open(metadata_filepath, 'w') as f:
            json.dump(generation_info, f, indent=4)

        return filepath, metadata_filepath

    def format_generation_info(self, input_data, job_token, job_id, image_url):
        """Format generation information for recovery"""
        recovery_info = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "generation_parameters": input_data,
            "job_details": {
                "token": job_token,
                "job_id": job_id,
                "image_url": image_url
            },
            "recovery_command": f"curl -X GET '{image_url}' --output recovered_image.png",
            "recovery_instructions": """
To recover this image:
1. Use the provided curl command to download the image
2. Or use the image_url directly in a browser
3. If the image is no longer available, you can retry generation with the same parameters
            """
        }
        return recovery_info

    def generate_single_image(self, input_data, job_token, job_id, timeout):
        """Generate a single image and return its tensor and info"""
        try:
            image_url = self.check_job_status(job_token, job_id, timeout)
            if not image_url:
                raise ValueError("No image URL received")

            image_response = requests.get(image_url)
            if image_response.status_code != 200:
                raise ConnectionError(f"Failed to download image: Status code {image_response.status_code}")

            img = Image.open(BytesIO(image_response.content))
            if img.mode != 'RGB':
                img = img.convert('RGB')

            number = self.get_next_number()
            generation_info = self.format_generation_info(input_data, job_token, job_id, image_url)
            image_path, metadata_path = self.save_image_and_metadata(img, generation_info, number)

            img_tensor = torch.from_numpy(np.array(img).astype(np.float32) / 255.0)
            img_tensor = img_tensor.unsqueeze(0)

            return img_tensor, generation_info

        except Exception as e:
            raise Exception(f"Error generating single image: {str(e)}")


    def generate(self, api_token, prompt, negative_prompt, width, height, model_urn, steps=20, 
                cfg_scale=7.0, seed=-1, number_of_images=1, timeout=300, add_LORA=""):

        # Set the environment variable
        if api_token:
            os.environ["CIVITAI_API_TOKEN"] = api_token
            # Get a fresh instance of civitai with the new token
            civitai = get_civitai()

        self._interrupt_event.clear()
        empty_image = torch.zeros((1, height, width, 3))
        
        try:
            # Handle seed
            if seed == -1:
                seed = random.randint(0, 0x7FFFFFFFFFFFFFFF)
            
            # Prepare jobs list
            jobs = []
            generation_tasks = []

            for i in range(number_of_images):
                current_seed = seed + i
                input_data = {
                    "model": model_urn,
                    "params": {
                        "prompt": prompt,
                        "negativePrompt": negative_prompt,
                        "scheduler": "EulerA",
                        "steps": steps,
                        "cfgScale": cfg_scale,
                        "width": width,
                        "height": height,
                        "clipSkip": 2,
                        "seed": current_seed
                    }
                }

                # Handle add_LORA input if provided
                if add_LORA:
                    try:
                        lora_data = json.loads(add_LORA)
                        if "additionalNetworks" in lora_data:
                            input_data["additionalNetworks"] = lora_data["additionalNetworks"]
                    except Exception as e:
                        print(f"Error processing LORA data: {str(e)}")

                # Create generation job
                response = civitai.image.create(input_data)
                if not response or 'token' not in response or 'jobs' not in response:
                    raise ValueError("Invalid response from Civitai API")

                jobs.append({
                    'token': response['token'],
                    'job_id': response['jobs'][0]['jobId'],
                    'input_data': input_data
                })

            # Process all jobs in parallel
            images = []
            infos = []
            failed_jobs = []

            for job in jobs:
                try:
                    img_tensor, generation_info = self.generate_single_image(
                        job['input_data'], 
                        job['token'], 
                        job['job_id'], 
                        timeout
                    )
                    images.append(img_tensor)
                    infos.append(generation_info)
                except Exception as e:
                    failed_jobs.append({
                        'job': job,
                        'error': str(e)
                    })

            if not images:  # If all jobs failed
                generation_info = {
                    "error": "All generation jobs failed",
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "failed_jobs": failed_jobs
                }
                return (empty_image, json.dumps(generation_info, indent=2))

            # Combine images into a batch
            combined_tensor = torch.cat(images, dim=0)
            
            # Combine generation info
            combined_info = {
                "successful_generations": len(images),
                "total_requested": number_of_images,
                "base_seed": seed,
                "generation_parameters": jobs[0]['input_data'],
                "individual_results": infos,
                "failed_jobs": failed_jobs if failed_jobs else None
            }

            return (combined_tensor, json.dumps(combined_info, indent=2))

        except InterruptedError:
            generation_info = {
                "error": "Generation interrupted by user",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "base_seed": seed
            }
            return (empty_image, json.dumps(generation_info, indent=2))
            
        except Exception as e:
            generation_info = {
                "error": f"Civitai generation failed: {str(e)}",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "base_seed": seed if 'seed' in locals() else None
            }
            return (empty_image, json.dumps(generation_info, indent=2))

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")

    def interrupt(self):
        """Method to handle interruption"""
        print("Interrupting CivitAI generation...")
        self._interrupt_event.set()

class APIGenerateCivitAIAddLORA:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "lora_urn": ("STRING", {
                    "multiline": False,
                    "default": "urn:air:flux1:lora:civitai:790034@883473"
                }),
                "strength": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 2.0,
                    "step": 0.01
                }),
            },
            "optional": {
                "add_LORA": ("add_LORA", {"forceInput": True}),
            }
        }

    RETURN_TYPES = ("add_LORA",)
    FUNCTION = "add_lora"
    CATEGORY = "Civitai"

    def add_lora(self, lora_urn, strength, add_LORA=None):
        try:
            request_data = {"additionalNetworks": {}}
            
            # Add the new LORA
            request_data["additionalNetworks"][lora_urn] = {
                "type": "Lora",
                "strength": strength
            }
            
            # If add_LORA is provided, concatenate it
            if add_LORA:
                additional_loras = json.loads(add_LORA)
                if "additionalNetworks" in additional_loras:
                    request_data["additionalNetworks"].update(additional_loras["additionalNetworks"])
            
            return (json.dumps(request_data),)
        except Exception as e:
            print(f"Error adding LORA: {str(e)}")
            return (json.dumps({"additionalNetworks": {}}),)

class CivitAIModelSelectorSD15:
    @classmethod
    def INPUT_TYPES(s):
        # Get list of supported image extensions
        image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp')
        files = [f"sd_1.5/{f}" for f in folder_paths.get_filename_list("sd_1.5") 
                if f.lower().endswith(image_extensions)]
        
        if not files:  # If no files found, provide a default option
            files = ["none"]
            
        return {
            "required": {
                        "image": (sorted(files), {"image_upload": True}),
                        "civitai_token": ("STRING", {"default": ""})
            },
        }

    RETURN_TYPES = ("MODEL", "CLIP", "VAE", "STRING", "STRING")
    RETURN_NAMES = ("model", "clip", "vae", "name", "civitai_url")
    FUNCTION = "load_model"
    CATEGORY = "Bjornulf"
 
    def load_model(self, image, civitai_token):
        def download_file(url, destination_path, model_name, api_token=None):
            """
            Download file with proper authentication headers and simple progress bar.
            """
            filename = f"{model_name}.safetensors"
            file_path = os.path.join(destination_path, filename)

            headers = {}
            if api_token:
                headers['Authorization'] = f'Bearer {api_token}'

            try:
                print(f"Downloading from: {url}")
                response = requests.get(url, headers=headers, stream=True)
                response.raise_for_status()

                # Get file size if available
                file_size = int(response.headers.get('content-length', 0))
                block_size = 8192
                downloaded = 0

                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=block_size):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            
                            # Calculate progress
                            if file_size > 0:
                                progress = int(50 * downloaded / file_size)
                                bars = '=' * progress + '-' * (50 - progress)
                                percent = (downloaded / file_size) * 100
                                print(f'\rProgress: [{bars}] {percent:.1f}%', end='')

                print(f"\nFile downloaded successfully to: {file_path}")
                return file_path

            except requests.exceptions.RequestException as e:
                print(f"Error downloading file: {e}")
                raise
        
        if image == "none":
            raise ValueError("No image selected")

        # Get the absolute path to the JSON file
        json_path = os.path.join(parsed_models_path, 'parsed_sd_1.5_models.json')

        # Load models info
        with open(json_path, 'r') as f:
            models_info = json.load(f)
        
        # Extract model name from image path
        image_name = os.path.basename(image)
        # Find corresponding model info
        model_info = next((model for model in models_info 
                          if os.path.basename(model['image_path']) == image_name), None)
        
        if not model_info:
            raise ValueError(f"No model information found for image: {image_name}")

        # Create checkpoints directory if it doesn't exist
        checkpoint_dir = os.path.join(folder_paths.models_dir, "checkpoints", "Bjornulf_civitAI", "sd1.5")
        os.makedirs(checkpoint_dir, exist_ok=True)

        # Expected model filename
        model_filename = f"{model_info['name']}.safetensors"
        full_model_path = os.path.join(checkpoint_dir, model_filename)

        # Check if model is already downloaded
        if not os.path.exists(full_model_path):
            print(f"Downloading model {model_info['name']}...")
            
            # Construct download URL with token
            download_url = model_info['download_url']
            if civitai_token:
                download_url += f"?token={civitai_token}" if '?' not in download_url else f"&token={civitai_token}"

            try:
                # Download the file using class method
                download_file(download_url, checkpoint_dir, model_info['name'], civitai_token)
            except Exception as e:
                raise ValueError(f"Failed to download model: {e}")

        # Get relative path
        relative_model_path = os.path.join("Bjornulf_civitAI", "sd1.5", model_filename)

        # Try loading with relative path first
        try:
            model = nodes.CheckpointLoaderSimple().load_checkpoint(relative_model_path)
        except Exception as e:
            print(f"Error loading model with relative path: {e}")
            print(f"Attempting to load from full path: {full_model_path}")
            # Fallback to direct loading if needed
            from comfy.sd import load_checkpoint_guess_config
            model = load_checkpoint_guess_config(full_model_path)

        return (model[0], model[1], model[2], model_info['name'], f"https://civitai.com/models/{model_info['model_id']}")

    @classmethod
    def IS_CHANGED(s, image, **kwargs):
        if image == "none":
            return ""
        image_path = os.path.join(civitai_base_path, image)
        if not os.path.exists(image_path):
            return ""
        
        m = hashlib.sha256()
        with open(image_path, 'rb') as f:
            m.update(f.read())
        m.update(image.encode('utf-8'))
        return m.digest().hex()


class CivitAIModelSelectorSDXL:
    @classmethod
    def INPUT_TYPES(s):
        # Get list of supported image extensions
        image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp')
        files = [f"sdxl_1.0/{f}" for f in folder_paths.get_filename_list("sdxl_1.0") 
                if f.lower().endswith(image_extensions)]
        
        if not files:  # If no files found, provide a default option
            files = ["none"]
            
        return {
            "required": {
                        "image": (sorted(files), {"image_upload": True}),
                        "civitai_token": ("STRING", {"default": ""})
            },
        }

    RETURN_TYPES = ("MODEL", "CLIP", "VAE", "STRING", "STRING")
    RETURN_NAMES = ("model", "clip", "vae", "name", "civitai_url")
    FUNCTION = "load_model"
    CATEGORY = "Bjornulf"
 
    def load_model(self, image, civitai_token):
        def download_file(url, destination_path, model_name, api_token=None):
            """
            Download file with proper authentication headers and simple progress bar.
            """
            filename = f"{model_name}.safetensors"
            file_path = os.path.join(destination_path, filename)

            headers = {}
            if api_token:
                headers['Authorization'] = f'Bearer {api_token}'

            try:
                print(f"Downloading from: {url}")
                response = requests.get(url, headers=headers, stream=True)
                response.raise_for_status()

                # Get file size if available
                file_size = int(response.headers.get('content-length', 0))
                block_size = 8192
                downloaded = 0

                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=block_size):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            
                            # Calculate progress
                            if file_size > 0:
                                progress = int(50 * downloaded / file_size)
                                bars = '=' * progress + '-' * (50 - progress)
                                percent = (downloaded / file_size) * 100
                                print(f'\rProgress: [{bars}] {percent:.1f}%', end='')

                print(f"\nFile downloaded successfully to: {file_path}")
                return file_path

            except requests.exceptions.RequestException as e:
                print(f"Error downloading file: {e}")
                raise
        
        if image == "none":
            raise ValueError("No image selected")

        # Get the absolute path to the JSON file
        json_path = os.path.join(parsed_models_path, 'parsed_sdxl_1.0_models.json')

        # Load models info
        with open(json_path, 'r') as f:
            models_info = json.load(f)
        
        # Extract model name from image path
        image_name = os.path.basename(image)
        # Find corresponding model info
        model_info = next((model for model in models_info 
                          if os.path.basename(model['image_path']) == image_name), None)
        
        if not model_info:
            raise ValueError(f"No model information found for image: {image_name}")

        # Create checkpoints directory if it doesn't exist
        checkpoint_dir = os.path.join(folder_paths.models_dir, "checkpoints", "Bjornulf_civitAI", "sdxl_1.0")
        os.makedirs(checkpoint_dir, exist_ok=True)

        # Expected model filename
        model_filename = f"{model_info['name']}.safetensors"
        full_model_path = os.path.join(checkpoint_dir, model_filename)

        # Check if model is already downloaded
        if not os.path.exists(full_model_path):
            print(f"Downloading model {model_info['name']}...")
            
            # Construct download URL with token
            download_url = model_info['download_url']
            if civitai_token:
                download_url += f"?token={civitai_token}" if '?' not in download_url else f"&token={civitai_token}"

            try:
                # Download the file using class method
                download_file(download_url, checkpoint_dir, model_info['name'], civitai_token)
            except Exception as e:
                raise ValueError(f"Failed to download model: {e}")

        # Get relative path
        relative_model_path = os.path.join("Bjornulf_civitAI", "sdxl_1.0", model_filename)

        # Try loading with relative path first
        try:
            model = nodes.CheckpointLoaderSimple().load_checkpoint(relative_model_path)
        except Exception as e:
            print(f"Error loading model with relative path: {e}")
            print(f"Attempting to load from full path: {full_model_path}")
            # Fallback to direct loading if needed
            from comfy.sd import load_checkpoint_guess_config
            model = load_checkpoint_guess_config(full_model_path)

        # return (model[0], model[1], model[2], model_info['name'], model_info['download_url'])
        return (model[0], model[1], model[2], model_info['name'], f"https://civitai.com/models/{model_info['model_id']}")

    @classmethod
    def IS_CHANGED(s, image, **kwargs):
        if image == "none":
            return ""
        image_path = os.path.join(civitai_base_path, image)
        if not os.path.exists(image_path):
            return ""
        
        m = hashlib.sha256()
        with open(image_path, 'rb') as f:
            m.update(f.read())
        m.update(image.encode('utf-8'))
        return m.digest().hex()

class CivitAIModelSelectorFLUX_D:
    @classmethod
    def INPUT_TYPES(s):
        # Get list of supported image extensions
        image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp')
        files = [f"flux.1_d/{f}" for f in folder_paths.get_filename_list("flux.1_d") 
                if f.lower().endswith(image_extensions)]
        
        if not files:  # If no files found, provide a default option
            files = ["none"]
            
        return {
            "required": {
                        "image": (sorted(files), {"image_upload": True}),
                        "civitai_token": ("STRING", {"default": ""})
            },
        }

    RETURN_TYPES = ("MODEL", "CLIP", "VAE", "STRING", "STRING")
    RETURN_NAMES = ("model", "clip", "vae", "name", "civitai_url")
    FUNCTION = "load_model"
    CATEGORY = "Bjornulf"
 
    def load_model(self, image, civitai_token):
        def download_file(url, destination_path, model_name, api_token=None):
            """
            Download file with proper authentication headers and simple progress bar.
            """
            filename = f"{model_name}.safetensors"
            file_path = os.path.join(destination_path, filename)

            headers = {}
            if api_token:
                headers['Authorization'] = f'Bearer {api_token}'

            try:
                print(f"Downloading from: {url}")
                response = requests.get(url, headers=headers, stream=True)
                response.raise_for_status()

                # Get file size if available
                file_size = int(response.headers.get('content-length', 0))
                block_size = 8192
                downloaded = 0

                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=block_size):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            
                            # Calculate progress
                            if file_size > 0:
                                progress = int(50 * downloaded / file_size)
                                bars = '=' * progress + '-' * (50 - progress)
                                percent = (downloaded / file_size) * 100
                                print(f'\rProgress: [{bars}] {percent:.1f}%', end='')

                print(f"\nFile downloaded successfully to: {file_path}")
                return file_path

            except requests.exceptions.RequestException as e:
                print(f"Error downloading file: {e}")
                raise
        
        if image == "none":
            raise ValueError("No image selected")

        # Get the absolute path to the JSON file
        json_path = os.path.join(parsed_models_path, 'parsed_flux.1_d_models.json')

        # Load models info
        with open(json_path, 'r') as f:
            models_info = json.load(f)
        
        # Extract model name from image path
        image_name = os.path.basename(image)
        # Find corresponding model info
        model_info = next((model for model in models_info 
                          if os.path.basename(model['image_path']) == image_name), None)
        
        if not model_info:
            raise ValueError(f"No model information found for image: {image_name}")

        # Create checkpoints directory if it doesn't exist
        checkpoint_dir = os.path.join(folder_paths.models_dir, "checkpoints", "Bjornulf_civitAI", "flux_d")
        os.makedirs(checkpoint_dir, exist_ok=True)

        # Expected model filename
        model_filename = f"{model_info['name']}.safetensors"
        full_model_path = os.path.join(checkpoint_dir, model_filename)

        # Check if model is already downloaded
        if not os.path.exists(full_model_path):
            print(f"Downloading model {model_info['name']}...")
            
            # Construct download URL with token
            download_url = model_info['download_url']
            if civitai_token:
                download_url += f"?token={civitai_token}" if '?' not in download_url else f"&token={civitai_token}"

            try:
                # Download the file using class method
                download_file(download_url, checkpoint_dir, model_info['name'], civitai_token)
            except Exception as e:
                raise ValueError(f"Failed to download model: {e}")

        # Get relative path
        relative_model_path = os.path.join("Bjornulf_civitAI", "flux_d", model_filename)

        # Try loading with relative path first
        try:
            model = nodes.CheckpointLoaderSimple().load_checkpoint(relative_model_path)
        except Exception as e:
            print(f"Error loading model with relative path: {e}")
            print(f"Attempting to load from full path: {full_model_path}")
            # Fallback to direct loading if needed
            from comfy.sd import load_checkpoint_guess_config
            model = load_checkpoint_guess_config(full_model_path)

        return (model[0], model[1], model[2], model_info['name'], f"https://civitai.com/models/{model_info['model_id']}")

    @classmethod
    def IS_CHANGED(s, image, **kwargs):
        if image == "none":
            return ""
        image_path = os.path.join(civitai_base_path, image)
        if not os.path.exists(image_path):
            return ""
        
        m = hashlib.sha256()
        with open(image_path, 'rb') as f:
            m.update(f.read())
        m.update(image.encode('utf-8'))
        return m.digest().hex()


class CivitAIModelSelectorFLUX_S:
    @classmethod
    def INPUT_TYPES(s):
        # Get list of supported image extensions
        image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp')
        files = [f"flux.1_s/{f}" for f in folder_paths.get_filename_list("flux.1_s") 
                if f.lower().endswith(image_extensions)]
        
        if not files:  # If no files found, provide a default option
            files = ["none"]
            
        return {
            "required": {
                        "image": (sorted(files), {"image_upload": True}),
                        "civitai_token": ("STRING", {"default": ""})
            },
        }

    RETURN_TYPES = ("MODEL", "CLIP", "VAE", "STRING", "STRING")
    RETURN_NAMES = ("model", "clip", "vae", "name", "civitai_url")
    FUNCTION = "load_model"
    CATEGORY = "Bjornulf"
 
    def load_model(self, image, civitai_token):
        def download_file(url, destination_path, model_name, api_token=None):
            """
            Download file with proper authentication headers and simple progress bar.
            """
            filename = f"{model_name}.safetensors"
            file_path = os.path.join(destination_path, filename)

            headers = {}
            if api_token:
                headers['Authorization'] = f'Bearer {api_token}'

            try:
                print(f"Downloading from: {url}")
                response = requests.get(url, headers=headers, stream=True)
                response.raise_for_status()

                # Get file size if available
                file_size = int(response.headers.get('content-length', 0))
                block_size = 8192
                downloaded = 0

                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=block_size):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            
                            # Calculate progress
                            if file_size > 0:
                                progress = int(50 * downloaded / file_size)
                                bars = '=' * progress + '-' * (50 - progress)
                                percent = (downloaded / file_size) * 100
                                print(f'\rProgress: [{bars}] {percent:.1f}%', end='')

                print(f"\nFile downloaded successfully to: {file_path}")
                return file_path

            except requests.exceptions.RequestException as e:
                print(f"Error downloading file: {e}")
                raise
        
        if image == "none":
            raise ValueError("No image selected")

        # Get the absolute path to the JSON file
        json_path = os.path.join(parsed_models_path, 'parsed_flux.1_s_models.json')

        # Load models info
        with open(json_path, 'r') as f:
            models_info = json.load(f)
        
        # Extract model name from image path
        image_name = os.path.basename(image)
        # Find corresponding model info
        model_info = next((model for model in models_info 
                          if os.path.basename(model['image_path']) == image_name), None)
        
        if not model_info:
            raise ValueError(f"No model information found for image: {image_name}")

        # Create checkpoints directory if it doesn't exist
        checkpoint_dir = os.path.join(folder_paths.models_dir, "checkpoints", "Bjornulf_civitAI", "flux_s")
        os.makedirs(checkpoint_dir, exist_ok=True)

        # Expected model filename
        model_filename = f"{model_info['name']}.safetensors"
        full_model_path = os.path.join(checkpoint_dir, model_filename)

        # Check if model is already downloaded
        if not os.path.exists(full_model_path):
            print(f"Downloading model {model_info['name']}...")
            
            # Construct download URL with token
            download_url = model_info['download_url']
            if civitai_token:
                download_url += f"?token={civitai_token}" if '?' not in download_url else f"&token={civitai_token}"

            try:
                # Download the file using class method
                download_file(download_url, checkpoint_dir, model_info['name'], civitai_token)
            except Exception as e:
                raise ValueError(f"Failed to download model: {e}")

        # Get relative path
        relative_model_path = os.path.join("Bjornulf_civitAI", "flux_s", model_filename)

        # Try loading with relative path first
        try:
            model = nodes.CheckpointLoaderSimple().load_checkpoint(relative_model_path)
        except Exception as e:
            print(f"Error loading model with relative path: {e}")
            print(f"Attempting to load from full path: {full_model_path}")
            # Fallback to direct loading if needed
            from comfy.sd import load_checkpoint_guess_config
            model = load_checkpoint_guess_config(full_model_path)

        return (model[0], model[1], model[2], model_info['name'], f"https://civitai.com/models/{model_info['model_id']}")

    @classmethod
    def IS_CHANGED(s, image):
        if image == "none":
            return ""
        image_path = os.path.join(civitai_base_path, image)
        if not os.path.exists(image_path):
            return ""
        
        m = hashlib.sha256()
        with open(image_path, 'rb') as f:
            m.update(f.read())
        m.update(image.encode('utf-8'))
        return m.digest().hex()


class CivitAIModelSelectorPony:
    @classmethod
    def INPUT_TYPES(s):
        # Get list of supported image extensions
        image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp')
        files = [f"pony/{f}" for f in folder_paths.get_filename_list("pony") 
                if f.lower().endswith(image_extensions)]
        
        if not files:  # If no files found, provide a default option
            files = ["none"]
            
        return {
            "required": {
                        "image": (sorted(files), {"image_upload": True}),
                        "civitai_token": ("STRING", {"default": ""})
            },
        }

    RETURN_TYPES = ("MODEL", "CLIP", "VAE", "STRING", "STRING")
    RETURN_NAMES = ("model", "clip", "vae", "name", "civitai_url")
    FUNCTION = "load_model"
    CATEGORY = "Bjornulf"
 
    def load_model(self, image, civitai_token):
        def download_file(url, destination_path, model_name, api_token=None):
            """
            Download file with proper authentication headers and simple progress bar.
            """
            filename = f"{model_name}.safetensors"
            file_path = os.path.join(destination_path, filename)

            headers = {}
            if api_token:
                headers['Authorization'] = f'Bearer {api_token}'

            try:
                print(f"Downloading from: {url}")
                response = requests.get(url, headers=headers, stream=True)
                response.raise_for_status()

                # Get file size if available
                file_size = int(response.headers.get('content-length', 0))
                block_size = 8192
                downloaded = 0

                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=block_size):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            
                            # Calculate progress
                            if file_size > 0:
                                progress = int(50 * downloaded / file_size)
                                bars = '=' * progress + '-' * (50 - progress)
                                percent = (downloaded / file_size) * 100
                                print(f'\rProgress: [{bars}] {percent:.1f}%', end='')

                print(f"\nFile downloaded successfully to: {file_path}")
                return file_path

            except requests.exceptions.RequestException as e:
                print(f"Error downloading file: {e}")
                raise
        
        if image == "none":
            raise ValueError("No image selected")

        # Get the absolute path to the JSON file
        json_path = os.path.join(parsed_models_path, 'parsed_pony_models.json')

        # Load models info
        with open(json_path, 'r') as f:
            models_info = json.load(f)
        
        # Extract model name from image path
        image_name = os.path.basename(image)
        # Find corresponding model info
        model_info = next((model for model in models_info 
                          if os.path.basename(model['image_path']) == image_name), None)
        
        if not model_info:
            raise ValueError(f"No model information found for image: {image_name}")

        # Create checkpoints directory if it doesn't exist
        checkpoint_dir = os.path.join(folder_paths.models_dir, "checkpoints", "Bjornulf_civitAI", "pony")
        os.makedirs(checkpoint_dir, exist_ok=True)

        # Expected model filename
        model_filename = f"{model_info['name']}.safetensors"
        full_model_path = os.path.join(checkpoint_dir, model_filename)

        # Check if model is already downloaded
        if not os.path.exists(full_model_path):
            print(f"Downloading model {model_info['name']}...")
            
            # Construct download URL with token
            download_url = model_info['download_url']
            if civitai_token:
                download_url += f"?token={civitai_token}" if '?' not in download_url else f"&token={civitai_token}"

            try:
                # Download the file using class method
                download_file(download_url, checkpoint_dir, model_info['name'], civitai_token)
            except Exception as e:
                raise ValueError(f"Failed to download model: {e}")

        # Get relative path
        relative_model_path = os.path.join("Bjornulf_civitAI", "pony", model_filename)

        # Try loading with relative path first
        try:
            model = nodes.CheckpointLoaderSimple().load_checkpoint(relative_model_path)
        except Exception as e:
            print(f"Error loading model with relative path: {e}")
            print(f"Attempting to load from full path: {full_model_path}")
            # Fallback to direct loading if needed
            from comfy.sd import load_checkpoint_guess_config
            model = load_checkpoint_guess_config(full_model_path)

        return (model[0], model[1], model[2], model_info['name'], f"https://civitai.com/models/{model_info['model_id']}")

    @classmethod
    def IS_CHANGED(s, image, **kwargs):
        if image == "none":
            return ""
        image_path = os.path.join(civitai_base_path, image)
        if not os.path.exists(image_path):
            return ""
        
        m = hashlib.sha256()
        with open(image_path, 'rb') as f:
            m.update(f.read())
        m.update(image.encode('utf-8'))
        return m.digest().hex()


# class CivitAILoraSelector:
#     @classmethod
#     def INPUT_TYPES(s):
#         # Get list of supported image extensions
#         image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp')
#         files = [f"lora_images/{f}" for f in folder_paths.get_filename_list("lora_images") 
#                 if f.lower().endswith(image_extensions)]
        
#         if not files:  # If no files found, provide a default option
#             files = ["none"]
            
#         return {"required":
#                     {"image": (sorted(files), {"image_upload": True})},  # Added image_upload option here
#                 }


#     RETURN_TYPES = ("IMAGE", "STRING")
#     RETURN_NAMES = ("image", "image_name")
#     FUNCTION = "load_image"
#     CATEGORY = "Bjornulf"

#     def load_image(self, image):
#         if image == "none":
#             # Return a small blank image if no image is selected
#             blank_image = torch.zeros((1, 64, 64, 3), dtype=torch.float32)
#             return (blank_image, "none")
            
#         image_path = os.path.join(lora_images_path, image)
        
#         if not os.path.exists(image_path):
#             raise FileNotFoundError(f"Image not found: {image_path}")
        
#         # Copy the image to ComfyUI/input directory
#         input_dir = folder_paths.get_input_directory()
#         dest_path = os.path.join(input_dir, os.path.basename(image))
#         try:
#             shutil.copy2(image_path, dest_path)
#         except Exception as e:
#             print(f"Warning: Failed to copy image to input directory: {e}")
            
#         img = node_helpers.pillow(Image.open, image_path)
        
#         output_images = []
#         w, h = None, None

#         excluded_formats = ['MPO']
        
#         for i in ImageSequence.Iterator(img):
#             i = node_helpers.pillow(ImageOps.exif_transpose, i)

#             if i.mode == 'I':
#                 i = i.point(lambda i: i * (1 / 255))
#             image = i.convert("RGBA")

#             if len(output_images) == 0:
#                 w = image.size[0]
#                 h = image.size[1]
            
#             if image.size[0] != w or image.size[1] != h:
#                 continue
            
#             image = np.array(image).astype(np.float32) / 255.0
#             image = torch.from_numpy(image)[None,]
#             output_images.append(image)

#         if len(output_images) > 1 and img.format not in excluded_formats:
#             output_image = torch.cat(output_images, dim=0)
#         else:
#             output_image = output_images[0]

#         return (output_image, image)
    
#     @classmethod
#     def IS_CHANGED(s, image):
#         if image == "none":
#             return ""
#         # Use the full path for the image
#         image_path = os.path.join(lora_images_path, image)
#         if not os.path.exists(image_path):
#             return ""
        
#         # Calculate hash of the image content
#         m = hashlib.sha256()
#         with open(image_path, 'rb') as f:
#             m.update(f.read())
#         # Include the image name in the hash to ensure updates when selection changes
#         m.update(image.encode('utf-8'))
#         return m.digest().hex()

#     @classmethod
#     def VALIDATE_INPUTS(s, image):
#         if image == "none":
#             return True
#         image_path = os.path.join(lora_images_path, image)
#         if not os.path.exists(image_path):
#             return f"Invalid image file: {image}"
#         return True

class CivitAILoraSelectorSD15:
    @classmethod
    def INPUT_TYPES(s):
        # Get list of supported image extensions
        image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp')
        files = [f"lora_sd_1.5/{f}" for f in folder_paths.get_filename_list("lora_sd_1.5") 
                if f.lower().endswith(image_extensions)]
        
        if not files:  # If no files found, provide a default option
            files = ["none"]
            
        return {
            "required": {
                        "image": (sorted(files), {"image_upload": True}),
                        "model": ("MODEL",),
                        "clip": ("CLIP",),
                        "strength_model": ("FLOAT", {"default": 1.0, "min": -20.0, "max": 20.0, "step": 0.01}),
                        "strength_clip": ("FLOAT", {"default": 1.0, "min": -20.0, "max": 20.0, "step": 0.01}),
                        "civitai_token": ("STRING", {"default": ""})
            },
        }
    
    RETURN_TYPES = ("MODEL", "CLIP", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("model", "clip", "name", "civitai_url", "trigger_words")
    FUNCTION = "load_lora"
    CATEGORY = "Bjornulf"
 
    def load_lora(self, image, model, clip, strength_model, strength_clip, civitai_token):
        def download_file(url, destination_path, lora_name, api_token=None):
            """
            Download file with proper authentication headers and simple progress bar.
            """
            filename = f"{lora_name}.safetensors"
            file_path = os.path.join(destination_path, filename)

            headers = {}
            if api_token:
                headers['Authorization'] = f'Bearer {api_token}'

            try:
                print(f"Downloading from: {url}")
                response = requests.get(url, headers=headers, stream=True)
                response.raise_for_status()

                file_size = int(response.headers.get('content-length', 0))
                block_size = 8192
                downloaded = 0

                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=block_size):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            
                            if file_size > 0:
                                progress = int(50 * downloaded / file_size)
                                bars = '=' * progress + '-' * (50 - progress)
                                percent = (downloaded / file_size) * 100
                                print(f'\rProgress: [{bars}] {percent:.1f}%', end='')

                print(f"\nFile downloaded successfully to: {file_path}")
                return file_path

            except requests.exceptions.RequestException as e:
                print(f"Error downloading file: {e}")
                raise
        
        if image == "none":
            raise ValueError("No image selected")

        # Get the absolute path to the JSON file
        json_path = os.path.join(parsed_models_path, 'parsed_lora_sd_1.5_loras.json')

        # Load loras info
        with open(json_path, 'r') as f:
            loras_info = json.load(f)
        
        # Extract lora name from image path
        image_name = os.path.basename(image)
        # Find corresponding lora info
        lora_info = next((lora for lora in loras_info 
                         if os.path.basename(lora['image_path']) == image_name), None)
        
        if not lora_info:
            raise ValueError(f"No LoRA information found for image: {image_name}")

        # Create loras directory if it doesn't exist
        lora_dir = os.path.join(folder_paths.models_dir, "loras", "Bjornulf_civitAI", "sd_1.5")
        os.makedirs(lora_dir, exist_ok=True)

        # Expected lora filename
        lora_filename = f"{lora_info['name']}.safetensors"
        full_lora_path = os.path.join(lora_dir, lora_filename)

        # Check if lora is already downloaded
        if not os.path.exists(full_lora_path):
            print(f"Downloading LoRA {lora_info['name']}...")
            
            # Construct download URL with token
            download_url = lora_info['download_url']
            if civitai_token:
                download_url += f"?token={civitai_token}" if '?' not in download_url else f"&token={civitai_token}"

            try:
                # Download the file
                download_file(download_url, lora_dir, lora_info['name'], civitai_token)
            except Exception as e:
                raise ValueError(f"Failed to download LoRA: {e}")

        # Get relative path
        relative_lora_path = os.path.join("Bjornulf_civitAI", "sd_1.5", lora_filename)

        # Load the LoRA
        try:
            lora_loader = nodes.LoraLoader()
            model_lora, clip_lora = lora_loader.load_lora(model=model, 
                                                        clip=clip,
                                                        lora_name=relative_lora_path,
                                                        strength_model=strength_model,
                                                        strength_clip=strength_clip)
        except Exception as e:
            raise ValueError(f"Failed to load LoRA: {e}")

        # Convert trained words list to comma-separated string
        trained_words_str = ", ".join(lora_info.get('trained_words', []))
        
        return (model_lora, clip_lora, lora_info['name'], f"https://civitai.com/models/{lora_info['lora_id']}", trained_words_str)

    @classmethod
    def IS_CHANGED(s, image, **kwargs):
        if image == "none":
            return ""
        image_path = os.path.join(civitai_base_path, image)
        if not os.path.exists(image_path):
            return ""
        
        m = hashlib.sha256()
        with open(image_path, 'rb') as f:
            m.update(f.read())
        m.update(image.encode('utf-8'))
        return m.digest().hex()


class CivitAILoraSelectorSDXL:
    @classmethod
    def INPUT_TYPES(s):
        # Get list of supported image extensions
        image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp')
        files = [f"lora_sdxl_1.0/{f}" for f in folder_paths.get_filename_list("lora_sdxl_1.0") 
                if f.lower().endswith(image_extensions)]
        
        if not files:  # If no files found, provide a default option
            files = ["none"]
            
        return {
            "required": {
                        "image": (sorted(files), {"image_upload": True}),
                        "model": ("MODEL",),
                        "clip": ("CLIP",),
                        "strength_model": ("FLOAT", {"default": 1.0, "min": -20.0, "max": 20.0, "step": 0.01}),
                        "strength_clip": ("FLOAT", {"default": 1.0, "min": -20.0, "max": 20.0, "step": 0.01}),
                        "civitai_token": ("STRING", {"default": ""})
            },
        }
    
    RETURN_TYPES = ("MODEL", "CLIP", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("model", "clip", "name", "civitai_url", "trigger_words")
    FUNCTION = "load_lora"
    CATEGORY = "Bjornulf"
 
    def load_lora(self, image, model, clip, strength_model, strength_clip, civitai_token):
        def download_file(url, destination_path, lora_name, api_token=None):
            """
            Download file with proper authentication headers and simple progress bar.
            """
            filename = f"{lora_name}.safetensors"
            file_path = os.path.join(destination_path, filename)

            headers = {}
            if api_token:
                headers['Authorization'] = f'Bearer {api_token}'

            try:
                print(f"Downloading from: {url}")
                response = requests.get(url, headers=headers, stream=True)
                response.raise_for_status()

                file_size = int(response.headers.get('content-length', 0))
                block_size = 8192
                downloaded = 0

                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=block_size):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            
                            if file_size > 0:
                                progress = int(50 * downloaded / file_size)
                                bars = '=' * progress + '-' * (50 - progress)
                                percent = (downloaded / file_size) * 100
                                print(f'\rProgress: [{bars}] {percent:.1f}%', end='')

                print(f"\nFile downloaded successfully to: {file_path}")
                return file_path

            except requests.exceptions.RequestException as e:
                print(f"Error downloading file: {e}")
                raise
        
        if image == "none":
            raise ValueError("No image selected")

        # Get the absolute path to the JSON file
        json_path = os.path.join(parsed_models_path, 'parsed_lora_sdxl_1.0_loras.json')

        # Load loras info
        with open(json_path, 'r') as f:
            loras_info = json.load(f)
        
        # Extract lora name from image path
        image_name = os.path.basename(image)
        # Find corresponding lora info
        lora_info = next((lora for lora in loras_info 
                         if os.path.basename(lora['image_path']) == image_name), None)
        
        if not lora_info:
            raise ValueError(f"No LoRA information found for image: {image_name}")

        # Create loras directory if it doesn't exist
        lora_dir = os.path.join(folder_paths.models_dir, "loras", "Bjornulf_civitAI", "sdxl_1.0")
        os.makedirs(lora_dir, exist_ok=True)

        # Expected lora filename
        lora_filename = f"{lora_info['name']}.safetensors"
        full_lora_path = os.path.join(lora_dir, lora_filename)

        # Check if lora is already downloaded
        if not os.path.exists(full_lora_path):
            print(f"Downloading LoRA {lora_info['name']}...")
            
            # Construct download URL with token
            download_url = lora_info['download_url']
            if civitai_token:
                download_url += f"?token={civitai_token}" if '?' not in download_url else f"&token={civitai_token}"

            try:
                # Download the file
                download_file(download_url, lora_dir, lora_info['name'], civitai_token)
            except Exception as e:
                raise ValueError(f"Failed to download LoRA: {e}")

        # Get relative path
        relative_lora_path = os.path.join("Bjornulf_civitAI", "sdxl_1.0", lora_filename)

        # Load the LoRA
        try:
            lora_loader = nodes.LoraLoader()
            model_lora, clip_lora = lora_loader.load_lora(model=model, 
                                                        clip=clip,
                                                        lora_name=relative_lora_path,
                                                        strength_model=strength_model,
                                                        strength_clip=strength_clip)
        except Exception as e:
            raise ValueError(f"Failed to load LoRA: {e}")

        # Convert trained words list to comma-separated string
        trained_words_str = ", ".join(lora_info.get('trained_words', []))
        
        return (model_lora, clip_lora, lora_info['name'], f"https://civitai.com/models/{lora_info['lora_id']}", trained_words_str)

    @classmethod
    def IS_CHANGED(s, image, **kwargs):
        if image == "none":
            return ""
        image_path = os.path.join(civitai_base_path, image)
        if not os.path.exists(image_path):
            return ""
        
        m = hashlib.sha256()
        with open(image_path, 'rb') as f:
            m.update(f.read())
        m.update(image.encode('utf-8'))
        return m.digest().hex()


class CivitAILoraSelectorPONY:
    @classmethod
    def INPUT_TYPES(s):
        # Get list of supported image extensions
        image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp')
        files = [f"lora_pony/{f}" for f in folder_paths.get_filename_list("lora_pony") 
                if f.lower().endswith(image_extensions)]
        
        if not files:  # If no files found, provide a default option
            files = ["none"]
            
        return {
            "required": {
                        "image": (sorted(files), {"image_upload": True}),
                        "model": ("MODEL",),
                        "clip": ("CLIP",),
                        "strength_model": ("FLOAT", {"default": 1.0, "min": -20.0, "max": 20.0, "step": 0.01}),
                        "strength_clip": ("FLOAT", {"default": 1.0, "min": -20.0, "max": 20.0, "step": 0.01}),
                        "civitai_token": ("STRING", {"default": ""})
            },
        }
    
    RETURN_TYPES = ("MODEL", "CLIP", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("model", "clip", "name", "civitai_url", "trigger_words")
    FUNCTION = "load_lora"
    CATEGORY = "Bjornulf"
 
    def load_lora(self, image, model, clip, strength_model, strength_clip, civitai_token):
        def download_file(url, destination_path, lora_name, api_token=None):
            """
            Download file with proper authentication headers and simple progress bar.
            """
            filename = f"{lora_name}.safetensors"
            file_path = os.path.join(destination_path, filename)

            headers = {}
            if api_token:
                headers['Authorization'] = f'Bearer {api_token}'

            try:
                print(f"Downloading from: {url}")
                response = requests.get(url, headers=headers, stream=True)
                response.raise_for_status()

                file_size = int(response.headers.get('content-length', 0))
                block_size = 8192
                downloaded = 0

                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=block_size):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            
                            if file_size > 0:
                                progress = int(50 * downloaded / file_size)
                                bars = '=' * progress + '-' * (50 - progress)
                                percent = (downloaded / file_size) * 100
                                print(f'\rProgress: [{bars}] {percent:.1f}%', end='')

                print(f"\nFile downloaded successfully to: {file_path}")
                return file_path

            except requests.exceptions.RequestException as e:
                print(f"Error downloading file: {e}")
                raise
        
        if image == "none":
            raise ValueError("No image selected")

        # Get the absolute path to the JSON file
        json_path = os.path.join(parsed_models_path, 'parsed_lora_pony_loras.json')

        # Load loras info
        with open(json_path, 'r') as f:
            loras_info = json.load(f)
        
        # Extract lora name from image path
        image_name = os.path.basename(image)
        # Find corresponding lora info
        lora_info = next((lora for lora in loras_info 
                         if os.path.basename(lora['image_path']) == image_name), None)
        
        if not lora_info:
            raise ValueError(f"No LoRA information found for image: {image_name}")

        # Create loras directory if it doesn't exist
        lora_dir = os.path.join(folder_paths.models_dir, "loras", "Bjornulf_civitAI", "pony")
        os.makedirs(lora_dir, exist_ok=True)

        # Expected lora filename
        lora_filename = f"{lora_info['name']}.safetensors"
        full_lora_path = os.path.join(lora_dir, lora_filename)

        # Check if lora is already downloaded
        if not os.path.exists(full_lora_path):
            print(f"Downloading LoRA {lora_info['name']}...")
            
            # Construct download URL with token
            download_url = lora_info['download_url']
            if civitai_token:
                download_url += f"?token={civitai_token}" if '?' not in download_url else f"&token={civitai_token}"

            try:
                # Download the file
                download_file(download_url, lora_dir, lora_info['name'], civitai_token)
            except Exception as e:
                raise ValueError(f"Failed to download LoRA: {e}")

        # Get relative path
        relative_lora_path = os.path.join("Bjornulf_civitAI", "pony", lora_filename)

        # Load the LoRA
        try:
            lora_loader = nodes.LoraLoader()
            model_lora, clip_lora = lora_loader.load_lora(model=model, 
                                                        clip=clip,
                                                        lora_name=relative_lora_path,
                                                        strength_model=strength_model,
                                                        strength_clip=strength_clip)
        except Exception as e:
            raise ValueError(f"Failed to load LoRA: {e}")

        # Convert trained words list to comma-separated string
        trained_words_str = ", ".join(lora_info.get('trained_words', []))
        
        return (model_lora, clip_lora, lora_info['name'], f"https://civitai.com/models/{lora_info['lora_id']}", trained_words_str)

    @classmethod
    def IS_CHANGED(s, image, **kwargs):
        if image == "none":
            return ""
        image_path = os.path.join(civitai_base_path, image)
        if not os.path.exists(image_path):
            return ""
        
        m = hashlib.sha256()
        with open(image_path, 'rb') as f:
            m.update(f.read())
        m.update(image.encode('utf-8'))
        return m.digest().hex()



class CivitAILoraSelectorHunyuan:
    @classmethod
    def INPUT_TYPES(s):
        image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp')
    
        # Try NSFW folder first
        nsfw_files = [f"NSFW_lora_hunyuan_video/{f}" for f in folder_paths.get_filename_list("NSFW_lora_hunyuan_video") 
                if f.lower().endswith(image_extensions)]
        
        # If NSFW folder is empty or doesn't exist, try regular folder
        if not nsfw_files:
            files = [f"lora_hunyuan_video/{f}" for f in folder_paths.get_filename_list("lora_hunyuan_video") 
                    if f.lower().endswith(image_extensions)]
        else:
            files = nsfw_files
        
        if not files:
            files = ["none"]
            
            
        return {
            "required": {
                        "image": (sorted(files), {"image_upload": True}),
                        "model": ("MODEL",),
                        "clip": ("CLIP",),
                        "strength_model": ("FLOAT", {"default": 1.0, "min": -20.0, "max": 20.0, "step": 0.01}),
                        "strength_clip": ("FLOAT", {"default": 1.0, "min": -20.0, "max": 20.0, "step": 0.01}),
                        "civitai_token": ("STRING", {"default": ""})
            },
        }
    
    RETURN_TYPES = ("MODEL", "CLIP", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("model", "clip", "name", "civitai_url", "trigger_words")
    FUNCTION = "load_lora"
    CATEGORY = "Bjornulf"
 
    def load_lora(self, image, model, clip, strength_model, strength_clip, civitai_token):
        def download_file(url, destination_path, lora_name, api_token=None):
            filename = f"{lora_name}.safetensors"
            file_path = os.path.join(destination_path, filename)

            headers = {}
            if api_token:
                headers['Authorization'] = f'Bearer {api_token}'

            try:
                print(f"Downloading from: {url}")
                response = requests.get(url, headers=headers, stream=True)
                response.raise_for_status()

                file_size = int(response.headers.get('content-length', 0))
                block_size = 8192
                downloaded = 0

                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=block_size):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            
                            if file_size > 0:
                                progress = int(50 * downloaded / file_size)
                                bars = '=' * progress + '-' * (50 - progress)
                                percent = (downloaded / file_size) * 100
                                print(f'\rProgress: [{bars}] {percent:.1f}%', end='')

                print(f"\nFile downloaded successfully to: {file_path}")
                return file_path

            except requests.exceptions.RequestException as e:
                print(f"Error downloading file: {e}")
                raise
        
        if image == "none":
            raise ValueError("No image selected")

        # Try loading NSFW JSON first, fall back to regular JSON if not found
        nsfw_json_path = os.path.join(parsed_models_path, 'NSFW_parsed_lora_hunyuan_video_loras.json')
        regular_json_path = os.path.join(parsed_models_path, 'parsed_lora_hunyuan_video_loras.json')
        
        json_path = nsfw_json_path if os.path.exists(nsfw_json_path) else regular_json_path
        hunYuan = "hunyuan_video"

        with open(json_path, 'r') as f:
            loras_info = json.load(f)
        
        image_name = os.path.basename(image)
        lora_info = next((lora for lora in loras_info 
                         if os.path.basename(lora['image_path']) == image_name), None)
        
        if not lora_info:
            raise ValueError(f"No LoRA information found for image: {image_name}")

        lora_dir = os.path.join(folder_paths.models_dir, "loras", "Bjornulf_civitAI", hunYuan)
        os.makedirs(lora_dir, exist_ok=True)

        lora_filename = f"{lora_info['name']}.safetensors"
        full_lora_path = os.path.join(lora_dir, lora_filename)

        if not os.path.exists(full_lora_path):
            print(f"Downloading LoRA {lora_info['name']}...")
            
            download_url = lora_info['download_url']
            if civitai_token:
                download_url += f"?token={civitai_token}" if '?' not in download_url else f"&token={civitai_token}"

            try:
                download_file(download_url, lora_dir, lora_info['name'], civitai_token)
            except Exception as e:
                raise ValueError(f"Failed to download LoRA: {e}")

        relative_lora_path = os.path.join("Bjornulf_civitAI", hunYuan, lora_filename)

        try:
            lora_loader = nodes.LoraLoader()
            model_lora, clip_lora = lora_loader.load_lora(model=model, 
                                                        clip=clip,
                                                        lora_name=relative_lora_path,
                                                        strength_model=strength_model,
                                                        strength_clip=strength_clip)
        except Exception as e:
            raise ValueError(f"Failed to load LoRA: {e}")

        trained_words_str = ", ".join(lora_info.get('trained_words', []))
        
        return (model_lora, clip_lora, lora_info['name'], f"https://civitai.com/models/{lora_info['lora_id']}", trained_words_str)

    @classmethod
    def IS_CHANGED(s, image, **kwargs):
        if image == "none":
            return ""
        image_path = os.path.join(civitai_base_path, image)
        if not os.path.exists(image_path):
            return ""
        
        m = hashlib.sha256()
        with open(image_path, 'rb') as f:
            m.update(f.read())
        m.update(image.encode('utf-8'))
        return m.digest().hex()
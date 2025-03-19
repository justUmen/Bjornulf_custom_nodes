import base64
import numpy as np
from PIL import Image
from io import BytesIO

class OllamaImageVision:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "IMAGE": ("IMAGE",),
                "OLLAMA_VISION_PROMPT": ("STRING", {"forceInput": True}),
                "vram_retention_minutes": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 99
                }),
                "seed": ("INT", {
                    "default": -1,
                    "min": -1,
                    "max": 2147483647
                }),
                "answer_single_line": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "OLLAMA_CONFIG": ("OLLAMA_CONFIG", {"forceInput": True}),
                "context": ("STRING", {"multiline": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("response",)
    FUNCTION = "process_image"
    CATEGORY = "Bjornulf"

    def process_image(self, IMAGE, OLLAMA_VISION_PROMPT, answer_single_line, vram_retention_minutes, seed, OLLAMA_CONFIG=None, context=None):
        from ollama import Client
        
        # Default OLLAMA_CONFIG if not provided
        if OLLAMA_CONFIG is None:
            OLLAMA_CONFIG = {
                "model": "moondream",
                "url": "http://0.0.0.0:11434"
            }
        selected_model = OLLAMA_CONFIG["model"]
        ollama_url = OLLAMA_CONFIG["url"]

        # Convert images to base64
        images_base64 = []
        for img in IMAGE:
            numpy_img = (255. * img.cpu().numpy()).clip(0, 255).astype(np.uint8)
            pil_image = Image.fromarray(numpy_img)
            buffered = BytesIO()
            pil_image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
            images_base64.append(img_str)
            buffered.close()

        # Initialize client
        client = Client(host=ollama_url)

        # Construct the final prompt
        if context:
            final_prompt = context + "\n" + OLLAMA_VISION_PROMPT
        else:
            final_prompt = OLLAMA_VISION_PROMPT
        
        # Generate response with the final prompt
        response = client.generate(
            model=selected_model,
            prompt=final_prompt,
            images=images_base64,
            keep_alive=f"{vram_retention_minutes}m"
        )
        
        if answer_single_line:
            response['response'] = ' '.join(response['response'].split())
        
        return (response['response'].strip(),)

class OllamaVisionPromptSelector: #Prompts made for gemma3
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt_type": (["NONE", "basic", "advanced", "characters", "objects", "semantic", "basic_action", "advanced_action", "context", "SDXL", "FLUX", "video"],),
            },
            "optional": {
                "prefix_custom_prompt": ("STRING", {"multiline": True, "default": ""}),
                "suffix_custom_prompt": ("STRING", {"multiline": True, "default": "Do not include any introductory text or explanations, make it a clean one line answer."}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("OLLAMA_VISION_PROMPT",)
    FUNCTION = "select_prompt"
    CATEGORY = "Bjornulf"

    def get_prompts(self):
        """Returns a dictionary of predefined prompts for each prompt_type."""
        return {
            "basic": "Summarize the main content of the image in one concise sentence.",
            "advanced": "Describe the scene thoroughly, capturing intricate details, colors, textures, and significant actions.",
            "characters": "Describe each character's physical appearance, including clothing, expressions, and notable features.",
            "objects": "Identify and describe the primary objects, detailing their size, position, color, and characteristics.",
            "semantic": "Analyze the image's mood, environment, and implied meaning, focusing on symbolic elements and atmosphere.",
            "context": "Describe relationships and interactions between objects and characters, focusing on spatial arrangement and actions.",
            "basic_action": "Describe the action that is happening in the image.",
            "advanced_action": "Describe the action that is happening in the image in details.",
            "SDXL": "Generate a concise, comma-separated list of visual elements from the image, suitable for Stable Diffusion XL. Focus on objects, colors, textures, and composition. Use adjectives for key features. Output only the final prompt. Example: vibrant sunset, tropical beach, silhouetted palm trees, calm ocean, orange sky.",
            "FLUX": "Generate a detailed, structured description of the image for FLUX, including scene type, primary subject, environment details, lighting, colors, perspective, textures, atmosphere, and unique elements. Use concise descriptive phrases. Output only the final prompt. Example: A serene, moonlit forest clearing with a glowing, ethereal portal, surrounded by ancient, towering trees, casting long shadows in the silver light.",
            "video": "Analyze the image to identify the characters. Then, imagine and describe in a single sentence a random dynamic actions they might perform next, involving movement or interaction, based on their appearance and the scene's context. Example : The woman is smirking seductively while staring at the camera, then suddenly winks. Do not add new characters that are not in the image."
        }

    def select_prompt(self, prompt_type, prefix_custom_prompt="", suffix_custom_prompt=""):
        if prompt_type == "NONE":
            selected_prompt = prefix_custom_prompt + suffix_custom_prompt
        else:
            prompts = self.get_prompts()
            selected_prompt = prefix_custom_prompt + prompts.get(prompt_type, "") + suffix_custom_prompt
        return (selected_prompt,)  # Return as a tuple for ComfyUI compatibility

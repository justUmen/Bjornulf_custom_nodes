import torch
import base64
from PIL import Image
import numpy as np
from io import BytesIO
import requests
import json
import ollama
from ollama import Client
# import logging
import hashlib
from typing import Dict, Any
from PIL.PngImagePlugin import PngInfo

class OllamaImageVision:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "IMAGE": ("IMAGE",),
                "output_selection": ("INT", {"default": 7, "min": 1, "max": 8, 
                    "step": 1, "display": "slider", "label": "Number of outputs (1-8)"}),
                "process_below_output_selection": ("BOOLEAN", {"default": False, "label": "Process all up to selection"})
            },
            "optional": {
                "OLLAMA_CONFIG": ("OLLAMA_CONFIG", {"forceInput": True}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING",)
    RETURN_NAMES = ("1 - Basic Description", "2 - Advanced Description", "3 - Characters Description", "4 - Object Recognition", "5 - Semantic Understanding", "6 - Contextual Analysis", "7 - SDXL Prompt (words)", "8 - FLUX Prompt (sentences)")
    FUNCTION = "process_image_base64"
    CATEGORY = "Bjornulf"

    def __init__(self):
        self.client = None

    def create_prompts(self):
        # return {
        #     "basic": "Describe the image in one sentence.",
        #     "advanced": "Describe the image in details.",
        #     "characters": "Describe the physical appearance of the character in vivid detail.",
        #     "objects": "List the key objects and elements visible in the image.",
        #     "semantic": "Provide an in-depth interpretation including mood, environment, and purpose in the image.",
        #     "context": "Describe the relationships and context between objects and people in the image."
        # }
        return {
            # Do not describe what isn't there.
            "basic": "Summarize the main content of the image in one concise sentence.",
            "advanced": "Describe the scene thoroughly, capturing intricate details, colors, textures, and any significant actions or events occurring in the image.",
            "characters": "Describe each character's physical appearance in vivid, descriptive terms, including clothing, expressions, body language, and notable features.",
            "objects": "Identify and describe the primary objects in the image, detailing their size, position, color, and any unique characteristics.",
            "semantic": "Analyze the image's mood, environment, and implied meaning. Discuss any symbolic elements, artistic style, and possible intent or story conveyed.",
            "context": "Describe the relationships and interactions between objects and characters, focusing on spatial arrangement, implied actions, and any contextual clues suggesting connections or purpose.",
            "SDXL": "Describe the image. The goal is to generate a concise, detailed, and effective description. Guidelines for describing the image:- Focus on visual elements, be specific about objects, colors, textures, and compositions. Use adjectives to describe key features. Avoid complete sentences or narrative descriptions. Prioritize important elements over minor details. Your input will be a detailed description of an image. Process this description and refine it into a prompt suitable for stable diffusion models using the following steps: 1. Identify the most important visual elements and characteristics. 2. Condense the description into a series of comma-separated phrases or words. 3. Prioritize specific, descriptive terms over general ones. Here are two examples of good outputs: Example 1:vibrant sunset, tropical beach, silhouetted palm trees, calm ocean, orange and purple sky, wispy clouds, golden sand, gentle waves, beachgoers in distance, serene atmosphere, warm lighting, panoramic view. Example 2: steampunk cityscape, towering clockwork structures, brass and copper tones, billowing steam, airships in sky, cobblestone streets, Victorian-era citizens, gears and pipes visible, warm sepia lighting, hazy atmosphere, intricate mechanical details. Your final output should be a single line of text containing the refined prompt, without any additional explanation or commentary. IMPORTANT : DO NOT Include information about the overall style or artistic technique.",
            "FLUX": "Describe the given image in a detailed and structured format that is specifically designed for image generation. Use descriptive language to capture the essence of the image, including the environment, objects, characters, lighting, textures, and any other notable elements. The description must use some of these 9 points : 1. Scene Type: [Outdoor/Indoor/Abstract/Fantasy/Realistic/etc.] 2. Primary Subject: [Main focus or characters in the scene.] 3. Environment Details: [Describe the setting in vivid detail, including any landscapes, architecture, or surroundings.] 4. Lighting: [Specify the type, color, and intensity of the lighting.] 5. Colors and Tones: [Dominant colors and overall mood.] 6. Perspective: [Camera angle or viewpoint—close-up, wide shot, aerial, etc.] 7. Texture and Details: [Surface materials, patterns, and fine details.] 8. Emotion or Atmosphere: [Mood conveyed by the scene—serene, ominous, lively, etc.] 9. Unique Elements: [Special features or focal points that make the image distinctive.] For example: 1. Scene Type: Outdoor, natural landscape. 2. Primary Subject: A majestic lion standing atop a rocky hill. 3. Environment Details: A vast savannah with tall golden grass, sparse acacia trees, and distant mountains under a clear blue sky. 4. Lighting: Bright, warm sunlight casting long shadows. 5. Colors and Tones: Predominantly gold and blue, with subtle earthy browns and greens. 6. Perspective: Mid-range shot, slightly low angle to emphasize the lion's dominance. 7. Texture and Details: The lion's fur appears detailed with visible strands, and the rocks have a rough, weathered texture. 8. Emotion or Atmosphere: Majestic, powerful, and serene. 9. Unique Elements: A subtle wind effect in the grass and mane, adding movement to the scene. IMPORTANT : DO NOT Include information about the overall style or artistic technique."
        }


    def process_image_base64(self, IMAGE, OLLAMA_CONFIG=None, output_selection=6, process_below_output_selection=True):
        if OLLAMA_CONFIG is None:
            OLLAMA_CONFIG = {
                "model": "moondream",
                "url": "http://0.0.0.0:11434"
            }
        selected_model = OLLAMA_CONFIG["model"]
        ollama_url = OLLAMA_CONFIG["url"]
        
        images_base64 = []
        for img in IMAGE:
            # Convert tensor to numpy array
            numpy_img = (255. * img.cpu().numpy()).clip(0, 255).astype(np.uint8)
            
            # Create PIL Image
            pil_image = Image.fromarray(numpy_img)
            
            # Create a BytesIO object
            buffered = BytesIO()
            
            # Save the image into the BytesIO object
            pil_image.save(buffered, format="PNG")
            
            # Get the byte value and encode to base64
            img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
            images_base64.append(img_str)

            # Clean up
            buffered.close()

        # Initialize client
        client = Client(host=ollama_url)
        
        # Get prompts
        prompts = list(self.create_prompts().items())
        
        # Process outputs based on selection and process_below_output_selection flag
        responses = []
        for i in range(8):  # Always prepare 5 slots for output
            if process_below_output_selection:
                # Process all outputs up to output_selection
                if i < output_selection:
                    prompt_type, prompt = prompts[i]
                    response = client.generate(
                        model=selected_model,
                        prompt=prompt,
                        images=images_base64
                    )
                    responses.append(response['response'].strip())
                else:
                    responses.append("")
            else:
                # Process only the selected output (output_selection - 1)
                if i == (output_selection - 1):
                    prompt_type, prompt = prompts[i]
                    response = client.generate(
                        model=selected_model,
                        prompt=prompt,
                        images=images_base64
                    )
                    responses.append(response['response'].strip())
                else:
                    responses.append("")

        return tuple(responses)

    def handle_error(self, error_message: str) -> tuple:
        """Handle errors by returning appropriate error messages for all outputs"""
        error_response = f"Error: {error_message}"
        return tuple([error_response] * 4)
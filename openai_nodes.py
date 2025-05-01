import os
import base64
import io
import json
import numpy as np
import torch
from PIL import Image
from openai import OpenAI

class OpenAIVisionNode:
    """
    ComfyUI node for OpenAI's Vision API processing
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "prompt": ("STRING", {"multiline": True, "default": "Output one line, exactly 7 lowercase fields, separated by semicolons, no spaces:\nsex;race;age;hair_length;body;eye_wear;head_wear\n\nField values:\nsex: male/female\nrace: pale/caucasian/hispanic/black/asian\nage: adult/child\nhair_length: none/long\nbody: average/skinny/fat/obese/muscular\neye_wear: none/glasses\nhead_wear: none/hat/cap\nExamples:\nfemale;black;unknown;long;fat;none;none\nmale;hispanic;unknown;none;muscular;glasses;cap\nmale;asian;unknown;none;kid;none;hat"}),
                "model": (["GPT-4.1 ($2.00/$8.00 per 1M tokens)", 
                          "GPT-4.1 mini ($0.40/$1.60 per 1M tokens)", 
                          "GPT-4.1 nano ($0.10/$0.40 per 1M tokens)"],),
                "api_key": ("STRING", {"default": "", "multiline": False})
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("analysis",)
    FUNCTION = "analyze_image"
    CATEGORY = "Bjornulf"

    def analyze_image(self, image, prompt, model, api_key=""):
        """Process the image with OpenAI's Vision API"""
        # Get API key from environment if not provided
        if not api_key:
            api_key = os.environ.get('OPENAI_API_KEY')
            if not api_key:
                return ("No OpenAI API key provided. Please enter your API key or set the OPENAI_API_KEY environment variable.",)
        
        # Map selected model to actual model identifier
        model_mapping = {
            "GPT-4.1 ($2.00/$8.00 per 1M tokens)": "gpt-4.1",
            "GPT-4.1 mini ($0.40/$1.60 per 1M tokens)": "gpt-4.1-mini",
            "GPT-4.1 nano ($0.10/$0.40 per 1M tokens)": "gpt-4.1-nano"
        }
        
        model_id = model_mapping[model]
        
        try:
            # ComfyUI images are in BCHW format with float values [0,1]
            # Extract the first image if we have a batch
            if len(image.shape) == 4:
                image_tensor = image[0]  # Get the first image from the batch
            else:
                image_tensor = image
            
            # Convert from BCHW/CHW to HWC format for PIL
            if image_tensor.shape[0] in [1, 3, 4]:  # If first dimension is channels
                image_tensor = image_tensor.permute(1, 2, 0)
            
            # Convert to numpy and scale to 0-255 range
            np_image = image_tensor.cpu().numpy()
            if np_image.max() <= 1.0:
                np_image = (np_image * 255).astype(np.uint8)
            
            # Handle different channel configurations
            if np_image.shape[2] == 1:  # Grayscale
                np_image = np.repeat(np_image, 3, axis=2)
            elif np_image.shape[2] == 4:  # RGBA
                np_image = np_image[:, :, :3]  # Remove alpha channel
            
            # Create PIL image from numpy array
            pil_image = Image.fromarray(np_image)
            
            # Encode the PIL image to base64
            image_bytes = io.BytesIO()
            pil_image.save(image_bytes, format='PNG')
            image_bytes.seek(0)
            base64_image = base64.b64encode(image_bytes.getvalue()).decode('utf-8')
            
            # Create OpenAI client
            client = OpenAI(api_key=api_key)
            
            # Create completion with the Vision API
            response = client.responses.create(
                model=model_id,
                input=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "input_text",
                                "text": prompt,
                            },
                            {
                                "type": "input_image",
                                "image_url": f"data:image/png;base64,{base64_image}",
                            },
                        ],
                    }
                ]
            )
            
            analysis = response.output_text.strip()
            return (analysis,)
        
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            return (f"Error processing image: {str(e)}\n\nDetails: {error_details}",)
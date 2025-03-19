import torch
import gc
import requests
import json
class Everything(str):
    def __ne__(self, __value: object) -> bool:
        return False
class FreeVRAM:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"anything": (Everything("*"),)}}
    
    RETURN_TYPES = (Everything("*"),)
    RETURN_NAME = ("anything",)
    FUNCTION = "free_vram"
    CATEGORY = "Bjornulf"

    def free_vram(self, anything):
        print("Attempting to free VRAM...")
        
        # Clear CUDA cache
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            print("CUDA cache cleared.")
        
        # Run garbage collection
        collected = gc.collect()
        print(f"Garbage collector: collected {collected} objects.")
        
        # Trigger the HTTP request
        self.trigger_http_request()
        
        # Return the input image unchanged
        return (anything,)
    
    def trigger_http_request(self):
        url = "http://localhost:8188/prompt"
        headers = {"Content-Type": "application/json"}
        payload = {
            "prompt": {
                "3": {
                    "inputs": {"text": "free VRAM hack"},
                    "class_type": "Bjornulf_WriteText",
                    "_meta": {"title": "✒ Write Text"}
                },
                "4": {
                    "inputs": {"text_value": ["3", 0], "text": "free VRAM hack"},
                    "class_type": "Bjornulf_ShowText",
                    "_meta": {"title": "👁 Show (Text)"}
                }
            }
        }
        
        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            print("HTTP request triggered successfully")
        except requests.exceptions.RequestException as e:
            print(f"Failed to trigger HTTP request: {e}")
            
class PurgeCLIPNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {}}

    RETURN_TYPES = ()
    FUNCTION = "purge_clip"
    CATEGORY = "utils"

    def purge_clip(self):
        # Check if the CLIP model is accessible in the global scope
        global clip_model
        if 'clip_model' in globals():
            del clip_model  # Delete the CLIP model reference
            torch.cuda.empty_cache()  # Clear VRAM cache
        return ()
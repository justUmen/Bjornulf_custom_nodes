class WriteTextPickMeGlobal:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "global_pickme_id": ("STRING", {"default": "default"}),  # Custom text global_pickme_id
                "picked": ("BOOLEAN", {"default": False}),         # Picked state
                "text": ("STRING", {"multiline": True, "lines": 10})  # Text input
            },
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "write_text"
    OUTPUT_NODE = True
    CATEGORY = "Bjornulf"
    
    def write_text(self, global_pickme_id, picked, text, **kwargs):
        return (text,)  # Simply returns the input text

import random

class LoadTextPickMeGlobal:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "global_pickme_id": ("STRING", {"default": "default"})
            },
            "hidden": {"prompt": "PROMPT"}  # For accessing the graph state
        }
    
    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("picked_text", "picked_text_as_variable", "random")
    FUNCTION = "load_text"
    CATEGORY = "Bjornulf"
    
    def load_text(self, global_pickme_id, prompt=None):
        texts = []
        picked_text = ""
        if prompt:
            for node_id, node_data in prompt.items():
                if node_data.get("class_type") == "Bjornulf_WriteTextPickMeGlobal":
                    inputs = node_data.get("inputs", {})
                    node_global_pickme_id = inputs.get("global_pickme_id", "default")
                    if node_global_pickme_id == global_pickme_id:
                        text = inputs.get("text", "")
                        texts.append(text)
                        if inputs.get("picked", False):
                            picked_text = text
                            # Note: We don’t break here to collect all texts
        # Select random text
        random_text = random.choice(texts) if texts else ""
        # Return all three outputs
        return (picked_text, f"global_pickme_{global_pickme_id} = {picked_text}", random_text)
    
    @classmethod
    def IS_CHANGED(cls, global_pickme_id, input_text="", prompt=None):
        return float("NaN")
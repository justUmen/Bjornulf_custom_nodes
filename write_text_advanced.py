import re
import random
import time
# import logging

class WriteTextAdvanced:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "lines": 10}),
            },
            "optional": {
                "variables": ("STRING", {"multiline": True, "forceInput": True}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "write_text_special"
    OUTPUT_NODE = True
    CATEGORY = "Bjornulf"
    
    def write_text_special(self, text, variables="", seed=None):
        # logging.info(f"Raw text: {text}")
        # logging.info(f"Variables: {variables}")

        if len(text) > 10000:
            return ("Text too large to process at once. Please split into smaller parts.",)
        
        if seed is None or seed == 0:
            seed = int(time.time() * 1000)
        
        random.seed(seed)
        
        # Parse variables
        var_dict = {}
        for line in variables.split('\n'):
            if '=' in line:
                key, value = line.split('=', 1)
                var_dict[key.strip()] = value.strip()
        
        # logging.info(f"Parsed variables: {var_dict}")

        # Replace variables
        for key, value in var_dict.items():
            text = text.replace(f"<{key}>", value)

        # Handle random choices
        pattern = r'\{([^}]+)\}'
        
        def replace_random(match):
            return random.choice(match.group(1).split('|'))

        result = re.sub(pattern, replace_random, text)
        # logging.info(f"Final text: {result}")
        
        return (result,)

    @classmethod
    def IS_CHANGED(s, text, variables="", seed=None):
        return (text, variables, seed)
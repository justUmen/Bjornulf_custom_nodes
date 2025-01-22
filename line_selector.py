class LineSelector:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"multiline": True}),  # Input for multiple lines
                "line_number": ("INT", {"default": 0, "min": 0, "max": 99999}),  # 0 for random, >0 for specific line
            },
            "optional": {
                "variables": ("STRING", {"multiline": True, "forceInput": True}),
                "seed": ("INT", {
                    "default": -1,
                    "min": -1,
                    "max": 0x7FFFFFFFFFFFFFFF
                }),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "select_line"
    CATEGORY = "Bjornulf"

    def select_line(self, text, line_number, variables="", seed=-1):
        # Parse variables
        var_dict = {}
        for line in variables.split('\n'):
            if '=' in line:
                key, value = line.split('=', 1)
                var_dict[key.strip()] = value.strip()
        
        # Replace variables in the text
        for key, value in var_dict.items():
            text = text.replace(f"<{key}>", value)
        
        # Split the input text into lines, remove empty lines and lines starting with #
        lines = [line.strip() for line in text.split('\n') 
                if line.strip() and not line.strip().startswith('#')]
        
        if not lines:
            return ("No valid lines found.",)
        
        import random
        
        # Set seed if provided
        if seed >= 0:
            random.seed(seed)
            
        # If line_number is 0, select random line
        if line_number == 0:
            selected = random.choice(lines)
        else:
            # If line_number is greater than 0, select specific line (with bounds checking)
            index = min(line_number - 1, len(lines) - 1)  # -1 because user input starts at 1
            index = max(0, index)  # Ensure we don't go below 0
            selected = lines[index]
        
        return (selected,)

    @classmethod
    def IS_CHANGED(s, text, line_number, variables="", seed=-1):
        return (text, line_number, variables, seed)
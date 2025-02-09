import re

class TextReplace:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_text": ("STRING", {"multiline": True, "forceInput": True}),
                "search_text": ("STRING", {"multiline": True}),
                "replace_text": ("STRING", {"multiline": True, "default": ""}),
                "replace_count": ("INT", {"default": 0, "min": 0, "max": 1000, 
                                          "display": "number", 
                                          "tooltip": "Number of replacements (0 = replace all)"}),
                "use_regex": ("BOOLEAN", {"default": False}),
                "case_sensitive": ("BOOLEAN", {"default": True, 
                                             "tooltip": "Whether the search should be case-sensitive"}),
                "trim_whitespace": (["none", "left", "right", "both"], {
                    "default": "none", 
                    "tooltip": "Remove whitespace around the found text"
                }),
                "multiline_regex": ("BOOLEAN", {"default": False, 
                                              "tooltip": "Make dot (.) match newlines in regex"})
            }
        }
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "replace_text"
    CATEGORY = "Bjornulf"
    
    def replace_text(self, input_text, search_text, replace_text, replace_count, 
                    use_regex, multiline_regex, case_sensitive, trim_whitespace):
        try:
            # Convert input to string
            input_text = str(input_text)
            
            # Prepare regex flags
            regex_flags = 0
            if not case_sensitive:
                regex_flags |= re.IGNORECASE
            if multiline_regex and use_regex:
                regex_flags |= re.DOTALL
            
            if use_regex:
                try:
                    # Compile the regex pattern first
                    pattern = re.compile(search_text, flags=regex_flags)
                    
                    # Perform replacement
                    if replace_count == 0:
                        # Replace all instances
                        result = pattern.sub(replace_text, input_text)
                    else:
                        # Replace specific number of instances
                        result = pattern.sub(replace_text, input_text, count=replace_count)
                    
                    return (result,)
                
                except re.error as regex_compile_error:
                    return (input_text,)
            
            else:
                # Standard string replacement
                if not case_sensitive:
                    # Case-insensitive string replacement
                    result = input_text
                    count = 0
                    while search_text.lower() in result.lower() and (replace_count == 0 or count < replace_count):
                        # Find the index of the match
                        idx = result.lower().index(search_text.lower())
                        
                        # Determine left and right parts
                        left_part = result[:idx]
                        right_part = result[idx + len(search_text):]
                        
                        # Trim whitespace based on option
                        if trim_whitespace == "left":
                            left_part = left_part.rstrip()
                        elif trim_whitespace == "right":
                            right_part = right_part.lstrip()
                        elif trim_whitespace == "both":
                            left_part = left_part.rstrip()
                            right_part = right_part.lstrip()
                        
                        # Reconstruct the string
                        result = left_part + replace_text + right_part
                        count += 1
                else:
                    # Case-sensitive replacement
                    result = input_text
                    count = 0
                    while search_text in result and (replace_count == 0 or count < replace_count):
                        # Find the index of the match
                        idx = result.index(search_text)
                        
                        # Determine left and right parts
                        left_part = result[:idx]
                        right_part = result[idx + len(search_text):]
                        
                        # Trim whitespace based on option
                        if trim_whitespace == "left":
                            left_part = left_part.rstrip()
                        elif trim_whitespace == "right":
                            right_part = right_part.lstrip()
                        elif trim_whitespace == "both":
                            left_part = left_part.rstrip()
                            right_part = right_part.lstrip()
                        
                        # Reconstruct the string
                        result = left_part + replace_text + right_part
                        count += 1
            
            return (result,)
            
        except Exception as e:
            return (input_text,)

    @classmethod
    def IS_CHANGED(cls, *args):
        # Return float("NaN") to ensure the node always processes
        return float("NaN")
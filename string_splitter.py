class TextSplitin5:
    DELIMITER_NEWLINE = "\\n"  # Literal string "\n" for display
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_string": ("STRING", {
                    "multiline": True,
                    "forceInput": True
                }),
                "delimiter": ("STRING", {
                    "default": s.DELIMITER_NEWLINE,  # Show "\n" in widget
                    "multiline": False
                }),
                "ignore_before_equals": ("BOOLEAN", {
                    "default": False
                }),
            },
        }
    
    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("part1", "part2", "part3", "part4", "part5")
    FUNCTION = "split_string"
    CATEGORY = "Bjornulf"
    
    def split_string(self, input_string, delimiter, ignore_before_equals):
        # Handle the special case for newline delimiter
        actual_delimiter = "\n" if delimiter == self.DELIMITER_NEWLINE else delimiter
        
        # Split the string using the delimiter
        parts = input_string.split(actual_delimiter)
        
        # Ensure we always return exactly 5 parts
        result = []
        for i in range(5):
            if i < len(parts):
                part = parts[i].strip()
                # If ignore_before_equals is True and there's an equals sign
                if ignore_before_equals and '=' in part:
                    # Take only what's after the equals sign and strip whitespace
                    part = part.split('=', 1)[1].strip()
                result.append(part)
            else:
                # If no more parts, append empty string
                result.append("")
        
        # Convert to tuple and return all 5 parts
        return tuple(result)
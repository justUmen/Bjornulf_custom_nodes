import os

class SaveText:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "forceInput": True}),
                "filepath": ("STRING", {"default": "Bjornulf/Text/example.txt"}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("added_text", "complete_text", "filename", "full_path")
    FUNCTION = "save_text"
    OUTPUT_NODE = True
    CATEGORY = "Bjornulf"
    
    def save_text(self, text, filepath):
        # Validate file extension
        if not filepath.lower().endswith('.txt'):
            raise ValueError("Output file must be a .txt file")
            
        try:
            # Create directory if it doesn't exist
            directory = os.path.dirname(filepath)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
            
            # Get absolute path
            full_path = os.path.abspath(filepath)
            
            # Append text to file with a newline
            with open(filepath, 'a', encoding='utf-8') as file:
                file.write(text + '\n')
            
            # Read complete file content
            with open(filepath, 'r', encoding='utf-8') as file:
                complete_text = file.read()
            
            # Get just the filename
            filename = os.path.basename(filepath)
            
            # Return all requested information
            return {
                "ui": {"text": text},
                "result": (
                    text,           # added_text
                    complete_text,  # complete_text
                    filename,       # filename
                    full_path       # full_path
                )
            }
            
        except (OSError, IOError) as e:
            raise ValueError(f"Error saving file: {str(e)}")
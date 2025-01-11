import os

class LoadTextFromFolder:
    @classmethod
    def INPUT_TYPES(cls):
        """Define input parameters for the node"""
        default_dir = "Bjornulf/Text"
        available_files = []
        
        if os.path.exists(default_dir):
            available_files = [f for f in os.listdir(default_dir) 
                             if f.lower().endswith('.txt')]
            
        if not available_files:
            available_files = ["no_files_found"]
        
        return {
            "required": {
                "text_file": (available_files, {"default": available_files[0]}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("text", "filename", "full_path")
    FUNCTION = "load_text"
    CATEGORY = "Bjornulf"

    def load_text(self, text_file):
        try:
            if text_file == "no_files_found":
                raise ValueError("No text files found in Bjornulf/Text folder")
                
            filepath = os.path.join("Bjornulf/Text", text_file)
                
            # Check if file exists
            if not os.path.exists(filepath):
                raise ValueError(f"File not found: {filepath}")
                
            # Get absolute path
            full_path = os.path.abspath(filepath)
            
            # Get just the filename
            filename = os.path.basename(filepath)
            
            # Read text from file
            with open(filepath, 'r', encoding='utf-8') as file:
                text = file.read()
                
            return (text, filename, full_path)
            
        except (OSError, IOError) as e:
            raise ValueError(f"Error loading file: {str(e)}")

class LoadTextFromPath:
    @classmethod
    def INPUT_TYPES(cls):
        """Define input parameters for the node"""
        return {
            "required": {
                "file_path": ("STRING", {"default": "Bjornulf/Text/example.txt"}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("text", "filename", "full_path")
    FUNCTION = "load_text"
    CATEGORY = "Bjornulf"

    def load_text(self, file_path):
        try:
            # Validate file extension
            if not file_path.lower().endswith('.txt'):
                raise ValueError("File must be a .txt file")
                
            # Check if file exists
            if not os.path.exists(file_path):
                raise ValueError(f"File not found: {file_path}")
                
            # Get absolute path
            full_path = os.path.abspath(file_path)
            
            # Get just the filename
            filename = os.path.basename(file_path)
            
            # Read text from file
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                
            return (text, filename, full_path)
            
        except (OSError, IOError) as e:
            raise ValueError(f"Error loading file: {str(e)}")
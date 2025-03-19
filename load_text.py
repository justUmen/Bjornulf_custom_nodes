import os
from server import PromptServer
import aiohttp.web as web

class LoadTextFromFolder:
    default_dir = "Bjornulf/Text"
    
    @classmethod
    def INPUT_TYPES(cls):
        """Define input parameters for the node"""
        available_files = cls.get_available_files()
        if not available_files:
            available_files = ["no_files_found"]
        return {
            "required": {
                "text_file": (available_files, {"default": available_files[0]}),
            }
        }

    @classmethod
    def get_available_files(cls):
        """Get list of .txt files recursively from the default directory"""
        available_files = []
        if os.path.exists(cls.default_dir):
            for root, dirs, files in os.walk(cls.default_dir):
                for file in files:
                    if file.lower().endswith('.txt'):
                        full_path = os.path.join(root, file)
                        rel_path = os.path.relpath(full_path, cls.default_dir)
                        available_files.append(rel_path)
            available_files.sort()
        return available_files

    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("text", "filename", "full_path")
    FUNCTION = "load_text"
    CATEGORY = "Bjornulf"

    def load_text(self, text_file):
        """Load text from the selected file"""
        try:
            if text_file == "no_files_found":
                raise ValueError("No text files found in Bjornulf/Text folder")
            filepath = os.path.join(self.default_dir, text_file)
            if not os.path.exists(filepath):
                raise ValueError(f"File not found: {filepath}")
            full_path = os.path.abspath(filepath)
            filename = os.path.basename(filepath)
            with open(filepath, 'r', encoding='utf-8') as file:
                text = file.read()
            return (text, filename, full_path)
        except (OSError, IOError) as e:
            raise ValueError(f"Error loading file: {str(e)}")

@PromptServer.instance.routes.post("/get_text_files")
async def get_text_files(request):
    try:
        available_files = LoadTextFromFolder.get_available_files()
        return web.json_response({
            "success": True,
            "files": available_files
        }, status=200)
    except Exception as e:
        error_msg = str(e)
        return web.json_response({
            "success": False,
            "error": error_msg
        }, status=500)

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
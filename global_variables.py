import os
import re
import folder_paths
import logging

class Everything(str):
    def __ne__(self, __value: object) -> bool:
        return False

# Define VAR_PATTERN at module level if not already defined
VAR_PATTERN = re.compile(r'^([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(.+)$')

class SaveGlobalVariables:
    def __init__(self):
        self.base_dir = os.path.join(folder_paths.base_path, 'Bjornulf')
        self.global_vars_dir = os.path.join(self.base_dir, 'GlobalVariables')
        os.makedirs(self.global_vars_dir, exist_ok=True)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "variables": ("STRING", {"multiline": True, "default": ""}),
                "mode": (["append", "overwrite"], {"default": "append"}),
            },
            "optional": {
                "filename": ("STRING", {"default": ""}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("connect_to_workflow",)
    FUNCTION = "save_variables"
    OUTPUT_NODE = True
    CATEGORY = "Bjornulf"

    def save_variables(self, variables, mode, filename=""):
        # Determine target file path
        if filename.strip():
            filename_clean = os.path.basename(filename.strip())
            if not filename_clean.endswith('.txt'):
                filename_clean += '.txt'
            file_path = os.path.join(self.global_vars_dir, filename_clean)
        else:
            file_path = os.path.join(self.base_dir, 'GlobalVariables.txt')

        # Validate and parse input variables
        valid_vars = {}
        errors = []
        for line in variables.split('\n'):
            line = line.strip()
            if not line:
                continue
            match = VAR_PATTERN.match(line)
            if match:
                var_name, var_value = match.groups()
                logging.info(f"VALID syntax for Variable : {line}")
                valid_vars[var_name] = line
            else:
                logging.info(f"Invalid syntax for Variable : {line}")
                errors.append(f"Invalid syntax: {line}")

        if errors:
            print("\n".join(errors))
        
        # Merge based on mode
        if mode == "append":
            # Always read existing variables first
            existing_vars = {}
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        for line in f:
                            line = line.strip()
                            if match := VAR_PATTERN.match(line):
                                var_name = match.group(1)
                                existing_vars[var_name] = line
                except Exception as e:
                    logging.info(f"Error reading existing file: {e}")
            merged_vars = {**existing_vars, **valid_vars}
        else:  # overwrite
            merged_vars = valid_vars

        # Ensure directory exists before writing
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                if merged_vars:
                    f.write('\n'.join(merged_vars.values()) + '\n')
                else:
                    f.write('')  # Create empty file if no variables
        except Exception as e:
            logging.info(f"Error writing to file: {e}")

        return ("",)

class LoadGlobalVariables:
    def __init__(self):
        self.base_dir = os.path.join(folder_paths.base_path, 'Bjornulf')
        self.global_vars_dir = os.path.join(self.base_dir, 'GlobalVariables')
        os.makedirs(self.global_vars_dir, exist_ok=True)

    @classmethod
    def INPUT_TYPES(cls):
        var_files = []
        try:
            var_files = [f[:-4] for f in os.listdir(cls.global_vars_dir())
                        if f.endswith('.txt') and os.path.isfile(os.path.join(cls.global_vars_dir(), f))]
            var_files.sort()
        except FileNotFoundError:
            pass
            
        return {
            "required": {
                "seed": ("INT", {"default": -1, "min": -1, "max": 0x7FFFFFFFFFFFFFFF}),
            },
            "optional": {
                "filename": ("STRING", {"default": ""}),
                "file_list": (["default"] + var_files, {"default": "default"}),
                "connect_to_workflow": (Everything("*"), {"forceInput": True}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("variables",)
    FUNCTION = "load_variables"
    CATEGORY = "Bjornulf"

    @classmethod
    def global_vars_dir(cls):
        return os.path.join(folder_paths.base_path, 'Bjornulf', 'GlobalVariables')

    def load_variables(self, seed, connect_to_workflow="", filename="", file_list="default"):
        # First check if filename is provided and not empty
        if filename.strip():
            target_file = filename.strip()
        else:
            # If filename is empty, use file_list
            target_file = file_list.strip()

        if target_file and target_file != "default":
            # Ensure .txt extension
            if not target_file.endswith('.txt'):
                target_file += '.txt'
            # Load from GlobalVariables subdirectory
            file_path = os.path.join(self.global_vars_dir, target_file)
        else:
            # Load default GlobalVariables.txt from base directory
            file_path = os.path.join(self.base_dir, 'GlobalVariables.txt')

        # Return empty string if file doesn't exist
        if not os.path.exists(file_path):
            return ("",)

        # Read and return file contents
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read().strip()

        return (content,)

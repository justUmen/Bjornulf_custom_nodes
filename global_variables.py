import os
import folder_paths


class SaveGlobalVariables:
    def __init__(self):
        self.output_dir = os.path.join(folder_paths.base_path, 'Bjornulf')
        self.filename = os.path.join(self.output_dir, 'GlobalVariables.txt')
        os.makedirs(self.output_dir, exist_ok=True)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "variables": ("STRING", {"multiline": True, "default": ""}),
                "mode": (["append", "overwrite"], {"default": "append"}),
            },
        }

    RETURN_TYPES = ()
    FUNCTION = "save_variables"
    OUTPUT_NODE = True
    CATEGORY = "Bjornulf"

    def save_variables(self, variables, mode):
        # Clean and validate input
        new_lines = set(line.strip() for line in variables.split('\n') if line.strip())

        if mode == "overwrite":
            with open(self.filename, 'w', encoding='utf-8') as f:
                f.write('\n'.join(new_lines) + '\n')
        else:  # append mode
            if os.path.exists(self.filename):
                with open(self.filename, 'r', encoding='utf-8') as f:
                    existing_lines = set(line.strip() for line in f.readlines() if line.strip())
            else:
                existing_lines = set()

            # Add only new unique lines
            unique_lines = new_lines - existing_lines
            if unique_lines:
                with open(self.filename, 'a', encoding='utf-8') as f:
                    f.write('\n'.join(unique_lines) + '\n')

        return ()


class LoadGlobalVariables:
    def __init__(self):
        self.output_dir = os.path.join(folder_paths.base_path, 'Bjornulf')
        self.filename = os.path.join(self.output_dir, 'GlobalVariables.txt')
        os.makedirs(self.output_dir, exist_ok=True)

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {
                "seed": ("INT", {
                    "default": -1,
                    "min": -1,
                    "max": 0x7FFFFFFFFFFFFFFF
                }),
            }}

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("variables",)
    FUNCTION = "load_variables"
    CATEGORY = "Bjornulf"

    def load_variables(self, seed):
        if not os.path.exists(self.filename):
            return ("",)

        with open(self.filename, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read().strip()
        
        os.sync()  # Ensures that any pending file writes are flushed to disk
        return (content,)
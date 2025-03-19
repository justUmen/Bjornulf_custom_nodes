import os
import shutil
import time
import uuid
import urllib.request
import urllib.parse

class AudioPreview:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "audio_path": ("STRING", {"default": ""}),
                "autoplay": ("BOOLEAN", {"default": False}),
                "loop": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ()
    FUNCTION = "preview_audio"
    CATEGORY = "audio"
    OUTPUT_NODE = True

    def preview_audio(self, audio_path, autoplay, loop):
        try:
            # Validate input
            if not audio_path or not isinstance(audio_path, str) or not audio_path.strip():
                raise ValueError("No valid audio path provided.")

            # Set up destination directory
            dest_dir = os.path.join("temp", "Bjornulf")
            os.makedirs(dest_dir, exist_ok=True)

            # Generate unique filename components
            timestamp = int(time.time())
            uuid_str = str(uuid.uuid4()).replace('-', '')[:8]  # Short unique string
            base_name = "Bjornulf"

            if audio_path.startswith("http://") or audio_path.startswith("https://"):
                # Handle URL input
                parsed_url = urllib.parse.urlparse(audio_path)
                path = parsed_url.path
                ext = os.path.splitext(path)[1]
                if not ext:
                    raise ValueError("URL does not have a file extension.")
                dest_name = f"{base_name}_{timestamp}_{uuid_str}{ext}"
                dest_path = os.path.join(dest_dir, dest_name)
                try:
                    urllib.request.urlretrieve(audio_path, dest_path)
                except Exception as e:
                    raise ValueError(f"Failed to download audio from URL: {audio_path}. Error: {e}")
            else:
                # Handle local file input
                audio_path = os.path.abspath(audio_path)
                if not os.path.exists(audio_path):
                    raise FileNotFoundError(f"Audio file not found: {audio_path}")
                ext = os.path.splitext(audio_path)[1]
                dest_name = f"{base_name}_{timestamp}_{uuid_str}{ext}"
                dest_path = os.path.join(dest_dir, dest_name)
                shutil.copy2(audio_path, dest_path)

            # Return UI data for frontend
            return {
                "ui": {
                    "audio": [dest_name, "Bjornulf"],
                    "metadata": {
                        "autoplay": autoplay,
                        "loop": loop
                    }
                }
            }

        except Exception as e:
            # Handle errors gracefully
            return {
                "ui": {
                    "audio": [],
                    "error": str(e)
                }
            }
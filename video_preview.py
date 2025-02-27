import os
import shutil
import time
import hashlib
from pathlib import Path

SUPPORTED_EXTENSIONS = {'.mp4', '.webm', '.ogg', '.mov', '.mkv'}

class VideoPreview:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video_path": ("STRING", {"forceInput": True}),
                "autoplay": ("BOOLEAN", {"default": False}),
                "mute": ("BOOLEAN", {"default": True}),
            },
        }

    RETURN_TYPES = ()
    FUNCTION = "preview_video"
    CATEGORY = "Bjornulf"
    OUTPUT_NODE = True

    def preview_video(self, video_path, autoplay, mute):
        try:
            if not video_path or not isinstance(video_path, str):
                raise ValueError("Invalid video path provided")

            video_path = os.path.abspath(video_path)
            if not os.path.exists(video_path):
                raise FileNotFoundError(f"Video file not found: {video_path}")

            ext = Path(video_path).suffix.lower()
            if ext not in SUPPORTED_EXTENSIONS:
                raise ValueError(f"Unsupported video format: {ext}. Supported formats: {', '.join(SUPPORTED_EXTENSIONS)}")

            dest_dir = os.path.join("output", "Bjornulf", "preview_video")
            os.makedirs(dest_dir, exist_ok=True)

            file_hash = hashlib.md5(open(video_path,'rb').read()).hexdigest()[:8]
            timestamp = int(time.time())
            base_name = Path(video_path).stem
            dest_name = f"{base_name}_{timestamp}_{file_hash}{ext}"
            dest_path = os.path.join(dest_dir, dest_name)

            if not os.path.exists(dest_path):
                shutil.copy2(video_path, dest_path)

            return {
                "ui": {
                    "video": [dest_name, "Bjornulf/preview_video"],
                    "metadata": {
                        "width": 512,
                        "height": 512,
                        "autoplay": autoplay,
                        "mute": mute
                    }
                }
            }

        except Exception as e:
            return {
                "ui": {
                    "error": str(e),
                    "video": None
                }
            }
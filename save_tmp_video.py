import os
import shutil

class SaveTmpVideo:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video_path": ("STRING", {"forceInput": True}),
            },
        }

    FUNCTION = "save_video"
    RETURN_TYPES = ()
    OUTPUT_NODE = True
    CATEGORY = "Bjornulf"

    def save_video(self, video_path):
        # Ensure the output directory exists
        os.makedirs("./output", exist_ok=True)

        # Verify the video file exists
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
        # Get the file extension
        ext = os.path.splitext(video_path)[1].lower()
        if ext not in ('.mp4', '.mkv', '.webm'):
            raise ValueError("video_path must be a .mp4, .mkv, or .webm file")
        # Copy the file to the output directory with the same extension
        filename = f"./output/tmp_api{ext}"
        shutil.copy(video_path, filename)

        print(f"Temporary video saved as: {filename}")
        return {"ui": {"videos": [{"filename": filename, "type": "output"}]}}
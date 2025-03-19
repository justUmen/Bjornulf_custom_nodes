import os
import shutil
import time
import hashlib
from pathlib import Path
import subprocess
import numpy as np
import cv2
import tempfile

# Supported extensions for video inputs
SUPPORTED_VIDEO_EXTENSIONS = {'.mp4', '.webm', '.ogg', '.mov', '.mkv'}

class VideoPreview:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "fps_for_IMAGES": ("FLOAT", {"default": 24.0, "min": 1.0, "max": 60.0}),
                "autoplay": ("BOOLEAN", {"default": False}),
                "mute": ("BOOLEAN", {"default": True}),
                "loop": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "video_path": ("STRING", {"forceInput": True, "default": ""}),
                "IMAGES": ("IMAGE", {"default": None}),
            }
        }

    RETURN_TYPES = ()
    FUNCTION = "preview_video"
    CATEGORY = "Bjornulf"
    OUTPUT_NODE = True

    def preview_video(self, fps_for_IMAGES, autoplay, mute, loop, video_path="", IMAGES=None):
        try:
            # Destination directory for preview videos
            dest_dir = os.path.join("output", "Bjornulf", "preview_video")
            os.makedirs(dest_dir, exist_ok=True)

            # Determine which input is provided
            if video_path and isinstance(video_path, str) and video_path.strip():
                video_path = os.path.abspath(video_path)
                if not os.path.exists(video_path):
                    raise FileNotFoundError(f"Video file not found: {video_path}")

                ext = Path(video_path).suffix.lower()  # e.g., '.mp4', '.webm'
                if ext not in SUPPORTED_VIDEO_EXTENSIONS:
                    raise ValueError(f"Unsupported video format: {ext}. Supported formats: {', '.join(SUPPORTED_VIDEO_EXTENSIONS)}")

                final_video_path = video_path

                # Generate unique filename with original extension
                file_hash = hashlib.md5(open(final_video_path, 'rb').read()).hexdigest()[:8]
                timestamp = int(time.time())
                base_name = "video_preview"  # More descriptive than "image_sequence"
                dest_name = f"{base_name}_{timestamp}_{file_hash}{ext}"  # Keeps original extension
                dest_path = os.path.join(dest_dir, dest_name)

                shutil.copy2(final_video_path, dest_path)
                print(f"Video copied to: {dest_path}")

            elif IMAGES is not None and len(IMAGES) > 0:
                # Use a unique temporary directory for this run
                with tempfile.TemporaryDirectory(prefix="bjornulf_temp_video_") as temp_dir:
                    # Convert image tensors to files in the unique temp directory
                    image_files = []
                    for i, img_tensor in enumerate(IMAGES):
                        # Convert tensor (H, W, C) in range [0, 1] to numpy array in range [0, 255]
                        img_np = (img_tensor.numpy() * 255).astype(np.uint8)
                        # Ensure RGB format for OpenCV (ComfyUI IMAGES are typically RGB)
                        img_path = os.path.join(temp_dir, f"frame_{i:04d}.png")
                        cv2.imwrite(img_path, cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR))
                        image_files.append(img_path)

                    if not image_files:
                        raise ValueError("No valid IMAGES provided to create a video.")

                    # Create temporary video using FFmpeg
                    output_video = os.path.join(temp_dir, "temp_video.mp4")
                    pattern = os.path.join(temp_dir, "frame_%04d.png")
                    cmd = [
                        "ffmpeg",
                        "-framerate", str(fps_for_IMAGES),
                        "-i", pattern,
                        "-c:v", "libx264",
                        "-pix_fmt", "yuv420p",
                        "-y",  # Overwrite output file if it exists
                        output_video
                    ]
                    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                    if not os.path.exists(output_video):
                        raise RuntimeError("Failed to create temporary video from IMAGES.")

                    final_video_path = output_video

                    # Generate unique destination filename
                    file_hash = hashlib.md5(open(final_video_path, 'rb').read()).hexdigest()[:8]
                    timestamp = int(time.time())
                    base_name = "image_sequence"
                    dest_name = f"{base_name}_{timestamp}_{file_hash}.mp4"
                    dest_path = os.path.join(dest_dir, dest_name)

                    # Copy the video to the preview directory
                    if not os.path.exists(dest_path):
                        shutil.copy2(final_video_path, dest_path)

            else:
                raise ValueError("Either 'video_path' or 'IMAGES' must be provided.")

            # Successful return with video data
            return {
                "ui": {
                    "video": [dest_name, "Bjornulf/preview_video"],
                    "metadata": {
                        "width": 512,
                        "height": 512,
                        "autoplay": autoplay,
                        "mute": mute,
                        "loop": loop
                    }
                }
            }

        except Exception as e:
            # Error case: return an empty list for "video" to prevent iteration error
            return {
                "ui": {
                    "video": [],  # Changed from None to []
                    "error": str(e)
                }
            }
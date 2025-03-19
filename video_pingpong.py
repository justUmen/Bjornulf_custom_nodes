import torch
import os
import shutil
from PIL import Image
import numpy as np
import glob
import subprocess

class VideoPingPong:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": {
                "images": ("IMAGE",),
                "video_path": ("STRING", {"default": ""}),
                "use_python_ffmpeg": ("BOOLEAN", {"default": False}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("IMAGES",)
    FUNCTION = "pingpong_images"
    CATEGORY = "Bjornulf"

    def extract_frames(self, video_path, temp_dir, use_python_ffmpeg):
        """Extract frames from a video file using FFmpeg, preserving original settings."""
        if use_python_ffmpeg:
            try:
                import ffmpeg
                (
                    ffmpeg
                    .input(video_path)
                    .output(os.path.join(temp_dir, 'frame_%04d.png'), start_number=0)
                    .run()
                )
            except ImportError:
                raise RuntimeError("ffmpeg-python is not installed. Please install it or set use_python_ffmpeg to False.")
            except ffmpeg.Error as e:
                raise RuntimeError(f"Failed to extract frames using ffmpeg-python: {e}")
        else:
            ffmpeg_cmd = ['ffmpeg', '-i', video_path, '-start_number', '0', os.path.join(temp_dir, 'frame_%04d.png')]
            try:
                subprocess.run(ffmpeg_cmd, check=True)
            except subprocess.CalledProcessError as e:
                raise RuntimeError(f"Failed to extract frames using FFmpeg: {e}")

    def pingpong_images(self, images=None, video_path="", use_python_ffmpeg=False):
        """Generate a ping-pong sequence from images or a video file, prioritizing images if provided."""
        temp_dir = "temp_pingpong"
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.makedirs(temp_dir)

        try:
            if images is not None:
                num_frames = images.shape[0]
                for i in range(num_frames):
                    img_tensor = images[i]
                    img_pil = Image.fromarray((img_tensor.cpu().numpy() * 255).astype('uint8'))
                    img_path = os.path.join(temp_dir, f"frame_{i:04d}.png")
                    img_pil.save(img_path)
            elif video_path and os.path.exists(video_path):
                self.extract_frames(video_path, temp_dir, use_python_ffmpeg)
            else:
                raise ValueError("Either images or a valid video_path must be provided")

            frame_files = sorted(glob.glob(os.path.join(temp_dir, "frame_*.png")))
            num_frames = len(frame_files)
            if num_frames == 0:
                raise RuntimeError("No frames available to process")

            pingpong_list = list(range(num_frames)) + list(range(num_frames - 2, 0, -1))

            batch_size = 10
            pingpong_tensors = []
            for i in range(0, len(pingpong_list), batch_size):
                batch = pingpong_list[i:i + batch_size]
                batch_tensors = []
                for j in batch:
                    img_path = os.path.join(temp_dir, f"frame_{j:04d}.png")
                    img_pil = Image.open(img_path)
                    img_np = np.array(img_pil).astype(np.float32) / 255.0
                    img_tensor = torch.from_numpy(img_np)
                    batch_tensors.append(img_tensor)
                    img_pil.close()
                batch_tensor = torch.stack(batch_tensors)
                pingpong_tensors.append(batch_tensor)
                del batch_tensors
                torch.cuda.empty_cache()

            pingpong_tensor = torch.cat(pingpong_tensors, dim=0)

        finally:
            shutil.rmtree(temp_dir)

        return (pingpong_tensor,)
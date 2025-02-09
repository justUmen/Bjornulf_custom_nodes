import os
import uuid
import subprocess
import tempfile
import torch
import numpy as np
from PIL import Image
import wave
import json
import ffmpeg

class ImagesListToVideo:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),
                "frames_per_second": ("FLOAT", {"default": 30, "min": 1, "max": 120, "step": 1}),
            },
            "optional": {
                "audio_path": ("STRING", {"default": "", "multiline": False}),
                "audio": ("AUDIO", {"default": None}),
                "FFMPEG_CONFIG_JSON": ("STRING", {"default": None}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("video_path",)
    FUNCTION = "images_to_video"
    CATEGORY = "Bjornulf"

    def parse_ffmpeg_config(self, config_json):
        if not config_json:
            return None
        try:
            return json.loads(config_json)
        except json.JSONDecodeError:
            print("Invalid FFmpeg configuration JSON")
            return None

    def build_ffmpeg_command(self, input_pattern, output_path, fps, config=None):
        if not config:
            return [
                "ffmpeg",
                "-framerate", str(fps),
                "-i", input_pattern,
                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                "-crf", "19"
            ]

        cmd = [config["ffmpeg"]["path"]] if config["ffmpeg"]["path"] else ["ffmpeg"]
        cmd.extend(["-framerate", str(config["video"]["fps"]["force_fps"] if config["video"]["fps"]["enabled"] else fps)])
        cmd.extend(["-i", input_pattern])

        # Video settings
        if config["video"]["codec"] not in [None, "None", "copy"]:
            cmd.extend(["-c:v", config["video"]["codec"]])
        
        if config["video"]["pixel_format"] not in [None, "None"]:
            cmd.extend(["-pix_fmt", config["video"]["pixel_format"]])
        
        if config["video"]["preset"] not in [None, "None"]:
            cmd.extend(["-preset", config["video"]["preset"]])
        
        if config["video"]["bitrate"] not in [None, "None", ""]:
            cmd.extend(["-b:v", config["video"]["bitrate"]])
        
        cmd.extend(["-crf", str(config["video"]["crf"])])

        if config["video"]["resolution"] and config["video"]["resolution"]["width"] > 0 and config["video"]["resolution"]["height"] > 0:
            cmd.extend(["-s", f"{config['video']['resolution']['width']}x{config['video']['resolution']['height']}"])

        return cmd

    def images_to_video(self, images, frames_per_second=30, audio_path="", audio=None, ffmpeg_config=None):
        config = self.parse_ffmpeg_config(ffmpeg_config)
        
        output_dir = os.path.join("Bjornulf", "images_to_video")
        os.makedirs(output_dir, exist_ok=True)

        # Determine output format
        output_format = "mp4"
        if config and config["output"]["container_format"] not in [None, "None"]:
            output_format = config["output"]["container_format"]

        video_filename = f"video_{uuid.uuid4().hex}.{output_format}"
        video_path = os.path.join(output_dir, video_filename)

        with tempfile.TemporaryDirectory() as temp_dir:
            for i, img in enumerate(images):
                img_np = self.convert_to_numpy(img)
                if img_np.shape[-1] != 3:
                    img_np = self.convert_to_rgb(img_np)
                img_pil = Image.fromarray(img_np)
                img_path = os.path.join(temp_dir, f"frame_{i:05d}.png")
                img_pil.save(img_path)

            input_pattern = os.path.join(temp_dir, "frame_%05d.png")
            ffmpeg_cmd = self.build_ffmpeg_command(input_pattern, video_path, frames_per_second, config)

            # Handle audio
            temp_audio_path = None
            if not (config and config["audio"]["enabled"] == False):
                if audio is not None and isinstance(audio, dict):
                    waveform = audio['waveform'].numpy().squeeze()
                    sample_rate = audio['sample_rate']
                    temp_audio_path = os.path.join(temp_dir, "temp_audio.wav")
                    self.write_wav(temp_audio_path, waveform, sample_rate)
                elif audio_path and os.path.isfile(audio_path):
                    temp_audio_path = audio_path

            if temp_audio_path:
                temp_video = os.path.join(temp_dir, "temp_video.mp4")
                temp_cmd = ffmpeg_cmd + ["-y", temp_video]
                
                try:
                    subprocess.run(temp_cmd, check=True, capture_output=True, text=True)
                    
                    audio_cmd = [
                        config["ffmpeg"]["path"] if config else "ffmpeg",
                        "-i", temp_video,
                        "-i", temp_audio_path,
                        "-c:v", "copy"
                    ]

                    # Audio codec settings from config
                    if config and config["audio"]["codec"] not in [None, "None"]:
                        audio_cmd.extend(["-c:a", config["audio"]["codec"]])
                    else:
                        audio_cmd.extend(["-c:a", "aac"])

                    if config and config["audio"]["bitrate"]:
                        audio_cmd.extend(["-b:a", config["audio"]["bitrate"]])

                    audio_cmd.extend(["-shortest", "-y", video_path])
                    
                    subprocess.run(audio_cmd, check=True, capture_output=True, text=True)
                except subprocess.CalledProcessError as e:
                    print(f"FFmpeg error: {e.stderr}")
                    return ("",)
            else:
                ffmpeg_cmd.append("-y")
                ffmpeg_cmd.append(video_path)
                try:
                    subprocess.run(ffmpeg_cmd, check=True, capture_output=True, text=True)
                except subprocess.CalledProcessError as e:
                    print(f"FFmpeg error: {e.stderr}")
                    return ("",)

        return (video_path,)

    def write_wav(self, file_path, audio_data, sample_rate):
        with wave.open(file_path, 'wb') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            audio_data = np.int16(audio_data * 32767)
            wav_file.writeframes(audio_data.tobytes())

    def convert_to_numpy(self, img):
        if isinstance(img, torch.Tensor):
            img = img.cpu().numpy()
        if img.dtype == np.uint8:
            return img
        elif img.dtype == np.float32 or img.dtype == np.float64:
            return (img * 255).astype(np.uint8)
        else:
            raise ValueError(f"Unsupported data type: {img.dtype}")

    def convert_to_rgb(self, img):
        if img.shape[-1] == 1:
            return np.repeat(img, 3, axis=-1)
        elif img.shape[-1] == 768:
            img = img.reshape((-1, 3))
            img = (img - img.min()) / (img.max() - img.min())
            img = (img * 255).astype(np.uint8)
            return img.reshape((img.shape[0], -1, 3))
        elif len(img.shape) == 2:
            return np.stack([img, img, img], axis=-1)
        else:
            raise ValueError(f"Unsupported image shape: {img.shape}")
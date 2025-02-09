import json
import subprocess
import ffmpeg

class FFmpegConfig:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "ffmpeg_path": ("STRING", {"default": "ffmpeg"}),
                "video_codec": ([
                    "None",
                    "copy",
                    "libx264 (H.264)",
                    "h264_nvenc (H.264 / NVIDIA GPU)", 
                    "libx265 (H.265)",
                    "hevc_nvenc (H.265 / NVIDIA GPU)",
                    "libvpx-vp9 (WebM)",
                    "libaom-av1"
                ], {"default": "None"}),
                
                "video_bitrate": ("STRING", {"default": "3045k"}),
                
                "preset": ([
                    "None",
                    "ultrafast",
                    "superfast",
                    "veryfast", 
                    "faster",
                    "fast",
                    "medium",
                    "slow",
                    "slower",
                    "veryslow"
                ], {"default": "medium"}),
                
                "pixel_format": ([
                    "None",
                    "yuv420p",
                    "yuv444p",
                    "yuv420p10le",
                    "yuv444p10le", 
                    "rgb24",
                    "rgba",
                    "yuva420p"
                ], {"default": "yuv420p"}),
                
                "container_format": ([
                    "None",
                    "mp4",
                    "mkv", 
                    "webm",
                    "mov",
                    "avi"
                ], {"default": "mp4"}),
                
                "crf": ("INT", {"default": 19, "min": 1, "max": 63}),
                
                "force_fps": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 240.0,
                    "step": 0.01,
                    "description": "Force output FPS (0 = use source FPS)"
                }),
                "enabled_change_resolution": ("BOOLEAN", {"default": False}),
                "width": ("INT", {"default": 0, "min": 0, "max": 10000}),
                "height": ("INT", {"default": 0, "min": 0, "max": 10000}),
                
                "ignore_audio": ("BOOLEAN", {"default": False}),
                "audio_codec": ([
                    "None",
                    "copy",
                    "aac",
                    "libmp3lame",
                    "libvorbis", 
                    "libopus",
                    "none"
                ], {"default": "aac"}),
                "audio_bitrate": ("STRING", {"default": "192k"}),
                
                "force_transparency": ("BOOLEAN", {
                    "default": False,
                    "description": "Force transparency in WebM output"
                }),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("FFMPEG_CONFIG_JSON",)
    FUNCTION = "create_config"
    CATEGORY = "Bjornulf"

    def get_ffmpeg_version(self, ffmpeg_path):
        try:
            result = subprocess.run(
                [ffmpeg_path, "-version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            version_line = result.stdout.splitlines()[0]
            return version_line
        except Exception as e:
            return f"Error fetching FFmpeg version: {e}"

    def create_json_output(self, config):
        """Create a JSON string containing all FFmpeg configuration."""
        ffmpeg_version = self.get_ffmpeg_version(config["ffmpeg_path"])
        config_info = {
            "ffmpeg": {
                "path": config["ffmpeg_path"],
                "version": ffmpeg_version
            },
            "video": {
                "codec": config["video_codec"] or "None",
                "bitrate": config["video_bitrate"],
                "preset": config["preset"] or "None",
                "pixel_format": config["pixel_format"] or "None",
                "crf": config["crf"],
                "resolution": (
                    {"width": config["width"], "height": config["height"]}
                    if (config["enabled_change_resolution"] and config["width"] > 0 and config["height"] > 0)
                    else None
                ),
                "fps": {
                    "force_fps": config["force_fps"],
                    "enabled": config["force_fps"] > 0
                },
                "force_transparency": config["force_transparency"]
            },
            "audio": {
                "enabled": not config["ignore_audio"],
                "codec": config["audio_codec"] or "None",
                "bitrate": config["audio_bitrate"]
            },
            "output": {
                "container_format": config["container_format"] or "None"
            }
        }
        return json.dumps(config_info, indent=2)

    def create_config(self, ffmpeg_path, ignore_audio, video_codec, audio_codec,
                     video_bitrate, audio_bitrate, preset, pixel_format,
                     container_format, crf, force_fps, enabled_change_resolution, 
                     width, height, force_transparency):
                     
        config = {
            "ffmpeg_path": ffmpeg_path,
            "video_bitrate": video_bitrate,
            "preset": None if preset == "None" else preset,
            "crf": crf,
            "force_fps": force_fps,
            "enabled_change_resolution": enabled_change_resolution,
            "ignore_audio": ignore_audio,
            "audio_bitrate": audio_bitrate,
            "width": width,
            "height": height,
            "video_codec": video_codec.split(" ")[0] if video_codec != "None" else None,
            "pixel_format": None if pixel_format == "None" else pixel_format,
            "container_format": None if container_format == "None" else container_format,
            "audio_codec": None if audio_codec == "None" or ignore_audio else audio_codec,
            "force_transparency": force_transparency
        }

        return (self.create_json_output(config),)

    @classmethod 
    def IS_CHANGED(cls, ffmpeg_path, ignore_audio, video_codec, audio_codec,
                  video_bitrate, audio_bitrate, preset, pixel_format,
                  container_format, crf, force_fps, enabled_change_resolution, 
                  width, height, force_transparency) -> float:
        return 0.0
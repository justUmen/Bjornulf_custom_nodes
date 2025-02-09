import os
import numpy as np
import torch
import subprocess
import json
from PIL import Image
import soundfile as sf
import glob

class imagesToVideo:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "fps": ("FLOAT", {"default": 24, "min": 1, "max": 120}),
                "name_prefix": ("STRING", {"default": "imgs2video/me"}),
                "use_python_ffmpeg": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "audio": ("AUDIO",),
                "FFMPEG_CONFIG_JSON": ("STRING", {"forceInput": True}),
            },
        }

    RETURN_TYPES = ("STRING", "STRING",)
    RETURN_NAMES = ("comment", "ffmpeg_command",)
    FUNCTION = "image_to_video"
    OUTPUT_NODE = True
    CATEGORY = "Bjornulf"
    
    def parse_ffmpeg_config(self, config_json):
        if not config_json:
            return None
        try:
            return json.loads(config_json)
        except json.JSONDecodeError:
            print("Error parsing FFmpeg config JSON")
            return None

    def run_ffmpeg_python(self, ffmpeg_cmd, output_file, ffmpeg_path):
        try:
            import ffmpeg
        except ImportError as e:
            print(f"Error importing ffmpeg-python: {e}")
            return False, "ffmpeg-python library not installed"

        try:
            # Reconstruct the command using ffmpeg-python syntax
            inputs = []
            streams = []
            audio_added = False
            
            # Parse command elements
            i = 0
            while i < len(ffmpeg_cmd):
                if ffmpeg_cmd[i] == "-framerate":
                    framerate = float(ffmpeg_cmd[i+1])
                    i += 2
                elif ffmpeg_cmd[i] == "-i":
                    if "frame_" in ffmpeg_cmd[i+1]:  # Image sequence input
                        video_input = ffmpeg.input(ffmpeg_cmd[i+1], framerate=framerate)
                        streams.append(video_input.video)
                    else:  # Audio input
                        audio_input = ffmpeg.input(ffmpeg_cmd[i+1])
                        streams.append(audio_input.audio)
                        audio_added = True
                    i += 2
                elif ffmpeg_cmd[i] == "-vf":
                    filters = ffmpeg_cmd[i+1].split(',')
                    for f in filters:
                        if 'scale=' in f:
                            w, h = f.split('=')[1].split(':')
                            video_input = video_input.filter('scale', w, h)
                    i += 2
                elif ffmpeg_cmd[i] in ["-c:v", "-preset", "-crf", "-cq", "-b:v", "-pix_fmt"]:
                    key = ffmpeg_cmd[i][1:]
                    value = ffmpeg_cmd[i+1]
                    if key == 'c:v':
                        streams[-1] = streams[-1].output(vcodec=value)
                    elif key == 'preset':
                        streams[-1] = streams[-1].output(preset=value)
                    elif key in ['crf', 'cq']:
                        streams[-1] = streams[-1].output(**{key: value})
                    elif key == 'b:v':
                        streams[-1] = streams[-1].output(**{'b:v': value})
                    elif key == 'pix_fmt':
                        streams[-1] = streams[-1].output(pix_fmt=value)
                    i += 2
                else:
                    i += 1

            # Handle output
            output = ffmpeg.output(*streams, output_file)
            output.run(cmd=ffmpeg_path, overwrite_output=True)
            return True, "Success"

        except ffmpeg.Error as e:
            return False, f"FFmpeg error: {e.stderr.decode()}"
        except Exception as e:
            return False, f"Error: {str(e)}"

    def image_to_video(self, images, fps, name_prefix, use_python_ffmpeg=False, audio=None, FFMPEG_CONFIG_JSON=None):
        ffmpeg_config = self.parse_ffmpeg_config(FFMPEG_CONFIG_JSON)
        
        format = "mp4"
        if ffmpeg_config and ffmpeg_config["output"]["container_format"] != "None":
            format = ffmpeg_config["output"]["container_format"]
        
        name_prefix = os.path.splitext(name_prefix)[0]
        output_base = os.path.join("output", name_prefix)
        
        existing_files = glob.glob(f"{output_base}_*.{format}")
        if existing_files:
            max_num = max([int(f.split('_')[-1].split('.')[0]) for f in existing_files])
            next_num = max_num + 1
        else:
            next_num = 1
        
        output_file = f"{output_base}_{next_num:04d}.{format}"
        
        temp_dir = "Bjornulf/temp_images_imgs2video"
        if os.path.exists(temp_dir) and os.path.isdir(temp_dir):
            for file in os.listdir(temp_dir):
                os.remove(os.path.join(temp_dir, file))
            os.rmdir(temp_dir)
        
        os.makedirs(temp_dir, exist_ok=True)
        os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else ".", exist_ok=True)

        for i, img_tensor in enumerate(images):
            img = Image.fromarray((img_tensor.cpu().numpy() * 255).astype(np.uint8))
            if format == "webm":
                img = img.convert("RGBA")
            img.save(os.path.join(temp_dir, f"frame_{i:04d}.png"))

        temp_audio_file = None
        if audio is not None and (not ffmpeg_config or not ffmpeg_config["audio"]["enabled"]):
            temp_audio_file = os.path.join(temp_dir, "temp_audio.wav")
            waveform = audio['waveform'].squeeze().numpy()
            sample_rate = audio['sample_rate']
            sf.write(temp_audio_file, waveform, sample_rate)

        ffmpeg_path = "ffmpeg"
        if ffmpeg_config and ffmpeg_config["ffmpeg"]["path"]:
            ffmpeg_path = ffmpeg_config["ffmpeg"]["path"]

        ffmpeg_cmd = [
            ffmpeg_path,
            "-y",
            "-framerate", str(fps),
            "-i", os.path.join(temp_dir, "frame_%04d.png"),
        ]

        if temp_audio_file:
            ffmpeg_cmd.extend(["-i", temp_audio_file])

        if ffmpeg_config and format == "webm" and ffmpeg_config["video"]["force_transparency"]:
            ffmpeg_cmd.extend([
                "-vf", "scale=iw:ih,format=rgba,split[s0][s1];[s0]lutrgb=r=0:g=0:b=0:a=0[transparent];[transparent][s1]overlay"
            ])

        if ffmpeg_config:
            if ffmpeg_config["video"]["codec"] != "None":
                ffmpeg_cmd.extend(["-c:v", ffmpeg_config["video"]["codec"]])
            
            if ffmpeg_config["video"]["preset"] != "None":
                ffmpeg_cmd.extend(["-preset", ffmpeg_config["video"]["preset"]])
            
            if ffmpeg_config["video"]["bitrate"]:
                ffmpeg_cmd.extend(["-b:v", ffmpeg_config["video"]["bitrate"]])
            
            if ffmpeg_config["video"]["crf"]:
                if "nvenc" in (ffmpeg_config["video"]["codec"] or ""):
                    ffmpeg_cmd.extend(["-cq", str(ffmpeg_config["video"]["crf"])])
                else:
                    ffmpeg_cmd.extend(["-crf", str(ffmpeg_config["video"]["crf"])])
            
            if ffmpeg_config["video"]["pixel_format"] != "None":
                ffmpeg_cmd.extend(["-pix_fmt", ffmpeg_config["video"]["pixel_format"]])
            
            if ffmpeg_config["video"]["resolution"]:
                scale_filter = f"scale={ffmpeg_config['video']['resolution']['width']}:{ffmpeg_config['video']['resolution']['height']}"
                if format == "webm" and ffmpeg_config["video"]["force_transparency"]:
                    current_filter_idx = ffmpeg_cmd.index("-vf") + 1
                    current_filter = ffmpeg_cmd[current_filter_idx]
                    ffmpeg_cmd[current_filter_idx] = scale_filter + "," + current_filter
                else:
                    ffmpeg_cmd.extend(["-vf", scale_filter])
            
            if ffmpeg_config["video"]["fps"]["enabled"]:
                ffmpeg_cmd.extend(["-r", str(ffmpeg_config["video"]["fps"]["force_fps"])])
            
            if not ffmpeg_config["audio"]["enabled"]:
                ffmpeg_cmd.extend(["-an"])
            elif ffmpeg_config["audio"]["codec"] != "None" and temp_audio_file:
                ffmpeg_cmd.extend(["-c:a", ffmpeg_config["audio"]["codec"]])
                if ffmpeg_config["audio"]["bitrate"]:
                    ffmpeg_cmd.extend(["-b:a", ffmpeg_config["audio"]["bitrate"]])
        else:
            if format == "mp4":
                ffmpeg_cmd.extend([
                    "-c:v", "libx264",
                    "-preset", "medium",
                    "-crf", "19",
                    "-pix_fmt", "yuv420p"
                ])
                if temp_audio_file:
                    ffmpeg_cmd.extend(["-c:a", "aac"])
            elif format == "webm":
                ffmpeg_cmd.extend([
                    "-c:v", "libvpx-vp9",
                    "-crf", "30",
                    "-b:v", "0",
                    "-pix_fmt", "yuva420p"
                ])
                if temp_audio_file:
                    ffmpeg_cmd.extend(["-c:a", "libvorbis"])

        ffmpeg_cmd.append(output_file)

        try:
            if use_python_ffmpeg:
                success, message = self.run_ffmpeg_python(ffmpeg_cmd, output_file, ffmpeg_path)
                comment = f"Python FFmpeg: {message}" if not success else f"Video created successfully with {'custom' if ffmpeg_config else 'default'} settings (Python FFmpeg)"
            else:
                subprocess.run(ffmpeg_cmd, check=True)
                comment = f"Video created successfully with {'custom' if ffmpeg_config else 'default'} FFmpeg settings"
            
            print(f"Video created successfully: {output_file}")
        except subprocess.CalledProcessError as e:
            print(f"Error creating video: {e}")
            comment = f"Error creating video: {e}"
        finally:
            print("Temporary files not removed for debugging purposes.")

        return (comment,ffmpeg_cmd,)
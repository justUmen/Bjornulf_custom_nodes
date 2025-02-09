import os
import subprocess
import tempfile
from PIL import Image
import numpy as np
import torch
import torchaudio
import time
import shutil

class CombineVideoAudio:
    def __init__(self):
        self.base_dir = "Bjornulf"
        self.temp_dir = os.path.join(self.base_dir, "temp_frames")
        self.output_dir = os.path.join(self.base_dir, "combined_output")
        os.makedirs(self.temp_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {
                "IMAGES": ("IMAGE", {"forceInput": True}),
                "AUDIO": ("AUDIO", {"forceInput": True}),
                "audio_path": ("STRING", {"default": "", "multiline": False, "forceInput": True}),
                "video_path": ("STRING", {"default": "", "multiline": False, "forceInput": True}),
                "fps": ("FLOAT", {"default": 30.0, "min": 1.0, "max": 120.0, "step": 0.1}),
            }
        }

    RETURN_TYPES = ("STRING", "FLOAT", "FLOAT", "INT")
    RETURN_NAMES = ("video_path", "video_duration", "fps", "number_of_frames")
    FUNCTION = "combine_audio_video"
    CATEGORY = "Bjornulf"
    
    def get_video_frame_count(self, video_path):
        try:
            result = subprocess.run([
                "ffprobe", "-v", "error", "-count_packets",
                "-select_streams", "v:0", "-show_entries", "stream=nb_read_packets",
                "-of", "csv=p=0", video_path
            ], capture_output=True, text=True, check=True)
            
            frame_count = result.stdout.strip()
            if not frame_count:
                raise ValueError("ffprobe returned empty frame count")
            
            return int(frame_count)
        except subprocess.CalledProcessError as e:
            print(f"Error running ffprobe: {e}")
            print(f"ffprobe stderr: {e.stderr}")
            raise
        except ValueError as e:
            print(f"Error parsing ffprobe output: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error getting frame count: {e}")
            raise
    
    def get_video_duration(self, video_path):
        try:
            result = subprocess.run([
                "ffprobe", "-v", "error", "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1", video_path
            ], capture_output=True, text=True, check=True)
            
            duration = result.stdout.strip()
            if not duration:
                raise ValueError("ffprobe returned empty duration")
            
            return float(duration)
        except subprocess.CalledProcessError as e:
            print(f"Error running ffprobe: {e}")
            print(f"ffprobe stderr: {e.stderr}")
            raise
        except ValueError as e:
            print(f"Error parsing ffprobe output: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error getting video duration: {e}")
            raise
    
    def combine_audio_video(self, IMAGES=None, AUDIO=None, audio_path="", video_path="", fps=30.0):
        temp_dir = tempfile.mkdtemp(dir=self.temp_dir)
        try:
            # Handle audio input
            if audio_path and os.path.exists(audio_path):
                final_audio_path = audio_path
            elif AUDIO is not None:
                final_audio_path = os.path.join(temp_dir, "temp_audio.wav")
                waveform = AUDIO['waveform']
                sample_rate = AUDIO['sample_rate']
                
                # Ensure waveform is 2D
                if waveform.dim() == 3:
                    waveform = waveform.squeeze(0)
                elif waveform.dim() == 1:
                    waveform = waveform.unsqueeze(0)
                
                # Ensure waveform is float and in the range [-1, 1]
                if waveform.dtype != torch.float32:
                    waveform = waveform.float()
                waveform = waveform.clamp(-1, 1)
                
                torchaudio.save(final_audio_path, waveform, sample_rate)
            else:
                raise ValueError("No valid audio input provided")

            
            # Handle video input
            if video_path and os.path.exists(video_path):
                final_video_path = video_path
            elif IMAGES is not None:
                frames_path = os.path.join(temp_dir, "frame_%04d.png")
                for i, frame in enumerate(IMAGES):
                    if isinstance(frame, torch.Tensor):
                        frame = frame.cpu().numpy()
                    
                    if frame.ndim == 4:
                        frame = frame.squeeze(0)  # Remove batch dimension if present
                    if frame.shape[0] == 3:
                        frame = frame.transpose(1, 2, 0)  # CHW to HWC
                    
                    if frame.dtype != np.uint8:
                        frame = (frame * 255).astype(np.uint8)
                    
                    Image.fromarray(frame).save(frames_path % (i + 1))
                
                final_video_path = os.path.join(temp_dir, "temp_video.mp4")
                subprocess.run([
                    "ffmpeg", "-y", "-framerate", str(fps),
                    "-i", frames_path, "-c:v", "libx264", "-pix_fmt", "yuv420p",
                    final_video_path
                ], check=True)
            else:
                raise ValueError("No valid video input provided")

            # Get video duration
            duration = self.get_video_duration(final_video_path)

            # Generate a unique filename for the output
            output_filename = f"combined_output_{int(time.time())}.mp4"
            output_path = os.path.join(self.output_dir, output_filename)

            # Combine audio and video
            subprocess.run([
                "ffmpeg", "-y", "-i", final_video_path, "-i", final_audio_path,
                "-t", str(duration), "-c:v", "copy", "-c:a", "aac",
                output_path
            ], check=True)

            # Get the number of frames
            number_of_frames = self.get_video_frame_count(output_path)

            return (output_path, duration, fps, number_of_frames)
        
        finally:
            # Clean up temporary directory
            shutil.rmtree(temp_dir, ignore_errors=True)


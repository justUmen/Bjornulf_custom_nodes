import torch
import torchaudio
import os
import subprocess
from datetime import datetime
import math
from PIL import Image
# import logging
import torchvision.transforms as transforms

class AudioVideoSync:
    """
    ComfyUI custom node for synchronizing audio and video with configurable speed adjustments.
    Supports both video files and image sequences as input, as well as audio files or AUDIO objects.
    """
    
    def __init__(self):
        """Initialize the AudioVideoSync node."""
        self.base_dir = "Bjornulf"
        self.temp_dir = os.path.join(self.base_dir, "temp_frames")
        self.sync_video_dir = os.path.join(self.base_dir, "sync_video")
        self.sync_audio_dir = os.path.join(self.base_dir, "sync_audio")
        
        # Create necessary directories
        for directory in [self.temp_dir, self.sync_video_dir, self.sync_audio_dir]:
            os.makedirs(directory, exist_ok=True)

    @classmethod
    def INPUT_TYPES(cls):
        """Define input parameters for the node."""
        return {
            "required": {
                "max_speedup": ("FLOAT", {
                    "default": 1.5,
                    "min": 1.0,
                    "max": 10.0,
                    "step": 0.1
                }),
                "max_slowdown": ("FLOAT", {
                    "default": 0.5,
                    "min": 0.1,
                    "max": 1.0,
                    "step": 0.1
                }),
            },
            "optional": {
                "IMAGES": ("IMAGE",),
                "AUDIO": ("AUDIO",),
                "audio_path": ("STRING", {"default": "", "forceInput": True}),
                "audio_duration": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 3600.0,
                    "step": 0.001
                }),
                "video_path": ("STRING", {
                    "default": "",
                    "forceInput": True
                }),
                "output_fps": ("FLOAT", {
                    "default": 30.0,
                    "min": 1.0,
                    "max": 120.0,
                    "step": 0.1
                }),
            }
        }

    RETURN_TYPES = ("IMAGE", "AUDIO", "STRING", "STRING", "FLOAT", "FLOAT", "FLOAT", "FLOAT", "INT")
    RETURN_NAMES = ("sync_IMAGES", "sync_AUDIO", "sync_audio_path", "sync_video_path", 
                    "input_video_duration", "sync_video_duration", "input_audio_duration", "sync_audio_duration",
                    "sync_video_frame_count")
    FUNCTION = "sync_audio_video"
    CATEGORY = "Bjornulf"

    def generate_timestamp(self):
        """Generate a unique timestamp for file naming."""
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    def validate_audio_input(self, audio):
        """Validate the audio input format."""
        if not isinstance(audio, dict) or 'waveform' not in audio or 'sample_rate' not in audio:
            raise ValueError("Expected audio input to be a dictionary with 'waveform' and 'sample_rate' keys")

    def validate_speed_limits(self, max_speedup, max_slowdown):
        """Validate the speed limit parameters."""
        if max_speedup < 1.0:
            raise ValueError("max_speedup must be greater than or equal to 1.0")
        if max_slowdown > 1.0:
            raise ValueError("max_slowdown must be less than or equal to 1.0")

    def get_audio_duration(self, audio):
        """Calculate audio duration from audio input."""
        if isinstance(audio, dict) and 'waveform' in audio and 'sample_rate' in audio:
            return audio['waveform'].shape[-1] / audio['sample_rate']
        else:
            raise ValueError("Invalid audio input format")

    def ffprobe_run(self, cmd):
        """Run ffprobe command and return the output."""
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout.strip()

    def get_video_info(self, video_path):
        """Get video duration, fps, and frame count."""
        duration = float(self.ffprobe_run([
            'ffprobe', '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            video_path
        ]))

        fps_str = self.ffprobe_run([
            'ffprobe', '-v', 'error',
            '-select_streams', 'v:0',
            '-show_entries', 'stream=r_frame_rate',
            '-of', 'csv=p=0',
            video_path
        ])
        fps = float(eval(fps_str)) if '/' in fps_str else float(fps_str)

        frame_count = int(self.ffprobe_run([
            'ffprobe', '-v', 'error',
            '-count_packets',
            '-select_streams', 'v:0',
            '-show_entries', 'stream=nb_read_packets',
            '-of', 'csv=p=0',
            video_path
        ]))

        return duration, fps, frame_count

    def process_images_to_video(self, IMAGES, fps):
        """Convert image sequence to video."""
        timestamp = self.generate_timestamp()
        temp_dir = os.path.join(self.temp_dir, f"frames_{timestamp}")
        os.makedirs(temp_dir, exist_ok=True)
        
        # Save frames
        frame_paths = []
        for i, img in enumerate(IMAGES):
            if isinstance(img, torch.Tensor):
                if img.dim() == 4:
                    img = img.squeeze(0)
                img = (img * 255).byte().cpu().numpy()
                img = Image.fromarray(img)
            
            frame_path = os.path.join(temp_dir, f"frame_{i:05d}.png")
            img.save(frame_path)
            frame_paths.append(frame_path)

        # Create video
        output_path = os.path.join(self.temp_dir, f"video_{timestamp}.mp4")
        subprocess.run([
            'ffmpeg', '-y',
            '-framerate', str(fps),
            '-i', os.path.join(temp_dir, 'frame_%05d.png'),
            '-c:v', 'libx264',
            '-pix_fmt', 'yuv420p',
            '-preset', 'medium',
            '-crf', '19',
            output_path
        ], check=True)

        # Cleanup
        for path in frame_paths:
            os.remove(path)
        os.rmdir(temp_dir)

        return output_path

    def adjust_video_speed(self, video_path, speed_factor, output_path):
        """Adjust video speed using ffmpeg."""
        pts_speed = 1 / speed_factor
        subprocess.run([
            'ffmpeg', '-y',
            '-i', video_path,
            '-filter:v', f'setpts={pts_speed}*PTS',
            '-an',
            '-c:v', 'libx264',
            '-preset', 'medium',
            '-crf', '19',
            output_path
        ], check=True)

    def create_sync_video(self, video_path, original_duration, target_duration, max_speedup, max_slowdown):
        """Create synchronized version of the video."""
        timestamp = self.generate_timestamp()
        output_path = os.path.join(self.sync_video_dir, f"sync_video_{timestamp}.mp4")

        if target_duration > original_duration:
            speed_ratio = original_duration / target_duration
            if speed_ratio >= max_slowdown:
                # Slow down video within limits
                self.adjust_video_speed(video_path, speed_ratio, output_path)
            else:
                # Repeat video if slowdown would exceed limit
                repeat_count = math.ceil(target_duration / original_duration)
                concat_file = os.path.join(self.sync_video_dir, f"concat_{timestamp}.txt")
                
                with open(concat_file, 'w') as f:
                    for _ in range(repeat_count):
                        f.write(f"file '{os.path.abspath(video_path)}'\n")

                subprocess.run([
                    'ffmpeg', '-y',
                    '-f', 'concat',
                    '-safe', '0',
                    '-i', concat_file,
                    '-c', 'copy',
                    output_path
                ], check=True)
                os.remove(concat_file)
        else:
            speed_ratio = original_duration / target_duration
            if abs(speed_ratio - 1.0) <= 0.1:
                # Copy video if speed change is minimal
                subprocess.run([
                    'ffmpeg', '-y',
                    '-i', video_path,
                    '-c', 'copy',
                    output_path
                ], check=True)
            else:
                # Speed up video within limits
                speed = min(speed_ratio, max_speedup)
                self.adjust_video_speed(video_path, speed, output_path)

        return os.path.abspath(output_path)

    def process_audio(self, audio_tensor, sample_rate, target_duration, original_duration,
                     max_speedup, max_slowdown):
        """Process audio to match video duration."""
        # Ensure audio tensor has correct dimensions
        if audio_tensor.dim() == 2:
            audio_tensor = audio_tensor.unsqueeze(0)
        elif audio_tensor.dim() == 1:
            audio_tensor = audio_tensor.unsqueeze(0).unsqueeze(0)

        current_duration = audio_tensor.shape[-1] / sample_rate

        # Calculate synchronized video duration
        if target_duration > original_duration:
            speed_ratio = original_duration / target_duration
            if speed_ratio >= max_slowdown:
                sync_duration = target_duration
            else:
                sync_duration = math.ceil(target_duration / original_duration) * original_duration
        else:
            speed_ratio = original_duration / target_duration
            if abs(speed_ratio - 1.0) <= 0.1:
                sync_duration = original_duration
            else:
                speed = min(speed_ratio, max_speedup)
                sync_duration = original_duration / speed

        # Adjust audio length
        if current_duration < sync_duration:
            silence_samples = int((sync_duration - current_duration) * sample_rate)
            silence = torch.zeros(audio_tensor.shape[0], audio_tensor.shape[1], silence_samples)
            processed_audio = torch.cat([audio_tensor, silence], dim=-1)
        else:
            required_samples = int(sync_duration * sample_rate)
            processed_audio = audio_tensor[..., :required_samples]

        return processed_audio, sync_duration

    def save_audio(self, audio_tensor, sample_rate, target_duration, original_duration,
                  max_speedup, max_slowdown):
        """Save processed audio to file and return consistent AUDIO format."""
        timestamp = self.generate_timestamp()
        output_path = os.path.join(self.sync_audio_dir, f"sync_audio_{timestamp}.wav")

        processed_audio, sync_duration = self.process_audio(
            audio_tensor, sample_rate, target_duration, original_duration,
            max_speedup, max_slowdown
        )

        # Save with proper format
        torchaudio.save(output_path, processed_audio.squeeze(0), sample_rate)
        
        # Return consistent AUDIO format
        return {
            'waveform': processed_audio,
            'sample_rate': sample_rate
        }

    def load_audio_from_path(self, audio_path):
        """Load audio from file path and format it consistently with AUDIO input."""
        waveform, sample_rate = torchaudio.load(audio_path)
        
        # Ensure waveform has 3 dimensions (batch, channels, samples) like AUDIO input
        if waveform.dim() == 2:
            waveform = waveform.unsqueeze(0)  # Add batch dimension
        
        # Convert to float32 and normalize to range [0, 1] if needed
        if waveform.dtype != torch.float32:
            waveform = waveform.float()
        if waveform.max() > 1.0:
            waveform = waveform / 32768.0  # Normalize 16-bit audio
            
        return {'waveform': waveform, 'sample_rate': sample_rate}

    def extract_frames(self, video_path):
        """Extract all frames of the video as a tensor."""
        temp_dir = os.path.join(self.temp_dir, "temp_frames")
        os.makedirs(temp_dir, exist_ok=True)

        # Extract frames using ffmpeg
        subprocess.run([
            'ffmpeg', '-i', video_path,
            os.path.join(temp_dir, 'frame_%05d.png')
        ], check=True)

        # Load frames and convert to tensor
        frames = []
        frame_files = sorted(os.listdir(temp_dir))
        transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Lambda(lambda x: x * 255)  # Scale to 0-255 range
        ])

        for frame_file in frame_files:
            image = Image.open(os.path.join(temp_dir, frame_file))
            frame_tensor = transform(image)
            frames.append(frame_tensor)

        # Stack frames into a single tensor
        frames_tensor = torch.stack(frames)

        # Ensure the tensor is in the correct format (B, C, H, W)
        if frames_tensor.dim() == 3:
            frames_tensor = frames_tensor.unsqueeze(0)

        # Convert to uint8
        frames_tensor = frames_tensor.byte()

        # Clean up temporary directory
        for frame_file in frame_files:
            os.remove(os.path.join(temp_dir, frame_file))
        os.rmdir(temp_dir)

        return frames_tensor

    def sync_audio_video(self, max_speedup=1.5, max_slowdown=0.5,
                         AUDIO=None, audio_path="", audio_duration=None,
                         video_path="", IMAGES=None, output_fps=30.0):
        """Main function to synchronize audio and video."""
        self.validate_speed_limits(max_speedup, max_slowdown)

        # Handle audio input
        if AUDIO is None and not audio_path:
            raise ValueError("Either AUDIO or audio_path must be provided")
        
        if audio_path:
            AUDIO = self.load_audio_from_path(audio_path)
        
        self.validate_audio_input(AUDIO)

        # Calculate audio duration if not provided
        if audio_duration is None or audio_duration == 0.0:
            audio_duration = self.get_audio_duration(AUDIO)
            
        # logging.info(f"Audio duration: {audio_duration}")

        # Process input source
        if IMAGES is not None and len(IMAGES) > 0:
            video_path = self.process_images_to_video(IMAGES, output_fps)
            original_duration = len(IMAGES) / output_fps
            video_fps = output_fps
            original_frame_count = len(IMAGES)
        elif video_path:
            original_duration, video_fps, original_frame_count = self.get_video_info(video_path)
        else:
            raise ValueError("Either video_path or IMAGES must be provided")

        # Create synchronized versions
        sync_video_path = self.create_sync_video(
            video_path, original_duration, audio_duration, max_speedup, max_slowdown
        )
        
        # Process and save audio, getting consistent AUDIO format back
        sync_audio = self.save_audio(
            AUDIO['waveform'], AUDIO['sample_rate'], audio_duration,
            original_duration, max_speedup, max_slowdown
        )
        
        # Get sync_audio_path separately
        sync_audio_path = os.path.join(self.sync_audio_dir, f"sync_audio_{self.generate_timestamp()}.wav")
        torchaudio.save(sync_audio_path, sync_audio['waveform'].squeeze(0), sync_audio['sample_rate'])

        # Get final properties
        sync_video_duration, _, sync_frame_count = self.get_video_info(sync_video_path)
        sync_audio_duration = sync_audio['waveform'].shape[-1] / sync_audio['sample_rate']

        video_frames = self.extract_frames(sync_video_path)
        
        # Convert video_frames to the format expected by ComfyUI
        video_frames = video_frames.float() / 255.0
        video_frames = video_frames.permute(0, 2, 3, 1)
        
        return (
            video_frames,
            sync_audio,  # Now returns consistent AUDIO format
            sync_audio_path,
            sync_video_path,
            original_duration,
            sync_video_duration,
            audio_duration,
            sync_audio_duration,
            sync_frame_count
        )
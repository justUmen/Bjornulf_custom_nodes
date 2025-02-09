import subprocess
from pathlib import Path
import os
import json

class ConcatVideos:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "number_of_videos": ("INT", {"default": 2, "min": 2, "max": 50, "step": 1}),
                "output_filename": ("STRING", {"default": "concatenated.mp4"}),
                "use_python_ffmpeg": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "FFMPEG_CONFIG_JSON": ("STRING", {"forceInput": True}),
            },
            "hidden": {
                **{f"video_path_{i}": ("STRING", {"forceInput": True}) for i in range(1, 51)}
            }
        }

    RETURN_TYPES = ("STRING", "STRING",)
    RETURN_NAMES = ("concat_path", "ffmpeg_command",)
    FUNCTION = "concat_videos"
    OUTPUT_NODE = True
    CATEGORY = "Bjornulf"

    def __init__(self):
        self.work_dir = Path(os.path.abspath("temp_concat"))
        self.output_dir = Path(os.path.abspath("Bjornulf/concat_videos"))
        os.makedirs(self.work_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)

    def concat_videos(self, number_of_videos: int, output_filename: str, 
                     use_python_ffmpeg: bool = False, 
                     FFMPEG_CONFIG_JSON: str = None, **kwargs):
        """
        Concatenate multiple videos using ffmpeg.
        Supports both subprocess and python-ffmpeg methods.
        """
        # Get and validate video paths
        video_paths = [kwargs[f"video_path_{i}"] for i in range(1, number_of_videos + 1) 
                      if f"video_path_{i}" in kwargs]
        
        video_paths = [os.path.abspath(path) for path in video_paths]
        for path in video_paths:
            if not Path(path).exists():
                raise ValueError(f"Video path does not exist: {path}")

        # Ensure output filename has mp4 extension
        output_filename = Path(output_filename).with_suffix('.mp4')
        output_path = self.output_dir / output_filename
        
        # Create concat file with absolute paths
        concat_file = self.work_dir / "concat.txt"
        with open(concat_file, 'w') as f:
            for path in video_paths:
                f.write(f"file '{path}'\n")

        # Default configuration
        config = {
            'ffmpeg': {'path': 'ffmpeg', 'use_python_ffmpeg': use_python_ffmpeg}
        }

        # If FFMPEG_CONFIG_JSON provided, parse and merge with default config
        if FFMPEG_CONFIG_JSON:
            try:
                json_config = json.loads(FFMPEG_CONFIG_JSON)
                # Merge JSON config, giving priority to use_python_ffmpeg from the node input
                config = {**json_config, 'ffmpeg': {**json_config.get('ffmpeg', {}), 'use_python_ffmpeg': use_python_ffmpeg}}
            except json.JSONDecodeError:
                raise ValueError("Invalid FFMPEG_CONFIG_JSON format")

        try:
            # Use python-ffmpeg if enabled
            if config.get('ffmpeg', {}).get('use_python_ffmpeg', False):
                import ffmpeg
                
                # Create input streams
                input_streams = [ffmpeg.input(path) for path in video_paths]
                
                # Set up output stream
                output_kwargs = {}
                
                # Video settings
                video_config = config.get('video', {})
                if video_config.get('codec') and video_config['codec'] != 'None':
                    output_kwargs['vcodec'] = video_config['codec']
                    
                    # Additional video encoding parameters
                    if video_config['codec'] != 'copy':
                        if video_config.get('bitrate'):
                            output_kwargs['video_bitrate'] = video_config['bitrate']
                        if video_config.get('crf') is not None:
                            output_kwargs['crf'] = video_config['crf']
                        if video_config.get('preset') and video_config['preset'] != 'None':
                            output_kwargs['preset'] = video_config['preset']
                
                # Audio settings
                audio_config = config.get('audio', {})
                if audio_config.get('enabled') is False or audio_config.get('codec') == 'None':
                    output_kwargs['an'] = None  # No audio
                elif audio_config.get('codec') and audio_config['codec'] != 'None':
                    output_kwargs['acodec'] = audio_config['codec']
                    if audio_config.get('bitrate'):
                        output_kwargs['audio_bitrate'] = audio_config['bitrate']
                
                # Concatenate and output
                output = ffmpeg.concat(*input_streams)
                output = output.output(str(output_path), **output_kwargs)
                
                # Compile and run the command
                ffmpeg_cmd = output.compile()
                output.run(overwrite_output=True)
                
                return str(output_path), ' '.join(ffmpeg_cmd)

            # Default to subprocess method
            else:
                # Default simple concatenation command
                cmd = [
                    'ffmpeg', '-y',
                    '-f', 'concat',
                    '-safe', '0',
                    '-i', str(concat_file),
                    '-c', 'copy',
                    '-movflags', '+faststart',
                    str(output_path)
                ]

                # If FFMPEG_CONFIG_JSON provided, modify command
                if FFMPEG_CONFIG_JSON:
                    cmd = [
                        config.get('ffmpeg', {}).get('path', 'ffmpeg'), '-y',
                        '-f', 'concat',
                        '-safe', '0',
                        '-i', str(concat_file)
                    ]

                    # Video codec settings
                    video_config = config.get('video', {})
                    if video_config.get('codec') and video_config['codec'] != 'None':
                        cmd.extend(['-c:v', video_config['codec']])
                        
                        # Add encoding parameters if not copying
                        if video_config['codec'] != 'copy':
                            if video_config.get('bitrate'):
                                cmd.extend(['-b:v', video_config['bitrate']])
                            if video_config.get('crf') is not None:
                                cmd.extend(['-crf', str(video_config['crf'])])
                            
                            # Add preset if specified
                            if video_config.get('preset') and video_config['preset'] != 'None':
                                cmd.extend(['-preset', video_config['preset']])
                            
                            # Add pixel format if specified
                            if video_config.get('pixel_format') and video_config['pixel_format'] != 'None':
                                cmd.extend(['-pix_fmt', video_config['pixel_format']])

                    # Audio settings
                    audio_config = config.get('audio', {})
                    if audio_config.get('enabled') is False or audio_config.get('codec') == 'None':
                        cmd.extend(['-an'])
                    elif audio_config.get('codec') and audio_config['codec'] != 'None':
                        cmd.extend(['-c:a', audio_config['codec']])
                        if audio_config.get('bitrate'):
                            cmd.extend(['-b:a', audio_config['bitrate']])

                    cmd.extend(['-movflags', '+faststart', str(output_path)])

                # Run subprocess command
                process = subprocess.run(
                    cmd,
                    check=True,
                    capture_output=True,
                    text=True
                )
                return str(output_path), ' '.join(cmd)
            
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"FFmpeg error: {e.stderr}")
        except Exception as e:
            raise RuntimeError(f"Error during video concatenation: {str(e)}")

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")
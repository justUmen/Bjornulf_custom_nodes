import subprocess
from pathlib import Path
import os
import json

class ConvertVideo:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video_path": ("STRING", {"forceInput": True}),
                "output_filename": ("STRING", {"default": "converted.mp4"}),
                "use_python_ffmpeg": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "FFMPEG_CONFIG_JSON": ("STRING", {"forceInput": True}),
            },
        }

    RETURN_TYPES = ("STRING", "STRING",)
    RETURN_NAMES = ("video_path", "ffmpeg_command",)
    FUNCTION = "convert_video"
    OUTPUT_NODE = True
    CATEGORY = "Bjornulf"

    def __init__(self):
        self.output_dir = Path(os.path.abspath("Bjornulf/ffmpeg/converted_videos"))
        os.makedirs(self.output_dir, exist_ok=True)

    def get_default_config(self):
        """Provide basic default configuration."""
        return {
            'ffmpeg_path': 'ffmpeg',  # Assuming ffmpeg is in PATH
            'video_codec': 'libx264',
            'video_bitrate': None,
            'preset': 'medium',
            'pixel_format': 'yuv420p',
            'container_format': 'mp4',
            'crf': 19,
            'force_fps': 0,
            'width': None,
            'height': None,
            'ignore_audio': True,
            'audio_codec': 'aac',
            'audio_bitrate': '128k'
        }
        
    def parse_config_json(self, config_json: str) -> dict:
        """Parse the JSON configuration string into a dictionary format compatible with the converter"""
        config = json.loads(config_json)
        
        return {
            # 'use_python_ffmpeg': config['ffmpeg']['use_python_ffmpeg'],
            'ffmpeg_path': config['ffmpeg']['path'],
            'video_codec': None if config['video']['codec'] == 'None' else config['video']['codec'],
            'video_bitrate': config['video']['bitrate'],
            'preset': None if config['video']['preset'] == 'None' else config['video']['preset'],
            'pixel_format': None if config['video']['pixel_format'] == 'None' else config['video']['pixel_format'],
            'container_format': None if config['output']['container_format'] == 'None' else config['output']['container_format'],
            'crf': config['video']['crf'],
            'force_fps': config['video']['fps']['force_fps'],
            'width': config['video']['resolution']['width'],
            'height': config['video']['resolution']['height'],
            'ignore_audio': not config['audio']['enabled'],
            'audio_codec': None if config['audio']['codec'] == 'None' else config['audio']['codec'],
            'audio_bitrate': config['audio']['bitrate']
        }

    def convert_video_subprocess(self, input_path, output_path, FFMPEG_CONFIG_JSON):
        """Use subprocess to run ffmpeg command"""
        cmd = [
            FFMPEG_CONFIG_JSON['ffmpeg_path'], '-y',
            '-i', str(input_path)
        ]

        # Add video codec settings if not None
        if FFMPEG_CONFIG_JSON['video_codec'] is not None:
            if FFMPEG_CONFIG_JSON['video_codec'] == 'copy':
                cmd.extend(['-c:v', 'copy'])
            else:
                cmd.extend(['-c:v', FFMPEG_CONFIG_JSON['video_codec']])
                
                # Add preset if specified
                if FFMPEG_CONFIG_JSON['preset'] is not None:
                    cmd.extend(['-preset', FFMPEG_CONFIG_JSON['preset']])
                
                # Add width and height if specified
                if FFMPEG_CONFIG_JSON['width'] and FFMPEG_CONFIG_JSON['height']:
                    cmd.extend(['-vf', f'scale={FFMPEG_CONFIG_JSON["width"]}:{FFMPEG_CONFIG_JSON["height"]}'])
                
                # Add video bitrate if specified
                if FFMPEG_CONFIG_JSON['video_bitrate']:
                    cmd.extend(['-b:v', FFMPEG_CONFIG_JSON['video_bitrate']])
                
                # Add CRF if video codec isn't copy
                cmd.extend(['-crf', str(FFMPEG_CONFIG_JSON['crf'])])
                
                # Add pixel format if specified
                if FFMPEG_CONFIG_JSON['pixel_format'] is not None:
                    cmd.extend(['-pix_fmt', FFMPEG_CONFIG_JSON['pixel_format']])
                
                # Add force fps if enabled
                if FFMPEG_CONFIG_JSON['force_fps'] > 0:
                    cmd.extend(['-r', str(FFMPEG_CONFIG_JSON['force_fps'])])

        # Add audio codec settings
        if FFMPEG_CONFIG_JSON['ignore_audio'] or FFMPEG_CONFIG_JSON['audio_codec'] is None:
            cmd.extend(['-an'])
        elif FFMPEG_CONFIG_JSON['audio_codec'] == 'copy':
            cmd.extend(['-c:a', 'copy'])
        else:
            cmd.extend([
                '-c:a', FFMPEG_CONFIG_JSON['audio_codec'],
                '-b:a', FFMPEG_CONFIG_JSON['audio_bitrate']
            ])

        # Add output path
        cmd.append(str(output_path))
        
        process = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True
        )

    def convert_video_python_ffmpeg(self, input_path, output_path, FFMPEG_CONFIG_JSON):
        """Use ffmpeg-python library"""
        try:
            import ffmpeg
        except ImportError:
            raise ImportError("ffmpeg-python is not installed. Please install it with: pip install ffmpeg-python")

        # Start building the ffmpeg-python chain
        stream = ffmpeg.input(str(input_path))

        # Build stream arguments based on config
        stream_args = {}
        
        # Video settings if not None
        if FFMPEG_CONFIG_JSON['video_codec'] is not None:
            if FFMPEG_CONFIG_JSON['video_codec'] != 'copy':
                stream_args['vcodec'] = FFMPEG_CONFIG_JSON['video_codec']
                
                if FFMPEG_CONFIG_JSON['preset'] is not None:
                    stream_args['preset'] = FFMPEG_CONFIG_JSON['preset']
                
                # Add width and height if specified
                if FFMPEG_CONFIG_JSON['width'] and FFMPEG_CONFIG_JSON['height']:
                    stream = ffmpeg.filter(stream, 'scale', 
                        w=FFMPEG_CONFIG_JSON['width'], 
                        h=FFMPEG_CONFIG_JSON['height'])
                
                if FFMPEG_CONFIG_JSON['video_bitrate']:
                    stream_args['video_bitrate'] = FFMPEG_CONFIG_JSON['video_bitrate']
                    
                if FFMPEG_CONFIG_JSON['force_fps'] > 0:
                    stream_args['crf'] = FFMPEG_CONFIG_JSON['crf']
                else:
                    stream_args['crf'] = 19
                
                if FFMPEG_CONFIG_JSON['pixel_format'] is not None:
                    stream_args['pix_fmt'] = FFMPEG_CONFIG_JSON['pixel_format']
                
                if FFMPEG_CONFIG_JSON['force_fps'] > 0:
                    stream_args['r'] = FFMPEG_CONFIG_JSON['force_fps']
            else:
                stream_args['vcodec'] = 'copy'

        # Audio settings
        if FFMPEG_CONFIG_JSON['ignore_audio'] or FFMPEG_CONFIG_JSON['audio_codec'] is None:
            stream_args['an'] = None
        elif FFMPEG_CONFIG_JSON['audio_codec'] == 'copy':
            stream_args['acodec'] = 'copy'
        else:
            stream_args.update({
                'acodec': FFMPEG_CONFIG_JSON['audio_codec'],
                'audio_bitrate': FFMPEG_CONFIG_JSON['audio_bitrate']
            })

        # Run the ffmpeg operation
        stream = ffmpeg.output(stream, str(output_path), **stream_args, y=None)
        stream.run()

    def convert_video(self, video_path: str, output_filename: str, FFMPEG_CONFIG_JSON: str = None, use_python_ffmpeg: bool = False):
        """
        Convert a video using either subprocess or python-ffmpeg based on config.
        If no configuration is provided, uses default configuration.
        """
        # Use default configuration if no JSON is provided
        if FFMPEG_CONFIG_JSON is None:
            default_config = self.get_default_config()
            config_json = {
                'ffmpeg': {
                    'path': default_config['ffmpeg_path']
                },
                'video': {
                    'codec': default_config['video_codec'],
                    'bitrate': default_config['video_bitrate'],
                    'preset': default_config['preset'],
                    'pixel_format': default_config['pixel_format'],
                    'crf': default_config['crf'],
                    'fps': {
                        'force_fps': default_config['force_fps']
                    },
                    'resolution': None if default_config['width'] == 0 or default_config['height'] == 0 else {
                        'width': default_config['width'],
                        'height': default_config['height']
                    }
                },
                'output': {
                    'container_format': default_config['container_format']
                },
                'audio': {
                    'enabled': not default_config['ignore_audio'],
                    'codec': default_config['audio_codec'],
                    'bitrate': default_config['audio_bitrate']
                }
            }
            FFMPEG_CONFIG_JSON = json.dumps(config_json)
        
        # Parse the JSON configuration
        FFMPEG_CONFIG_JSON = self.parse_config_json(FFMPEG_CONFIG_JSON)
        
        # Validate input path
        input_path = Path(os.path.abspath(video_path))
        if not input_path.exists():
            raise ValueError(f"Input video path does not exist: {input_path}")
        
        # Set output path
        if FFMPEG_CONFIG_JSON['container_format']:
            output_filename = Path(output_filename).with_suffix(f".{FFMPEG_CONFIG_JSON['container_format']}")
        output_path = self.output_dir / output_filename
        output_path = output_path.absolute()
        
        # Construct FFmpeg command for command string return
        cmd = [
            FFMPEG_CONFIG_JSON['ffmpeg_path'], '-y',
            '-i', str(input_path)
        ]
        # Add video codec settings if not None
        if FFMPEG_CONFIG_JSON['video_codec'] is not None:
            if FFMPEG_CONFIG_JSON['video_codec'] == 'copy':
                cmd.extend(['-c:v', 'copy'])
            else:
                cmd.extend(['-c:v', FFMPEG_CONFIG_JSON['video_codec']])
                
                if FFMPEG_CONFIG_JSON['preset'] is not None:
                    cmd.extend(['-preset', FFMPEG_CONFIG_JSON['preset']])
                
                if 'resolution' in FFMPEG_CONFIG_JSON and FFMPEG_CONFIG_JSON['resolution'] is not None:
                    cmd.extend(['-vf', f'scale={FFMPEG_CONFIG_JSON["resolution"]["width"]}:{FFMPEG_CONFIG_JSON["resolution"]["height"]}'])
                
                if FFMPEG_CONFIG_JSON['video_bitrate']:
                    cmd.extend(['-b:v', FFMPEG_CONFIG_JSON['video_bitrate']])
                
                if FFMPEG_CONFIG_JSON['crf'] > 0:
                    cmd.extend(['-crf', str(FFMPEG_CONFIG_JSON['crf'])])
                else:
                    cmd.extend(['-crf', '19'])
                
                if FFMPEG_CONFIG_JSON['pixel_format'] is not None:
                    cmd.extend(['-pix_fmt', FFMPEG_CONFIG_JSON['pixel_format']])
                
                if FFMPEG_CONFIG_JSON['force_fps'] > 0:
                    cmd.extend(['-r', str(FFMPEG_CONFIG_JSON['force_fps'])])

            # Add audio codec settings
            if FFMPEG_CONFIG_JSON['ignore_audio'] or FFMPEG_CONFIG_JSON['audio_codec'] is None:
                cmd.extend(['-an'])
            elif FFMPEG_CONFIG_JSON['audio_codec'] == 'copy':
                cmd.extend(['-c:a', 'copy'])
            else:
                cmd.extend([
                    '-c:a', FFMPEG_CONFIG_JSON['audio_codec'],
                    '-b:a', FFMPEG_CONFIG_JSON['audio_bitrate']
                ])

            cmd.append(str(output_path))
        
        # Convert command list to string
        ffmpeg_command = ' '.join(cmd)
        
        try:
            if use_python_ffmpeg:
                self.convert_video_python_ffmpeg(input_path, output_path, FFMPEG_CONFIG_JSON)
            else:
                self.convert_video_subprocess(input_path, output_path, FFMPEG_CONFIG_JSON)
            
            return (str(output_path), ffmpeg_command)
            
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"FFmpeg error: {e.stderr}")
        except Exception as e:
            raise RuntimeError(f"Error during video conversion: {str(e)}")

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")
import os
import numpy as np
import torch
import subprocess
import json
from PIL import Image
import soundfile as sf
import glob
import logging

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
                "audio_path": ("STRING", {"forceInput": True}),
                "FFMPEG_CONFIG_JSON": ("STRING", {"forceInput": True}),
            },
        }

    RETURN_TYPES = ("STRING", "STRING","STRING",)
    RETURN_NAMES = ("comment", "ffmpeg_command", "video_path",)
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
        except ImportError:
            logging.error("ffmpeg-python library not installed")
            return False, "ffmpeg-python library not installed"

        try:
            # Find frame rate
            idx_fr = ffmpeg_cmd.index('-framerate')
            fps = ffmpeg_cmd[idx_fr + 1]

            # Find all input indices
            idx_inputs = [i for i, x in enumerate(ffmpeg_cmd) if x == '-i']
            if not idx_inputs:
                return False, "Error: No input found"

            # First input is the image sequence
            image_sequence = ffmpeg_cmd[idx_inputs[0] + 1]

            # Second input (if present) is the audio file
            audio_file = ffmpeg_cmd[idx_inputs[1] + 1] if len(idx_inputs) > 1 else None

            # Determine position after the last input
            idx_after = idx_inputs[-1] + 2

            # Check for video filter
            filter_graph = None
            output_options_start = idx_after
            if idx_after < len(ffmpeg_cmd) - 1 and ffmpeg_cmd[idx_after] == '-vf':
                filter_graph = ffmpeg_cmd[idx_after + 1]
                output_options_start = idx_after + 2

            # Extract output options (everything between last input/filter and output file)
            output_options = ffmpeg_cmd[output_options_start:-1]
            if len(output_options) % 2 != 0:
                return False, "Error: Output options have odd number of elements"

            # Convert output options to a dictionary, preserving colons
            options = {}
            for i in range(0, len(output_options), 2):
                key = output_options[i].lstrip('-')  # Remove '-' but keep ':'
                value = output_options[i + 1]
                options[key] = value

            # Add filter graph to options if present
            if filter_graph:
                options['vf'] = filter_graph

            # Create video input
            video_input = ffmpeg.input(image_sequence, framerate=fps)
            video_stream = video_input.video

            # Create audio input if present
            audio_stream = None
            if audio_file:
                audio_input = ffmpeg.input(audio_file)
                audio_stream = audio_input.audio

            # Construct output
            if audio_stream:
                output = ffmpeg.output(video_stream, audio_stream, output_file, **options)
            else:
                output = ffmpeg.output(video_stream, output_file, **options)

            # Execute FFmpeg command
            output.run(cmd=ffmpeg_path, overwrite_output=True)
            logging.debug(f"FFmpeg-python executed successfully for {output_file}")
            return True, "Success"

        except ffmpeg.Error as e:
            error_message = "Unknown FFmpeg error"
            if hasattr(e, 'stderr') and e.stderr is not None:
                try:
                    error_message = e.stderr.decode(errors='replace')
                except Exception as decode_err:
                    error_message = f"Could not decode stderr: {decode_err}"
            logging.error(f"FFmpeg-python failed: {error_message}\nCommand: {' '.join(ffmpeg_cmd)}")
            return False, f"FFmpeg error: {error_message}\nCommand: {' '.join(ffmpeg_cmd)}"
        except Exception as e:
            logging.error(f"Unexpected error in FFmpeg-python: {str(e)}")
            return False, f"Error: {str(e)}"
    
    def get_next_filename(self, output_base, format="mp4"):
        """
        Determines the next filename in a sequence with 4-digit numbering (0001, 0002, etc.).
        
        Args:
            output_base (str): The base path and prefix (e.g., 'output/imgs2video/me')
            format (str): The file extension (e.g., 'mp4')
        
        Returns:
            str: The next filename in the sequence (e.g., 'output/imgs2video/me_0001.mp4')
        """
        # Ensure output_base is clean
        output_base = output_base.rstrip(os.sep)
        
        # Pattern to match files with 4-digit numbers: e.g., 'output/imgs2video/me_0001.mp4'
        pattern = f"{output_base}_[0-9][0-9][0-9][0-9].{format}"
        
        # Get all files matching the pattern
        existing_files = glob.glob(pattern)
        
        # Extract numbers from filenames
        numbers = []
        for filepath in existing_files:
            # Get the filename from the full path
            filename = os.path.basename(filepath)
            # Extract the 4-digit number between '_' and '.'
            number_part = filename.split('_')[-1].split('.')[0]
            # Verify it's a 4-digit number
            if number_part.isdigit() and len(number_part) == 4:
                numbers.append(int(number_part))
        
        # Determine the next number
        if numbers:
            next_num = max(numbers) + 1
        else:
            next_num = 1
        
        # Construct the next filename with zero-padding to 4 digits
        next_filename = f"{output_base}_{next_num:04d}.{format}"
        
        return next_filename

    def image_to_video(self, images, fps, name_prefix, use_python_ffmpeg=False, audio=None, audio_path=None, FFMPEG_CONFIG_JSON=None):
        ffmpeg_config = self.parse_ffmpeg_config(FFMPEG_CONFIG_JSON)
        
        format = "mp4"
        if ffmpeg_config and ffmpeg_config["output"]["container_format"] != "None":
            format = ffmpeg_config["output"]["container_format"]
        
        # Remove any extension from name_prefix and create output_base
        name_prefix = os.path.splitext(name_prefix)[0]
        output_base = os.path.join("output", name_prefix)
        
        # Get the next filename using the corrected function
        output_file = self.get_next_filename(output_base, format)
        
        # Clean up and prepare temporary directory
        temp_dir = os.path.join("Bjornulf", "temp_images_imgs2video")  # Use os.path.join for cross-platform compatibility
        if os.path.exists(temp_dir) and os.path.isdir(temp_dir):
            for file in os.listdir(temp_dir):
                os.remove(os.path.join(temp_dir, file))
            os.rmdir(temp_dir)
        
        # Create necessary directories
        os.makedirs(temp_dir, exist_ok=True)
        os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else ".", exist_ok=True)
        
        for i, img_tensor in enumerate(images):
            img = Image.fromarray((img_tensor.cpu().numpy() * 255).astype(np.uint8))
            if format == "webm":
                img = img.convert("RGBA")
            img.save(os.path.join(temp_dir, f"frame_{i:04d}.png"))

        # Handle audio from either AUDIO type or audio_path
        temp_audio_file = None
        # Always use audio if either audio or audio_path is provided
        # logging.info(f"audio : {audio}")
        # logging.info(f"audio_path : {audio_path}")
        audio_enabled = (audio is not None) or (audio_path is not None and os.path.exists(audio_path))
        # logging.info(f"audio_enabled : {audio_enabled}")

        if audio_enabled:
            if audio is not None:
                # Process AUDIO type input
                temp_audio_file = os.path.join(temp_dir, "temp_audio.wav")
                waveform = audio['waveform'].squeeze().numpy()
                sample_rate = audio['sample_rate']
                sf.write(temp_audio_file, waveform, sample_rate)
            elif audio_path and os.path.exists(audio_path):
                # Use provided audio path directly
                temp_audio_file = audio_path

        ffmpeg_path = "ffmpeg"
        if ffmpeg_config and ffmpeg_config["ffmpeg"]["path"]:
            ffmpeg_path = ffmpeg_config["ffmpeg"]["path"]

        ffmpeg_cmd = [
            ffmpeg_path,
            "-y",
            "-framerate", str(fps),
            "-i", os.path.join(temp_dir, "frame_%04d.png"),
        ]

        # logging.info(f"temp_audio_file : {temp_audio_file}")
        if temp_audio_file:
            ffmpeg_cmd.extend(["-i", temp_audio_file])

        if ffmpeg_config and format == "webm" and ffmpeg_config["video"]["force_transparency_webm"]:
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
                if format == "webm" and ffmpeg_config["video"]["force_transparency_webm"]:
                    current_filter_idx = ffmpeg_cmd.index("-vf") + 1
                    current_filter = ffmpeg_cmd[current_filter_idx]
                    ffmpeg_cmd[current_filter_idx] = scale_filter + "," + current_filter
                else:
                    ffmpeg_cmd.extend(["-vf", scale_filter])
            
            if ffmpeg_config["video"]["fps"]["enabled"]:
                ffmpeg_cmd.extend(["-r", str(ffmpeg_config["video"]["fps"]["force_fps"])])
            
            # if not ffmpeg_config["audio"]["enabled"]:
            #     ffmpeg_cmd.extend(["-an"])
            # elif ffmpeg_config["audio"]["codec"] != "None" and temp_audio_file:
            #  ffmpeg_config["audio"]["codec"] != "None" and
            #Need codec ????
            if temp_audio_file:
                # Check if we have ffmpeg_config with audio codec settings
                if ffmpeg_config and "audio" in ffmpeg_config and ffmpeg_config["audio"]["codec"] != "None":
                    ffmpeg_cmd.extend(["-c:a", ffmpeg_config["audio"]["codec"]])
                    if "bitrate" in ffmpeg_config["audio"] and ffmpeg_config["audio"]["bitrate"]:
                        ffmpeg_cmd.extend(["-b:a", ffmpeg_config["audio"]["bitrate"]])
                else:
                    # Use default audio codec based on format if no specific codec is set
                    if format == "mp4":
                        ffmpeg_cmd.extend(["-c:a", "aac"])
                    elif format == "webm":
                        ffmpeg_cmd.extend(["-c:a", "libvorbis"])
            else:
                ffmpeg_cmd.extend(["-an"])  # No audio
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
                    "-crf", "19",
                    # "-b:v", "0",
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
            # Only remove temp_audio_file if it was created here (not if it's an external path)
            if temp_audio_file and audio_path != temp_audio_file:
                print("Temporary files not removed for debugging purposes.")
                
        # Generate configuration report
        comment_lines = []
        comment_lines.append("📽 Video Generation Configuration Report 📽\n")

        # Quick format overview based on selected format
        if format.lower() == "mp4":
            comment_lines.append("MP4 FORMAT OVERVIEW:")
            comment_lines.append("✅ Advantages: Universal compatibility, excellent streaming support")
            comment_lines.append("❌ Drawbacks: No transparency support, less efficient than newer formats")
            comment_lines.append("🏆 Best for: General distribution, web streaming, maximum device compatibility\n")
        elif format.lower() == "webm":
            comment_lines.append("WEBM FORMAT OVERVIEW:")
            comment_lines.append("✅ Advantages: Better compression efficiency, transparency support, open format")
            comment_lines.append("❌ Drawbacks: Limited compatibility on older devices/iOS, slower encoding")
            comment_lines.append("🏆 Best for: Web delivery, animations with transparency, modern browsers\n")
        elif format.lower() == "mov":
            comment_lines.append("MOV FORMAT OVERVIEW:")
            comment_lines.append("✅ Advantages: Professional codec support, good for editing workflows, Apple ecosystem")
            comment_lines.append("❌ Drawbacks: Larger file sizes, less web-friendly")
            comment_lines.append("🏆 Best for: Professional workflows, Mac/iOS delivery, intermediate editing files\n")
        elif format.lower() == "mkv":
            comment_lines.append("MKV FORMAT OVERVIEW:")
            comment_lines.append("✅ Advantages: Superior flexibility, supports all codecs, multiple audio/subtitle tracks")
            comment_lines.append("❌ Drawbacks: Not viewable in browsers, limited device support")
            comment_lines.append("🏆 Best for: Archiving, local playback, advanced feature support\n")
        elif format.lower() == "gif":
            comment_lines.append("GIF FORMAT OVERVIEW:")
            comment_lines.append("✅ Advantages: Universal compatibility, simple animation support")
            comment_lines.append("❌ Drawbacks: Extremely inefficient compression, limited to 256 colors, no audio")
            comment_lines.append("🏆 Best for: Simple animations, maximum compatibility\n")

        # Basic parameters section
        comment_lines.append("=== Core Parameters ===")
        comment_lines.append(f"• FPS: {fps} ({24 if fps == 24 else 'custom'} fps)")
        if fps == 24:
            comment_lines.append("  ℹ️ 24 fps is the cinema standard, offering a classic film look")
        elif fps == 30:
            comment_lines.append("  ℹ️ 30 fps provides smoother motion for general video content")
        elif fps == 60:
            comment_lines.append("  ℹ️ 60 fps delivers very smooth motion ideal for gaming/sports")
        elif fps > 60:
            comment_lines.append("  ℹ️ High frame rate (>60 fps) used for slow-motion effects")
        comment_lines.append(f"  📊 Valid range: 1-120 fps (Higher values increase file size significantly)")

        comment_lines.append(f"• Output Naming: '{name_prefix}'")
        comment_lines.append(f"  📁 Full path: {output_file}")

        comment_lines.append(f"• Execution Mode: {'Python ffmpeg' if use_python_ffmpeg else 'System FFmpeg'}")
        if use_python_ffmpeg:
            comment_lines.append("  ℹ️ Python FFmpeg: Integrated library approach with cleaner error handling")
            comment_lines.append("  ⚠️ May have fewer codec options than system FFmpeg")
            comment_lines.append("  💡 For next improvement: Switch to system FFmpeg for access to more codecs and options")
        else:
            comment_lines.append("  ℹ️ System FFmpeg: Direct shell access with full codec/options support")
            comment_lines.append("  ⚠️ Requires FFmpeg to be installed and in system PATH")

        # Video configuration section
        comment_lines.append("\n=== Video Encoding Configuration ===")
        if ffmpeg_config:
            comment_lines.append("🔧 Custom Configuration Active")
            v = ffmpeg_config.get('video', {})
            
            default_codec = "libx264"
            # Codec information
            if format.lower() == "webm":
                default_codec = "libvpx-vp9"
            
            codec = v.get('codec', default_codec)
            comment_lines.append(f"• Codec: {codec}")
            
            if "264" in codec:
                comment_lines.append("  ℹ️ H.264/AVC: Universal compatibility, good balance of quality and size")
                comment_lines.append("  ⭐ Quality: 8/10 | Compatibility: 10/10 | Encoding Speed: 7/10")
                comment_lines.append("  💡 For next improvement: Consider H.265/HEVC for 20-30% better compression at same quality")
            elif "265" in codec in codec.lower():
                comment_lines.append("  ℹ️ H.265/HEVC: Better compression than H.264, but slower encoding")
                comment_lines.append("  ⭐ Quality: 9/10 | Compatibility: 6/10 | Encoding Speed: 5/10")
                comment_lines.append("  ⚠️ Limited browser/device support, best for archiving")
                comment_lines.append("  💡 For next improvement: Try AV1 for even better compression")
            elif "vp9" in codec.lower():
                comment_lines.append("  ℹ️ VP9: Google's open codec with excellent quality-to-size ratio")
                comment_lines.append("  ⭐ Quality: 9/10 | Compatibility: 7/10 | Encoding Speed: 4/10")
                comment_lines.append("  ✅ Good support in modern browsers, especially Chrome")
                comment_lines.append("  💡 For next improvement: Consider AV1 for 20% better compression or faster encoding preset")
            elif "av1" in codec.lower():
                comment_lines.append("  ℹ️ AV1: Next-gen open codec with superior compression")
                comment_lines.append("  ⭐ Quality: 10/10 | Compatibility: 5/10 | Encoding Speed: 2/10")
                comment_lines.append("  ⚠️ Very slow encoding, requires modern hardware")
                comment_lines.append("  💡 For next improvement: Use SVT-AV1 encoder for faster processing")
            
            # Quality parameters
            crf = v.get('crf', 19)
            comment_lines.append(f"• Quality: CRF {crf}")
            
            if crf != 'N/A':
                if 0 <= int(crf) <= 14:
                    comment_lines.append("  ℹ️ Very High Quality (CRF 0-14): Nearly lossless, very large files")
                    comment_lines.append("  ⭐ Visual Quality: 9-10/10 | File Size: Very Large")
                elif 15 <= int(crf) <= 19:
                    comment_lines.append("  ℹ️ High Quality (CRF 15-19): Visually transparent, good for archiving")
                    comment_lines.append("  ⭐ Visual Quality: 8-9/10 | File Size: Large")
                    comment_lines.append("  💡 For next improvement: Lower CRF to 17 for even better quality")
                elif 20 <= int(crf) <= 24:
                    comment_lines.append("  ℹ️ Balanced Quality (CRF 20-24): Good for general distribution")
                    comment_lines.append("  ⭐ Visual Quality: 7-8/10 | File Size: Moderate")
                    comment_lines.append("  💡 For next improvement: Lower CRF to 18 for higher quality or switch to H.265 at same CRF")
                elif 25 <= int(crf) <= 30:
                    comment_lines.append("  ℹ️ Reduced Quality (CRF 25-30): Noticeable compression artifacts")
                    comment_lines.append("  ⭐ Visual Quality: 5-6/10 | File Size: Small")
                    comment_lines.append("  💡 For next improvement: Lower CRF to 22 for better quality-size balance")
                else:
                    comment_lines.append("  ℹ️ Low Quality (CRF 31+): Heavy compression, significant artifacts")
                    comment_lines.append("  ⭐ Visual Quality: <5/10 | File Size: Very Small")
                    comment_lines.append("  💡 For next improvement: Use CRF 28 for better quality with minimal size increase")
            
            comment_lines.append("  ⚠️ Cannot combine CRF with static bitrate settings")
            
            # Encoding speed/preset
            preset = v.get('preset', 'medium')
            comment_lines.append(f"• Performance: {preset} preset")
            
            if preset == 'ultrafast':
                comment_lines.append("  ℹ️ Ultrafast: Maximum encoding speed, largest file size")
                comment_lines.append("  ⏱️ Speed: 10/10 | Efficiency: 3/10 | Use case: Live streaming")
                comment_lines.append("  💡 For next improvement: Try 'superfast' for 30% better compression with minimal speed loss")
            elif preset == 'superfast' or preset == 'veryfast':
                comment_lines.append("  ℹ️ Very Fast: Quick encoding, larger file sizes")
                comment_lines.append("  ⏱️ Speed: 8-9/10 | Efficiency: 4-5/10 | Use case: Quick exports")
                comment_lines.append("  💡 For next improvement: Try 'slower' preset for better compression")
            elif preset == 'faster' or preset == 'fast':
                comment_lines.append("  ℹ️ Fast: Good balance of speed and compression")
                comment_lines.append("  ⏱️ Speed: 6-7/10 | Efficiency: 6-7/10 | Use case: General purpose")
                comment_lines.append("  💡 For next improvement: Consider 'veryslow' preset for better compression")
            elif preset == 'medium':
                comment_lines.append("  ℹ️ Medium: Default preset, balanced speed/compression")
                comment_lines.append("  ⏱️ Speed: 5/10 | Efficiency: 7/10 | Use case: Standard encoding")
                comment_lines.append("  💡 For next improvement: Try 'veryslow' preset for 15-20% better compression")
            elif preset == 'slow' or preset == 'slower':
                comment_lines.append("  ℹ️ Slow: Better compression, slower encoding")
                comment_lines.append("  ⏱️ Speed: 3-4/10 | Efficiency: 8-9/10 | Use case: Distribution/archiving")
                comment_lines.append("  💡 For next improvement: Try 'veryslow' for archival quality or reduce CRF slightly")
            elif preset == 'veryslow' or preset == 'placebo':
                comment_lines.append("  ℹ️ Very Slow: Maximum compression, extremely slow encoding")
                comment_lines.append("  ⏱️ Speed: 1-2/10 | Efficiency: 9-10/10 | Use case: Final archiving")
            
            # Bitrate information
            bitrate = v.get('bitrate', 'Auto')
            comment_lines.append(f"• Bitrate: {bitrate}")
            
            if bitrate == 'Auto':
                comment_lines.append("  ℹ️ Auto Bitrate: Determined by CRF value (recommended)")
            else:
                comment_lines.append(f"  ℹ️ Fixed Bitrate: {bitrate}")
                comment_lines.append("  ⚠️ Fixed bitrate overrides quality-based settings (CRF)")
                
                # Rough bitrate quality indicators
                if isinstance(bitrate, str):
                    bitrate_value = int(''.join(filter(str.isdigit, bitrate)))
                    if 'k' in bitrate.lower():
                        bitrate_value *= 1000
                    
                    if bitrate_value < 1000000:
                        comment_lines.append("  ⭐ Quality: Low (< 1 Mbps) - Suitable for mobile/web previews")
                        comment_lines.append("  💡 For next improvement: Increase to at least 2-3 Mbps for SD content")
                    elif 1000000 <= bitrate_value < 5000000:
                        comment_lines.append("  ⭐ Quality: Medium (1-5 Mbps) - Standard web video")
                        comment_lines.append("  💡 For next improvement: Use 5-8 Mbps for higher quality HD content")
                    elif 5000000 <= bitrate_value < 10000000:
                        comment_lines.append("  ⭐ Quality: High (5-10 Mbps) - HD streaming")
                        comment_lines.append("  💡 For next improvement: Consider two-pass encoding for consistent quality")
                    elif 10000000 <= bitrate_value < 20000000:
                        comment_lines.append("  ⭐ Quality: Very High (10-20 Mbps) - Full HD premium content")
                        comment_lines.append("  💡 For next improvement: Switch to CRF-based encoding for more efficient sizing")
                    else:
                        comment_lines.append("  ⭐ Quality: Ultra High (20+ Mbps) - 4K/professional use")
            
            # Pixel format details
            pixel_format = v.get('pixel_format', 'yuv420p/yuva420p')
            comment_lines.append(f"• Pixel Format: {pixel_format}")
            
            if '420' in pixel_format:
                comment_lines.append("  ℹ️ YUV 4:2:0: Standard chroma subsampling, best compatibility")
                comment_lines.append("  ✅ Recommended for most content")
                comment_lines.append("  💡 For next improvement: Consider 4:2:2 for professional content or chroma keying")
            elif '422' in pixel_format:
                comment_lines.append("  ℹ️ YUV 4:2:2: Better color accuracy, larger files")
                comment_lines.append("  ✅ Good for professional content/chroma keying")
                comment_lines.append("  💡 For next improvement: Use 4:4:4 for graphic design work or precision color grading")
            elif '444' in pixel_format:
                comment_lines.append("  ℹ️ YUV 4:4:4: Full chroma resolution, largest files")
                comment_lines.append("  ✅ Best for high-end professional work")
            
            if 'a' in pixel_format:
                comment_lines.append("  ℹ️ Alpha channel support active (transparency)")
                comment_lines.append("  ⚠️ Only supported in WebM (VP8/VP9) and some MOV containers")
                comment_lines.append("  💡 For next improvement: Use VP9 for better quality transparency")
            
            # Resolution information
            if v.get('resolution'):
                width = v['resolution']['width']
                height = v['resolution']['height']
                comment_lines.append(f"• Resolution: {width}x{height}")
                
                # Add resolution category information
                if width >= 3840 or height >= 2160:
                    comment_lines.append("  ℹ️ 4K Ultra HD (3840×2160 or higher)")
                    comment_lines.append("  ⚠️ Very large files, may require powerful hardware to play")
                    comment_lines.append("  💡 For next improvement: Try 1440p (2560×1440) for better balance of quality and size")
                elif width >= 1920 or height >= 1080:
                    comment_lines.append("  ℹ️ Full HD (1920×1080)")
                    comment_lines.append("  ✅ Standard for high-quality video")
                    comment_lines.append("  💡 For next improvement: Consider H.265/HEVC codec for better compression at this resolution")
                elif width >= 1280 or height >= 720:
                    comment_lines.append("  ℹ️ HD (1280×720)")
                    comment_lines.append("  ✅ Good balance of quality and file size")
                    comment_lines.append("  💡 For next improvement: Upgrade to 1080p for higher quality or lower CRF")
                elif width >= 854 or height >= 480:
                    comment_lines.append("  ℹ️ SD (854×480 or similar)")
                    comment_lines.append("  ✅ Suitable for mobile devices or low bandwidth")
                    comment_lines.append("  💡 For next improvement: Increase to 720p for better viewing experience")
                else:
                    comment_lines.append("  ℹ️ Low Resolution (< 480p)")
                    comment_lines.append("  ⚠️ May appear pixelated on modern displays")
                    comment_lines.append("  💡 For next improvement: Increase to at least 480p for acceptable quality")
            
            # Container format detailed information
            comment_lines.append(f"• Container: {format.upper()}")
        else:
            comment_lines.append(f"🔄 Default {format.upper()} Configuration:")
            comment_lines.append("• Codec: " + ("libx264" if format == "mp4" else "libvpx-vp9"))
            comment_lines.append("• CRF: 19")
            comment_lines.append("• Preset: medium" + (" (slow for VP9)" if format == "webm" else ""))
            comment_lines.append("  💡 For next improvement: Lower CRF to 16-18 for better quality")

        # Container format information
        comment_lines.append("\n=== Container Format Details ===")
        if format.lower() == "mp4":
            comment_lines.append("• MP4 (.mp4)")
            comment_lines.append("  ℹ️ Universal compatibility with nearly all devices and platforms")
            comment_lines.append("  ✅ Excellent for web, mobile, and general distribution")
            comment_lines.append("  ✅ Supports H.264, H.265, AAC audio")
            comment_lines.append("  ❌ Limited support for transparency")
            comment_lines.append("  ⭐ Compatibility: 10/10 | Flexibility: 7/10")
            comment_lines.append("  💡 For next improvement: Consider H.265 in MP4 for 30% smaller files")
        elif format.lower() == "webm":
            comment_lines.append("• WebM (.webm)")
            comment_lines.append("  ℹ️ Open format optimized for web delivery")
            comment_lines.append("  ✅ Excellent support in modern browsers")
            comment_lines.append("  ✅ Native support for transparency (alpha channel)")
            comment_lines.append("  ✅ Supports VP8/VP9 video, Vorbis/Opus audio")
            comment_lines.append("  ❌ Limited support on older devices/iOS")
            comment_lines.append("  ⭐ Compatibility: 7/10 | Web Performance: 9/10")
            comment_lines.append("  💡 For next improvement: Try AV1 in WebM for better quality/size ratio")
        elif format.lower() == "mov":
            comment_lines.append("• QuickTime (.mov)")
            comment_lines.append("  ℹ️ Apple's native container format")
            comment_lines.append("  ✅ Excellent for macOS/iOS ecosystem")
            comment_lines.append("  ✅ Good support for professional codecs (ProRes, DNxHD)")
            comment_lines.append("  ✅ Can support transparency")
            comment_lines.append("  ❌ Less compatible outside Apple ecosystem")
            comment_lines.append("  ⭐ Compatibility: 6/10 | Professional Use: 8/10")
            comment_lines.append("  💡 For next improvement: Use ProRes 422 for editing workflows or H.264 for delivery")
        elif format.lower() == "mkv":
            comment_lines.append("• Matroska (.mkv)")
            comment_lines.append("  ℹ️ Highly flexible open container format")
            comment_lines.append("  ✅ Supports virtually all codecs and features")
            comment_lines.append("  ✅ Excellent for archiving and local playback")
            comment_lines.append("  ✅ Supports multiple audio/subtitle tracks")
            comment_lines.append("  ❌ Not natively supported in browsers or some devices")
            comment_lines.append("  ⚠️ Cannot be viewed directly in web browsers")
            comment_lines.append("  ⭐ Compatibility: 5/10 | Flexibility: 10/10")
            comment_lines.append("  💡 For next improvement: Use H.265 or AV1 codec inside MKV for best archival quality")
        elif format.lower() == "gif":
            comment_lines.append("• GIF (.gif)")
            comment_lines.append("  ℹ️ Simple animated image format")
            comment_lines.append("  ✅ Universal compatibility across all platforms")
            comment_lines.append("  ✅ Supports basic transparency")
            comment_lines.append("  ❌ Limited to 256 colors, no audio")
            comment_lines.append("  ❌ Very inefficient compression (large files)")
            comment_lines.append("  ⭐ Compatibility: 10/10 | Quality: 2/10")
            comment_lines.append("  💡 For next improvement: Use WebM or MP4 with autoplay for much better quality/size")

        # Audio configuration section
        comment_lines.append("\n=== Audio Configuration ===")
        if audio_enabled:
            comment_lines.append(f"• Audio Source: {'Direct input' if audio else 'External file'}")
            if ffmpeg_config and ffmpeg_config.get('audio'):
                a = ffmpeg_config['audio']
                codec = a.get('codec', 'AAC/Vorbis')
                comment_lines.append(f"• Codec: {codec}")
                
                if 'aac' in codec.lower():
                    comment_lines.append("  ℹ️ AAC: High-quality lossy compression, excellent compatibility")
                    comment_lines.append("  ⭐ Quality: 8/10 | Compatibility: 10/10")
                    comment_lines.append("  💡 For next improvement: Use higher bitrate (192+ kbps) or switch to Opus for better quality")
                elif 'opus' in codec.lower():
                    comment_lines.append("  ℹ️ Opus: Modern codec with superior quality at low bitrates")
                    comment_lines.append("  ⭐ Quality: 9/10 | Compatibility: 7/10")
                    comment_lines.append("  💡 For next improvement: Fine-tune VBR settings or increase bitrate by 10-20%")
                elif 'vorbis' in codec.lower():
                    comment_lines.append("  ℹ️ Vorbis: Open audio codec, good quality-to-size ratio")
                    comment_lines.append("  ⭐ Quality: 7/10 | Compatibility: 8/10")
                    comment_lines.append("  💡 For next improvement: Switch to Opus for better quality at same bitrate")
                elif 'mp3' in codec.lower():
                    comment_lines.append("  ℹ️ MP3: Widely compatible but older codec technology")
                    comment_lines.append("  ⭐ Quality: 6/10 | Compatibility: 10/10")
                    comment_lines.append("  💡 For next improvement: Switch to AAC for better quality at same bitrate")
                elif 'flac' in codec.lower() or 'alac' in codec.lower():
                    comment_lines.append("  ℹ️ FLAC/ALAC: Lossless audio compression")
                    comment_lines.append("  ⭐ Quality: 10/10 | Compatibility: 6/10 | File Size: Large")
                
                bitrate = a.get('bitrate', 'Default')
                comment_lines.append(f"• Bitrate: {bitrate}")
                
                # Audio bitrate quality indicators
                if bitrate != 'Default':
                    if isinstance(bitrate, str):
                        bitrate_value = int(''.join(filter(str.isdigit, bitrate)))
                        if 'k' in bitrate.lower():
                            bitrate_value *= 1000
                        
                        if bitrate_value < 96000:
                            comment_lines.append("  ℹ️ Low Bitrate (<96 kbps): Basic audio quality")
                            comment_lines.append("  ⭐ Quality: 4/10 | Use case: Voice/basic audio")
                            comment_lines.append("  💡 For next improvement: Increase to at least 128 kbps for music or 96 kbps for speech")
                        elif 96000 <= bitrate_value < 128000:
                            comment_lines.append("  ℹ️ Standard Bitrate (96-128 kbps): Acceptable quality")
                            comment_lines.append("  ⭐ Quality: 6/10 | Use case: General purpose")
                            comment_lines.append("  💡 For next improvement: Use 160-192 kbps for better music quality")
                        elif 128000 <= bitrate_value < 192000:
                            comment_lines.append("  ℹ️ Good Bitrate (128-192 kbps): Good quality")
                            comment_lines.append("  ⭐ Quality: 7/10 | Use case: Music/general media")
                            comment_lines.append("  💡 For next improvement: Use 192-256 kbps for higher quality music")
                        elif 192000 <= bitrate_value < 256000:
                            comment_lines.append("  ℹ️ High Bitrate (192-256 kbps): Near transparent")
                            comment_lines.append("  ⭐ Quality: 8/10 | Use case: Music distribution")
                            comment_lines.append("  💡 For next improvement: Consider VBR encoding for more efficient size/quality")
                        else:
                            comment_lines.append("  ℹ️ Very High Bitrate (256+ kbps): Transparent quality")
                            comment_lines.append("  ⭐ Quality: 9-10/10 | Use case: Archiving/professional")
                else:
                    comment_lines.append("  ℹ️ Default bitrate selected based on codec")
                    comment_lines.append("  ✅ Typically 128-192 kbps for lossy formats")
                    comment_lines.append("  💡 For next improvement: Specify 192-256 kbps for music content")
            else:
                comment_lines.append("• Codec: " + ("AAC" if format == "mp4" else "Vorbis"))
                if format == "mp4":
                    comment_lines.append("  ℹ️ AAC: Standard audio codec for MP4 with excellent quality")
                    comment_lines.append("  ⭐ Quality: 8/10 at default bitrate (128-192 kbps)")
                    comment_lines.append("  💡 For next improvement: Set explicit bitrate of 192 kbps for better quality")
                else:
                    comment_lines.append("  ℹ️ Vorbis: Open audio codec with good compression efficiency")
                    comment_lines.append("  ⭐ Quality: 7/10 at default bitrate (128 kbps)")
                    comment_lines.append("  💡 For next improvement: Switch to Opus codec for better quality at same bitrate")
        else:
            comment_lines.append("• Audio: Disabled")
            comment_lines.append("  ℹ️ No audio track will be included in the output file")
            comment_lines.append("  ✅ Results in smaller file size")
            comment_lines.append("  💡 For next improvement: Add audio if applicable to content")

        # Advanced features with detailed explanations
        comment_lines.append("\n=== Advanced Features ===")

        # Transparency handling
        transparency_enabled = format == 'webm' and ffmpeg_config and ffmpeg_config['video'].get('force_transparency_webm', False)
        comment_lines.append(f"• Transparency Handling: {'Enabled' if transparency_enabled else 'Disabled'}")

        if transparency_enabled:
            comment_lines.append("  ℹ️ Alpha channel (transparency) will be preserved")
            comment_lines.append("  ✅ WebM with VP9 codec provides excellent transparency support")
            comment_lines.append("  ⚠️ Requires 'yuva420p' pixel format")
            comment_lines.append("  ⚠️ Increases file size by approximately 33%")
            comment_lines.append("  💡 For next improvement: Ensure original content has high-quality alpha channel")
        else:
            if format == 'webm':
                comment_lines.append("  ℹ️ Transparency can be enabled for WebM format")
                comment_lines.append("  💡 For next improvement: Set 'force_transparency_webm: True' in ffmpeg_config to enable")
            elif format == 'mov':
                comment_lines.append("  ℹ️ MOV format can support transparency with certain codecs")
                comment_lines.append("  💡 For next improvement: Use ProRes 4444 or PNG codec for transparency in MOV")
            elif format == 'gif':
                comment_lines.append("  ℹ️ GIF supports basic binary transparency (on/off)")
                comment_lines.append("  💡 For next improvement: Use WebM for smooth alpha transparency")
            else:
                comment_lines.append("  ℹ️ Selected format does not support transparency")
                comment_lines.append("  💡 For next improvement: Use WebM format for web-compatible transparency")

        # Temp frames information
        comment_lines.append(f"• Temp Frames: {len(images)} images @ {temp_dir}")
        comment_lines.append(f"  ℹ️ Processing {len(images)} individual frames")
        if len(images) > 1000:
            comment_lines.append("  ⚠️ Large frame count (>1000): May require significant processing time")
            comment_lines.append(f"  💡 Estimated size: ~{len(images) * 0.2:.1f}MB temporary storage")
        comment_lines.append(f"  🗂️ Temporary directory: {temp_dir}")

        # Execution status
        try:
            # [Existing FFmpeg execution code...]
            comment_lines.append("\n=== Execution Status ===")
            comment_lines.append("✅ Success: Video created")
            comment_lines.append(f"  📁 Output: {output_file}")
            # comment_lines.append(f"  📊 Final file size: {"[Will be calculated after processing]"}")
            
            # Add estimated output quality based on settings
            if ffmpeg_config and ffmpeg_config.get('video'):
                v = ffmpeg_config['video']
                crf = v.get('crf')
                preset = v.get('preset', 'medium')
                codec = v.get('codec', '')
                
                quality_score = 0
                # Base quality on CRF
                if crf is not None:
                    if 0 <= int(crf) <= 14:
                        quality_score = 9.5
                    elif 15 <= int(crf) <= 19:
                        quality_score = 8.5
                    elif 20 <= int(crf) <= 24:
                        quality_score = 7.5
                    elif 25 <= int(crf) <= 30:
                        quality_score = 5.5
                    else:
                        quality_score = 4.0
                
                # Adjust for codec
                if "265" in codec or "hevc" in codec.lower() or "av1" in codec.lower():
                    quality_score += 0.5
                elif "vp9" in codec.lower():
                    quality_score += 0.3
                elif "nvenc" in codec.lower():
                    quality_score -= 0.5
                
                # Adjust for preset
                if preset in ['veryslow', 'placebo']:
                    quality_score += 0.5
                elif preset in ['ultrafast', 'superfast']:
                    quality_score -= 0.5
                
                # Cap at 10
                quality_score = min(10, quality_score)
                
                comment_lines.append(f"  ⭐ Estimated quality: {quality_score:.1f}/10")
            else:
                comment_lines.append(f"  ⭐ For estimated quality x/10, connect FFMPEG Configuration node")
                
        except Exception as e:
            comment_lines.append("\n=== Execution Status ===")
            comment_lines.append(f"❌ Error: {str(e)}")
            comment_lines.append("  ⚠️ See log for detailed error information")
            comment_lines.append("  💡 Common issues:")
            comment_lines.append("    - FFmpeg not installed or not in PATH")
            comment_lines.append("    - Insufficient disk space")
            comment_lines.append("    - Incompatible codec/container combination")
            comment_lines.append("    - Invalid parameter values")

        return ("\n".join(comment_lines), " ".join(ffmpeg_cmd), output_file)

        # return (comment, " ".join(ffmpeg_cmd), output_file)
import requests
import json
import logging
import hashlib
from typing import Dict, Any
from server import PromptServer
from pydub import AudioSegment
from pydub.playback import play
from aiohttp import web
import sys
import os
import time
import glob

class OllamaTalk:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "user_prompt": ("STRING", {"multiline": True}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "max_tokens": ("INT", {"default": 600, "min": 1, "max": 4096}),
                "vram_retention_minutes": ("INT", {"default": 0, "min": 0, "max": 99}),
                "answer_single_line": ("BOOLEAN", {"default": False}),
                "waiting_for_prompt": ("BOOLEAN", {"default": False}),
                "use_context_file": ("BOOLEAN", {"default": False}),
                # "context_size": ("INT", {"default": 0, "min": 0, "max": 1000}),
            },
            "optional": {
                "OLLAMA_CONFIG": ("OLLAMA_CONFIG", {"forceInput": True}),
                "context": ("STRING", {"multiline": True, "forceInput": True}),
                "OLLAMA_JOB": ("OLLAMA_JOB", {
                    "forceInput": True
                }),
            }
        }
    
    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("ollama_response", "updated_context", "system_prompt")
    FUNCTION = "chat_response"
    CATEGORY = "Bjornulf"
    
    is_paused = True
    is_interrupted = False
    current_instance = None
        
    def __init__(self):
        import ollama
        from ollama import Client
        self.last_content_hash = None
        self.waiting = False
        self.OLLAMA_CONFIG = None
        self.OLLAMA_JOB = None
        self.context = ""
        self.answer_single_line = True
        self.vram_retention_minutes = 1
        self.ollama_response = ""
        self.widgets = {}
        self.use_context_file = False
        OllamaTalk.current_instance = self
    
    def play_audio(self):
        try:
            if sys.platform.startswith('win'):
                try:
                    audio_file = os.path.join(os.path.dirname(__file__), 'bell.m4a')
                    sound = AudioSegment.from_file(audio_file, format="m4a")
                    wav_io = io.BytesIO()
                    sound.export(wav_io, format='wav')
                    wav_data = wav_io.getvalue()
                    import winsound
                    winsound.PlaySound(wav_data, winsound.SND_MEMORY)
                except Exception as e:
                    print(f"An error occurred: {e}")
            else:
                audio_file = os.path.join(os.path.dirname(__file__), 'bell.m4a')
                sound = AudioSegment.from_file(audio_file, format="m4a")
                play(sound)
        except Exception:
            pass  # Silently handle exceptions, no console output

    @classmethod
    def IS_CHANGED(cls, waiting_for_prompt, **kwargs):
        if waiting_for_prompt:
            return float("nan")
        return float(0)

    def save_context(self, context):
        os_path = os.path.join("Bjornulf", "ollama", "ollama_context.txt")
        os.makedirs(os.path.dirname(os_path), exist_ok=True)
        with open(os_path, "a", encoding="utf-8") as f:
            f.write(context + "\n")
            # f.write(context + "\n" + "-" * 80 + "\n")

    def load_context(self):
        os_path = os.path.join("Bjornulf", "ollama", "ollama_context.txt")
        if os.path.exists(os_path):
            with open(os_path, "r", encoding="utf-8") as f:
                return f.read().strip()
        return ""

    def process_ollama_request(self, user_prompt, answer_single_line, max_tokens, use_context_file=False):
        if self.OLLAMA_CONFIG is None:
            self.OLLAMA_CONFIG = {
                "model": "llama3.2:3b",
                "url": "http://0.0.0.0:11434"
            }
        
        selected_model = self.OLLAMA_CONFIG["model"]
        ollama_url = self.OLLAMA_CONFIG["url"]
        
        if self.OLLAMA_JOB is None:
            OLLAMA_JOB_text = "You are an helpful AI assistant."
        else:
            OLLAMA_JOB_text = self.OLLAMA_JOB["prompt"]

        formatted_prompt = "User: " + user_prompt
        
        if use_context_file:
            file_context = self.load_context()
            conversation = file_context + "\n" + formatted_prompt if file_context else formatted_prompt
        else:
            conversation = self.context + "\n" + formatted_prompt if self.context else formatted_prompt
        
        keep_alive_minutes = self.vram_retention_minutes
        
        try:
            client = Client(host=ollama_url)
            response = client.generate(
                model=selected_model,
                system=OLLAMA_JOB_text,
                prompt=conversation,
                options={
                    "num_ctx": max_tokens
                },
                keep_alive=f"{keep_alive_minutes}m"
            )
            result = response['response']
            updated_context = conversation + "\nAssistant: " + result
            self.context = updated_context
            
            if use_context_file:
                self.save_context(formatted_prompt + "\nAssistant: " + result)
            
            if answer_single_line:
                result = ' '.join(result.split())
                
            self.ollama_response = result
            return result, updated_context
        except Exception as e:
            logging.error(f"Connection to {ollama_url} failed: {e}")
            return "Connection to Ollama failed.", self.context

    def chat_response(self, user_prompt, seed, vram_retention_minutes, waiting_for_prompt=False,
                     context="", OLLAMA_CONFIG=None, OLLAMA_JOB=None, answer_single_line=False,
                     use_context_file=False, max_tokens=600, context_size=0):
        
        # Store configurations
        self.OLLAMA_CONFIG = OLLAMA_CONFIG
        self.OLLAMA_JOB = OLLAMA_JOB
        self.context = context
        self.answer_single_line = answer_single_line
        self.vram_retention_minutes = vram_retention_minutes
        self.user_prompt = user_prompt
        self.max_tokens = max_tokens
        self.use_context_file = use_context_file

        if waiting_for_prompt:
            self.play_audio()
            
            # Wait until either resumed or interrupted
            while OllamaTalk.is_paused and not OllamaTalk.is_interrupted:
                time.sleep(1)
            
            # Check if we were interrupted
            if OllamaTalk.is_interrupted:
                OllamaTalk.is_paused = True
                OllamaTalk.is_interrupted = False
                return ("Interrupted", self.context, self.OLLAMA_JOB["prompt"] if self.OLLAMA_JOB else "")
            
            OllamaTalk.is_paused = True
            return (self.ollama_response, self.context, self.OLLAMA_JOB["prompt"] if self.OLLAMA_JOB else "")
            #     result, updated_context = self.process_ollama_request(user_prompt, answer_single_line, use_context_file)
            #     return (result, updated_context, OLLAMA_JOB["prompt"] if OLLAMA_JOB else "")
        else:
            # Direct execution without waiting        
            result, updated_context = self.process_ollama_request(user_prompt, answer_single_line, max_tokens, use_context_file)
            return (result, updated_context, OLLAMA_JOB["prompt"] if OLLAMA_JOB else "")
    
@PromptServer.instance.routes.post("/bjornulf_ollama_send_prompt")
async def resume_node(request):
    if OllamaTalk.current_instance:
        instance = OllamaTalk.current_instance
        
        # Get the data from the request
        data = await request.json()
        updated_prompt = data.get('user_prompt')
        
        # Use the updated_prompt directly if it's not None
        prompt_to_use = updated_prompt if updated_prompt is not None else instance.user_prompt
        
        result, updated_context = instance.process_ollama_request(
            prompt_to_use, 
            instance.answer_single_line,
            instance.max_tokens,
            use_context_file=instance.use_context_file  # Ensure this is set to True
        )
            
        OllamaTalk.is_paused = False
        return web.Response(text="Node resumed")
    return web.Response(text="No active instance", status=400)

@PromptServer.instance.routes.post("/get_current_context_size")
async def get_current_context_size(request):
    counter_file = os.path.join("Bjornulf", "ollama", "ollama_context.txt")
    try:
        if not os.path.exists(counter_file):
            logging.info("[Ollama] Context file does not exist")
            # Create parent directories if they don't exist
            os.makedirs(os.path.dirname(counter_file), exist_ok=True)
            # Create empty file
            open(counter_file, 'w').close()
            logging.info(f"[Ollama] Created empty context file at: {counter_file}")
            return web.json_response({"success": True, "value": 0}, status=200)
            
        with open(counter_file, 'r', encoding='utf-8') as f:
            # Count non-empty lines in the file
            lines = [line.strip() for line in f.readlines() if line.strip()]
            line_count = len(lines)
            logging.info(f"[Ollama] Found {line_count} lines in context file")
            return web.json_response({"success": True, "value": line_count}, status=200)
                
    except Exception as e:
        # logging.error(f"Error reading context size: {str(e)}")
        return web.json_response({
            "success": False, 
            "error": str(e),
            "value": 0
        }, status=500)

def get_next_filename(base_path, base_name):
    """
    Find the next available filename with format base_name.XXX.txt
    where XXX is a 3-digit number starting from 001
    """
    pattern = os.path.join(base_path, f"{base_name}.[0-9][0-9][0-9].txt")
    existing_files = glob.glob(pattern)
    
    if not existing_files:
        return f"{base_name}.001.txt"
    
    # Extract numbers from existing files and find the highest
    numbers = []
    for f in existing_files:
        try:
            num = int(f.split('.')[-2])
            numbers.append(num)
        except (ValueError, IndexError):
            continue
    
    next_number = max(numbers) + 1 if numbers else 1
    return f"{base_name}.{next_number:03d}.txt"

@PromptServer.instance.routes.post("/reset_lines_context")
def reset_lines_context(request):
    # logging.info("Reset lines counter called")
    base_dir = os.path.join("Bjornulf", "ollama")
    base_file = "ollama_context"
    counter_file = os.path.join(base_dir, f"{base_file}.txt")
    
    try:
        if os.path.exists(counter_file):
            # Get new filename and rename
            new_filename = os.path.join(base_dir, get_next_filename(base_dir, base_file))
            os.rename(counter_file, new_filename)
            # logging.info(f"Renamed {counter_file} to {new_filename}")
            
            # Send notification through ComfyUI
            notification = {
                "ui": {
                    "notification_text": [f"Context file renamed to: {os.path.basename(new_filename)}"]
                }
            }
            return web.json_response({
                "success": True, 
                **notification
            }, status=200)
        
        return web.json_response({
            "success": True,
            "ui": {
                "notification_text": ["No context file to rename"]
            }
        }, status=200)
        
    except Exception as e:
        error_msg = str(e)
        return web.json_response({
            "success": False, 
            "error": error_msg,
            "ui": {
                "notification_text": [f"Error renaming file: {error_msg}"]
            }
        }, status=500)

@PromptServer.instance.routes.post("/bjornulf_ollama_interrupt")
async def interrupt_node(request):
    OllamaTalk.is_interrupted = True
    return web.Response(text="Node interrupted")

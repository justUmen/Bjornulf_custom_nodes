# 🔗 Comfyui : Bjornulf_custom_nodes v0.70 🔗

A list of 128 custom nodes for Comfyui : Display, manipulate, create and edit text, images, videos, loras, generate characters and more.  
You can manage looping operations, generate randomized content, trigger logical conditions, pause and manually control your workflows and even work with external AI tools, like Ollama or Text To Speech.  

#  Watch Video Intro (Quick overview 28 minutes) :
[![Watch the video](https://img.youtube.com/vi/jTg9QsgKYmA/hqdefault.jpg)](https://youtu.be/jTg9QsgKYmA)

# Coffee : ☕☕☕☕☕ 5/5

Support me and my work : ❤️❤️❤️ <https://ko-fi.com/bjornulf> ❤️❤️❤️

# ☘ This project is part of my AI trio. ☘

1 - 📝 Text/Chat AI generation : [Bjornulf Lobe Chat Fork](https://github.com/justUmen/Bjornulf_lobe-chat)  
2 - 🔊 Speech AI generation : [Bjornulf Text To Speech](https://github.com/justUmen/Bjornulf_XTTS)  
<u>**3 - 🎨 Image AI generation :** [Bjornulf Comfyui custom nodes](https://github.com/justUmen/Bjornulf_custom_nodes) (you are here)</u>  

# 📋 Nodes menu by category

## 👁 Display and Show 👁
`1.` [👁 Show (Text, Int, Float)](#1----show-text-int-float)  
`49.` [📹👁 Video Preview](#49----video-preview)  
`68.` [🔢 Add line numbers](#68----add-line-numbers)  
`71.` [👁 Show (Int)](#71----show-int)  
`72.` [👁 Show (Float)](#72----show-float)  
`73.` [👁 Show (String/Text)](#73----show-stringtext)  
`74.` [👁 Show (JSON)](#74----show-json)  
`126.` [📒 Note](#126----note)  
`127.` [🖼📒 Image Note](#127----image-note)  
`128.` [🖼👁 Preview (first) image](#128----preview-first-image)  

## ✒ Text ✒
`2.` [✒ Write Text](#2----write-text)  
`3.` [✒🗔 Advanced Write Text (+ 🎲 random selection and 🅰️ variables)](#3----advanced-write-text---random-selection-and-🅰%EF%B8%8F-variables)  
`4.` [🔗 Combine Texts](#4----combine-texts)  
`15.` [💾 Save Text](#15----save-text)  
`26.` [🎲 Random line from input](#26----random-line-from-input)  
`28.` [🔢🎲 Text with random Seed](#28----text-with-random-seed)  
`32.` [🧑📝 Character Description Generator](#32----character-description-generator)  
`48.` [🔀🎲 Text scrambler (🧑 Character)](#48----text-scrambler--character)  
`67.` [📝➜✨ Text to Anything](#67----text-to-anything)  
`68.` [✨➜📝 Anything to Text](#68----anything-to-text)  
`75.` [📝➜📝 Replace text](#75----replace-text)  
`15.` [💾 Save Text](#15----save-text)  
`111.` [✨➜🔢 Anything to Int](#111----anything-to-int)  
`112.` [✨➜🔢 Anything to Float](#112----anything-to-float)  
`113.` [📝🔪 Text split in 5](#113----text-split-in-5)  
`115.` [📥 Load Text From Bjornulf Folder](115----load-text-from-bjornulf-folder)  
`116.` [📥 Load Text From Path](#116----load-text-from-path)  
`117.` [📝👈 Line selector (🎲 or ♻ or ♻📑)](#117)  

## 🔥 Text Generator 🔥
`81.` [🔥📝 Text Generator 📝🔥](#81----text-generator-)  
`82.` [👩‍🦰📝 Text Generator (Character Female)](#82----text-generator-character-female)  
`83.` [👨‍🦰📝 Text Generator (Character Male)](#83----text-generator-character-male)  
`84.` [👾📝 Text Generator (Character Creature)](#84----text-generator-character-creature)  
`85.` [💃🕺📝 Text Generator (Character Pose)](#85----text-generator-character-pose)  
`86.` [🔧👨‍🔧📝 Text Generator (Object for Character)](#86----text-generator-object-for-character)  
`87.` [🌄📝 Text Generator (Scene)](#87----text-generator-scene)  
`88.` [🎨📝 Text Generator (Style)](#88----text-generator-style)  
`89.` [👗 Text Generator (Outfit Female)](#89----text-generator-outfit-female)  
`90.` [👚 Text Generator (Outfit Male)](#90----text-generator-outfit-male)  
`91.` [♻🔥📝 List Looper (Text Generator)](#91----list-looper-text-generator)  
`92.` [♻🌄📝 List Looper (Text Generator Scenes)](#92----list-looper-text-generator-scenes)  
`93.` [♻🎨📝 List Looper (Text Generator Styles)](#93----list-looper-text-generator-styles)  
`94.` [♻💃🕺📝 List Looper (Text Generator Poses)](#94----list-looper-text-generator-poses)  
`95.` [♻👨‍🦰👩‍🦰👾 List Looper (Text Generator Characters)](#95----list-looper-text-generator-characters)  
`96.` [♻👚 List Looper (Text Generator Outfits Male)](#96----list-looper-text-generator-outfits-male)  
`97.` [♻👗 List Looper (Text Generator Outfits Female)](#97----list-looper-text-generator-outfits-female)  

## ♻ Loop ♻
`6.` [♻ Loop](#6----loop)  
`7.` [♻ Loop Texts](#7----loop-texts)  
`8.` [♻ Loop Integer](#8----loop-integer)  
`9.` [♻ Loop Float](#9----loop-float)  
`10.` [♻ Loop All Samplers](#10----loop-all-samplers)  
`11.` [♻ Loop All Schedulers](#11----loop-all-schedulers)  
`12.` [♻ Loop Combos](#12----loop-combos)  
`27.` [♻ Loop (All Lines from input)](#27----loop-all-lines-from-input)  
`33.` [♻ Loop (All Lines from input 🔗 combine by lines)](#33----loop-all-lines-from-input--combine-by-lines)  
`38.` [♻🖼 Loop (Images)](#38----loop-images)  
`39.` [♻ Loop (✒🗔 Advanced Write Text + 🅰️ variables)](#39----loop--advanced-write-text)  
`42.` [♻ Loop (Model+Clip+Vae) - aka Checkpoint / Model](#42----loop-modelclipvae---aka-checkpoint--model)  
`53.` [♻ Loop Load checkpoint (Model Selector)](#53----loop-load-checkpoint-model-selector)  
`54.` [♻👑 Loop Lora Selector](#54----loop-lora-selector)  
`56.` [♻📑 Loop Sequential (Integer)](#56----loop-sequential-integer)  
`57.` [♻📑 Loop Sequential (input Lines)](#57----loop-sequential-input-lines)  
`90.` [♻🔥📝 List Looper (Text Generator)](#8)  
`91.` [♻🌄📝 List Looper (Text Generator Scenes)](#8)  
`92.` [♻🎨📝 List Looper (Text Generator Styles)](#8)  
`93.` [♻💃🕺📝 List Looper (Text Generator Poses)](#8)  
`94.` [♻👨‍🦰👩‍🦰📝 List Looper (Text Generator Characters)](#8)  
`95.` [♻👚 List Looper (Text Generator Outfits Male)](#8)  
`96.` [♻👗 List Looper (Text Generator Outfits Female)](#8)  

## 🎲 Randomization 🎲
`3.` [✒🗔 Advanced Write Text (+ 🎲 random selection and 🅰️ variables)](#3----advanced-write-text---random-selection-and-🅰%EF%B8%8F-variables)  
`5.` [🎲 Random (Texts)](#5----random-texts)  
`26.` [🎲 Random line from input](#26----random-line-from-input)  
`28.` [🔢🎲 Text with random Seed](#28----text-with-random-seed)  
`37.` [🎲🖼 Random Image](#37----random-image)  
`40.` [🎲 Random (Model+Clip+Vae) - aka Checkpoint / Model](#40----random-modelclipvae---aka-checkpoint--model)  
`41.` [🎲 Random Load checkpoint (Model Selector)](#41----random-load-checkpoint-model-selector)  
`48.` [🔀🎲 Text scrambler (🧑 Character)](#48----text-scrambler--character)  
`55.` [🎲👑 Random Lora Selector](#55----random-lora-selector)  
`117.` [📝👈 Line selector (🎲 or ♻ or ♻📑)](#117----line-selector--or--or-)  

## 🖼💾 Save Image / Text 💾🖼
`16.` [💾🖼💬 Save image for Bjornulf LobeChat](#16----save-image-for-bjornulf-lobechat-for-my-custom-lobe-chat)  
`17.` [💾🖼 Save image as `tmp_api.png` Temporary API](#17----save-image-as-tmp_apipng-temporary-api-%EF%B8%8F)  
`18.` [💾🖼📁 Save image to a chosen folder name](#18----save-image-to-a-chosen-folder-name)  
`14.` [💾🖼 Save Exact name](#1314------resize-and-save-exact-name-%EF%B8%8F)  
`123.` [💾 Save Global Variables](#123----save-global-variables)  

## 🖼📥 Load Image / Text 📥🖼
`29.` [📥🖼 Load Image with Transparency ▢](#29----load-image-with-transparency-)  
`43.` [📥🖼📂 Load Images from output folder](#43----load-images-from-output-folder)  
`124.` [📥 Load Global Variables](#124----load-global-variables)  

## 🖼 Image - others 🖼
`13.` [📏 Resize Image](#1314------resize-and-save-exact-name-%EF%B8%8F)  
`22.` [🔲 Remove image Transparency (alpha)](#22----remove-image-transparency-alpha)  
`23.` [🔲 Image to grayscale (black & white)](#23----image-to-grayscale-black--white)  
`24.` [🖼+🖼 Stack two images (Background + Overlay)](#24----stack-two-images-background--overlay)  
`25.` [🟩➜▢ Green Screen to Transparency](#25----green-screen-to-transparency)  
`29.` [⬇️🖼 Load Image with Transparency ▢](#29----load-image-with-transparency-)  
`30.` [🖼✂ Cut image with a mask](#30----cut-image-with-a-mask)  
`37.` [🎲🖼 Random Image](#37----random-image)  
`38.` [♻🖼 Loop (Images)](#38----loop-images)  
`43.` [⬇️📂🖼 Load Images from output folder](#43----load-images-from-output-folder)  
`44.` [🖼👈 Select an Image, Pick](#44----select-an-image-pick)  
`46.` [🖼🔍 Image Details](#46----image-details)  
`47.` [🖼 Combine Images](#47----combine-images)  
`60.` [🖼🖼 Merge Images/Videos 📹📹 (Horizontally)](#60----merge-imagesvideos--horizontally)  
`61.` [🖼🖼 Merge Images/Videos 📹📹 (Vertically)](#61----merge-imagesvideos--vertically)  
`62.` [🦙👁 Ollama Vision](#62----ollama-vision)  
`70.` [📏 Resize Image Percentage](#70----resize-image-percentage)  
`80.` [🩷 Empty Latent Selector](#80----empty-latent-selector)  

## 🚀 Load checkpoints 🚀
`40.` [🎲 Random (Model+Clip+Vae) - aka Checkpoint / Model](#40----random-modelclipvae---aka-checkpoint--model)  
`41.` [🎲 Random Load checkpoint (Model Selector)](#41----random-load-checkpoint-model-selector)  
`42.` [♻ Loop (Model+Clip+Vae) - aka Checkpoint / Model](#42----loop-modelclipvae---aka-checkpoint--model)  
`53.` [♻ Loop Load checkpoint (Model Selector)](#53----loop-load-checkpoint-model-selector)  
`125.` [📝👈 Model-Clip-Vae selector (🎲 or ♻ or ♻📑)](#125----model-clip-vae-selector--or--or-)  

## 🚀 Load loras 🚀
`54.` [♻ Loop Lora Selector](#54----loop-lora-selector)  
`55.` [🎲 Random Lora@ Selector](#55----random-lora-selector)  
`114.` [📥👑 Load Lora with Path](#114----load-lora-with-path)  
`122.` [👑 Combine Loras, Lora stack](#122----combine-loras-lora-stack)  

## ☁ Image Creation : API / cloud / remote ☁
`106.` [☁🎨 API Image Generator (FalAI) ☁](#106----api-image-generator-falai-)  
`107.` [☁🎨 API Image Generator (CivitAI) ☁](#107----api-image-generator-civitai-)  
`108.` [☁👑 Add Lora (API ONLY - CivitAI) 👑☁](#108----add-lora-api-only---civitai-)  
`109.` [☁🎨 API Image Generator (Black Forest Labs - Flux) ☁](#109----api-image-generator-black-forest-labs---flux-)  
`110.` [☁🎨 API Image Generator (Stability - Stable Diffusion) ☁](#110----api-image-generator-stability---stable-diffusion-)  

## 📥 Take from CivitAI / Hugginface 📥
`98.` [📥 Load checkpoint SD1.5 (+Download from CivitAi)](#98----load-checkpoint-sd15-download-from-civitai)  
`99.` [📥 Load checkpoint SDXL (+Download from CivitAi)](#99----load-checkpoint-sdxl-download-from-civitai)  
`100.` [📥 Load checkpoint Pony (+Download from CivitAi)](#100----load-checkpoint-pony-download-from-civitai)  
`101.` [📥 Load checkpoint FLUX Dev (+Download from CivitAi)](#101----load-checkpoint-flux-dev-download-from-civitai)  
`102.` [📥 Load checkpoint FLUX Schnell (+Download from CivitAi)](#102----load-checkpoint-flux-schnell-download-from-civitai)  
`103.` [📥👑 Load Lora SD1.5 (+Download from CivitAi)](#103----load-lora-sd15-download-from-civitai)  
`104.` [📥👑 Load Lora SDXL (+Download from CivitAi)](#104----load-lora-sdxl-download-from-civitai)  
`105.` [📥👑 Load Lora Pony (+Download from CivitAi)](#105----load-lora-pony-download-from-civitai)  
`119.` [📥👑📹 Load Lora Hunyuan Video (+Download from CivitAi)](#119----load-lora-hunyuan-video-download-from-civitai)  
`121.` [💾 Huggingface Downloader](#121----huggingface-downloader)  

## 📹 Video 📹
`20.` [📹 Video Ping Pong](#20----video-ping-pong)  
`21.` [📹 Images to Video (FFmpeg)](#21----images-to-video)  
`49.` [📹👁 Video Preview](#49----video-preview)  
`50.` [🖼➜📹 Images to Video path (tmp video)](#50----images-to-video-path-tmp-video)  
`51.` [📹➜🖼 Video Path to Images](#51----video-path-to-images)  
`52.` [🔊📹 Audio Video Sync](#52----audio-video-sync) 
`58.` [📹🔗 Concat Videos](#58----concat-videos)  
`59.` [📹🔊 Combine Video + Audio](#59----combine-video--audio)  
`60.` [🖼🖼 Merge Images/Videos 📹📹 (Horizontally)](#60----merge-imagesvideos--horizontally)  
`61.` [🖼🖼 Merge Images/Videos 📹📹 (Vertically)](#61----merge-imagesvideos--vertically)  
`76.` [⚙📹 FFmpeg Configuration 📹⚙](#76----ffmpeg-configuration-)  
`77.` [📹🔍 Video details ⚙](#77----video-details-)  
`78.` [📹➜📹 Convert Video](#78----convert-video)  
`79.` [📹🔗 Concat Videos from list](#79----concat-videos-from-list)  
`119.` [📥👑📹 Load Lora Hunyuan Video (+Download from CivitAi)](#119----load-lora-hunyuan-video-download-from-civitai)  

## 🤖 AI 🤖
`19.` [🦙💬 Ollama Talk](#19----ollama-talk)  
`31.` [📝➜🔊 TTS - Text to Speech](#31----tts---text-to-speech-100-local-any-voice-you-want-any-language)  
`62.` [🦙👁 Ollama Vision](#62----ollama-vision)  
`63.` [🦙 Ollama Configuration ⚙](#63----ollama-configuration-)  
`64.` [🦙 Ollama Job Selector 💼](#64----ollama-job-selector-)  
`65.` [🦙 Ollama Persona Selector 🧑](#65----ollama-persona-selector-)  
`66.` [🔊➜📝 STT - Speech to Text](#66----stt---speech-to-text)  
`118.` [🔊 TTS Configuration ⚙](#118----tts-configuration-)  

## 🔊 Audio 🔊
`31.` [📝➜🔊 TTS - Text to Speech](#31----tts---text-to-speech-100-local-any-voice-you-want-any-language)  
`52.` [🔊📹 Audio Video Sync](#52----audio-video-sync)  
`59.` [📹🔊 Combine Video + Audio](#59----combine-video--audio)  
`66.` [🔊➜📝 STT - Speech to Text](#66----stt---speech-to-text)  
`118.` [🔊 TTS Configuration ⚙](#118----tts-configuration-)  
`120.` [📝➜🔊 Kokoro - Text to Speech](#120----kokoro---text-to-speech)  

## 💻 System 💻
`34.` [🧹 Free VRAM hack](#34----free-vram-hack)  

## 🧍 Manual user Control 🧍
`35.` [⏸️ Paused. Resume or Stop, Pick 👇](#35---%EF%B8%8F-paused-resume-or-stop-)  
`36.` [⏸️ Paused. Select input, Pick 👇](#36---%EF%B8%8F-paused-select-input-pick-one)  
`117.` [📝👈 Line selector (🎲 or ♻ or ♻📑)](#117----line-selector--or--or-)  

## 🧠 Logic / Conditional Operations 🧠
`45.` [🔀 If-Else (input / compare_with)](#45----if-else-input--compare_with)  

# ☁ Usage in cloud : 

Comfyui is great for local usage, but I sometimes need more power than what I have...  
I have a computer with a 4070 super with 12GB and flux fp8 simple wokflow take about ~40 seconds. With a 4090 in the cloud I can run flux fp16 in ~12 seconds. (There are of course also some workflow that I can't even run locally.)  

My referal link for Runpod : <https://runpod.io?ref=tkowk7g5> (If you use that i will have a commission, at no extra cost for you.)  
If you want to use my nodes and comfyui in the cloud (and can install more stuff), I'm managing an optimized ready-to-use template on runpod : <https://runpod.io/console/deploy?template=r32dtr35u1&ref=tkowk7g5>  
Template name : `bjornulf-comfyui-allin-workspace`, can be operational in ~3 minutes. (Depending on your pod, setup and download of extra models or whatever not included.)  
You need to create and select a network volume before using that, size is up to you, i have 50Gb Storage because i use cloud only for Flux or lora training on a 4090. (~0.7$/hour)  
⚠️ When pod is ready, you need to open a terminal in browser (After clicking on `connect` from your pod) and use this to launch ComfyUI manually : `cd /workspace/ComfyUI && python main.py --listen 0.0.0.0 --port 3000` or the alias `start_comfy` (Much better to control it with a terminal, check logs, etc...)  
After that you can just click on the `Connect to port 3000` button.  
As file manager, you can use the included `JupyterLab` on port 8888.  
If you have any issues with it, please let me know.  
It will manage everything in Runpod network storage (`/workspace/ComfyUI`), so you can stop and start the cloud GPU without losing anything, change GPU or whatever.  
Zone : I recommend `EU-RO-1`, but up to you.  
Top-up your Runpod account with minimum 10$ to start.  
⚠️ Warning, you will pay by the minute, so not recommended for testing or learning comfyui. Do that locally !!!  
Run cloud GPU only when you already have your workflow ready to run.  
Advice : take a cheap GPU for testing, downloading models or settings things up.  
To download checkpoint or anything else, you need to use the terminal.  
For downloading from Huggingface (get token here <https://huggingface.co/settings/tokens>).  
Here is example for everything you need for flux dev :  
```
huggingface-cli login --token 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
huggingface-cli download black-forest-labs/FLUX.1-dev flux1-dev.safetensors --local-dir /workspace/ComfyUI/models/unet
huggingface-cli download comfyanonymous/flux_text_encoders clip_l.safetensors --local-dir /workspace/ComfyUI/models/clip
huggingface-cli download comfyanonymous/flux_text_encoders t5xxl_fp16.safetensors --local-dir /workspace/ComfyUI/models/clip
huggingface-cli download black-forest-labs/FLUX.1-dev ae.safetensors --local-dir /workspace/ComfyUI/models/vae
```
To use Flux you can just drag and drop in your browser comfyui interface the .json from my github repo : `workflows/FLUX_dev_troll.json`, direct link : <https://github.com/justUmen/ComfyUI-BjornulfNodes/blob/main/workflows/FLUX_dev_troll.json>.  

For downloading from civitai (get token here <https://civitai.com/user/account>), just copy/paste the link of checkpoint you want to download and use something like that, with your token in URL :  
```
CIVITAI="8b275fada679ba5812b3da2bf35016f6"
wget --content-disposition -P /workspace/ComfyUI/models/checkpoints "https://civitai.com/api/download/models/272376?type=Model&format=SafeTensor&size=pruned&fp=fp16&token=$CIVITAI"
```

If you want to download for example the entire output folder, you can just compress it : 
```
cd /workspace/ComfyUI/output && tar -czvf /workspace/output.tar.gz .
```

Then you can download it from the file manager JupyterLab.  

If you have any issues with this template from Runpod, please let me know, I'm here to help. 😊  

# 🏗 Dependencies (nothing to do for runpod ☁)

Check `requirements.txt` for the latest dependencies...  

## 🪟🐍 Windows : Install dependencies on windows with embedded python (portable version)

First you need to find this python_embedded `python.exe`, then you can right click or shift + right click inside the folder in your file manager to open a terminal there.  

This is where I have it, with the command you need :  
`H:\ComfyUI_windows_portable\python_embeded> .\python.exe -m pip install pydub ollama opencv-python`  

When you have to install something you can retake the same code and install the dependency you want :  
`.\python.exe -m pip install whateveryouwant`  

You can then run comfyui.  

## 🐧🐍 Linux : Install dependencies (without venv, not recommended)

Move the the custom_node folder and :  `pip install -r requirements.txt`

OR

- `pip install ollama` (you can also install ollama if you want :  https://ollama.com/download) - You don't need to really install it if you don't want to use my ollama node. (BUT you need to run `pip install ollama`)
- `pip install pydub` (for TTS node)
- `pip install opencv-python`
- etc...

## 🐧🐍 Linux : Install dependencies with python virtual environment (venv)

If you want to use a python virtual environment only for comfyUI, which I recommended, you can do that for example (also pre-install pip) :  

```
sudo apt-get install python3-venv python3-pip
python3 -m venv /the/path/you/want/venv/bjornulf_comfyui
```

Once you have your environment in this new folder, you can activate it with and install dependencies inside :  

```
source /the/path/you/want/venv/bjornulf_comfyui/bin/activate
cd custom_nodes/Bjornulf_custom_nodes
pip install -r requirements.txt
```

Then you can start comfyui with this environment (notice that you need to re-activate it each time you want to launch comfyui) :  

```
cd /where/you/installed/ComfyUI && python main.py
```

# 📝 Changelog

- **v0.2**: Improve ollama node with system prompt + model selection.
- **v0.3**: Add a new node : Save image to a chosen folder.
- **v0.3**: Add comfyui Metadata / workflow to all my image-related nodes.
- **v0.4**: Support transparency option with webm format, options encoders. As well as input for audio stream. 
- **v0.5**: New node : Remove image transparency (alpha) - Fill alpha channel with solid color.
- **v0.5**: New node : Image to grayscale (black & white) - Convert an image to grayscale.
- **v0.6**: New node : Combine images (Background + Overlay) - Combine two images into a single image.
- **v0.7**: Replace Save API node with Save Bjornulf Lobechat node. (For my custom lobe-chat)
- **v0.8**: Combine images : add an option to put image top, bottom or center.
- **v0.8**: Combine texts : add option for slashes /
- **v0.8**: Add basic node to transform greenscreen in to transparency.
- **v0.9**: Add a new node : Return one random line from input.
- **v0.10**: Add a new node : Loop (All Lines from input) - Iterate over all lines from an input text.
- **v0.11**: Add a new node : Text with random Seed - Generate a random seed, along with text.
- **v0.12**: Combine images : Add option to move vertically and horizontally. (from -50% to 150%)
- **v0.13**: Add a new node: Load image with transparency (alpha) - Load an image with transparency.
- **v0.14**: Add a new node: Cut image from a mask
- **v0.15**: Add two new nodes: TTS - Text to Speech and Character Description Generator
- **v0.16**: Big changes on Character Description Generator
- **v0.17**: New loop node, combine by lines.
- **v0.18**: New loop node, Free VRAM hack
- **v0.19**: Changes for save to folder node : ignore missing images filenames, will use the highest number found + 1.
- **v0.20**: Changes for lobechat save image : include the code of free VRAM hack + ignore missing images filenames
- **v0.21**: Add a new write text node that also display the text in the comfyui console (good for debugging)
- **v0.22**: Allow write text node to use random selection like this {hood|helmet} will randomly choose between hood or helmet.
- **v0.23**: Add a new node: Pause, resume or stop workflow.
- **v0.24**: Add a new node: Pause, select input, pick one.
- **v0.25**: Two new nodes: Loop Images and Random image.
- **v0.26**: New node : Loop write Text. Also increase nb of inputs allowed for most nodes. (+ update some breaking changes)
- **v0.27**: Two new nodes : Loop (Model+Clip+Vae) and Random (Model+Clip+Vae) - aka Checkpoint / Model
- **v0.28**: Fix random texts and add a lot of screenshots examples for several nodes.
- **v0.29**: Fix floating points issues with loop float node.
- **v0.30**: Update the basic Loop node with optional input.
- **v0.31**: ❗Sorry, Breaking changes for Write/Show text nodes, cleaner system : 1 simple write text and the other is 1 advanced with console and special syntax. Also Show can now manage INT, FLOAT, TEXT.
- **v0.32**: Quick rename to avoid breaking loop_text node.
- **v0.33**: Control random on paused nodes, fix pydub sound bug permissions on Windows.
- **v0.34**: Two new nodes : Load Images from output folder and Select an Image, Pick.
- **v0.35**: Great improvements of the TTS node 31. It will also save the audio file in the "ComfyUI/Bjornulf_TTS/" folder. - Not tested on windows yet -
- **v0.36**: Fix random model.
- **v0.37**: New node : Random Load checkpoint (Model Selector). Alternative to the random checkpoint node. (Not preloading all checkpoints in memory, slower to switch between checkpoints, but more outputs to decide where to store your results.)
- **v0.38**: New node : If-Else logic. (input == compare_with), examples with different latent space size. +fix some deserialization issues.
- **v0.39**: Add variables management to Advanced Write Text node.
- **v0.40**: Add variables management to Loop Advanced Write Text node. Add menu for all nodes to the README.
- **v0.41**: Two new nodes : image details and combine images. Also ❗ Big changes to the If-Else node. (+many minor changes)
- **v0.42**: Better README with category nodes, changes some node titles
- **v0.43**: Add control_after_generate to Ollama and allow to keep in VRAM for 1 minute if needed. (For chaining quick generations.) Add fallback to 0.0.0.0
- **v0.44**: Allow ollama to have a custom url in the file `ollama_ip.txt` in the comfyui custom nodes folder. Minor changes, add details/updates to README.
- **v0.45**: Add a new node : Text scrambler (Character), change text randomly using the file `scrambler/scrambler_character.json` in the comfyui custom nodes folder.
- **v0.46**: ❗ A lot of changes to Video nodes. Save to video is now using FLOAT for fps, not INT. (A lot of other custom nodes do that as well...) Add node to preview video, add node to convert a video path to a list of images. add node to convert a list of images to a temporary video + video_path. add node to synchronize duration of audio with video. (useful for MuseTalk) change TTS node with many new outputs ("audio_path", "full_path", "duration") to reuse with other nodes like MuseTalk, also TTS rename input to "connect_to_workflow", to avoid mistakes sending text to it.
- **v0.47**: New node : Loop Load checkpoint (Model Selector).
- **v0.48**: Two new nodes for loras : Random Lora Selector and Loop Lora Selector.
- **v0.49**: New node : Loop Sequential (Integer) - Loop through a range of integer values. (But once per workflow run), audio sync is smarter and adapt the video duration to the audio duration.
- **v0.50**: allow audio in Images to Video path (tmp video). Add three new nodes : Concat Videos, combine video/audio and Loop Sequential (input Lines). save text changes to write inside Comfyui folder. Fix random line from input outputing LIST. ❗ Breaking change to audio/video sync node, allowing different types as input.
- **v0.51**: Fix some issues with audio/video sync node. Add two new nodes : merge images/videos vertical and horizontal. add requirements.txt and ollama_ip.txt
- **v0.52-53**: Revert name git to Bjornulf_custom_nodes, match registry comfy
- **v0.54-55**: add opencv-python to requirements.txt
- **0.56**: ❗Breaking changes : ollama node simplified, no ollama_ip.txt needed, waiting for collection ollama nodes to be ready.
- **0.57**: ❗❗Huge changes, new Ollama node "Ollama Chat" with real functionalities. 5 Ollama nodes total. (Model selector + Job selector + Persona selector + Ollama vision + Ollama Talk) Ollama talk use context and can use context file. Add number of lines / current counter + next to sequential nodes. Add new node STT. (+ faster_whisper dep) better management of empty loras/checkpoints on selectors. (list preset) Add "default_for_language" for TTS node, taking the default voice for a language (ex: fr/default.wav) Otherwise take the first wav with the selected language.
- **0.58**: small fix in model selector default value. (Set to None by default)
- **0.59**: A lot of Javascript fixing to avoid resizing and better properties mangement / recoveries
- **0.60**: Revert changes from ollama_talk (implement _user mode later / another node)
- **0.61**: Add/modify a bunch of Ffmpeg / video nodes. With a global configuration system and toggle python-ffmpeg / system.
- **0.62**: MASSIVE update, Text Generator nodes. (15 nodes), API nodes generate (civitai / black forest labs / fal.ai), API civit ai download models nodes, lora
- **0.63**: delete long file, useless
- **0.64**: remove "import wget", added some keywords to text generators.
- **0.65**: ❗Breaking changes : Combine Text inputs are now all optional (PLease remake your nodes, sorry.) Add 6 new nodes : any2int, any2float, load text from folder, load text from path, load lora from path. Also upgraded the Save text node.
- **0.66**: Add lora hunyuan CIVIT ai + download, add TTS configuration node, edit requirements.txt
- **0.67**: Add kokoro TTS node.
- **0.68**: Update kokoro TTS node with connect_to_workflow and same outputs as XTTS.
- **0.69**: Small fixes
- **0.70**: ❗Breaking changes : "Line Selector Node" is now a "universal node" : manual selection, random, and LOOP + Sequential.
Text replace now have multine option for regex. (https://github.com/justUmen/Bjornulf_custom_nodes/issues/17) - can remove <think> tag from ollama.  
8 new nodes : "🖼👁 Preview (first) image", "💾 Huggingface Downloader", "👑 Combine Loras, Lora stack", "📥 Load Global Variables", "💾 Save Global Variables", "📝👈 Model-Clip-Vae selector (🎲 or ♻ or ♻📑)", "📒 Note", "🖼📒 Image Note".
Fix a lot of code everywhere, a little better logging system, etc...  
WIP : Rewrite of all my ffmpeg nodes. (Still need improvements and fixes, will do that in 0.71) Maybe don't use them yet...

# 📝 Nodes descriptions

## 1 - 👁 Show (Text, Int, Float)

**Description:**  
The show node will only display text, or a list of several texts. (read only node)  
3 types are managed : Green is for STRING type, Orange is for FLOAT type and blue is for INT type. I put colors so I/you don't try to edit them. 🤣  

Update 0.61 : You now also have 4 other nodes to display format specific values : INT, FLOAT, STRING and JSON (STRING)  
These are convenient because these are automatically recommended on drag and drop.  

![Show Text](screenshots/show.png)

## 2 - ✒ Write Text

**Description:**  
Simple node to write text.  

![write Text](screenshots/write.png)

## 3 - ✒🗔 Advanced Write Text (+ 🎲 random selection and 🅰️ variables)

**Description:**  
Advanced Write Text node allows for special syntax to accept random variants, like `{hood|helmet}` will randomly choose between hood or helmet.  
You also have `seed` and `control_after_generate` to manage the randomness.  
It is also displaying the text in the comfyui console. (Useful for debugging)  
Example of console logs :  
```
Raw text: photo of a {green|blue|red|orange|yellow} {cat|rat|house}
Picked text: photo of a green house
```

![write Text Advanced](screenshots/write_advanced.png)

You can also create and reuse variables with this syntax : `<name>`.
Usage example : 

![variables](screenshots/variables.png)

## 4 - 🔗 Combine Texts

**Description:**  
Combine multiple text inputs into a single output. (can have separation with : comma, space, new line or nothing.)

![Combine Texts](screenshots/combine_texts.png)

## 5 - 🎲 Random (Texts)

**Description:**  
Generate and display random text from a predefined list. Great for creating random prompts.  
You also have `control_after_generate` to manage the randomness.  

![Random Text](screenshots/random_text.png)


## 6 - ♻ Loop

**Description:**  
General-purpose loop node, you can connect that in between anything.  

![Loop](screenshots/loop.png)

It has an optional input, if no input is given, it will loop over the value of the STRING "if_no_input" (take you can edit).  
❗ Careful this node accept everything as input and output, so you can use it with texts, integers, images, mask, segs etc... but be consistent with your inputs/outputs.  
Do not use this Loop if you can do otherwise.  

This is an example together with my node 28, to force a different seed for each iteration :   
![Loop](screenshots/loop4.png)

## 7 - ♻ Loop Texts

**Description:**  
Cycle through a list of text inputs.  

![Loop Texts](screenshots/loop_texts.png)

Here is an example of usage with combine texts and flux :  
![Loop Texts example](screenshots/loop_text_example.png)

## 8 - ♻ Loop Integer

**Description:**  
Iterate through a range of integer values, good for `steps` in ksampler, etc...

![Loop Integer](screenshots/loop_integer.png)
![Loop Int + Show Text](screenshots/loop_int+show_text.png)

❗ Don't forget that you can convert ksampler widgets to input by right-clicking the ksampler node :  
![Widget to Input](screenshots/widget-to-input.png)

Here is an example of usage with ksampler (Notice that with "steps" this node isn't optimized, but good enough for quick testing.) :  
![Widget to Input](screenshots/example_loop_integer.png)

## 9 - ♻ Loop Float

**Description:**  
Loop through a range of floating-point numbers, good for `cfg`, `denoise`, etc...  

![Loop Float + Show Text](screenshots/loop_float+show_text.png)
![Loop Float](screenshots/loop_float.png)

Here is an example with controlnet, trying to make a red cat based on a blue rabbit :  
![Loop All Samplers](screenshots/loop_float_example.png)

## 10 - ♻ Loop All Samplers

**Description:**  
Iterate over all available samplers to apply them one by one. Ideal for testing.  

![Loop All Samplers](screenshots/loop_all_samplers.png)

Here is an example of looping over all the samplers with the normal scheduler :  
![Loop All Samplers](screenshots/example_loop_all_samplers.png)

## 11 - ♻ Loop All Schedulers

**Description:**  
Iterate over all available schedulers to apply them one by one. Ideal for testing. (same idea as sampler above, but for schedulers)  

![Loop All Schedulers](screenshots/loop_all_schedulers.png)

## 12 - ♻ Loop Combos

**Description:**  
Generate a loop from a list of my own custom combinations (scheduler+sampler), or select one combo manually.  
Good for testing.

![Loop Combos](screenshots/loop_combos.png)

Example of usage to see the differences between different combinations :    
![example combos](screenshots/example_combos.png)

## 13/14 - 📏 + 🖼 Resize and Save Exact name ⚠️💣

**Description:**  
Resize an image to exact dimensions. The other node will save the image to the exact path.  
⚠️💣 Warning : The image will be overwritten if it already exists.

![Resize and Save Exact](screenshots/resize_save_exact.png)

## 15 - 💾 Save Text

**Description:**  
Save the given text input to a file. Useful for logging and storing text data.  
If the file already exist, it will add the text at the end of the file.  
I recommend you to keep saving them in "Bjornulf/Text" (Which is in the Comfyui folder, next to output), this is where the node 116 `Load text from folder` is looking for text files.  

![Save Text](screenshots/save_text.png)

## 16 - 💾🖼💬 Save image for Bjornulf LobeChat (❗For my custom [lobe-chat](https://github.com/justUmen/Bjornulf_lobe-chat)❗)

**Description:**  
❓ I made that node for my custom lobe-chat to send+receive images from Comfyui API : [lobe-chat](https://github.com/justUmen/Bjornulf_lobe-chat)  
It will save the image in the folder `output/BJORNULF_LOBECHAT/`. 
The name will start at `api_00001.png`, then `api_00002.png`, etc...  
It will also create a link to the last generated image at the location `output/BJORNULF_API_LAST_IMAGE.png`.  
This link will be used by my custom lobe-chat to copy the image inside the lobe-chat project.  

![Save Bjornulf Lobechat](screenshots/save_bjornulf_lobechat.png)

## 17 - 💾🖼 Save image as `tmp_api.png` Temporary API ⚠️💣

**Description:**  
Save image for short-term use : ./output/tmp_api.png ⚠️💣  

![Save Temporary API](screenshots/save_tmp_api.png)

## 18 - 💾🖼📁 Save image to a chosen folder name

**Description:**  
Save image in a specific folder : `my_folder/00001.png`, `my_folder/00002.png`, etc...  
Also allow multiple nested folders, like for example : `animal/dog/small`.

![Save Temporary API](screenshots/save_image_to_folder.png)

## 19 - 🦙💬 Ollama Talk

**Description:**  
Use Ollama inside Comfyui. (Require the backend Ollama to be installed and currently running.)  
Use by default the model `llama3.2:3b` and the URL `http://0.0.0.0:11434`. (For custom configuration, use node 63)  

Example of basic usage :  
![Ollama](screenshots/1_ollama_basic.png)  

Example of usage with context, notice that with context you can follow up a conversation, "there" is clearly understood as "Bucharest" :  
![Ollama](screenshots/2_ollama_context.png)  

You can also use `use_context_file` (set to True), this will save the context in a file : `ComfyUI/Bjornulf/ollama_context.txt`.  
This way you can keep using the context without having to connect many nodes connected to each other, just run the same workflow several times.  

### Example in 3 steps of context file conversation

Step 1 : Notice that for now context is empty, so it will be the first message in `ComfyUI/Bjornulf/ollama_context.txt` :  
![Ollama](screenshots/3_ollama_contextFile_1.png)  

Step 2 : Notice that now the number of lines in context file has changed (These are the same as the `updated_context`):  
![Ollama](screenshots/3_ollama_contextFile_2.png)  

Step 3 : Notice that the number of lines keep incrementing.  
![Ollama](screenshots/3_ollama_contextFile_3.png)  

When clicking the `reset Button`, it will also save the context in : `ComfyUI/Bjornulf/ollama_context_001.txt`, `ComfyUI/Bjornulf/ollama_context_002.txt`, etc...  

⚠️ If you want to have an "interactive" conversation, you can enable the option `waiting_for_prompt`.  
When set to True, it will create a `Resume` button, use this to unpause the node and process the prompt.  

### Example in 3 steps of waiting_for_prompt interactive conversation

Step 1: I run the workflow, notice that Show node is empty, the node is pausing the workflow and is waiting for you to edit the prompt. (Notice that at this moment, it is asking for the capital of France.)  
![Ollama](screenshots/ollama_waiting_1.png)  

Step 2: I edit the prompt to change France into China, but the node won't process the request until you click on Resume.    
![Ollama](screenshots/ollama_waiting_2.png)  

Step 3: I click on Resume button, this is when the request is done. Notice that it used China and not France.  
![Ollama](screenshots/ollama_waiting_3.png)  

Other options :  
- You also have `control_after_generate` to force the node to rerun for every workflow run. (Even if there is no modification of the node or its inputs.)  
- You can set `max_tokens` to reduce the size of the answer, a token is about 3 english characters.  
- You can force the answer to be on a single line, can be useful.  
- You have the option to keep the mode in VRAM. (If you plan having to generate many times with the same prompt) - Each run will be significantly faster, but not free your VRAM for something else.  

⚠️ Warning : Using `vram_retention_minutes` might be a bit heavy on your VRAM. Think about if you really need it or not. Most of the time, when using `vram_retention_minutes`, you don't want to have also a generation of image or anything else in the same time.  

## 20 - 📹 Video Ping Pong

**Description:**  
Create a ping-pong effect from a list of images (from a video) by reversing the playback direction when reaching the last frame. Good for an "infinity loop" effect.

![Video Ping Pong](screenshots/video_pingpong.png)

## 21 - 📹 Images to Video

**Description:**  
Combine a sequence of images into a video file.  

![Images to Video](screenshots/imgs2video.png)

❓ I made this node because it supports transparency with webm format. (Needed for rembg)  
Temporary images are stored in the folder `ComfyUI/temp_images_imgs2video/` as well as the wav audio file.

## 22 - 🔲 Remove image Transparency (alpha)

**Description:**  
Remove transparency from an image by filling the alpha channel with a solid color. (black, white or greenscreen)  
Of course it takes in an image with transparency, like from rembg nodes.  
Necessary for some nodes that don't support transparency.  

![Remove Alpha](screenshots/remove_alpha.png)

## 23 - 🔲 Image to grayscale (black & white)

**Description:**  
Convert an image to grayscale (black & white)  

![Image to Grayscale](screenshots/grayscale.png)

Example : I sometimes use it with Ipadapter to disable color influence.  
But you can sometimes also want a black and white image... 

## 24 - 🖼+🖼 Stack two images (Background + Overlay)

**Description:**  
Stack two images into a single image : a background and one (or several) transparent overlay. (allow to have a video there, just send all the frames and recombine them after.)  

![Superpose Images](screenshots/combine_background_overlay.png)

Update 0.11 : Add option to move vertically and horizontally. (from -50% to 150%)  
❗ Warning : For now, `background` is a static image. (I will allow video there later too.)  
⚠️ Warning : If you want to directly load the image with transparency, use my node `🖼 Load Image with Transparency ▢` instead of the `Load Image` node.  

## 25 - 🟩➜▢ Green Screen to Transparency

**Description:**  
Transform greenscreen into transparency.  
Need clean greenscreen ofc. (Can adjust threshold but very basic node.)

![Greenscreen to Transparency](screenshots/greeenscreen_to_transparency.png)

## 26 - 🎲 Random line from input

**Description:**  
Take a random line from an input text. (When using multiple "Write Text" nodes is annoying for example, you can use that and just copy/paste a list from outside.)  
You can change fixed/randomize for `control_after_generate` to have a different text each time you run the workflow. (or not)  

![Random line from input](screenshots/random_line_from_input.png)

## 27 - ♻ Loop (All Lines from input)

**Description:**  
Iterate over all lines from an input text. (Good for testing multiple lines of text.)

![Loop input](screenshots/loop_all_lines.png)

## 28 - 🔢 Text with random Seed

**Description:**  
❗ This node is used to force to generate a random seed, along with text.  
But what does that mean ???  
When you use a loop (♻), the loop will use the same seed for each iteration. (That is the point, it will keep the same seed to compare results.)  
Even with `randomize` for `control_after_generate`, it is still using the same seed for every loop, it will change it only when the workflow is done.  
Simple example without using random seed node : (Both images have different prompt, but same seed)  

![Text with random Seed 1](screenshots/random_seed_1.png)

So if you want to force using another seed for each iteration, you can use this node in the middle.
For example, if you want to generate a different image every time. (aka : You use loop nodes not to compare or test results but to generate multiple images.)  
Use it like that for example : (Both images have different prompt AND different seed)  

![Text with random Seed 2](screenshots/random_seed_2.png)

Here is an example of the similarities that you want to avoid with FLUX with different prompt (hood/helmet) but same seed :

![Text with random Seed 3](screenshots/random_seed_3_flux.png)

Here is an example of the similarities that you want to avoid with SDXL with different prompt (blue/red) but same seed :

![Text with random Seed 4](screenshots/random_seed_4_sdxl.png)

FLUX : Here is an example of 4 images without Random Seed node on the left, and on the right 4 images with Random Seed node :

![Text with random Seed 5](screenshots/result_random_seed.png)

## 29 - 🖼 Load Image with Transparency ▢

**Description:**  
Load an image with transparency.  
The default `Load Image` node will not load the transparency.  

![Load image Alpha](screenshots/load_image_alpha.png)

## 30 - 🖼✂ Cut image with a mask

**Description:**  
Cut an image from a mask.  

![Cut image](screenshots/image_mask_cut.png)

## 31 - 🔊 TTS - Text to Speech (100% local, any voice you want, any language)

**Description:**  
Use my TTS server to generate high quality speech from text, with any voice you want, any language.  
[Listen to the audio example](https://github.com/user-attachments/assets/5a4a67ff-cf70-4092-8f3b-1ccc8023d8c6)  

![TTS](screenshots/tts.png)

❗ Node never tested on windows, only on linux for now. ❗  

Use my TTS server to generate speech from text, based on XTTS v2.  
❗ Of course to use this comfyui node (frontend) you need to use my TTS server (backend) : <https://github.com/justUmen/Bjornulf_XTTS>  
I made this backend for <https://github.com/justUmen/Bjornulf_lobe-chat>, but you can use it with comfyui too with this node.  
After having `Bjornulf_XTTS` installed, you NEED to create a link in my Comfyui custom node folder called `speakers` : `ComfyUI/custom_nodes/Bjornulf_custom_nodes/speakers`  
That link must be a link to the folder where you installed/stored the voice samples you use for my TTS, like `default.wav`.  
If my TTS server is running on port 8020 (You can test in browser with the link <http://localhost:8020/tts_stream?language=en&speaker_wav=default&text=Hello>) and voice samples are good, you can use this node to generate speech from text.  

**Details**  
This node should always be connected to a core node : `Preview audio`.  

My node will generate and save the audio files in the `ComfyUI/Bjornulf_TTS/` folder, followed by the language selected, the name of the voice sample, and the text.  
Example of audio file from the screenshot above : `ComfyUI/Bjornulf_TTS/Chinese/default.wav/你吃了吗.wav`  
You can notice that you don't NEED to select a chinese voice to speak chinese. Yes it will work, you can record yourself and make yourself speak whatever language you want.  
Also, when you select a voice with this format `fr/fake_Bjornulf.wav`, it will create an extra folder `fr` of course. : `ComfyUI/Bjornulf_TTS/English/fr/fake_Bjornulf.wav/hello_im_me.wav`. Easy to see that you are using a french voice sample for an english recording.  

`control_after_generate` as usual, it is used to force the node to rerun for every workflow run. (Even if there is no modification of the node or its inputs.)  
`overwrite` is used to overwrite the audio file if it already exists. (For example if you don't like the generation, just set overwrite to True and run the workflow again, until you have a good result. After you can set it to back to False. (Paraphrasing : without overwrite set to True, It won't generate the audio file again if it already exists in the `Bjornulf_TTS` folder.)  
`autoplay` is used to play the audio file inside the node when it is executed. (Manual replay or save is done in the `preview audio` node.)  

So... note that if you know you have an audio file ready to play, you can still use my node but you do NOT need my TTS server to be running.
My node will just play the audio file if it can find it, won't try to connect th backend TTS server.  
Let's say you already use this node to create an audio file saying `workflow is done` with the Attenborough voice  :  

![TTS](screenshots/tts_end.png)  

As long as you keep exactly the same settings, it will not use my server to play the audio file! You can safely turn the TTS server off, so it won't use your precious VRAM Duh. (TTS server should be using ~3GB of VRAM.)  

Also `connect_to_workflow` is optional, it means that you can make a workflow with ONLY my TTS node to pre-generate the audio files with the sentences you want to use later, example :  
![TTS](screenshots/tts_preload.png)  

If you want to run my TTS nodes along side image generation, i recommend you to use my PAUSE node so you can manually stop the TTS server after my TTS node. When the VRAM is freed, you can the click on the RESUME button to continue the workflow.  
If you can afford to run both at the same time, good for you, but Locally I can't run my TTS server and FLUX at the same time, so I use this trick. :  

![TTS](screenshots/tts_preload_2.png)  

### 32 - 🧑📝 Character Description Generator

**Description:**  
Generate a character description based on a json file in the folder `characters` : `ComfyUI/custom_nodes/Bjornulf_custom_nodes/characters`  
Make your own json file with your own characters, and use this node to generate a description.  

![characters](screenshots/characters.png)
![characters](screenshots/characters2.png)

❗ For now it's very basic node, a lot of things are going to be added and changed !!!  
Some details are unusable for some checkpoints, very much a work in progress, the json structure isn't set in stone either.  
Some characters are included.  

### 33 - ♻ Loop (All Lines from input 🔗 combine by lines)

**Description:**  
Sometimes you want to loop over several inputs but you also want to separate different lines of your output.  
So with this node, you can have the number of inputs and outputs you want. See example for usage.  

![loop combined](screenshots/loop_combined.png)

### 34 - 🧹 Free VRAM hack

**Description:**  
So this is my attempt at freeing up VRAM after usage, I will try to improve that.  

![free vram](screenshots/free_vram_hack1.png)
![free vram](screenshots/free_vram_hack2.png)

For me, on launch ComfyUI is using 180MB of VRAM, after my clean up VRAM node it can go back down to 376MB.  
I don't think there is a clean way to do that, so I'm using a hacky way.  
So, not perfect but better than being stuck at 6GB of VRAM used if I know I won't be using it again...  
Just connect this node with your workflow, it takes anything as input and return it as output.
You can therefore put it anywhere you want.  
❗ Comfyui is using cache to run faster (like not reloading checkpoints), so only use this free VRAM node when you need it.  
❗ For this node to work properly, you need to enable the dev/api mode in ComfyUI. (You can do that in the settings)  
It is also running an "empty/dummy" workflow to free up the VRAM, so it might take a few seconds to take effect after the end of the workflow.  

### 35 - ⏸️ Paused. Resume or Stop ?

**Description:**  
Automatically pause the workflow, and rings a bell when it does. (play the audio `bell.m4a` file provided)  

![pause resume stop](screenshots/pause1.png)
![pause resume stop](screenshots/pause2.png)
![pause resume stop](screenshots/pause3.png)

You can then manually resume or stop the workflow by clicking on the node's buttons.  
I do that let's say for example if I have a very long upscaling process, I can check if the input is good before continuing. Sometimes I might stop the workflow and restart it with another seed.  
You can connect any type of node to the pause node, above is an example with text, but you can send an IMAGE or whatever else, in the node `input = output`. (Of course you need to send the output to something that has the correct format...)  

### 36 - ⏸️🔍 Paused. Select input, Pick one

**Description:**  
Automatically pause the workflow, and rings a bell when it does. (play the audio `bell.m4a` file provided)  

![pick input](screenshots/pick.png)

You can then manually select the input you want to use, and resume the workflow with it.  
You can connect this node to anything you want, above is an example with IMAGE. But you can pick whatever you want, in the node `input = output`.  

### 37 - 🎲🖼 Random Image

**Description:**  
Just take a random image from a list of images.  

![random image](screenshots/random_image.png)

### 38 - ♻🖼 Loop (Images)

**Description:**  
Loop over a list of images.  

![loop images](screenshots/loop_images.png)

Usage example : You have a list of images, and you want to apply the same process to all of them.  
Above is an example of the loop images node sending them to an Ipadapter workflow. (Same seed of course.)  

### 39 - ♻ Loop (✒🗔 Advanced Write Text)

**Description:**  
If you need a quick loop but you don't want something too complex with a loop node, you can use this combined write text + loop.  

![loop write text](screenshots/loop_write_text.png)

It will take the same special syntax as the Advanced write text node `{blue|red}`, but it will loop over ALL the possibilities instead of taking one at random.  
0.40 : You can also use variables `<name>` in the loop.  

### 40 - 🎲 Random (Model+Clip+Vae) - aka Checkpoint / Model

**Description:**  
Just simply take a trio at random from a load checkpoint node.  

![random checkpoint](screenshots/random_checkpoint.png)

Notice that it is using the core Load checkpoint node. It means that all checkpoint will be preloaded in memory.  

Details :  
- It will take more VRAM, but it will be faster to switch between checkpoints.  
- It can't give you the currently loaded checkpoint name's.  

Check node number 41 before deciding which one to use.  

### 41 - 🎲 Random Load checkpoint (Model Selector)

**Description:**  
This is another way to select a load checkpoint node randomly.  

![pick input](screenshots/random_load_checkpoint.png)

It will not preload all the checkpoints in memory, so it will be slower to switch between checkpoints.  
But you can use more outputs to decide where to store your results. (`model_folder` is returning the last folder name of the checkpoint.)  
I always store my checkpoints in a folder with the type of the model like `SD1.5`, `SDXL`, etc... So it's a good way for me to recover that information quickly.  

Details :  
- Note that compared to node 40, you can't have separate configuration depending of the selected checkpoint. (For example `CLIP Set Last Layer` node set at -2 for a specific model, or a separate vae or clip.) Aka : All models are going to share the exact same workflow.  

Check node number 40 before deciding which one to use.  
Node 53 is the loop version of this node.  

NOTE : If you want to load a single checkpoint but want to extract its folder name (To use the checkpoint name as a folder name for example, or with if/else node), you can use my node 41 with only one checkpoint. (It will take one at random, so... always the same one.)    

### 42 - ♻ Loop (Model+Clip+Vae) - aka Checkpoint / Model

![pick input](screenshots/loop_checkpoint.png)

**Description:**  
Loop over all the trios from several checkpoint node.  

### 43 - 📥🖼📂 Load Images from output folder

**Description:**  
Quickly select all images from a folder inside the output folder. (Not recursively.)  

![pick input](screenshots/load_images_folder.png)

So... As you can see from the screenshot the images are split based on their resolution.  
It's also not possible to edit dynamically the number of outputs, so I just picked a number : 4.  
The node will separate the images based on their resolution, so with this node you can have 4 different resolutions per folder. (If you have more than that, maybe you should have another folder...)  
To avoid error or crash if you have less than 4 resolutions in a folder, the node will just output white tensors. (white square image.)  
So this node is a little hacky for now, but i can select my different characters in less than a second.  
If you want to know how i personnaly save my images for a specific character, here is part of my workflow (Notice that i personnaly use / for folders because I'm on linux) :  
![pick input](screenshots/character_save.png)  
In this example I put "character/" as a string and then combine with "nothing". But it's the same if you do "character" and then combine with "/". (I just like having a / at the end of my folder's name...)  

If you are satisfied with this logic, you can then select all these nodes, right click and `Convert to Group Node`, you can then have your own customized "save character node" :  
![pick input](screenshots/bjornulf_save_character_group.png)

Here is another example of the same thing but excluding the save folder node :  
![pick input](screenshots/bjornulf_save_character_group2.png)

⚠️ If you really want to regroup all the images in one flow, you can use my node 47 `Combine images` to put them all together.  

### 44 - 🖼👈 Select an Image, Pick

**Description:**  
Select an image from a list of images.  

![pick input](screenshots/select_image.png)  

Useful in combination with my Load images from folder and preview image nodes.  

You can also of course make a group node, like this one, which is the same as the screenshot above :  
![pick input](screenshots/select_image_group.png)

### 45 - 🔀 If-Else (input / compare_with)

**Description:**  
Complex logic node if/else system.  

![if else](screenshots/if_0.png)  

If the `input` given is equal to the `compare_with` given in the widget, it will forward `send_if_true`, otherwise it will forward `send_if_false`. (If no `send_if_false` it will return `None`.)  
You can forward anything, below is an example of forwarding a different size of latent space depending if it's SDXL or not.  

![if else](screenshots/if_0_1.png)

Here is an example of the node with all outputs displayed with Show text nodes :  

![if else](screenshots/if_1.png)

`send_if_false` is optional, if not connected, it will be replaced by `None`.  

![if else](screenshots/if_2.png)

If-Else are chainables, just connect `output` to `send_if_false`.  
⚠️ Always simply test `input` with `compare_with`, and connect the desired value to `send_if_true`. ⚠️  
Here a simple example with 2 If-Else nodes (choose between 3 different resolutions).  
❗ Notice that the same write text node is connected to both If-Else nodes input :  

![if else](screenshots/if_3.png)

Let's take a similar example but let's use my Write loop text node to display all 3 types once :  

![if else](screenshots/if_4.png)

If you understood the previous examples, here is a complete example that will create 3 images, landscape, portrait and square :  

![if else](screenshots/if_5.png)

Workflow is hidden for simplicity, but is very basic, just connect latent to Ksampler, nothing special.)  
You can also connect the same advanced loop write text node with my save folder node to save the images (landscape/portrait/square) in separate folders, but you do you...  

### 46 - 🖼🔍 Image Details

**Description:**  
Display the details of an image. (width, height, has_transparency, orientation, type)  
`RGBA` is considered as having transparency, `RGB` is not.  
`orientation` can be `landscape`, `portrait` or `square`.  

![image details](screenshots/image_details_1.png)

### 47 - 🖼🔗 Combine Images

**Description:**  
Combine multiple images (A single image or a list of images.)  
If you want to merge several images into a single image, check node 60 or 61.  

There are two types of logic to "combine images". With "all_in_one" enabled, it will combine all the images into one tensor.  
Otherwise it will send the images one by one. (check examples below) :  

This is an example of the "all_in_one" option disabled (Note that there are 2 images, these are NOT side by side, they are combined in a list.) :  

![combine images](screenshots/combine_images_1.png)

But for example, if you want to use my node `select an image, pick`, you need to enable `all_in_one` and the images must all have the same resolution.  

![combine images](screenshots/combine_images_2.png)

You can notice that there is no visible difference when you use `all_in_one` with `preview image` node. (this is why I added the `show text` node, note that show text will make it blue, because it's an image/tensor.)  

When you use `combine image` node, you can actually also send many images at once, it will combine them all.  
Here is an example with `Load images from folder` node, `Image details` node and `Combine images` node. (Of course it can't have `all_in_one` set to True in this situation because the images have different resolutions) :  

![combine images](screenshots/combine_images_3.png)

Here another simple example taking a few selected images from a folder and combining them (For later processing for example) :  

![combine images](screenshots/combine_images_4.png)

### 48 - 🔀🎲 Text scrambler (🧑 Character)

**Description:**  
Take text as input and scramble (randomize) the text by using the file `scrambler/character_scrambler.json` in the comfyui custom nodes folder.  

![scrambler character](screenshots/scrambler_character.png)

### 49 - 📹👁 Video Preview

**Description:**  
This node takes a video path as input and displays the video.  

![video preview](screenshots/video_preview.png)

### 50 - 🖼➜📹 Images to Video path (tmp video)

**Description:**  
This node will take a list of images and convert them to a temporary video file.  
❗ Update 0.50 : You can now send audio to the video. (audio_path OR audio TYPE)  

![image to video path](screenshots/image_to_video_path.png)

### 51 - 📹➜🖼 Video Path to Images

**Description:**  
This node will take a video path as input and convert it to a list of images.  

![video path to image](screenshots/video_path_to_image.png)

In the above example, I also take half of the frames by setting `frame_interval` to 2.  
Note that i had 16 frames, on the top right preview you can see 8 images.  

### 52 - 🔊📹 Audio Video Sync

**Description:**  

This node is an overengineered node that will try to synchronize the duration of an audio file with a video file.  
❗ Video ideally needs to be a loop, check my ping pong video node if needed.
The main goal of this synchronization is to have a clean transition between the end and the beginning of the video. (same frame)  
You can then chain up several video and they will transition smoothly.

Some details, this node will :  
- If video slightly too long : add silence to the audio file.  
- If video way too long : will slow down the video up to 0.50x the speed + add silence to the audio. (now editable)  
- If audio slightly too long : will speed up video up to 1.5x the speed. (now editable)  
- If video way too long : will speed up video up to 1.5x the speed + add silence to the audio.  

It is good like for example with MuseTalk <https://github.com/chaojie/ComfyUI-MuseTalk>

Here is an example of the `Audio Video Sync` node, notice that it is also convenient to recover the frames per second of the video, and send that to other nodes. (Spaghettis..., deal with it. 😎 If you don't understand it, you can test it.) :  

![audio sync video](screenshots/audio_sync_video.png)

❗ Update 0.50 : audio_duration is now optional, if not connected it will take it from the audio.  
❗ Update 0.50 : You can now send the video with a list of images OR a video_path, same for audio : AUDIO or audio_path.  

New v0.50 layout, same logic :  

![audio sync video](screenshots/audio_sync_video_new.png)

### 53 - ♻ Loop Load checkpoint (Model Selector)

**Description:**  
This is the loop version of node 41. (check there for similar details)  
It will loop over all the selected checkpoints.  

❗ The big difference with 41 is that checkpoints are preloaded in memory. You can run them all faster all at once.  
It is a good way to test multiple checkpoints quickly.  

![loop model selector](screenshots/loop_model_selector.png)

### 54 - ♻ Loop Lora Selector

**Description:**  
Loop over all the selected Loras.  

![loop lora selector](screenshots/loop_lora_selector.png)  

Above is an example with Pony and several styles of Lora.  

Below is another example, here with flux, to test if your Lora training was undertrained, overtrained or just right :  

![loop lora selector](screenshots/loop_lora_selector_flux.png)

### 55 - 🎲 Random Lora Selector

**Description:**  
Just take a single Lora at random from a list of Loras.  

![random lora selector](screenshots/random_lora_selector.png)

### 56 - ♻📑📝 Loop Sequential (Integer)

**Description:**  
This loop works like a normal loop, BUT it is sequential : It will run only once for each workflow run !!!  
The first time it will output the first integer, the second time the second integer, etc...  
When the last is reached, the node will STOP the workflow, preventing anything else to run after it.  
Under the hood it is using a single file `counter_integer.txt` in the `ComfyUI/Bjornulf` folder.  
❗ Do not use more than one node like this one in a workflow, because they will share the same `counter_integer.txt` file. (unexpected behaviour.)
Update 0.57: Now also contains the next counter in the reset button.  

![loop sequential integer](screenshots/loop_sequential_integer_1.png)  
![loop sequential integer](screenshots/loop_sequential_integer_2.png)  
![loop sequential integer](screenshots/loop_sequential_integer_3.png)  
![loop sequential integer](screenshots/loop_sequential_integer_4.png)  

### 57 - ♻📑 Loop Sequential (input Lines)

**Description:**  
This loop works like a normal loop, BUT it is sequential : It will run only once for each workflow run !!!  
The first time it will output the first line, the second time the second line, etc...  
You also have control of the line with +1 / -1 buttons.  
When the last is reached, the node will STOP the workflow, preventing anything else to run after it.  
Under the hood it is using the file `counter_lines.txt` in the `ComfyUI/Bjornulf` folder.  

Here is an example of usage with my TTS node : when I have a list of sentences to process, if i don't like a version, I can just click on the -1 button, tick "overwrite" on TTS node and it will generate the same sentence again, repeat until good.  
❗ Do not use more than one node like this one in a workflow, because they will share the same `counter_lines.txt` file. (unexpected behaviour.)

![loop sequential line](screenshots/loop_sequential_lines.png)  

Update 0.57: Now also contains the next counter in the reset button.  
If you want to be able to predict the next line, you can use node 68, to Add line numbers.

### 58 - 📹🔗 Concat Videos

**Description:**  
Take two videos and concatenate them. (One after the other in the same video.)  
Convert a video, can use FFMPEG_CONFIG_JSON. (From node 76 / 77)    

![concat video](screenshots/concat_video.png)  

### 59 - 📹🔊 Combine Video + Audio

**Description:**  
Simply combine video and audio together.  
Video : Use list of images or video path.   
Audio : Use audio path or audio type.  

![combine video audio](screenshots/combine_video_audio.png)  

### 60 - 🖼🖼 Merge Images/Videos 📹📹 (Horizontally)

**Description:**  
Merge images or videos horizontally.  

![merge images](screenshots/merge_images_h.png)  

Here is one possible example for videos with node 60 and 61 :  

![merge videos](screenshots/merge_videos.png)  

### 61 - 🖼🖼 Merge Images/Videos 📹📹 (Vertically)

**Description:**  
Merge images or videos vertically.  

![merge images](screenshots/merge_images_v.png)  

Here is one possible example for videos with node 60 and 61 :  

![merge videos](screenshots/merge_videos.png)  

### 62 - 🦙👁 Ollama Vision

**Description:**  
Take an image as input and will describe the image. Uses `moondream` by default, but can select anything with node 63.  

![ollama vision](screenshots/ollama_vision.png)  

### 63 - 🦙 Ollama Configuration ⚙

**Description:**  
Use custom configurations for Ollama Talk and Vision.  
You can change the ollama Url and the model used.  
Some vision models can also do text to a certain extent.  
Example of a `Ollama Vision Node` and `Ollama Talk Node` using the same `Ollama Configuration Node` :  

![ollama config](screenshots/ollama_config.png)  

### 64 - 🦙 Ollama Job Selector 💼

**Description:**  
Select a personnality for your Ollama Talk Node, set it to `None` for just chat.  
If you want to write your own, just set it to `None` and write your prompt as prefix.  

![ollama job](screenshots/ollama_job.png)  

### 65 - 🦙 Ollama Persona Selector 🧑

**Description:**  
Select a personnality for your Ollama Talk Node.  
If you want to write your own, just set it to `None` and write your prompt as prefix.  
Below, an example of a crazy scientist explaining gravity. (Notice that the LLM was smart enough to understand the typo) :  

![ollama persona](screenshots/ollama_persona.png)  

### 66 - 🔊➜📝 STT - Speech to Text

**Description:**  
Use `faster-whisper` to transform an AUDIO type or audio_path into text. (Autodetect language)  

![stt](screenshots/stt_1.png)  
![stt](screenshots/stt_2.png)  

### 67 - 📝➜✨ Text to Anything

**Description:**  
Sometimes you want to force a node to accept a STRING.  
You can't do that for example if the node is taking a LIST as input.  
This node can be used in the middle to force a STRING to be used anyway.  
Below is an example of that with my TTS node.  

![text to anything](screenshots/text_to_anything.png)  

### 68 - ✨➜📝 Anything to Text

**Description:**  
Sometimes you want to force something to be a STRING.  
Most outputs are indeed text, even though they might be unusable.  
This node ignore this fact and simply convert the input to a simple STRING.  

### 69 - 🔢 Add line numbers

**Description:**  

This node will just add line numbers to text.  
Useful when you want to use node 57 that will loop over input lines. (You can read/predict the next line.)  

![add line numbers](screenshots/add_line_numbers.png)  

### 70 - 📏 Resize Image Percentage

**Description:**  

Resize an image by percentage.  

![resize percentage](screenshots/resize_percentage.png)  

### 71 - 👁 Show (Int)

**Description:**  
Basic node, show an INT. (You can simply drag any INT node and it will be recommended.)  

![show int](screenshots/show_int.png)  

### 72 - 👁 Show (Float)

**Description:**  
Basic node, show a FLOAT. (You can simply drag any FLOAT node and it will be recommended.)  

![show float](screenshots/show_float.png)  

### 73 - 👁 Show (String/Text)

**Description:**  
Basic node, show a STRING. (You can simply drag any STRING node and it will be recommended.)  

![show string](screenshots/show_string_1.png)  
![show string](screenshots/show_string_2.png)  

### 74 - 👁 Show (JSON)

**Description:**  
This node will take a STRING and format it as a readable JSON. (and pink)  

![show json](screenshots/show_json.png)  
![show json](screenshots/show_json2.png)  

### 75 - 📝➜📝 Replace text

**Description:**  
Replace text with another text, allow regex and more options, check examples below :  

![text replace](screenshots/text_replace_1.png)  
![text replace](screenshots/text_replace_2.png)  
![text replace](screenshots/text_replace_3.png)  

0.70 ： Text replace now have multiline option for regex.

### 76 - ⚙📹 FFmpeg Configuration 📹⚙

**Description:**  
Create a FFMPEG_CONFIG_JSON, it will contains a JSON that can be used by other nodes :
- Convert video
- Concat videos
- Concat video from list

![text replace](screenshots/ffmpeg_conf.png)  

### 77 - 📹🔍 Video details ⚙

**Description:**  
Extract details from a video_path.  
You can use the all-in-one FFMPEG_CONFIG_JSON with other nodes or just use the other variables as your want.  

![video details](screenshots/video_details.png)  

### 78 - 📹➜📹 Convert Video

**Description:**  
Convert a video, can use FFMPEG_CONFIG_JSON.  

![convert video](screenshots/convert_video.png)  

#### 79 - 📹🔗 Concat Videos from list

**Description:**  
Take a list of videos (one per line) and concatenate them. (One after the other in the same video.)  
Can use FFMPEG_CONFIG_JSON. (From node 76 / 77)    

![concat video list](screenshots/concat_video_list.png)  

#### 80 - 🩷 Empty Latent Selector

**Description:**  
Tired of setting up latent space manually ?  
Select one from my custom list of formats.  
Just connect that to your KSampler.  

![empty_latent](screenshots/empty_latent.png)  

#### 81 - 🔥📝 Text Generator 📝🔥

**Description:**  
Main node to generate content, doesn't really do much by itself, just `camera angle` and `multicharacter action`. (For example : `... eat picnic, view from above.`)  
BUT, you can connect others `Text Generator Nodes` to it.  

⚠️ Warning for "Text Generator" : This node is JUST writing text, text is then interpreted by a checkpoint (SD1.5, SDXL, Flux...) to generate an image.  
Some models are very bad at doing some things, so DON'T EXPECT for everything you do to work properly all the time with every checkpoints or loras. (This node was made with FLUX in mind.)  

Below is a Tutorial on how to use all my `Text Generator nodes`. I did that small tutorial in 8 steps:  

Step 1 : You use the main Text Generator node, it will write general details about the image (here `camera_angle` and `shot_type`) - For now I just combine the text to a simple "write text" that will send `swamp monster` :  
![textgen](screenshots/textgen.png)  

Step 2 : Add a specific style to your image :  
![textgen_style](screenshots/textgen_style.png)  

Step 3 : Add scene/background to your image :  
![textgen_scene](screenshots/textgen_scene.png)  

Step 4 : Add a character to the scene using a character node, instead of the Write text Node.  
I will remove the "swamp monster" from the "write text node" and use my Character Node instead, I will use it to create an agressive dragon with lighting powers :  
![textgen_char](screenshots/textgen_char.png)  

Step 5 : Character nodes (Male/Female and creatures) can contain more than one character. (But they will share the same characteristics)  
Below I removed the dragon and I created 2 "Character male" fighting by using the `multi_char_action` from the main node. (You can set it to CUSTOM and write your own action too.)  
![textgen_2chars](screenshots/textgen_2chars.png)  

Step 5 : Let's try to add a location for the character, I want to put it on the left of the image. Here is a failure with the SDXL model I have been using all along :    
![textgen_charposition_FAIL_sdxl](screenshots/textgen_charposition_FAIL_sdxl.png)  

Step 6 : Switch to FLUX to test the `location_on_image` feature (which is working) :  
![textgen_location_on_image_flux](screenshots/textgen_location_on_image_flux.png)  

Step 7 : Switch to API black Forest Lab with FLUX Ultra, using my API custom node 109.  
If you want several characters with different characteristics (like `location_on_image` or whatever), you can chain several Character Nodes together by connecting them to each other.  
You can see below that I asked for 2 tiny dragons on the left and a zombie on the right.  
![textgen_Complex_ULTRA](screenshots/textgen_Complex_ULTRA.png)  

Step 8 : And to end this tutorial, I will disable the Zombie, I will add an outfit (here a `floral armor`), I will also add a `pose` node for the character and also connect this pose node to an `object` node. (They will together make the character `hold a book` and put his `hand on chin`)  
![textgen_final](screenshots/textgen_final.png)  

#### 82 - 👩‍🦰📝 Text Generator (Character Female)

**Description:**  
Generate text related to female characters.  
Need to be connected to "Text Generator" main node.  

⚠️ For "Text Generator" tutorial see node 81.  

#### 83 - 👨‍🦰📝 Text Generator (Character Male)

**Description:**  
Generate text related to male characters.  

⚠️ For "Text Generator" tutorial see node 81.  

#### 84 - 👾📝 Text Generator (Character Creature)

**Description:**  
Generate text related to creatures. (characters)  

⚠️ For "Text Generator" tutorial see node 81.  

#### 85 - 💃🕺📝 Text Generator (Character Pose)

**Description:**  
Generate text related to the pose of characters.  

⚠️ For "Text Generator" tutorial see node 81.  

#### 86 - 🔧👨‍🔧📝 Text Generator (Object for Character)

**Description:**  
Generate text related to an object connected to a pose, that is connected to a character.  

⚠️ For "Text Generator" tutorial see node 81.  

#### 87 - 🌄📝 Text Generator (Scene)

**Description:**  
Generate text related to a specific scene, connects directly to the main text generator.  

⚠️ For "Text Generator" tutorial see node 81.  

#### 88 - 🎨📝 Text Generator (Style)

**Description:**  
Generate text related to a specific style, connects directly to the main text generator.  

⚠️ For "Text Generator" tutorial see node 81.  

#### 89 - 👗 Text Generator (Outfit Female)

**Description:**  
Generate text related to a specific female outfit.  

⚠️ For "Text Generator" tutorial see node 81.  

#### 90 - 👚 Text Generator (Outfit Male)

**Description:**  
Generate text related to a specific male outfit.  

⚠️ For "Text Generator" tutorial see node 81.  

#### 91 - ♻🔥📝 List Looper (Text Generator)

**Description:**  
Loop made to loop over elements for the main node text generator.  

All the `List Looper` nodes have the same logic, you should be able to use them all the same way.  
Here is an example with node 92 (list looper scenes), looping over all the different `weather_condition` :  

![listlooper_USE](screenshots/listlooper_USE.png)  

⚠️ Note, if you want to Loop over the elements `One by One`, Not all-in one, DO NOT use this `list looper nodes` !!  
You can just convert the element you want as input and double click to create a new node that you can set to "increment".  

Example, here you can see that the value was "incremented", aka changed to the next from the list, the next run will then have the next value from the list (and so on) :  
![listlooper_notUSE](screenshots/listlooper_notUSE.png)  

#### 92 - ♻🌄📝 List Looper (Text Generator Scenes)

**Description:**  
Loop made to loop over elements for the node scenes.  

⚠️ For "List Looper" tutorial see node 91.  

#### 93 - ♻🎨📝 List Looper (Text Generator Styles)

**Description:**  
Loop made to loop over elements for the node style.  

⚠️ For "List Looper" tutorial see node 91.  

#### 94 - ♻💃🕺📝 List Looper (Text Generator Poses)

**Description:**  
Loop made to loop over elements for the node poses.  

⚠️ For "List Looper" tutorial see node 91.  

#### 95 - ♻👨‍🦰👩‍🦰👾 List Looper (Text Generator Characters)

**Description:**  
Loop made to loop over elements for the node charceter (male/female/creature).  

⚠️ For "List Looper" tutorial see node 91.  

#### 96 - ♻👚 List Looper (Text Generator Outfits Male)

**Description:**  
Loop made to loop over elements for the node for male outfits.  

⚠️ For "List Looper" tutorial see node 91.  

#### 97 - ♻👗 List Looper (Text Generator Outfits Female)

**Description:**  
Loop made to loop over elements for the node for female outfits.  

⚠️ For "List Looper" tutorial see node 91.  

#### 98 - 📥 Load checkpoint SD1.5 (+Download from CivitAi)

**Description:**  
This is the same as a basic "Load checkpoint" node, but the list is from civitai (not your local folder).  
It will also download the file from civitai if you don't have it on your computer yet. (You need an api token from your account. - Find yours on civitai.com settings. -)  
This is the `sd1.5` version, it will download the models in : `ComfyUI/models/checkpoints/Bjornulf_civitAI/sd1.5`  
After downloading, you can keep using this node as is to load your checkpoint, or use the downloaded model from a basic "Load checkpoint" node.  

![civitai_load_sd15](screenshots/civitai_load_sd15.png)  

#### 99 - 📥 Load checkpoint SDXL (+Download from CivitAi)

**Description:**  
This is the same as a basic "Load checkpoint" node, but the list is from civitai (not your local folder).  
It will also download the file from civitai if you don't have it on your computer yet. (You need an api token from your account. - Find yours on civitai.com settings. -)  
This is the `sdxl_1.0` version, it will download the models in : `ComfyUI/models/checkpoints/Bjornulf_civitAI/sdxl_1.0`  
After downloading, you can keep using this node as is to load your checkpoint, or use the downloaded model from a basic "Load checkpoint" node.  

![civitai_load_sdxl](screenshots/civitai_load_sdxl.png)  

#### 100 - 📥 Load checkpoint Pony (+Download from CivitAi)

**Description:**  
This is the same as a basic "Load checkpoint" node, but the list is from civitai (not your local folder).  
It will also download the file from civitai if you don't have it on your computer yet. (You need an api token from your account. - Find yours on civitai.com settings. -)  
This is the `pony` version, it will download the models in : `ComfyUI/models/checkpoints/Bjornulf_civitAI/pony`  
After downloading, you can keep using this node as is to load your checkpoint, or use the downloaded model from a basic "Load checkpoint" node.  

![civitai_load_pony](screenshots/civitai_load_pony.png)  

#### 101 - 📥 Load checkpoint FLUX Dev (+Download from CivitAi)

**Description:**  
This is the same as a basic "Load checkpoint" node, but the list is from civitai (not your local folder).  
It will also download the file from civitai if you don't have it on your computer yet. (You need an api token from your account. - Find yours on civitai.com settings. -)  
This is the `flux_d` version, it will download the models in : `ComfyUI/models/checkpoints/Bjornulf_civitAI/flux_d`  
After downloading, you can keep using this node as is to load your checkpoint, or use the downloaded model from a basic "Load checkpoint" node.  

🚧 Work in progress, need to manually clean up list, diffusers, etc.. ? 🚧

#### 102 - 📥 Load checkpoint FLUX Schnell (+Download from CivitAi)

**Description:**  
This is the same as a basic "Load checkpoint" node, but the list is from civitai (not your local folder).  
It will also download the file from civitai if you don't have it on your computer yet. (You need an api token from your account. - Find yours on civitai.com settings. -)  
This is the `flux_s` version, it will download the models in : `ComfyUI/models/checkpoints/Bjornulf_civitAI/flux_s`  
After downloading, you can keep using this node as is to load your checkpoint, or use the downloaded model from a basic "Load checkpoint" node.  

🚧 Work in progress, need to manually clean up list, diffusers, etc.. ? 🚧

#### 103 - 📥👑 Load Lora SD1.5 (+Download from CivitAi)

**Description:**  
This is the same as a basic "Load lora" node, but the list is from civitai (not your local folder).  
It will also download the file from civitai if you don't have it on your computer yet. (You need an api token from your account. - Find yours on civitai.com settings. -)  
This is the `sd_1.5` version, it will download the lora in : `ComfyUI/models/loras/Bjornulf_civitAI/sd_1.5`  
After downloading, you can keep using this node as is to load your lora, or use the downloaded lora from a basic "Load lora" node.  

Below is an example with Lora "Colorize" :  

![civitai_lora_sd15](screenshots/civitai_lora_sd15.png)  

#### 104 - 📥👑 Load Lora SDXL (+Download from CivitAi)

**Description:**  
This is the same as a basic "Load lora" node, but the list is from civitai (not your local folder).  
It will also download the file from civitai if you don't have it on your computer yet. (You need an api token from your account. - Find yours on civitai.com settings. -)  
This is the `sdxl_1.0` version, it will download the lora in : `ComfyUI/models/loras/Bjornulf_civitAI/sdxl_1.0`  
After downloading, you can keep using this node as is to load your lora, or use the downloaded lora from a basic "Load lora" node.  

Below is an example with Lora "Better faces" :  

![civitai_lora_sdxl](screenshots/civitai_lora_sdxl.png)  

#### 105 - 📥👑 Load Lora Pony (+Download from CivitAi)

**Description:**  
This is the same as a basic "Load lora" node, but the list is from civitai (not your local folder).  
It will also download the file from civitai if you don't have it on your computer yet. (You need an api token from your account. - Find yours on civitai.com settings. -)  
This is the `pony` version, it will download the lora in : `ComfyUI/models/loras/Bjornulf_civitAI/pony`  
After downloading, you can keep using this node as is to load your lora, or use the downloaded lora from a basic "Load lora" node.  

![civitai_lora_pony](screenshots/civitai_lora_pony.png)  

#### 106 - ☁🎨 API Image Generator (FalAI) 🎨☁

**Description:**  
Generate images with only a token.  
This is the `fal.ai` version and will save the image in `ComfyUI/output/API/CivitAI/`

![api falai](screenshots/api_falai.png)  

#### 107 - ☁🎨 API Image Generator (CivitAI) 🎨☁

**Description:**  
Generate images with only a token.  
This is the `civit.ai` version and will save the image in `ComfyUI/output/API/CivitAI/`  
⚠️ Warning : Civitai isn't the best reliable API, sometimes it doesn't answer, or take long time to answer, some urn don't answer as well as others, etc...  
Use it at your own risks, I do not recommend running anything "costly" using their API, like Flux Ultra, etc... (Use the website instead with blue buzz)  
API requests (like from this node) are using yellow buzz.  

![api civitai](screenshots/api_civitai.png)  

#### 108 - ☁👑 Add Lora (API ONLY - CivitAI) 👑☁

**Description:**  
Use lora with the API, below is an example to see clearly with the same seed the different with/without/lora.  

![api civitai lora](screenshots/api_civitai_lora.png)  

#### 109 - ☁🎨 API Image Generator (Black Forest Labs - Flux) 🎨☁

**Description:**  
Generate an image with the Black Forest Labs API. (flux)  

![api black forest](screenshots/api_black_forest.png)  

#### 110 - ☁🎨 API Image Generator (Stability - Stable Diffusion) 🎨☁

**Description:**  
Generate an image with the Stability API. (sd3)  

![api stability](screenshots/api_stability.png)  

#### 111 - ✨➜🔢 Anything to Int

**Description:**   

Just convert anything to a valid INT. (integer)  

![Anything to Int](screenshots/anything_to_int.png)  

#### 112 - ✨➜🔢 Anything to Float

**Description:**  

Just convert anything to a valid FLOAT. (floating number)  

![Anything to Float](screenshots/anything_to_float.png)  

#### 113 - 📝🔪 Text split in 5

**Description:**  

Take a single input and split it in 5 with a delimiter (newline by default).  
It can also ignore everything on the left side of a `=` symbol if you want to use a "variable type format".  

![Text split in 5](screenshots/split_in_5.png)  

#### 114 - 📥👑 Load Lora with Path

**Description:**  

Load a lora by using it's path.  

![load lora with path](screenshots/load_lora_with_path.png)  

Here is a complex practical example using node 113, 114, 112 :  
![load lora with path](screenshots/load_lora_with_path_COMPLEX.png)  

#### 115 - 📥 Load Text From Bjornulf Folder

**Description:**  

Just select a file from the folder `Bjornulf/Text` folder, it will recover its content.  
It is made to be used with node 15 `Save Text`.  

![Load Text](screenshots/load_text_from_Bjornulf.png)  

#### 116 - 📥 Load Text From Path 

**Description:**  

Just give the path of the file, it will recover its content.  

![Load Text](screenshots/load_text_requirements.png)  

If you want, with `Load Text From Path` you can also recover the elements in "Bjornulf/Text" by just adding it:  

![Load Text](screenshots/load_text_PATH.png)  

#### 117 - 📝👈 Line selector (🎲 or ♻ or ♻📑)

**Description:**  

Select a line from input text. If set to 0 it will take a line at random.  
If line taken at random,. it will not take a line starting with the symbol `#`.  
So use that if you want to ignore a line.  

![Line Selector](screenshots/line_selector.png)  

#### 118 - 🔊 TTS Configuration ⚙

**Description:**  

New optional configuration node to connect to TTS node, it can request a list of speakers for a given language and replace in the main TTS node :  
- The URL.
- The language.
- The speaker.
Connect them only if you want to replace them with the one from the configuration node.  

![tts config](screenshots/tts_config.png)  

#### 119 - 📥👑 Load Lora Hunyuan Video (+Download from CivitAi)

**Description:**  

Take a CivitAI Lora to use with Hunyuan. (NSFW list not on github of course.)

The workflow below is included : `workflows/HUNYUAN_basic_lora.json`) :  

![hunyuan lora](screenshots/hunyuan_lora.png)  

#### 120 - 📝➜🔊 Kokoro - Text to Speech

**Description:**  
Another Text to Speech node based on Kokoro. : https://github.com/thewh1teagle/kokoro-onnx  
Lightweight, much simpler, no configuration and fully integrated into Comfyui. (No external backend to run.)  

![tts kokoro](screenshots/kokoro_tts.png)  

#### 121 - 💾 Huggingface Downloader

**Description:**  
This node allows you to download models/vae/unet etc... directly from huggingface with your access token.  

![huggingface dl](screenshots/huggingface_dl.png)  

#### 122 - 👑 Combine Loras, Lora stack

**Description:**  
If you want to have multiple loras in a single node, well this is it.  

![Lora stack](screenshots/lora_stacks.png)  

#### 123 - 💾 Save Global Variables

**Description:**  
So if you know how to use variables with my nodes, this node gives you the opportunity to create global variables.  
This node is very simple, it will just append (or overwrite) the file : `Bjornulf/GlobalVariables.txt` (You can edit that manually if you want.)

![Global Save](screenshots/global_save.png)  

#### 124 - 📥 Load Global Variables

**Description:**  
This node will load the global variables as text from the file `Bjornulf/GlobalVariables.txt`.  
Here is an example of usage save/load :

![Global images](screenshots/global_load.png)  

#### 125 - 📝👈 Model-Clip-Vae selector (🎲 or ♻ or ♻📑)

**Description:**  
If you want to use and manage multiple models/clip/vae : this is the universal node for it.  
You can run them in a LOOP, one at RANDOM, a LOOP SEQUENTIAL (one at a time for each workflow run) and even SELECT a specific one.  

![model clip vae selector](screenshots/model_clip_vae_selector.png)  

#### 126 - 📒 Note

**Description:**  
Sometimes I want to add a NOTE but I want this note to be connected to a specific spaghetti.  
So you can use this to write details about a specific connection, it will move with it.  

You can do whatever you want of course, below is an example about HunYuan video generation. (You can quickly switch connection to the rest of your workflow, depending on what you want to run.)

![note](screenshots/note.png)  

#### 127 - 🖼📒 Image Note

**Description:**  
You can use this node to have it show a previously generated image and some custom text. (Use image_path or IMAGE type.)  
![Image note](screenshots/image_note.png)  

You can use the text to display the prompt used to generate the image for example.

Sometimes I want to display an image to explain what something specific is doing visually. (For example a stack of loras will have a specific style.)  
Here is a complex example on how i use that, for a list of loras stacks. (I then "select" a style by using node `125 - Model-Clip-Vae selector`)  

![Image note](screenshots/image_notes.png)  

#### 128 - 🖼👁 Preview (first) image

**Description:**  
This node can display a preview of an image...  
- But also can take a list of images and preview only the first image. (Useful for video, it will take the first image.)  
- But can also take as input the full path of an image.  
- BUT it can also take a video path as input and extract the first frame of it.  
Very useful for testing when working with videos.  
Below is a visual example of what I just said :  

![First image preview](screenshots/first_image_preview.png)  

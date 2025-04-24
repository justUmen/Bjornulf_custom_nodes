from .show_stuff import ShowFloat, ShowInt, ShowStringText, ShowJson
from .ffmpeg_images_to_video import imagesToVideo
from .write_text import WriteText
from .text_replace import TextReplace
# from .write_image_environment import WriteImageEnvironment
# from .write_image_characters import WriteImageCharacters
# from .write_image_character import WriteImageCharacter
# from .write_image_allinone import WriteImageAllInOne
from .combine_texts import CombineTexts
from .ffmpeg_configuration import FFmpegConfig
from .loop_texts import LoopTexts
from .random_texts import RandomTexts
from .random_model_clip_vae import RandomModelClipVae
from .video_pingpong import VideoPingPong
from .loop_float import LoopFloat
from .loop_integer import LoopInteger
from .loop_basic_batch import LoopBasicBatch
from .loop_samplers import LoopSamplers
from .loop_schedulers import LoopSchedulers
# from .ollama import ollamaLoader OBSOLETE
from .show_text import ShowText
from .save_text import SaveText
from .save_tmp_image import SaveTmpImage
from .save_image_path import SaveImagePath
from .save_img_to_folder import SaveImageToFolder
from .resize_image import ResizeImage
from .resize_image_percentage import ResizeImagePercentage
from .loop_my_combos_samplers_schedulers import LoopCombosSamplersSchedulers
from .remove_transparency import RemoveTransparency
from .image_to_grayscale import GrayscaleTransform
from .combine_background_overlay import CombineBackgroundOverlay
from .save_bjornulf_lobechat import SaveBjornulfLobeChat
from .green_to_transparency import GreenScreenToTransparency
from .random_line_from_input import RandomLineFromInput
from .loop_lines import LoopAllLines
from .random_seed_with_text import TextToStringAndSeed
from .load_image_alpha import LoadImageWithTransparency
from .image_mask_cutter import ImageMaskCutter
from .character_description import CharacterDescriptionGenerator
from .text_to_speech import TextToSpeech, XTTSConfig
from .loop_combine_texts_by_lines import CombineTextsByLines
from .free_vram_hack import FreeVRAM
#, PurgeCLIPNode
from .pause_resume_stop import PauseResume
from .pick_input import PickInput
from .loop_images import LoopImages
from .random_image import RandomImage
from .loop_model_clip_vae import LoopModelClipVae
from .write_text_advanced import WriteTextAdvanced
from .loop_write_text import LoopWriteText
from .load_images_from_folder import LoadImagesFromSelectedFolder
from .select_image_from_list import SelectImageFromList
from .random_model_selector import RandomModelSelector
from .if_else import IfElse
from .image_details import ImageDetails
from .video_details import VideoDetails
from .combine_images import CombineImages
# from .pass_preview_image import PassPreviewImage
from .text_scramble_character import ScramblerCharacter
from .audio_video_sync import AudioVideoSync
from .video_path_to_images import VideoToImagesList
from .ffmpeg_images_to_video_path import ImagesListToVideo
from .video_preview import VideoPreview
from .loop_model_selector import LoopModelSelector
from .random_lora_selector import RandomLoraSelector
from .loop_lora_selector import LoopLoraSelector
from .loop_sequential_integer import LoopIntegerSequential
from .loop_lines_sequential import LoopLinesSequential
from .ffmpeg_concat_videos import ConcatVideos
from .ffmpeg_concat_videos_from_list import ConcatVideosFromList
from .ffmpeg_combine_video_audio import CombineVideoAudio
from .images_merger_horizontal import MergeImagesHorizontally
from .images_merger_vertical import MergeImagesVertically
from .ollama_talk import OllamaTalk
from .ollama_image_vision import OllamaImageVision, OllamaVisionPromptSelector
from .ollama_config_selector import OllamaConfig
from .ollama_system_persona import OllamaSystemPersonaSelector
from .ollama_system_job import OllamaSystemJobSelector
from .speech_to_text import SpeechToText
from .text_to_anything import TextToAnything
from .anything_to_text import AnythingToText
from .anything_to_int import AnythingToInt
from .anything_to_float import AnythingToFloat
from .add_line_numbers import AddLineNumbers
from .ffmpeg_convert import ConvertVideo
# from .hiresfix import HiResFix
# from .show_images import ImageBlend
from .text_generator import TextGenerator, TextGeneratorScene, TextGeneratorStyle, TextGeneratorCharacterFemale, TextGeneratorCharacterMale, TextGeneratorOutfitMale, TextGeneratorOutfitFemale, ListLooper, ListLooperScene, ListLooperStyle, ListLooperCharacter, ListLooperOutfitFemale, ListLooperOutfitMale, TextGeneratorCharacterPose, TextGeneratorCharacterObject, TextGeneratorCharacterCreature
from .API_flux import APIGenerateFlux
from .API_StableDiffusion import APIGenerateStability
from .API_civitai import APIGenerateCivitAI, APIGenerateCivitAIAddLORA, CivitAIModelSelectorPony, CivitAIModelSelectorSD15, CivitAIModelSelectorSDXL, CivitAIModelSelectorFLUX_S, CivitAIModelSelectorFLUX_D, CivitAILoraSelectorSD15, CivitAILoraSelectorSDXL, CivitAILoraSelectorPONY, CivitAILoraSelectorHunyuan, LoadCivitAILinks
from .API_falAI import APIGenerateFalAI
from .latent_resolution_selector import LatentResolutionSelector
from .loader_lora_with_path import LoaderLoraWithPath
from .load_text import LoadTextFromFolder, LoadTextFromPath
from .string_splitter import TextSplitin5, TextSplitin10
from .line_selector import LineSelector
from .text_to_speech_kokoro import KokoroTTS
from .note_text import DisplayNote
from .note_image import ImageNote, ImageNoteLoadImage
from .model_clip_vae_selector import ModelClipVaeSelector
from .global_variables import LoadGlobalVariables, SaveGlobalVariables
from .lora_stacks import AllLoraSelector
from .hugginface_download import HuggingFaceDownloader
from .preview_first_image import PreviewFirstImage
# from .video_latent import VideoLatentResolutionSelector
# from .empty_latent_video import EmptyVideoLatentWithSingle
# from .text_generator_t2v import TextGeneratorText2Video
from .images_compare import FourImageViewer
# from .pickme import WriteTextPickMe, PickMe
from .write_pickme_chain import WriteTextPickMeChain
# from .todo import ToDoList
from .text_to_variable import TextToVariable
from .random_stuff import RandomIntNode, RandomFloatNode
from .global_seed_manager import GlobalSeedManager
from .play_sound import PlayAudio
from .switches import SwitchText, SwitchAnything
from .write_pickme_global import WriteTextPickMeGlobal, LoadTextPickMeGlobal
from .list_selector import ListSelector
from .text_analyzer import TextAnalyzer
from .math_node import MathNode
from .save_tmp_audio import SaveTmpAudio
from .save_tmp_video import SaveTmpVideo
from .audio_preview import AudioPreview
from .style_selector import StyleSelector
# from .switches import ConditionalSwitch
from .split_image import SplitImageGrid, ReassembleImageGrid
from .API_openai import APIGenerateGPT4o

# from .video_text_generator import VideoTextGenerator
# from .run_workflow_from_api import ExecuteWorkflowNode, ApiDynamicTextInputs
# from .remote_nodes import RemoteVAEDecoderNodeTiled, RemoteVAEDecoderNode, LoadFromBase64, SaveTensors, LoadTensor
# from .fix_face import FixFace, FaceSettings

#RemoteTextEncodingWithCLIPs

NODE_CLASS_MAPPINGS = {
    # "Bjornulf_PurgeCLIPNode": PurgeCLIPNode,
    # "Bjornulf_RemoteTextEncodingWithCLIPs": RemoteTextEncodingWithCLIPs,
    
    # "Bjornulf_FixFace": FixFace,
    # "Bjornulf_FaceSettings": FaceSettings,
    # "Bjornulf_SaveTensors": SaveTensors,
    # "Bjornulf_LoadTensor": LoadTensor,
    # "Bjornulf_LoadFromBase64": LoadFromBase64,
    # "Bjornulf_RemoteVAEDecoderNode": RemoteVAEDecoderNode,
    # "Bjornulf_RemoteVAEDecoderNodeTiled": RemoteVAEDecoderNodeTiled,
    # "Bjornulf_VideoTextGenerator": VideoTextGenerator,
    # "Bjornulf_ExecuteWorkflowNode": ExecuteWorkflowNode,
    # "Bjornulf_ApiDynamicTextInputs": ApiDynamicTextInputs,
    "Bjornulf_APIGenerateGPT4o": APIGenerateGPT4o,
    
    # "Bjornulf_ConditionalSwitch": ConditionalSwitch,
    "Bjornulf_LoadCivitAILinks": LoadCivitAILinks,
    "Bjornulf_SplitImageGrid": SplitImageGrid,
    "Bjornulf_ReassembleImageGrid": ReassembleImageGrid,
    "Bjornulf_StyleSelector": StyleSelector,
    "Bjornulf_OllamaVisionPromptSelector": OllamaVisionPromptSelector,
    "Bjornulf_AudioPreview": AudioPreview,
    "Bjornulf_SaveTmpAudio": SaveTmpAudio,
    "Bjornulf_SaveTmpVideo": SaveTmpVideo,
    "Bjornulf_MathNode": MathNode,
    "Bjornulf_TextAnalyzer": TextAnalyzer,
    "Bjornulf_ListSelector": ListSelector,
    "Bjornulf_WriteTextPickMeGlobal": WriteTextPickMeGlobal,
    "Bjornulf_LoadTextPickMeGlobal": LoadTextPickMeGlobal,
    "Bjornulf_PlayAudio": PlayAudio,
    "Bjornulf_SwitchText": SwitchText,
    "Bjornulf_SwitchAnything": SwitchAnything,
    "Bjornulf_GlobalSeedManager": GlobalSeedManager,
    "Bjornulf_RandomIntNode": RandomIntNode,
    "Bjornulf_RandomFloatNode": RandomFloatNode,
    "Bjornulf_TextToVariable": TextToVariable,
    # "Bjornulf_ToDoList": ToDoList,
    # "Bjornulf_WriteTextPickMe": WriteTextPickMe,
    "Bjornulf_WriteTextPickMeChain": WriteTextPickMeChain,
    # "Bjornulf_PickMe": PickMe,
    "Bjornulf_FourImageViewer": FourImageViewer,
    "Bjornulf_PreviewFirstImage": PreviewFirstImage,
    "Bjornulf_HuggingFaceDownloader": HuggingFaceDownloader,
    # "Bjornulf_VideoLatentResolutionSelector": VideoLatentResolutionSelector,
    "Bjornulf_AllLoraSelector": AllLoraSelector,
    "Bjornulf_LoadGlobalVariables": LoadGlobalVariables,
    "Bjornulf_SaveGlobalVariables": SaveGlobalVariables,
    "Bjornulf_ModelClipVaeSelector": ModelClipVaeSelector,
    "Bjornulf_DisplayNote": DisplayNote,
    "Bjornulf_ImageNote": ImageNote,
    "Bjornulf_ImageNoteLoadImage": ImageNoteLoadImage,
    "Bjornulf_LineSelector": LineSelector,
    # "Bjornulf_EmptyVideoLatentWithSingle": EmptyVideoLatentWithSingle,
    "Bjornulf_XTTSConfig": XTTSConfig,
    "Bjornulf_KokoroTTS": KokoroTTS,
    # "Bjornulf_TextGeneratorText2Video": TextGeneratorText2Video,
    "Bjornulf_LatentResolutionSelector": LatentResolutionSelector,
    "Bjornulf_LoaderLoraWithPath": LoaderLoraWithPath,
    "Bjornulf_LoadTextFromPath": LoadTextFromPath,
    "Bjornulf_LoadTextFromFolder": LoadTextFromFolder,
    "Bjornulf_TextSplitin5": TextSplitin5,
    "Bjornulf_TextSplitin10": TextSplitin10,
    "Bjornulf_APIGenerateFlux": APIGenerateFlux,
    "Bjornulf_APIGenerateFalAI": APIGenerateFalAI,
    "Bjornulf_APIGenerateStability": APIGenerateStability,
    "Bjornulf_APIGenerateCivitAI": APIGenerateCivitAI,
    "Bjornulf_CivitAIModelSelectorPony": CivitAIModelSelectorPony,
    "Bjornulf_CivitAIModelSelectorSD15": CivitAIModelSelectorSD15,
    "Bjornulf_CivitAIModelSelectorSDXL": CivitAIModelSelectorSDXL,
    "Bjornulf_CivitAIModelSelectorFLUX_S": CivitAIModelSelectorFLUX_S,
    "Bjornulf_CivitAIModelSelectorFLUX_D": CivitAIModelSelectorFLUX_D,
    "Bjornulf_CivitAILoraSelectorSD15": CivitAILoraSelectorSD15,
    "Bjornulf_CivitAILoraSelectorSDXL": CivitAILoraSelectorSDXL,
    "Bjornulf_CivitAILoraSelectorPONY": CivitAILoraSelectorPONY,
    "Bjornulf_CivitAILoraSelectorHunyuan": CivitAILoraSelectorHunyuan,
    # "Bjornulf_CivitAILoraSelector": CivitAILoraSelector,
    "Bjornulf_APIGenerateCivitAIAddLORA": APIGenerateCivitAIAddLORA,
    "Bjornulf_TextGenerator": TextGenerator,
    "Bjornulf_TextGeneratorCharacterPose": TextGeneratorCharacterPose,
    "Bjornulf_TextGeneratorCharacterObject": TextGeneratorCharacterObject,
    "Bjornulf_TextGeneratorScene": TextGeneratorScene,
    "Bjornulf_TextGeneratorStyle": TextGeneratorStyle,
    "Bjornulf_TextGeneratorCharacterFemale": TextGeneratorCharacterFemale,
    "Bjornulf_TextGeneratorCharacterMale": TextGeneratorCharacterMale,
    "Bjornulf_TextGeneratorCharacterCreature": TextGeneratorCharacterCreature,
    "Bjornulf_TextGeneratorOutfitFemale": TextGeneratorOutfitFemale,
    "Bjornulf_TextGeneratorOutfitMale": TextGeneratorOutfitMale,
    "Bjornulf_ListLooper": ListLooper,
    "Bjornulf_ListLooperScene": ListLooperScene,
    "Bjornulf_ListLooperStyle": ListLooperStyle,
    "Bjornulf_ListLooperCharacter": ListLooperCharacter,
    "Bjornulf_ListLooperOutfitMale": ListLooperOutfitMale,
    "Bjornulf_ListLooperOutfitFemale": ListLooperOutfitFemale,
    # "Bjornulf_HiResFix": HiResFix,
    # "Bjornulf_ImageBlend": ImageBlend,
    "Bjornulf_ShowInt": ShowInt, 
    "Bjornulf_TextReplace" : TextReplace,
    "Bjornulf_ShowFloat": ShowFloat,
    "Bjornulf_ShowJson": ShowJson,
    "Bjornulf_ShowStringText": ShowStringText,
    # "Bjornulf_ollamaLoader": ollamaLoader, OBSOLETE
    "Bjornulf_FFmpegConfig": FFmpegConfig,
    "Bjornulf_ConvertVideo": ConvertVideo,
    "Bjornulf_AddLineNumbers": AddLineNumbers,
    "Bjornulf_TextToAnything": TextToAnything,
    "Bjornulf_AnythingToText": AnythingToText,
    "Bjornulf_AnythingToInt": AnythingToInt,
    "Bjornulf_AnythingToFloat": AnythingToFloat,
    "Bjornulf_SpeechToText": SpeechToText,
    "Bjornulf_OllamaConfig": OllamaConfig,
    "Bjornulf_OllamaSystemPersonaSelector": OllamaSystemPersonaSelector,
    "Bjornulf_OllamaSystemJobSelector": OllamaSystemJobSelector,
    "Bjornulf_OllamaImageVision": OllamaImageVision,
    "Bjornulf_OllamaTalk": OllamaTalk,
    "Bjornulf_MergeImagesHorizontally": MergeImagesHorizontally,
    "Bjornulf_MergeImagesVertically": MergeImagesVertically,
    "Bjornulf_CombineVideoAudio": CombineVideoAudio,
    "Bjornulf_ConcatVideos": ConcatVideos,
    "Bjornulf_ConcatVideosFromList": ConcatVideosFromList,
    "Bjornulf_LoopLinesSequential": LoopLinesSequential,
    "Bjornulf_LoopIntegerSequential": LoopIntegerSequential,
    "Bjornulf_LoopLoraSelector": LoopLoraSelector,
    "Bjornulf_RandomLoraSelector": RandomLoraSelector,
    "Bjornulf_LoopModelSelector": LoopModelSelector,
    "Bjornulf_VideoPreview": VideoPreview,
    "Bjornulf_ImagesListToVideo": ImagesListToVideo,
    "Bjornulf_VideoToImagesList": VideoToImagesList,
    "Bjornulf_AudioVideoSync": AudioVideoSync,
    "Bjornulf_ScramblerCharacter": ScramblerCharacter,
    "Bjornulf_CombineImages": CombineImages,
    "Bjornulf_ImageDetails": ImageDetails,
    "Bjornulf_VideoDetails": VideoDetails,
    "Bjornulf_IfElse": IfElse,
    "Bjornulf_RandomModelSelector": RandomModelSelector,
    "Bjornulf_SelectImageFromList": SelectImageFromList,
    "Bjornulf_WriteText": WriteText,
    "Bjornulf_LoadImagesFromSelectedFolder": LoadImagesFromSelectedFolder,
    "Bjornulf_LoopModelClipVae": LoopModelClipVae,
    "Bjornulf_LoopWriteText": LoopWriteText,
    "Bjornulf_LoopImages": LoopImages,
    "Bjornulf_RandomImage": RandomImage,
    # "Bjornulf_PassPreviewImage": PassPreviewImage,
    "Bjornulf_PickInput": PickInput,
    "Bjornulf_PauseResume": PauseResume,
    "Bjornulf_FreeVRAM": FreeVRAM,
    "Bjornulf_CombineTextsByLines": CombineTextsByLines,
    "Bjornulf_TextToSpeech": TextToSpeech,
    "Bjornulf_CharacterDescriptionGenerator": CharacterDescriptionGenerator,
    "Bjornulf_ImageMaskCutter": ImageMaskCutter,
    "Bjornulf_LoadImageWithTransparency": LoadImageWithTransparency,
    "Bjornulf_LoopAllLines": LoopAllLines,
    "Bjornulf_TextToStringAndSeed": TextToStringAndSeed,
    "Bjornulf_GreenScreenToTransparency": GreenScreenToTransparency,
    "Bjornulf_RandomLineFromInput": RandomLineFromInput,
    "Bjornulf_SaveBjornulfLobeChat": SaveBjornulfLobeChat,
    "Bjornulf_WriteTextAdvanced": WriteTextAdvanced,
    "Bjornulf_RemoveTransparency": RemoveTransparency,
    "Bjornulf_GrayscaleTransform": GrayscaleTransform,
    "Bjornulf_CombineBackgroundOverlay": CombineBackgroundOverlay,
    "Bjornulf_ShowText": ShowText,
    "Bjornulf_SaveText": SaveText,
    "Bjornulf_ResizeImage": ResizeImage,
    "Bjornulf_ResizeImagePercentage": ResizeImagePercentage,
    "Bjornulf_SaveImageToFolder": SaveImageToFolder,
    "Bjornulf_SaveTmpImage": SaveTmpImage,
    "Bjornulf_SaveImagePath": SaveImagePath,
    "Bjornulf_CombineTexts": CombineTexts,
    "Bjornulf_LoopTexts": LoopTexts,
    "Bjornulf_RandomTexts": RandomTexts,
    "Bjornulf_RandomModelClipVae": RandomModelClipVae,
    "Bjornulf_imagesToVideo": imagesToVideo,
    "Bjornulf_VideoPingPong": VideoPingPong,
    "Bjornulf_LoopFloat": LoopFloat,
    "Bjornulf_LoopInteger": LoopInteger,
    "Bjornulf_LoopBasicBatch": LoopBasicBatch,
    "Bjornulf_LoopSamplers": LoopSamplers,
    "Bjornulf_LoopSchedulers": LoopSchedulers,
    "Bjornulf_LoopCombosSamplersSchedulers": LoopCombosSamplersSchedulers,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    # "Bjornulf_RemoteTextEncodingWithCLIPs": "[BETA] 🔮 Remote Text Encoding with CLIPs",
    # "Bjornulf_ConditionalSwitch": "ConditionalSwitch",
    # "Bjornulf_PurgeCLIPNode": "🧹📎 Purge CLIP",
    
    # "Bjornulf_FixFace": "[BETA] 🔧🧑 Fix Face",
    # "Bjornulf_FaceSettings": "[BETA] 🧑 Face Settings [Fix Face] ⚙",
    # "Bjornulf_SaveTensors": "[BETA] 💾 Save Tensors (tmp_api.pt) ⚠️💣",
    # "Bjornulf_LoadTensor": "[BETA] 📥 Load Tensor (tmp_api.pt)",
    # "Bjornulf_RemoteVAEDecoderNode": "[BETA] 🔮 Remote VAE Decoder",
    # "Bjornulf_RemoteVAEDecoderNodeTiled": "[BETA] 🔮 Remote VAE Decoder (Tiled)",
    # "Bjornulf_LoadFromBase64": "[BETA] 📥🔮 Load from Base64",
    # "Bjornulf_ApiDynamicTextInputs": "[BETA] 📥🔮📝 Text Manager Api (Execute Workflow)",
    # "Bjornulf_ExecuteWorkflowNode": "[BETA] 🔮⚡ Remote Execute Workflow",
    # "Bjornulf_VideoTextGenerator": "[BETA] 🔥📝📹 Video Text Generator 📹📝🔥",
    
    "Bjornulf_LoadCivitAILinks": "📥🕑🤖 Load CivitAI Links",
    "Bjornulf_StyleSelector": "🎨📜 Style Selector (🎲 or ♻ or ♻📑) + Civitai urn",
    "Bjornulf_ReassembleImageGrid": "🖼📹🔨 Reassemble Image/Video Grid",
    "Bjornulf_SplitImageGrid": "🖼📹🔪 Split Image/Video Grid",
    "Bjornulf_SaveTmpAudio": "💾🔊 Save Audio (tmp_api.wav/mp3) ⚠️💣",
    "Bjornulf_SaveTmpVideo": "💾📹 Save Video (tmp_api.mp4/mkv/webm) ⚠️💣",
    "Bjornulf_AudioPreview": "🔊▶ Audio Preview (Audio player)",
    "Bjornulf_MathNode": "🧮 Basic Math",
    "Bjornulf_TextAnalyzer": "📊🔍 Text Analyzer",
    "Bjornulf_OllamaVisionPromptSelector": "🦙👁 Ollama Vision Prompt Selector",
    "Bjornulf_ListSelector": "📑👈 Select from List",
    "Bjornulf_PlayAudio": "🔊▶ Play Audio",
    "Bjornulf_SwitchText": "🔛📝 Text Switch On/Off",
    "Bjornulf_SwitchAnything": "🔛✨ Anything Switch On/Off",
    "Bjornulf_GlobalSeedManager": "🌎🎲 Global Seed Manager",
    "Bjornulf_RandomIntNode": "🎲 Random Integer",
    "Bjornulf_RandomFloatNode": "🎲 Random Float",
    "Bjornulf_WriteTextPickMeGlobal": "🌎✒👉 Global Write Pick Me",
    "Bjornulf_LoadTextPickMeGlobal": "🌎📥 Load Global Pick Me",
    "Bjornulf_TextToVariable": "📌🅰️ Set Variable from Text",
    # "Bjornulf_ToDoList": "ToDoList",
    # "Bjornulf_WriteTextPickMe": "✒👉 Write Pick Me",
    "Bjornulf_WriteTextPickMeChain": "✒👉 Write Pick Me Chain",
    # "Bjornulf_PickByText": "✒👉 Pick Me by Text",
    # "Bjornulf_PickMe": "✋ Recover Pick Me ! ✋",
    "Bjornulf_FourImageViewer": "🖼👁 Preview 1-4 images (compare)",
    "Bjornulf_PreviewFirstImage": "🖼👁 Preview (first) image",
    "Bjornulf_HuggingFaceDownloader": "💾 Huggingface Downloader",
    "Bjornulf_AllLoraSelector": "👑 Combine Loras, Lora stack",
    "Bjornulf_LoadGlobalVariables": "📥🅰️ Load Global Variables",
    "Bjornulf_SaveGlobalVariables": "💾🅰️ Save Global Variables",
    "Bjornulf_ModelClipVaeSelector": "📝👈 Model-Clip-Vae selector (🎲 or ♻ or ♻📑)",
    "Bjornulf_DisplayNote": "📒 Note",
    "Bjornulf_ImageNote": "🖼📒 Image Note",
    "Bjornulf_ImageNoteLoadImage": "📥🖼📒 Image Note (Load image)",
    # "Bjornulf_VideoLatentResolutionSelector": "🩷📹 Empty Video Latent Selector",
    # "Bjornulf_EmptyVideoLatentWithSingle": "Bjornulf_EmptyVideoLatentWithSingle",
    "Bjornulf_XTTSConfig": "🔊 TTS Configuration ⚙",
    "Bjornulf_TextToSpeech": "📝➜🔊 TTS - Text to Speech",
    # "Bjornulf_HiResFix": "HiResFix",
    # "Bjornulf_ImageBlend": "🎨 Image Blend",
    # "Bjornulf_APIHiResCivitAI": "🎨➜🎨 API Image hires fix (CivitAI)",
    # "Bjornulf_CivitAILoraSelector": "lora Civit",
    "Bjornulf_KokoroTTS": "📝➜🔊 Kokoro - Text to Speech",
    "Bjornulf_LineSelector": "📝👈🅰️ Line selector (🎲 or ♻ or ♻📑)",
    "Bjornulf_LoaderLoraWithPath": "📥👑 Load Lora with Path",
    # "Bjornulf_TextGeneratorText2Video": "🔥📝📹 Text Generator for text to video 📹📝🔥",
    "Bjornulf_TextSplitin5": "📝🔪 Text split in 5",
    "Bjornulf_TextSplitin10": "📝🔪 Text split in 10",
    "Bjornulf_LatentResolutionSelector": "🩷 Empty Latent Selector",
    "Bjornulf_CivitAIModelSelectorSD15": "📥 Load checkpoint SD1.5 (+Download from CivitAi)",
    "Bjornulf_CivitAIModelSelectorSDXL": "📥 Load checkpoint SDXL (+Download from CivitAi)",
    "Bjornulf_CivitAIModelSelectorPony": "📥 Load checkpoint Pony (+Download from CivitAi)",
    "Bjornulf_CivitAIModelSelectorFLUX_D": "📥 Load checkpoint FLUX Dev (+Download from CivitAi)",
    "Bjornulf_CivitAIModelSelectorFLUX_S": "📥 Load checkpoint FLUX Schnell (+Download from CivitAi)",
    "Bjornulf_CivitAILoraSelectorSD15": "📥👑 Load Lora SD1.5 (+Download from CivitAi)",
    "Bjornulf_CivitAILoraSelectorSDXL": "📥👑 Load Lora SDXL (+Download from CivitAi)",
    "Bjornulf_CivitAILoraSelectorPONY": "📥👑 Load Lora Pony (+Download from CivitAi)",
    "Bjornulf_CivitAILoraSelectorHunyuan": "📥👑📹 Load Lora Hunyuan Video (+Download from CivitAi)",
    "Bjornulf_APIGenerateFalAI": "☁🎨 API Image Generator (FalAI) 🎨☁",
    "Bjornulf_APIGenerateCivitAI": "☁🎨 API Image Generator (CivitAI) 🎨☁",
    "Bjornulf_APIGenerateCivitAIAddLORA": "☁👑 Add Lora (API ONLY - CivitAI) 👑☁",
    "Bjornulf_APIGenerateFlux": "☁🎨 API Image Generator (Black Forest Labs - Flux) 🎨☁",
    "Bjornulf_APIGenerateStability": "☁🎨 API Image Generator (Stability - Stable Diffusion) 🎨☁",
    "Bjornulf_TextGenerator": "🔥📝 Image Text Generator 📝🔥",
    "Bjornulf_TextGeneratorCharacterFemale": "👩‍🦰📝 Text Generator (Character Female)",
    "Bjornulf_TextGeneratorCharacterMale": "👨‍🦰📝 Text Generator (Character Male)",
    "Bjornulf_TextGeneratorCharacterPose": "💃🕺📝 Text Generator (Character Pose)",
    "Bjornulf_TextGeneratorCharacterObject": "🔧👨‍🔧📝 Text Generator (Object for Character)",
    "Bjornulf_TextGeneratorCharacterCreature": "👾📝 Text Generator (Character Creature)",
    "Bjornulf_TextGeneratorScene": "🌄📝 Text Generator (Scene)",
    "Bjornulf_TextGeneratorStyle": "🎨📝 Text Generator (Style)",
    "Bjornulf_TextGeneratorOutfitFemale": "👗 Text Generator (Outfit Female)",
    "Bjornulf_TextGeneratorOutfitMale": "👚 Text Generator (Outfit Male)",
    "Bjornulf_ListLooper": "♻🔥📝 List Looper (Text Generator)",
    "Bjornulf_ListLooperScene": "♻🌄📝 List Looper (Text Generator Scenes)",
    "Bjornulf_ListLooperStyle": "♻🎨📝 List Looper (Text Generator Styles)",
    "Bjornulf_ListLooperPose": "♻💃🕺📝 List Looper (Text Generator Poses)",
    "Bjornulf_ListLooperCharacter": "♻👨‍🦰👩‍🦰👾 List Looper (Text Generator Characters)",
    "Bjornulf_ListLooperOutfitMale": "♻👚 List Looper (Text Generator Outfits Male)",
    "Bjornulf_ListLooperOutfitFemale": "♻👗 List Looper (Text Generator Outfits Female)",
    "Bjornulf_ShowInt": "👁 Show (Int)",
    "Bjornulf_ShowFloat": "👁 Show (Float)",
    "Bjornulf_ShowJson": "👁 Show (JSON)",
    "Bjornulf_ShowStringText": "👁 Show (String/Text)",
    "Bjornulf_OllamaTalk": "🦙💬 Ollama Talk",
    "Bjornulf_OllamaImageVision": "🦙👁 Ollama Vision",
    "Bjornulf_OllamaConfig": "🦙 Ollama Configuration ⚙",
    "Bjornulf_XTTSConfig": "🔊 TTS Configuration ⚙",
    "Bjornulf_OllamaSystemJobSelector": "🦙 Ollama Job Selector 👇",
    "Bjornulf_OllamaSystemPersonaSelector": "🦙 Ollama Persona Selector 👇",
    "Bjornulf_SpeechToText": "🔊➜📝 STT - Speech to Text",
    "Bjornulf_TextToSpeech": "📝➜🔊 TTS - Text to Speech",
    "Bjornulf_TextToAnything": "📝➜✨ Text to Anything",
    "Bjornulf_AnythingToText": "✨➜📝 Anything to Text",
    "Bjornulf_AnythingToInt": "✨➜🔢 Anything to Int",
    "Bjornulf_AnythingToFloat": "✨➜🔢 Anything to Float",
    "Bjornulf_TextReplace": "📝➜📝 Replace text",
    "Bjornulf_AddLineNumbers": "🔢 Add line numbers",
    "Bjornulf_FFmpegConfig": "⚙📹 FFmpeg Configuration 📹⚙",
    "Bjornulf_ConvertVideo": "📹➜📹 Convert Video (FFmpeg)",
    "Bjornulf_VideoDetails": "📹🔍 Video details (FFmpeg) ⚙",
    "Bjornulf_WriteText": "✒ Write Text",
    "Bjornulf_MergeImagesHorizontally": "🖼🖼 Merge Images/Videos 📹📹 (Horizontally)",
    "Bjornulf_MergeImagesVertically": "🖼🖼 Merge Images/Videos 📹📹 (Vertically)",
    "Bjornulf_CombineVideoAudio": "📹🔊 Combine Video + Audio",
    "Bjornulf_ConcatVideos": "📹🔗 Concat Videos (FFmpeg)",
    "Bjornulf_ConcatVideosFromList": "📹🔗 Concat Videos from list (FFmpeg)",
    "Bjornulf_LoopLinesSequential": "♻📑 Loop Sequential (input Lines)",
    "Bjornulf_LoopIntegerSequential": "♻📑 Loop Sequential (Integer)",
    "Bjornulf_LoopLoraSelector": "♻👑 Loop Lora Selector",
    "Bjornulf_RandomLoraSelector": "🎲👑 Random Lora Selector",
    "Bjornulf_LoopModelSelector": "♻ Loop Load checkpoint (Model Selector)",
    "Bjornulf_VideoPreview": "📹👁 Video Preview",
    "Bjornulf_ImagesListToVideo": "🖼➜📹 Images to Video path (tmp video) (FFmpeg)",
    "Bjornulf_VideoToImagesList": "📹➜🖼 Video Path to Images (Load video)",
    "Bjornulf_AudioVideoSync": "🔊📹 Audio Video Sync",
    "Bjornulf_ScramblerCharacter": "🔀🎲 Text scrambler (🧑 Character)",
    "Bjornulf_WriteTextAdvanced": "✒🗔🅰️ Advanced Write Text",
    "Bjornulf_LoopWriteText": "♻ Loop (✒🗔🅰️ Advanced Write Text)",
    "Bjornulf_LoopModelClipVae": "♻ Loop (Model+Clip+Vae)",
    "Bjornulf_LoopImages": "♻🖼 Loop (Images)",
    "Bjornulf_CombineTextsByLines": "♻ Loop (All Lines from input 🔗 combine by lines)",
    "Bjornulf_LoopTexts": "♻ Loop (Texts)",
    "Bjornulf_LoopFloat": "♻ Loop (Float)",
    "Bjornulf_LoopInteger": "♻ Loop (Integer)",
    "Bjornulf_LoopBasicBatch": "♻ Loop",
    "Bjornulf_LoopAllLines": "♻ Loop (All Lines from input)",
    "Bjornulf_LoopSamplers": "♻ Loop (All Samplers)",
    "Bjornulf_LoopSchedulers": "♻ Loop (All Schedulers)",
    "Bjornulf_LoopCombosSamplersSchedulers": "♻ Loop (My combos Sampler⚔Scheduler)",
    "Bjornulf_RandomImage": "🎲🖼 Random Image",
    "Bjornulf_RandomLineFromInput": "🎲 Random line from input",
    "Bjornulf_RandomTexts": "🎲 Random (Texts)",
    "Bjornulf_RandomModelClipVae": "🎲 Random (Model+Clip+Vae)",
    "Bjornulf_RandomModelSelector": "🎲 Random Load checkpoint (Model Selector)",
    # "Bjornulf_PassPreviewImage": "🖼⮕ Pass Preview Image",
    "Bjornulf_CharacterDescriptionGenerator": "🧑📝 Character Description Generator",
    "Bjornulf_GreenScreenToTransparency": "🟩➜▢ Green Screen to Transparency",
    "Bjornulf_SaveBjornulfLobeChat": "🖼💬 Save image for Bjornulf LobeChat",
    "Bjornulf_TextToStringAndSeed": "🔢🎲 Text with random Seed",
    "Bjornulf_ShowText": "👁 Show (Text, Int, Float)",
    "Bjornulf_ImageMaskCutter": "🖼✂ Cut Image with Mask",
    "Bjornulf_LoadImageWithTransparency": "📥🖼 Load Image with Transparency ▢",
    "Bjornulf_CombineBackgroundOverlay": "🖼+🖼 Stack two images (Background+Overlay alpha)",
    "Bjornulf_GrayscaleTransform": "🖼➜🔲 Image to grayscale (black & white)",
    "Bjornulf_RemoveTransparency": "▢➜⬛ Remove image Transparency (alpha)",
    "Bjornulf_ResizeImage": "📏 Resize Image",
    "Bjornulf_ResizeImagePercentage": "📏 Resize Image Percentage",
    "Bjornulf_SaveImagePath": "💾🖼 Save Image (exact path, exact name) ⚠️💣",
    "Bjornulf_SaveImageToFolder": "💾🖼📁 Save Image(s) to a folder",
    "Bjornulf_SaveTmpImage": "💾🖼 Save Image (tmp_api.png) ⚠️💣",
    "Bjornulf_SaveText": "💾 Save Text",
    "Bjornulf_LoadTextFromPath": "📥 Load Text From Path",
    "Bjornulf_LoadTextFromFolder": "📥 Load Text From Bjornulf Folder",
    "Bjornulf_CombineTexts": "🔗 Combine (Texts)",
    "Bjornulf_imagesToVideo": "🖼➜📹 images to video (FFMPEG Save Video)",
    "Bjornulf_VideoPingPong": "📹 video PingPong",
    "Bjornulf_ollamaLoader": "🦙 Ollama (Description)",
    "Bjornulf_FreeVRAM": "🧹 Free VRAM hack",
    "Bjornulf_PickInput": "⏸️ Paused. Select input, Pick 👇",
    "Bjornulf_PauseResume": "⏸️ Paused. Resume or Stop, Pick 👇",
    "Bjornulf_LoadImagesFromSelectedFolder": "📥🖼📂 Load Images from output folder",
    "Bjornulf_SelectImageFromList": "🖼👈 Select an Image, Pick",
    "Bjornulf_IfElse": "🔀 If-Else (input / compare_with)",
    "Bjornulf_ImageDetails": "🖼🔍 Image Details",
    "Bjornulf_CombineImages": "🖼🔗 Combine Images",
    "Bjornulf_APIGenerateGPT4o": "☁🎨 API Image Generator (openai, gpt-image-1)",
}

WEB_DIRECTORY = "./web"
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']
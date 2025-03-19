import os
import random
from aiohttp import web
from server import PromptServer

# Shared data structures (unchanged)
CATEGORIES = ["Painting", "Photography", "Digital Art", "3D Rendering", "Illustration"]

BRANCHES = {
    "Painting": [
        "Renaissance", "Baroque", "Rococo", "Neoclassicism",
        "Romanticism", "Realism", "Impressionism", "Post-Impressionism",
        "Expressionism", "Fauvism", "Cubism", "Futurism", "Dadaism",
        "Surrealism", "Abstract Expressionism", "Pop Art", "Op Art",
        "Minimalism"
    ],
    "Photography": [
        "Black and White", "Color", "Vintage", "Sepia Tone", "HDR",
        "Long Exposure", "Macro", "Portrait", "Landscape", "Street",
        "Fashion", "Analog Film", "Cinematic"
    ],
    "Digital Art": [
        "Digital Painting", "Vector Art", "Pixel Art", "Fractal Art",
        "Algorithmic Art", "Glitch Art"
    ],
    "3D Rendering": [
        "Low Poly", "Voxel", "Isometric", "Ray Tracing"
    ],
    "Illustration": [
        "Line Art", "Cartoon", "Comic Book", "Manga", "Anime",
        "Technical Illustration", "Botanical Illustration",
        "Architectural Rendering", "Concept Art", "Storyboard Art"
    ],
}

BRANCHES_MODELS = {
    "Photography": [
        ("SDXL", "urn:air:sdxl:checkpoint:civitai:101055@128078", "https://civitai.green/models/101055?modelVersionId=128078"),
        ("Juggernaut XL", "urn:air:sdxl:checkpoint:civitai:133005@166909", "https://civitai.green/models/133005?modelVersionId=166909"),
        ("Realistic Stock Photo", "urn:air:sdxl:checkpoint:civitai:139565@154593", "https://civitai.green/models/139565?modelVersionId=154593"),
    ],
    "Illustration": [
        ("Hassaku XL", "urn:air:sdxl:checkpoint:civitai:140272@176059", "https://civitai.green/models/140272?modelVersionId=176059"),
        ("[Lah] Mysterious", "urn:air:sdxl:checkpoint:civitai:118441@162380", "https://civitai.green/models/118441?modelVersionId=162380"),
        ("Copax TimeLessXL", "urn:air:sdxl:checkpoint:civitai:118111@1108377", "https://civitai.green/models/118111?modelVersionId=172160"),
    ],
    "3D Rendering": [
        ("Samaritan 3D Cartoon", "urn:air:sdxl:checkpoint:civitai:81270@144566", "https://civitai.green/models/81270?modelVersionId=144566"),
        ("FormulaXL", "urn:air:sdxl:checkpoint:civitai:129922@160525", "https://civitai.green/models/129922?modelVersionId=160525"),
    ],
    "Digital Art": [
        ("BriXL", "urn:air:sdxl:checkpoint:civitai:131703@166762", "https://civitai.green/models/131703?modelVersionId=166762"),
        ("SDXL Unstable Diffusers", "urn:air:sdxl:checkpoint:civitai:84040@395107", "https://civitai.green/models/84040?modelVersionId=395107"),
    ],
    "Painting": [
        ("Copax TimeLessXL", "urn:air:sdxl:checkpoint:civitai:118111@1108377", "https://civitai.green/models/118111?modelVersionId=172160"),
        ("PixelPaint - Beautiful Painting Style", "urn:air:sdxl:checkpoint:civitai:284101@319693", "https://civitai.green/models/284101?modelVersionId=319693"),
    ],
}

MODELS = {model_name: (urn, link) for category in BRANCHES_MODELS for model_name, urn, link in BRANCHES_MODELS[category]}

# Counter files
STYLE_LIST_COUNTER_FILE = os.path.join("Bjornulf", "style_list_counter.txt")
MODEL_LIST_COUNTER_FILE = os.path.join("Bjornulf", "model_list_counter.txt")

class StyleSelector:
    @classmethod
    def INPUT_TYPES(cls):
        ALL_STYLES = sorted(set(style for styles in BRANCHES.values() for style in styles))
        ALL_MODELS = ["None"] + sorted(MODELS.keys())
        return {
            "required": {
                "category": (CATEGORIES,),
                "style": (ALL_STYLES,),
                "model": (ALL_MODELS, {"default": "None"}),
                "seed": ("INT", {"default": -1, "min": -1, "max": 0x7FFFFFFFFFFFFFFF}),
                "LOOP_random_LIST": ("BOOLEAN", {"default": False}),
                "LOOP_style_LIST": ("BOOLEAN", {"default": False}),
                "LOOP_SEQUENTIAL": ("BOOLEAN", {"default": False}),
                "jump": ("INT", {"default": 1, "min": 1, "max": 100, "step": 1}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = (
        "selected_category",
        "selected_style_LIST",
        "recommended_with_selected_category",
        "random_LIST_with_selected_category"
    )
    OUTPUT_IS_LIST = (False, True, False, True)
    FUNCTION = "select_style"
    CATEGORY = "Bjornulf"

    def format_style(self, s, descriptor, model=None):
        """Helper function to format a style string."""
        if model != "None" and model in MODELS:
            urn, link = MODELS[model]
            return f"{s} {descriptor};{model};{urn};{link}"
        return f"{s} {descriptor}"

    def get_next_index(self, counter_file, jump, max_items):
        """Get the next index from the counter file, stopping at max_items."""
        os.makedirs(os.path.dirname(counter_file), exist_ok=True)
        try:
            with open(counter_file, 'r') as f:
                current_index = int(f.read().strip())
        except (FileNotFoundError, ValueError):
            current_index = -jump  # Start before the first index (e.g., -1 if jump=1)

        next_index = current_index + jump
        if next_index >= max_items:
            raise ValueError(f"Counter has reached its limit of {max_items}. Reset counter to continue.")

        with open(counter_file, 'w') as f:
            f.write(str(next_index))

        return next_index

    def select_style(self, category, style, seed, LOOP_random_LIST, LOOP_style_LIST, LOOP_SEQUENTIAL, jump, model=None):
        DESCRIPTORS = {
            "Painting": "painting",
            "Photography": "photography",
            "Illustration": "illustration",
        }
        rng = random.Random() if seed == -1 else random.Random(seed)
        descriptor = DESCRIPTORS.get(category, "")

        # Get styles and models for the category
        styles = BRANCHES.get(category, [])
        models = BRANCHES_MODELS.get(category, [])

        # selected_category: Single string
        selected_category = category

        # selected_style_LIST: List based on loop mode
        if not styles:
            selected_style_LIST = ["No styles found."]
        elif LOOP_SEQUENTIAL and LOOP_style_LIST:
            # Sequential mode for styles
            max_styles = len(styles)
            next_index = self.get_next_index(STYLE_LIST_COUNTER_FILE, jump, max_styles)
            selected_style = styles[next_index]
            selected_style_LIST = [self.format_style(selected_style, descriptor, model)]
        elif LOOP_style_LIST:
            # Return full list of styles
            selected_style_LIST = [self.format_style(s, descriptor, model) for s in styles]
        else:
            # Default: single selected style
            selected_style_LIST = [self.format_style(style, descriptor, model)]

        # recommended_with_selected_category: Single string based on input style
        if models:
            recommended_model = models[0][0]  # First model's name
            recommended_with_selected_category = self.format_style(style, descriptor, recommended_model)
        else:
            recommended_with_selected_category = ""

        # random_LIST_with_selected_category: List based on LOOP_random_LIST and LOOP_SEQUENTIAL
        if LOOP_SEQUENTIAL and LOOP_random_LIST:
            # Sequential mode for models
            if not models:
                random_LIST_with_selected_category = []
            else:
                max_models = len(models)
                next_index = self.get_next_index(MODEL_LIST_COUNTER_FILE, jump, max_models)
                selected_model = models[next_index][0]
                random_LIST_with_selected_category = [self.format_style(style, descriptor, selected_model)]
        elif LOOP_random_LIST:
            # Return list of selected style with all models
            random_LIST_with_selected_category = [self.format_style(style, descriptor, m[0]) for m in models] if models else []
        else:
            # Default: single random style and model
            if models:
                random_model = rng.choice(models)[0]
                random_style = rng.choice(styles)
                random_LIST_with_selected_category = [self.format_style(random_style, descriptor, random_model)]
            else:
                random_LIST_with_selected_category = []

        return (
            selected_category,
            selected_style_LIST,
            recommended_with_selected_category,
            random_LIST_with_selected_category
        )

# API endpoints for counter management
@PromptServer.instance.routes.post("/reset_style_list_counter")
async def reset_style_list_counter(request):
    try:
        os.remove(STYLE_LIST_COUNTER_FILE)
        return web.json_response({"success": True}, status=200)
    except FileNotFoundError:
        return web.json_response({"success": True}, status=200)
    except Exception as e:
        return web.json_response({"success": False, "error": str(e)}, status=500)

@PromptServer.instance.routes.post("/reset_model_list_counter")
async def reset_model_list_counter(request):
    try:
        os.remove(MODEL_LIST_COUNTER_FILE)
        return web.json_response({"success": True}, status=200)
    except FileNotFoundError:
        return web.json_response({"success": True}, status=200)
    except Exception as e:
        return web.json_response({"success": False, "error": str(e)}, status=500)

@PromptServer.instance.routes.post("/get_style_list_counter")
async def get_style_list_counter(request):
    try:
        with open(STYLE_LIST_COUNTER_FILE, 'r') as f:
            current_index = int(f.read().strip())
        return web.json_response({"success": True, "value": current_index + 1}, status=200)
    except (FileNotFoundError, ValueError):
        return web.json_response({"success": True, "value": 0}, status=200)
    except Exception as e:
        return web.json_response({"success": False, "error": str(e)}, status=500)

@PromptServer.instance.routes.post("/get_model_list_counter")
async def get_model_list_counter(request):
    try:
        with open(MODEL_LIST_COUNTER_FILE, 'r') as f:
            current_index = int(f.read().strip())
        return web.json_response({"success": True, "value": current_index + 1}, status=200)
    except (FileNotFoundError, ValueError):
        return web.json_response({"success": True, "value": 0}, status=200)
    except Exception as e:
        return web.json_response({"success": False, "error": str(e)}, status=500)
    
    
    
    
    
# class StyleSelector:
#     @classmethod
#     def INPUT_TYPES(cls):
#         # Input configuration remains unchanged
#         ALL_STYLES = sorted(set(style for styles in BRANCHES.values() for style in styles))
#         ALL_MODELS = ["None"] + sorted(MODELS.keys())
#         return {
#             "required": {
#                 "category": (CATEGORIES,),
#                 "style": (ALL_STYLES,),
#                 "model": (ALL_MODELS, {"default": "None"}),
#                 "seed": ("INT", {"default": -1, "min": -1, "max": 0x7FFFFFFFFFFFFFFF}),
#                 "LOOP_random_LIST": ("BOOLEAN", {"default": False}),
#                 "LOOP_style_LIST": ("BOOLEAN", {"default": False}),
#             }
#         }

#     RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING")
#     RETURN_NAMES = (
#         "selected_category",
#         "selected_style_LIST",
#         "recommended_with_selected_category",
#         "random_LIST_with_selected_category"
#     )
#     OUTPUT_IS_LIST = (False, True, False, True)  # Updated: third element is now False
#     FUNCTION = "select_style"
#     CATEGORY = "Bjornulf"

#     def select_style(self, category, style, seed, LOOP_random_LIST, LOOP_style_LIST, model=None):
#         DESCRIPTORS = {
#             "Painting": "painting",
#             "Photography": "photography",
#             "Illustration": "illustration",
#         }
#         rng = random.Random() if seed == -1 else random.Random(seed)
#         descriptor = DESCRIPTORS.get(category, "")

#         # selected_category: Single string (unchanged)
#         selected_category = category

#         # selected_style_LIST: List (unchanged)
#         if LOOP_style_LIST:
#             styles = BRANCHES.get(category, [])
#             if model != "None" and model in MODELS:
#                 urn, link = MODELS[model]
#                 selected_style_LIST = [
#                     f"{s} {descriptor};{model};{urn};{link}" for s in styles
#                 ]
#             else:
#                 selected_style_LIST = [f"{s} {descriptor}" for s in styles]
#         else:
#             if model != "None" and model in MODELS:
#                 urn, link = MODELS[model]
#                 selected_style_LIST = [f"{style} {descriptor};{model};{urn};{link}"]
#             else:
#                 selected_style_LIST = [f"{style} {descriptor}"]

#         # recommended_with_selected_category: Now a single string
#         if category in BRANCHES_MODELS and BRANCHES_MODELS[category]:
#             recommended_model = BRANCHES_MODELS[category][0]  # First model
#             recommended_with_selected_category = f"{style} {descriptor};{recommended_model[0]};{recommended_model[1]};{recommended_model[2]}"
#         else:
#             recommended_with_selected_category = ""

#         # random_LIST_with_selected_category: List (unchanged)
#         if LOOP_random_LIST:
#             if category in BRANCHES_MODELS and BRANCHES_MODELS[category]:
#                 models = BRANCHES_MODELS[category]
#                 random_LIST_with_selected_category = [
#                     f"{style} {descriptor};{m[0]};{m[1]};{m[2]}" for m in models
#                 ]
#             else:
#                 random_LIST_with_selected_category = []
#         else:
#             if category in BRANCHES_MODELS and BRANCHES_MODELS[category]:
#                 random_model = rng.choice(BRANCHES_MODELS[category])
#                 random_style_base = rng.choice(BRANCHES[category])
#                 random_style = f"{random_style_base} {descriptor}" if descriptor else random_style_base
#                 random_LIST_with_selected_category = [
#                     f"{random_style};{random_model[0]};{random_model[1]};{random_model[2]}"
#                 ]
#             else:
#                 random_LIST_with_selected_category = []

#         return (
#             selected_category,
#             selected_style_LIST,
#             recommended_with_selected_category,
#             random_LIST_with_selected_category
#         )
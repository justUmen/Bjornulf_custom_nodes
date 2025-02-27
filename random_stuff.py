import random
from typing import Tuple

class RandomIntNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"min_value": ("INT", {"default": 1}), "max_value": ("INT", {"default": 10}), "seed": ("INT", {
            "default": 0,
            "min": 0,
            "max": 4294967294
        })}}

    RETURN_TYPES = ("INT", "STRING")
    FUNCTION = "generate_random_int"
    CATEGORY = "Bjornulf"

    def generate_random_int(self, min_value: int, max_value: int, seed: int) -> Tuple[int, str]:
        rand_int = random.randint(min_value, max_value)
        return rand_int, f"{rand_int}"


class RandomFloatNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"min_value": ("FLOAT", {"default": 1.0}), "max_value": ("FLOAT", {"default": 10.0}), "seed": ("INT", {
            "default": 0,
            "min": 0,
            "max": 4294967294
        })}}

    RETURN_TYPES = ("FLOAT", "STRING")
    FUNCTION = "generate_random_float"
    CATEGORY = "Bjornulf"

    def generate_random_float(self, min_value: float, max_value: float, seed: int) -> Tuple[float, str]:
        rand_float = round(random.uniform(min_value, max_value), 2)
        return rand_float, f"{rand_float:.2f}"

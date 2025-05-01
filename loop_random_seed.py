class LoopRandomSeed:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "num_seeds": ("INT", {"default": 10, "min": 1, "max": 1000, "step": 1}),
                "generator_seed": ("INT", {"default": 0, "min": 0, "max": 1000000, "step": 1}),
            }
        }

    RETURN_TYPES = ("INT",)
    OUTPUT_IS_LIST = (True,)
    FUNCTION = "create_random_seeds"
    CATEGORY = "Bjornulf"

    def create_random_seeds(self, num_seeds, generator_seed):
        import random
        rng = random.Random(generator_seed)
        seeds = [rng.randint(0, 4294967295) for _ in range(num_seeds)]
        return (seeds,)
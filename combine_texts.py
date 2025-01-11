class CombineTexts:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "number_of_inputs": ("INT", {"default": 2, "min": 2, "max": 50, "step": 1}),
                "delimiter": (["newline", "comma", "space", "slash", "nothing"], {"default": "newline"}),
            },
            "hidden": {
                **{f"text_{i}": ("STRING", {"forceInput": True}) for i in range(1, 51)}
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "combine_texts"
    OUTPUT_IS_LIST = (False,)
    CATEGORY = "Bjornulf"

    def combine_texts(self, number_of_inputs, delimiter, **kwargs):
        def flatten(item):
            if isinstance(item, str):
                return item
            elif isinstance(item, list):
                return self.get_delimiter(delimiter).join(map(flatten, item))
            else:
                return str(item)

        combined_text = self.get_delimiter(delimiter).join([
            flatten(kwargs[f"text_{i}"])
            for i in range(1, number_of_inputs + 1)
            if f"text_{i}" in kwargs
        ])
        return (combined_text,)

    @staticmethod
    def get_delimiter(delimiter):
        if delimiter == "newline":
            return "\n"
        elif delimiter == "comma":
            return ","
        elif delimiter == "space":
            return " "
        elif delimiter == "slash":
            return "/"
        elif delimiter == "nothing":
            return ""
        else:
            return "\n"
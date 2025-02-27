class CombineTexts:
    SPECIAL_PREFIX = "ImSpEcIaL"  # The special text (password) to look for

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "number_of_inputs": ("INT", {"default": 2, "min": 2, "max": 100, "step": 1}),
                "delimiter": (["newline", "comma", "space", "slash", "backslash", "nothing"], {"default": "newline"}),
            },
            "hidden": {
                **{f"text_{i}": ("STRING", {"forceInput": True}) for i in range(1, 101)}
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

        # Check each input for the special prefix
        for i in range(1, number_of_inputs + 1):
            text_key = f"text_{i}"
            if text_key in kwargs:
                text = flatten(kwargs[text_key])
                if text.startswith(self.SPECIAL_PREFIX):
                    # Output only the text after the prefix, stripping leading whitespace
                    return (text[len(self.SPECIAL_PREFIX):].lstrip(),)

        # If no prefix is found, combine all non-empty inputs as usual
        text_entries = [
            flatten(kwargs.get(f"text_{i}", ""))
            for i in range(1, number_of_inputs + 1)
            if f"text_{i}" in kwargs and flatten(kwargs.get(f"text_{i}", "")).strip() != ""
        ]
        combined_text = self.get_delimiter(delimiter).join(text_entries)
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
        elif delimiter == "backslash":
            return "\\"
        elif delimiter == "nothing":
            return ""
        else:
            return "\n"
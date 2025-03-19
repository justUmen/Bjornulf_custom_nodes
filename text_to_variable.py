class TextToVariable:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"variable_name": ("STRING", {"default": "variable_name"}),
                              "text_value": ("STRING", {"forceInput": True})}}
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "process"
    CATEGORY = "Custom"
    
    def process(self, variable_name, text_value):
        text_value = text_value.replace("\n", "")
        output_string = f"{variable_name} = {text_value}"
        return (output_string,)
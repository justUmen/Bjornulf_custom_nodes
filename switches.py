class Everything(str):
    def __ne__(self, __value: object) -> bool:
        return False

class SwitchAnything:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "anything": (Everything("*"), {"forceInput": True}),
                "switch": ("BOOLEAN", {"default": True})
            }
        }

    RETURN_TYPES = (Everything("*"),)
    RETURN_NAMES = ("anything",)
    FUNCTION = "process_switch"
    CATEGORY = "Bjornulf"

    def process_switch(self, anything, switch):
        if switch:
            return (anything,)
        else:
            return ("",)
        
class SwitchText:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "STRING": ("STRING", {"forceInput": True}),
                "switch": ("BOOLEAN", {"default": True}),
                "ONLY_ME_combine_text": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("STRING",)
    FUNCTION = "process_switch"
    CATEGORY = "Bjornulf"

    def process_switch(self, STRING, switch, ONLY_ME_combine_text):
        if ONLY_ME_combine_text:
            return (f"ImSpEcIaL{STRING}",)
        if switch:
            return (STRING,)
        else:
            return ("",)
        
class ConditionalSwitch:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "condition": ("BOOLEAN", {"default": False}),  # True or False to pick the path
            },
            "optional": {
                "input_data": (Everything("*"), {"forceInput": True}),  # Passthrough any data type
            }
        }

    RETURN_TYPES = (Everything("*"), Everything("*"))  # Two outputs, dynamically typed
    RETURN_NAMES = ("TRUE", "FALSE")  # Named outputs for clarity
    FUNCTION = "switch"
    CATEGORY = "Utilities"

    def switch(self, condition, input_data=None):
        if condition:
            # If condition is True, send data to TRUE output, FALSE gets None
            return (input_data, None)
        else:
            # If condition is False, send data to FALSE output, TRUE gets None
            return (None, input_data)
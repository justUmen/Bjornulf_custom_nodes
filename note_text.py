class Everything(str):
    def __ne__(self, __value: object) -> bool:
        return False

class DisplayNote:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "any": (Everything("*"), {"forceInput": True}),  # Accept any input
                "display_text": ("STRING", {
                    "multiline": True,  # Allow multiline text
                    "default": ""  # Default text
                }),
            }
        }
    
    RETURN_TYPES = (Everything("*"),)  # Return same type as input
    RETURN_NAMES = ("any",)  # Return same type as input
    FUNCTION = "display_text_pass"
    CATEGORY = "Bjornulf"
    
    def display_text_pass(self, any, display_text):
        # Simply pass through the input
        if any is None:
            return (None,)
        else:
            return (any,)
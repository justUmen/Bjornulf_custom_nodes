class Everything(str):
    def __ne__(self, __value: object) -> bool:
        return False
class AnythingToText:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": { 
                "anything": (Everything("*"), {"forceInput": True})
            },
        }
    
    @classmethod
    def VALIDATE_INPUTS(s, input_types):
        return True
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "any_to_text"
    CATEGORY = "Bjornulf"
    
    def any_to_text(self, anything):
        # Convert the input to string representation
        return (str(anything),)
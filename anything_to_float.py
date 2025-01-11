class Everything(str):
    def __ne__(self, __value: object) -> bool:
        return False

class AnythingToFloat:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "anything": (Everything("*"), {"forceInput": True}),
            },
        }
    
    @classmethod
    def VALIDATE_INPUTS(s, input_types):
        return True
    
    RETURN_TYPES = ("FLOAT",)
    RETURN_NAMES = ("float",)
    FUNCTION = "any_to_float"
    CATEGORY = "Bjornulf"
    
    def any_to_float(self, anything):
        try:
            return (float(anything),)
        except (ValueError, TypeError):
            # Return 0.0 if conversion fails
            return (0.0,)
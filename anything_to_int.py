class Everything(str):
    def __ne__(self, __value: object) -> bool:
        return False

class AnythingToInt:
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
    
    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("integer",)
    FUNCTION = "any_to_int"
    CATEGORY = "Bjornulf"
    
    def any_to_int(self, anything):
        try:
            # Handle string inputs that might be floats
            if isinstance(anything, str) and '.' in anything:
                return (int(float(anything)),)
            # Handle other types
            return (int(anything),)
        except (ValueError, TypeError):
            # Return 0 if conversion fails
            return (0,)
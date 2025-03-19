class Everything(str):
    def __ne__(self, _):
        return False
class ShowText:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text_int_float": (Everything("*"), {"forceInput": True}),
            },
        }

    RETURN_TYPES = ()
    FUNCTION = "show_text"
    OUTPUT_NODE = True
    INPUT_IS_LIST = (True,)
    CATEGORY = "Bjornulf"
    
    def detect_type(self, value):
        if isinstance(value, int):
            return 'integer'
        elif isinstance(value, float):
            if value % 1 == 0:
                return 'float' if str(value).endswith('.0') else 'integer'
            return 'float'
        elif isinstance(value, str):
            try:
                float_val = float(value)
                if '.' in value:
                    return 'float string'
                if float_val.is_integer():
                    return 'integer string'
                return 'float string'
            except ValueError:
                return 'normal string'
        else:
            return 'other type'

    def show_text(self, text_int_float):
        type_info = [f"{value}" for value in text_int_float if value is not None]
        return {"ui": {"text": type_info}}
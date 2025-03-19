class ListSelector:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_LIST": ("STRING", {"forceInput": True}),
                "selection": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 9999  # Reasonable upper limit
                }),
                "delimiter": ("STRING", {
                    "default": ";",
                    "multiline": False
                })
            }
        }

    RETURN_TYPES = ("INT", "STRING", "INT")
    RETURN_NAMES = ("selected_element_INT", "selected_element_STRING", "list_length_INT")
    FUNCTION = "select_number"
    CATEGORY = "Bjornulf"

    def select_number(self, input_LIST: str, selection: int, delimiter: str):
        # Split the string into a list using the delimiter
        numbers = input_LIST.split(delimiter)
        
        # Remove any empty strings and strip whitespace
        numbers = [num.strip() for num in numbers if num.strip()]
        
        # Get list length
        list_length = len(numbers)
        
        # Validate selection
        if list_length == 0:
            return 0, "0", 0
        if selection > list_length:
            selection = list_length  # Clamp to max
        elif selection < 1:
            selection = 1  # Clamp to min
            
        # Convert to 0-based index
        index = selection - 1
        
        # Get the selected element
        selected = numbers[index]
        
        # Try to convert to integer, but keep string value regardless
        try:
            selected_int = int(selected)
        except ValueError:
            selected_int = 0  # Return 0 for non-numeric values
            
        selected_str = selected  # Return original string value
        
        return selected_int, selected_str, list_length
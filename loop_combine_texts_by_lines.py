class CombineTextsByLines:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "number_of_inputs": ("INT", {"default": 2, "min": 1, "max": 50, "step": 1}),
                "number_of_lines": ("INT", {"default": 3, "min": 1, "max": 50, "step": 1}),
            }
        }

    RETURN_TYPES = tuple(["STRING"] * 50)  # Maximum 50 lines
    RETURN_NAMES = tuple([f"line_{i+1}" for i in range(50)])
    FUNCTION = "extract_lines"
    OUTPUT_NODE = True
    CATEGORY = "Bjornulf"
    OUTPUT_IS_LIST = tuple([True] * 50)  # Indicate that all outputs are lists

    def extract_lines(self, number_of_inputs, number_of_lines, **kwargs):
        grouped_lines = [[] for _ in range(number_of_lines)]

        for i in range(1, number_of_inputs + 1):
            text_key = f"text_{i}"
            if text_key in kwargs and kwargs[text_key]:
                lines = kwargs[text_key].split('\n')
                lines = [line.strip() for line in lines if line.strip()]
                for j, line in enumerate(lines[:number_of_lines]):
                    grouped_lines[j].append(line)

        outputs = []
        for group in grouped_lines:
            # Instead of joining the lines, keep them as a list
            outputs.append(group)

        # Pad the output to always return 50 items
        outputs.extend([[] for _ in range(50 - len(outputs))])

        return tuple(outputs)

    @classmethod
    def IS_CHANGED(cls, number_of_inputs, number_of_lines, ** kwargs):
        return float("NaN")  # This forces the node to always update

    @classmethod
    def VALIDATE_INPUTS(cls, number_of_inputs, number_of_lines, **kwargs):
        if number_of_lines < 1 or number_of_lines > 50:
            return "Number of lines must be between 1 and 50"
        if number_of_inputs < 1 or number_of_inputs > 50:
            return "Number of inputs must be between 1 and 50"
        return True

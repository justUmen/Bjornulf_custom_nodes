class MathNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "operation": (["+", "-", "*", "/", "%"], {"default": "+"}),
                "num_inputs": ("INT", {"default": 2, "min": 2, "max": 100, "step": 1}),
            },
            "hidden": {
                **{f"value_{i}": ("*", {"forceInput": True}) for i in range(1, 101)}
            }
        }

    RETURN_TYPES = ("FLOAT", "INT", "STRING")
    FUNCTION = "compute"
    CATEGORY = "Utilities/Math"

    def compute(self, operation, num_inputs, **kwargs):
        # Collect and convert inputs to float, defaulting to 0.0 if conversion fails or input is missing
        values = []
        for i in range(1, num_inputs + 1):
            key = f"value_{i}"
            raw_value = kwargs.get(key, 0.0)
            try:
                # Attempt to convert any input to float
                value = float(raw_value)
            except (ValueError, TypeError):
                value = 0.0  # Fallback to 0.0 if conversion fails
            values.append(value)

        # If no valid values, return 0.0, 0, "0.0"
        if not values:
            return (0.0, 0, "0.0")

        # Initialize result with the first value
        result = values[0]

        # Apply the selected operation cumulatively from left to right
        for val in values[1:]:
            if operation == "+":
                result += val
            elif operation == "-":
                result -= val
            elif operation == "*":
                result *= val
            elif operation == "/":
                if val == 0:
                    result = 0.0  # Handle division by zero
                else:
                    result /= val
            elif operation == "%":
                if val == 0:
                    result = 0.0  # Handle modulo by zero
                else:
                    result %= val

        # Create integer and string versions of the result
        int_result = int(result)  # Truncate to integer
        str_result = str(result)  # Convert to string

        # Return the three outputs
        return (result, int_result, str_result)
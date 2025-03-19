class Everything(str):
    def __ne__(self, __value: object) -> bool:
        return False

class IfElse:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input": (Everything("*"), {"forceInput": True, "multiline": False}),
                "input_type": ([
                    "STRING: input EQUAL TO compare_with",
                    "STRING: input NOT EQUAL TO compare_with",
                    "BOOLEAN: input IS TRUE",
                    "BOOLEAN: input IS FALSE",
                    "NUMBER: input GREATER THAN compare_with",
                    "NUMBER: input GREATER OR EQUAL TO compare_with",
                    "NUMBER: input LESS THAN compare_with",
                    "NUMBER: input LESS OR EQUAL TO compare_with"
                ], {"default": "STRING: input EQUAL TO compare_with"}),
                "send_if_true": (Everything("*"),),
                "compare_with": ("STRING", {"multiline": False}),
            },
            "optional": {
                "send_if_false": (Everything("*"),),
            }
        }

    RETURN_TYPES = (Everything("*"), Everything("*"), "STRING", "STRING", "STRING")
    RETURN_NAMES = ("output", "rejected", "input_type", "true_or_false", "details")
    FUNCTION = "if_else"
    CATEGORY = "Bjornulf"

    def if_else(self, input, send_if_true, compare_with, input_type, send_if_false=None):
        result = False
        input_type_str = "STRING"
        details = f"input: {input}\ncompare_with: {compare_with}\n"
        error_message = ""

        # Input validation
        if input_type.startswith("NUMBER:"):
            try:
                float(input)
                float(compare_with)
            except ValueError:
                error_message = "If-Else ERROR: For numeric comparisons, both \"input\" and \"compare_with\" must be valid numbers.\n"
        elif input_type == "BOOLEAN: input IS TRUE":
            if str(input).lower() not in ("true", "false", "1", "0", "yes", "no", "y", "n", "on", "off"):
                error_message = "If-Else ERROR: For boolean check, \"input\" must be a recognizable boolean value.\n"

        if error_message:
            details = error_message + "\n" + details
            details += "\nContinuing with default string comparison."
            input_type = "STRING: input EQUAL TO compare_with"

        if input_type == "STRING: input EQUAL TO compare_with":
            result = str(input) == str(compare_with)
            details += f"\nCompared strings: '{input}' == '{compare_with}'"
        elif input_type == "STRING: input NOT EQUAL TO compare_with":
            result = str(input) != str(compare_with)
            details += f"\nCompared strings: '{input}' != '{compare_with}'"
        elif input_type == "BOOLEAN: input IS TRUE":
            result = str(input).lower() in ("true", "1", "yes", "y", "on")
            details += f"\nChecked if '{input}' is considered True"
        elif input_type == "BOOLEAN: input IS FALSE":
            result = str(input).lower() in ("false", "0", "no", "n", "off")
            details += f"\nChecked if '{input}' is considered True"
        else:  # Numeric comparisons
            try:
                input_num = float(input)
                compare_num = float(compare_with)
                if input_type == "NUMBER: input GREATER THAN compare_with":
                    result = input_num > compare_num
                    details += f"\nCompared numbers: {input_num} > {compare_num}"
                elif input_type == "NUMBER: input GREATER OR EQUAL TO compare_with":
                    result = input_num >= compare_num
                    details += f"\nCompared numbers: {input_num} >= {compare_num}"
                elif input_type == "NUMBER: input LESS THAN compare_with":
                    result = input_num < compare_num
                    details += f"\nCompared numbers: {input_num} < {compare_num}"
                elif input_type == "NUMBER: input LESS OR EQUAL TO compare_with":
                    result = input_num <= compare_num
                    details += f"\nCompared numbers: {input_num} <= {compare_num}"
                input_type_str = "FLOAT" if "." in str(input) else "INT"
            except ValueError:
                result = str(input) == str(compare_with)
                details += f"\nUnexpected error in numeric conversion, compared as strings: '{input}' == '{compare_with}'"

        if result:
            output = send_if_true
            rejected = send_if_false if send_if_false is not None else None
        else:
            output = send_if_false if send_if_false is not None else None
            rejected = send_if_true


        result_str = str(result)
        details += f"\nResult: {result_str}"
        details += f"\nReturned value to {'output' if result else 'rejected'}"
        details += f"\n\noutput: {output}"
        details += f"\nrejected: {rejected}"

        return (output, rejected, input_type_str, result_str, details)
    
    @classmethod
    def IS_CHANGED(cls, input, send_if_true, compare_with, input_type, send_if_false=None):
        return float("NaN")
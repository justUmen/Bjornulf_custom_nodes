import os
import re
import random
import csv
from itertools import cycle
from aiohttp import web
from server import PromptServer

class LineSelector:
    def __init__(self):
        self._counter = -1
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"multiline": True}),  # Input for multiple lines
                "line_number": ("INT", {"default": 0, "min": 0, "max": 99999}),  # 0 for random, >0 for specific line
                "RANDOM": ("BOOLEAN", {"default": False}),  # Force random selection
                "LOOP": ("BOOLEAN", {"default": False}),  # Return all lines as list
                "LOOP_SEQUENTIAL": ("BOOLEAN", {"default": False}),  # Sequential looping
                "jump": ("INT", {"default": 1, "min": 1, "max": 100, "step": 1}),  # Jump size for sequential loop
                "pick_random_variable": ("BOOLEAN", {"default": True}),  # Enable random choice functionality
            },
            "optional": {
                "variables": ("STRING", {"multiline": True, "forceInput": True}),
                "seed": ("INT", {
                    "default": -1,
                    "min": -1,
                    "max": 0x7FFFFFFFFFFFFFFF
                }),
            },
        }

    RETURN_TYPES = ("STRING", "INT", "INT")  # String output, remaining cycles, current line number
    RETURN_NAMES = ("text", "remaining_cycles", "current_line")
    OUTPUT_IS_LIST = (True, False, False)  # Only text output can be a list
    FUNCTION = "select_line"
    CATEGORY = "Bjornulf"

    def find_variables(self, text):
        stack = []
        variables = []
        for i, char in enumerate(text):
            if char == '{':
                stack.append((i, len(stack) + 1))
            elif char == '}' and stack:
                start, nesting = stack.pop()
                variables.append({
                    'start': start,
                    'end': i + 1,
                    'nesting': nesting
                })
        variables.sort(key=lambda x: (-x['nesting'], -x['end']))
        return variables

    def parse_option(self, part):
        if part.startswith('%csv='):
            try:
                filename = part.split('=', 1)[1].strip()
                with open(filename, 'r') as f:
                    return [row[0] for row in csv.reader(f)]
            except Exception as e:
                return [f"[CSV Error: {str(e)}]"]
        elif '(' in part and '%)' in part:
            option, weight = part.rsplit('(', 1)
            return (option.strip(), float(weight.split('%)')[0]))
        return part.strip()

    def process_content(self, content, seed):
        random.seed(seed)
        parts = []
        weights = []
        group_defined = False
        group_name = None
        
        for p in content.split('|'):
            p = p.strip()
            if p.startswith('group='):
                group_name = p.split('=', 1)[1].strip()
                group_defined = True
                continue
                
            parsed = self.parse_option(p)
            if isinstance(parsed, list):  # CSV data
                parts.extend(parsed)
                weights.extend([1]*len(parsed))
            elif isinstance(parsed, tuple):  # Weighted option
                parts.append(parsed[0])
                weights.append(parsed[1])
            else:
                parts.append(parsed)
                weights.append(1)

        if group_defined:
            return {'type': 'group', 'name': group_name, 'options': parts}

        if any(w != 1 for w in weights):
            total = sum(weights)
            if total == 0: weights = [1]*len(parts)
            return random.choices(parts, weights=[w/total for w in weights])[0]
            
        return random.choice(parts) if parts else ''

    def process_advanced_syntax(self, text, seed):
        # Process nested variables
        variables = self.find_variables(text)
        substitutions = []
        groups = {}

        for var in variables:
            start, end = var['start'], var['end']
            content = text[start+1:end-1]
            processed = self.process_content(content, seed)
            
            if isinstance(processed, dict):
                if processed['type'] == 'group':
                    group_name = processed['name']
                    if group_name not in groups:
                        groups[group_name] = []
                    groups[group_name].append({
                        'start': start,
                        'end': end,
                        'options': processed['options']
                    })
            else:
                substitutions.append({
                    'start': start,
                    'end': end,
                    'sub': processed
                })

        # Handle groups
        for group_name, matches in groups.items():
            if not matches or not matches[0]['options']:
                continue
            
            options = matches[0]['options']
            permuted = random.sample(options, len(options))
            perm_cycle = cycle(permuted)
            
            for m in matches:
                substitutions.append({
                    'start': m['start'],
                    'end': m['end'],
                    'sub': next(perm_cycle)
                })

        # Apply regular substitutions
        substitutions.sort(key=lambda x: -x['start'])
        result_text = text
        for sub in substitutions:
            result_text = result_text[:sub['start']] + sub['sub'] + result_text[sub['end']:]

        return result_text

    def select_line(self, text, line_number, RANDOM, LOOP, LOOP_SEQUENTIAL, jump, pick_random_variable, variables="", seed=-1):
        # Parse variables
        var_dict = {}
        for line in variables.split('\n'):
            if '=' in line:
                key, value = line.split('=', 1)
                var_dict[key.strip()] = value.strip()
        
        # Replace variables in the text
        for key, value in var_dict.items():
            text = text.replace(f"<{key}>", value)
        
        # Split the input text into lines, remove empty lines and lines starting with #
        lines = [line.strip() for line in text.split('\n') 
                if line.strip() and not line.strip().startswith('#')]
        
        if not lines:
            return (["No valid lines found."], 0, 0)
        
        import random
        import os
        
        # Set seed if provided
        if seed < 0:
            seed = random.randint(0, 0x7FFFFFFFFFFFFFFF)

        # Process WriteTextAdvanced syntax if enabled
        if pick_random_variable:
            processed_lines = []
            for line in lines:
                processed_lines.append(self.process_advanced_syntax(line, seed))
            lines = processed_lines

        # Handle sequential looping
        if LOOP_SEQUENTIAL:
            counter_file = os.path.join("Bjornulf", "line_selector_counter.txt")
            os.makedirs(os.path.dirname(counter_file), exist_ok=True)

            try:
                with open(counter_file, 'r') as f:
                    current_index = int(f.read().strip())
            except (FileNotFoundError, ValueError):
                current_index = -jump

            next_index = current_index + jump

            if next_index >= len(lines):
                with open(counter_file, 'w') as f:
                    f.write(str(-jump))
                raise ValueError(f"Counter has reached the last line (total lines: {len(lines)}). Counter has be reset.")

            with open(counter_file, 'w') as f:
                f.write(str(next_index))

            remaining_cycles = max(0, (len(lines) - next_index - 1) // jump + 1)
            return ([lines[next_index]], remaining_cycles, next_index + 1)

        # Handle normal LOOP mode
        if LOOP:
            return (lines, len(lines), 0)
            
        # Handle RANDOM or line_number selection
        if RANDOM or line_number == 0:
            selected = random.choice(lines)
        else:
            index = min(line_number - 1, len(lines) - 1)
            index = max(0, index)
            selected = lines[index]
        
        return ([selected], 0, line_number if line_number > 0 else 0)

    @classmethod
    def IS_CHANGED(s, text, line_number, RANDOM, LOOP, LOOP_SEQUENTIAL, jump, pick_random_variable, variables="", seed=-1):
        return float("NaN") if LOOP_SEQUENTIAL else (text, line_number, RANDOM, LOOP, LOOP_SEQUENTIAL, jump, pick_random_variable, variables, seed)

@PromptServer.instance.routes.post("/reset_line_selector_counter")
async def reset_line_selector_counter(request):
    counter_file = os.path.join("Bjornulf", "line_selector_counter.txt")
    try:
        os.remove(counter_file)
        return web.json_response({"success": True}, status=200)
    except FileNotFoundError:
        return web.json_response({"success": True}, status=200)
    except Exception as e:
        return web.json_response({"success": False, "error": str(e)}, status=500)

@PromptServer.instance.routes.post("/get_line_selector_counter")
async def get_line_selector_counter(request):
    counter_file = os.path.join("Bjornulf", "line_selector_counter.txt")
    try:
        with open(counter_file, 'r') as f:
            current_index = int(f.read().strip())
        return web.json_response({"success": True, "value": current_index + 1}, status=200)
    except (FileNotFoundError, ValueError):
        return web.json_response({"success": True, "value": 0}, status=200)
    except Exception as e:
        return web.json_response({"success": False, "error": str(e)}, status=500)
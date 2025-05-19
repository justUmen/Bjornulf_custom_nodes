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
                "text": ("STRING", {"multiline": True}),
                "line_number": ("INT", {"default": 0, "min": 0, "max": 99999}),
                "RANDOM": ("BOOLEAN", {"default": False}),
                "LOOP": ("BOOLEAN", {"default": False}),
                "LOOP_SEQUENTIAL": ("BOOLEAN", {"default": False}),
                "jump": ("INT", {"default": 1, "min": 1, "max": 100, "step": 1}),
                "pick_random_variable": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "variables": ("STRING", {"multiline": True, "forceInput": True}),
                #"seed": ("INT", {"default": -1, "min": -1, "max": 0x7FFFFFFFFFFFFFFF}),
            },
        }

    RETURN_TYPES = ("STRING", "INT", "INT")
    RETURN_NAMES = ("text", "remaining_cycles", "current_line")
    OUTPUT_IS_LIST = (True, False, False)
    FUNCTION = "select_line"
    CATEGORY = "Bjornulf"

    def find_variables(self, text):
        """Identify nested curly brace sections in the text."""
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
        """Parse options within curly braces, handling CSV and weighted choices."""
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

    def process_content(self, content, base_seed, position):
        """Process content within curly braces, handling groups and random choices."""
        # Use a unique seed for regular choices based on position
        random.seed(base_seed + position)
        parts = [p.strip() for p in content.split('|')]
        options = []
        weights = []
        static_group = None
        cycling_group = None
        
        for p in parts:
            if p.startswith('static_group='):
                static_group = p.split('=', 1)[1].strip()
            elif p.startswith('group='):
                cycling_group = p.split('=', 1)[1].strip()
            else:
                parsed = self.parse_option(p)
                if isinstance(parsed, list):  # CSV data
                    options.extend(parsed)
                    weights.extend([1] * len(parsed))
                elif isinstance(parsed, tuple):  # Weighted option
                    options.append(parsed[0])
                    weights.append(parsed[1])
                else:
                    options.append(parsed)
                    weights.append(1)
        
        if static_group and cycling_group:
            raise ValueError("Cannot specify both static_group and group in the same section.")
        
        if static_group:
            return {'type': 'static_group', 'name': static_group, 'options': options, 'weights': weights}
        elif cycling_group:
            return {'type': 'cycling_group', 'name': cycling_group, 'options': options, 'weights': weights}
        else:
            if options:
                if any(w != 1 for w in weights):
                    total = sum(weights)
                    if total == 0:
                        weights = [1] * len(options)
                    return random.choices(options, weights=[w / total for w in weights])[0]
                else:
                    return random.choice(options)
            return ''

    def process_advanced_syntax(self, text, seed):
        """Process the entire text for advanced syntax, handling nested variables and groups."""
        variables = self.find_variables(text)
        static_groups = {}
        cycling_groups = {}
        substitutions = []

        for var in variables:
            start, end = var['start'], var['end']
            content = text[start + 1:end - 1]
            processed = self.process_content(content, seed, start)
            
            if isinstance(processed, dict):
                if processed['type'] == 'static_group':
                    name = processed['name']
                    if name not in static_groups:
                        static_groups[name] = []
                    static_groups[name].append({
                        'start': start,
                        'end': end,
                        'options': processed['options'],
                        'weights': processed['weights']
                    })
                elif processed['type'] == 'cycling_group':
                    name = processed['name']
                    if name not in cycling_groups:
                        cycling_groups[name] = []
                    cycling_groups[name].append({
                        'start': start,
                        'end': end,
                        'options': processed['options'],
                        'weights': processed['weights']
                    })
            else:
                substitutions.append({
                    'start': start,
                    'end': end,
                    'sub': processed
                })

        # Handle static groups: choose one value per group name
        random.seed(seed)  # Reset seed for consistent static group behavior
        for name, matches in static_groups.items():
            if not matches or not matches[0]['options']:
                continue
            options = matches[0]['options']
            weights = matches[0]['weights']
            if any(w != 1 for w in weights):
                total = sum(weights)
                if total == 0:
                    weights = [1] * len(options)
                chosen = random.choices(options, weights=[w / total for w in weights])[0]
            else:
                chosen = random.choice(options) if options else ''
            for m in matches:
                substitutions.append({
                    'start': m['start'],
                    'end': m['end'],
                    'sub': chosen
                })

        # Handle cycling groups: cycle through shuffled options
        random.seed(seed)  # Reset seed for consistent cycling group behavior
        for name, matches in cycling_groups.items():
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

        # Apply substitutions in reverse order
        substitutions.sort(key=lambda x: -x['start'])
        result_text = text
        for sub in substitutions:
            result_text = result_text[:sub['start']] + sub['sub'] + result_text[sub['end']:]

        return result_text

    def select_line(self, text, line_number, RANDOM, LOOP, LOOP_SEQUENTIAL, jump, pick_random_variable, variables="", seed=-1):
        """Select lines from the text based on the specified mode after processing advanced syntax."""
        var_dict = {}
        for line in variables.split('\n'):
            if '=' in line:
                key, value = line.split('=', 1)
                var_dict[key.strip()] = value.strip()
        
        for key, value in var_dict.items():
            text = text.replace(f"<{key}>", value)
        
        if seed < 0:
            seed = random.randint(0, 0x7FFFFFFFFFFFFFFF)
        
        if pick_random_variable:
            text = self.process_advanced_syntax(text, seed)
        
        lines = [line.strip() for line in text.split('\n') 
                 if line.strip() and not line.strip().startswith('#')]
        
        if not lines:
            return (["No valid lines found."], 0, 0)
        
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
                raise ValueError(f"Counter has reached the last line (total lines: {len(lines)}). Counter has been reset.")

            with open(counter_file, 'w') as f:
                f.write(str(next_index))

            remaining_cycles = max(0, (len(lines) - next_index - 1) // jump + 1)
            return ([lines[next_index]], remaining_cycles, next_index + 1)

        if LOOP:
            return (lines, len(lines), 0)
            
        if RANDOM or line_number == 0:
            selected = random.choice(lines)
        else:
            index = min(line_number - 1, len(lines) - 1)
            index = max(0, index)
            selected = lines[index]
        
        return ([selected], 0, line_number if line_number > 0 else 0)

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")

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
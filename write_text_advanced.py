import re
import random
import time
import csv
from itertools import cycle

#{red|blue}
#{left|right|middle|group=LR}+{left|right|middle|group=LR}+{left|right|middle|group=LR}
#{A(80%)|B(15%)|C(5%)}

class WriteTextAdvanced:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "lines": 10}),
            },
            "optional": {
                "variables": ("STRING", {"multiline": True, "forceInput": True}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "write_text_special"
    OUTPUT_NODE = True
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

    def write_text_special(self, text, variables="", seed=None):
        if seed is None or seed == 0:
            seed = int(time.time() * 1000)
        random.seed(seed)

        # Handle variables
        var_dict = {}
        for line in variables.split('\n'):
            if '=' in line:
                key, value = line.split('=', 1)
                var_dict[key.strip()] = value.strip()
        for key, value in var_dict.items():
            text = text.replace(f"<{key}>", value)

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

        return (result_text,)

    @classmethod
    def IS_CHANGED(s, text, variables="", seed=None):
        return (text, variables, seed)
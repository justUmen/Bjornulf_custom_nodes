import re
import random
import time
import csv
from itertools import cycle

#{red|blue}
#{left|right|middle|group=LMR}+{left|right|middle|group=LMR}+{left|right|middle|group=LMR}
#{A(80%)|B(15%)|C(5%)}
#2 {apple|orange|banana|static_group=FRUIT}s, one {apple|orange|banana|static_group=FRUIT} on the left, one {apple|orange|banana|static_group=FRUIT} on the right
#Double layer variable : <<CHAR>>
#CHAR = JESSICA
#JESSICA = en/jess.wav

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
        # Sort by descending nesting level and position to process inner variables first
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
        # Use position to vary the seed for independent random choices
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
            raise ValueError("Cannot specify both static_group and group in the same curly brace section.")
        
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

    def write_text_special(self, text, variables="", seed=None):
        """Main function to process text with special syntax."""
        if seed is None or seed == 0:
            seed = int(time.time() * 1000)

        # Process text: remove comments and empty lines
        text_lines = [line.strip() for line in text.split('\n') 
                     if line.strip() and not line.strip().startswith('#')]
        text = '\n'.join(text_lines)

        # Replace predefined variables
        var_dict = {}
        var_lines = [line.strip() for line in variables.split('\n')
                    if line.strip() and not line.strip().startswith('#')]
        for line in var_lines:
            if '=' in line:
                key, value = line.split('=', 1)
                var_dict[key.strip()] = value.strip()
        for key, value in var_dict.items():
            text = text.replace(f"<{key}>", value)

        # Process nested variables
        variables = self.find_variables(text)
        static_groups = {}
        cycling_groups = {}
        substitutions = []

        for var in variables:
            start, end = var['start'], var['end']
            content = text[start + 1:end - 1]
            # Pass the position (start) to vary the seed for non-group choices
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

        return (result_text,)

    @classmethod
    def IS_CHANGED(s, text, variables="", seed=None):
        """Check if inputs have changed."""
        return (text, variables, seed)
import re

def parse_settings(lines):
    settings = {}

    for line in lines:
        stripped = line.strip()
        
        match = re.match(r"\[(.+?):\s*(.+?)\]", stripped)
        if match:
            key, value = match.groups()

            if value.lower() == "true":
                value = True
            elif value.lower() == "false":
                value = False
            elif value.lower() == "null":
                value = None
            elif re.match(r'^-?\d+(\.\d+)?$', value):
                value = float(value) if "." in value else int(value)

            settings[key] = value
        else:
            break

    return settings

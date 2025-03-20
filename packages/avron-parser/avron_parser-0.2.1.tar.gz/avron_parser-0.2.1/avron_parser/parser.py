import re
from avron_parser.inline_parser import *
from avron_parser.settings_parser import *

def parse_avron(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    settings = parse_settings(lines)
    indent_level = settings.get("INDENT_LEVEL", 2)
    comment_syntax = settings.get("COMMENT_SYNTAX", "#")
    multi_line_comment_syntax = comment_syntax * 3
    use_tabs = settings.get("TAB_MODE", False)
    null_style = settings.get("NULL_STYLE", "null")
    boolean_style = settings.get("BOOLEAN_STYLE", "").split("-")
    multiline_style = settings.get("MULTILINE_STYLE", '"""')

    if len(boolean_style) == 2:
        true_value = boolean_style[0].strip('"').lower()
        false_value = boolean_style[1].strip('"').lower()
    else:
        true_value = "true"
        false_value = "false"

    root = {}
    context_stack = [(root, -indent_level)]
    multi_line_string = None
    last_key = None
    in_multi_line_comment = False

    for line in lines:
        line = line.rstrip()

        if use_tabs and " " in line[:len(line) - len(line.lstrip())]:
            raise ValueError("Invalid indentation: Spaces used in TAB_MODE.")
        if not use_tabs and "\t" in line[:len(line) - len(line.lstrip())]:
            raise ValueError("Invalid indentation: Tabs used when TAB_MODE is false.")

        if not use_tabs:
            line = line.replace("\t", " " * indent_level)

        if not line.strip():
            continue

        settings_line = re.match(r"\[(.+?):\s*(.+?)\]", line)
        if settings_line:
            continue

        if line.strip().startswith(f"{multi_line_comment_syntax}"):
            in_multi_line_comment = not in_multi_line_comment
            continue
        if in_multi_line_comment or line.strip().startswith(f"{comment_syntax}"):
            continue

        if f'{multiline_style}' in line:
            if multi_line_string is None:
                stripped = line.strip()
                last_key = stripped.split(":")[0].strip()
                multi_line_string = []
                continue
            else:
                value = "\n".join(multi_line_string).strip()
                current_obj, _ = context_stack[-1]
                current_obj[last_key] = value
                multi_line_string = None
                last_key = None
                continue

        if multi_line_string is not None:
            multi_line_string.append(line)
            continue

        indent = len(line) - len(line.lstrip())

        if indent % indent_level != 0:
            raise ValueError(f"Invalid indentation at: {line}\nExpected multiple of {indent_level}, got {indent}")

        indent = indent // indent_level
        stripped = line.strip()

        if ":" in stripped and not stripped.startswith("-"):
            key, value = map(str.strip, stripped.split(":", 1))
            last_key = key

            while context_stack and indent <= context_stack[-1][1]:
                context_stack.pop()

            current_obj, _ = context_stack[-1]

            if not value:
                new_obj = {}
                current_obj[key] = new_obj
                context_stack.append((new_obj, indent))
                continue

            value_lower = value.lower()
            if value_lower == true_value:
                value = True
            elif value_lower == false_value:
                value = False
            elif value.lower() == null_style:
                value = None
            elif re.match(r'^-?\d+(\.\d+)?$', value):
                value = float(value) if "." in value else int(value)
            elif value.startswith("[") and value.endswith("]"):
                value = parse_inline_list(value[1:-1])
            elif value.startswith("{") and value.endswith("}"):
                value = parse_inline_object(value[1:-1])

            current_obj[key] = value

        elif stripped.startswith("-"):
            value = stripped[1:].strip()

            value_lower = value.lower()
            if value_lower == true_value:
                value = True
            elif value_lower == false_value:
                value = False
            elif value.lower() == null_style:
                value = None
            elif re.match(r'^-?\d+(\.\d+)?$', value):
                value = float(value) if "." in value else int(value)

            current_obj, _ = context_stack[-1]

            if last_key not in current_obj:
                current_obj[last_key] = []
            elif not isinstance(current_obj[last_key], list):
                current_obj[last_key] = [current_obj[last_key]]

            current_obj[last_key].append(value)

    return root
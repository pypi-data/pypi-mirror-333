import re

def parse_inline_list(text):
  """Parse an inline list like [item1, item2, item3]"""
  items = []
  for item in text.split(","):
    item = item.strip()
    if not item:
      continue

    if item.lower() == "true":
      items.append(True)
    elif item.lower() == "false":
      items.append(False)
    elif item.lower() == "null":
      items.append(None)
    elif re.match(r'^-?\d+(\.\d+)?$', item):
      items.append(float(item) if "." in item else int(item))
    else:
      items.append(item)

  return items


def parse_inline_object(text):
  """Parse an inline object like {key1: value1, key2: value2}"""
  obj = {}
  for item in text.split(","):
    if ":" not in item:
      continue

    key, value = map(str.strip, item.split(":", 1))

    if value.lower() == "true":
      obj[key] = True
    elif value.lower() == "false":
      obj[key] = False
    elif value.lower() == "null":
      obj[key] = None
    elif re.match(r'^-?\d+(\.\d+)?$', value):
      obj[key] = float(value) if "." in value else int(value)
    else:
      obj[key] = value

  return obj
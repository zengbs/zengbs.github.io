import re
import sys

if len(sys.argv) < 2:
    print("Usage: python convert.py <input_file>")
    sys.exit(1)

input_file = sys.argv[1]

with open(input_file, "r", encoding="utf-8") as f:
    content = f.read()

# pattern: [title](/randomID)
pattern = re.compile(r'\[([^\]]+)\]\(/[^)]+\)')

def convert(match):
    title = match.group(1)
    slug = title.replace(" ", "_")
    return f'[{"{}".format(title)}]({{{{ "/notes/{slug}" | relative_url }}}})'

new_content = pattern.sub(convert, content)

with open(input_file, "w", encoding="utf-8") as f:
    f.write(new_content)

print(f"Converted: {input_file}")

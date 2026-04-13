import os

target_string = "tags: [linear-algebra]"
root_dir = "."

for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith(".md"):  # change extension filter if needed
            path = os.path.join(root, file)

            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

            new_content = content.replace(target_string, "")

            if new_content != content:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new_content)

                print(f"Updated: {path}")

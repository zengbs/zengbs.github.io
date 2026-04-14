import os

target = "tags: [linear-algebra]"

for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".md"):
            path = os.path.join(root, file)

            with open(path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            new_lines = [line for line in lines if target not in line]

            if new_lines != lines:
                with open(path, "w", encoding="utf-8") as f:
                    f.writelines(new_lines)

                print(f"Updated: {path}")

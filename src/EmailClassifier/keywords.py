from pathlib import Path

folder_path = Path("../../types")

keywords = dict()
senders = dict()

for type_path in folder_path.glob("*.txt"):
    if not type_path.is_file():
        continue
    name = type_path.stem
    lines = type_path.read_text(encoding="utf-8").splitlines()
    keywords[name] = []
    senders[name] = []

    i = 0
    while i < len(lines):
        if lines[i] == "":
            i += 1
            break
        keywords[name].append(lines[i].strip())
        i += 1

    while i < len(lines):
        if lines[i] != "":
            senders[name].append(lines[i].strip())

        i += 1


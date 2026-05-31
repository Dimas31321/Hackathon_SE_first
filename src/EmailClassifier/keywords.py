from pathlib import Path

folder_path = Path("types")

keywords = dict()

for type_path in folder_path.glob("*.txt"):
    if not type_path.is_file():
        continue
    name = type_path.stem
    lines = type_path.read_text(encoding="utf-8").splitlines()
    keywords[name] = [x.strip() for x in lines]
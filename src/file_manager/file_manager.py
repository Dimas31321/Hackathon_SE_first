from email import Email
from pathlib import Path
import logging

class Manager:
    path = Path('out')

    @staticmethod
    def put(email: Email):
        source_path = Path(email.filename)
        for category in email.categories:
            Manager._copy(source_path, category)

    @staticmethod
    def _copy(source_path: Path, category: str):
        name = source_path.name
        file_path = Manager.path / category / name
        if file_path.exists():
            logging.warning(f"{file_path} уже существует.")
            return
        file_path.parent.mkdir(parents=True, exist_ok=True)
        source_path.copy(file_path)
        

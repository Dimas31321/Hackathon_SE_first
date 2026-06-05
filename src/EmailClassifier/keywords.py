from pathlib import Path
import logging


logger = logging.getLogger(__name__)


def loadKeywords():
    keywords = dict()
    rootdit = Path(__file__).resolve()
    folder_path = Path(rootdit).parent.parent.parent / "types"


    logger.info("Чтение категорий успешно инициализироваось.")
    for type_path in folder_path.glob("*.txt"):
        if not type_path.is_file():
            logger.warning(f"{type_path.name} не является файлом")
            continue
        name = type_path.stem
        lines = type_path.read_text(encoding="utf-8").splitlines()
        keywords[name] = []

        i = 0
        while i < len(lines):
            if lines[i] == "":
                i += 1
                break
            keywords[name].append(lines[i].strip())
            i += 1

    return keywords


def loadSenders():
    senders = dict()

    rootdit = Path(__file__).resolve()
    folder_path = Path(rootdit).parent.parent.parent / "types"

    logger.info("Чтение категорий успешно инициализироваось.")
    for type_path in folder_path.glob("*.txt"):
        if not type_path.is_file():
            logger.warning(f"{type_path.name} не является файлом")
            continue
        name = type_path.stem
        lines = type_path.read_text(encoding="utf-8").splitlines()
        senders[name] = []

        i = 0
        
        while i < len(lines):
            if lines[i] == "":
                i += 1
                break
            i += 1

        while i < len(lines):
            if lines[i] != "":
                senders[name].append(lines[i].strip())

            i += 1

    return senders
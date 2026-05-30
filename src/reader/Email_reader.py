from src.Email import Email
from pathlib import Path
import re

class EmailReader:

    def __init__(self, filename: str):
        self.filename = filename if filename.endswith(".txt") else filename + ".txt"
        self.path = Path(filename)

    def _extract_address(self, address_str: str):
        if match := re.search(r'<(.*?)>', address_str):
            return match.group(1)
        return address_str

    def read_email(self) -> Email:
        try:
            with open(self.path, 'r') as file:
                lines = file.readlines()
        except FileNotFoundError:
            print(f"Файл '{self.filename}' не найден.")
            return None
        except PermissionError:
            print(f"Нет доступа к файлу '{self.filename}'.")
            return None
        except IsADirectoryError:
            print(f"'{self.filename}' является директорией, а не файлом.")
            return None
        except UnicodeDecodeError:
            print(f"Ошибка декодирования файла '{self.filename}'.")
            return None
        except Exception as e:
            print(f"Произошла ошибка при чтении файла '{self.filename}': {e}.")
            return None
        sender: str
        recipient: str
        theme: str
        sent_or_received: str
        body: str = ""
        date: str
        for line in lines:
            clean_line = line.strip()
            if clean_line.startswith("From:"):
                sender = clean_line[5:].strip() # Проверить 
                sender = self._extract_address(sender)
            elif clean_line.startswith("От кого:"):
                sender = clean_line[8:].strip()
                sender = self._extract_address(sender)
            # Рассмотреть и добавить другие варианты
            elif clean_line.startswith("To:"):
                recipient = clean_line[3:].strip() if len(clean_line) > 0 else None
                recipient = self._extract_address(recipient)
            elif clean_line.startswith("Кому:"):
                recipient = clean_line[6:].strip() if len(clean_line) > 0 else None
                recipient = self._extract_address(recipient)
            elif clean_line.startswith("Subject:"):
                theme = clean_line[8:].strip() if len(clean_line) > 0 else None
            elif clean_line.startswith("Тема:"):
            # Рассмотреть и добавить другие вариант
                theme = clean_line[5:].strip() if len(clean_line) > 0 else None
            elif (clean_line.startswith("Date:") 
                  or clean_line.startswith("Дата:")):
                date = clean_line[5:].strip() 
            else:
                body = body + line + "\n"
        return Email(sender, 
                     recipient, 
                     theme, 
                     self.filename,
                     None, # Неизвестно, отправлено или получено
                     body)
            
from src.email import Email
from pathlib import Path
import json

class EmailReader:
    def __init__(self, filename: str):
        self.filename = filename # Filename следует вводить с раширением, например "email.txt"
        self.path = Path(filename)
    def read_email(self) -> Email:
        if (self.filename.endswith('.txt') or self.filename.endswith('.bin')):
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
        elif self.filename.endswith('.json'):
            try:
                with open(self.path, 'r') as file:
                    lines = json.load(file)
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
        else:
            print(f"Неподдерживаемый формат файла '{self.filename}'. Поддерживаются только .txt и .json.")
            return None
        sender: str =""
        recipient: str = ""
        theme: str = ""
        sent_or_received: str = ""
        body: str = ""
        date: str = ""
        for line in lines:
            clean_line = line.strip()
            if clean_line.startswith("From:") and not sender: 
                sender = clean_line[5:].strip() # Проверить 
            elif clean_line.startswith("От кого:") and not sender:
                sender = clean_line[8:].strip()
            # Рассмотреть и добавить другие варианты
            elif clean_line.startswith("To:") and not recipient:
                recipient = clean_line[3:].strip() if len(clean_line) > 0 else None
            elif clean_line.startswith("Кому:") and not recipient:
                recipient = clean_line[6:].strip() if len(clean_line) > 0 else None
            elif clean_line.startswith("Subject:") and not theme:
                theme = clean_line[8:].strip() if len(clean_line) > 0 else None
            elif clean_line.startswith("Тема:") and not theme:
            # Рассмотреть и добавить другие вариант
                theme = clean_line[5:].strip() if len(clean_line) > 0 else None
            elif (clean_line.startswith("Date:") 
                  or clean_line.startswith("Дата:")) and not date:
                date = clean_line[5:].strip() 
            else:
                body = body + line + "\n"
        return Email(sender, 
                     recipient, 
                     theme, 
                     date, # Дата может быть в разных форматах, сложно распарсить
                     self.filename,
                     None, # Неизвестно, отправлено или получено
                     body)


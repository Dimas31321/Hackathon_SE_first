from src.email import Email
from pathlib import Path
import json
import re

class EmailReader:
    def __init__(self, filename: str):
        self.filename = filename # Filename следует вводить с раширением, например "email.txt"
        self.path = Path(filename)

    def _extract_address(self, address_str: str):
        if match := re.search(r'<(.*?)>', address_str):
            return match.group(1)
        return address_str

    def read_email(self) -> Email | None:
        if not self.path.exists():
            print(f"Файл '{self.filename}' не найден.")
            return None
        
        if self.path.is_dir():
            print(f"'{self.filename}' является директорией, а не файлом.")
            return None
        if self.filename.endswith(".txt"):
            data = self._read_txt_file()
        elif self.filename.endswith(".json"):
            data = self._read_json_file()
        elif self.filename.endswith(".bin"):
            data = self._read_bin_file()
        else:
            print(
                f"Неподдерживаемый формат файла '{self.filename}'. "
                f"Поддерживаются только .txt, .json и .bin."
            )
            return None
        if data is None or len(data) == 0:
            return None
        else:
            return self._build_email(data)
        
    def _read_bin_file(self) -> None | list[str]:
        try:
            with open(self.path, 'rb') as file:
                content = file.read()
                try:
                    text = content.decode('utf-8')
                except UnicodeDecodeError:
                    text = content.decode("cp1251")
                    
                return text.splitlines(keepends=True)
        # TODO: Добавить обработку других кодировок. Проверить работает ли
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
        
        
    def _read_txt_file(self) -> list[str] | None:
        try:
            with open(self.path, 'r') as file:
                return file.readlines()
                
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
            
    def _read_json_file(self) -> None | list[str] | dict:
        try:
            with open(self.path, 'r') as file:
                data = json.load(file)
            if isinstance(data, list):
                return data
            
            if isinstance(data, dict):
                lines = []
                if "From" in data:
                    lines.append(f"From: {data['From']}")
                elif "От кого" in data:
                    lines.append(f"От кого: {data['От кого']}")
                if "To" in data:
                    lines.append(f"To: {data['To']}")
                elif "Кому" in data:
                    lines.append(f"Кому: {data['Кому']}")
                if "Subject" in data:
                    lines.append(f"Subject: {data['Subject']}")
                elif "Тема" in data:
                    lines.append(f"Тема: {data['Тема']}")
                if "Date" in data:
                    lines.append(f"Date: {data['Date']}")
                elif "Дата" in data:
                    lines.append(f"Дата: {data['Дата']}")
                if "body" in data:
                    lines.append(data["body"])
                elif "text" in data: # Добавить аналоги на русском
                    lines.append(data["text"])

                return lines
            
            print(f"Некорректная структура JSON в файле '{self.filename}'.")
            return None
            # TODO: Проверить на наличие других полей, которые могут содержать тело письма
                
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
    
    def _build_email(self, lines: list[str]) -> Email:
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
                body += line
        return Email(
                        self._extract_address(sender),
                        self._extract_address(recipient),
                        theme,
                        date,
                        self.filename,
                        body
                    )
        # TODO: Добавить обработку других полей. Также расмотреть другие форматы файлов. 

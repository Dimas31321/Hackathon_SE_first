import re
from src.email import Email
from pathlib import Path
import json


class EmailReader:
    def __init__(self, filename: str):
        self.filename = filename # Filename следует вводить с раширением, например "email.txt"
        self.path = Path(filename)

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
    
    def _extract_address(self, address_str: str) -> str:
        if match := re.search(r'<(.*?)>', address_str):
            return match.group(1).strip()
        return address_str.strip()
        
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
            try:
                with open(self.path, 'r', encoding='utf-8') as file: # Проверить кодировку
                    return file.readlines()
            except UnicodeDecodeError:
                with open(self.path, 'r', encoding='cp1251') as file:
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
            try:
                with open(self.path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
            except UnicodeDecodeError:
                with open(self.path, 'r', encoding='cp1251') as file:
                    data = json.load(file)

            if isinstance(data, list):
                return data
            
            if isinstance(data, dict):
                lines = []

                if "From" in data:
                    lines.append(f"From: {data['From']}\n")
                elif "От кого" in data:
                    lines.append(f"От кого: {data['От кого']}\n")

                if "To" in data:
                    lines.append(f"To: {data['To']}\n")
                elif "Кому" in data:
                    lines.append(f"Кому: {data['Кому']}\n")

                if "Subject" in data:
                    lines.append(f"Subject: {data['Subject']}\n")
                elif "Тема" in data:
                    lines.append(f"Тема: {data['Тема']}\n")

                if "Date" in data:
                    lines.append(f"Date: {data['Date']}\n")
                elif "Дата" in data:
                    lines.append(f"Дата: {data['Дата']}\n")

                if "body" in data:
                    lines.append(data["body"])
                elif "text" in data: 
                    lines.append(data["text"])
                elif "Текст" in data:
                    lines.append(data["Текст"])
                elif "Сообщение" in data:
                    lines.append(data["Сообщение"])

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
        
        except json.JSONDecodeError:
            print(f"Некорректный JSON в файле '{self.filename}'.")
            return None
        
        except Exception as e:
            print(f"Произошла ошибка при чтении файла '{self.filename}': {e}.")
            return None
    
    def _build_email(self, lines: list[str]) -> Email:
        sender: str = ""
        recipient: str = ""
        theme: str = ""
        body: str = ""
        date: str = ""

        for line in lines:
            clean_line = line.strip()
            if clean_line.lower().startswith("from:") and not sender: 
                sender = self._extract_address(
                    clean_line[len("From:"):].strip()
                ) # Проверить 
                
            elif (clean_line.lower().startswith("от кого:") or clean_line.lower().startswith("ot kogo"))and not sender:
                sender = self._extract_address(
                    clean_line[len("От кого:"):].strip()
                )

            # Рассмотреть и добавить другие варианты
            elif clean_line.lower().startswith("to:") and not recipient:
                recipient = self._extract_address(
                    clean_line[len("To:"):].strip()
                )

            elif (clean_line.lower().startswith("кому:") or   clean_line.lower().startswith("komu:"))and not recipient:
                recipient = self._extract_address(
                    clean_line[len("Кому:"):].strip()
                )

            elif (clean_line.lower().startswith("subject:"))and not theme:
                theme = clean_line[len("Subject:"):].strip()

            elif (clean_line.lower().startswith("тема:") or clean_line.lower().startswith("tema:")) and not theme:
                # Рассмотреть и добавить другие вариант
                theme = clean_line[len("Тема:"):].strip()

            elif (clean_line.lower().startswith("date:")) and not date:
                date = clean_line[len("Date:"):].strip()

            elif (clean_line.lower().startswith("дата:") or clean_line.lower().startswith("data:")) and not date:
                date = clean_line[len("Дата:"):].strip()

            else:
                body += line

        sender = sender if len(sender) >0 else "Unknown"
        recipient = recipient if len(recipient) >0 else "Unknown"
        theme = theme if len(theme) >0 else "No theme"
        date = date if len(date) >0 else "Unknown"
        return Email(
            sender,
            recipient,
            theme,
            date,
            self.filename,
            body
        )
        # TODO: Добавить обработку других полей. Также рассмотреть другие форматы файлов.
from src.Email import Email
from pathlib import Path

class EmailReader:
    def __init__(self, filename: str):
        self.filename = filename
        self.path = Path(filename)
    def read_email(self) -> Email:
        with open(self.path) as file:
            lines = file.readlines()
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
            elif clean_line.startswith("От кого:"):
                sender = clean_line[8:].strip()
            # Рассмотреть и добавить другие варианты
            elif clean_line.startswith("To:"):
                recipient = clean_line[3:].strip() if len(clean_line) > 0 else None
            elif clean_line.startswith("Кому:"):
                recipient = clean_line[6:].strip() if len(clean_line) > 0 else None
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
            
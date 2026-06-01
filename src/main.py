import os #работа с файлами и папками
from email import Email #данные письма
from reader.email_reader import EmailReader #считывает письма с файлов
from file_manager.file_manager import Manager #раскладывает письма по папкам
import logging
Inbox = "inbox"
Types = "types"
Out = "out"
categories = {}
for filename in os.listdir(Types):
    category_name = filename[:-4]
    filepath = os.path.join(Types, filename)
    with open(filepath, "r", encoding="utf-8") as file:
        keywords = []
        for line in file:
            keyword = line.strip()
            if keyword:
                keywords.append(keyword)
        categories[category_name] = keywords
emails = []
failed_mails = []
for filename in os.listdir(Inbox):
    filepath = os.path.join(Inbox, filename)
    if not os.path.isfile(filepath):
        logging.warning(f"'{filepath}' является директорией, а не файлом. Пропускаем.")
        continue #проверка на всякий случай
    reader = EmailReader(filepath)
    email = reader.read_email()
    if email is None:
        logging.warning("ERROR: ошика чтения письма из файла " + filepath)
        pass
    else:
        logging.info(f"ACCEPT: from {email.sender}, theme: {email.theme}")
        emails.append(email)
for email in emails:
    general_text = email.theme + " " + email.body
    scores = {}
    for cat_name, words in categories.items():
        count = 0
        for word in words:
            if word in general_text:
                count+=1
        if count>0:
            scores[cat_name] = count
    if not scores:
        email.categories = ["Другое"]
    else:
        best_variant = max(scores, key=scores.get)


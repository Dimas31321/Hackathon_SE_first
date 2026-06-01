"""import os #работа с файлами и папками
from email import Email #данные письма
from reader import EmailReader #считывает письма с файлов
from src.file_manager.file_manager import Manager #раскладывает письма по папкам
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
        continue #проверка на всякий случай
    reader = EmailReader(filepath)
    email = reader.read_email()
    if email in None:
        logging.error("     ERROR: не удалось прочитать")
        pass
    else:
        print(f"    ACCEPT: from {email.sender}, theme: {email.theme}")
        emails.append(email)
for email in emails:
    print(f"Got letter: {email.filename} \n")
    general_text = email.theme + " " + email.body
    scores = {}
    for cat_name, words in categories.items():
        count = 0
        for word in words:
            if word in general_text:
                count+=1
        if count>0:
            scores[cat_name] = count
            #print(f"In category {cat_name} was found {count} words")
    if not scores:
        email.categories = ["Другое"]
    else:
        best_variant = max(scores, key=scores.get())
"""
import sys #работа с файлами и папками
from EmailClassifier.Rules.keywordrule import KeywordRule
from EmailClassifier.Rules.mailsenderrule import MailSenderRule
from EmailClassifier.classifier import Classifier
from reader.email_reader import EmailReader #считывает письма с файлов
from src.file_manager.file_manager import Manager #раскладывает письма по папкам
from pathlib import Path
from src.EmailClassifier.keywords import keywords
from src.EmailClassifier.keywords import senders
base = Path(__file__).parent
type_path = base / "types"
inbox_path = base / "inbox"
if type_path.exists() == False:
    print("ERROR: this type was not found")
    sys.exit(1)
if inbox_path.exists() == False:
    print("ERROR: this inbox does not exist")
    sys.exit(1)
keyrules = KeywordRule(keywords)
senderrules = MailSenderRule(senders)
classifire = Classifier(rules = [keyrules, senderrules])
classifire.min_value = 1
classifire.a = 1
email_list = list(inbox_path.glob("*.txt") + inbox_path.glob("*bin") + inbox_path.glob("*.json") + inbox_path.glob("*.jpeg"))
statistics = {}
for f_path in email_list:
    reader = EmailReader(str(f_path))
    email = reader.read_email()
    if email is None:
        print("ERROR: could not read the file")
        continue
    categories = classifire.classify(email)
    for cat in categories:
        email.add_category(cat)
    for cat in categories:
        if cat in statistics:
            statistics[cat] += 1
        else:
            statistics[cat] = 1
    Manager.put(email)
    print(f"DONE: {f_path.name} is in {categories}")
for cat, count in statistics.items():
    print(f"    Category {cat} got {count} files...")
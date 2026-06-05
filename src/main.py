# Lite version of main.py without embeddings
import sys #работа с файлами и папками
import os #работа с переменными окружения
from src.EmailClassifier.Rules.keywordrule import KeywordRule
from src.EmailClassifier.Rules.mailsenderrule import MailSenderRule
from src.EmailClassifier.classifier import Classifier
from src.reader.email_reader import EmailReader #считывает письма с файлов
from src.file_manager.file_manager import Manager #раскладывает письма по папкам
from pathlib import Path
from src.EmailClassifier.keywords import loadKeywords, loadSenders
import logging
logging.basicConfig(
    filename="./out/main.log",
    filemode= "w",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)
all_emails = []
base = Path(".")
type_path = base / "types"
inbox_path = base / "inbox"
if type_path.exists() == False:
    logging.error("ERROR: this type was not found")
    sys.exit(1)
if inbox_path.exists() == False:
    logging.error("ERROR: this inbox does not exist")
    sys.exit(1)
keyrules = KeywordRule(loadKeywords())
senderrules = MailSenderRule(loadSenders())
classifire = Classifier(rules = [keyrules, senderrules])
classifire.min_value = 1
classifire.a = 0.1
email_list =(
    list(inbox_path.glob("*.txt")) +
    list(inbox_path.glob("*.bin")) +
    list(inbox_path.glob("*.json")) +
    list(inbox_path.glob("*.jpeg"))
)
statistics = {}
for f_path in email_list:
    reader = EmailReader(str(f_path))
    email = reader.read_email()
    if email is None:
        logging.error("ERROR: could not read the file")
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
    all_emails.append(email)
    logging.info(f"DONE: {f_path.name} is in {categories}")
for cat, count in statistics.items():
    logging.info(f"Category {cat} got {count} files...")

Manager.remove_empty_dirs() # удаление пустых папок после сортировки

# Expanded version of main.py with embeddings

value = os.environ.get("NO_EXTENDED_VERSION")
if value == '0':
    from extended_src.query_sort import Query_sorter
    query_sorter = Query_sorter(all_emails)
    while True:
        message = input("Введите сообщение для классификации (exit для выхода): ").strip()
        if message.lower() == "exit" or message.lower() == "выход":
            break
        try:
            num = int(input("Введите число сообщений что вы хотите увидеть: "))
            if num <= 0:
                continue
        except:
            continue
        sorted_emails = query_sorter.query(message)
        print("Найдены следующие письма по теме запроса:")
        for email in sorted_emails[0:num]:
            print(email)
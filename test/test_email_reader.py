import pytest 
from src.email import Email
from src.reader.email_reader import EmailReader

TXT_FILE_1 = "inbox/mail_0001.txt"
TXT_FILE_2 = "inbox/mail_0002.txt"
JSON_FILE = "inbox/mail_0105.json"

def test_email_from_txt():
    email = EmailReader(TXT_FILE_1)
    email = email.read_email()
    assert email is not None
    assert email.sender == "s.volkov@partner.ru"
    assert email.theme == "браузер Chrome зависает при открытии"
    assert email.recipient == "Unknown"
    email = EmailReader(TXT_FILE_2)
    email = email.read_email()
    assert email is not None
    assert email.sender == "john.smith@globaltech.com"
    assert email.recipient == "it-support@company.ru"
    assert email.date == "03.04.2025 11:08"
    assert email.theme == "URGENT: Запрос от внешнего пользователя"
    assert email.body == "\nДобрый день.\n\nКлиент обращается повторно — заявка висит без ответа уже 3 дня. Прошу срочно разобраться.\n\nP.S. Это уже второй запрос по данной теме."

def test_email_from_json():
    email = EmailReader(JSON_FILE)
    email = email.read_email()
    assert email is None

def test_email_from_nonexistent_file():
    email = EmailReader("inbox/nonexistent_file.txt")
    email = email.read_email()
    assert email is None

def test_email_from_directory():
    email = EmailReader("inbox")
    email = email.read_email()
    assert email is None

def test_email_from_unreadable_file():
    email = EmailReader("inbox/unreadable_file.txt")
    email = email.read_email()
    assert email is None


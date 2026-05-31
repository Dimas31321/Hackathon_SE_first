from src.email import Email
import pytest

BODY_TEXT = (
    "\nДобрый день.\n\n"
    "Клиент обращается повторно — заявка висит без ответа уже 3 дня. "
    "Прошу срочно разобраться.\n\n"
    "P.S. Это уже второй запрос по данной теме."
)

def create_test_email():
    return Email(
        sender="uniqueguy@company.com",
        recipient="it-support@company.ru",
        theme="Не работает принтер",
        date="25.05.2025 05:55",
        filename="somemail.txt",
        body=BODY_TEXT
    )


def test_email_initialization():
    email = create_test_email()

    assert email.sender == "uniqueguy@company.com"
    assert email.recipient == "it-support@company.ru"
    assert email.date == "25.05.2025 05:55"
    assert email.theme == "Не работает принтер"
    assert email.filename == "somemail.txt"
    assert email.body == BODY_TEXT
    assert email.categories == []


def test_email_add_category():
    email = create_test_email()

    result = email.add_category("Urgent")

    assert result is True
    assert "Urgent" in email.categories


def test_email_add_duplicate_category():
    email = create_test_email()

    email.add_category("Urgent")
    result = email.add_category("Urgent")

    assert result is False
    assert email.categories.count("Urgent") == 1


def test_email_str():
    email = create_test_email()
    assert str(email) == (
        "From: uniqueguy@company.com\n"
        "To: it-support@company.ru\n"
        "Theme: Не работает принтер\n"
        "Filename: somemail.txt\n"
        f"Body: {BODY_TEXT}\n"
        "Categories: []\n"
        "Date: 25.05.2025 05:55"
    )
    
def test_categories_are_independent():
    email1 = create_test_email()
    email2 = create_test_email()

    email1.add_category("Urgent")

    assert email1.categories == ["Urgent"]
    assert email2.categories == []
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
        sender="s.volkov@partner.ru",
        recipient="it-support@company.ru",
        theme="URGENT: Запрос от внешнего пользователя",
        date="03.04.2025 11:08",
        filename="mail_0001.txt",
        body=BODY_TEXT
    )


def test_email_initialization():
    email = create_test_email()

    assert email.sender == "s.volkov@partner.ru"
    assert email.recipient == "it-support@company.ru"
    assert email.date == "03.04.2025 11:08"
    assert email.theme == "URGENT: Запрос от внешнего пользователя"
    assert email.filename == "mail_0001.txt"
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
        "From: s.volkov@partner.ru\n"
        "To: it-support@company.ru\n"
        "Theme: URGENT: Запрос от внешнего пользователя\n"
        "Filename: mail_0001.txt\n"
        f"Body: {BODY_TEXT}\n"
        "Categories: []\n"
        "Date: 03.04.2025 11:08"
    )
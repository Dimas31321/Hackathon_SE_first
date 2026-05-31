import pytest
from src.reader.email_reader import EmailReader


def test_email_from_txt_english_format(tmp_path):
    file = tmp_path / "test_mail_1.txt"
    file.write_text(
        "Subject: Продажа ручки\n"
        "From: marketingmanager@company.com\n"
        "To: sales@company.com\n"
        "\n"
        "Здравствуйте!\n"
        "\n"
        "Продайте мне эту ручку\n"
        "\n"
        "Спасибо.",
        encoding="utf-8"
    )
    email = EmailReader(str(file)).read_email()
    assert email is not None
    assert email.sender == "marketingmanager@company.com"
    assert email.theme == "Продажа ручки"
    assert email.recipient == "sales@company.com"
    assert "Продайте мне эту ручку" in email.body


def test_email_from_invalid_json(tmp_path):
    file = tmp_path / "mail.json"
    file.write_text('{"test": "value"}', encoding="utf-8")
    email = EmailReader(str(file)).read_email()
    assert email is None


def test_email_from_nonexistent_file(tmp_path):
    file = tmp_path / "nonexistent.txt"
    email = EmailReader(str(file)).read_email()
    assert email is None


def test_email_from_directory(tmp_path):
    email = EmailReader(str(tmp_path)).read_email()
    assert email is None


def test_email_from_empty_file(tmp_path):
    file = tmp_path / "empty.txt"
    file.write_text("", encoding="utf-8")
    email = EmailReader(str(file)).read_email()
    assert email is None

def test_email_from_valid_json(tmp_path):
    file = tmp_path / "mail.json"
    file.write_text(
        """
{
    "From": "marketingmanager@company.com",
    "To": "sales@company.com",
    "Subject": "Продажа ручки",
    "Date": "31.05.2026 12:00",
    "Body": "Здравствуйте!\\n\\nПродайте мне эту ручку\\n\\nСпасибо."
}
        """,
        encoding="utf-8"
    )
    email = EmailReader(str(file)).read_email()
    assert email is not None
    assert email.sender == "marketingmanager@company.com"
    assert email.recipient == "sales@company.com"
    assert email.theme == "Продажа ручки"
    assert email.date == "31.05.2026 12:00"
    assert "Продайте мне эту ручку" in email.body
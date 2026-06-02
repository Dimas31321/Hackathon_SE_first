import pytest

from src.EmailClassifier.Rules.mailsenderrule import MailSenderRule
from src.EmailClassifier.classifier import Classifier
from src.EmailClassifier.Rules.keywordrule import KeywordRule
from src.EmailClassifier.keywords import loadKeywords, loadSenders
from src.email import Email

def create_test_email_by_text(sender: str, body: str):
    return Email(
        sender=sender,
        recipient="it-support@company.ru",
        theme="Не работает принтер",
        date="25.05.2025 05:55",
        filename="somemail.txt",
        body=body
    )


def test_keyword_rule():
    text = """
    акция , скидка, """
    testEmail = create_test_email_by_text("uniqueguy@company.com", text)
    keywordTest = {"Спам" :["акция", "скидка"],
                   "Важное": ["важно", "срочно"]}

    keywordRule = KeywordRule(keywordTest)

    classifier = Classifier([keywordRule])

    assert classifier.classify(testEmail) == ["Спам"]

def test_mailsender_rule():
    text = """
    акция, скидка"""
    testEmail1 = create_test_email_by_text("uniqueguy@company.com", text)
    testEmail2 = create_test_email_by_text("megaguy@company.com", text)
    sendersTest = {"Спам" :["uniqueguy@company.com"],
                   "Важное": ["other@email.com"]}

    senderRule = MailSenderRule(sendersTest)
    classifire = Classifier([senderRule])

    assert classifire.classify(testEmail1) == ["Спам"]
    assert classifire.classify(testEmail2) == ["Другие"]

def test_keywordLoad():
    text = """
    акция, акция, """
    testEmail = create_test_email_by_text("uniqueguy@company.com", text)

    keywordRule = KeywordRule(loadKeywords())
    senderRule = MailSenderRule(loadSenders())

    classifier = Classifier([keywordRule, senderRule])

    assert classifier.classify(testEmail) == ["Спам"]

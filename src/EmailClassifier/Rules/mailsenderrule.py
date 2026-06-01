from src.EmailClassifier.Rules.rule import Rule
from src.email import Email

import logging

logger = logging.getLogger(__name__)


class MailSenderRule(Rule):
    def __init__(self, categories: dict) -> None:
        self.senders = dict() # адресс - категория

        for cat, value in categories.items():
            if isinstance(value, list):
                for name in value:
                    if name in self.senders:
                        logger.warning(f"Почтовый адрес {name} находится в >2 категориях.")
                        self.senders[name].append(cat)
                    else:
                        self.senders[name] = [cat]
            else:
                self.senders[value] = cat


    def score(self, email: Email) -> dict:
        scoring = dict()
        if email.sender in self.senders:
            for i in self.senders[email.sender]:
                scoring[i] = 99999

        return scoring

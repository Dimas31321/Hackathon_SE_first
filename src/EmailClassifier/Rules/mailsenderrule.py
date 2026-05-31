from src.EmailClassifier.Rules.rule import Rule
from src.email import Email


class MailSenderRule(Rule):
    def __init__(self, categories: dict) -> None:
        self.senders = dict() # адресс - категория

        for cat, value in categories.items():
            if isinstance(value, list):
                for name in value:
                    if name in self.senders:
                        raise ValueError("Почтовый адрес находится в >2 категориях.")
                    self.senders[name] = cat
            else:
                self.senders[value] = cat

        print(self.senders)

    def score(self, email: Email) -> dict:
        scoring = dict()
        if email.sender in self.senders:
            scoring[self.senders[email.sender]] = 99999
            return scoring
        return scoring

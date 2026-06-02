from src.EmailClassifier.Rules.rule import Rule

import logging

logger = logging.getLogger(__name__)

class KeywordRule(Rule):

    def __init__(self, categories: dict):
        self.keywords = categories
        self.list = list() #категории

        for cat in categories.keys():
            self.list.append(cat)



    def score(self, email):
        scoring = dict()

        text = email.body

        for cat in self.list:
            scoring[cat] = 0

        for cat in self.list:
            for word in self.keywords[cat]:
                scoring[cat] += text.count(word)

        return scoring

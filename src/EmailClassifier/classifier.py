from typing import List

from src.Email import Email
from src.EmailClassifier.Rules.rule import Rule


class Classifier:
    def __init__(self, rules: List[Rule]):
        self.rules = rules

    def classify(self, email: Email):
        finalScore = dict()

        for rule in self.rules:
            score = rule.score(email)

            for cat, value in score.items(): #пройтись по всем результатам и их суммировать
                if cat in finalScore:
                    finalScore[cat] += value
                else:
                    finalScore[cat] = value
        

        result = max(finalScore.items(), key= lambda x: x[1])

        if result[1] == 0:
            return "нераспределен"
        return result[0]
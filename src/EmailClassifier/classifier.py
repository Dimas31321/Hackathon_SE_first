from typing import List

from src.email import Email
from src.EmailClassifier.Rules.rule import Rule


class Classifier:
    def __init__(self, rules: List[Rule]):
        self.rules = rules
        self.min_value = 1 # минимальное совпадение для добавления
        self.a = 0 # некоторый коэффициент, для только максимальных ставить 1, для добавления всех 0

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
        
        results = []
        eps = 0.01
        for cat, value in finalScore.items():
            if value + eps >= self.a * result[1] and value >= self.min_value: 
                results.append(cat)

        if not len(results): 
            return ["Другие"]

        return results
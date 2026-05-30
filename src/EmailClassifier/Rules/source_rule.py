from src.EmailClassifier.Rules.rule import Rule

class KeywordRule(Rule):

    def __init__(self):
        self.trust_domains = [
            'local',
            'internal',
            'company.ru',
            'partner.ru'
        ]


    def score(self, email):
        text = email.body
        text = text.lower().replace(",", " ")
        text = text.replace(".", " ")
        text = text.replace("'", " ")
        text = text.replace('"', " ")
        text = text.split()

        for word in text:
            if word in self.keywords:
                for cat in self.keywords[word]:
                    self.scoring[cat] += self.scoretabel[word]

        
        return self.scoring
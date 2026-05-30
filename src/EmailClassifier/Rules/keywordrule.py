from src.EmailClassifier.Rules.rule import Rule
# входящие, отправленные, спам, важные, черновики

class KeywordRule(Rule):

    def __init__(self, categories: dict):
        self.keywords = dict() # привязка слова к категории
        self.scoring = dict() # словарь с результам

        for i in categories.keys():
            self.scoring[i] = 0

        for cat, words in categories.items():
            for i in words:
                if i in self.keywords:
                    self.keywords[i].append(cat)
                else:
                    self.keywords[i] = [cat]


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
                    self.scoring[cat] += 5

        
        return self.scoring
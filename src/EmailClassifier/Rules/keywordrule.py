from src.EmailClassifier.Rules.rule import Rule
# входящие, отправленные, спам, важные, черновики

class KeywordRule(Rule):

    def __init__(self, categories: dict):
        self.keywords = dict() # привязка слова к категории
        self.scoretabel = dict() ## слово - его вес
        self.list = list() #категории

        for cat in categories.keys:
            self.list.append(cat)

        for cat, words in categories.items():
            for item in words:
                if isinstance(item, tuple):    
                    i, value = item
                else:
                    i = item
                    value = 1
                self.scoretabel[i] = value
                if i in self.keywords:
                    self.keywords[i].append(cat)
                else:
                    self.keywords[i] = [cat]


    def score(self, email):
        scoring = dict()

        text = email.body
        text = text.lower().replace(",", " ")
        text = text.replace(".", " ")
        text = text.replace("'", " ")
        text = text.replace('"', " ")
        text = text.split()

        for cat in self.list:
            self.scoring[word] = 0

        for word in text:
            if word in self.keywords:
                for cat in self.keywords[word]:
                    scoring[cat] += self.scoretabel[word]

        return scoring
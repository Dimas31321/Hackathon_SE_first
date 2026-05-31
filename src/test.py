from src.Email import Email
from src.EmailClassifier.classifier import Classifier
from src.EmailClassifier.Rules.rule import Rule
from src.EmailClassifier.Rules.keywordrule import KeywordRule

keywords = {
    "спам": [("акция", 10), ("бесплатно", 10)],
    "важное": [("критическая", 10), ("внимание", 20), ("срочно", 50)]
}


text = """
Hi,

Направляем счёт и акт за оказанные услуги за март. Просьба передать в бухгалтерию для оплаты до конца недели.
Срочно, акция акция
Спасибо.
"""
a = Email("123", "1233", "123", "12121", "124", text)

b = KeywordRule(keywords)

c = Classifier([b])

print(c.classify(a))
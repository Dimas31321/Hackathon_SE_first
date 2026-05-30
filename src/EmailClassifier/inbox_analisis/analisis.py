from src.EmailClassifier.keywords import keywords

from src.EmailClassifier.classifier import Classifier

from src.EmailClassifier.Rules.keywordrule import KeywordRule

from src.reader.email_reader import EmailReader

import json

from pathlib import Path

list = [KeywordRule(keywords)]

classifier = Classifier(list)

folder_path = Path("inbox")

result = dict()

email_list = []

a = 0
for file_path in folder_path.iterdir():
    email = EmailReader(str(file_path)).read_email()
    if email == None:
        continue
    a += 1
    print(a)
    sender = email.sender
    if sender in result:
        sender_res = result[sender]
    else:
        sender_res = dict()
        result[sender] = sender_res

    for cat in classifier.classify(email):
        if cat not in sender_res:
            sender_res[cat] = 0
        sender_res[cat] += 1


json_res = Path("src") / "EmailClassifier" / 'inbox_analisis' / 'result.json'

json_data = json.dumps(result, indent=4, ensure_ascii=False)

json_res.write_text(json_data, encoding="utf-8")




        


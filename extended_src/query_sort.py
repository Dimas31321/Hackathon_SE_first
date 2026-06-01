import os
os.environ["HF_HUB_OFFLINE"] = "1"

from fastembed import TextEmbedding
import logging
from src.email import Email
from sklearn.metrics.pairwise import cosine_similarity 

logging.getLogger("fastembed").setLevel(logging.WARNING)

try:
    model = TextEmbedding(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
except:
    error_text = "Не удалось загрузить модель"
    logging.error(error_text)
    raise FileNotFoundError(error_text)

class Query_sorter:
    def __init__(self, emails:list[Email]):
        self.emails = emails
        email_texts = []

        for email in emails:
            email_texts.append(f"{email.theme}\n{email.body}")

        self.email_embeddings = list(model.embed(email_texts))

    def query(self, query:str) -> list[Email]:
        query_embedding = list(model.embed([query]))

        cos_similarities = cosine_similarity(query_embedding, self.email_embeddings).flatten()

        out = sorted(zip(cos_similarities, self.emails), key=lambda x: -x[0])
        return [email for cos, email in out]


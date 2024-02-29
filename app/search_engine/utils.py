from sentence_transformers import SentenceTransformer
import torch
from transformers import AutoModel, AutoTokenizer

# device = "cuda" if torch.cuda.is_available() else "cpu"
# model = SentenceTransformer("BAAI/bge-m3")



class SearchModel:
    def __init__(self, model_name="BAAI/bge-m3", is_sentence_transformers=True):
        self.is_sentence_transformers = is_sentence_transformers
        if is_sentence_transformers:
            self.model = SentenceTransformer(model_name)
        else:
            self.model = AutoModel.from_pretrained(model_name)
            self.tokenize = AutoTokenizer.from_pretrained(model_name)

    
    def tokenize(self, text):
        if self.is_sentence_transformers:
            if isinstance(text, list):
                return self.model.tokenize(text)['input_ids'].tolist()
            return self.model.tokenize([text])['input_ids'].tolist()[0]
        else:
            return self.tokenize(text)["input_ids"]
    
    def encode(self, texts):
        with torch.no_grad():
            if self.is_sentence_transformers:
                return self.model.encode(texts)
            else:
                return self.model(**self.tokenize(texts))["last_hidden_state"][:, 0, :].cpu().tolist()
    
    def __str__(self):
        return f"SearchModel({self.model_name}, {self.is_sentence_transformers})"
    
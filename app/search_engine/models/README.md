# Use model default bge-m3 otherwise you can download the model checkpoint and save in ./app/search_engine/models folder and change the model path.

sample code
```
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("BAAI/bge-m3")
```
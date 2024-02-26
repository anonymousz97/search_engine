import models.milvus_utils as milvus_utils
from pymilvus import (
    connections,
    utility,
    FieldSchema,
    CollectionSchema,
    DataType,
    Collection,
)

class MilvusModel:
    def __init__(self, user="", password="", host="localhost", port="19530", search_model=None):
        self.search_model = search_model
        self.connection = connections.connect("default", user=user, password=password, host=host, port=port)

    def ping(self):
        print(self.connection.is_connected())
        print("Connected")

    def insert(self, collection_name, data, max_chunk_size=1024, batch_size=16):
        # split chunks
        chunks = []
        for i in data:
            max_content_size = max_chunk_size - 5 - self.search_model.tokenize(i['full_title'])
            content = i['full_content']
            start = 0
            end = max_content_size
            while start < len(content):
                chunk = content[start:end]
                i['content'] = i['full_title'] + "\n\n" + chunk
                chunks.append(i)
                start = end - int(max_content_size * 0.1)
                end = start + max_content_size
                if end > len(content):
                    break

        # insert chunks by batch size
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i+batch_size]
            emb = self.search_model.encode(batch)
            batch_id = [milvus_utils.get_id() for x in batch]
            vectors = [
                batch_id,
                emb
            ]
            status = milvus_utils.insert_vectors(collection_name, vectors)
            print(status)

        return vectors
    

    
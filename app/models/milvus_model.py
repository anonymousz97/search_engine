import milvus_utils
from pymilvus import (
    connections,
    utility,
    FieldSchema,
    CollectionSchema,
    DataType,
    Collection,
)

class MilvusModel:
    def __init__(self, user, password, host, port, search_model):
        self.search_model = search_model
        self.connection = connections.connect("default", user=user, password=password, host=host, port=port)

    

    
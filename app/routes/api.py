from models.milvus_model import MilvusModel
from pymilvus import (
    connections
)


model = MilvusModel()
model.ping()

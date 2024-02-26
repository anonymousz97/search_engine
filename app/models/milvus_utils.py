from milvus import Milvus, IndexType, MetricType
from pymilvus import (
    connections,
    utility,
    FieldSchema,
    CollectionSchema,
    DataType,
    Collection,
)
import random

# # Connect to Milvus server
# milvus = Milvus(host='localhost', port='19530')

def create_collection_first_time(uuid, emb_size):
    fields = [
        FieldSchema(name="pk", dtype=DataType.INT64, is_primary=True, auto_id=False),
        FieldSchema(name="embeddings", dtype=DataType.FLOAT_VECTOR, dim=emb_size)
    ]
    schema = CollectionSchema(fields=fields, description=f"collection for uuid {uuid}")
    clt = Collection(name=uuid, schema=schema)

    # insert vector 0 sample points
    entities = [
        [0],  # field pk
        [[0] * emb_size],  # field embeddings
    ]
    insert_result = clt.insert(entities)
    clt.flush()  




# Insert vectors into a collection
def insert_vectors(connection, collection_name, vectors):
    status, ids = connection.insert(collection_name=collection_name, records=vectors)
    if status.OK():
        print(f"Vectors inserted successfully. IDs: {ids}")
    else:
        print(f"Failed to insert vectors: {status.message}")

# Search vectors in a collection
def search_vectors(connection, collection_name, query_vector, top_k):
    param = {
        'collection_name': collection_name,
        'query_records': [query_vector],
        'top_k': top_k,
        'params': {'nprobe': 16}
    }
    status, results = connection.search(**param)
    if status.OK():
        print(f"Search results: {results}")
    else:
        print(f"Failed to search vectors: {status.message}")

# Delete vectors from a collection
def delete_vectors(connection, collection_name, ids):
    status = connection.delete_entity_by_id(collection_name=collection_name, id_array=ids)
    if status.OK():
        print(f"Vectors deleted successfully")
    else:
        print(f"Failed to delete vectors: {status.message}")

# Drop a collection
def drop_collection(connection, collection_name):
    status = connection.drop_collection(collection_name=collection_name)
    if status.OK():
        print(f"Collection '{collection_name}' dropped successfully")
    else:
        print(f"Failed to drop collection: {status.message}")
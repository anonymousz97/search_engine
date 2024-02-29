import models.milvus_utils as milvus_utils
from pymilvus import (
    connections,
    utility,
    FieldSchema,
    CollectionSchema,
    DataType,
    Collection,
)
from copy import deepcopy
from search_engine import utils

class MilvusModel:
    def __init__(self, user="", password="", host="localhost", port="19530", search_model=None):
        self.search_model = search_model
        # self.connection = connections.connect("default", host=host, port=port)
        self.connection = connections.connect("default", user=user, password=password, host=host, port=port)

    def insert(self, collection_name, data, max_chunk_size=1024, batch_size=16):
        # split chunks
        chunks = []
        for i in data:
            max_content_size = max_chunk_size - 5 - len(self.search_model.tokenize(i['full_title']))
            content = i['full_content']
            start = 0
            end = max_content_size
            while start < len(content):
                tmp = deepcopy(i)
                chunk = content[start:end]
                tmp['content'] = tmp['full_title'] + "\n\n" + chunk
                chunks.append(tmp)
                start = end - int(max_content_size * 0.1)
                end = start + max_content_size
                if end > len(content):
                    break
        
        # mysql save information
        
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

        return 1


search_model = utils.SearchModel()
milvus = MilvusModel(host='localhost', port='19530', search_model=search_model)
# milvus.insert("test", [{"full_title": "test", "full_content": """Ông Trần Quí Thanh và 2 con gái bị truy tố với cáo buộc chiếm đoạt 1.040 tỷ đồng của 4 tổ chức, cá nhân thông qua hoạt động vay tiền nhưng ký hợp đồng là mua bán tài sản.
# Thông tin cho hay, VKSND tối cao vừa ban hành cáo trạng truy tố ông Trần Quí Thanh (71 tuổi, Giám đốc Công ty TNHH TM-DV Tân Hiệp Phát) cùng 2 con gái là Trần Uyên Phương (44 tuổi, Phó Giám đốc Công ty Tân Hiệp Phát) và Trần Ngọc Bích (40 tuổi) về tội “Lạm dụng tín nhiệm chiếm đoạt tài sản”, theo Khoản 4, Điều 175 Bộ luật Hình sự năm 2015. 

# Được biết, tháng 11/2023, Cơ quan CSĐT Bộ Công an có kết luận và khi tiếp nhận Viện KSND tối cao đã trả hồ sơ, yêu cầu điều tra bổ sung 5 nội dung. Các nội dung này chủ yếu xác định rõ lại giá trị tài sản bị cha con ông Trần Quí Thanh chiếm đoạt; đáng nói có nội dung bổ sung tình tiết giảm nhẹ trách nhiệm hình sự của từng bị can.

# Cuối tháng 1/2024, Cơ quan CSĐT Bộ Công an có kết luận điều tra bổ sung. Trong đó, cơ quan điều tra xác định, giá trị tài sản mà ông Trần Quí Thanh cùng 2 con gái chiếm đoạt của 4 bị hại là 1.040 tỷ đồng, còn kết luận điều tra lần đầu chỉ xác định là 767 tỷ đồng."""}, {"full_title": "test2", "full_content": "test2"}], max_chunk_size=256)
# milvus.ping()
milvus_utils.find_by_ids("test", ["666df145a6a72eaa192485c7d7a0e2c9"])

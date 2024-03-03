# search_engine
Search engine API 


### Docker 

Milvus
Run bash standalone_embed.sh

MySQL : 
docker run -d -p 3306:3306 --name mysql-docker-container -e MYSQL_ROOT_PASSWORD=linh -e MYSQL_DATABASE=default -e MYSQL_USER=minhbc4 -e MYSQL_PASSWORD=minhbc4 mysql/mysql-server:latest

ATTU : (tracking Milvus)
docker run -dit -p 8000:3000 -e MILVUS_URL=http://172.18.0.1:19530 zilliz/attu:v2.3.8

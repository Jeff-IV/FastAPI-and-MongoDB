from pymongo import MongoClient

# Base de datos local
#db_client = MongoClient("mongodb://localhost:27017/").local

# Base de datos remota
db_client = MongoClient("mongodb+srv://jefegarcia2003_db_user:IshqNLELSoddLcZI@cluster0.l2uepvd.mongodb.net/?appName=Cluster0").test


from pymongo import MongoClient

client = MongoClient("mongodb://mongo-service:27017/")
db = client["smartdoor"]
users_collection = db["users"]
logs_collection = db["access_logs"]
admins_collection = db["admins"]

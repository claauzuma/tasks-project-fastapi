from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://claauzuma:940250311@cluster0.7jf4lsj.mongodb.net/taskdatabase?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
database = client.taskdatabase
collection = database["todo_data"]

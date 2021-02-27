from db.mongodb_client import client
from bson.objectid import ObjectId

class MongoNewsDao:
    # 添加新闻记录
    def insert(self,title,content):
        try:
            client.vege.news.insert_one({"title":title,"content":content})
        except Exception as e:
            print(e)

    # 通过标题查找新闻主键值
    def search_id(self,title):
        try:
            news = client.vege.news.find_one({"title":title})
            return str(news["_id"])
        except Exception as e:
            print(e)

    # 修改新闻标题和内容
    def update(self,id,title,content):
        try:
            client.vege.news.update_one({"_id":ObjectId(id)},{"$set":{"title":title,"content":content}})
        except Exception as e:
            print(e)

    
    def search_content_by_id(self,id):
        try:
            news = client.vege.news.find_one({"_id":ObjectId(id)})
            return news["content"]
        except Exception as e:
            print(e)

    def delete_by_id(self,id):
        try:
            client.vege.news.delete_one({"_id":ObjectId(id)})
        except Exception as e:
            print(e)
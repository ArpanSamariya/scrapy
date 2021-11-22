import pymongo
from scrapy.exceptions import DropItem


class MongoDBPipeline(object):

    # Establishing Connection to MongoDB
    def __init__(self):
        connection = pymongo.MongoClient("mongodb+srv://arpan:Arpansam16@cluster0.0f1d0.mongodb.net/ArpanSamariya?retryWrites=true&w=majority")
        db = connection.ArpanSamariya
        self.collection = db.flipkart

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            self.collection.insert(dict(item))
        return item
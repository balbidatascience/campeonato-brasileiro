from pymongo import MongoClient


class Mongo():

    client = MongoClient('mongodb://localhost:27017/')

    def saveTweet(self, tweet):
        db = self.client.dbsocialsentiment
        id = db.tweets.insert_one(tweet).inserted_id
        # print(id)
        return True

    def listTweets(self):
        return self.client.dbsocialsentiment.tweets.find()

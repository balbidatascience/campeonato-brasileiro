from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import time
from pymongo import MongoClient
from SentimentAnalysis import SentimentAnalysis

# User credentials to access Twitter API
consumer_key = "BMLdHNoJGavqRxJUNvZ5fyjzf"
consumer_secret = "GTw2e7eNt0Q7airO0ck4MMkv8LZ21ky4TVK2oAkAyBZBi0UHpF"
access_token = "289365370-MJmm0ekadUH6gJfw48iarT9d9zAsUwsz1sf9m0uN"
access_token_secret = "XnWsRuIoMF8jqhxAFovIAJMCf3sHvpB3dE1WyUzThu2di"


class Mongo():

    client = MongoClient('mongodb://localhost:27017/')

    def saveTweet(self, tweet):

        db = self.client.dbsocialsentiment
        id = db.tweets.insert_one(tweet).inserted_id
        #print(id)
        return True


# Receive data stream
class Listener(StreamListener):

    #tweets = []
    mongo = Mongo()
    ml = SentimentAnalysis()

    def on_data(self, data):

        self.ml.TrainModel()
        tweet = json.loads(data)

        #print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
        #print(tweet)
        #print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')

        #self.tweets.append(tweet['text'])

        # Salva json no Mongo
        self.mongo.saveTweet(tweet)

        #print(self.ml.getSentimentAnalysis(tweet['text']))
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':

    while True:

        try:
            # Connect to Twitter Streaming API
            auth = OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)

            stream = Stream(auth, Listener())

            # Filter Twitter Streams by soccer teams
            stream.filter(track=['#BRA', '#ESP', '#ARG', '#GER', '#FRA', '#POR', '#ENG', '#BEL', '#URU'])

        except Exception as e:
            print(str(e))
            time.sleep(5)
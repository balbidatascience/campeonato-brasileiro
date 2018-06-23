from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import time
from pymongo import MongoClient
from SentimentAnalysis import SentimentAnalysis
from DataLake import Mongo

# User credentials to access Twitter API
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

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
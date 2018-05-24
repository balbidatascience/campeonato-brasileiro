from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json

# User credentials to access Twitter API
consumer_key = "BMLdHNoJGavqRxJUNvZ5fyjzf"
consumer_secret = "GTw2e7eNt0Q7airO0ck4MMkv8LZ21ky4TVK2oAkAyBZBi0UHpF"
access_token = "289365370-MJmm0ekadUH6gJfw48iarT9d9zAsUwsz1sf9m0uN"
access_token_secret = "XnWsRuIoMF8jqhxAFovIAJMCf3sHvpB3dE1WyUzThu2di"


# Receive data stream
class Listener(StreamListener):

    tweets = []

    def on_data(self, data):
        #print(data)
        tweet = json.loads(data)
        #self.tweets.append(tweet)
        print(tweet['text'])
        return True

    def on_error(self, status):
        print(status)



if __name__ == '__main__':

    try:
        # Connect to Twitter Streaming API
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        stream = Stream(auth, Listener())

        # Filter Twitter Streams by soccer teams
        stream.filter(track=['flamengo'])
    except Exception as e:
        print(str(e))

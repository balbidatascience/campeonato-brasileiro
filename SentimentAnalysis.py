import re
import pandas as pd
from textblob import TextBlob
from DataLake import Mongo


class SentimentAnalysis:

    df_tweet = pd.read_csv('data/Tweets_Mg.csv')
    tweets = df_tweet['Text'].values
    classes = df_tweet['Classificacao'].values

    analysis_return = []
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags=re.UNICODE)

    # Verify if is RT
    def isReTweet(self, tweet):
        if re.match(r'^RT.*', tweet):
            return True
        else:
            return False

    def cleanTweet(self, tweet):
        tweet = str(tweet).lower()

        # Remove URLS. (I stole this regex from the internet.)
        tweet = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', tweet)
        # remove emojis
        tweet = self.emoji_pattern.sub(r'', tweet)

        return tweet

    # Analize text tweet sentiment (polarity and subjectivity).
    def analyzeTweetSentiment(self, tweet):

        text_blod = TextBlob(tweet)
        sentences = text_blod.sentences
        sentences_sentiment = []
        sentence_sentiment = []
        tmp_sentiment = []

        # print('------------------------------------------------------------------')
        #print('Tweet Clear: {0}'.format(tweet))
        # print('\n')

        if text_blod.detect_language() != 'en':
            try:
                trad = TextBlob(str(text_blod.translate(to='en')))
                sentences_sentiment = trad.sentiment
            except Exception as e:
                print(e)
                sentences_sentiment = text_blod.sentiment
            # print('Sentimento Geral: {0}'.format(trad.sentiment))
        else:
            sentences_sentiment = text_blod.sentiment
            # print('Sentimento Geral: {0}'.format(text_blod.sentiment))

        # print('\n')

        # Analyze each sentence
        # for sentence in sentences:
#
        #     if sentence.detect_language() != 'en':
        #         traducao = TextBlob(str(sentence.translate(to='en')))
        #         tmp_sentiment.append((traducao.sentiment.polarity, traducao.sentiment.subjectivity))
        #         print('Frase: {0} - Sentimento: {1}'.format(traducao, traducao.sentiment))
        #     else:
        #         tmp_sentiment.append((sentence.sentiment.polarity, sentence.sentiment.subjectivity))
        #         print('Frase: {0} - Sentimento: {1}'.format(sentence, sentence.sentiment))
#
        # polarity = pd.DataFrame(tmp_sentiment, columns=['polarity', 'subjectivity'])
        # polarity = polarity[polarity['polarity'] != 0.0]

        # if polarity.empty:
        #     print('OK')
        # else:
        #     a = sum(polarity['polarity'].map(lambda x: float(x)))
        #     b = polarity['polarity'].count()
        #     media = a/b
        #     print('Soma: {0} e Qtde: {1} e Med: {2}'.format(a, b, media))

        return sentences_sentiment

    def listTweetResult(self):

        db = Mongo()
        tweets = db.listTweets()
        analysis_result = []

        for tweet in tweets:

            # tweet = json.loads(tweet)

            if tweet['truncated']:
                text = tweet['extended_tweet']['full_text']
            else:
                text = tweet['text']

            time_ms = tweet['timestamp_ms']

            # tweets['text'] = tweet['text']
            hashtags = pd.DataFrame(tweet['entities']['hashtags'])

            if hashtags.empty:
                tags = list()
            else:
                tags = hashtags.query('text == "BRA" or text == "ARG" or text == "ESP" or text == "GER" or '
                                      'text == "FRA" or text == "POR" or text == "ENG" or text == "BEL" or '
                                      'text == "URU" ')['text'].tolist()

            # Sentiment Analysis
            clean_text = self.cleanTweet(text)
            sent = self.analyzeTweetSentiment(clean_text)

            analysis_result.append((text, time_ms, tags, sent))

            print('Time: {0}'.format(time_ms))
            print('Tweet: {0}'.format(text))
            print('Sentimento: {0}'.format(sent.polarity))
            print('Hastags: {0}'.format(tags))

        return analysis_result


obj = SentimentAnalysis()
result = obj.listTweetResult()

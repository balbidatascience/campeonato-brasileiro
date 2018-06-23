import nltk
import re
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from sklearn.model_selection import cross_val_predict

#nltk.download('punkt')

from textblob import TextBlob


class SentimentAnalysis:
    df_tweet = pd.read_csv('data/Tweets_Mg.csv')

    tweets = df_tweet['Text'].values
    classes = df_tweet['Classificacao'].values

    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags=re.UNICODE)

    def TrainModel(self):
        vectorizer = CountVectorizer(analyzer="word")
        freq_tweets = vectorizer.fit_transform(self.tweets)
        modelo = MultinomialNB()
        modelo.fit(freq_tweets, self.classes)
        return vectorizer, modelo

    def TrainModel2(self):
        vectorizer2 = CountVectorizer(ngram_range=(1, 2))
        freq_tweets = vectorizer2.fit_transform(self.tweets)
        modelo2 = MultinomialNB()
        modelo2.fit(freq_tweets, self.classes)
        return vectorizer2, modelo2

    def Predict(self, tweet):
        vec, model = self.TrainModel()

        freq_testes = vec.transform(tweet)
        return {'tweet': tweet,
                'result': model.predict(freq_testes)}

    def Predict2(self, tweet):
        vec, model = self.TrainModel2()

        freq_testes = vec.transform(tweet)
        return {'tweet': tweet,
                'result': model.predict(freq_testes)}

    def ComparePredict(self, tweet):
        vec, model = self.TrainModel()
        vec2, model2 = self.TrainModel2()

        freq_testes = vec.transform(tweet)
        # freq_testes2 = vec2.transform(tweet)
        return {'tweet': tweet,
                'result': model.predict(freq_testes).values}

    def isReTweet(self, tweet):
        # Ignore retweets
        if re.match(r'^RT.*', tweet):
            return True
        else:
            return False

    def cleanTweet(self, tweet):
        tweet = tweet.lower()

        # Remove URLS. (I stole this regex from the internet.)
        tweet = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', tweet)

        tweet = re.sub(r'\bthats\b', 'that is', tweet)
        tweet = re.sub(r'\bive\b', 'i have', tweet)
        tweet = re.sub(r'\bim\b', 'i am', tweet)
        tweet = re.sub(r'\bya\b', 'yeah', tweet)
        tweet = re.sub(r'\bcant\b', 'can not', tweet)
        tweet = re.sub(r'\bwont\b', 'will not', tweet)
        tweet = re.sub(r'\bid\b', 'i would', tweet)
        tweet = re.sub(r'wtf', 'what the fuck', tweet)
        tweet = re.sub(r'\bwth\b', 'what the hell', tweet)
        tweet = re.sub(r'\br\b', 'are', tweet)
        tweet = re.sub(r'\bu\b', 'you', tweet)
        tweet = re.sub(r'\bk\b', 'OK', tweet)
        tweet = re.sub(r'\bsux\b', 'sucks', tweet)
        tweet = re.sub(r'\bno+\b', 'no', tweet)
        tweet = re.sub(r'\bcoo+\b', 'cool', tweet)

        # remove emojis
        tweet = self.emoji_pattern.sub(r'', tweet)

        return tweet

    # Utilizando o pacote TextBlob, mas foi necessário traduzir para o Inglês.
    def getSentimentAnalysis(self, tweet):

        # Verify if retweet
        # print(self.isReTweet(str(tweet)))

        text = self.cleanTweet(tweet)

        textBlod = TextBlob(text)
        frase = textBlod.sentences

        print('------------------------------------------------------------------')
        print('Antes: {0}'.format(tweet))
        print('Depoi: {0}'.format(text))
        if textBlod.detect_language() != 'en':
            trad = TextBlob(str(textBlod.translate(to='en')))
            print('Frase: {0} - Sentimento: {1}'.format(trad, trad.sentiment))
        else:
            print('Frase: {0} - Sentimento: {1}'.format(textBlod, textBlod.sentiment))

        print('\n')

        for sentence in frase:
            if sentence.detect_language() != 'en':
                traducao = TextBlob(str(sentence.translate(to='en')))
                print('Frase: {0} - Sentimento: {1}'.format(traducao, traducao.sentiment))
            else:
                print('Frase: {0} - Sentimento: {1}'.format(sentence, sentence.sentiment))

        print('------------------------------------------------------------------')

        #if frase.detect_language() != 'en':
        #    traducao = TextBlob(str(frase.translate(to='en')))
        #    print('Tweet: {0} - Sentimento: {1}'.format(tweet, traducao.sentiment))
        #else:
        #    print('Tweet: {0} - Sentimento: {1}'.format(tweet, frase.sentiment))

        return True


#obj = SentimentAnalysis()
#print(obj.cleanTweet('😂😂😂😬👀🙄👹😍😜😎 Gabriel é lindo'))

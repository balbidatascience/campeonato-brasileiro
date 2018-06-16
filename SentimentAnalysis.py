import nltk
import re
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from sklearn.model_selection import cross_val_predict

from textblob import TextBlob


class SentimentAnalysis:
    df_tweet = pd.read_csv('data/Tweets_Mg.csv')

    tweets = df_tweet['Text'].values
    classes = df_tweet['Classificacao'].values

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
        #freq_testes2 = vec2.transform(tweet)
        return {'tweet': tweet,
                'result': model.predict(freq_testes).values}

    # Utilizando o pacote TextBlob, mas foi necessário traduzir para o Inglês.
    def Predict3(self, tweet):
        frase = TextBlob(tweet)

        if frase.detect_language() != 'en':
            traducao = TextBlob(str(frase.translate(to='en')))
            print('Tweet: {0} - Sentimento: {1}'.format(tweet, traducao.sentiment))
        else:
            print('Tweet: {0} - Sentimento: {1}'.format(tweet, frase.sentiment))


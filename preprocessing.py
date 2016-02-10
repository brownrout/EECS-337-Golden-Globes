import json
import sys
import nltk

def getTweets(file):
    decoded_response = file.read()
    jsonData=json.loads(decoded_response)
    text = []
    for item in jsonData:
        name = item.get("text")
        text.append(name)

    tokenized_tweets = []

    for tweet in text:
        tokenized_tweets.append(nltk.wordpunct_tokenize(tweet))

#    print tokenized_tweets[0][0]

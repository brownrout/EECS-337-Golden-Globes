import json
import sys
import nltk
import string
from nltk.tokenize import RegexpTokenizer

tokenized_tweets = []
tokenized_tweets2 = []

official_tweets = []
official_tweets2 = []

def getTweets():

	twitterHandle = raw_input("Official Award Show Twitter Account (i.e. @goldenglobes): ")
	twitterHandleText = twitterHandle[1:]
	
	corpus = open('gg2013.json')
	corpus2 = open('gg2015.json')
	
	decoded_response = corpus.read()
	decoded_response2 = corpus2.read()

	jsonData=json.loads(decoded_response)
	jsonData2=json.loads(decoded_response2)
	
	text = []
	text2 = []

	for item in jsonData:
		name = item.get("text")
		text.append(name)

	for item in jsonData2:
		name = item.get("text")
		text2.append(name)

	tokenized_tweets = []
	tokenized_tweets2 = []

	tokenizer = RegexpTokenizer(r'\w+')

	for tweet in text:
		if twitterHandle in tweet and 'RT' not in tweet:
			temp_tweet = tokenizer.tokenize(tweet)
			if twitterHandleText == temp_tweet[0]:
			 	official_tweets.append(temp_tweet)
		tweet = tokenizer.tokenize(tweet)
		tokenized_tweets.append(tweet)

	for tweet in text2:
		if twitterHandle in tweet and 'RT' not in tweet:
			temp_tweet = tokenizer.tokenize(tweet)
			if twitterHandleText == temp_tweet[0]:
			 	official_tweets2.append(temp_tweet)
		tweet = tokenizer.tokenize(tweet)
		tokenized_tweets2.append(tweet)

	return tokenized_tweets, official_tweets, tokenized_tweets2, official_tweets2
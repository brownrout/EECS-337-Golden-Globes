EECS 337 Project 1

GROUP 4: Eric Brownrout, Sonia Nigam, Shraya Soundararajan, Richard Gates Porter

PROJECT DESCRIPTION:
Our project expands the five functions of the API in various ways: using stoplists, the functions themselves, and lists of key search words we looked to close in on the right information.  We leverage a global stoplist, in combination with analysis of consecutive capital words. We also make calls to the IMDbPY database as a substitute for a celebrity-specific name list. 
    
REQURIED FUNCTIONS
    - get_nominees
    - get_winner
    - get_hosts
    - get_presenters
    - get_awards
    - get_sentiment_analysis

BONUS FUNCTIONS:
    - best_dressed
    - worst_dressed.

EXTERNAL LIBRARIES: 
- nltk corpus: we imported English stopwords, a list of high frequency words, that could help us filter out unnecessary words from tweets.

- IMDbPY library: http://imdbpy.sourceforge.net/ which gave us access to the IMDb actor/actress database in order to cross check names.

REPOSITORIES
We were inspired to utilize emojis for sentiment analysis by this repo: https://github.com/rmacedo1/EECS337_GG2015




IMPORTANT NOTES:
GET_AWARDS_ALT: We implemented a more refined award function that removed duplicate awards by comparing two strings and measuring the similarities.  We leveraged a python library and was not sure if it violated the rules, so the less accurate version of get_awards is hooked up to the autograder.
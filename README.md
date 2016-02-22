EECS 337 Project 1

Group 4: Eric Brownrout, Sonia Nigam, Shraya Soundararajan, Richard Gates Porter

Project Description:

Our project expands the five functions of the API in various ways: using stoplists, the functions themselves, and lists of key search words we looked to close in on the right information.  We leverage a global stoplist, in combination with analysis of consecutive capital words. We also make calls to the IMDbPY database as a substitute for a celebrity-specific name list. 
    
Required Functions
    - get_nominees
    - get_winner
    - get_hosts
    - get_presenters
    - get_awards
    - get_sentiment_analysis

Bonus Functions
    - best_dressed
    - worst_dressed.

External Libraries: 

- NLTK CORPUS: we imported English stopwords, a list of high frequency words, that could help us filter out unnecessary words from tweets.

- IMDbPY LIBRARY: http://imdbpy.sourceforge.net/ which gave us access to the IMDb actor/actress database in order to cross check names.

Reposotories: 

We were inspired to utilize emojis for sentiment analysis by this repo: https://github.com/rmacedo1/EECS337_GG2015
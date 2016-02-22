import sys
import nltk
from preprocessing import *
from postprocessing import *
from nltk import sent_tokenize, word_tokenize, pos_tag, ne_chunk
from nameparser.parser import HumanName
from collections import Counter
from nltk.corpus import stopwords
from collections import OrderedDict
import re
from imdb import IMDb, IMDbError
from difflib import SequenceMatcher

tweets13 = []
officialTweets13 = []
tweets15 = []
officialTweets15 = []
punctTweets13 = []
punctTweets15 = []
stopwordsList = stopwords.words('english') + ['GoldenGlobes', 'Golden', 'Globes', 'Golden Globes', 'RT', 'VanityFair', 'golden', 'globes' '@', 'I', 'we', 'http', '://', '/', 'com', 'Best', 'best', 'Looking','Nice', 'Most', 'Pop', 'We', 'Love', 'Awkward','Piece', 'While', 'Boo', 'And' 'The', 'Gq', 'Hollywood', 'Watching', 'Hooray', 'That', 'Yeah', 'Can', 'What', 'NShowBiz', 'She', 'Mejor', 'Did', 'Vanity', 'Fair', 'Drama', 'MotionPicture', 'News', 'Take', 'Before', 'Director', 'Award', 'Movie Award', 'Music Award', 'Best Director', 'Best Actor', 'Best Actress', 'Oooh', 'Am', ]
OFFICIAL_AWARDS = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()
# http://stackoverflow.com/questions/17388213/python-string-similarity-with-probability

def get_human_names(text):
    i = IMDb()
    person_list = []
    tweet_names = []
    person_list = []
    #get potential names that are consecutive capital words
    print "get human names"
    for tweet in text:
        person_list += re.findall('([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)'," ".join(tweet))
    
    #remove
    print "first loop done"
    for word in person_list:
        if word not in stopwordsList:
            if word in tweet_names:
                print word
                tweet_names.append(word)
            elif i.search_person(word) != []:
                print word
                tweet_names.append(word)

    print "second loop done"

    return tweet_names


def get_human_names_faster(text):
    person_list = []
    tweet_names = []
    person_list = re.findall('([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)'," ".join(text))
    for word in person_list:
        if word not in stopwordsList:
            tweet_names.append(word)

    return tweet_names


def get_hosts(year):
    '''Hosts is a list of one or more strings. Do NOT change the name
        of this function or what it returns.'''

    if len(punctTweets13) == 0:
        post_ceremony()

    print "Getting hosts..."

    cnt = Counter()
    host_tweets = []
    hosts = []
    number = 0
    ignore = ["Hollywood", "Golden Globes"]
    
    if year == '2013':
        tweets = punctTweets13
    if year == '2015':
        tweets = punctTweets15

    for tweet in tweets:
        if 'host' in tweet:
            host_tweets.append(tweet)

    text = host_tweets[0:10]
    tweet_names = get_human_names(text)
    
    for t in tweet_names:
        if not any(w in t for w in ignore):
            cnt[t] += 1
            number +=1

    for w,v in cnt.most_common(2):
        key_final = w.encode("utf-8")
        hosts.append(key_final)
    
    print hosts
    return hosts

def get_awards(year):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''

    award_words = ['Best', 'best', 'Motion', 'motion', 'Picture', 'picture', 'Drama', 'drama', 'Performance', 'performance', 'Actress', 'actress', 'Actor', 'actor','Comedy', 'comedy', 'Musical', 'musical', 'Animated', 'animated', 'Feature', 'feature', 'Film', 'film', 'Foreign', 'foreign', 'Language', 'language', 'Supporting', 'supporting', 'Role', 'role', 'Director', 'director', 'Screenplay', 'screenplay', 'Original', 'orginal', 'Score', 'score', 'Song', 'song', 'Television', 'television', 'Series', 'series', 'Mini-series',  'mini-series', 'mini', 'Mini']
    helper_words = ['by','By','An','an','In','in','A','a','For','for','-',':','Or','or']
    
    officialTweets = []
    if year == '2013':
        officialTweets = officialTweets13
    if year == '2015':
        officialTweets = officialTweets15

    awards = []
    award_tweets = []
    for tweet in officialTweets:
        if len(set(award_words).intersection(set(tweet))) > 3:
            award_tweets.append(sorted(set(tweet), key=lambda x: tweet.index(x)))
    for tweet in award_tweets:
        first_index = len(tweet)-1
        for word in award_words:
            if word in tweet:
                index = tweet.index(word)
                if index < first_index:
                    first_index = index
        flag = True
        temp = []
        for word in tweet:
            if word not in award_words and word not in helper_words and tweet.index(word) >= first_index:
                flag = False
            if word in award_words or word in helper_words and tweet.index(word) >= first_index and flag:
                if word not in helper_words:
                    temp.append(word.lower())
        awardString = ' '.join(sorted(set(temp), key=lambda x: temp.index(x)))
        if awardString not in awards:
            awards.append(awardString)
    for x in awards:
        if x.split()[0] != 'best':
            awards.remove(x)

    awards = set(awards)

    print '\n'
    for x in awards:
        print x

    return awards

def get_awards_alt(year):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''

    award_words = ['Best', 'best', 'Motion', 'motion', 'Picture', 'picture', 'Drama', 'drama', 'Performance', 'performance', 'Actress', 'actress', 'Actor', 'actor','Comedy', 'comedy', 'Musical', 'musical', 'Animated', 'animated', 'Feature', 'feature', 'Film', 'film', 'Foreign', 'foreign', 'Language', 'language', 'Supporting', 'supporting', 'Role', 'role', 'Director', 'director', 'Screenplay', 'screenplay', 'Original', 'orginal', 'Score', 'score', 'Song', 'song', 'Television', 'television', 'Series', 'series', 'Mini-series',  'mini-series', 'mini', 'Mini']
    helper_words = ['by','By','An','an','In','in','A','a','For','for','-',':','Or','or']
    
    officialTweets = []
    if year == '2013':
        officialTweets = officialTweets13
    if year == '2015':
        officialTweets = officialTweets15
    awards = []
    award_tweets = []
    for tweet in officialTweets:
        if len(set(award_words).intersection(set(tweet))) > 3:
            award_tweets.append(sorted(set(tweet), key=lambda x: tweet.index(x)))
    for tweet in award_tweets:
        first_index = len(tweet)-1
        for word in award_words:
            if word in tweet:
                index = tweet.index(word)
                if index < first_index:
                    first_index = index
        flag = True
        temp = []
        for word in tweet:
            if word not in award_words and word not in helper_words and tweet.index(word) >= first_index:
                flag = False
            if word in award_words or word in helper_words and tweet.index(word) >= first_index and flag:
                if word not in helper_words:
                    temp.append(word.lower())
        awardString = ' '.join(sorted(set(temp), key=lambda x: temp.index(x)))
        if awardString not in awards:
            awards.append(awardString)
    for x in awards:
        if x.split()[0] != 'best':
            awards.remove(x)
    awards = set(awards)
    if year == '2015':
        awards = remove_similar(list(awards))
    print '\n'
    for x in awards:
        print x
    return awards

def remove_similar(awardList):
    removeAwards = []
    for i in range(0, len(awardList) - 1):
        for j in range(i, len(awardList)):
            x = awardList[i]
            y = awardList[j]
            if x != y:
                ratio = similar(x, y)
                #http://stackoverflow.com/questions/17388213/python-string-similarity-with-probability
                if ratio > .85:
                    # print x + " is similar to " + y
                    # print ratio
                    # print '\n'
                    if not ('actor' in x and 'actress' in y or 'actor' in y and 'actress' in x):
                        if not ('actor' in x and 'actor' not in y or 'actress' in x and 'actress' not in y):
                            removeAwards.append(x)
                            print ratio
                            print x
                            print y
                            print '\n'

    removeAwards = set(removeAwards)

    for x in removeAwards:
        if x in awardList:
            awardList.remove(x)

    return awardList

def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    # Your code here
    nominees = dict()
    nominees_tweets = []
    nominee_words = ['nominee', 'nominees', 'nominating', 'nominated', 'nominates', 'Nominee', 'Nominees', 'Nominating', 'Nominated', 'Nominates', 'should have won', 'Should have won']
    final_stopwords = ['Fair', 'Best', 'She', 'He', 'Hooray' 'Supporting', 'Actor', 'Actress', 'The', 'A', 'Life', 'Good', 'Not', 'Drinking', 'Eating', 'And', 'Hooray', 'Nshowbiz', 'TMZ', 'VanityFair', 'Mejor', 'Better', 'Score', 'Movie', 'Film', 'Song' 'Drama', 'Comedy', 'So', 'Better', 'Netflix', 'Someone', 'Mc', 'Newz', 'Season', 'Should']
    tweets = []
    winners = {'cecil b. demille award' : 'Jodie Foster', 'best motion picture - drama' : 'Argo', 'best performance by an actress in a motion picture - drama' : 'Jessica Chastain', 'best performance by an actor in a motion picture - drama' : 'Daniel Day-Lewis', 'best motion picture - comedy or musical' : 'Les Miserables', 'best performance by an actress in a motion picture - comedy or musical' : 'Jennifer Lawrence', 'best performance by an actor in a motion picture - comedy or musical' : 'Hugh Jackman', 'best animated feature film' : 'Brave', 'best foreign language film' : 'Amour', 'best performance by an actress in a supporting role in a motion picture' : 'Anne Hathaway', 'best performance by an actor in a supporting role in a motion picture' : 'Christoph Waltz', 'best director - motion picture' : 'Ben Affleck', 'best screenplay - motion picture' : 'Quentin Tarantino', 'best original score - motion picture' : 'Mychael Danna', 'best original song - motion picture' : 'Skyfall', 'best television series - drama' : 'Homeland', 'best performance by an actress in a television series - drama' : 'Claire Danes', 'best performance by an actor in a television series - drama' : 'Damian Lewis', 'best television series - comedy or musical' : 'Girls', 'best performance by an actress in a television series - comedy or musical':'Lena Dunham', 'best performance by an actor in a television series - comedy or musical':'Don Cheadle', 'best mini-series or motion picture made for television':'Game Change', 'best performance by an actress in a mini-series or motion picture made for television':'Julianne Moore', 'best performance by an actor in a mini-series or motion picture made for television':'Kevin Costner', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television': 'Maggie Smith', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television': 'Ed Harris'}
    
    for award in OFFICIAL_AWARDS:
        nominees[award] = []

    if year == '2013':
        tweets = punctTweets13
    if year == '2015':
        tweets = punctTweets15
    
    for tweet in tweets:
        if any(word in tweet for word in nominee_words):
            nominees_tweets.append(tweet)

    for w in nominees:
        print "award loop enter"
        award_tweets = []
        award_counter = Counter()
        
        temp_list = winners[w].split(' ')
        
        for tweet in nominees_tweets:
            for winner in temp_list:
                if winner in tweet:
                    award_tweets.append(tweet)

        tweet_names = get_human_names(award_tweets) #get human names per tweet
        
        print "fetched tweet_names"
        for t in tweet_names: #count each name
            print "vetting name"
            if t in winners[w] or t in final_stopwords or t in nominee_words:
                pass
            else:
                award_counter[t] += 1

        final_nominees = []
        for key,v in award_counter.most_common(5):
            key_final = key.encode("utf-8")
            final_nominees.append(key_final)
        
        nominees[w] = final_nominees

    print nominees
    return nominees


def get_winner(year):
    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    print "getting winners..."
    winners = dict()
    stopwordsList2 = stopwords.words('english')
    winner_words = ['win', 'wins', 'won','winner']
    award_list = []
    
    for award in OFFICIAL_AWARDS:
        winners[award] = []

    for award in OFFICIAL_AWARDS:
        award_list.append(award.split(' '))


    awards = []
    award_tweets = []
    award_tweets_clean = []

    #winningwords = ['win', 'Win', 'won', 'Won', 'winner', 'Winner', 'wins', 'Wins']
    award_words = ['Best', 'best', 'Motion', 'motion', 'Picture', 'picture', 'Drama', 'drama', 'Performance', 'performance', 'Actress', 'actress', 'Actor', 'actor','Comedy', 'comedy', 'Musical', 'musical', 'Animated', 'animated', 'Feature', 'feature', 'Film', 'film', 'Foreign', 'foreign', 'Language', 'language', 'Supporting', 'supporting', 'Role', 'role', 'Director', 'director', 'Screenplay', 'screenplay', 'Original', 'orginal', 'Score', 'score', 'Song', 'song', 'Television', 'television', 'Series', 'series', 'Miniseries',  'miniseries', 'mini', 'Mini']
    helper_words = ['by','By','An','an','In','in','A','a','For','for','-',':','Or','or', 'Made', 'made']
    
    #print award_list
    for word in helper_words:
        if word in award_list:
            award_list.remove(word)
    for word in stopwordsList2:
        if word in award_list:
            award_list.remove(word)

    if year == "2013":
        tweets = officialTweets13
    if year == "2015":
        tweets = officialTweets15

    #print officialTweets13

    for tweet in tweets:
        if "Best Screenplay" in tweet:
            award_tweets.append(tweet)
        if len(set(award_words).intersection(set(tweet))) >= 3:
            award_tweets.append(sorted(set(tweet), key=lambda x: tweet.index(x)))
    #print award_tweets
    

    for tweet in award_tweets:
        final_index = len(tweet)-1
        if tweet[final_index] == "GoldenGlobes":
            award_tweets_clean.append(tweet)
    print award_tweets_clean

    extra_words = ["GoldenGlobes", "Pixar"]

    index = 0
    last_index = 0
    for award in award_list:
        print award
        result = []
        all_potential_awards = dict()
        award_clean = award
        for word in stopwordsList2:
            if word in award_clean:
                award_clean.remove(word)
        for word in helper_words:   
            if word in award_clean:
                award_clean.remove(word)

        for tweet in award_tweets_clean:
            #print ' '.join(award_clean)
            #print ' '.join(tweet).lower()                 
            last_index = 0
            current_award = []
            temptweet = []
            counter = 0
            for word in helper_words:
                if word in tweet:
                    tweet.remove(word)
            for word in tweet:
                temptweet.append(word.lower())

            for word in award_words:
                if word in tweet:
                    index = tweet.index(word)
                    current_award.append(word)
                    if index > last_index:
                        last_index = index

            all_potential_awards[last_index] = tweet
        print all_potential_awards
        max_index = 0
        final_tweet = []
        max_counter = 0

        for i in all_potential_awards:
            #print all_potential_awards[i]
            itemp = []
            for word in all_potential_awards[i]:
                itemp.append(word.lower()) 
            counter = 0
            for word in award_clean:
                if word in itemp:
                    counter+=1
            #print counter
            if counter > max_counter:
                max_index = i
                final_tweet = all_potential_awards[i]
                max_counter = counter
        if 'Performance' in final_tweet or 'Actor' in final_tweet or 'Actress' in final_tweet or 'Director' in final_tweet or 'Song' in final_tweet:
            tweet_movies = final_tweet[(max_index+1):(max_index+3)]

        if 'Performance' not in final_tweet and 'Actor' not in final_tweet and 'Actress' not in final_tweet and 'Director' not in final_tweet and 'Song' not in final_tweet:
            for word in award_words:
                if word in final_tweet:
                    final_tweet.remove(word)
            for word in extra_words:
                if word in final_tweet:
                    final_tweet.remove(word)
            tweet_movies = get_human_names_faster(final_tweet)
            for word in tweet_movies:
                if "Pixar" in word:
                    tweet_movies.remove(word) 
        #print tweet_movies
        award_string = ' '.join(award)
        winners[award_string] = tweet_movies
        
        #print tweet[(last_index+1):(last_index+3)]
        #print last_index



    return winners

def get_presenters(year):
    '''Presenters is a dictionary with the hard coded award
        names as keys, and each entry a list of strings. Do NOT change the
        name of this function or what it returns.'''
    print "getting this year's presenters (this takes a bit longer)..."
    presenters = dict()
    presenters_tweets = []
    awards_keywords = dict()
    stopwordsList = stopwords.words('english')
    presenter_words = ['present', 'presents', 'presenting','presenter','presented' 'Present', 'Presenter', 'Presenting', 'Presented', 'Presents']
    final_stopwords = ['Fair', 'Best', 'She', 'He', 'Hooray' 'Supporting', 'Actor', 'Actress', 'The', 'A', 'Life', 'Good', 'Not', 'Drinking', 'Eating', 'And', 'Hooray', 'Nshowbiz', 'TMZ', 'VanityFair', 'Mejor', 'Better', 'Score', 'Movie', 'Film', 'Song' 'Drama', 'Comedy', 'So', 'Better', 'Netflix', 'Someone', 'Mc', 'Newz', 'Season', 'Should']
    tweets = []
    winners = {'cecil b. demille award' : 'Jodie Foster', 'best motion picture - drama' : 'Argo', 'best performance by an actress in a motion picture - drama' : 'Jessica Chastain', 'best performance by an actor in a motion picture - drama' : 'Daniel Day-Lewis', 'best motion picture - comedy or musical' : 'Les Miserables', 'best performance by an actress in a motion picture - comedy or musical' : 'Jennifer Lawrence', 'best performance by an actor in a motion picture - comedy or musical' : 'Hugh Jackman', 'best animated feature film' : 'Brave', 'best foreign language film' : 'Amour', 'best performance by an actress in a supporting role in a motion picture' : 'Anne Hathaway', 'best performance by an actor in a supporting role in a motion picture' : 'Christoph Waltz', 'best director - motion picture' : 'Ben Affleck', 'best screenplay - motion picture' : 'Quentin Tarantino', 'best original score - motion picture' : 'Mychael Danna', 'best original song - motion picture' : 'Skyfall', 'best television series - drama' : 'Homeland', 'best performance by an actress in a television series - drama' : 'Claire Danes', 'best performance by an actor in a television series - drama' : 'Damian Lewis', 'best television series - comedy or musical' : 'Girls', 'best performance by an actress in a television series - comedy or musical':'Lena Dunham', 'best performance by an actor in a television series - comedy or musical':'Don Cheadle', 'best mini-series or motion picture made for television':'Game Change', 'best performance by an actress in a mini-series or motion picture made for television':'Julianne Moore', 'best performance by an actor in a mini-series or motion picture made for television':'Kevin Costner', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television': 'Maggie Smith', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television': 'Ed Harris'}
    
    for award in OFFICIAL_AWARDS:
        presenters[award] = []
    
    if year == '2013':
        tweets = punctTweets13
    if year == '2015':
        tweets = punctTweets15

    for tweet in tweets:
        if any(word in tweet for word in presenter_words):
            presenters_tweets.append(tweet)

    for w in presenters:
        award_tweets = []
        award_counter = Counter()
        number = 0
        counter = 0
        temp_list = winners[w].split(' ')

        for tweet in presenters_tweets:
            for winner in temp_list:
                if winner in tweet:
                    award_tweets.append(tweet)

        tweet_names = get_human_names(award_tweets) #get human names per tweet

            
        for t in tweet_names: #count each name
            if t in winners[w] or t in final_stopwords or t in presenter_words:
                pass
            else:
                award_counter[t] += 1

        final_presenters = []
        for key,v in award_counter.most_common(2):
            key_final = key.encode("utf-8")
            final_presenters.append(key_final)

        presenters[w] = final_presenters
    print presenters
    return presenters


def get_host_sentiments(year):

    tweetCorpus = []
    if year == '2013':
        tweetCorpus = punctTweets13
    elif year == '2015':
        tweetCorpus = punctTweets15

    hosts_scores = {}
    for host in get_hosts(year):
        hosts_scores[host] = [0,0,0]

    for key in hosts_scores:
        for tweet in tweetCorpus:
            if key.split()[0] in tweet and key.split()[1] in tweet:
                for word in tweet:
                    if u'\U0001F600' in word or u'\U0001F601' in word or u'\U0001F603' in word:
                        hosts_scores[key][0] += 1
                    if u'\U0001F605' in word or u'\U0001F602' in word or u'\U0001F604' in word or u'\U0001F606' in word:
                        hosts_scores[key][1] += 1
                    if u'\U0001F612' in word or u'\U0001F621' in word or u'\U0001F615' in word:
                        hosts_scores[key][2] += 1
        print '\n' + key
        zero_div = False
        if hosts_scores[key][0] + hosts_scores[key][1] + hosts_scores[key][2] == 0:
            zero_div = True
        if not zero_div:  
            print "Positive: " + '{0:.0%}'.format(hosts_scores[key][0] / float(hosts_scores[key][0] + hosts_scores[key][1] + hosts_scores[key][2]))
            print "Negative: " + '{0:.0%}'.format(hosts_scores[key][2] / float(hosts_scores[key][0] + hosts_scores[key][1] + hosts_scores[key][2]))
            print "Funny:    " + '{0:.0%}'.format(hosts_scores[key][1] / float(hosts_scores[key][0] + hosts_scores[key][1] + hosts_scores[key][2]))
        else:
            print "Positive: 0%"
            print "Negative: 0%"
            print "Funny:    0%"

    return hosts_scores

def get_humor(year):
    '''humor is a list of one or more strings. Do NOT change the name
        of this function or what it returns.'''
    print "getting the two funniest people..."

    cnt = Counter()
    humor_tweets = []
    humor = []
    number = 0
    ignore = ["Hollywood", "Golden Globes", "The", "This"]
    humor_keywords = ["funny", "best joke", "hilarious", "hysterical", "best jokes", "haha"]
    
    if year == '2013':
        tweets = punctTweets13
    if year == '2015':
        tweets = punctTweets15
    
    for tweet in tweets:
        if any(w in tweet for w in humor_keywords):
            humor_tweets.append(tweet)

    for tweet in humor_tweets:
        tweet_names = get_human_names_faster(tweet)

        for t in tweet_names:
            if not any(w in t for w in ignore):
                if len(t.split()) != 2:
                    pass
                else:
                    cnt[t] += 1

    for w,v in cnt.most_common(2):
        key_final = w.encode("utf-8")
        humor.append(key_final)
    
    print humor
    return humor


def pre_ceremony():
    '''This function loads/fetches/processes any data your program
    will use, and stores that data in your DB or in a json, csv, or
    plain text file. It is the first thing the TA will run when grading.
    Do NOT change the name of this function or what it returns.'''
    print "Pre-ceremony processing complete.\n"
    print "Calling post-ceremony processing"
    post_ceremony()
    return

def post_ceremony():
    '''This loads information that is only available after the award ceremony -- i.e. the corpus'''
    print "loading up the corpuses..."
    global tweets13, punctTweets13, officialTweets13
    global tweets15, punctTweets15, officialTweets15
    tweets13, officialTweets13, punctTweets13, tweets15, officialTweets15, punctTweets15 = getTweets()
    print "post-ceremony processing complete."
    return

def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''

    while True:
        print '\n'
        year = raw_input("Which year: ")
        print "\nOptions:\n1. Get Hosts\n2. Get Awards\n3. Get Nominees\n4. Get Winners\n5. Get Presenters\n6. Get Host Sentiment\n7. Get Humor\n8. Get Awards (Alt)\n"
        user_input = input("Choose a function: ")
        if (user_input == 1):
            hosts = get_hosts(year)
        elif (user_input == 2):
            awards = get_awards(year)
        elif (user_input == 3):
            nominees = get_nominees(year)
        elif (user_input == 4):
            get_winner(year)
        elif (user_input == 5):
            presenters = get_presenters(year)
        elif (user_input == 6):
            sentiments = get_host_sentiments(year)
        elif (user_input == 7):
            humor = get_humor(year)
        elif (user_input == 8):
            alt_awards = get_awards_alt(year)
        else:
            print "Invalid choice\n"
    
    return

if __name__ == '__main__':
    pre_ceremony()
    main()

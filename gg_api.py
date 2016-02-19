import sys
import nltk
from preprocessing import *
from nltk import sent_tokenize, word_tokenize, pos_tag, ne_chunk
from nameparser.parser import HumanName
from collections import Counter

tweets = []
officialTweets = []

OFFICIAL_AWARDS = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']


def get_human_names(text):
    #print("called")
    pos = nltk.pos_tag(text)
    sentt = nltk.ne_chunk(pos, binary = False)
    person = []
    person_list = []
    name = ""
    for subtree in sentt.subtrees(filter=lambda t: t.label() == 'PERSON'):
        for leaf in subtree.leaves():
            person.append(leaf[0])
        if len(person) > 1:
            for part in person:
                name += part + ' '
            if name[:-1] not in person_list:
                person_list.append(name[:-1])
            name = ''
            person = []
    return person_list

def get_hosts(year):
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
    cnt = Counter()
    host_tweets = []
    hosts = []
    number = 0
    
    for tweet in tweets:
        if 'host' in tweet:
            #print("called")
            host_tweets.append(tweet)

    for tweet in host_tweets:
        tweet_names = get_human_names(tweet)
            # if number > 50: #THIS IS OUR PROBLEM, WHEN THERE ARE MORE TWEETS FOR SOME REASON THE THRESHOLD IS NOT BEING CALCULATED CORRECTLY, EVEN THOUGH THE COUNTER STILL WORKS
        if number > 10:
            break
        for t in tweet_names:
            cnt[t] += 1
            number +=1

    print cnt[max(cnt)]
    print cnt
    threshold = (cnt[max(cnt)]/2 * 1.5)
    print threshold

    for w,v in cnt.most_common(3):
        if v > threshold:
            hosts.append(w)

    print hosts
    return hosts

def get_awards(year):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    
    awards = []

    award_tweets = []
    #mini-series may give problems
    award_words = ['Best', 'best', 'Motion', 'motion', 'Picture', 'picture', 'Drama', 'drama', 'Performance', 'performance', 'Actress', 'actress', 'Actor', 'actor','Comedy', 'comedy', 'Musical', 'musical', 'Animated', 'animated', 'Feature', 'feature', 'Film', 'film', 'Foreign', 'foreign', 'Language', 'language', 'Supporting', 'supporting', 'Role', 'role', 'Director', 'director', 'Screenplay', 'screenplay', 'Original', 'orginal', 'Score', 'score', 'Song', 'song', 'Television', 'television', 'Series', 'series', 'Mini-series',  'mini-series']
    helper_words = ['by','By','An','an','In','in','A','a','For','for','-',':','Or','or']

    for tweet in officialTweets:
        if len(set(award_words).intersection(set(tweet))) > 2:
            award_tweets.append(sorted(set(tweet), key=lambda x: tweet.index(x)))

    for tweet in award_tweets:
        temp = []
        for word in tweet:
            # if word in award_words or word in helper_words:
            if word in award_words:
                temp.append(word.lower())
        awardString = ' '.join(sorted(set(temp), key=lambda x: temp.index(x)))
        if awardString not in awards:
            awards.append(awardString)

    for x in awards:
        if x.split()[0] != 'best':
            awards.remove(x)
        print x

    return awards

def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    # Your code here
    print "Unimplemented"
    return #nominees

def get_winners(year):
    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    print "Unimplemented"
    return #winners

def get_presenters(year):
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''
    
    presenters = dict()
    presenters_tweets = []
    cnt = Counter()
    presenters_keywords = dict()
    stopwordsList = stopwords.words('english')
    presenter_words = ['present', 'presents', 'presenting','presnter']
    
    for award in OFFICIAL_AWARDS:
        presenters[award] = []  #setting up output dictionary
    
    for award in OFFICIAL_AWARDS:
        award_list = award.split(' ') #convert into an iterable list
        award_values = []
        
        for word in award_list:
            if word not in stopwordsList: #extracting key words per award
                award_values.append(word)
        presenters_keywords[award] = award_values

    for tweet in tweets:
        if 'presents' in tweet or 'present' in tweet or 'presenting' in tweet or 'presenter' in tweet:
            print("called")
            presenters_tweets.append(tweet)

    for w in presenters:
        award_tweets = []
        award_counter = Counter()
        number = 0
        
        for tweet in presenters_tweets:
            counter = 0
            for word in presenters_keywords[w]: #checking to see how many key award words are in the tweet
                if word in tweet:
                    counter+= 1
            if counter > 2: #only check tweets with at least 3 key words
                award_tweets.append(tweet)

        print award_tweets
    
        for tweet in award_tweets:
            tweet_names = get_human_names(tweet) #get human names per tweet
            print tweet_names #here you can see how Julia Roberts is not being recognized
            if number > 50:
                break
            for t in tweet_names: #count each name
                cnt[t] += 1
                number +=1

        print cnt
        return

    # Your code here
    print "Unimplemented"
    return #presenters

def pre_ceremony():
    '''This function loads/fetches/processes any data your program
    will use, and stores that data in your DB or in a json, csv, or
    plain text file. It is the first thing the TA will run when grading.
    Do NOT change the name of this function or what it returns.'''
    user_input = raw_input("Which corpus to process: ")
    global tweets
    global officialTweets
    tweets, officialTweets = getTweets(user_input)
    print "Pre-ceremony processing complete.\n"
    return

def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    pre_ceremony()
    while True:
        print "\nOptions:\n1. Get Hosts\n2. Get Awards\n3. Get Nominees\n4. Get Winners\n5. Get Presenters\n"
        user_input = input("Choose a function: ")
        if (user_input == 1):
            hosts = get_hosts(2013)
        elif (user_input == 2):
            awards = get_awards(2013)
        elif (user_input == 3): {get_nominees(2013)}
        elif (user_input == 4): {get_winners(2013)}
        elif (user_input == 5): {get_presenters(2013)}
        else: print "invalid choice\n"
    
    return

if __name__ == '__main__':
    main()

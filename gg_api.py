import sys
import nltk
from preprocessing import *
from nltk import sent_tokenize, word_tokenize, pos_tag, ne_chunk
from nameparser.parser import HumanName
from collections import Counter
from nltk.corpus import stopwords
from alchemyapi import AlchemyAPI
from collections import OrderedDict

alchemyapi = AlchemyAPI()
tweets13 = []
officialTweets13 = []
tweets15 = []
officialTweets15 = []
punctTweets13 = []
punctTweets15 = []
stopwordsList = stopwords.words('english')

OFFICIAL_AWARDS = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']

def get_human_names_hosts(text):
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

#    for name in person_list:
#        last_first = HumanName(name).last + ', ' + HumanName(name).first
#        print last_first

    return person_list


def get_human_names_general(text):
    output = []
    tagged = nltk.pos_tag(text)
    namedEnt = nltk.ne_chunk(tagged, binary = True)
    # print namedEnt
    result = [' '.join([y[0] for y in x.leaves()]) for x in namedEnt.subtrees() if x.label() == "NE"]
    # print result
    for x in result:
        if len(x.split()) == 2:
            output.append(x)
    return output

def get_hosts(year):
    '''Hosts is a list of one or more strings. Do NOT change the name
        of this function or what it returns.'''
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
            #print("called")
            host_tweets.append(tweet)

    for tweet in host_tweets:
        tweet_names = get_human_names_hosts(tweet)
        if number > 10:
            break
        for t in tweet_names:
            if not any(w in t for w in ignore):
                cnt[t] += 1
                number +=1

#    print cnt[max(cnt)]
#    print cnt
#    threshold = (cnt[max(cnt)]/2 * 1.5)
#    print threshold
#
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
                temp.append(word.lower())
        awardString = ' '.join(sorted(set(temp), key=lambda x: temp.index(x)))
        if awardString not in awards:
            awards.append(awardString)
    for x in awards:
        if x.split()[0] != 'best':
            awards.remove(x)
    for x in awards:
        x = x.split()
    awards = set(awards)
    for x in awards:
        print x
    return awards

def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    # Your code here
    print "Unimplemented"
    return #nominees

def get_winner(year):
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
    awards_keywords = dict()
    stopwordsList = stopwords.words('english')
    presenter_words = ['present', 'presents', 'presenting','presenter','presented' 'Present', 'Presenter', 'Presenting', 'Presented', 'Presents']
    final_stoplist = ['GoldenGlobes', 'Golden Globes' 'RT', 'VanityFair']
    tweets = []
    
    winners = {'cecil b. demille award' : 'Jodie Foster', 'best motion picture - drama' : 'Argo', 'best performance by an actress in a motion picture - drama' : 'Jessica Chastain', 'best performance by an actor in a motion picture - drama' : 'Daniel Day-Lewis', 'best motion picture - comedy or musical' : 'Les Miserables', 'best performance by an actress in a motion picture - comedy or musical' : 'Jennifer Lawrence', 'best performance by an actor in a motion picture - comedy or musical' : 'Hugh Jackman', 'best animated feature film' : 'Brave', 'best foreign language film' : 'Amour', 'best performance by an actress in a supporting role in a motion picture' : 'Anne Hathaway', 'best performance by an actor in a supporting role in a motion picture' : 'Christoph Waltz', 'best director - motion picture' : 'Ben Affleck', 'best screenplay - motion picture' : 'Quentin Tarantino', 'best original score - motion picture' : 'Mychael Danna', 'best original song - motion picture' : 'Skyfall', 'best television series - drama' : 'Homeland', 'best performance by an actress in a television series - drama' : 'Claire Danes', 'best performance by an actor in a television series - drama' : 'Damian Lewis', 'best television series - comedy or musical' : 'Girls', 'best performance by an actress in a television series - comedy or musical':'Lena Dunham', 'best performance by an actor in a television series - comedy or musical':'Don Cheadle', 'best mini-series or motion picture made for television':'Game Change', 'best performance by an actress in a mini-series or motion picture made for television':'Julianne Moore', 'best performance by an actor in a mini-series or motion picture made for television':'Kevin Costner', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television': 'Maggie Smith', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television': 'Ed Harris'}
    
    
    for award in OFFICIAL_AWARDS:
        presenters[award] = []
    
    for award in OFFICIAL_AWARDS:
        award_list = award.split(' ')
        award_values = []
        
        for word in award_list:
            if word not in stopwordsList: #extracting key words per award
                award_values.append(word)
        awards_keywords[award] = award_values
    
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

        for tweet in award_tweets:
            tweet_names = get_human_names_general(tweet) #get human names per tweet
            for t in tweet_names: #count each name
                
                if t in winners[w] or t in final_stoplist:
                    pass
                else:
                    award_counter[t] += 1
        print award_counter

        final_presenters = []
        for key,v in award_counter.most_common(2):
            key_final = key.encode("utf-8")
            print key_final
            final_presenters.append(key_final)

        presenters[w] = final_presenters
        print presenters
            
    print presenters
    return presenters


def get_sentiment():
    #my code here
    return sentiments

def pre_ceremony():
    '''This function loads/fetches/processes any data your program
    will use, and stores that data in your DB or in a json, csv, or
    plain text file. It is the first thing the TA will run when grading.
    Do NOT change the name of this function or what it returns.'''
    global tweets13, punctTweets13, officialTweets13
    global tweets15, punctTweets15, officialTweets15
    
    tweets13, officialTweets13, punctTweets13, tweets15, officialTweets15, punctTweets15 = getTweets()
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
        print '\n'
        year = raw_input("Which year: ")
        print "\nOptions:\n1. Get Hosts\n2. Get Awards\n3. Get Nominees\n4. Get Winners\n5. Get Presenters\n"
        user_input = input("Choose a function: ")
        if (user_input == 1):
            hosts = get_hosts(year)
        elif (user_input == 2):
            awards = get_awards(year)
        elif (user_input == 3): {get_nominees(year)}
        elif (user_input == 4): {get_winners(year)}
        elif (user_input == 5): {get_presenters(year)}
        else:
            print "Invalid choice\n"
    
    return

if __name__ == '__main__':
    main()

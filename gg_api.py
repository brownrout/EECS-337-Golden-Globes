import sys
import nltk
from preprocessing import *
from nltk import sent_tokenize, word_tokenize, pos_tag, ne_chunk
from nameparser.parser import HumanName
from collections import Counter

tweets = []

OFFICIAL_AWARDS = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']


def get_human_names(text):
    print("called")
    pos = nltk.pos_tag(text)
    sentt = nltk.ne_chunk(pos, binary = False)
    person = []
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
    number = 0
    for tweet in tokenized_tweets:
        if number > 20:
            break
        if "host" in tweet:
            host_tweets.append(tweet)
            number=+1

    for tweet in host_tweets:
        tweet_names = get_human_names(tweet)
        for t in tweet_names:
            cnt[t] += 1

    print cnt


    
    
    # Your code here
    print "Unimplemented"
    return #hosts

def get_awards(year):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    print "Unimplemented"
    return #awards

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
    tweets = getTweets(user_input)
    print "Pre-ceremony processing complete.\n"
    return

def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    pre_ceremony()

    print person_list
    while True:
        print "\nOptions:\n1. Get Hosts\n2. Get Awards\n3. Get Nominees\n4. Get Winners\n5. Get Presenters\n"
        user_input = input("Choose a function: ")
        if (user_input == 1): {get_hosts(2013)}
        elif (user_input == 2): {get_awards(2013)}
        elif (user_input == 3): {get_nominees(2013)}
        elif (user_input == 4): {get_winners(2013)}
        elif (user_input == 5): {get_presenters(2013)}
        else: print "invalid choice\n"
    
    return

if __name__ == '__main__':
    main()

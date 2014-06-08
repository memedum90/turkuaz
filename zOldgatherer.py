'''
This code is written by Mehmet Durna  
Anyways, so Fede, what you'll find here is working. If you run the code, it will put tweets with keyword 
(defined in line 80)  into a file named keyword.txt. The function to read from these files are also available 
in the code(commented out). Everything works if twitter allows. Sometimes we are not allowed to retrieve the tweets by to_reply ID
if they're private tweets and the program ends. I will try to find a way for this. 
 Also there is a limit by Twitter, so try not to overuse it. 
350 requests in 1 hour. remember we have different request when we try to get a tweet by ID, 
so it may reach to limit faster than expected.

'''

import glob
import tweepy
import os
import json
import time
import sys
from random import randint

relevant2 = ["terrorist","muslim","islam","morsi","erdogan","gaymarriage","euthanasia","syria","abortion","feminism","gender","racism","jesus","religion","church","communism","massacre","holocaust"]
relevant=['islamist', 'terrorist', 'disagree', 'gaymarriage' ,'politics', 'racist', 'rape', 'communist', 'fascist', 'massacre' ,'holocaust' , 'feminist', 'mosque', 'erdogan' ,'morsi' ,'obama' ]
# Pick randomly one of the relevant argument
def pick():
    return relevant[randint(0,(len(relevant) - 1))] 

# Keys to initialize twitter API. DO NOT PLAY with this function
def init(): 
    consumer_key="ZBswvG6Iy6jcKUS7Y9TvhA"
    consumer_secret="0sbDaAJyXVRg8xwLu22HRuZG0IPGRZHtfH8zVw8Xpk"
    access_token="136962327-CMU75RcaKcZVh3cqxfVPP1MIkdVLVrxjLdfRAD4q"
    access_token_secret="s6UZaKV7In4ZpVvGV9tkDYkVhq2nU1uVp0hkHSy7f8gqq"
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api

def init_2():
    consumer_key="NY9AK7xur7y4vMs3nE54KA"
    consumer_secret="0obr9aNiGe27AjDzkatEeul4nDFUxKMSVcNtjZzf4"
    access_token="1914766603-p6PnLYcWgMprjq8V2t1Fh1s93FAgWRPyGpTylEH"
    access_token_secret="Zal2KPlizVaoQUzB1Bqx0t3uCmM1OXCl5J2o2at9MW0Aj"
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api

# function to take tweet object and turn it into a dict and return the resulting dict.
# rep is whether it was replied to someone or not. 1 means it was a reply, 0 means it wasn't
def obj2dict(tweet,rep,keyword):
    dictt={}
    dictt['rep']=rep
    dictt['id']=tweet.id
    dictt['text']=tweet.text
    #dictt['fvt_cnt']=tweet.favorite_count
    #dictt['rt_cnt']=tweet.retweet_count
    dictt['username']=tweet.user.screen_name
    dictt['user_id']= tweet.user.id_str
    dictt['reply_to']=tweet.in_reply_to_status_id
    dictt['topic']=keyword
    dictt['lang']=tweet.user.lang
    #dictt['flw_cnt']=tweet.user.followers_count
    #dictt['flg_cnt']=tweet.user.friends_count
    #dictt['lst_cnt']=tweet.user.listed_count
    #dictt['us_fvt_cnt']=tweet.user.favourites_count
    #dictt['stat_cnt']=tweet.user.statuses_count
    return dictt

# This function simply writes the dicts into files given the tweet list and the keyword to name the file
def write2file(tweets_list,keyword):
    if os.path.exists("archives/%s.txt" % keyword):
        f=open("archives/%s.txt" % keyword, 'a+')
    else:
        f=open("archives/%s.txt" % keyword, 'w')
    for tweet in tweets_list:
        f.write(unicode(tweet))
        f.write("\n")
    f.close()

# TODO 
def write2cvs(tweets_list,keyword):
    return 0

# This function can read the written dicts from the file into a list of dicts, dicts being tweets and 
# returns the tweet list.
# keyword is the name of the file
# if file is not in the directory, error message is printed and 0 is returned
def readfromfile(keyword):
    tweetlist=[]
    if os.path.exists("archives/%s.txt" % keyword):
        f=open("archives/%s.txt" % keyword, 'r')
        tweetstr=f.readline()
        while tweetstr:
            tweet=eval(tweetstr)
            tweetlist.append(tweet)
            tweetstr=f.readline()
        # Return tweet_list
        f.close()
        return tweetlist
    else: 
        print "File %s.txt is not in the current directory" % keyword
        return 0
# Variation
def readfromall():
    tweetlist=[]
    for filename in glob.glob(os.path.join('archives/','*.txt')):
        f=open(filename, 'r')
        tweetstr=f.readline()
        while tweetstr:
            tweet=eval(tweetstr)
            tweetlist.append(tweet)
            tweetstr=f.readline()
        # Return tweet_list
        f.close()
    return tweetlist
 
def isInDict(checkedTweet, tlist):
    if not tlist==0:
        for tweet_obj in tlist:
            #print 'tweet_obj id:\t%s' % tweet_obj['id']
            #print 'smp id:\t\t%s'% checkedTweet.id
            if tweet_obj['id']==checkedTweet.id:
                return True
        return False
    else:
        return False    

   
# GLOBAL VARIABLES

if 'init1' in sys.argv:


	api = init()
else:
	api=init_2()


# Search keyword
#keyword = 'terrorist'

#list to store all the tweets gathered
tweet_list=[]



def gatherer(keyword):
    tlistfromfile=readfromfile(keyword)
   
    # This line does the search, more parameters can be specified, count is the number of tweets gathered. max is 100
    tweets=api.search(q=keyword, count=100, lang='en')
    
    # The part to get tweets with their replied tweets and put them into the list making them dicts (from tweet objects)
    for tweet_obj in tweets:
    
        if not tweet_obj.in_reply_to_status_id ==None:
            to_reply_id=tweet_obj.in_reply_to_status_id
            reply=1
            #print 'text:' ,tweet_obj.text
            
            if not isInDict(tweet_obj, tlistfromfile):
                
                #tweet is dictionary of the object
                tweet=obj2dict(tweet_obj,reply, keyword)
                tweet_list.append(tweet)
            else:
                reply=0
            
            repcount=0 #this line is updated
            while reply==1:
                repcount+=1  #updated from here till ... 
                try: 
                    reply_tweet=api.get_status(to_reply_id)
                    if not reply_tweet.in_reply_to_status_id ==None:
                        to_reply_id=reply_tweet.in_reply_to_status_id
                        tweet=obj2dict(reply_tweet,reply,keyword)
                        tweet_list.append(tweet)
                    else:
                        reply=0
                        tweet=obj2dict(reply_tweet,reply,keyword)
                        tweet_list.append(tweet)
                   
                except:
                    print 'not authorized to see the replied tweet'
                    reply=0
                    if repcount==1:
                        tweet_list.pop()
                    elif repcount>1:
                        last_tweet=tweet_list.pop()
                        last_tweet['rep']=0
                        tweet_list.append(last_tweet)
           # ...here. copy till here         
    #write the tweets gathered into the relevant file, namely keyword.txt file
    write2file(tweet_list, keyword)
    #write to console  the list of tweets
    for tweet in tweet_list:
        print tweet


i=0
while i<15:
	i=i+1
	kelime=pick()
	print "searching  for the keyword '%s'"% kelime
	gatherer(kelime)
	print "Search is done for '%s'"% kelime
        

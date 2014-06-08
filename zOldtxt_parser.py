#gathererla topladigimiz tweetleri annotate etme toolu. flaming.txt , notrelevant.txt politedisagreemet.txt . burda maplere flaming field'i eklenmiyor.

import os
import glob
    
def readfromall():
    tweetlist=[]
    count=0
    for filename in glob.glob(os.path.join('archives/','*.txt')):
        print  "====================================\nNew file: %s"% filename
        f=open(filename, 'r')
        tweetstr=f.readline()
        while tweetstr:
            count+=1
            tweet=eval(tweetstr)
            tweetlist.append(tweet)
            tweetstr=f.readline()
        # Return tweet_list
        f.close()
    return [tweetlist,count]  
def isInDict(checkedTweet, tlist):
    if not tlist==0:
        for tweet_obj in tlist:
            #print 'tweet_obj id:\t%s' % tweet_obj['id']
            #print 'smp id:\t\t%s'% checkedTweet.id
            if tweet_obj['id']==checkedTweet['id']:
                return True
        return False
    else:
        return False    

def readfromfile():
    tweetlist=[]
    if os.path.exists("flaming.txt"):
        f=open("flaming.txt", 'r')
        tweetstr=f.readline()
        while tweetstr:
            tweet=eval(tweetstr)
            tweetlist.append(tweet)
            tweetstr=f.readline()
        # Return tweet_list
        f.close()
    if os.path.exists("notrelevant.txt"):
        f=open("notrelevant.txt", 'r')
        tweetstr=f.readline()
        while tweetstr:
            tweet=eval(tweetstr)
            tweetlist.append(tweet)
            tweetstr=f.readline()
        # Return tweet_list
        f.close()
    if os.path.exists("politedisagreement"):
        f=open("politedisagreement.txt", 'r')
        tweetstr=f.readline()
        while tweetstr:
            tweet=eval(tweetstr)
            tweetlist.append(tweet)
            tweetstr=f.readline()
        # Return tweet_list
        f.close()
     
    return tweetlist

#isFlaming=2 flaming
#isFlaming=1 politedisagreement
#isFlaming=0 notrelevant
def writetofile(tweet,isFlaming):
    if isFlaming==2:
        if os.path.exists("./flaming.txt"):
            f=open("flaming.txt", 'a+')
        else:
            f=open("flaming.txt", 'w')
    elif isFlaming==1:
        if os.path.exists("./politedisagreement.txt"):
            f=open("politedisagreement.txt", 'a+')
        else:
            f=open("politedisagreement.txt", 'w')
    elif isFlaming==0:
        if os.path.exists("./notrelevant.txt"):
            f=open("notrelevant.txt", 'a+')
        else:
            f=open("notrelevant.txt", 'w')
    else: 
        f=open("wtf.txt", 'w')
    f.write(unicode(tweet))
    f.write("\n")
    f.close()
    
#flaming when do verb
def display(tweets,count):
    tlistfromfile=readfromfile()
    lastt=1
    i=0 
    displist=[]
    
    for tweet in tweets:
        if not isInDict(tweet,tlistfromfile):
            displist.append(tweet)
           #tlistfromfile.append(tweet)
            if tweet['rep']==0:
                i+=1
                print "%d" %i
                print "%d/%d" % (100-((count-i)*100/count), 100)
                j=len(displist)-1
                while j >= 0:
               	    print displist[j]['username'],':',displist[j]['text']
                    j-=1
                for tw in displist:
                    print "Tweet to be annotated:\n%s" % tw['text']
                    select=raw_input ("if flaming press 1 or f, if polite disagrement press 3 or p, if not relevant press 5 or n")
                    if select=='f' or select=='1':
                        writetofile(tw, 2)
                    elif select=='3' or select=='p':
                        writetofile(tw, 1)
                    elif select=='5' or select=='n':
                        writetofile(tw, 0)
                    else:
                        writetofile(tw, 5)
                    j=len(displist)-1
                    tlistfromfile.append(tw)
                displist=[]
                   
[tweetlist,count]=readfromall()

''''f=open("input.txt",'w')
i=0
for tweet in tweetlist:
    i+=1
    if i>=1500:
        f.write(unicode(tweet))
        f.write('\n')
f.close()  '''      
display(tweetlist,count)

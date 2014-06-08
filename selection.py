import glob
import os



def readfromfile():
    tweetlist=[]
    count=0
    filename='./archieves/alldata.txt'
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


[tweetlist,count]=readfromfile()

def writetofile(tweet,isFlaming):
    if isFlaming==3:
        if os.path.exists("./archieves/flaming.txt"):
            f=open("./archieves/flaming.txt", 'a+')
        else:
            f=open("./archieves/flaming.txt", 'w')
    elif isFlaming==2:
        if os.path.exists("./archieves/polite.txt"):
            f=open("./archieves/polite.txt", 'a+')
        else:
            f=open("./archieves/polite.txt", 'w')
    elif isFlaming==1:
        if os.path.exists("./archieves/nonflam.txt"):
            f=open("./archieves/nonflam.txt", 'a+')
        else:
            f=open("./archieves/nonflam.txt", 'w')
    elif isFlaming==0:
        if os.path.exists("./archieves/general_anger.txt"):
            f=open("./archieves/general_anger.txt", 'a+')
        else:
            f=open("./archieves/general_anger.txt", 'w')  
    elif isFlaming==4:
        if os.path.exists("./archieves/notsure.txt"):
            f=open("./archieves/notsure.txt", 'a+')
        else:
            f=open("./archieves/notsure.txt", 'w')      
    else: 
        f=open("./archieves/wtf.txt", 'w')
    f.write(unicode(tweet))
    f.write("\n")
    f.close()
    
def display(tweets,count):
    c=1
    lst=raw_input ("last seen tweet")
    lst=int(lst)
    for tweet in tweets:
        if lst<=c:
            print "%d/%d: Tweet to be annotated:\n%s" %(c,count, tweet['text'])
            select=raw_input ("if flaming press  f or y, if polite disagrement p, if swearing or generalanger s, unsure u, if not flaming n")
            if select=='f' or select=='y':
                writetofile(tweet, 3)
            elif  select=='p':
                writetofile(tweet, 2)
            elif  select=='n':
                writetofile(tweet, 1)
            elif  select=='u':
                writetofile(tweet, 4)
            elif  select=='s':
                writetofile(tweet, 0)
            else:
                writetofile(tweet, 5)
        c=c+1           


#textlerden feature cikarilacak
#txt ayiklanacak
#nonflaming data gecilecek
#suan benimsedigim yaklasim tweet bazli flaming iceren tweeti tek basina tesbit eden featurelari cikarabilmek

# random olarak training ve test setlerini ayir 10da biri test, testler degisiyor. 10fold
# bag of words, feature olarak kelimeler


display(tweetlist,count)










# def isInDict(checkedTweet, tlist):
#     if not tlist==0:
#         for tweet_obj in tlist:
#             #print 'tweet_obj id:\t%s' % tweet_obj['id']
#             #print 'smp id:\t\t%s'% checkedTweet.id
#             if tweet_obj['id']==checkedTweet['id']:
#                 return True
#         return False
#     else:
#         return False   
#     
#     
# def readfromallfiles():
# 
#     tweetlist=[]
#     count=0
#     for filename in glob.glob(os.path.join('flaming*.txt')):
#         print  "====================================\nNew file: %s"% filename
#         f=open(filename, 'r')
#         tweetstr=f.readline()
#         while tweetstr:
#             count+=1
#             tweet=eval(tweetstr)
#             if not isInDict(tweet, tweetlist):
#                 tweetlist.append(tweet)
#             else:
#                 print "vardi: %s\n" % tweet['text']
#             tweetstr=f.readline()
#         # Return tweet_list
#         f.close()
#         
#     return [tweetlist,count]

# def ilksey():
#     [tweetlist,count]=readfromallfiles()
#     ff=open("flaming.txt", 'w')
#     for tweet in tweetlist:
#         ff.write(unicode(tweet))
#         ff.write('\n')
#     ff.close()
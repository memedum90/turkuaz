#annotate edilmis tek tweetleri flaming.txt dosyasindan cekip conversationlar haline getirip flamingcorpus.txt'ye yaziyor. 


import glob
import os

def readfromallfiles():
    flaminglist=[]
    poldislist=[]
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
        if os.path.exists("flaming.txt"):
            f=open("flaming.txt", 'r')
            tweetstr=f.readline()
            while tweetstr:
                tweet=eval(tweetstr)
                flaminglist.append(tweet)
                tweetstr=f.readline()
            
            f.close()
        if os.path.exists("politedisagreement.txt"):
            f=open("politedisagreement.txt", 'r')
            tweetstr=f.readline()
            while tweetstr:
                tweet=eval(tweetstr)
                poldislist.append(tweet)
                tweetstr=f.readline()
            
            f.close()
    return [flaminglist,poldislist,tweetlist,count]

[flaminglist,poldislist,tweetlist,count]=readfromallfiles()


ff=open("flamingcorpus.txt", 'w')
i=0
j=0
flame=0
pllen=len(poldislist)
fllen=len(flaminglist)
for tweet in tweetlist:
    
    #print "len poldis: %d, %d, len flaminglist:%d, %d" % (len(poldislist), j, len(flaminglist), i)
    if pllen>j and tweet['id']==poldislist[j]['id']:
        tweet['type']='poldis'
        if not flame==2:
        	flame=1
        j+=1
    
    elif fllen>i and tweet['id']==flaminglist[i]['id']:
        tweet['type']='flaming'
        flame=2
        i+=1
    
    else:
    	tweet['type']='notrelevant'
    	
    if tweet['rep']==0:
        tweet['contype']=flame
        flame=0
    
    ff.write(unicode(tweet))
    ff.write('\n')
         
         
ff.close()
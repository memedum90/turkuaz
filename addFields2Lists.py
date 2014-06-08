import os

tweetlist=[]

if os.path.exists("./archieves/flaming.txt"):
    f=open("./archieves/flaming.txt",'r')
    tweetstr=f.readline()
    
    while tweetstr:
        
        tweet=eval(tweetstr)
        tweet['type']='flaming'
        tweetlist.append(tweet)
        tweetstr=f.readline()
        
    
    f.close()    

f=open("./archieves/flaming.txt",'w')
for tweet in tweetlist:
    f.write(unicode(tweet))
    f.write('\n')
f.close()

tweetlist=[]    
if os.path.exists("./archieves/polite.txt"):
    f=open("./archieves/polite.txt", 'r')
    tweetstr=f.readline()
    
    while tweetstr:
        
        tweet=eval(tweetstr)
        tweet['type']='polite'
        tweetlist.append(tweet)
        tweetstr=f.readline()
        
    f.close()    


f=open("./archieves/polite.txt",'w')
for tweet in tweetlist:
    f.write(unicode(tweet))
    f.write('\n')
f.close()

tweetlist=[]
if os.path.exists("./archieves/nonflam.txt"):
    f=open("./archieves/nonflam.txt", 'r')
    tweetstr=f.readline()
    
    while tweetstr:
        
        tweet=eval(tweetstr)
        tweet['type']='notflaming'
        tweetlist.append(tweet)
        tweetstr=f.readline()
        
    
    f.close()    

f=open("./archieves/nonflam.txt",'w')
for tweet in tweetlist:
    f.write(unicode(tweet))
    f.write('\n')
f.close()


tweetlist=[]
if os.path.exists("./archieves/general_anger.txt"):
    f=open("./archieves/general_anger.txt", 'r')
    tweetstr=f.readline()
    
    while tweetstr:
        tweet=eval(tweetstr)
        tweet['type']='swearing'
        tweetlist.append(tweet)
        tweetstr=f.readline()
        
    f.close() 
f=open("./archieves/general_anger.txt",'w')
for tweet in tweetlist:
    f.write(unicode(tweet))
    f.write('\n')
f.close()


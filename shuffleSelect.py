import os
from random import shuffle
import sys
def readFiles(flmt,lmt):
    tweetlist=[]
    
    if os.path.exists("./archieves/flamingf.txt"):
        f=open("./archieves/flamingf.txt",'r')
        tweetstr=f.readline()
        cnt=1
        while tweetstr:
            
            tweet=eval(tweetstr)
            
            tweetlist.append(tweet)
            tweetstr=f.readline()
            if cnt>flmt:
                tweetstr=''
            cnt=cnt+1
        
        f.close()    
        
    if os.path.exists("./archieves/politef.txt"):
        f=open("./archieves/politef.txt", 'r')
        tweetstr=f.readline()
        cnt=1
        while tweetstr:
            
            tweet=eval(tweetstr)
            
            tweetlist.append(tweet)
            tweetstr=f.readline()
            if cnt>lmt:
                tweetstr=''
            cnt=cnt+1
        
        f.close()    
    if os.path.exists("./archieves/nonflamf.txt"):
        f=open("./archieves/nonflamf.txt", 'r')
        tweetstr=f.readline()
        cnt=1
        while tweetstr:
            
            tweet=eval(tweetstr)
           
            tweetlist.append(tweet)
            tweetstr=f.readline()
            if cnt>lmt:
                tweetstr=''
            cnt=cnt+1
        
        f.close()    
    
    if os.path.exists("./archieves/general_angerf.txt"):
        f=open("./archieves/general_angerf.txt", 'r')
        tweetstr=f.readline()
        cnt=1
        while tweetstr:
            tweet=eval(tweetstr)
            
            tweetlist.append(tweet)
            tweetstr=f.readline()
            if cnt>lmt:
                tweetstr=''
            cnt=cnt+1
        f.close() 
    return tweetlist 

def write2file(tweetlist,filename):
    f=open(filename, 'w')
    for tweet in tweetlist:
        f.write(unicode(tweet))
        f.write("\n")
    f.close()  
      
def shuffleSelect(flmt, lmt): 
    print 'selecting %d from flamingf.txt and %d from others\nwriting to mixdata.txt' %(flmt,lmt)
    tweetlist=readFiles(flmt,lmt)
    shuffle(tweetlist)
    print 'writing %d tweet into the file' % len(tweetlist)
    write2file(tweetlist,'./archieves/mixdata.txt')   
    
if len(sys.argv)>2:
        flmt=int(sys.argv[1])
        lmt=int(sys.argv[2])
shuffleSelect(flmt,lmt)       
#sentiment140.com
#Copyright Mehmet Durna ;)


import json
import requests

def generateJson(tweetlist):
    data={"data" : []}
    for tweet in tweetlist:
        data["data"].append({"text" : tweet })
    return json.dumps(data)


def sendRequest(dataj):
    host = "http://www.sentiment140.com/api/bulkClassifyJson?appid=mehmet.durna@boun.edu.tr"
    r = requests.post(host, data=dataj)
    
    return r


    
def makeDict(tweetlist):
    dict={}
    for tweet in tweetlist:
        
        dict[tweet['id']]= tweet    
    return dict

#takes a list, returns the same list with dicts full with sentiment values
def classifyTweets(tweetlist):
    tdict=makeDict(tweetlist)
    dataj=generateJson(tweetlist)
    print 'request has been prepared'
    r= sendRequest(dataj)
    print "request sent"
    js=r.json()
    jsonlist=js['data']
    tlist=[]
    for tweet in jsonlist:
        
        
        dic=tdict[tweet['text']['id']]
        dic['sentiment']=polarity2str(tweet['polarity'])
        tlist.append(dic)
    return tlist

import json

def polarity2str(polarity):
    if polarity==0:
        return "negative"
    elif polarity==2:
        return "neutral"
    elif polarity==4:
        return "positive"
    else:
        return 0
    
    
def classifyTweet(tweet):
    tlist=[]
    tlist.append(tweet)
    dataj=generateJson(tlist)
    print 'request has been prepared'
    r= sendRequest(dataj)
    
    print "request sent"
    print r.content
    js=json.loads(r.content)
    
    polarity=js['data'][0]['polarity']
    return polarity2str(polarity)





def readTweets(filename):
    tweetlist=[]
    
    
    f=open(filename, 'r')
    tweetstr=f.readline()
    count=0
    while tweetstr:
        count+=1
        tweet=eval(tweetstr)
        tweetlist.append(tweet)
        tweetstr=f.readline()
        # Return tweet_list
    f.close()
    return [count,tweetlist ] 
def write2file(tweetlist, filename):
    
    f=open(filename, 'w')
    for tweet in tweetlist:
        f.write(unicode(tweet))
        f.write("\n")
    f.close()
    
    
def main():
    file2read='./archieves/polite.txt'
    file2write='./archieves/polite.txt'
    
    [count,tweetlist]=readTweets(file2read)
    print "%d tweets gathered" % count
    
    #returns the same list with the sentiment field
    tlist=classifyTweets(tweetlist)
    
    #writes the list to the file
    write2file(tlist, file2write)
main()
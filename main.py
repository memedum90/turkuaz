# -*- coding: utf-8 -*-
from random import shuffle
import os

import sys,site
reload(sys)

sys.setdefaultencoding('utf-8')




#divides lists to n groups, 1 group for test and others for training.
#takes a tweetlist and a number to divide 
def group_n_fold(tweetlist, nfold):
    size=len(tweetlist)
    testsize=size/nfold
    i=0
    grouplist=[]
    j=0
    while i<nfold-1:
        
        grouplist.append([])
        l=0
        while l<testsize:
            grouplist[i].append(tweetlist[j])
            j+=1
            l+=1
          
        
        i=i+1
    l=0
    kalan=size-(testsize*(nfold-1))
    grouplist.append([])
    while l<kalan :
        grouplist[i].append(tweetlist[j])
        j+=1
        l+=1
    return grouplist

def readFile():
    tweetlist=[]
    print 'reading from mixdata.txt'
    f=open("./archieves/mixdata.txt",'r')
    tweetstr=f.readline()
    
    while tweetstr:
        
        tweet=eval(tweetstr)
        
        tweetlist.append(tweet)
        
        tweetstr=f.readline()
    
    f.close()
    print 'reading done with %d tweets' % len(tweetlist)
    return tweetlist  
def printSizes(tlist,glist):
    print "orj list size=%d" % len(tlist)
    total=0
    i=0
    for list in glist:
        size = len(list)
        total+=size
        print "list %d size=%d" % (i, size)
        i+=1
    print "total size=%d" % total 
def divideGroups(groups, groupnum,i):
    test=groups[i]
    train=[]
    j=0
    while j<groupnum:
        if not i==j:
            for tweet in groups[j]:
                train.append(tweet)
        j+=1
    return [train,test]
    
    
            
def processBaseline(groups,allgroups,baseline,allfeats):
    scores=[]
        
    
    groupnum=len(groups)
    i=0
    if allgroups==1:
        types=['polite', 'flaming', 'notflaming', 'swearing']
    else:
        types=['flaming' , 'notflaming']
    while i<groupnum:
        
        precision={}
        recall={}
        fscore={}
        total={}
        tp={}
        fp={}
        fn={}
        for typ in types:
            total[typ]=0
            tp[typ]=0
            fp[typ]=0
            fn[typ]=0
        [train,test]=divideGroups(groups,groupnum,i)
        if verbose==1 or verbose==2:
            print 'train:%d, test:%d' %(len(train), len(test))
        i+=1
        f=open('train.data', 'w')
        for tweet in train:
            if allgroups==1:
                f.write(tweet['type'])
            else:
                if tweet['type']=='flaming':
                    f.write('flaming')
                else:
                    f.write('notflaming')
                
            f.write(' ')
            if baseline==1:
                words=tweet['words']
                for word in words:
                    f.write(' %s' % unicode(word))
                f.write('\n')
            elif baseline==2:
                words=tweet['words']
                for word in words:
                    f.write(' %s' % unicode(word))
                    features=tweet['features']
                
                for feat in features:
                    for fs in allfeats:
                        if feat.startswith(fs):
                            f.write(' %s' % unicode(feat))
                f.write('\n')
            else:
                features=tweet['features']
                
                for feat in features:
                    for fs in allfeats:
                        if feat.startswith(fs):
                            f.write(' %s' % unicode(feat))
                f.write('\n')
        f.close()
        f=open('test.data', 'w')
        for tweet in test:
            if allgroups==1:
                f.write(tweet['type'])
            else:
                if tweet['type']=='flaming':
                    f.write('flaming')
                else:
                    f.write('notflaming')
                
            f.write(' ')
            if baseline==1:
                words=tweet['words']
                for word in words:
                    f.write(' %s' % unicode(word))
                f.write('\n')
            elif baseline==2:
                words=tweet['words']
                for word in words:
                    f.write(' %s' % unicode(word))
                    features=tweet['features']
                
                for feat in features:
                    for fs in allfeats:
                        if feat.startswith(fs):
                            f.write(' %s' % unicode(feat))
                f.write('\n')
            else:
                features=tweet['features']
                
                for feat in features:
                    for fs in allfeats:
                        if feat.startswith(fs):
                            f.write(' %s' % unicode(feat))
                f.write('\n')
                    
        f.close()
        command1="maxent train.data -i 100 -m model --gis > /dev/null 2> /dev/null"
        command2="maxent -p test.data -m model -oout --gis > /dev/null 2> /dev/null"
        os.system(command1)
        os.system(command2)
       
        f1=open('out')
        f2=open('test.data')
        lines=f1.readlines()
        texts=f2.readlines()
        f1.close()
        f2.close()
#         if os.path.exists("./out%d.data"%i):
#             out=open('out%d.data'%i,'a+')
#         else:
#             out=open('out%d.data'%i,'w')
            
        j=0
        
        for  line in lines:
            
            line= line.split()[0]
            #print line
            kel= texts[j].split()[0]
            total[kel]+=1
#             out.write("%s %s\n" % (line, kel))
            #kel gercek line prediction
            #print kel
            if line==kel:
                tp[line]+=1
            else:
                fp[line]+=1
                fn[kel]+=1
            j+=1
#         out.close()
        for typ in types:
            
            precision[typ]=tp[typ]/(tp[typ]+fp[typ]+0.00001)
            recall[typ]=tp[typ]/(tp[typ]+fn[typ]+0.00001)
            fscore[typ]=2.0*recall[typ]*precision[typ] /(recall[typ]+precision[typ]+0.00001) 
        tmp={}
        tmp['precision']=precision
        tmp['recall']=recall
        tmp['fscore']=fscore
        tmp['total']=total
        scores.append(tmp)
        
    return scores
 
 
 
n=int(sys.argv[1] )
verbose=0
allgroups=0
baseline=0
allfeats=['goodsmiley', 'badsmiley' , 'upper', 'question_marks', 'exclamation_marks', 'raw_vulgarity', 'vulgarity', 'you','disagreement', 'unpoliteness', 'sentiment']

if '-v' in sys.argv:
    verbose=1
if '-vv' in sys.argv:
    verbose=2
if '-all' in sys.argv:
    allgroups=1
if '-baseline' in sys.argv:
    baseline=1
    print 'program running for baseline'
if '-baseline2' in sys.argv:
    baseline=2
    print 'program running for baseline plus features'   
if '+feat' in sys.argv:
    
    ind=sys.argv.index('+feat' )
    allfeats=sys.argv[ind+1:]
    
if '-feat' in sys.argv:
    
    ind=sys.argv.index('-feat' )
    fets=sys.argv[ind+1:]
    for fet in fets:
        allfeats.remove(fet)
    
if not baseline==1:
    print "using following features %s"%allfeats
    
    
tweets=readFile()
groups=group_n_fold(tweets,n)
scores=processBaseline(groups,allgroups,baseline, allfeats)
i=0
fscoresum={}
prec={}
recal={}
if allgroups==1:
    types=['polite', 'flaming', 'notflaming', 'swearing']
else:
    types=['flaming' , 'notflaming']
while i<n:
    if verbose==2:
        print "run %d= %s\n"% (i,scores[i])
    if verbose==1:
        print "fscores for types: %s\n" % scores[i]['fscore']
    
    for typ in types:
        
       
        if typ in fscoresum.keys():
            fscoresum[typ]+=scores[i]['fscore'][typ]
            prec[typ]+=scores[i]['precision'][typ]
            recal[typ]+=scores[i]['recall'][typ]
        else:
            fscoresum[typ]=scores[i]['fscore'][typ]
            prec[typ]=scores[i]['precision'][typ]
            recal[typ]=scores[i]['recall'][typ]
    
    
    
    
    if verbose==1:
        print "total number of types: %s\n\n--------------------------\n\n" % scores[i]['total']
    
    i+=1

genel=0.0
for typ in types:
    fscoresum[typ]=fscoresum[typ]/n
    recal[typ]=recal[typ]/n
    prec[typ]=prec[typ]/n
    print "fscore %s=%f" %(typ,fscoresum[typ])
    genel+=fscoresum[typ]
genel=genel/len(types)
print "fscore average=%f" % genel
if '-o' in sys.argv:
    if os.path.exists("./archieves/results.txt"):
        f=open("./archieves/results.txt", 'a+')
    else:
        f=open("./archieves/results.txt", 'w')
    feats={}
    feats['nfold']=n
    feats['allgroups']=allgroups
    feats['baseline']=baseline
    if baseline==0:
        feats['feats_used']=allfeats
    else:
        feats['feats_used']=[]
    feats['precision']=prec
    feats['recall']=recal
    feats['fscore']=fscoresum
    feats['allscores']=scores
    f.write(unicode(feats))
    f.write('\n')
    
    
    
    f.close()


        
# cross validation 5*5 : farkli tweetler secerek tekrar run et. 
#en iyi sonuc hangi featurelarla aliniyor
#tek tek cikarildiginda sonuc nasil degisiyor
#unlem harf tekrari.... 



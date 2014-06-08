import os

def readFile():
    tweetlist=[]
    print 'Scorer running-----------------\nreading from results.txt'
    f=open('./archieves/results.txt','r')
    tweetstr=f.readline()
    
    while tweetstr:
        
        tweet=eval(tweetstr)
        
        tweetlist.append(tweet)
        
        tweetstr=f.readline()
    
    f.close()
    print 'reading done with %d runs' % len(tweetlist)
    return tweetlist  
def calc(lst):
    
    score={}
    keyss=lst.keys()
    for ky in keyss:
        if ky not in score.keys():
            score[ky]={}
        keys=lst[ky][0].keys()
        
        for key in keys:
            score[ky][key]=0.0
        i=0
        total=len(lst[ky])
        while i<total:
            for key in keys:
                score[ky][key]+=lst[ky][i][key]
            i+=1
        for key in keys:
            score[ky][key]=score[ky][key]/total
   
    
    return score
    
    
def calculateScore(scorelist):
    
    all1={}
    prec1={}
    recal1={}
    for score in scorelist:
        keys=all1.keys()
        if "%d&%d&%d&%s"%(score['nfold'], score['allgroups'], score['baseline'], score['feats_used']) not in keys:
            all1["%d&%d&%d&%s"%(score['nfold'], score['allgroups'], score['baseline'], score['feats_used'])]=[score['fscore']]
            prec1["%d&%d&%d&%s"%(score['nfold'], score['allgroups'], score['baseline'], score['feats_used'])]=[score['precision']]
            recal1["%d&%d&%d&%s"%(score['nfold'], score['allgroups'], score['baseline'], score['feats_used'])]=[score['recall']]
        else:
            all1["%d&%d&%d&%s"%(score['nfold'], score['allgroups'], score['baseline'], score['feats_used'])].append(score['fscore'])
            prec1["%d&%d&%d&%s"%(score['nfold'], score['allgroups'], score['baseline'], score['feats_used'])].append(score['precision'])
            recal1["%d&%d&%d&%s"%(score['nfold'], score['allgroups'], score['baseline'], score['feats_used'])].append(score['recall'])
    all=calc(all1)   
    prec=calc(prec1)
    recal=calc(recal1)
    keyys=all.keys()
    
    for ky in keyys:  
        if os.path.exists("./archieves/avgresults.txt"):
            out=open('./archieves/avgresults.txt','a+')
        else:
            out=open('./archieves/avgresults.txt','w')  
        keys=all[ky].keys()
        all[ky]['avg']=0
        prec[ky]['avg']=0
        recal[ky]['avg']=0
        how=ky.split('&')
        baseline=int(how[2])
        nfold=int(how[0])
        allgroups=int(how[1])
        feats=eval(how[3])
       
        i=0
        for key in keys:
            all[ky]['avg']+=all[ky][key]
            prec[ky]['avg']+=prec[ky][key]
            recal[ky]['avg']+=recal[ky][key]
            i+=1
        all[ky]['avg']/=i 
        prec[ky]['avg']/=i
        recal[ky]['avg']/=i   
        if baseline==1:
            out.write('baseline ')
        else:
            out.write('featured ')
        keys=all[ky].keys()    
        for key in keys:
            all[ky][key]= 2*prec[ky][key]*recal[ky][key]/(prec[ky][key]+recal[ky][key])
        out.write("%d-fold with %d allgroups:avg: %s precision:%s recall:%s " % (nfold, allgroups, all[ky], prec[ky], recal[ky]))
        if not baseline==1:
            out.write('feats_used:[')
            for feat in feats:
                out.write("%s "%feat)
            out.write('] \n')
        else:
            out.write('\n')
        out.close()
        if baseline==1:
            print "baseline %d-fold with %d allgroups: avg: %s precision:%s recall:%s\n" % (nfold, allgroups, all[ky], prec[ky], recal[ky])
        else:
            print "featured %d-fold with %d allgroups: avg: %s precision:%s recall:%s\n" % (nfold, allgroups, all[ky], prec[ky], recal[ky])
        
        
lst=readFile()
calculateScore(lst)        


# import os
# 
# def readFile():
#     tweetlist=[]
#     print 'Scorer running-----------------\nreading from results.txt'
#     f=open('./archieves/results.txt','r')
#     tweetstr=f.readline()
#     
#     while tweetstr:
#         
#         tweet=eval(tweetstr)
#         
#         tweetlist.append(tweet)
#         
#         tweetstr=f.readline()
#     
#     f.close()
#     print 'reading done with %d runs' % len(tweetlist)
#     return tweetlist  
# def calc(lst):
#     score={}
#     keys=lst[0].keys()
#     
#     for key in keys:
#         score[key]=0.0
#     i=0
#     total=len(lst)
#     while i<total:
#         for key in keys:
#             score[key]+=lst[i][key]
#         i+=1
#     for key in keys:
#         score[key]=score[key]/total
#    
#     
#     return score
#     
#     
# def calculateScore(scorelist):
#     besfold=[]
#     besfoldall=[]
#     onfold=[]
#     onfoldall=[]
#     
#     
#     for score in scorelist:
#         if score['nfold']==5 and score['allgroups']==1:
#             besfoldall.append(score['fscore'])
#         if score['nfold']==5 and score['allgroups']==0:
#             besfold.append(score['fscore'])
#         if score['nfold']==10 and score['allgroups']==1:
#             onfoldall.append(score['fscore'])
#         if score['nfold']==10 and score['allgroups']==0:
#             onfold.append(score['fscore'])
#     bfa=calc(besfoldall)
#     ofa=calc(onfoldall)
#     bf=calc(besfold)
#     of=calc(onfold)
#     
#     if os.path.exists("./archieves/avgresults.txt"):
#         out=open('./archieves/avgresults.txt','a+')
#     else:
#         out=open('./archieves/avgresults.txt','w')
#     keys=bf.keys()
#     bf['avg']=0
#     of['avg']=0
#     
#     for key in keys:
#         bf['avg']+=bf[key]
#         of['avg']+=of[key]
#     bf['avg']/=2
#     of['avg']/=2
#     keys=bfa.keys()
#     bfa['avg']=0
#     ofa['avg']=0
#     
#     for key in keys:
#         bfa['avg']+=bfa[key]
#         ofa['avg']+=ofa[key]
#     bfa['avg']/=4
#     ofa['avg']/=4
#     if score['baseline']==1:
#         out.write('baseline ')
#     else:
#         out.write('feats_used:[')
#         for feat in score['feats_used']:
#             out.write("%s "%feat)
#         out.write('] ')
#     out.write("five-fold with 2 groups: %s\n" % bf)
#     out.write("five-fold with 4 groups: %s\n" % bfa)
#     out.write("ten-fold with 2 groups: %s\n" % of)
#     out.write("ten-fold with 4 groups: %s\n" % ofa)
#     out.close()
#     print "five-fold with 2 groups: %s" % bf
#     print "five-fold with 4 groups: %s" % bfa
#     print "ten-fold with 2 groups: %s" % of
#     print "ten-fold with 4 groups: %s" % ofa
#     
#         
# lst=readFile()
# calculateScore(lst)        
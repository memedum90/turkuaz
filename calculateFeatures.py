# -*- coding: utf-8 -*-
import enchant
import nltk
from TT_prep import *
import re,sys

from TT_debate import *
from TT_politeness import *

reload(sys)

sys.setdefaultencoding('utf-8')

def readFile(filename):
    tweetlist=[]
    f=open(filename)
    tweetstr=f.readline()
    while tweetstr:
        tweet=eval(tweetstr)
        tweetlist.append(tweet)
        tweetstr=f.readline()
    f.close()
    return tweetlist  

# Function to count upper case letters in a string
def n_upper_chars(string):
    return sum(1 for c in string if c.isupper())

# Function to count question and exclamation/question marks in a string
def n_marks_question(string):
    return sum(1 for c in string if c in ('?'))

def n_marks_excl(string):
    return sum(1 for c in string if c in ('!'))

#Function to count good smileys in a string FIXME
def n_good_smile(string):
    return len(re.findall(r'([:=;B]-?(\)+|D+|\*+|[pP]+))|(\b[lL]+[oO]+[lL]+\b)|[😍♥😘😜😭😂]', string))

#Function to count bad smileys in a string
def n_bad_smile(string):
    return len(re.findall('(:|=)-?(\(+|\/)', string))

# Function to count the occurrences of vulgar words or insults (vulgar word + 2nd person in a little distance)
def process_vulgarity(list_of_words, Dic):
    total = 0
    for word in list_of_words:
        if Dic.check(word):
            total += 1
    return total
def you_cnt(words):
    cnt=0
    pronouns = ["you","your","you're","you'll","you've", "u", "yours" , "you'd"]
    for word in words:
        if word in pronouns:
            cnt+=1
    return cnt
    
def process_insults(list_of_words, Dic):
    pronouns = ["you","your","you're","you'll","you've", "u", "yours" , "you'd"]
    intr = [list_of_words.index(val) for val in pronouns if val in list_of_words]
    total = 0.3 * len(intr)
    for idx, word in enumerate(list_of_words):
        if Dic.check(word):
            total += 0.3
            for i in intr:
                if abs(idx-i) < 3: 
                    total += 5
    return total
Dict = enchant.DictWithPWL('en_US', 'dicts/bad-words.txt')
slg = mount_slang_dict()
pwl = enchant.request_pwl_dict('dicts/bad-words.txt')


def calculateFeatures(tweet):
    featlist=[]
     
    goodsmil = n_good_smile(tweet['text'])
    if goodsmil>0:
        featlist.append('goodsmiley')
    badsmil = n_bad_smile(tweet['text'])
    if badsmil>0:
        featlist.append('badsmiley')
    text = put_readable(tweet['text'].decode('utf-8'), slg)
    upper = n_upper_chars(text)
    if upper>0:
        featlist.append('upper:%d'% upper)
    ques = n_marks_question(text)
    if ques>0:
        featlist.append('question_marks:%d'% ques)
    excl=  n_marks_excl(text)
    if excl>0:
        featlist.append('exclamation_marks:%d'% excl)
        
    text = lower_punct(text)
    unigrams =  tweet['words']
    bigrams = nltk.bigrams(unigrams)
 
    text = " ".join(word for word in spell_correct(unigrams, Dict))
    
    rawvulgarity = process_vulgarity(unigrams, pwl)
    if rawvulgarity>0:
        featlist.append('raw_vulgarity:%d'% rawvulgarity)
    vulgarity = process_insults(unigrams, pwl)
    if vulgarity>0:
        featlist.append('vulgarity:%d'% vulgarity)
    youcount=you_cnt(unigrams)
    if youcount>0:
        featlist.append('you')
      
    unpoliteness = process_politeness(unigrams, bigrams)
    featlist.append('unpoliteness:%f'% unpoliteness)
    disagreement= process_vs(text)
    featlist.append('disagreement:%f'% disagreement)
    featlist.append('sentiment_%s'% tweet['sentiment'] )
    
    return featlist
def bagofwords(text):
    #pwl = enchant.request_pwl_dict('dicts/bad-words.txt')
    Dict = enchant.DictWithPWL('en_US', 'dicts/bad-words.txt')
    slg = mount_slang_dict()
    # Retrieve the original utf-8 codification on the text and eliminate hashtags and cite
    # Inside the function calls the slang translation before eliminating marks
    utftext = put_readable(text.decode('utf-8'), slg)
    # Remove useless punctuation and put everything in lower case
    utftext = lower_punct(utftext)
    
    words = utftext.split()
    #utftext = " ".join(word for word in spell_correct(words, Dict))
    #words2 = nltk.word_tokenize(utftext)
#     print words,'\n',words2
#     raw_input()
    #return [words,words2]
    return words
def write2file(filename):
    f=open(filename,'w')
    i=0
    for tweet in tweets:
        print i
        i+=1
        txt=tweet['text']
        tweet['words']=bagofwords(txt)
        tweet['features']= calculateFeatures(tweet)
        #[tweet['words'],tweet['words2']]=bagofwords(txt)
        
        f.write(unicode(tweet))
        f.write('\n')
    f.close()
    


sys.stdout.write("Gathering and formatting Disagreement lexicon... ")
fill_vs_lexicon()
sys.stdout.write("done!\n")   
# Mount the politeness corpus
sys.stdout.write("Gathering and formatting Stanford politeness corpus... ")
fill_politeness_corpus()
sys.stdout.write("done!\n")
 
tweets= readFile('./archieves/nonflam.txt')
write2file('./archieves/nonflamf.txt')

tweets= readFile('./archieves/general_anger.txt')
write2file('./archieves/general_angerf.txt')

tweets= readFile('./archieves/flaming.txt')
write2file('./archieves/flamingf.txt')

tweets= readFile('./archieves/polite.txt')
write2file('./archieves/politef.txt')


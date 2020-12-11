import os
import sys
import string
import numpy as np
import np_utils
import pandas as pd
import lyricsgenius as lg
import nltk
from nltk.corpus import stopwords  
import json
from collections import Counter
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

#Fixes the tokenization step, so words like "ain't", "gotta", etc get recognized as actual words
def mend_tokens(l):

    punctuation = ['?',")","(",",",".","?","!","`"]
    #splits = ["\'","na","n't","ta"]
    temp = l
    i = len(l)-1
    
    while(i>=0):
        temp[i] = temp[i].lower()
        if temp[i][0] == '\'' or temp[i] == "na" or temp[i] == "n't" or temp[i] == "ta":
            temp[i-1]+=temp[i]
            del temp[i]
        elif len(temp[i])==1:
            if temp[i] in punctuation:
                del temp[i]
        i-=1
    
    return temp

#removes stopwords from the list of tokens
def remove_stopwords(tokens):
    stop_words = set(stopwords.words('english'))
    filtered = [w for w in tokens if not w in stop_words]  
    return filtered
    #return tokens

#Returns the 10 most common n-grams (n=1,2,3,4)
def calcCommonNgrams(tokens):
    unigrams = Counter(nltk.ngrams(tokens,1))
    bigrams = Counter(nltk.ngrams(tokens,2))
    trigrams = Counter(nltk.ngrams(tokens,3))
    fourgrams = Counter(nltk.ngrams(tokens,4))

    print(unigrams.most_common(10))
    print("")
    print(len(bigrams))
    print(bigrams.most_common(11))
    print("")
    print(len(trigrams))
    print(trigrams.most_common(10))
    print("")
    print(fourgrams.most_common(10))

def getTopSentiments(lines,scores):
    compound_scores = [x['compound'] for x in scores]
    positives = list()
    negatives = list()
    #top10p = list()
    #top10n = list()

    for i in range(0,50):
        phrase = lines[np.argmax(compound_scores)]
        if phrase not in positives:
            positives.append(phrase)
        #print(str(i+1)+". "+lines[np.argmax(compound_scores)])
        del lines[np.argmax(compound_scores)]
        del compound_scores[np.argmax(compound_scores)]

    print("NEGATIVE SCORES")

    for j in range(0,50):
        phrase = lines[np.argmin(compound_scores)]
        if phrase not in negatives:
            negatives.append(phrase)
        #print(str(j+1)+". "+lines[np.argmin(compound_scores)])
        del lines[np.argmin(compound_scores)]
        del compound_scores[np.argmin(compound_scores)]
    
    print("POSITVE SCORES:")

    for i in range(0,10):
        print(str(i+1)+". "+positives[i])
    
    print("\nNEGATIVE SCORES")

    for j in range(0,10):
        print(str(j+1)+". "+negatives[j])
        
#main driver method
def main():
    
    files = [f for f in os.listdir("lyrics_json") if os.path.isfile(os.path.join("lyrics_json", f))]
    lyrics_list = list()
    pre_wordlist = list()
    
    for j in files:
        with open(r"lyrics_json/"+str(j)) as k:
            data = json.load(k)
            #print(data["lyrics"])
            entry = list()
            entry.append(str([j]))
            entry.append(data["lyrics"])
            lyrics_list.append(entry)
            pre_wordlist.append(data["lyrics"])
    
    tokens = nltk.word_tokenize("".join(pre_wordlist))
    mended_tokens = mend_tokens(tokens)
    clean_tokens = remove_stopwords(mended_tokens)
    print(len(clean_tokens))
    calcCommonNgrams(clean_tokens)

    lines_list = list()
    for song in pre_wordlist:
        sentences = song.split("\n")
        for line in sentences:
            lines_list.append(line)
    #print(lines_list)

    sent_test = pre_wordlist[1].split("\n")
    i = len(sent_test)-1
    while i>=0:
        if sent_test[i]=='':
            del sent_test[i]
        elif "\\" in sent_test[i]:
            sent_test[i].replace('\\','')
        i-=1
    #print(sent_test)
    sentiment_list = list()
    sia = SentimentIntensityAnalyzer()
    for s in lines_list:
        #print(s)
        vs = sia.polarity_scores(s)
        sentiment_list.append(vs)
        #print("{:-<65} {}".format(s, str(vs)))
        #print()

    getTopSentiments(lines_list,sentiment_list)
   
    
    
    
if __name__ == "__main__":
    main()
import os
import math
import sys
import pickle

def tokenize_test(line):
    splitLine = line.strip().split(" ")
    return splitLine

def classify_class(file, nbmodel):
    hamProb = nbmodel["HamClass"]["probHam"]
    spamProb = nbmodel["SpamClass"]["probSpam"]
    ham_smooth= nbmodel["HamClass"]["smoothScore"]
    spam_smooth= nbmodel["SpamClass"]["smoothScore"]
    hamScore = 0
    spamScore = 0
    splitFile = file.split("\n")
    for eachLine in splitFile:
        line = eachLine.strip()
        splitTokens = tokenize_test(line)
        for token in splitTokens:
            token=token.lower()
            if token.strip() not in ham_smooth and token.strip() not in spam_smooth:
                continue
            hamScore=hamScore+math.log10(ham_smooth[token.strip()])
            spamScore=spamScore+math.log10(spam_smooth[token.strip()])
        hamScore=hamScore+math.log10(hamProb)
        spamScore = spamScore+math.log10(spamProb)
    if hamScore>spamScore:
        return "pos"
    else:
        return "neg"

def classify(inputDict):
    analysedSentimentDict = {}
    model={}
    with open("/Users/louis/Documents/CSCI_544/BSLVChatbot/nbmodel.txt","rb") as handle:
        model=pickle.load(handle)
    for key,value in inputDict.items():
        posCount = 0
        negCount = 0
        for item in value:
            result = classify_class(item, model)
            if result == "pos":
                posCount+=1
            elif result == "neg":
                negCount+=1
        posProb = int((posCount/len(value))*100)
        negProb = int((negCount/len(value))*100)
        analysedSentimentDict[key] = str(posProb)+ "% Positive and "+str(negProb)+"% Negative"

    return analysedSentimentDict
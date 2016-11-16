import os
import math
import sys
from nbCalculation import nbCalculate
import pickle

def tokenize_test(line):
    splitLine = line.strip().split(" ")
    return splitLine

def clssify_class(file,nbmodel):
    inputFileHandler = open(file, "r",encoding="UTF-8")
    hamProb = nbmodel["HamClass"]["probHam"]
    spamProb = nbmodel["SpamClass"]["probSpam"]
    ham_smooth= nbmodel["HamClass"]["smoothScore"]
    spam_smooth= nbmodel["SpamClass"]["smoothScore"]
    hamScore = 0
    spamScore = 0
    for eachLine in inputFileHandler:
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
    #print(hamScore,spamScore)
    if hamScore>spamScore:
        return "pos"
    else:
        return "neg"

def main():
    model={}
#    path = "E:\USCSUb\NLP\Assign1\dev"
    args = sys.argv
    path = args[1]
    #readFileHandler = open("", "r")
    with open("nbmodel.txt","rb") as handle:
        model=pickle.load(handle)
    #model = eval(readFileHandler.read())
    hamCount = 0
    spamCount = 0
    correct_spam=0
    correct_ham=0
    hamfiles=0
    spamfiles=0
    writeHandler = open("nboutput.txt", "w")
    for root, dirs, files in os.walk(path):
        for name in files:
            if name.endswith((".txt")):
                if "pos" in name:
                     hamfiles+=1
                if "neg" in name:
                    spamfiles+=1
                result = clssify_class(root+'/'+name,model)
                if result == "pos":
                    if "pos" in name:
                        correct_ham+=1
                    hamCount+=1
                    '''fullpath=os.path.join(root,name)
                    towrite = result+" "+ root+'/'+name+"\n"
                    towrite = towrite.replace("\\", "/")
                    writeHandler.write(towrite)'''
                elif result == "neg":
                    if "neg" in name:
                        correct_spam+=1
                    spamCount+=1

                #print(result)
    nbCalculate(correct_spam,correct_ham,spamfiles,hamfiles,spamCount,hamCount)
    print(hamCount)
    print(correct_ham)
    print(spamCount)
    print(correct_spam)


if __name__ == '__main__':
    main()

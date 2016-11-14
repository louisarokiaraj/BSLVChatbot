
import sys

def read(filename):
    l1=list()
    with open(filename,'r') as fobj:
        tuple_list=list()
        for line in fobj:
            line=line.strip("\n")
            if line=="":
                l1.append(tuple_list)
                tuple_list=list()

            if line !='':
                if(len(line)>0):
                    words=line.split("\t")
                    if(len(words)>=2):
                        word=words[0]
                        tag=words[1]
                        tup=word,tag
                        tuple_list.append(tup)
    return l1

def main():
    filename=sys.argv[1]
    list=read(filename)
    print (list)
    print ("length is ",len(list))



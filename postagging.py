from nltk.tag import StanfordPOSTagger
import os
import sys
import string

# Set encoding to be utf8
#reload(sys)
#sys.setdefaultencoding('utf8')

os.environ['CLASSPATH']="/home/vrushali/Desktop/NLPProject/stanford-postagger-2015-12-09/stanford-postagger.jar"
os.environ['STANFORD_MODELS']="/home/vrushali/Desktop/NLPProject/stanford-postagger-2015-12-09/models"

count =0
def pos_tags(line_split_no_punctuation, st):
    """
    Predict the pos tag for each word in line_split_no_punctuation.
    """
    global  count
    count+=1
    print ("here count ",count)
    tags = st.tag(line_split_no_punctuation) # a list of [(w0, tag0), (w1, tag1), (w2, tag2)]
    print ("returning ")
    return tags

def main():
    st = StanfordPOSTagger('english-bidirectional-distsim.tagger', java_options="-mx3g")

       
    input_file= sys.argv[1]
    output_file = sys.argv[2]

    fwrite=open(output_file,'w')
    f = open(input_file, 'r')
    for line in f:
            line = line.strip('\n')
            line_split = line.split()
            line_split_no_punctuation = []

            if len(line_split) > 0:
                for word in line_split:
                    word = word.lstrip(string.punctuation)
                    word = word.rstrip(string.punctuation)

                    if len(word) != 0:
                        line_split_no_punctuation.append(word)
                tags = pos_tags(line_split_no_punctuation, st)

                for i in range(len(line_split_no_punctuation)):
                    fwrite.write((line_split_no_punctuation[i]) + '\t' + tags[i][1])
                    fwrite.write(("\n"))
                fwrite.write(("\n"))


if __name__ == '__main__':
    main()
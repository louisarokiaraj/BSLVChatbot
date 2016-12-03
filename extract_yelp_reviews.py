import simplejson as json
import os

def read_yelp():
    copypath_pos = "/home/vrushali/Desktop/NLPProject/smalltraindata/positive_reviews"
    copypath_neg = "/home/vrushali/Desktop/NLPProject/smalltraindata/negative_reviews"
    count_pos = 0
    count_neg = 0

    with open("/home/vrushali/Desktop/NLPProject/yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_review.json") as fin:
        for line in fin:
            line_contents = json.loads(line)
            filename=line_contents['review_id']
            if count_neg>5000 and count_pos>5000:
                break
            if(line_contents['stars']>=3) and count_pos<=5000:
                if not os.path.exists(copypath_pos):
                    os.makedirs(copypath_pos)
                with open(copypath_pos+"/"+filename, 'w') as fout:
                    print(line_contents['text'])
                    fout.write (line_contents['text'])
                    count_pos += 1
            elif(line_contents['stars']<3 and count_neg<=5000):
                if not os.path.exists(copypath_neg):
                    os.makedirs(copypath_neg)
                with open(copypath_neg + "/" + filename, 'w') as fout:
                    fout.write(line_contents['text'])
                    count_neg += 1
    print ("count pos",count_pos)
    print("count neg",count_neg)


read_yelp()
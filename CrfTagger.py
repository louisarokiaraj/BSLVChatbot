# -*- coding: utf-8 -*-
# Natural Language Toolkit: Interface to the CRFSuite Tagger
#
# Copyright (C) 2001-2016 NLTK Project
# Author: Long Duong <longdt219@gmail.com>
# URL: <http://nltk.org/>
# For license information, see LICENSE.TXT

"""
A module for POS tagging using CRFSuite
"""
from __future__ import absolute_import
from __future__ import unicode_literals
import unicodedata
import re
from nltk.tag.api import TaggerI
from nltk.tag import StanfordPOSTagger
import AnnotationFile as an
import os

os.environ['CLASSPATH']="/Users/louis/Documents/CSCI_544/BSLVChatbot/stanford-postagger-2015-12-09/stanford-postagger.jar"
os.environ['STANFORD_MODELS']="/Users/louis/Documents/CSCI_544/BSLVChatbot/stanford-postagger-2015-12-09/models"

import pycrfsuite




class CRFTagger(TaggerI):
    """
    A module for POS tagging using CRFSuite https://pypi.python.org/pypi/python-crfsuite
    from nltk.tag import CRFTagger
     ct = CRFTagger()
    train_data = [[('University','Noun'), ('is','Verb'), ('a','Det'), ('good','Adj'), ('place','Noun')], ... [('dog','Noun'),('eat','Verb'),('meat','Noun')]]
    ct.train(train_data,'model.crf.tagger')
    ct.tag_sents([['dog','is','good'], ['Cat','eat','meat']]) [[('dog', 'Noun'), ('is', 'Verb'), ('good', 'Adj')], [('Cat', 'Noun'), ('eat', 'Verb'), ('meat', 'Noun')]]
    gold_sentences = [[('dog','Noun'),('is','Verb'),('good','Adj')] , [('Cat','Noun'),('eat','Verb'), ('meat','Noun')]]
    ct.evaluate(gold_sentences) 1.0 Setting learned model file
    ct = CRFTagger()
    ct.set_model_file('model.crf.tagger')
    ct.evaluate(gold_sentences) 1.0
     """


    def __init__(self, feature_func=None, verbose=False, training_opt={}):
        """
        Initialize the CRFSuite tagger :param feature_func: The function that extracts features for each token of a sentence.
        This function should take 2 parameters: tokens and index which extract features at index position from tokens list.
        See the build in _get_features function for more detail.
         """
        #print("I am called")
        self._model_file = ''
        self._tagger = pycrfsuite.Tagger()
        if feature_func is None:
            self._feature_func = self._get_features
            #print("features set")
        else:
            self._feature_func = feature_func
        self._verbose = verbose
        self._training_options = training_opt
        self._pattern = re.compile(r'\d')
        self.st = StanfordPOSTagger('english-bidirectional-distsim.tagger', java_options="-mx3g")
        self.count=0
        self.pos_map={}

    def pos_tags(self,String):
        """
        Predict the pos tag for each word in String.
        """

        self.count += 1
        #print("here count ", self.count)
        tags = self.st.tag(String)  # a list of [(w0, tag0), (w1, tag1), (w2, tag2)]
        #print("returning ")
        return tags

    def set_model_file(self, model_file):
        self._model_file = model_file
        self._tagger.open(self._model_file)


    def _get_features(self, tokens,idx):
        """ Extract basic features about this word including - Current Word - Is Capitalized ? - Has Punctuation ? - Has Number ? -
        Suffixes up to length 3 Note that : we might include feature over previous word, next word ect.
        :return : a list which contains the features :rtype : list(str) """

        tokenString=' '.join(tokens)
        if tokenString in self.pos_map:
            #print(tokenString)
            #print(self.pos_map[tokenString])
            #print("-------------------------------")
            tags=self.pos_map[tokenString]

        else:
            tags=self.pos_tags(tokens)
            self.pos_map[tokenString]=tags

        token = tokens[idx]
        #print ("hereeee")
        #print("and tokens are ", tokens)
        feature_list = []
        if not token: return feature_list
        # Punctuation
        punc_cat = set(["Pc", "Pd", "Ps", "Pe", "Pi", "Pf", "Po"])
        if all (unicodedata.category(x) in punc_cat for x in token):
            feature_list.append('PUNCTUATION')

        if idx==0:
            feature_list.append('WORD_'+token)

            cur_tag=tags[idx][1]
            if len(tokens) != 1:
                next_tag=tags[idx+1][1]
                feature_list.append('NEXT_WORD' + tokens[idx + 1])
                feature_list.append('POS[0]'+cur_tag)
                feature_list.append('POS[1]' + next_tag)
            else:
                feature_list.append('POS[0]' + cur_tag)

        elif idx==(len(tokens)-1):
            feature_list.append('PREV_WORD_'+tokens[idx-1])
            feature_list.append('WORD_'+token)
            cur_tag = tags[idx][1]
            prev_tag = tags[idx - 1][1]
            feature_list.append('POS[-1]' + prev_tag)
            feature_list.append('POS[0]' + cur_tag)
        else:
            feature_list.append('PREV_WORD'+tokens[idx - 1])
            feature_list.append('WORD_'+token)
            feature_list.append('NEXT_WORD'+tokens[idx + 1])
            prev_tag = tags[idx-1][1]
            cur_tag = tags[idx][1]
            next_tag = tags[idx + 1][1]
            feature_list.append('POS[-1]' + prev_tag)
            feature_list.append('POS[0]' + cur_tag)
            feature_list.append('POS[1]' + next_tag)

        return feature_list



    def tag_sents(self,sents):
        """
        Tag a list of sentences. NB before using this function, user should specify the mode_file either by - Train a new model using ``train''
         function - Use the pre-trained model which is set via ``set_model_file'' function
         :params sentences : list of sentences needed to tag.
         :type sentences : list(list(str))
         :return : list of tagged sentences.
         :rtype : list (list (tuple(str,str)))
         """
        self._model_file="/Users/louis/Documents/CSCI_544/BSLVChatbot/model.crf.tagger"

        if os.path.isfile(self._model_file):
            self.set_model_file(self._model_file)



        if self._model_file == '':
            raise Exception(' No model file is found !! Please use train or set_model_file function')

            # We need the list of sentences instead of the list generator for matching the input and output
        result = []
        for tokens in sents:
            features = [self._feature_func(tokens,i) for i in range(len(tokens))]
            labels = self._tagger.tag(features)

            if len(labels) != len(tokens):
                raise Exception(' Predicted Length Not Matched, Expect Errors !')

            tagged_sent = list(zip(tokens,labels))
            result.append(tagged_sent)
        return result

    def form_pos_tag_list(self,filename):
        with open(filename,'r') as fobj:
            tuple_list = list()
            sentence=""
            for line in fobj:
                line = line.strip("\n")
                if line == "":
                    self.pos_map[sentence]=tuple_list
                    tuple_list = list()
                    sentence=""

                if line != '':
                    if (len(line) > 0):
                        words = line.split("\t")
                        if (len(words) == 2):
                            word = words[0]
                            if sentence=="":
                                sentence=word
                            else:
                                sentence=sentence+' '+word
                            tag = words[1]
                            tup = word, tag
                            tuple_list.append(tup)
        #print("len of hashmap ",len(self.pos_map))

    def train(self, train_data,model_file):
        ''' Train the CRF tagger using CRFSuite :params train_data : is the list of annotated sentences.
        :type train_data : list (list(tuple(str,str)))
        :params model_file : the model will be saved to this file.
        '''


        trainer = pycrfsuite.Trainer(verbose=self._verbose)
        trainer.set_params(self._training_options)
        for sent in train_data:
            tokens, labels = zip(*sent)
            features = [self._feature_func(tokens, i) for i in range(len(tokens))]
            trainer.append(features, labels)  # Now train the model, the output should be model_file
        trainer.train(model_file)
        # Save the model file
        self.set_model_file(model_file)



    def tag(self,tokens):
        '''
        Tag a sentence using Python CRFSuite Tagger.
         NB before using this function, user should specify the mode_file either by - Train a new model using ``train'' function
         - Use the pre-trained model which is set via ``set_model_file'' function :params tokens : list of tokens needed to tag.
          :type tokens : list(str) :return : list of tagged tokens. :rtype : list (tuple(str,str))
          '''

        #print (tokens)
        return self.tag_sents([tokens])[0]

def main():
    ct = CRFTagger()
    #train_data = [[('University', 'Noun'), ('is', 'Verb'), ('a', 'Det'), ('good', 'Adj'), ('place', 'Noun')],[('dog', 'Noun'), ('eat', 'Verb'), ('meat', 'Noun')]]
    ct.form_pos_tag_list("pos_data.txt")
    #train_data=an.read('labelledWords')
    #print("Length of train data",len(train_data))

    #ct.train(train_data, 'model.crf.tagger')

    result=ct.tag_sents([['I','prefer','spicy','Chinese'],['Please','recommend','some','indian','restaurant','near','las','vegas'],
                        ['I','am','interested','in','mexican','food'],['Mexican','food'],['cheap','food','near','santa','monica'],['Give','me','a','list','of','asian','cuisines','near','sacramento'],
                         ['costly','in','price'],['Los','Angeles'],['Pasedina'],['Moderate','is','fine']])
    #print (result)



from __future__ import absolute_import
from __future__ import unicode_literals
from subprocess import call
from speech_recognition.mainModule import Speech_Reg
import random
from CrfTagger import CRFTagger
from yelpAPI import GetAPIResults
import unicodedata
import re
from nltk.tag.api import TaggerI
from nltk.tag import StanfordPOSTagger

import os

os.environ['CLASSPATH']="/Users/louis/Documents/CSCI_544/BSLVChatbot/stanford-postagger-2015-12-09/stanford-postagger.jar"
os.environ['STANFORD_MODELS']="/Users/louis/Documents/CSCI_544/BSLVChatbot/stanford-postagger-2015-12-09/models"

class BSLVChatBot:

    def __init__(self):
        self.sr = Speech_Reg()

class Fix_choice:

    def __init__(self):
        self.bslvChatBotObj = BSLVChatBot().sr
        self.STARTUP_FILTER={}
        self.resultDict = {}
        self.analyzedSentimentDict = {}
        self.BOOLEAN_PRICE = False
        self.BOOLEAN_LOCATION = False
        self.BOOLEAN_CUISINE = False

        self.fetchedRestaurant=[]
        self.fetchedAddress = []
        self.fetchedURL = []

        self.PRICE_VALUE = ""
        self.LOCATION_VALUE = ""
        self.CUISINE_VALUE = ""

        self.STARTUP_FILTER["GREETING_WORDS"]=["Hi, How may I help you","What can I do for you Today",
                                          "How may I help you today"," Hi, Ready to eat ?", "Hi, I am happy you are here !. What type of restaurant you are looking for ?"]

        self.STARTUP_FILTER['PRICE_GIVEN']=["Great!, May I know what location would you like ?",
                                            "Great!, May I know what type of cuisine would you like ?","Location ?",
                                       "Cuisine?","Awesome!, can you tell me location and Cuisine ?",
                                       "Any preferences of location and cuisine ?","Location please", "May I know your choice of Cuisine please ?"
                                       "Cuisine and Location please"]

        self.STARTUP_FILTER['LOCATION_GIVEN']=["I would like to know the type of cuisine please","cuisine preferences?",
                                          "Wow!, good choice now tell me the price (Cheap / Moderate / Medium / Expensive) range ",
                                          "Great place, can you tell me what cuisine and price (Cheap / Moderate / Medium / Expensive) you looking for?",
                                          "Price please (Cheap / Moderate / Medium / Expensive) ","Cuisine please","great , May I know your preferred price (Cheap / Moderate / Medium / Expensive) range"]

        self.STARTUP_FILTER['CUISINE_GIVEN']=["Tell me the Price (Cheap / Moderate / Medium / Expensive) range","Tell me the location please",
                                         "Can you tell me the price (Cheap / Moderate / Medium / Expensive) and location","Price please (Cheap / Moderate / Medium / Expensive) ","Any preferred price (Cheap / Moderate / Medium / Expensive)",
                                         "Any preferred location",
                                         "Good choice, I would like to know your preferred location as well"]

        self.STARTUP_FILTER['PRICE_LOCATION_GIVEN']= ["I just need one more Information, can you tell me the Cuisine type please",
                                                 "Favourite cuisine ?", "Can I have your cuisine preference please ?"]

        self.STARTUP_FILTER['PRICE_CUISINE_GIVEN'] = ["Can you tell me the location please","Location please","Preferred Location?",
                                                 "I would like to know what location you are looking for?"]

        self.STARTUP_FILTER['LOCATION_CUISINE_GIVEN'] = ["What price (Cheap / Moderate / Medium / Expensive) range you are looking for?","Can you tell me the expected price (Cheap / Moderate / Medium / Expensive) please?",
                                                    "May i know your price (Cheap / Moderate / Medium / Expensive) range?","Any price preferences (Cheap / Moderate / Medium / Expensive) ?"]

        self.STARTUP_FILTER['STANDARD_RESPONSE'] = ["let's talk about restaurants",
                                               "I'm here to recommend you restaurants","My knowledge is limited to restaurants","I can assist you to choose good restaurants", "Shall we discuss about restaurants ?"]

        self.STARTUP_FILTER['INCORRECT_ANSWERS'] = ["Sorry, I didn't catch that"]

    def temp_crf(self, sentence):
        split_list = sentence.split(" ")
        ct = CRFTagger()
        ct.form_pos_tag_list("/Users/louis/Documents/CSCI_544/BSLVChatbot/pos_data.txt")
        result = ct.tag(split_list)

        for word, tag in result:
            if 'B-CUISINE' in tag:
                if self.BOOLEAN_CUISINE == False:
                    self.BOOLEAN_CUISINE = True
                    self.CUISINE_VALUE = word.lower()
            if 'B-PRICE' in tag:
                if self.BOOLEAN_PRICE == False:
                    self.BOOLEAN_PRICE = True
                    self.PRICE_VALUE = word.lower()
            if 'B-LOCATION' in tag:
                if self.BOOLEAN_LOCATION == False:
                    self.BOOLEAN_LOCATION = True
                    self.LOCATION_VALUE = word.lower()
            if 'I-LOCATION' in tag:
                    self.BOOLEAN_LOCATION = True
                    self.LOCATION_VALUE += " "+word.lower()

        if self.BOOLEAN_LOCATION or self.BOOLEAN_PRICE or self.BOOLEAN_CUISINE:
            return self.fix_choice()
        else:
            return self.fix_choice("invalid_choice")

    def handle_negatives(self):
        print("My apology. Can you please tell me with what attribute you are uncomfortable with ? [Cuisine / Location / Price]")
        confirmValue2 = self.bslvChatBotObj.speech_recognition()
        if confirmValue2 is not None:
            if "cuisine" in confirmValue2.lower() and "location" in confirmValue2.lower() and "price" in confirmValue2.lower():
                print("Line 106")
                self.BOOLEAN_CUISINE = False
                self.BOOLEAN_LOCATION = False
                self.BOOLEAN_PRICE = False
            elif "cuisine" in confirmValue2.lower() and "location" in confirmValue2.lower():
                self.BOOLEAN_CUISINE = False
                self.BOOLEAN_LOCATION = False
            elif "cuisine" in confirmValue2.lower() and "price" in confirmValue2.lower():
                self.BOOLEAN_CUISINE = False
                self.BOOLEAN_PRICE = False
            elif "location" in confirmValue2.lower() and "price" in confirmValue2.lower():
                self.BOOLEAN_LOCATION = False
                self.BOOLEAN_PRICE = False
            elif "cuisine" in confirmValue2.lower():
                self.BOOLEAN_CUISINE = False
            elif "location" in confirmValue2.lower():
                self.BOOLEAN_LOCATION = False
            elif "price" in confirmValue2.lower():
                self.BOOLEAN_PRICE = False
            else:
                self.handle_negatives()
            return self.fix_choice()
        else:
            self.handle_negatives()

    def call_speech(self):
        confirmValue = None
        while confirmValue is None or ("yes" not in confirmValue.lower() and "no" not in confirmValue.lower()):
            confirmValue = self.bslvChatBotObj.speech_recognition()
        if "yes" in confirmValue.lower():
            return True
        elif "no" in confirmValue.lower():
            return self.handle_negatives()


    def fix_choice(self, invalid_choice=False):
        final_return_value =""
        if invalid_choice == "invalid_choice":
            question = random.choice(self.STARTUP_FILTER['STANDARD_RESPONSE'])
            if question is not None:
                final_return_value += question
            else:
                final_return_value += random.choice(self.STARTUP_FILTER['STANDARD_RESPONSE'])
        if self.BOOLEAN_PRICE and self.BOOLEAN_LOCATION and self.BOOLEAN_CUISINE:
            print("Just to confirm once, You preferred " + self.CUISINE_VALUE + " for Cuisine , " + self.PRICE_VALUE + " for Price and " + self.LOCATION_VALUE + " for Location., Is this correct ?. [Yes / No]")
            ret = self.call_speech()
            if ret == True:
                yelpObj = GetAPIResults()
                self.resultDict,self.analyzedSentimentDict = yelpObj.get_results(self.LOCATION_VALUE.lower(), self.PRICE_VALUE, self.CUISINE_VALUE.lower())
                if self.resultDict is None or len(self.resultDict) == 0:
                    self.BOOLEAN_LOCATION = False
                    self.BOOLEAN_PRICE = False
                    self.BOOLEAN_CUISINE = False
                    self.CUISINE_VALUE = ""
                    self.PRICE_VALUE = ""
                    self.LOCATION_VALUE = ""
                    print("Sorry, No results found for the given preferences. Let me give another try")
                    return self.temp_crf("I want to eat")
                print()
                print("################# Here you Go #################")
                print()
                counter = 0
                keylist = ["Name: ","URL: ","Address: ","Overall Review: "]
                for key,value in self.resultDict.items():
                    if counter < 3:
                        i=0
                        counter_2 = 0
                        print("---------------------------------")
                        for val in value:
                            if counter_2 == 3:
                                if val in self.analyzedSentimentDict:
                                   review = self.analyzedSentimentDict[val]
                                   print(keylist[i],review)
                            else:
                                print(keylist[i],val)
                            i=i+1
                            counter_2+=1
                        print("---------------------------------")
                        counter = counter+1
                    print()
                return "!!!!!!!!!!!!!!!!!!!!!! Bon appetit !!!!!!!!!!!!!!!!!!!!!!"
            else:
                return ret
        elif self.BOOLEAN_CUISINE and self.BOOLEAN_LOCATION:
            question = random.choice(self.STARTUP_FILTER['LOCATION_CUISINE_GIVEN'])
            if question is not None:
                final_return_value += question
            else:
                final_return_value += random.choice(self.STARTUP_FILTER['LOCATION_CUISINE_GIVEN'])

        elif self.BOOLEAN_PRICE and self.BOOLEAN_LOCATION:
            question = random.choice(self.STARTUP_FILTER['PRICE_LOCATION_GIVEN'])
            if question is not None:
                final_return_value += question
            else:
                final_return_value += random.choice(self.STARTUP_FILTER['PRICE_LOCATION_GIVEN'])

        elif self.BOOLEAN_CUISINE and self.BOOLEAN_PRICE:
            question = random.choice(self.STARTUP_FILTER['PRICE_CUISINE_GIVEN'])
            if question is not None:
                final_return_value += question
            else:
                final_return_value += random.choice(self.STARTUP_FILTER['PRICE_CUISINE_GIVEN'])

        elif self.BOOLEAN_PRICE:
            question = random.choice(self.STARTUP_FILTER['PRICE_GIVEN'])
            if question is not None:
                final_return_value += question
            else:
                final_return_value += random.choice(self.STARTUP_FILTER['PRICE_GIVEN'])

        elif self.BOOLEAN_CUISINE:
            question = random.choice(self.STARTUP_FILTER['CUISINE_GIVEN'])
            if question is not None:
                final_return_value += question
            else:
                final_return_value += random.choice(self.STARTUP_FILTER['CUISINE_GIVEN'])

        elif self.BOOLEAN_LOCATION:
            question = random.choice(self.STARTUP_FILTER['LOCATION_GIVEN'])
            if question is not None:
                final_return_value += question
            else:
                final_return_value += random.choice(self.STARTUP_FILTER['LOCATION_GIVEN'])
        return final_return_value

if __name__ == '__main__':
    choice = Fix_choice()
    while True:
        return_value = choice.bslvChatBotObj.speech_recognition()
        if return_value is not None:
            print("ChatBot: "+str(choice.temp_crf(return_value)))
        if choice.BOOLEAN_CUISINE and choice.BOOLEAN_LOCATION and choice.BOOLEAN_PRICE:
            break
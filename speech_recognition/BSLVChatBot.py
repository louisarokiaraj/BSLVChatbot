from subprocess import call
from SpeechReg.speech_recognition.mainModule import Speech_Reg
import random

class BSLVChatBot:
    def __init__(self):
        self.sr = Speech_Reg()


class Fix_choice:

    def __init__(self):

        self.STARTUP_FILTER={}

        self.BOOLEAN_PRICE = False
        self.BOOLEAN_LOCATION = False
        self.BOOLEAN_CUSINE = False

        self.PRICE_VALUE = ""
        self.LOCATION_VALUE = ""
        self.CUSINE_VALUE = ""

        self.STARTUP_FILTER["GREETING_WORDS"]=["Hi, How may I help you","Hello","What can I do for you Today",
                                          "How may I help you today"," Hi, Ready to eat"]
        self.STARTUP_FILTER['PRICE_GIVEN']=["Great!, May I know what location would you like","Great!, May I know what type of "
                                        "cuisine Would you like","Location ?",
                                       "Cuisine?","Awesome!, can you tell me location and price",
                                       "Any preferences of location and price?","Price please","Location please",
                                       "price and location please"]

        self.STARTUP_FILTER['LOCATION_GIVEN']=["I would like to know the type of cuisine please","cuisine preferences?",
                                          "Wow!, good choice now tell me the price range",
                                          "Great place, can you tell me what cuisine and price you looking for?",
                                          "price please","cuisine please","great , may i know your preferred price range"]
        self.STARTUP_FILTER['CUISINE_GIVEN']=["Tell me the Price range","tell me the location please",
                                         "Can you tell me the price and location","Price please","any preferred price",
                                         "any preferred location",
                                         "good choice, I would like to know your preferred location as well"]

        self.STARTUP_FILTER['PRICE_LOCATION_GIVEN']= ["I just need one more Information, can you tell me the Cuisine type please",
                                                 "Favourite cuisine", "Can i have your cuisine preference"]

        self.STARTUP_FILTER['PRICE_CUISINE_GIVEN'] = ["Can you tell me the location please","Location please","Preferred Location?",
                                                 "I would like to know what location you are looking far?"]
        self.STARTUP_FILTER['LOCATION_CUISINE_GIVEN'] = ["What price range you are looking for?","Price please?",
                                                    "May i know your price range?"]
        self.STARTUP_FILTER['STANDARD_RESPONSE'] = ["OOPS, I didn't get that","let's talk about restaurants",
                                               "I'm here to recommend you restaurants","My knowledge is limited to restaurants"]
        self.STARTUP_FILTER['INCORRECT_ANSWERS'] = ["Sorry, I didn't catch that"]


    def temp_crf(self, sentence):
        self.cusine_type = ["indian", "chinese","italian","mexican"]
        self.location_type = ["los angeles", "san jose", "san francisco","downtown"]
        self.price_type = ["medium", "moderate","cheap","expensive"]


        split_list = sentence.split(" ")
        for word in split_list:
            if word.lower()in self.cusine_type:
                self.BOOLEAN_CUSINE = True
                self.cusine_type = word.lower()
                return self.fix_choice()
            elif word.lower()in self.location_type:
                self.BOOLEAN_LOCATION = True
                self.location_type = word.lower()
                return self.fix_choice()
            elif word.lower()in self.price_type:
                self.BOOLEAN_PRICE = True
                self.price_type = word.lower()
                return self.fix_choice()

        return self.fix_choice("invalid_choice")


    def fix_choice(self, invalid_choice=False):
        final_return_value =""
        if invalid_choice == True:
            final_return_value = random.choice(self.STARTUP_FILTER['STANDARD_RESPONSE'])
        if self.BOOLEAN_PRICE and self.BOOLEAN_LOCATION and self.BOOLEAN_CUSINE:
            return "got all values"
        elif self.BOOLEAN_CUSINE and self.BOOLEAN_LOCATION:
            final_return_value += random.choice(self.STARTUP_FILTER['LOCATION_CUISINE_GIVEN'])
        elif self.BOOLEAN_PRICE and self.BOOLEAN_LOCATION:
            final_return_value += random.choice(self.STARTUP_FILTER['PRICE_LOCATION_GIVEN'])
        elif self.BOOLEAN_CUSINE and self.BOOLEAN_PRICE:
            final_return_value += random.choice(self.STARTUP_FILTER['PRICE_CUISINE_GIVEN'])
        elif self.BOOLEAN_PRICE:
            final_return_value += random.choice(self.STARTUP_FILTER['PRICE_GIVEN'])
        elif self.BOOLEAN_CUSINE:
            final_return_value += random.choice(self.STARTUP_FILTER['CUISINE_GIVEN'])
        elif self.BOOLEAN_LOCATION:
            final_return_value += random.choice(self.STARTUP_FILTER['LOCATION_GIVEN'])

        return final_return_value


if __name__ == '__main__':
    bot = BSLVChatBot()
    choice = Fix_choice()
    while True:
        return_value = bot.sr.speech_recognition()
        print("my value ",return_value)
        print(choice.temp_crf(return_value))

        if choice.BOOLEAN_CUSINE and choice.BOOLEAN_LOCATION and choice.BOOLEAN_PRICE:
            break

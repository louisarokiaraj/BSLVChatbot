import http.client
import nbClassify

class GetAPIResults:
    def __init__(self):
        self.name = []
        self.reviewList = []
        self.foodType = {}
        self.parsedReviews={}
        self.url = []
        self.address = []
        self.resultDict = {}
        self.conn = http.client.HTTPSConnection("api.yelp.com")

    def loadFoodType(self):
        with open('/Users/louis/Documents/CSCI_544/BSLVChatbot/foodMap.txt','r') as fileHandler:
            for line in fileHandler:
                line_split = line.split('-')
                self.foodType[line_split[0].strip().lower()] = line_split[1].strip().lower()


    def makeExternalCall(self,URL,isQueryString=None):
        import requests
        url = URL

        headers = {
            'authorization': "bearer c9N0YruaB-ZFAMkkESOQmHUseB6XlEufsfwDQeZtDBrpfYeBrAlzUm-TaewH-OVDl7eOJKcld3lfJXcMc9vqt6302B4tECWEeQst7frkDx4Jc24BSVFoUuAu4ygoWHYx",
            'cache-control': "no-cache",
            'postman-token': "cbcfc3dd-3198-971e-a1e2-4db46019968e"
        }
        if isQueryString is not None:
            response = requests.request("GET", url, headers=headers, params=isQueryString)
        else:
            response = requests.request("GET", url, headers=headers)

        return response

    def get_api_data(self, location, price, categories, sort_by, limit):
        self.loadFoodType()
        if categories in self.foodType.keys():
            categories = self.foodType[categories]
        else:
            self.resultDict = {}
        querystring = {"location": location, "price": str(price), "categories": categories, "sort_by": sort_by,
                       "limit": limit}
        response = self.makeExternalCall("https://api.yelp.com/v3/businesses/search",querystring)
        data = response.text
        import json
        try:
            dict = json.loads(data)
            self.parse_json(dict)
        except Exception:
            self.resultDict = {}

    def parse_json(self, json_dict):

        for i in range(0, len(json_dict.get('businesses'))):
            self.resultDict[i] = []
            add = ""
            if json_dict.get('businesses')[i].get('location').get('address1') is not None:
                add += " " + json_dict.get('businesses')[i].get('location').get('address1')
            if json_dict.get('businesses')[i].get('location').get('address2') is not None:
                add += " " + json_dict.get('businesses')[i].get('location').get('address2')
            if json_dict.get('businesses')[i].get('location').get('address3') is not None:
                add += " " + json_dict.get('businesses')[i].get('location').get('address3')
            if json_dict.get('businesses')[i].get('location').get('city') is not None:
                add += " " + json_dict.get('businesses')[i].get('location').get('city')
            if json_dict.get('businesses')[i].get('location').get('zip_code') is not None:
                add += " " + json_dict.get('businesses')[i].get('location').get('zip_code')
            self.resultDict[i].append(json_dict.get('businesses')[i].get('name'))
            self.resultDict[i].append(json_dict.get('businesses')[i].get('url'))
            self.resultDict[i].append(add)
            self.reviewList.append(json_dict.get('businesses')[i].get('id'))
            self.resultDict[i].append(json_dict.get('businesses')[i].get('id'))

    def extractReviews(self):
        for id in self.reviewList:
            response = self.makeExternalCall("https://api.yelp.com/v3/businesses/"+id+"/reviews")
            data = response.text
            import json
            try:
                dict = json.loads(data)
                tempList = []
                for values in dict['reviews']:
                    tempList.append(values['text'])
                    self.parsedReviews[id] = tempList
            except Exception:
                self.parsedReviews[id] = []

        analyzedDictOutput = nbClassify.classify(self.parsedReviews)
        return analyzedDictOutput


    def get_results(self,location, price, categories):
        api = GetAPIResults()
        sort_by = "rating"
        limit = "6"
        if(price.lower() == "cheap"):
            price = "1"
        elif(price.lower() == "moderate" or price.lower() == "moderately" or price.lower() == "medium"):
            price = "2,3"
        elif(price.lower() == "expensive"):
            price = "4"
        api.get_api_data(location, price, categories, sort_by, limit)
        return api.resultDict,api.extractReviews()
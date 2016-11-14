import http.client

class GetAPIResults:
    def __init__(self):
        self.name = []
        self.url = []
        self.address = []
        self.conn = http.client.HTTPSConnection("api.yelp.com")

    def get_api_data(self, location, price, categories, sort_by, limit):
        headers = {
            'authorization': "bearer c9N0YruaB-ZFAMkkESOQmHUseB6XlEufsfwDQeZtDBrpfYeBrAlzUm-TaewH-OVDl7eOJKcld3lfJXcMc9vqt6302B4tECWEeQst7frkDx4Jc24BSVFoUuAu4ygoWHYx",
            'cache-control': "no-cache"
        }
        self.conn.request("GET",
                          "/v3/businesses/search?location==" + location + "&price=" + price + "&categories=" + categories + "&sort_by=" + sort_by + "&limit=" + limit + "",
                          headers=headers)
        res = self.conn.getresponse()
        data = res.read()
        # print(data.decode("utf-8"))
        import json
        dict = json.loads(data.decode("utf-8"))
        self.parse_json(dict)

    def parse_json(self, json_dict):

        for i in range(0, len(json_dict.get('businesses'))):
            self.name.append(json_dict.get('businesses')[i].get('name'))
            self.url.append(json_dict.get('businesses')[i].get('url'))
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
            self.address.append(add)

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
        return api.name,api.url,api.address
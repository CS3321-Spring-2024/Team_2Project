
import json
import requests
import os
# import jsonify
import re


# for the NASA API to work you need to get an API key from the NASA website and set it as an environment variable
#  get key here ->      https://api.nasa.gov/
# in poetry shell run -> export NASA_API_KEY="your_key_"


# POTD -> photo of the day

class POTD:
    '''Photo of the day object. This object is used to store the data from the NASA API. It has a url, title, and description.\
    The description is optional. If the description is not provided, the object will return a dictionary without the description.'''
    url:str
    title:str
    desc:str

    def __init__(self, url:str, title:str, desc:str = None):
        self.url = url
        self.title = title
        self.desc = desc

    
    def get_title(self) -> str:
        return self.title
    
    def no_desc(self):
        return {
            "url": self.url,
            "title": self.title
        }

    
class WikiData:
    '''Wikipedia data object. This object is used to store the data from the Wikipedia API. It has a title, description, url, and thumbnail.'''
    title:str
    description:str
    url:str
    thumbnail:str

    def __init__(self, title:str = None, description:str = None, url:str = None, thumbnail:str = None):
        self.title = title
        self.description = description
        self.url = url
        self.thumbnail = thumbnail

    def __str__(self) -> str:
        return f"Title: {self.title}, Description: {self.description}, URL: {self.url}, Thumbnail: {self.thumbnail}"

## construct the defualt error objects
def generate_error_message():
    error_potd = POTD("https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Challenger_explosion.jpg/1920px-Challenger_explosion.jpg?20211117142956", "Challenger Disaster", "An error occurred while fetching the data. Much like the Challenger Disaster, this is a disaster, but much less fatal.")
    error_w1 = WikiData("Challenger Disaster", "On January 28, 1986, the Space Shuttle Challenger broke apart 73 seconds into its flight, killing all seven crew members aboard. The spacecraft disintegrated 46,000 feet (14 km) above the Atlantic Ocean, off the coast of Cape Canaveral, Florida, at 11:39 a.m. EST (16:39 UTC). It was the first fatal accident involving an American spacecraft while in flight.", "https://en.wikipedia.org/wiki/Space_Shuttle_Challenger_disaster","https://upload.wikimedia.org/wikipedia/commons/b/b5/Challenger_The_Final_Flight_2020.png")
    error_w2 = WikiData("HTTP status codes","The server failed to fulfill a request. Response status codes beginning with the digit '5' indicate cases in which the server is aware that it has encountered an error or is otherwise incapable of performing the request.","https://en.wikipedia.org/wiki/List_of_HTTP_status_codes#5xx_server_errors","https://upload.wikimedia.org/wikipedia/commons/9/95/Error-Logo.png")
    error_wiki = [error_w1, error_w2]

    error_json = {
        "POTD": error_potd.__dict__,
        "Query": "ERROR 500",
        "WIKI_DATA": [data.__dict__ for data in error_wiki]
    }
    return error_potd, error_json

## end defualt error objects

def validate_date(date:str) -> bool:
    '''This function takes a date string and returns True if the date is in the format yyyy-mm-dd, otherwise it returns False.'''
    # date format should be yyyy-mm-dd
    date_regex = re.compile(r"\d{4}-\d{2}-\d{2}")
    return date_regex.match(date) != None

def get_potd(date:str = None) -> POTD:
    baseURL = "https://api.nasa.gov/planetary/apod"
    apiKey = os.getenv("NASA_API_KEY")
    params = {
        "api_key": apiKey,
    }
    if date != None and validate_date(date):
        params["date"] = date
    
    response = requests.get(baseURL, params=params)
    json_data = response.json()
    # POTD_obj = generate_error_message()[0]
    try:                        #
        POTD_obj = POTD(json_data["url"], json_data["title"], json_data['explanation'] )
        data = json.dumps(POTD_obj.__dict__)
    except:
        print(json_data)                                                        ## add error response for missing key of json parsing (challenger?)
    
    return POTD_obj



def get_wiki_data(search_Query:str = "blue_shift")-> list[WikiData]:
    '''This function takes a search query and returns a list of WikiData objects.\
    The search query is used to search Wikipedia for relevant articles. The function returns a list of WikiData objects.\
    If the search query is not provided, the function will return a list of WikiData objects for the search query "blue_shift".'''
    language_code = "en"
    
    number_of_results = 5
    base_url = 'https://api.wikimedia.org/core/v1/wikipedia/'
    endpoint = '/search/page'
    url = base_url + language_code + endpoint
    parameters = {'q': search_Query, 'limit': number_of_results}
    response = requests.get(url,  params=parameters)
    list_of_wiki_data = []
    for result in response.json()["pages"]:
        # print(result)
        try:
            title = result["title"]
            description = result["description"]
            url = f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"
            if result['thumbnail'] == None:
                thumbnail = 'None' 
            else:
                thumbnail ="http://"+ result["thumbnail"]["url"][2:]
            wiki_data = WikiData(title, description, url, thumbnail)
            list_of_wiki_data.append(wiki_data)
        except:
            print(result)
        
    return list_of_wiki_data




def get_POTD_with_desc():
    '''This function returns a dictionary with the POTD, a query, and the Wikipedia data.'''
    try:
        NASA_data:POTD = get_potd()
        WIKI_DATA:list[WikiData] = get_wiki_data(NASA_data.get_title())
        return_data =  {
            "POTD": NASA_data.__dict__,
            "Query": "Get More context from Wikipedia.",
            "WIKI_DATA": [data.__dict__ for data in WIKI_DATA]
        }
        return return_data
    except:
        return generate_error_message()[1]
    # return json.dumps(return_data)



def get_POTD_without_desc():
    '''Not Currently used, we were unsure about if we should return the description from NASA or not.'''
    NASA_data:POTD = get_potd()
    WIKI_DATA:list[WikiData] = get_wiki_data(NASA_data.get_title())
    return_data =  {
        "POTD": NASA_data.no_desc(),
        "Query": "Get More context from Wikipedia.",
        "WIKI_DATA": [data.__dict__ for data in WIKI_DATA]
    }
    return return_data
    
def get_past_POTD_with_desc(date:str):
    '''This function takes a date string and returns a dictionary with the POTD, a query, and the Wikipedia data.'''
    if validate_date(date):
        NASA_data:POTD = get_potd(date)
        WIKI_DATA:list[WikiData] = get_wiki_data(NASA_data.get_title())
        return_data =  {
            "POTD": NASA_data.__dict__,
            "Query": "Get More context from Wikipedia.",
            "WIKI_DATA": [data.__dict__ for data in WIKI_DATA]
        }
        return return_data
    else:
        return generate_error_message()[1]   # add error response for invalid date (challenger?)
    


if __name__ == "__main__":
    print(get_past_POTD_with_desc("2023-11-29"))
    print(get_POTD_with_desc())
from datetime import datetime
import json
import re
import requests

class timesketchAPI:
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.csrf_token = self.authentication()

    
    def get_csrf(self, content):
        regex = r"<meta name=csrf-token content=\"([^\"]+)\">"

        matches = re.findall(regex, content)
        if len(matches) > 0: csrf_token = matches[0]

        return csrf_token


    def authentication(self):
        url = f"{self.url}/login/"

        # Get CSRF
        response = self.session.get(url=url)

        csrf_token = self.get_csrf(response.text)
        data = {
            "username": self.username,
            "password": self.password,
            "csrf_token": csrf_token
        }
        response = self.session.post(url=url, data=data)
        csrf_token = self.get_csrf(response.text)
        ## DEBUG print(csrf_token)
        return csrf_token


    def list_sketches(self):
        url = f"{self.url}/api/v1/sketches/"
        response = self.session.get(url)

        if response.status_code == 200:
            print("Connexion réussie.")
            print(response.text)
            sketches = response.json().get("objects", [])
            for sketch in sketches:
                print(f"- [{sketch['id']}] {sketch['name']}")
        else:
            print(f"Erreur : {response.status_code}")
            print(response.text)


    def get_starred_events(self, sketch_id, max_event_retrieved=10000):

        url = f"{self.url}/api/v1/sketches/{sketch_id}/explore/"
        headers = {
            'X-CSRFToken' : self.csrf_token,
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language' : 'en-US,en;q=0.5',
            'Accept-Encoding' : 'gzip, deflate',
            'Content-Type' : 'application/json'
        }

        data = {
            "query":"*",
            "filter":{
                "from":0,
                "terminate_after":max_event_retrieved,
                "size":max_event_retrieved,
                "order":"asc",
                "chips": [
                    {
                        "field":"",
                        "value":"__ts_star",
                        "type":"label",
                        "operator":"must",
                        "active":True
                    }],
                    "fields":[
                        {
                            "field":"message","type":"text"
                        },
                        {
                            "field":"data_type","type":"text"
                        },
                        {
                            "field":"computer_name","type":"text"
                        },
                        {
                            "field":"Computer","type":"text"
                        },
                        {
                            "field":"filename","type":"text"
                        },
                        {
                            "field":"sha256_hash","type":"text"
                        },
                        {
                            "field":"xml_string","type":"text"
                        },
                        ]
                },
            "include_processing_timelines":False
        }

        response = self.session.post(url=url, headers=headers, json=data)
        try:
            return response.json()
        except Exception as error:
            return error 



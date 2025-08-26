import json
import requests
from requests.auth import HTTPBasicAuth


# Configuration
TIMESKETCH_URL = "http://127.0.0.1:5080"
TIMESKETCH_SKETCH_ID = 2
TIMESKETCH_MAX_EVENTS_RETRIEVED = 10000
USERNAME = ""
PASSWORD = ""

session = requests.Session()

def get_csrf(content):
    import re
    regex = r"<meta name=csrf-token content=\"([^\"]+)\">"

    matches = re.findall(regex, content)
    if len(matches) > 0: csrf_token = matches[0]

    return csrf_token


def authentication():
    url = f"{TIMESKETCH_URL}/login/"

    # Get CSRF
    response = session.get(url=url)

    csrf_token = get_csrf(response.text)
    data = {
        "username": USERNAME,
        "password": PASSWORD,
        "csrf_token": csrf_token
    }
    response = session.post(url=url, data=data)
    csrf_token = get_csrf(response.text)
    print(csrf_token)

    ## DEBUG print(response.text)
    return csrf_token


def list_sketches():
    url = f"{TIMESKETCH_URL}/api/v1/sketches/"
    response = session.get(url)

    if response.status_code == 200:
        print("Connexion réussie.")
        print(response.text)
        sketches = response.json().get("objects", [])
        for sketch in sketches:
            print(f"- [{sketch['id']}] {sketch['name']}")
    else:
        print(f"Erreur : {response.status_code}")
        print(response.text)


def get_starred_events(csrf_token, sketch_id, max_event_retrieved):

    url = f"{TIMESKETCH_URL}/api/v1/sketches/{sketch_id}/explore/"
    headers = {
        'X-CSRFToken' : csrf_token,
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
                        "field":"message",
                        "type":"text"
                    }]
            },
        "include_processing_timelines":False
    }

    response = session.post(url=url, headers=headers, json=data)
    try:
        return response.json()
    except Exception as error:
        return error 


if __name__ == "__main__":
    # Authentication
    csrf_token = authentication()

    # Get sketches
    #list_sketches()

    # Get Starred events
    starredEvents = get_starred_events(csrf_token, TIMESKETCH_SKETCH_ID, TIMESKETCH_MAX_EVENTS_RETRIEVED)

    # DEBUG / Print Starred Events
    for event in starredEvents['objects']:
        #print(f"{event} \n")
        print(f"{event['_source']['datetime']}:  {event['_source']['message']} / Comment: {event['_source']['comment']}\n")

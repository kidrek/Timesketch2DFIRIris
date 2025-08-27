from datetime import datetime
import json
import requests
import iris_api


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

    response = session.post(url=url, headers=headers, json=data)
    try:
        return response.json()
    except Exception as error:
        return error 


if __name__ == "__main__":

    ## DFIR IRIS
    # Get all old timesketch starred events stored in IRIS Timeline
    filter = {"tag":["timesketch_starred_events"]}
    events = iris_api.get_timesketch_events(filter)
    events = json.loads(events)

    # Remove all old timesketch starred events stored in IRIS Timeline to prevent dupplicated events
    eventsIDs = iris_api.get_eventId_from_timeline_events(events['data']['timeline'])
    for eventID in eventsIDs:
        iris_api.delete_event(eventID)


    ## TIMESKETCH
    # Authentication
    csrf_token = authentication()

    # Get Starred events
    starredEvents = get_starred_events(csrf_token, TIMESKETCH_SKETCH_ID, TIMESKETCH_MAX_EVENTS_RETRIEVED)

    # DEBUG / Print Starred Events
    for event in starredEvents['objects']:
        print(f"{event} \n")


        # Parser la date ISO avec timezone
        dt = datetime.fromisoformat(event['_source']['datetime'])
        # Supprimer la timezone et reformater avec microsecondes
        formatted_date = dt.replace(tzinfo=None).isoformat()

        message = f"Commentaire de l'analyste : {event['_source']['comment']} \n\n --- \n {event['_source']['message']}"
        try: title = f"[{event['_source']['data_type']}] {event['_source']['message'][:40]}..." 
        except : title = f"{event['_source']['message'][:40]}..."

        iris_api.add_event(formatted_date, title, message, event['_source']['message'], [])
        #print(f"{event['_source']['datetime']}:  {event['_source']['message']} / Comment: {event['_source']['comment']}\n")

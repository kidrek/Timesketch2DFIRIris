import requests
from datetime import datetime


IRIS_CASE_ID = 1
IRIS_API_URL = "https://127.0.0.1:7443/"
IRIS_API_TOKEN = ""

HEADERS = {
    "Authorization": f"Bearer {IRIS_API_TOKEN}",
    "Content-Type": "application/json",
}

def add_event():
    url = f"{IRIS_API_URL}/case/timeline/events/add?cid={IRIS_CASE_ID}"
    data = {
    "event_title": "An event",
    "event_raw": "",
    "event_source": "Timesketch",
    "event_assets": [],
    "event_iocs": [],
    "event_category_id": "5",
    "event_in_summary": True,
    "event_in_graph": True,
    "event_color": "#1572E899",
    "event_date": "2025-08-11T09:23:13.135674",
    "event_sync_iocs_assets": True,
    "event_tags": "timesketch_starred_events",
    "event_tz": "+00:00",
    "event_content": "",
    "parent_event_id": None,
    "custom_attributes": {}
    }

    response = requests.post(url, json=data, headers=HEADERS, verify=False)
    print(response.text)

def delete_event(eventID):
    url = f"{IRIS_API_URL}/case/timeline/events/delete/{eventID}?cid={IRIS_CASE_ID}"
    response = requests.post(url, headers=HEADERS, verify=False)
    print(response.text)

def get_timesketch_events(filter):
    url = f"{IRIS_API_URL}/case/timeline/advanced-filter?cid={IRIS_CASE_ID}&q={json.dumps(filter)}"
    response = requests.get(url=url, headers=HEADERS, verify=False)
    return response.text

def get_eventId_from_timeline_events(timeline):
    eventsIDs = []
    for event in timeline:
        eventsIDs.append(event['event_id'])
    return eventsIDs


def get_timesketch_events(filter):
    url = f"{IRIS_API_URL}/case/timeline/advanced-filter?cid={IRIS_CASE_ID}&q={json.dumps(filter)}"
    response = requests.get(url=url, headers=HEADERS, verify=False)
    return response.text

def get_eventId_from_timeline_events(timeline):
    eventsIDs = []
    for event in timeline:
        eventsIDs.append(event['event_id'])
    return eventsIDs


if __name__ == "__main__":

    # Get all old timesketch starred events stored in IRIS Timeline
    filter = {"tag":["timesketch_starred_events"]}
    events = get_timesketch_events(filter)
    events = json.loads(events)

    # Remove all old timesketch starred events stored in IRIS Timeline to prevent dupplicated events
    eventsIDs = get_eventId_from_timeline_events(events['data']['timeline'])
    for eventID in eventsIDs:
        delete_event(eventID)

    # Add events from Timesketch with Starred tags
    add_event()


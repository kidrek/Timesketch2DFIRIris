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


## Error in filter
def get_timesketch_events():
    filter = "{tag:[timesketch_starred_events]}"
    url = f"{IRIS_API_URL}/case/timeline/advanced-filter?cid={IRIS_CASE_ID}&q={filter}"
    response = requests.get(url=url, headers=HEADERS, verify=False)
    print(response.text)


#add_event()
get_timesketch_events()

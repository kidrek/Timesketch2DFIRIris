import requests
from datetime import datetime
import json


class irisAPI:
    def __init__(self, url, token):
        self.url = url
        self.token = token
        self.session = requests.Session()

        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }


    def delete_event(self, caseID, eventID):
        url = f"{self.url}/case/timeline/events/delete/{eventID}?cid={caseID}"
        response = self.session.post(url, headers=self.headers, verify=False)
        print(response.text)


    def add_event(self, caseID, date, title = 'Event title', message = '', raw_message = '', assets = []):
        url = f"{self.url}/case/timeline/events/add?cid={caseID}"
        data = {
        "event_title": title,
        "event_raw": raw_message,
        "event_source": "Timesketch",
        "event_assets": assets,
        "event_iocs": [],
        "event_category_id": "5",
        "event_in_summary": True,
        "event_in_graph": True,
        "event_color": "#1572E899",
        "event_date": date,
        "event_sync_iocs_assets": True,
        "event_tags": "timesketch_starred_events",
        "event_tz": "+00:00",
        "event_content": message,
        "parent_event_id": None,
        "custom_attributes": {}
        }

        response = self.session.post(url, json=data, headers=self.headers, verify=False)
        print(response.text)


    def get_timesketch_events(self, caseID, filter):
        url = f"{self.url}/case/timeline/advanced-filter?cid={caseID}&q={json.dumps(filter)}"
        response = self.session.get(url=url, headers=self.headers, verify=False)
        return response.text

    def get_eventId_from_timeline_events(self, timeline):
        eventsIDs = []
        for event in timeline:
            eventsIDs.append(event['event_id'])
        return eventsIDs


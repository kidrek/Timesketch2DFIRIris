import timesketch_api
import iris_api
import secrets

import argparse
from datetime import datetime
import json


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Transferer les événements d'une timeline présente sur Timesketch vers la solution DFIR IRIS")
    parser.add_argument("--ts_sketch_id", type=int, help="Timesketch sketch id")
    parser.add_argument("--iris_case_id", type=int, help="DFIR IRIS case id")
    args = parser.parse_args()

    if args.ts_sketch_id is None or args.iris_case_id is None:
        print("⚠️  Spécifier les arguments attendus ts_sketch_id et iris_case_id")
        print("usage : python timesketch2iris.py --ts_sketch_id 2 --iris_case_id 1")
        exit(1)

    ## DFIR IRIS
    iris = iris_api.irisAPI(secrets.IRIS_API_URL, secrets.IRIS_API_TOKEN)
    # Get all old timesketch starred events stored in IRIS Timeline
    filter = {"tag":["timesketch_starred_events"]}
    events = iris.get_timesketch_events(args.iris_case_id, filter)
    events = json.loads(events)

    # Remove all old timesketch starred events stored in IRIS Timeline to prevent dupplicated events
    eventsIDs = iris.get_eventId_from_timeline_events(events['data']['timeline'])
    for eventID in eventsIDs:
        iris.delete_event(args.iris_case_id, eventID)


    ## TIMESKETCH
    timesketch = timesketch_api.timesketchAPI(secrets.TIMESKETCH_URL, secrets.TIMESKETCH_USERNAME, secrets.TIMESKETCH_PASSWORD)

    # Get Starred events
    starredEvents = timesketch.get_starred_events(args.ts_sketch_id, secrets.TIMESKETCH_MAX_EVENTS_RETRIEVED)

    for event in starredEvents['objects']:
        # DEBUG / Print Starred Events
        #print(f"{event} \n")

        # Parser la date ISO avec timezone
        dt = datetime.fromisoformat(event['_source']['datetime'])
        # Supprimer la timezone et reformater avec microsecondes
        formatted_date = dt.replace(tzinfo=None).isoformat()

        message = f"Commentaire de l'analyste : {event['_source']['comment']} \n\n --- \n {event['_source']['message']}"
        try: title = f"[{event['_source']['data_type']}] {event['_source']['message'][:40]}..." 
        except : title = f"{event['_source']['message'][:40]}..."

        iris.add_event(args.iris_case_id, formatted_date, title, message, event['_source']['message'], [])
        #print(f"{event['_source']['datetime']}:  {event['_source']['message']} / Comment: {event['_source']['comment']}\n")

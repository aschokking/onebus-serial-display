import os
from os.path import abspath
import requests
try:
    import urlparse as parse
except:
    import urllib.parse as parse
import urllib
import datetime
import json
from collections import defaultdict
# don't tell me about anything less than this since I won't be able to make it anyway
min_arrival_time = 60 * 3
max_arrivals = 3

key = os.getenv('oba_key')
base_url = 'http://api.pugetsound.onebusaway.org/api/'

arrivals_base_url = 'where/arrivals-and-departures-for-stop/%s.json'

def get_url(api, params=None):
    url = parse.urljoin(base_url, api) + ("?key=%s" % key)
    if params:
        url = url + "&" + params
    return url

def dt_for_ms_ts(ts):
    return datetime.datetime.fromtimestamp(ts / 1000)

def seconds_away(dt):
    return (dt - datetime.datetime.now()).total_seconds()

def get_arrival_times_for(records):
    result = []
    for record in records:
        in_s, is_predicted = get_arrival_time(record)
        if in_s > min_arrival_time:
            result.append({'in_s': in_s, 'is_predicted': is_predicted})
    return result[:max_arrivals]

def get_arrival_time(arrival_record):
    if arrival_record['predictedArrivalTime']:
        return seconds_away(dt_for_ms_ts(arrival_record['predictedArrivalTime'])), True
    else:
        return seconds_away(dt_for_ms_ts(arrival_record['scheduledArrivalTime'])), False
    
def get_arrival_times():
    result = {}
    stops_path = os.path.join(os.path.dirname(__file__), 'stops.json')
    stops = json.load(open(stops_path))['stops']

    for stop in stops:
        arrivals_url = get_url(arrivals_base_url % stop['id'])
        arrivals_data = requests.get(arrivals_url).json()['data']['entry']['arrivalsAndDepartures']
        if 'route_ids' in stop:
            # filter to selected route ids only
            arrivals_data = [entry for entry in arrivals_data if
                             entry['routeId'] in stop['route_ids']]
        result[stop['label']] = get_arrival_times_for(arrivals_data)
    
    return result


def get_display_rows(arrival_times):
    rows = []
    for route, arrivals in arrival_times.items():
        row = "{}: ".format(route)
        row += " ".join([get_display_for_arrival(arrival) for arrival in arrivals])
        rows.append(row)
    return rows

def get_display_for_arrival(arrival):
    min_away = arrival['in_s'] / 60.0
    if min_away < 6:
        in_min = "{:0.1f}".format(min_away)
    else:
        in_min = "{:0.0f}".format(min_away)
    if arrival['is_predicted']:
        return in_min
    else:
        return "{}*".format(in_min)
    

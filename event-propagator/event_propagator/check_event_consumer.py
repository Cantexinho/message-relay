"""
    Script used to check the availability of event-consumer api,
    as it fully starts after event-propagator sends first request
"""

import time
import requests

service1_url = "http://event-consumer:8000/ready/"

while True:
    try:
        response = requests.get(service1_url)
        if response.status_code == 200:
            break
    except requests.exceptions.ConnectionError:
        pass
    print("Waiting for service1 to be available...")
    time.sleep(5)

print("Service1 is up and running!")

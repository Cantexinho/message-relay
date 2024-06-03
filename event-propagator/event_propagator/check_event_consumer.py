"""
    Script used to check the availability of event-consumer api,
    as it fully starts after event-propagator sends first request
"""

import time
import requests


# REVIEW COMMENT:
# Since you're using pydantic settings, it would be cleaner to define this URL there.
# Also, we could define the consumer url separately and just construct /event and /ready endpoints from it as well.
service1_url = "http://event-consumer:8000/ready/"

while True:
    try:
        response = requests.get(service1_url)
        # REVIEW COMMENT:
        # More of a nitpick, but the `requests` response object has a method called `raise_for_status`.
        # Using it here and catching the exception would be more pythonic IMO.
        if response.status_code == 200:
            break
    except requests.exceptions.ConnectionError:
        pass
    print("Waiting for service1 to be available...")
    time.sleep(5)

print("Service1 is up and running!")

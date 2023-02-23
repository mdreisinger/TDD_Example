"""
Function that utilizes pythons request library to hit an API.
Uses logic to determine if API is healthy or unhealthy based on
the given requirements for the request response.
"""

import requests


def get(url):
    """
    Basic method that uses requests.get() to hit the url.
    Returns False if status_code is not 200, or status is not OK.
    Returns True otherwise.
    """

    try:
        response = requests.get(url, timeout=10)
    except Exception as error: # pylint: disable=broad-except
        print("Unable to request response from url")
        print(error)
        return False

    if response.status_code != 200:
        print(f"Failed to invoke API. Response status_code: {response.return_code}")
        return False

    try:
        json = response.json()
    except Exception as error: # pylint: disable=broad-except
        print("Response does not include json parameter.")
        print(error)
        return False

    try:
        status = json['status']
    except KeyError:
        print("json parameter of response does not include a 'status' field.")
        return False

    if status != "OK":
        return False

    print("API is up.")

    return True

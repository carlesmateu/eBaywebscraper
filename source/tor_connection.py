# tor_connection.py

import requests
from stem import Signal
from stem.control import Controller
import time

def connect_to_tor():
    """ Connect to Tor and get a new IP address """
    with Controller.from_port(port=9051) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)
        time.sleep(5)  # wait a few seconds to get a new IP
    proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
    }
    return proxies

def send_request_with_tor(url, params):
    """ Send a GET request using Tor """
    proxies = connect_to_tor()
    response = requests.get(url, params=params, proxies=proxies)
    return response

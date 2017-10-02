#!/usr/bin/env python3

import socket
import configargparse
import requests
import sys
from time import sleep
from random import randrange


p = configargparse.get_argument_parser()
p.add('--hosts', required=True, env_var='HOSTS')
p.add('--server', required=True, env_var='SERVER')

hostnames = p.parse_args().hosts.split(',')

payload_url = p.parse_args().server + "/payload"

this_host = socket.getfqdn()


def get_ips(hostname):
    try:
        result = socket.getaddrinfo(hostname, None)
    except OSError as e:
        print(e)
        return None
    output = list(set([x[4][0] for x in result]))
    output.sort()
    return output


def worker():
    payload = {}
    payload['this_host'] = this_host
    payload['results'] = {}
    for hostname in hostnames:
        payload['results'][hostname] = get_ips(hostname)
    try:
        r = requests.post(payload_url, json=payload)
        print(r.status_code)
    except requests.exceptions.ConnectionError as e:
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    while True:
        worker()
        sleep(randrange(1, 3))

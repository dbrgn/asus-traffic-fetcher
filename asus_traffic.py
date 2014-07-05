# -*- coding: utf-8 -*-
"""asus_traffic.py

Fetch traffic data from an Asus RT-N66U router web interface.

Usage:
    asus_traffic.py [-i <ip>] [--tls] -u <username> -p <password>
    asus_traffic.py -h | --help
    asus_traffic.py -v | --version

Options:
    -h --help      Show this screen.
    -v --version   Show version.
    -i <ip>        The router IP address [default: 192.168.1.1].
    --tls          Use HTTPS on port 8443.
    -u <username>  The router username.
    -p <password>  The router password.

"""
from __future__ import print_function, division, absolute_import, unicode_literals

import re
from datetime import date

import docopt
import requests
from requests.auth import HTTPBasicAuth


class TrafficDay(object):

    def __init__(self, triple):
        self.triple = triple

    @property
    def date(self):
        ymd = get_ymd(self.triple[0])
        return ymd

    @property
    def rx(self):
        return self.triple[1]

    @property
    def tx(self):
        return self.triple[2]

    @property
    def total(self):
        return self.rx + self.tx

    def __repr__(self):
        return '(day=%s, rx=%s, tx=%s)' % (self.date, self.rx, self.tx)


def fetch_html(username, password, ip, tls=False):
    if tls:
        url_base = 'https://%s:8443' % ip
    else:
        url_base = 'http://%s' % ip

    # URL definitions
    url_data = url_base + '/Main_TrafficMonitor_daily.asp'
    url_logout = url_base + '/Logout.asp'

    # Authentication object
    auth = HTTPBasicAuth(username, password)

    # Get session
    requests.get(url_base, auth=auth, verify=False)

    # Fetch data
    r = requests.get(url_data, auth=auth, verify=False)

    # Log out
    requests.get(url_logout, auth=auth, verify=False)

    # Return data
    r.raise_for_status()
    return r.text


def parse_html(html):
    # Get list string from HTML
    re_mode = re.IGNORECASE | re.DOTALL
    matches = re.search(r'daily_history\s*=\s*\[(.*?)\];', html, re_mode)
    if not matches:
        return
    data = matches.groups()[0].strip()

    # Make sure only safe characters are contained
    safe_data = ''.join(c for c in data if c.isalnum() or c in '[], ')

    # Convert string to Python list
    return eval(safe_data)


def get_ymd(value):
    """
    Parse some obscure fucked-up date format used by Asus.

    The return value is a date object.

    """
    year = ((value >> 16) & 0xff) % 100 + 2000
    month = ((value >> 8) & 0xff) + 1
    day = value & 0xff

    return date(year, month, day)


if __name__ == '__main__':
    arguments = docopt.docopt(__doc__, version='asus_traffic.py 0.1')

    username = arguments['-u']
    password = arguments['-p']
    ip = arguments['-i']
    tls = arguments['--tls']

    html = fetch_html(username, password, ip, tls)
    data = parse_html(html)

    days = []
    for item in data:
        days.append(TrafficDay(item))

    print('date, rx, tx, total')
    for day in days:
        if day.rx or day.tx:
            print('%s, %s, %s, %s' % (day.date.isoformat(), day.rx, day.tx, day.total))

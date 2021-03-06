ASUS Traffic Fetcher
====================

Fetch internet traffic data from the Asus RT-N66U web interface and output it
as CSV.

Requirements
------------

- Python 2 or 3
- python-requests library

Usage
-----

::

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

Example output::

    date, rx, tx, total
    2014-07-05, 1143762, 974313, 2118075

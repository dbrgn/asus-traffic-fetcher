ASUS Traffic Fetcher
====================

Fetch internet traffic data from the Asus RT-N66U web interface.

Usage::

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

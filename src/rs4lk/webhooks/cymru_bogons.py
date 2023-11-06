import ipaddress
import os.path

import requests
from dateutil.parser import parse as parsedate

from ..globals import RESOURCES_FOLDER


class CymruBogons:
    V4_BOGONS: str = 'https://team-cymru.org/Services/Bogons/fullbogons-ipv4.txt'
    V6_BOGONS: str = 'https://team-cymru.org/Services/Bogons/fullbogons-ipv6.txt'

    V4_FILE_PATH: str = os.path.join(RESOURCES_FOLDER, 'bogons-ipv4.txt')
    V6_FILE_PATH: str = os.path.join(RESOURCES_FOLDER, 'bogons-ipv6.txt')

    __slots__ = ['_bogons']

    def __init__(self):
        self._bogons: set[ipaddress.IPv4Network | ipaddress.IPv6Network] = set()
        self._init()

    def _init(self) -> None:
        self._download_if_newer(self.V4_BOGONS, self.V4_FILE_PATH)
        self._download_if_newer(self.V6_BOGONS, self.V6_FILE_PATH)

        self._parse_and_add()

    def _download_if_newer(self, url: str, cache_file: str) -> None:
        if not os.path.exists(cache_file):
            self._write_cache_file(url, cache_file)
            return

        r = requests.head(url)
        r.raise_for_status()
        last_modified = parsedate(r.headers['last-modified'])

        with open(cache_file, 'r') as bogons_file:
            content = bogons_file.readlines()

        date_line = content[0].split(' ')
        file_date = int(date_line[3]) + 1

        if last_modified.timestamp() > file_date:
            self._write_cache_file(url, cache_file)

    @staticmethod
    def _write_cache_file(url: str, path: str) -> None:
        r = requests.get(url)
        r.raise_for_status()
        with open(path, 'w') as bogons_file:
            bogons_file.write(r.text)

    def _parse_and_add(self) -> None:
        lines = []

        with open(self.V4_FILE_PATH, 'r') as v4_bogons:
            lines.extend(v4_bogons.readlines())

        with open(self.V6_FILE_PATH, 'r') as v6_bogons:
            lines.extend(v6_bogons.readlines())

        for line in lines:
            if line.startswith('#'):
                continue
            try:
                self._bogons.add(ipaddress.ip_network(line.strip()))
            except ValueError:
                pass

    def is_network_bogon(self, net: ipaddress.IPv4Network | ipaddress.IPv6Network) -> bool:
        return net in self._bogons

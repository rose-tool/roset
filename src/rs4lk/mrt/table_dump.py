from __future__ import annotations

import ipaddress
import logging
import os
import sqlite3
from functools import lru_cache

from ..model.rib import RibEntry


class TableDump:
    __slots__ = ['conn']

    def __init__(self, path: str) -> None:
        if not os.path.exists(path):
            raise FileNotFoundError(f"File `{path}` not found.")

        logging.info(f"Loading MRT Table Dump in file `{path}`...")
        self.conn: sqlite3.Connection = sqlite3.connect(path)

    def close(self):
        self.conn.close()

    def get_by_network(self, network: ipaddress.IPv4Network | ipaddress.IPv6Network) -> list[RibEntry]:
        return self._execute_query("SELECT * FROM rib WHERE network = ?", (str(network),))

    def get_by_peer_as(self, peer_as: int) -> list[RibEntry]:
        return self._execute_query("SELECT * FROM rib WHERE peer_as = ?", (peer_as,))

    def get_by_as_origin(self, as_origin: int) -> list[RibEntry]:
        return self._execute_query("SELECT * FROM rib WHERE as_path LIKE ?", (f"%{as_origin}]%",))

    def get_by_traversed_as(self, as_origin: int) -> list[RibEntry]:
        return self._execute_query("SELECT * FROM rib WHERE as_path LIKE ?", (f"%{as_origin}%",))

    def _execute_query(self, query: str, params: tuple | None) -> list[RibEntry]:
        query = self.conn.execute(query, params)
        raw_result = query.fetchall()
        return [self._to_rib_entry(*x) for x in raw_result]

    @lru_cache
    def _to_rib_entry(self, peer_as: int, network: str, as_path: str) -> RibEntry:
        return RibEntry(peer_as, network, as_path)

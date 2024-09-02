import base64
import hashlib
import re


# General Helpers
def urlsafe_hash(string: str) -> str:
    string = re.sub(r'[^\x00-\x7F]+', '', string)
    return base64.urlsafe_b64encode(hashlib.md5(string.encode('utf-8', errors='ignore')).digest())[:-2] \
        .decode('utf-8') \
        .replace('-', '').replace('_', '')


# Network IP Helpers
def aggregate_v4_6_networks(nets: dict[int, set]) -> None:
    for v, networks in nets.items():
        nets[v] = aggregate_networks(networks)


def aggregate_networks(networks: set) -> set:
    aggregated_networks = set(networks)
    for network in networks:
        for prefix in range(network.prefixlen - 1, 0, -1):
            super_network = network.supernet(new_prefix=prefix)
            if super_network in aggregated_networks and network in aggregated_networks:
                aggregated_networks.remove(network)

    return aggregated_networks

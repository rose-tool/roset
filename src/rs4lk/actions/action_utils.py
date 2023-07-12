from __future__ import annotations

import ipaddress
import json
import logging
import random
import secrets
import shlex

from Kathara.manager.Kathara import Kathara
from Kathara.model.Machine import Machine


def get_bgp_networks(device: Machine) -> dict[int, set]:
    device_networks = {4: set(), 6: set()}

    exec_output = Kathara.get_instance().exec(
        machine_name=device.name,
        command=shlex.split(f"vtysh -c 'show ip bgp json'"),
        lab_name=device.lab.name
    )
    ipv4_bgp_nets = ""
    try:
        while True:
            (stdout, _) = next(exec_output)
            stdout = stdout.decode('utf-8') if stdout else ""

            if stdout:
                ipv4_bgp_nets += stdout
    except StopIteration:
        pass
    ipv4_bgp_nets = json.loads(ipv4_bgp_nets)
    device_networks[4] = {ipaddress.ip_network(net) for net in ipv4_bgp_nets['routes'].keys()}

    exec_output = Kathara.get_instance().exec(
        machine_name=device.name,
        command=shlex.split("vtysh -c 'show ipv6 route bgp json'"),
        lab_name=device.lab.name
    )
    ipv6_bgp_nets = ""
    try:
        while True:
            (stdout, _) = next(exec_output)
            stdout = stdout.decode('utf-8') if stdout else ""

            if stdout:
                ipv6_bgp_nets += stdout
    except StopIteration:
        pass
    ipv6_bgp_nets = json.loads(ipv6_bgp_nets)
    device_networks[6] = {ipaddress.ip_network(net) for net in ipv6_bgp_nets.keys()}

    return device_networks


def get_neighbour_bgp_networks(device: Machine,
                               neighbour_ip: ipaddress.IPv4Address | ipaddress.IPv6Address) -> set:
    command = f"vtysh -c 'show bgp ipv{neighbour_ip.version} neighbors {neighbour_ip} routes json'"

    exec_output = Kathara.get_instance().exec(
        machine_name=device.name,
        command=shlex.split(command),
        lab_name=device.lab.name
    )
    bgp_nets = ""
    try:
        while True:
            (stdout, _) = next(exec_output)
            stdout = stdout.decode('utf-8') if stdout else ""

            if stdout:
                bgp_nets += stdout
    except StopIteration:
        pass
    bgp_nets = json.loads(bgp_nets)

    return {ipaddress.ip_network(net) for net in bgp_nets['routes'].keys()}


def get_non_overlapping_network(v: int, networks: set) -> ipaddress.IPv4Network | ipaddress.IPv6Network:
    n_bytes = 4 if v == 4 else 16
    # For IPv4: It is a good practice to reject routes below /24
    # For IPv6: It is a good practice to reject routes below /48
    lower_prefixlen = 24 if v == 4 else 48
    higher_prefixlen = 8 if v == 4 else 3

    while True:
        random_bytes = secrets.token_bytes(n_bytes) if v == 4 else b"\x20\x00" + secrets.token_bytes(n_bytes - 2)
        prefixlen = random.randint(higher_prefixlen, lower_prefixlen)
        random_network = ipaddress.IPv4Network((random_bytes, prefixlen), strict=False) if v == 4 else \
            ipaddress.IPv6Network((random_bytes, prefixlen), strict=False)

        logging.info(f"Generated random network: {random_network}.")

        regenerate = False
        for network in networks:
            if network.overlaps(random_network):
                logging.warning(f"Network overlapping with {network}, regenerating...")
                regenerate = True
                break

        # Check if any of the flags is active
        if not regenerate and random_network.is_multicast:
            logging.warning(f"{random_network} is multicast, regenerating.")
            regenerate = True
        if not regenerate and random_network.is_private:
            logging.warning(f"{random_network} is private, regenerating.")
            regenerate = True
        if not regenerate and random_network.is_unspecified:
            logging.warning(f"{random_network} is unspecified, regenerating.")
            regenerate = True
        if not regenerate and random_network.is_reserved:
            logging.warning(f"{random_network} is reserved, regenerating.")
            regenerate = True
        if not regenerate and random_network.is_loopback:
            logging.warning(f"{random_network} is loopback, regenerating.")
            regenerate = True
        if not regenerate and random_network.is_link_local:
            logging.warning(f"{random_network} is link local, regenerating.")
            regenerate = True
        if not regenerate and v == 6 and random_network.is_site_local:
            logging.warning(f"{random_network} is site local, regenerating.")
            regenerate = True

        # The network is good, return it
        if not regenerate:
            break

    return random_network

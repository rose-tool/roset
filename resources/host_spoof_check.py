import argparse
import logging

from scapy.all import sr1
from scapy.layers.inet import IP, ICMP
from scapy.layers.inet6 import IPv6, ICMPv6EchoRequest

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)


def send(src_ip: str, dst_ip: str, version: int) -> bool:
    if version == 4:
        return sr1(IP(src=src_ip, dst=dst_ip, ttl=255) / ICMP(), iface="eth0", timeout=5, verbose=0)
    elif version == 6:
        return sr1(IPv6(src=src_ip, dst=dst_ip, hlim=255) / ICMPv6EchoRequest(), iface="eth0", timeout=5, verbose=0)
    else:
        return False


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('candidate_ip', nargs=1, type=str)
    parser.add_argument('spoofed_ip', nargs=1, type=str)
    parser.add_argument('dst_ip', nargs=1, type=str)
    parser.add_argument('version', nargs=1, type=int)

    return parser.parse_args()


def main(args):
    candidate_ip = args.candidate_ip.pop()
    spoofed_ip = args.spoofed_ip.pop()
    dst_ip = args.dst_ip.pop()
    version = args.version.pop()

    responses = []

    response = send(candidate_ip, dst_ip, version)
    responses.append(response is not None)

    response = send(spoofed_ip, dst_ip, version)
    responses.append(response is None)

    print(int(all(responses)))
    exit(0)


if __name__ == "__main__":
    main(parse_args())

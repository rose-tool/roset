import argparse
import logging

from scapy.all import sniff

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)


def capture(src_ip: str, dst_ip: str, version: int) -> bool:
    if version == 4:
        type = "icmp"
    elif version == 6:
        type = "icmp6"
    else:
        return False

    pkts = sniff(filter=f"{type} and src {src_ip} and dst {dst_ip}", count=1, timeout=10)
    return len(pkts) == 0


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('src_ip', nargs=1, type=str)
    parser.add_argument('spoofed_ip', nargs=1, type=str)
    parser.add_argument('version', nargs=1, type=int)

    return parser.parse_args()


def main(args):
    src_ip = args.src_ip.pop()
    spoofed_ip = args.spoofed_ip.pop()
    version = args.version.pop()

    response = capture(src_ip, spoofed_ip, version)
    print(int(response))
    exit(0)


if __name__ == "__main__":
    main(parse_args())

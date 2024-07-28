import sys

from rs4lk.configuration.parser.routeros.routeros_configuration import RouterosConfiguration

if __name__ == '__main__':
    config = RouterosConfiguration(sys.argv[1])
    print("Interfaces")
    print(config.interfaces)
    print("peerings")
    print(config.peerings)
    print("local_as", config.local_as)
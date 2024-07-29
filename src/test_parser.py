import sys

from rs4lk.parser.configuration_parser import ConfigurationParser

if __name__ == '__main__':
    parser = ConfigurationParser()
    config = parser.parse(sys.argv[1], sys.argv[2])
    print("Interfaces")
    print(config.interfaces)
    print("peerings")
    print(config.peerings)
    print("local_as", config.local_as)
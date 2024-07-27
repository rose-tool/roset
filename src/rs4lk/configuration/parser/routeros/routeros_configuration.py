import ipaddress
import sys
from antlr4 import *
from RouterosLexer import RouterosLexer
from RouterosParser import RouterosParser
from antlr4.tree.Tree import TerminalNodeImpl


def parse_key_value_pair(node):
    key = str(node.children[0].children[0]).strip()
    value = str(node.children[2].children[0]).strip()
    return key, value


class RouterosConfiguration:
    def __init__(self, config_path: str):
        self._config_path = config_path
        input_stream = FileStream(config_path)
        lexer = RouterosLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = RouterosParser(stream)
        tree = parser.config()
        self.interfaces: dict[str, dict] = {}
        self.peerings: list[dict] = []
        self.local_as = None
        self.rule_names = parser.ruleNames
        self.parse_tree(tree)

    def parse_tree(self, tree):
        if isinstance(tree, TerminalNodeImpl):
            pass
        else:
            rule_name = self.rule_names[tree.getRuleIndex()]
            if rule_name == "interfaceName":
                self.parse_interface_name(tree.children.pop())
            elif rule_name == "vlanConfig":
                self.parse_vlan_config(tree)
            elif rule_name == "ipv4Config":
                self.parse_ip_config(tree)
            elif rule_name == "ipv6Config":
                self.parse_ip_config(tree)
            elif rule_name == "bgpPeeringConfig":
                self.parse_bgp_peering_config(tree)
            else:
                for child in tree.children:
                    self.parse_tree(child)

    def parse_interface_name(self, node):
        if isinstance(node, TerminalNodeImpl):
            self.interfaces[str(node)] = {}

    def parse_vlan_config(self, node):
        interface = None
        vlan_name = None
        vlan_id = None
        for child in node.children:
            if isinstance(child, TerminalNodeImpl):
                continue
            rule_name = self.rule_names[child.getRuleIndex()]
            if rule_name == "keyValuePair":
                key, value = parse_key_value_pair(child)
                if key == "interface":
                    interface = value
                if key == "name":
                    vlan_name = value
                if key == "vlan-id":
                    vlan_id = int(value)
        self.interfaces[vlan_name] = {
            "interface": interface,
            "vlan_id": vlan_id
        }

    def parse_ip_config(self, node):
        interface = None
        address = None
        for child in node.children:
            if isinstance(child, TerminalNodeImpl):
                continue
            rule_name = self.rule_names[child.getRuleIndex()]
            if rule_name == "keyValuePair":
                key, value = parse_key_value_pair(child)
                if key == "interface":
                    interface = value
                if key == "address":
                    address = ipaddress.ip_network(value, strict=False)
        if interface not in self.interfaces:
            self.interfaces[interface] = {}
        ip_ver = f"ipv{address.version}"
        if ip_ver not in self.interfaces[interface]:
            self.interfaces[interface][ip_ver] = []
        self.interfaces[interface][ip_ver].append(address)

    def parse_bgp_peering_config(self, node):
        remote_as = None
        local_ip = None
        remote_ip = None
        role = None
        address = None

        for child in node.children:
            if isinstance(child, TerminalNodeImpl):
                continue
            else:
                rule_name = self.rule_names[child.getRuleIndex()]
                if rule_name == "keyValuePair":
                    key, value = parse_key_value_pair(child)

                    if key == "local.address":
                        local_ip = ipaddress.ip_network(value, strict=False)
                    if key == "remote.address":
                        remote_ip = ipaddress.ip_network(value, strict=False)
                    if key == "as":
                        self.local_as = int(value)
                    if key == ".as":
                        remote_as = int(value)
                    if key == ".role":
                        role = value
        if role != "ebgp":
            return
        if remote_as and local_ip and remote_ip:
            self.peerings.append({
                'remote_as': remote_as,
                'local_ip': local_ip,
                'remote_ip': remote_ip,
            })





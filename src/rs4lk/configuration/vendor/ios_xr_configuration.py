import ipaddress
import json
import logging
import os
import tempfile
import re
from typing import Any

from Kathara.model.Lab import Lab
from cisco_config_parser.cisco_config_parser import ConfigParser

from ...foundation.configuration.vendor_configuration import VendorConfiguration
from ...foundation.exceptions import ConfigError
from ...model.bgp_session import BgpSession


class IosXrConfiguration(VendorConfiguration):
    __slots__ = ['_cisco_parser']

    CONFIG_FILE_PATH: str = "disk0:/startup-config.cfg"

    CLI_COMMAND: str = "/pkg/bin/xr_cli \"{command}\""
    ZTP_CLI_COMMAND: str = "/bin/bash -c 'source /pkg/bin/ztp_helper.sh; xrcmd \"{command}\"'"
    ZTP_APPLY_COMMAND: str = "/bin/bash -c 'source /pkg/bin/ztp_helper.sh; xrapply {file}'"
    ZTP_DIFF_APPLY_COMMAND: str = "/bin/bash -c 'source /pkg/bin/ztp_helper.sh; xrapply_string \"{command}\"'"

    PREFIX_REGEX: re.Pattern = re.compile(
        r"((\s*((([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}"
        r"([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))/\d+\s*)|"
        r"(\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|"
        r"(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)"
        r"(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|"
        r":((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}"
        r"(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)"
        r"(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|"
        r"((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|"
        r"(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:"
        r"((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}"
        r"(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)"
        r"(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|"
        r"((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))"
        r"(%.+)?/\d+\s*))"
    )

    def _init(self) -> None:
        # Cisco Parser needs a txt file, create a temporary one and read it back
        (fd, temp_file_path) = tempfile.mkstemp(suffix='.txt')
        with open(temp_file_path, 'w') as temp_file:
            temp_file.writelines(self._lines)
        self._cisco_parser: ConfigParser = ConfigParser(method="file", content=temp_file_path)

        self._parse_ipv6_interface_addresses()
        self._parse_ipv6_sessions()
        self._remap_interfaces()

        os.remove(temp_file_path)

    def _parse_ipv6_interface_addresses(self) -> None:
        logging.info("Inferring IPv6 interface addresses.")

        ipv6_addrs = {}
        for iface_block in self._cisco_parser.find_parent_child("^interface"):
            (_, iface_name) = iface_block.parent.split('interface ')
            iface_name = iface_name.strip()

            for child in iface_block.child:
                if 'ipv6 address' in child:
                    (_, addr_part) = child.split('ipv6 address ')
                    addr = ipaddress.IPv6Interface(addr_part)

                    if iface_name not in ipv6_addrs:
                        ipv6_addrs[iface_name] = set()

                    ipv6_addrs[iface_name].add(addr)

        for iface_name, addrs in ipv6_addrs.items():
            self.interfaces[iface_name]['All_Prefixes'].extend(addrs)

        logging.debug(f"Resulting interfaces: {self.interfaces}")

    def _parse_ipv6_sessions(self) -> None:
        logging.info("Inferring IPv6 BGP sessions.")

        local_as = self.get_local_as()

        router_bgp_block = self._cisco_parser.find_parent_child("^router bgp").pop(0)

        ipv6_bgp_sessions = []
        last_neighbor_idx = -1
        for child in router_bgp_block.child:
            if 'neighbor' in child:
                ipv6_bgp_sessions.append({'local_as': local_as, 'is_v6': True})
                last_neighbor_idx += 1

                (_, str_addr) = child.split('neighbor ')
                try:
                    addr = ipaddress.IPv6Address(str_addr)
                except ipaddress.AddressValueError:
                    ipv6_bgp_sessions[last_neighbor_idx]['is_v6'] = False
                    continue

                ipv6_bgp_sessions[last_neighbor_idx]['remote_ip'] = addr
            elif 'remote-as' in child:
                (_, str_peer) = child.split('remote-as ')
                peer = int(str_peer)

                ipv6_bgp_sessions[last_neighbor_idx]['remote_as'] = peer

        # Filter out non-valid sessions
        ipv6_bgp_sessions = filter(
            lambda x: 'remote_as' in x and x['is_v6'] and
                      self._batfish_config.is_valid_session(x['local_as'], x['remote_as']),
            ipv6_bgp_sessions
        )

        for session in ipv6_bgp_sessions:
            remote_as = session['remote_as']

            if remote_as not in self.bgp_sessions:
                self.bgp_sessions[remote_as] = BgpSession(local_as, remote_as)

            self.bgp_sessions[remote_as].add_peering(None, session['remote_ip'], None)

        logging.debug(f"Resulting sessions: {self.bgp_sessions}")

    def _get_bgp_local_as_vendor(self) -> int:
        router_bgp_blocks = self._cisco_parser.find_parent_child("^router bgp")
        if not router_bgp_blocks:
            raise ConfigError("Cannot find local AS value")

        (_, as_str) = router_bgp_blocks.pop().parent.split('router bgp ')
        return int(as_str)

    def _remap_interfaces(self) -> None:
        last_iface_idx = [-1]
        for iface in self.interfaces.values():
            self._remap_interface(iface, last_iface_idx)

    def _remap_interface(self, iface: dict, last_iface_idx: list[int]) -> None:
        iface_name = iface['Interface']['interface']
        if '/' not in iface_name:
            return

        iface_type, unit, slot, num, vlan = self._parse_iface_format(iface['Interface']['interface'])
        if vlan is None:
            last_iface_idx[0] += 1

        # IOS XR container requires all interfaces to be "GigabitEthernet0", in unit 0, and slot 0
        iface['Interface']['vendor_interface'] = iface['Interface']['interface']
        iface['Interface']['interface'] = self._build_iface_name(
            "GigabitEthernet0", 0, 0, last_iface_idx[0], vlan
        )

        self.iface_to_iface_idx[iface['Interface']['interface']] = last_iface_idx[0]

        logging.debug(f"Interface `{iface['Interface']['vendor_interface']}` "
                      f"remapped into `{iface['Interface']['interface']}`.")

    def _on_load_complete(self) -> None:
        for session in self.bgp_sessions.values():
            if session.iface:
                _, _, _, num, vlan = self._parse_iface_format(session.iface)

                session.iface_idx = num
                session.vlan = vlan

    def get_image(self) -> str:
        return 'ios-xr/xrd-control-plane:7.9.2'

    def apply_to_network_scenario(self, net_scenario: Lab) -> None:
        net_scenario.add_option('privileged_machines', True)

        candidate_name = f"as{self.get_local_as()}"
        candidate_router = net_scenario.get_machine(candidate_name)
        candidate_router.add_meta('image', self.get_image())
        candidate_router.add_meta('ipv6', True)

        env_ifaces = []
        for iface_name, iface_idx in self.iface_to_iface_idx.items():
            if "." in iface_name:
                continue

            env_ifaces.append(f"linux:eth{iface_idx},xr_name={iface_name}")

        candidate_router.add_meta('env', "XR_INTERFACES=%s" % ";".join(env_ifaces))
        candidate_router.add_meta('env', "XR_ZTP_ENABLE=0")

        all_lines = "\n".join(self.get_lines())
        candidate_router.create_file_from_string(all_lines, self.CONFIG_FILE_PATH)

        # Apply custom configuration after the container has started
        # We use CLI_COMMAND instead of ZTP since ZTP is still not initialized at this point.
        check_cmd_1 = (self.CLI_COMMAND.format(command="show run") +
                       " | egrep -e 'No configuration change' -e 'No such file or directory'")
        check_cmd_2 = (self.CLI_COMMAND.format(command="sh ip interface GigabitEthernet0/0/0/0") +
                       " | egrep -e 'ipv4 protocol is Down'")
        check_cmd_3 = (self.CLI_COMMAND.format(command="sh ipv6 interface GigabitEthernet0/0/0/0") +
                       " | egrep -e 'ipv6 protocol is Down'")
        net_scenario.create_file_from_list(
            [
                # Wait that xrd-startup finishes
                "pgrep xrd-startup; while [[ $? -eq 0 ]]; do sleep 3; pgrep xrd-startup; done",
                # Check when the control plane is ready
                check_cmd_1,
                f"while [[ $? -eq 0 ]]; do sleep 3; {check_cmd_1}; done",
                # Check when the IPv4 stack goes up
                check_cmd_2,
                f"while [[ $? -eq 0 ]]; do sleep 3; {check_cmd_2}; done",
                # Check when the IPv6 stack goes up
                check_cmd_3,
                f"while [[ $? -eq 0 ]]; do sleep 3; {check_cmd_3}; done",
                # Kill ZTP (it removes the IPs from the interfaces)!
                "source /pkg/bin/ztp_helper.sh; ztp_disable; ztp_kill_all; killall -9 pyztp2",
                # Finally apply the configuration
                self.ZTP_APPLY_COMMAND.format(file=self.CONFIG_FILE_PATH)
            ],
            f"{candidate_name}.startup"
        )

    def get_lines(self) -> list[str]:
        all_lines = "".join(self._lines)
        for iface_name, iface in self.interfaces.items():
            if '/' not in iface_name:
                continue

            if iface['Interface']['vendor_interface'] == iface['Interface']['interface']:
                continue

            all_lines = re.sub(
                rf"\b{iface['Interface']['vendor_interface']}\b",
                iface['Interface']['interface'],
                all_lines
            )

        tmp_clean_lines = []
        for line in all_lines.split("\n"):
            # Remove easy unsupported (by XRd container) configurations
            if ('clock' in line or 'telnet' in line or 'snmp-server' in line or 'aaa' in line or
                    'service-policy type control subscriber' in line or 'pppoe enable' in line or
                    'transceiver permit' in line or
                    ('track ' in line and len(line) - len(line.lstrip(' ')) > 0)):  # track but not at root level
                continue

            tmp_clean_lines.append(line)

        # Remove multi-line unsupported (by XRd container) configurations
        start_skipping = 0
        clean_lines = []
        for line in tmp_clean_lines:
            if start_skipping > 0:
                start_skipping = len(line) - len(line.lstrip(' '))

                continue
            elif ('line console' in line or 'ntp' in line or 'dynamic-template' in line or 'l2vpn' in line or
                  'ipsla' in line or 'subscriber' in line or 'pppoe' in line or
                  'class-map type control subscriber' in line or 'policy-map type control subscriber' in line or
                  'monitor-session capture ethernet' in line or
                  ('interface' in line and ('/' not in line or 'PTP' in line)) or  # Clean virtual interfaces
                  ('interface' in line and ('GigabitEthernet0/0/0' not in line)) or  # Clean non-parsed interfaces
                  ('track ' in line and len(line) - len(line.lstrip(' ')) == 0)):  # track but at root level
                start_skipping += 1
                continue

            clean_lines.append(line)

        # Remove shutdown interfaces (if any)
        lines_to_remove = []
        for n, line in enumerate(clean_lines):
            if 'shutdown' in line:
                lines_to_remove.append(n - 1)
                lines_to_remove.append(n)
                lines_to_remove.append(n + 1)

        final_clean_lines = []
        for n, line in enumerate(clean_lines):
            if n not in lines_to_remove:
                final_clean_lines.append(line)

        return [x for x in final_clean_lines if 'monitor-session capture ethernet' not in x]

    @staticmethod
    def _parse_iface_format(x) -> (str, int, int, int, int | None):
        (iface_type, unit, slot, num) = x.split('/')

        vlan = None
        if '.' in num:
            (num, vlan) = num.split('.')

        return iface_type, int(unit), int(slot), int(num), int(vlan) if vlan else None

    @staticmethod
    def _build_iface_name(iface_type: str, unit: int, slot: int, num: int, vlan: int | None) -> str:
        values = [iface_type, str(unit), str(slot), str(num)]
        name = "/".join(values)

        if vlan is not None:
            name += f".{vlan}"

        return name

    # CommandsMixin
    def command_healthcheck(self) -> str:
        command = "pgrep xrd-startup"
        logging.debug(f"[{__class__}] command_healthcheck: `{command}`")
        return command

    def command_list_file(self) -> str:
        command = f"ls {self.CONFIG_FILE_PATH}"
        logging.debug(f"[{__class__}] command_list_file: `{command}`")
        return command

    def command_test_configuration(self) -> str:
        # Use non-ZTP command because ZTP is still not ready here.
        command = self.CLI_COMMAND.format(command="show configuration failed")
        logging.debug(f"[{__class__}] command_test_configuration: `{command}`")
        return command

    def command_get_neighbour_bgp(self, neighbour_ip: ipaddress.IPv4Address | ipaddress.IPv6Address) -> str:
        ip_str = "ipv6 unicast" if neighbour_ip.version == 6 else ""
        command = self.ZTP_CLI_COMMAND.format(
            command=f"show bgp {ip_str} neighbors {str(neighbour_ip)}"
        )
        logging.info(f"[{__class__}] command_get_neighbour_bgp: `{command}`")
        return command

    def command_get_neighbour_bgp_networks(self, neighbour_ip: ipaddress.IPv4Address | ipaddress.IPv6Address) -> str:
        ip_str = "ipv6 unicast" if neighbour_ip.version == 6 else ""
        command = self.ZTP_CLI_COMMAND.format(
            command=f"show bgp {ip_str} neighbors {str(neighbour_ip)} routes | include /"
        )
        logging.debug(f"[{__class__}] command_get_neighbour_bgp_networks: `{command}`")
        return command

    def command_set_iface_ip(self, num: int, ip: ipaddress.IPv4Interface | ipaddress.IPv6Interface) -> str:
        iface_name = IosXrConfiguration._build_iface_name("GigabitEthernet0", 0, 0, num, None)
        ip_str = f"ipv{ip.version}"

        iface_configure = [f"interface {iface_name}", f" {ip_str} address {str(ip)}", "!"]
        command = self.ZTP_DIFF_APPLY_COMMAND.format(command="\\n".join(iface_configure))
        logging.debug(f"[{__name__}] command_set_iface_ip: `{command}`")
        return command

    def command_unset_iface_ip(self, num: int, ip: ipaddress.IPv4Interface | ipaddress.IPv6Interface) -> str:
        iface_name = IosXrConfiguration._build_iface_name("GigabitEthernet0", 0, 0, num, None)
        ip_str = f"ipv{ip.version}"

        iface_configure = [f"interface {iface_name}", f" no {ip_str} address {str(ip)}", "!"]
        command = self.ZTP_DIFF_APPLY_COMMAND.format(command="\\n".join(iface_configure))
        logging.debug(f"[{__class__}] command_unset_iface_ip: `{command}`")
        return command

    # FormatParserMixin
    def check_health(self, result: str) -> bool:
        return result.strip() != ""

    def check_file_existence(self, result: str) -> bool:
        return "No such file or directory" not in result

    def check_configuration_validity(self, result: str) -> bool:
        # Remove empty lines and remove first line which is the command executed
        lines = [x for x in result.split("\n") if x][1:]
        # If it is empty, means that there are no errors
        return not lines

    def check_bgp_state(self, result: str) -> bool:
        for line in result.split("\n"):
            if 'BGP state' not in line:
                continue

            (_, state) = line.split("=")
            return "Established" in state

        return False

    def parse_bgp_routes(self, result: Any) -> set:
        bgp_routes = set()
        for line in result.split("\n"):
            matches = self.PREFIX_REGEX.search(line)
            if matches:
                bgp_routes.add(ipaddress.ip_network(matches.group(1).strip()))

        return bgp_routes

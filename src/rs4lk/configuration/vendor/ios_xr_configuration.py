import ipaddress
import json
import logging
import os
import tempfile
from subprocess import Popen, PIPE
from typing import Any

from Kathara.model.Lab import Lab
from cisco_config_parser.cisco_config_parser import ConfigParser

from ...foundation.configuration.vendor_configuration import VendorConfiguration
from ...foundation.exceptions import ConfigError
from ...model.bgp_session import BgpSession


class IosXrConfiguration(VendorConfiguration):
    __slots__ = ['_cisco_parser']

    CONFIG_FILE_PATH: str = "disk0:/startup-config.cfg"
    FS_SYSCTL: int = 64000

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

        self._check_host_sysctls()

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

        logging.info(f"Interface `{iface['Interface']['vendor_interface']}` "
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

        all_lines = "".join(self._lines)
        # Start replacing in reverse order to avoid replacing a substring.
        for iface_name, iface in reversed(self.interfaces.items()):
            if '/' not in iface_name:
                continue

            if iface['Interface']['vendor_interface'] == iface['Interface']['interface']:
                continue

            all_lines = all_lines.replace(iface['Interface']['vendor_interface'], iface['Interface']['interface'])

        candidate_router.create_file_from_string(all_lines, self.CONFIG_FILE_PATH)

        # Apply custom configuration after the container has started
        check_cmd_1 = "/pkg/bin/xr_cli \"show run\" | egrep -e 'No configuration change' -e 'No such file or directory'"
        check_cmd_2 = "/pkg/bin/xr_cli \"sh ip interface GigabitEthernet0/0/0/0\" | egrep -e 'ipv4 protocol is Down'"
        check_cmd_3 = "/pkg/bin/xr_cli \"sh ipv6 interface GigabitEthernet0/0/0/0\" | egrep -e 'ipv6 protocol is Down'"
        cfg_cmd = f"/pkg/bin/xr_cli \"copy {self.CONFIG_FILE_PATH} running-config\" | egrep -e 'Updated Commit'"
        net_scenario.create_file_from_list(
            [
                # Wait that xrd-startup finishes
                "pgrep xrd-startup; while [[ $? -eq 0 ]]; do sleep 1; pgrep xrd-startup; done",
                # Check when the control plane is ready
                check_cmd_1,
                f"while [[ $? -eq 0 ]]; do sleep 1; {check_cmd_1}; done",
                # Check when the IPv4 stack goes up
                check_cmd_2,
                f"while [[ $? -eq 0 ]]; do sleep 1; {check_cmd_2}; done",
                # Check when the IPv6 stack goes up
                check_cmd_3,
                f"while [[ $? -eq 0 ]]; do sleep 1; {check_cmd_3}; done",
                # Finally apply the configuration
                cfg_cmd,
                f"while [[ $? -ne 0 ]]; do sleep 1; {cfg_cmd}; done",
            ],
            f"{candidate_name}.startup"
        )

    def _check_host_sysctls(self) -> None:
        for sysctl in ["fs.inotify.max_user_instances", "fs.inotify.max_user_watches"]:
            process = Popen(f"sysctl -n {sysctl}", stdout=PIPE, shell=True)
            output, _ = process.communicate()
            process.terminate()

            num = int(output.decode('utf-8').strip())
            if num < self.FS_SYSCTL:
                logging.warning(f"Increase `{sysctl}` value to {self.FS_SYSCTL}!")

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
    def command_list_file(self) -> str:
        return f"ls {self.CONFIG_FILE_PATH}"

    def command_test_configuration(self) -> str:
        return "configure; commit check; exit"

    def command_get_neighbour_bgp_networks(self, neighbour_ip: ipaddress.IPv4Address | ipaddress.IPv6Address) -> str:
        return f"show route receive-protocol bgp {str(neighbour_ip)} all | display json"

    def command_set_iface_ip(self, num: int, ip: ipaddress.IPv4Interface | ipaddress.IPv6Interface) -> str:
        unit_name = IosXrConfiguration._build_iface_name("ge", 0, 0, num, 0)
        inet_str = "inet" if ip.version == 4 else "inet6"

        return f"configure; set interfaces {unit_name} family {inet_str} address {str(ip)}; commit; exit;"

    def command_unset_iface_ip(self, num: int, ip: ipaddress.IPv4Interface | ipaddress.IPv6Interface) -> str:
        unit_name = IosXrConfiguration._build_iface_name("ge", 0, 0, num, 0)
        inet_str = "inet" if ip.version == 4 else "inet6"

        return f"configure; delete interfaces {unit_name} family {inet_str} address {str(ip)}; commit; exit;"

    # FormatParserMixin
    def check_file_existence(self, result: str) -> bool:
        return "No such file or directory" not in result

    def check_configuration_validity(self, result: str) -> bool:
        return "configuration check succeeds" in result

    def parse_bgp_routes(self, result: Any) -> set:
        output = json.loads(result)

        bgp_routes = set()
        for route_table in output['route-information'][0]['route-table']:
            if 'rt' in route_table:
                for route_entry in route_table['rt']:
                    bgp_routes.add(ipaddress.ip_network(route_entry['rt-destination'][0]['data']))

        return bgp_routes

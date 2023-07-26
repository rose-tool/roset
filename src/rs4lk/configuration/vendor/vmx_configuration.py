from __future__ import annotations

import ipaddress
import json
import logging
from typing import Any

from Kathara.model.Lab import Lab

from ...foundation.configuration.vendor_configuration import VendorConfiguration
from ...foundation.exceptions import ConfigError
from ...model.bgp_session import BgpSession


class VmxConfiguration(VendorConfiguration):
    def _init(self):
        self._parse_ipv6_interface_addresses()
        self._parse_ipv6_sessions()
        self._remap_interfaces()

    def _parse_ipv6_interface_addresses(self) -> None:
        logging.info("Inferring IPv6 interface addresses.")

        ipv6_addrs = {}
        for line in self._lines:
            if 'set interfaces' in line and 'family inet6 address' in line:
                (before_addr, addr_part) = line.split('family inet6 address ')
                addr_parts = addr_part.strip().split(' ')
                addr = ipaddress.IPv6Interface(addr_parts[0])

                (_, iface_parts) = before_addr.split('set interfaces ')
                iface_parts = iface_parts.split(' ')
                iface_name = iface_parts[0].strip()

                # Search for unit
                if 'unit' in iface_parts:
                    iface_name += '.' + iface_parts[2]

                if iface_name not in ipv6_addrs:
                    ipv6_addrs[iface_name] = set()

                ipv6_addrs[iface_name].add(addr)

        for iface_name, addrs in ipv6_addrs.items():
            self.interfaces[iface_name]['All_Prefixes'].extend(addrs)

        logging.debug(f"Resulting interfaces: {self.interfaces}")

    def _parse_ipv6_sessions(self) -> None:
        logging.info("Inferring IPv6 BGP sessions.")

        local_as = self.get_local_as()

        ipv6_bgp_sessions = {}
        for line in self._lines:
            if 'set protocols bgp group' in line:
                (_, group_parts) = line.split('set protocols bgp group ')
                group_parts = group_parts if type(group_parts) == str else group_parts[1]
                group_parts = group_parts.split(' ')
                group = group_parts[0].strip()

                if group not in ipv6_bgp_sessions:
                    ipv6_bgp_sessions[group] = {'group': group, 'local_as': local_as, 'is_v6': True}

                if 'neighbor' in line:
                    (before_addr, addr_part) = line.split('neighbor ')
                    addr_parts = addr_part.strip().split(' ')
                    try:
                        addr = ipaddress.IPv6Address(addr_parts[0])
                    except ipaddress.AddressValueError:
                        ipv6_bgp_sessions[group]['is_v6'] = False
                        continue

                    ipv6_bgp_sessions[group]['remote_ip'] = addr
                elif 'peer-as' in line:
                    (before_peer, peer_part) = line.split('peer-as ')
                    peer_parts = peer_part.strip().split(' ')
                    peer = int(peer_parts[0])

                    ipv6_bgp_sessions[group]['remote_as'] = peer
                elif 'local-address' in line:
                    (before_local_addr, local_addr_part) = line.split('local-address ')
                    local_addr_parts = local_addr_part.strip().split(' ')
                    try:
                        local_addr = ipaddress.IPv6Address(local_addr_parts[0])
                    except ipaddress.AddressValueError:
                        ipv6_bgp_sessions[group]['is_v6'] = False
                        continue

                    ipv6_bgp_sessions[group]['local_ip'] = local_addr

        # Filter out non-valid sessions
        ipv6_bgp_sessions = filter(
            lambda x: 'remote_as' in x and x['is_v6'] and \
                      self._batfish_config.is_valid_session(x['local_as'], x['remote_as']),
            ipv6_bgp_sessions.values()
        )

        for session in ipv6_bgp_sessions:
            remote_as = session['remote_as']

            if remote_as not in self.bgp_sessions:
                self.bgp_sessions[remote_as] = BgpSession(local_as, remote_as)

            local_ip = session['local_ip'] if 'local_ip' in session else None
            self.bgp_sessions[remote_as].add_peering(local_ip, session['remote_ip'], session['group'])

        logging.debug(f"Resulting sessions: {self.bgp_sessions}")

    def _get_bgp_local_as_vendor(self) -> int:
        as_lines = list(filter(lambda x: 'set routing-options autonomous-system' in x, self._lines))
        if not as_lines:
            raise ConfigError("Cannot find local AS value")

        (_, as_str) = as_lines.pop().split('set routing-options autonomous-system ')

        return int(as_str)

    def _remap_interfaces(self) -> None:
        for iface in self.interfaces.values():
            self._remap_interface(iface)

    def _remap_interface(self, iface: dict) -> None:
        if '-' not in iface['Interface']['interface']:
            return

        iface_type, slot, port, pic, unit = self._parse_iface_format(iface['Interface']['interface'])
        if unit is None:
            unit = 0

        # Put it as 'ge', in slot 0 and increment by 1 the PIC (because iface 0 is already taken)
        iface['Interface']['vendor_interface'] = iface['Interface']['interface']
        iface['Interface']['interface'] = self._build_iface_name('ge', slot, 0, pic + 1, unit)

        logging.debug(f"Interface `{iface['Interface']['vendor_interface']}` "
                      f"remapped into `{iface['Interface']['interface']}`.")

    def _on_load_complete(self) -> None:
        for session in self.bgp_sessions.values():
            if session.iface:
                iface_name = session.iface
                iface_type, slot, port, pic, unit = self._parse_iface_format(iface_name)
                iface_idx = pic

                session.iface_idx = iface_idx

    def get_image(self) -> str:
        return 'vrnetlab/vr-vmx:18.2R1.9'

    def apply_to_network_scenario(self, net_scenario: Lab) -> None:
        candidate_name = f"as{self.get_local_as()}"
        candidate_router = net_scenario.get_machine(candidate_name)
        candidate_router.add_meta('image', self.get_image())
        candidate_router.add_meta('vr', True)

        all_lines = self._clean_filters_on_loopback()
        all_lines = "\n".join(all_lines)

        for iface_name, iface in self.interfaces.items():
            if '-' not in iface_name:
                continue

            v_iface_type, v_slot, v_port, v_pic, v_unit = self._parse_iface_format(
                iface['Interface']['vendor_interface']
            )
            if v_unit is None:
                v_unit = 0
            iface_type, slot, port, pic, unit = self._parse_iface_format(
                iface['Interface']['interface']
            )
            if unit is None:
                unit = 0

            name_to_search = self._build_iface_name(v_iface_type, v_slot, v_port, v_pic, None)
            name_to_search_unit = f"{name_to_search} unit {v_unit}"

            name_to_replace = self._build_iface_name(iface_type, slot, port, pic, None)
            name_to_replace_unit = f"{name_to_replace} unit {unit}"

            all_lines = all_lines.replace(name_to_search_unit, name_to_replace_unit)
            all_lines = all_lines.replace(name_to_search, name_to_replace)

        candidate_router.create_file_from_string(all_lines, "/config/startup-config.cfg")

    def get_lines(self) -> list[str]:
        clean_lines = []

        for line in self._lines:
            # Clean system setup lines (these are handled by the vrnetlab)
            if 'set version' in line or 'set system' in line or 'set chassis' in line:
                continue

            # Skip fxp0 configuration (it is done by vrnetlab)
            if 'set interfaces' in line and 'fxp0' in line:
                continue

            # Skip lines setting speed
            if 'set interface' in line and 'gigether-options speed' in line:
                continue

            # Skip SNMP
            if 'set snmp' in line:
                continue

            # Clean the BGP add path lines (not supported in VMX18)
            if 'set protocols bgp' in line and 'add-path' in line:
                if 'neighbor' in line:
                    line = line.replace(' add-path receive', '')
                else:
                    continue

            clean_lines.append(line)

        return clean_lines

    def _clean_filters_on_loopback(self) -> list[str]:
        filter_line_idx = -1

        all_lines = self.get_lines()
        for idx, line in enumerate(all_lines):
            if 'set interfaces lo0' in line and 'filter input':
                filter_line_idx = idx
                break

        if filter_line_idx != -1:
            all_lines.pop(filter_line_idx)

        return all_lines

    @staticmethod
    def _parse_iface_format(x) -> (str, int, int, int, int | None):
        (iface_type, iface_parts) = x.split('-')
        (slot, port, pic) = iface_parts.split('/')

        unit = None
        if '.' in pic:
            (pic, unit) = pic.split('.')

        return iface_type, int(slot), int(port), int(pic), int(unit) if unit else None

    @staticmethod
    def _build_iface_name(speed: str, slot: int, port: int, pic: int, unit: int | None, compact: bool = True) -> str:
        values = [str(slot), str(port), str(pic)]
        name = f"{speed}-" + "/".join(values)

        if unit is not None:
            name += (".%d" if compact else " unit %d") % unit

        return name

    # CommandsMixin
    def command_list_file(self) -> str:
        return "file list startup-config.cfg"

    def command_test_configuration(self) -> str:
        return "configure; commit check; exit"

    def command_get_neighbour_bgp_networks(self, neighbour_ip: ipaddress.IPv4Address | ipaddress.IPv6Address) -> str:
        return f"show route receive-protocol bgp {str(neighbour_ip)} all | display json"

    def command_set_iface_ip(self, num: int, ip: ipaddress.IPv4Interface | ipaddress.IPv6Interface) -> str:
        unit_name = VmxConfiguration._build_iface_name("ge", 0, 0, num, 0)
        inet_str = "inet" if ip.version == 4 else "inet6"

        return f"configure; set interfaces {unit_name} family {inet_str} address {str(ip)}; commit; exit;"

    def command_unset_iface_ip(self, num: int, ip: ipaddress.IPv4Interface | ipaddress.IPv6Interface) -> str:
        unit_name = VmxConfiguration._build_iface_name("ge", 0, 0, num, 0)
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

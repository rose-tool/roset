import ipaddress
import logging
import os
import shutil
import tempfile

from pybatfish.client.session import Session

from ...model.bgp_session import BgpSession, BgpPeering


class BatfishConfiguration:
    __slots__ = ['path', 'name', 'session',
                 '_format', '_interfaces', '_local_as', '_sessions', '_snapshot_tmp_path']

    def __init__(self, url: str, path: str) -> None:
        self.session: Session = Session(host=url)
        self.path: str = os.path.abspath(path)
        # self.name: str = "snapshot-%d" % time.time()
        # TODO: Debug
        self.name: str = "snapshot"

        self._format: str | None = None
        self._interfaces: dict[str, dict] | None = None
        self._local_as: int = 0
        self._sessions: dict[int, BgpSession] | None = None

        self._snapshot_tmp_path: str | None = None
        self._create_temporary_snapshot()

    def get_format(self) -> str:
        if self._format is None:
            result = self.session.q.nodeProperties().answer().dict()
            config = result['answerElements'][0]['rows'][0]

            self._format = config['Configuration_Format']

        return self._format

    def get_interfaces(self) -> dict[str, dict]:
        if self._interfaces is None:
            result = self.session.q.interfaceProperties().answer().dict()
            self._interfaces = dict(
                map(lambda x: (x['Interface']['interface'], x),
                    filter(lambda x: x['Active'], result['answerElements'][0]['rows'])
                    )
            )
            for iface in self._interfaces.values():
                iface['All_Prefixes'] = [ipaddress.IPv4Interface(x) for x in iface['All_Prefixes']]

        return self._interfaces

    def set_interfaces(self, ifaces: dict[str, dict]) -> None:
        self._interfaces = ifaces

    def get_local_as(self) -> int:
        return self._local_as

    def set_local_as(self, local_as: int) -> None:
        self._local_as = local_as

    def get_bgp_sessions(self) -> dict[int, BgpSession]:
        if self._sessions is None:
            self._sessions = {}

            result = self.session.q.bgpPeerConfiguration().answer().dict()
            for row in result['answerElements'][0]['rows']:
                local_as = int(row['Local_AS'])
                if self._local_as == 0:
                    self._local_as = local_as
                remote_as = int(row['Remote_AS'])
                if not self.is_valid_session(local_as, remote_as):
                    continue

                if remote_as not in self._sessions:
                    self._sessions[remote_as] = BgpSession(local_as, remote_as)

                self._sessions[remote_as].add_peering(row['Local_IP'], row['Remote_IP']['value'], row['Peer_Group'])

        return self._sessions

    def set_bgp_sessions(self, sessions: dict[int, BgpSession]) -> None:
        self._sessions = sessions

    def get_interface_for_peering(self, bgp_peering: BgpPeering) \
            -> (str | None, ipaddress.IPv4Interface | ipaddress.IPv6Interface | None):
        selected_iface_name = None
        selected_iface_ip = None
        last_plen = -1

        # Do LPM algorithm
        for iface in self.get_interfaces().values():
            for iface_ip in iface['All_Prefixes']:
                if bgp_peering.remote_ip.version != iface_ip.network.version:
                    continue

                if bgp_peering.remote_ip in iface_ip.network and iface_ip.network.prefixlen > last_plen:
                    selected_iface_name = iface['Interface']['interface']
                    selected_iface_ip = iface_ip
                    last_plen = iface_ip.network.prefixlen

        if selected_iface_name:
            return selected_iface_name, selected_iface_ip

        logging.warning(f"Cannot find interface for directly connected peering with AS{bgp_peering.session.remote_as}.")

        return None, None

    def cleanup(self) -> None:
        shutil.rmtree(self._snapshot_tmp_path, ignore_errors=True)

    @staticmethod
    def is_valid_session(local_as: int, remote_as: int) -> bool:
        if 64000 <= remote_as <= 131071:
            logging.warning(f"Skipping session with AS{remote_as} is in reserved range 64000-131071.")
            return False
        if local_as == remote_as:
            logging.warning(f"Skipping session with AS{remote_as} is a iBGP peering.")
            return False

        return True

    def _create_temporary_snapshot(self) -> None:
        logging.info(f"Parsing configuration in file: `{self.path}`.")

        with tempfile.TemporaryDirectory('-manrs-snapshot') as temp_dir:
            snapshot_dir = os.path.join(temp_dir, "snapshot")
            configs_dir = os.path.join(snapshot_dir, "configs")
            os.makedirs(configs_dir, exist_ok=True)

            shutil.copyfile(self.path, os.path.join(configs_dir, "candidate_config.cfg"))

            self.session.init_snapshot(snapshot_dir, name=self.name, overwrite=True)

            self._snapshot_tmp_path = temp_dir

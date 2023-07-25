import logging
import shlex
import time

from Kathara.manager.Kathara import Kathara
from Kathara.model.Lab import Lab
from Kathara.model.Machine import Machine

from ..foundation.configuration.vendor_configuration import VendorConfiguration
from ..foundation.exceptions import NetworkScenarioError
from ..model.topology import BgpRouter, Node, Topology, Client


class NetworkScenarioManager:
    def build_from_topology(self, name: str, topology: Topology) -> Lab:
        logging.info("Creating Kathara network scenario from AS Topology...")

        if not topology:
            raise NetworkScenarioError("Cannot create network scenario")

        net_scenario = Lab(name)

        for as_num, node in topology.all():
            device = self._build_device(net_scenario, node)

            # Do not configure interfaces on candidate
            if isinstance(node, BgpRouter) and node.relationship is None:
                continue

            for iface_idx, iface in node.neighbours.items():
                with device.lab.fs.open(f"{device.name}.startup", 'a+') as startup:
                    for v_ips in iface.local_ips.values():
                        startup.write("".join([f"ip addr add {x} dev eth{iface_idx}\n" for (x, _) in v_ips]))

        return net_scenario

    def _build_device(self, net_scenario: Lab, node: Node) -> Machine:
        device_name = node.name

        if not net_scenario.find_machine(node.name):
            device = net_scenario.new_machine(device_name)
            logging.info(f"Device `{device_name}` created.")

            if isinstance(node, BgpRouter):
                device.add_meta('image', 'kathara/frr')
            elif isinstance(node, Client):
                device.add_meta('image', 'kathara/base')

            if isinstance(node, BgpRouter) and node.relationship is None:
                device.add_meta('ipv6', "False")
            else:
                device.add_meta('ipv6', "True")

            for iface_idx, iface in node.neighbours.items():
                net_scenario.connect_machine_to_link(device_name, iface.cd, machine_iface_number=iface_idx)

                logging.info(f"Device `{device_name}` connected " +
                             (f"with `{iface.neighbour.name}` " if iface.neighbour else "") +
                             f"on collision domain `{iface.cd}` with "
                             f"interface idx={iface_idx}.")

                if iface.neighbour:
                    self._build_device(net_scenario, iface.neighbour)

            return device
        else:
            return net_scenario.get_machine(device_name)

    @staticmethod
    def start_candidate_device(net_scenario: Lab, vendor_config: VendorConfiguration) -> None:
        candidate_device = net_scenario.machines[f"as{vendor_config.get_local_as()}"]

        logging.info(f"Starting candidate device `{candidate_device.name}`...")
        Kathara.get_instance().deploy_machine(candidate_device)
        logging.info(f"Waiting candidate device `{candidate_device.name}` startup...")

        # Ask to print something in order to wait the startup
        exec_output = Kathara.get_instance().exec(
            machine_name=candidate_device.name,
            command=shlex.split(vendor_config.command_list_file()),
            lab_name=net_scenario.name
        )

        is_running = False
        # Triggers the command.
        while not is_running:
            time.sleep(5)
            try:
                (stdout, _) = next(exec_output)
                stdout = stdout.decode('utf-8')
                is_running = "Waiting" not in stdout
            except StopIteration:
                pass

    @staticmethod
    def start_other_devices(net_scenario: Lab, vendor_config: VendorConfiguration) -> None:
        logging.info("Starting all other devices...")

        all_except_candidate = {x for x in net_scenario.machines.keys() if x != f"as{vendor_config.get_local_as()}"}
        Kathara.get_instance().deploy_lab(net_scenario, selected_machines=all_except_candidate)

    @staticmethod
    def undeploy(net_scenario: Lab) -> None:
        logging.info("Undeploying network scenario...")
        Kathara.get_instance().undeploy_lab(net_scenario.hash)

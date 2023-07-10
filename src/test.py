import argparse
import logging
import os
import subprocess
import sys

from Kathara.setting.Setting import Setting

from rs4lk.actions.action_manager import ActionManager
from rs4lk.batfish.batfish_configuration import BatfishConfiguration
from rs4lk.colored_logging import set_logging
from rs4lk.configuration.bgp_configuration import BgpConfiguration
from rs4lk.configuration.vendor_configuration_factory import VendorConfigurationFactory
from rs4lk.globals import DEFAULT_RIB, DEFAULT_BATFISH_URL
from rs4lk.model.topology import Topology
from rs4lk.mrt.table_dump import TableDump
from rs4lk.network_scenario.network_scenario_manager import NetworkScenarioManager


def connect(machine):
    command = "%s -c \"from Kathara.manager.Kathara import Kathara; " \
              "Kathara.get_instance().connect_tty('%s', lab_name='%s', shell='%s', logs=True)\"" \
              % (sys.executable, machine.name, machine.lab.name, Setting.get_instance().device_shell)
    subprocess.Popen([Setting.get_instance().terminal, "-e", command], start_new_session=True)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--batfish_url', type=str, required=False, default=DEFAULT_BATFISH_URL)
    parser.add_argument('--config_path', type=str, required=True)
    parser.add_argument('--rib_dump', type=str, required=False, default=DEFAULT_RIB)
    parser.add_argument('--exclude_checks', type=str, required=False, default="")

    return parser.parse_args()


def main(args):
    batfish_config = BatfishConfiguration(args.batfish_url, args.config_path)
    vendor_config_factory = VendorConfigurationFactory()
    vendor_config = vendor_config_factory.create_from_batfish_config(batfish_config)

    rib_dump_file = os.path.abspath(args.rib_dump)
    table_dump = TableDump(rib_dump_file)
    topology = Topology(vendor_config, table_dump)

    net_scenario_manager = NetworkScenarioManager()
    net_scenario = net_scenario_manager.build_from_topology(vendor_config.name, topology)

    bgp_config = BgpConfiguration(topology)
    bgp_config.apply_to_network_scenario(net_scenario)

    vendor_config.apply_to_network_scenario(net_scenario)

    Setting.get_instance().load_from_dict({'image': 'kathara/frr'})
    logging.info("Deploying network scenario...")
    net_scenario_manager.start_candidate_device(net_scenario, vendor_config)
    net_scenario_manager.start_other_devices(net_scenario, vendor_config)
    logging.success("Network scenario deployed successfully.")

    # for machine in net_scenario.machines.values():
    #     connect(machine)

    action_manager = ActionManager(exclude=args.exclude_checks.split(','))
    result = action_manager.start(vendor_config, topology, net_scenario)
    if result:
        logging.success(f"Configuration file `{args.config_path}` is MANRS compliant!")
    else:
        logging.error(f"Configuration file `{args.config_path}` is not MANRS compliant!")

    table_dump.close()

    net_scenario_manager.undeploy(net_scenario)


if __name__ == "__main__":
    set_logging()

    main(parse_args())

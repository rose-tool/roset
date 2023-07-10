from __future__ import annotations

import json
import logging
import shlex
import time

from Kathara.manager.Kathara import Kathara
from Kathara.model.Lab import Lab

from .action_3 import Action3
from .action_4 import Action4
from ..foundation.actions.action import Action
from ..foundation.configuration.vendor_configuration import VendorConfiguration
from ..foundation.exceptions import BgpRuntimeError
from ..model.topology import Topology

CONVERGENCE_ATTEMPTS = 100


class ActionManager:
    __slots__ = ['_actions']

    DEFAULT_ACTIONS = [Action3(), Action4()]

    def __init__(self, exclude: list | None = None):
        if exclude is None:
            self._actions: list[Action] = self.DEFAULT_ACTIONS
        else:
            self._actions: list[Action] = list(filter(lambda x: x.name() not in exclude, self.DEFAULT_ACTIONS))

    def start(self, config: VendorConfiguration, topology: Topology, net_scenario: Lab) -> bool:
        converged = self._wait_convergence(net_scenario)
        if not converged:
            raise BgpRuntimeError("BGP did not converge")

        logging.info("Starting MANRS actions check...")
        for action in self._actions:
            logging.info(f"Starting `{action.display_name()}` verification...")
            result = action.verify(config, topology, net_scenario)
            if not result:
                logging.error(f"`{action.display_name()}` not passed!")
                return False

        return True

    def _wait_convergence(self, net_scenario: Lab) -> bool:
        logging.info("Checking routers convergence...")

        selected_devices = set(
            filter(
                lambda x: 'as' in x.name and '_client' not in x.name and not x.is_virtual_router(),
                net_scenario.machines.values()
            )
        )

        attempts = 0
        counter = 0
        while not counter >= 3:
            time.sleep(5)

            if attempts >= CONVERGENCE_ATTEMPTS:
                logging.error(f"BGP is not converging: {CONVERGENCE_ATTEMPTS} attempts. Aborting.")
                return False

            converged_routers = self._bgp_established(selected_devices)
            if all(converged_routers):
                counter += 1
            else:
                counter = 0
                attempts += 1

            converged_routers_count = sum([1 for x in converged_routers if x])
            logging.info(f"[ATTEMPT {attempts}] {converged_routers_count}/{len(converged_routers)} routers converged!")

        logging.info("Routers converged!")

        return True

    def _bgp_established(self, selected_devices: set) -> list:
        summaries = self._get_routers_summary(selected_devices)

        converged_routers = []

        for machine, summary in summaries.items():
            has_ipv4 = False
            flag_ipv4 = True
            has_ipv6 = False
            flag_ipv6 = True

            if not summary:
                converged_routers.append(False)
                continue

            if 'ipv4Unicast' in summary:
                has_ipv4 = True
                flag_ipv4 = summary['ipv4Unicast']['failedPeers'] == 0

            if 'ipv6Unicast' in summary:
                has_ipv6 = True
                flag_ipv6 = summary['ipv6Unicast']['failedPeers'] == 0

            inc = flag_ipv4 if has_ipv4 else True
            inc = flag_ipv6 and inc if has_ipv6 else inc
            converged_routers.append(inc)

        return converged_routers

    @staticmethod
    def _get_routers_summary(selected_devices: set) -> dict:
        summaries = {}

        for machine in selected_devices:
            logging.debug(f"Querying router `{machine.name}`...")

            exec_output = Kathara.get_instance().exec(
                machine_name=machine.name,
                command=shlex.split("vtysh -c 'show bgp summary json'"),
                lab_name=machine.lab.name
            )

            bgp_summary = ""
            try:
                while True:
                    (stdout, _) = next(exec_output)
                    stdout = stdout.decode('utf-8') if stdout else ""

                    if stdout:
                        bgp_summary += stdout
            except StopIteration:
                pass

            try:
                bgp_summary = json.loads(bgp_summary)
            except ValueError:
                bgp_summary = None
                logging.error(f"Unable to parse BGP JSON of device `{machine.name}`.")

            summaries[machine.name] = bgp_summary

        return summaries

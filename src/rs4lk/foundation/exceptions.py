# Generic Exceptions
class ClassNotFoundError(Exception):
    pass


class InstantiationError(Exception):
    pass


# Configuration Exceptions
class ConfigError(Exception):
    def __init__(self, error_str: str) -> None:
        super().__init__(f"[Configuration Error] {error_str}.")


# Topology Exceptions
class TopologyError(Exception):
    def __init__(self, error_str: str) -> None:
        super().__init__(f"[Topology Error] {error_str}.")


# Network Scenario Exceptions
class NetworkScenarioError(Exception):
    def __init__(self, error_str: str) -> None:
        super().__init__(f"[Network Scenario Error] {error_str}.")


# Runtime Exceptions
class BgpRuntimeError(Exception):
    def __init__(self, error_str: str) -> None:
        super().__init__(f"[BGP Runtime Error] {error_str}.")

from ..foundation.exceptions import InstantiationError


class CollisionDomain:
    __slots__ = ['_current_collision_domain', '_collision_domain_assignments']

    __instance = None

    @staticmethod
    def get_instance() -> 'marns.network_scenario.collision_domain.CollisionDomain':
        if CollisionDomain.__instance is None:
            CollisionDomain()

        return CollisionDomain.__instance

    def __init__(self) -> None:
        if CollisionDomain.__instance is not None:
            raise InstantiationError("This class is a singleton!")
        else:
            self._current_collision_domain: (str, str, str, str) = ('A', 'A', 'A', '@')
            self._collision_domain_assignments: dict = {}

            CollisionDomain.__instance = self

    def get(self, first_node: str, second_node: str) -> str:
        if (first_node, second_node) in self._collision_domain_assignments:
            return self._collision_domain_assignments[(first_node, second_node)]
        elif (second_node, first_node) in self._collision_domain_assignments:
            return self._collision_domain_assignments[(second_node, first_node)]
        else:
            collision_domain = self._new()
            self._collision_domain_assignments[(first_node, second_node)] = collision_domain

            return collision_domain

    def _new(self) -> str:
        (first, second, third, fourth) = self._current_collision_domain
        first, second, third, fourth = ord(first), ord(second), ord(third), ord(fourth)

        (third, fourth) = self._get_next_char(third, fourth, inc_second=True)
        (second, third) = self._get_next_char(second, third)
        (first, second) = self._get_next_char(second, first)

        first, second, third, fourth = chr(first), chr(second), chr(third), chr(fourth)
        self._current_collision_domain = (first, second, third, fourth)

        return "".join(list(self._current_collision_domain))

    @staticmethod
    def _get_next_char(first_char: int, second_char: int, inc_second: bool = False) -> (int, int):
        if second_char >= ord('Z'):
            first_char += 1
            second_char = ord('A')
        else:
            if inc_second:
                second_char += 1

        return first_char, second_char

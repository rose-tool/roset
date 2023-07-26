from __future__ import annotations

import logging

from .action import Action


class ActionResult:
    __slots__ = ['action', 'statuses', 'reasons']

    def __init__(self, action: Action) -> None:
        self.action: Action = action
        self.statuses: list[int] = []
        self.reasons: list[str | None] = []

    def add_result(self, status: int, reason: str | None = None) -> None:
        self.statuses.append(status)
        self.reasons.append(reason)

    def passed(self) -> bool:
        return all([x == 1 or x == 2 for x in self.statuses])

    def has_warnings(self) -> bool:
        return any([x == 1 for x in self.statuses])

    def print(self) -> None:
        for i, status in enumerate(self.statuses):
            reason_str = f"[{self.action.display_name()}] {self.reasons[i]}" if self.reasons[i] else \
                f"[{self.action.display_name()}] " + ("Passed" if status else "Failed") + " (No Message)."
            if status == 2:
                logging.success(reason_str)
            elif status == 1:
                logging.warning(reason_str)
            else:
                logging.error(reason_str)

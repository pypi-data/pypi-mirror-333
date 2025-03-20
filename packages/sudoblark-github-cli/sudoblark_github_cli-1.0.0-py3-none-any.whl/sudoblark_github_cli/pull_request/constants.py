from enum import Enum


class PermissiblePullRequestStates(str, Enum):
    ALL = "ALL"
    CLOSE = "CLOSE"
    OPEN = "OPEN"

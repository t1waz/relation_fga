import enum

CONDITION_SEPARATOR = "111"  # TODO


class PermissionOperator(str, enum.Enum):
    OR = "or"

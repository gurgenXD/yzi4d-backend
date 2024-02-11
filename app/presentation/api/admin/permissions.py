from enum import Enum


class PermissionType(Enum):
    """Типы прав."""

    ADMIN = "admin"
    MARKETER = "marketer"
    OPERATOR = "operator"

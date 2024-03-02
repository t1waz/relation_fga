import enum


DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


class JWTTokenKind(str, enum.Enum):
    ACCESS = "access"
    REFRESH = "refresh"

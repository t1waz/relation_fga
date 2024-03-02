import enum


class JWTTokenKind(str, enum.Enum):
    ACCESS = "access"
    REFRESH = "refresh"

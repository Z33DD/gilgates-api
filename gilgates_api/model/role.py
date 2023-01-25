from enum import Enum, auto


class Role(str, Enum):
    ADMIN = auto()
    SUPERVISOR = auto()
    AGENTE = auto()
    ANON = auto()

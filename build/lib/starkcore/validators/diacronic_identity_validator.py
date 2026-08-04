from dataclasses import dataclass
from enum import Enum


class IdentityVerdict(Enum):
    IDENTITY_PERSISTENT = "IDENTITY_PERSISTENT"
    LABEL_ONLY = "LABEL_ONLY"
    HISTORY_BROKEN = "HISTORY_BROKEN"
    CONSTRAINT_BROKEN = "CONSTRAINT_BROKEN"


@dataclass
class EntityState:
    name: str
    state: set
    history: list
    constraints: set


def check_state(previous, current):
    """
    La entidad puede cambiar estado,
    pero debe conservar continuidad.
    """
    if previous.name != current.name:
        return False

    return True


def check_history(entity):
    """
    Una identidad sin trayectoria
    solo tiene etiqueta.
    """
    return len(entity.history) > 0


def check_constraints(entity):
    """
    Las restricciones definen
    qué cambios son permitidos.
    """
    return entity.constraints.issubset(entity.state)


def diacronic_validator(previous, current):

    if not check_state(previous, current):
        return IdentityVerdict.LABEL_ONLY

    if not check_history(current):
        return IdentityVerdict.HISTORY_BROKEN

    if not check_constraints(current):
        return IdentityVerdict.CONSTRAINT_BROKEN

    return IdentityVerdict.IDENTITY_PERSISTENT

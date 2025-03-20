from iprm.core.core import get_objects as _get_objects
from iprm.core.core import Session as _Session
from iprm.core.core import FILE_NAME


def get_objects() -> list['Object']:
    return _get_objects()


class Session(_Session):
    pass

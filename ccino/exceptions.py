class CcinoBail(Exception):
    pass


class CcinoException(Exception):
    pass


class AlreadyRunnableException(CcinoException):
    pass


class TestDidNotRaise(CcinoException):
    pass


class TestDidNotReturn(CcinoException):
    pass


class UnknownSignature(CcinoException):
    pass

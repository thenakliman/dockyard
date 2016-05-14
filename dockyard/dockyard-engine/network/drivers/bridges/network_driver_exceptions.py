# This module holds all the exceptions used by bridge type driver.
class BridgeDriversExceptions(Exception):
    pass


class NamespaceNotFound(BridgeDriversExceptions):
    pass


class UnableToAttachNamespace(BridgeDriversExceptions):
    pass


class InsufficientInfo(BridgeDriversExceptions):
    pass


class AlreadyInNamespace(BridgeDriversExceptions):
    pass


class InterfaceNotFound(BridgeDriversExceptions):
    pass


class FailedToMoveInterface(BridgeDriversExceptions):
    pass


class UnableToAssignIP(BridgeDriversExceptions):
    pass


class UnableToChangeState(BridgeDriversExceptions):
    pass


class InvalidState(BridgeDriversExceptions):
    pass

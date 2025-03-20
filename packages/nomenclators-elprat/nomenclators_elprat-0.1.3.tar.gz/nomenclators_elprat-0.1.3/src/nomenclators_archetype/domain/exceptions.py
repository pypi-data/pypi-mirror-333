"""
----------------------------------------------------------------------------------------------------
Written by:
  - Yovany Dominico Girón (y.dominico.giron@elprat.cat)

for Ajuntament del Prat de Llobregat
----------------------------------------------------------------------------------------------------

----------------------------------------------------------------------------------------------------
"""


class InvalidEventTypeException(Exception):
    """Raised when the event does not valid type."""

    def __init__(self):
        super().__init__("Event with invalid type")


class InvalidParameterTypeException(Exception):
    """Raised when the parameter does not valid type."""

    def __init__(self):
        super().__init__("Invalid Parameter type")


class EmptyContextException(Exception):
    """Raised when the context is empty."""

    def __init__(self):
        super().__init__("Empty context")


class ParameterCountException(Exception):
    """Raised when has too many parameter."""

    def __init__(self):
        super().__init__("Too many parameter")


class RequiredParameterException(Exception):
    """Raised when the require parameter on Class"""

    def __init__(self, cls_name):
        super().__init__(f"`{cls_name}` had parameter required")


class RequiredElementError(Exception):
    """Raised when the require element on Class"""

    def __init__(self, cls_name):
        super().__init__(f"`{cls_name}`, had required")


class BusinessIntegrityError(Exception):
    """Raised when the domain integrity error on Class"""

    def __init__(self, cls_name, errors: list):
        self.errors = errors
        super().__init__(
            f"`{cls_name}`, had integrity problems:\n {', '.join(errors)}")

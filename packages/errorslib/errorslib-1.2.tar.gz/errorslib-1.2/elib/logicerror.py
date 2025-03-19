"""
Logic Error
"""

class LogicError(Exception):
    """Logic fucking died"""
    pass

class NotAnError(LogicError):
    """There is no error."""  # Wait, this is technically a paradox.
    pass

class ParadoxError(LogicError):
    """Oh no! paradox."""
    pass

class ThisErrorShouldNeverHappenError(LogicError):
    """this error should never happen."""
    pass

class ThisErrorIsInevitableError(LogicError):
    """this error is inevitable."""
    pass
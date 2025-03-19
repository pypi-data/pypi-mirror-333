"""
Developer Error
"""

from .absexc import AbsurdException

class DevError(AbsurdException):
    """Developer needs to RTFM."""
    pass

class AuthorError(DevError):
    """the author needs to read the fucking manual."""
    pass

class AuthorIsAnIdiotError(DevError):
    """problem exists between keyboard and chair. Except in the author's house."""
    pass

class DebuggingTimeError(DevError):
    """debug required."""
    pass

class DidntImplementedError(DevError):
    """i didn't implement it. (Obsolete)"""
    pass

class ForgotToImplementError(DevError):
    """forgot to implement."""
    pass
"""
User Error
"""

from .absexc import AbsurdException

class UserError(AbsurdException):
    """User needs to RTFM."""
    pass

class UserIsAnIdiotError(UserError):
    """problem exists between keyboard and chair."""
    pass

class UserIsNotAnIdiotError(UserError):
    """problem does not exist between keyboard and chair."""
    pass

class PICNICError(UserError):
    """Problem In Chair, Not In Computer."""
    pass

class FeatureNotABugError(UserError):
    """it's a feature. Not a bug."""
    pass

class UserIsUsingWindowsError(UserError):
    """the user is using an inferior operating system."""
    pass

class UserIsUsingMacOSError(UserError):
    """the user is using MacOS."""
    pass

class UserIsAppleSheepError(UserError):
    """the user is an Apple sheep."""
    pass

class UserIsUsingLinuxError(UserError):
    """the user is a Linux elitist."""
    pass

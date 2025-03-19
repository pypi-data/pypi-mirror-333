# elib/__init__.py

# Import base errors
from .codeerror import CodeError
from .deverror import DevError
from .dunnoerror import DunnoError
from .hardwareerror import HardwareError
from .logicerror import LogicError
from .usererror import UserError

# Import all subclasses from their respective modules
from .absexc import (AbsurdException)

from .usererror import (
    UserIsAnIdiotError, UserIsNotAnIdiotError, PICNICError,
    FeatureNotABugError, UserIsUsingWindowsError, UserIsUsingMacOSError,
    UserIsAppleSheepError, UserIsUsingLinuxError
)

from .deverror import (
    AuthorError, AuthorIsAnIdiotError, DebuggingTimeError,
    DidntImplementedError, ForgotToImplementError
)

from .codeerror import (
    CodeIsFuckedUpError, OvercomplicatedSolutionError,
    UndercomplicatedSolutionError, OopsIDidItAgainError, NotAGoodError
)

from .hardwareerror import (
    WTFNoBiosError, WTFNoOS, NoInternetError,
    NoKeyboardError, iGPUExistsError
)

from .logicerror import (
    NotAnError, ParadoxError, ThisErrorShouldNeverHappenError,
    ThisErrorIsInevitableError
)

from .dunnoerror import (
    WTFError, IdiotError
)

# Define what gets imported when doing "from elib import *"
__all__ = [
    # Base Errors
    "AbsurdException", "UserError", "DevError", "CodeError", "HardwareError", "LogicError", "DunnoError",

    # User Errors
    "UserIsAnIdiotError", "UserIsNotAnIdiotError", "PICNICError",
    "FeatureNotABugError", "UserIsUsingWindowsError", "UserIsUsingMacOSError",
    "UserIsAppleSheepError", "UserIsUsingLinuxError",

    # Developer Errors
    "AuthorError", "AuthorIsAnIdiotError", "DebuggingTimeError",
    "DidntImplementedError", "ForgotToImplementError",

    # Code Errors
    "CodeIsFuckedUpError", "OvercomplicatedSolutionError",
    "UndercomplicatedSolutionError", "OopsIDidItAgainError", "NotAGoodError",

    # Hardware Errors
    "WTFNoBiosError", "WTFNoOS", "NoInternetError",
    "NoKeyboardError", "iGPUExistsError",

    # Logic Errors
    "NotAnError", "ParadoxError", "ThisErrorShouldNeverHappenError",
    "ThisErrorIsInevitableError",

    # WTF Errors
    "WTFError", "IdiotError"
]

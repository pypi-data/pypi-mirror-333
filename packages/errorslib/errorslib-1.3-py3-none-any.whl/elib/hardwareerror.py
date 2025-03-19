"""
Hardware Error
"""

from .absexc import AbsurdException

class HardwareError(AbsurdException):
    """Problem in computer, not chair"""
    pass

class WTFNoBiosError(HardwareError):
    """how!?"""
    pass

class WTFNoOS(HardwareError):
    """how!?"""
    pass

class NoInternetError(HardwareError):
    """there is no internet connection."""
    pass

class NoKeyboardError(HardwareError):
    """Keyboard not found. Press any key to continue..."""
    pass

class iGPUExistsError(HardwareError):
    """the iGPU exists and is being used."""
    pass
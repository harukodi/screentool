import ctypes

class DisplayManager:
    """
    Switches screen topology directly via SetDisplayConfig (user32.dll).
    Only 'internal' and 'extend' are exposed as public methods.
    """

    # SetDisplayConfig topology flags (winuser.h)
    _SDC_TOPOLOGY_INTERNAL = 0x00000001
    _SDC_TOPOLOGY_EXTEND   = 0x00000004
    _SDC_APPLY             = 0x00000080

    _ERROR_SUCCESS = 0

    def __init__(self):
        self._user32 = ctypes.WinDLL("user32")

    def internal(self) -> bool:
        """Switches to internal mode"""
        return self._set_topology(self._SDC_TOPOLOGY_INTERNAL)

    def extend(self) -> bool:
        """Switches to extended mode"""
        return self._set_topology(self._SDC_TOPOLOGY_EXTEND)

    def _set_topology(self, topology_flag: int) -> bool:
        """
        Internal helper method that calls SetDisplayConfig with the given topology.
        With SDC_TOPOLOGY_* + SDC_APPLY, we don't need to pass path/mode arrays,
        Windows figures them out automatically based on the topology.
        """
        result = self._user32.SetDisplayConfig(
            0, None,
            0, None,
            topology_flag | self._SDC_APPLY
        )
        return result == self._ERROR_SUCCESS

display_manager = DisplayManager()
from lldb_typeinfo.error import SBError

class SBProcess(object):
    def Destroy(self) -> SBError:
        r"""
        Destroy(SBProcess self) -> SBError

            Kills the process and shuts down all threads that were spawned to
            track and monitor process.
        """

    def Continue(self) -> SBError:
        r"""Continue(SBProcess self) -> SBError"""

    def Stop(self) -> SBError:
        r"""Stop(SBProcess self) -> SBError"""

    def Kill(self) -> SBError:
        r"""
        Kill(SBProcess self) -> SBError
        Same as Destroy(self).
        """

    def Detach(self, keep_stopped=False) -> SBError:
        r"""
        Detach(SBProcess self) -> SBError
        Detach(SBProcess self, bool keep_stopped) -> SBError
        """

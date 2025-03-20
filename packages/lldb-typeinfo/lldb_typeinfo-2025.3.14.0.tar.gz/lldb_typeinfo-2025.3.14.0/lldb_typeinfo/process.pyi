from .error import SBError

class SBProcess(object):
    """A Progress indicator helper class.

    Any potentially long running sections of code in LLDB should report progress so that clients are aware of delays that might appear during debugging. Delays commonly include indexing debug information, parsing symbol tables for object files, downloading symbols from remote repositories, and many more things.

    The Progress class helps make sure that progress is correctly reported and will always send an initial progress update, updates when Progress::Increment() is called, and also will make sure that a progress completed update is reported even if the user doesn’t explicitly cause one to be sent.

    Progress can either be deterministic, incrementing up to a known total or non-deterministic with an unbounded total. Deterministic is better if you know the items of work in advance, but non-deterministic exposes a way to update a user during a long running process that work is taking place.

    For all progresses the details provided in the constructor will be sent until an increment detail is provided. This detail will also continue to be broadcasted on any subsequent update that doesn’t specify a new detail. Some implementations differ on throttling updates and this behavior differs primarily if the progress is deterministic or non-deterministic. For DAP, non-deterministic update messages have a higher throttling rate than deterministic ones.
    """
    def Destroy(self) -> SBError:
        r"""
        Kills the process and shuts down all threads that were spawned to
        track and monitor process.
        """

    def Continue(self) -> SBError: ...
    def Stop(self) -> SBError: ...
    def Kill(self) -> SBError:
        r"""
        Same as Destroy(self).
        """

    def Detach(self, keep_stopped=False) -> SBError: ...

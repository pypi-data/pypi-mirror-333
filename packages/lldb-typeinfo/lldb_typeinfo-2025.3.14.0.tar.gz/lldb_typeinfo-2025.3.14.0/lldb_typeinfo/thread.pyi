from .process import SBProcess

class SBThread(object):
    """
    Represents a thread of execution. SBProcess contains SBThread(s).

    SBThreads can be referred to by their ID, which maps to the system specific thread identifier, or by IndexID. The ID may or may not be unique depending on whether the system reuses its thread identifiers. The IndexID is a monotonically increasing identifier that will always uniquely reference a particular thread, and when that thread goes away it will not be reused.

    SBThread supports frame iteration.
    """
    def GetProcess(self) -> SBProcess: ...
    def GetName(self) -> str: ...
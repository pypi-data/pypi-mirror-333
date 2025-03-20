from .thread import SBThread

class SBFrame(object):
    """represents one of the stack frames associated with a thread.
    SBThread contains SBFrame(s).
    """

    def GetThread(self) -> SBThread: ...
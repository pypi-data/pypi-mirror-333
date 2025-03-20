from lldb_typeinfo.thread import SBThread

class SBFrame(object):
    def GetThread(self) -> SBThread:
        r"""GetThread(SBFrame self) -> SBThread"""

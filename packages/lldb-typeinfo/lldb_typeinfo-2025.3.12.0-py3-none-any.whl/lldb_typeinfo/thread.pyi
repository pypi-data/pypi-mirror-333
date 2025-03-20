from lldb_typeinfo.process import SBProcess

class SBThread(object):
    def GetProcess(self) -> SBProcess:
        r"""GetProcess(SBThread self) -> SBProcess"""

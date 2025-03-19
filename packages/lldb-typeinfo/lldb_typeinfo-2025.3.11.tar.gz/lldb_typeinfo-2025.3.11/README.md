# lldb-typeinfo

Additional type info for lldb.

Original:

```python
def GetChildAtIndex(self, *args):
    r"""
    GetChildAtIndex(SBValue self, uint32_t idx) -> SBValue
    GetChildAtIndex(SBValue self, uint32_t idx, lldb::DynamicValueType use_dynamic, bool can_create_synthetic) -> SBValue
```

fixed:

```python
def GetChildAtIndex(self, idx: int) -> SBValue: ...
```

## note

Work in progress

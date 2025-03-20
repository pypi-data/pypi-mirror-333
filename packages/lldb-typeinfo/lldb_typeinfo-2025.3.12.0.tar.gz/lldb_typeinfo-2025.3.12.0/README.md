# lldb-typeinfo

Type information for use with lldb scripting

## usage

in the script header, insert the following snippet:

```py
try:
    from lldb_typeinfo import SBFrame
except ImportError as _e:
    exec("""
class SBFrame:
    pass
        """)
    pass
```

replace `SBFrame` with the desired class.

## implementation details

this project change the original swig-generated binding:

```python
def GetChildAtIndex(self, *args):
    r"""
    GetChildAtIndex(SBValue self, uint32_t idx) -> SBValue
    GetChildAtIndex(SBValue self, uint32_t idx, lldb::DynamicValueType use_dynamic, bool can_create_synthetic) -> SBValue
```

with more detailed binding:

```python
def GetChildAtIndex(self, idx: int) -> SBValue: ...
```

## note

Work in progress

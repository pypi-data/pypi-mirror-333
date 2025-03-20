class SBValue(object):
    r"""
    Represents the value of a variable, a register, or an expression.

    SBValue supports iteration through its child, which in turn is represented
    as an SBValue.
    """

    def GetValueAsUnsigned(self, fail_value=0) -> int: ...
    def GetChildMemberWithName(self, name: str, use_dynamic=False) -> SBValue:
        r"""
        Returns the child member value.

        Matches child members of this object and child members of any base
        classes.

        @param[in] name
            The name of the child value to get

        @param[in] use_dynamic
            An enumeration that specifies whether to get dynamic values,
            and also if the target can be run to figure out the dynamic
            type of the child value.

        @return
            A new SBValue object that represents the child member value.
        """

    def GetSummary(self, *args) -> str:
        r"""
        returns the summary for this value as a string
        """

    def GetChildAtIndex(self, idx: int) -> SBValue:
        r"""
        Get a child value by index from a value.

        Structs, unions, classes, arrays and pointers have child
        values that can be access by index.

        Structs and unions access child members using a zero based index
        for each child member. For

        Classes reserve the first indexes for base classes that have
        members (empty base classes are omitted), and all members of the
        current class will then follow the base classes.

        Pointers differ depending on what they point to. If the pointer
        points to a simple type, the child at index zero
        is the only child value available, unless synthetic_allowed
        is true, in which case the pointer will be used as an array
        and can create 'synthetic' child values using positive or
        negative indexes. If the pointer points to an aggregate type
        (an array, class, union, struct), then the pointee is
        transparently skipped and any children are going to be the indexes
        of the child values within the aggregate type. For example if
        we have a 'Point' type and we have a SBValue that contains a
        pointer to a 'Point' type, then the child at index zero will be
        the 'x' member, and the child at index 1 will be the 'y' member
        (the child at index zero won't be a 'Point' instance).

        If you actually need an SBValue that represents the type pointed
        to by a SBValue for which GetType().IsPointeeType() returns true,
        regardless of the pointee type, you can do that with the SBValue.Dereference
        method (or the equivalent deref property).

        Arrays have a preset number of children that can be accessed by
        index and will returns invalid child values for indexes that are
        out of bounds unless the synthetic_allowed is true. In this
        case the array can create 'synthetic' child values for indexes
        that aren't in the array bounds using positive or negative
        indexes.

        @param[in] idx
            The index of the child value to get

        @param[in] use_dynamic
            An enumeration that specifies whether to get dynamic values,
            and also if the target can be run to figure out the dynamic
            type of the child value.

        @param[in] synthetic_allowed
            If true, then allow child values to be created by index
            for pointers and arrays for indexes that normally wouldn't
            be allowed.

        @return
            A new SBValue object that represents the child member value.
        """
    def GetValue(self) -> int: ...

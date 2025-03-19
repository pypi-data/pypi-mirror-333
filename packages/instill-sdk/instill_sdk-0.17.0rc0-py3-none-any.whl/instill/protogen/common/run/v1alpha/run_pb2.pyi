"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.internal.enum_type_wrapper
import sys
import typing

if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class _RunStatus:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _RunStatusEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_RunStatus.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    RUN_STATUS_UNSPECIFIED: _RunStatus.ValueType  # 0
    """Unspecified."""
    RUN_STATUS_PROCESSING: _RunStatus.ValueType  # 1
    """Run in progress."""
    RUN_STATUS_COMPLETED: _RunStatus.ValueType  # 2
    """Run succeeded."""
    RUN_STATUS_FAILED: _RunStatus.ValueType  # 3
    """Run failed."""
    RUN_STATUS_QUEUED: _RunStatus.ValueType  # 4
    """Run is waiting to be executed."""

class RunStatus(_RunStatus, metaclass=_RunStatusEnumTypeWrapper):
    """RunStatus defines the status of a pipeline or model run."""

RUN_STATUS_UNSPECIFIED: RunStatus.ValueType  # 0
"""Unspecified."""
RUN_STATUS_PROCESSING: RunStatus.ValueType  # 1
"""Run in progress."""
RUN_STATUS_COMPLETED: RunStatus.ValueType  # 2
"""Run succeeded."""
RUN_STATUS_FAILED: RunStatus.ValueType  # 3
"""Run failed."""
RUN_STATUS_QUEUED: RunStatus.ValueType  # 4
"""Run is waiting to be executed."""
global___RunStatus = RunStatus

class _RunSource:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _RunSourceEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_RunSource.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    RUN_SOURCE_UNSPECIFIED: _RunSource.ValueType  # 0
    """Unspecified."""
    RUN_SOURCE_CONSOLE: _RunSource.ValueType  # 1
    """Run from frontend UI."""
    RUN_SOURCE_API: _RunSource.ValueType  # 2
    """Run from API or SDK."""

class RunSource(_RunSource, metaclass=_RunSourceEnumTypeWrapper):
    """RunSource defines the source of a pipeline or model run."""

RUN_SOURCE_UNSPECIFIED: RunSource.ValueType  # 0
"""Unspecified."""
RUN_SOURCE_CONSOLE: RunSource.ValueType  # 1
"""Run from frontend UI."""
RUN_SOURCE_API: RunSource.ValueType  # 2
"""Run from API or SDK."""
global___RunSource = RunSource

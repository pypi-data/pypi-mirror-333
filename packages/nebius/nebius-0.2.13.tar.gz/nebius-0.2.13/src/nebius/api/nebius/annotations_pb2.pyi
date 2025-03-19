from google.protobuf import descriptor_pb2 as _descriptor_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ResourceBehavior(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    RESOURCE_BEHAVIOR_UNSPECIFIED: _ClassVar[ResourceBehavior]
    MOVABLE: _ClassVar[ResourceBehavior]
    UNNAMED: _ClassVar[ResourceBehavior]
    IMMUTABLE_NAME: _ClassVar[ResourceBehavior]

class FieldBehavior(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    FIELD_BEHAVIOR_UNSPECIFIED: _ClassVar[FieldBehavior]
    IMMUTABLE: _ClassVar[FieldBehavior]
    IDENTIFIER: _ClassVar[FieldBehavior]
    INPUT_ONLY: _ClassVar[FieldBehavior]
    OUTPUT_ONLY: _ClassVar[FieldBehavior]
    MEANINGFUL_EMPTY_VALUE: _ClassVar[FieldBehavior]
    NON_EMPTY_DEFAULT: _ClassVar[FieldBehavior]
RESOURCE_BEHAVIOR_UNSPECIFIED: ResourceBehavior
MOVABLE: ResourceBehavior
UNNAMED: ResourceBehavior
IMMUTABLE_NAME: ResourceBehavior
FIELD_BEHAVIOR_UNSPECIFIED: FieldBehavior
IMMUTABLE: FieldBehavior
IDENTIFIER: FieldBehavior
INPUT_ONLY: FieldBehavior
OUTPUT_ONLY: FieldBehavior
MEANINGFUL_EMPTY_VALUE: FieldBehavior
NON_EMPTY_DEFAULT: FieldBehavior
API_SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
api_service_name: _descriptor.FieldDescriptor
REGION_ROUTING_FIELD_NUMBER: _ClassVar[int]
region_routing: _descriptor.FieldDescriptor
RESOURCE_BEHAVIOR_FIELD_NUMBER: _ClassVar[int]
resource_behavior: _descriptor.FieldDescriptor
FIELD_BEHAVIOR_FIELD_NUMBER: _ClassVar[int]
field_behavior: _descriptor.FieldDescriptor
SENSITIVE_FIELD_NUMBER: _ClassVar[int]
sensitive: _descriptor.FieldDescriptor
CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
credentials: _descriptor.FieldDescriptor
ONEOF_BEHAVIOR_FIELD_NUMBER: _ClassVar[int]
oneof_behavior: _descriptor.FieldDescriptor

class RegionRouting(_message.Message):
    __slots__ = ["nid", "disabled", "strict"]
    NID_FIELD_NUMBER: _ClassVar[int]
    DISABLED_FIELD_NUMBER: _ClassVar[int]
    STRICT_FIELD_NUMBER: _ClassVar[int]
    nid: _containers.RepeatedScalarFieldContainer[str]
    disabled: bool
    strict: bool
    def __init__(self, nid: _Optional[_Iterable[str]] = ..., disabled: bool = ..., strict: bool = ...) -> None: ...

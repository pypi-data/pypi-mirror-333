# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: nebius/compute/v1/operation_service.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from nebius.api.buf.validate import validate_pb2 as buf_dot_validate_dot_validate__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n)nebius/compute/v1/operation_service.proto\x12\x11nebius.compute.v1\x1a\x1b\x62uf/validate/validate.proto\"\x80\x01\n\x1dListOperationsByParentRequest\x12#\n\tparent_id\x18\x01 \x01(\tB\x06\xbaH\x03\xc8\x01\x01R\x08parentId\x12\x1b\n\tpage_size\x18\x02 \x01(\x03R\x08pageSize\x12\x1d\n\npage_token\x18\x03 \x01(\tR\tpageTokenBd\n\x18\x61i.nebius.pub.compute.v1B\x15OperationServiceProtoP\x01Z/github.com/nebius/gosdk/proto/nebius/compute/v1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'nebius.compute.v1.operation_service_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\030ai.nebius.pub.compute.v1B\025OperationServiceProtoP\001Z/github.com/nebius/gosdk/proto/nebius/compute/v1'
  _LISTOPERATIONSBYPARENTREQUEST.fields_by_name['parent_id']._options = None
  _LISTOPERATIONSBYPARENTREQUEST.fields_by_name['parent_id']._serialized_options = b'\272H\003\310\001\001'
  _globals['_LISTOPERATIONSBYPARENTREQUEST']._serialized_start=94
  _globals['_LISTOPERATIONSBYPARENTREQUEST']._serialized_end=222
# @@protoc_insertion_point(module_scope)

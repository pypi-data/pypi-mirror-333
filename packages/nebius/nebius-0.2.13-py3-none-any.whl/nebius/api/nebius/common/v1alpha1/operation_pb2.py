# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: nebius/common/v1alpha1/operation.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from google.rpc import status_pb2 as google_dot_rpc_dot_status__pb2
from nebius.api.buf.validate import validate_pb2 as buf_dot_validate_dot_validate__pb2
from nebius.api.nebius import annotations_pb2 as nebius_dot_annotations__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n&nebius/common/v1alpha1/operation.proto\x12\x16nebius.common.v1alpha1\x1a\x19google/protobuf/any.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x17google/rpc/status.proto\x1a\x1b\x62uf/validate/validate.proto\x1a\x18nebius/annotations.proto\"\xe5\x05\n\tOperation\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\x12 \n\x0b\x64\x65scription\x18\x02 \x01(\tR\x0b\x64\x65scription\x12\x39\n\ncreated_at\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\tcreatedAt\x12\x1d\n\ncreated_by\x18\x04 \x01(\tR\tcreatedBy\x12;\n\x0b\x66inished_at\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\nfinishedAt\x12.\n\x07request\x18\x06 \x01(\x0b\x32\x14.google.protobuf.AnyR\x07request\x12|\n\x0frequest_headers\x18\x0b \x03(\x0b\x32\x35.nebius.common.v1alpha1.Operation.RequestHeadersEntryB\x1c\xbaH\x19\x9a\x01\x16\"\x14r\x12\x32\x10^[a-z][-a-z\\.]*$R\x0erequestHeaders\x12\x1f\n\x0bresource_id\x18\x07 \x01(\tR\nresourceId\x12\x30\n\x08resource\x18\x08 \x01(\x0b\x32\x14.google.protobuf.AnyR\x08resource\x12\x39\n\rprogress_data\x18\t \x01(\x0b\x32\x14.google.protobuf.AnyR\x0cprogressData\x12\x30\n\x06status\x18\n \x01(\x0b\x32\x12.google.rpc.StatusB\x04\xbaJ\x01\x06R\x06status\x1a(\n\x0erequest_header\x12\x16\n\x06values\x18\x01 \x03(\tR\x06values\x1as\n\x13RequestHeadersEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x46\n\x05value\x18\x02 \x01(\x0b\x32\x30.nebius.common.v1alpha1.Operation.request_headerR\x05value:\x02\x38\x01:\x02\x18\x01\x42j\n\x1d\x61i.nebius.pub.common.v1alpha1B\x0eOperationProtoP\x01Z4github.com/nebius/gosdk/proto/nebius/common/v1alpha1\xb8\x01\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'nebius.common.v1alpha1.operation_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\035ai.nebius.pub.common.v1alpha1B\016OperationProtoP\001Z4github.com/nebius/gosdk/proto/nebius/common/v1alpha1\270\001\001'
  _OPERATION_REQUESTHEADERSENTRY._options = None
  _OPERATION_REQUESTHEADERSENTRY._serialized_options = b'8\001'
  _OPERATION.fields_by_name['request_headers']._options = None
  _OPERATION.fields_by_name['request_headers']._serialized_options = b'\272H\031\232\001\026\"\024r\0222\020^[a-z][-a-z\\.]*$'
  _OPERATION.fields_by_name['status']._options = None
  _OPERATION.fields_by_name['status']._serialized_options = b'\272J\001\006'
  _OPERATION._options = None
  _OPERATION._serialized_options = b'\030\001'
  _globals['_OPERATION']._serialized_start=207
  _globals['_OPERATION']._serialized_end=948
  _globals['_OPERATION_REQUEST_HEADER']._serialized_start=787
  _globals['_OPERATION_REQUEST_HEADER']._serialized_end=827
  _globals['_OPERATION_REQUESTHEADERSENTRY']._serialized_start=829
  _globals['_OPERATION_REQUESTHEADERSENTRY']._serialized_end=944
# @@protoc_insertion_point(module_scope)

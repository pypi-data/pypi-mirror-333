# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: nebius/iam/v1/group.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from nebius.api.buf.validate import validate_pb2 as buf_dot_validate_dot_validate__pb2
from nebius.api.nebius import annotations_pb2 as nebius_dot_annotations__pb2
from nebius.api.nebius.common.v1 import metadata_pb2 as nebius_dot_common_dot_v1_dot_metadata__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x19nebius/iam/v1/group.proto\x12\rnebius.iam.v1\x1a\x1b\x62uf/validate/validate.proto\x1a\x18nebius/annotations.proto\x1a\x1fnebius/common/v1/metadata.proto\"\xbf\x01\n\x05Group\x12\x46\n\x08metadata\x18\x01 \x01(\x0b\x32\".nebius.common.v1.ResourceMetadataB\x06\xbaH\x03\xc8\x01\x01R\x08metadata\x12\x34\n\x04spec\x18\x02 \x01(\x0b\x32\x18.nebius.iam.v1.GroupSpecB\x06\xbaH\x03\xc8\x01\x01R\x04spec\x12\x38\n\x06status\x18\x03 \x01(\x0b\x32\x1a.nebius.iam.v1.GroupStatusB\x04\xbaJ\x01\x05R\x06status\"\x0b\n\tGroupSpec\"\x83\x02\n\x0bGroupStatus\x12\x36\n\x05state\x18\x01 \x01(\x0e\x32 .nebius.iam.v1.GroupStatus.StateR\x05state\x12#\n\rmembers_count\x18\x02 \x01(\x05R\x0cmembersCount\x12\x34\n\x16service_accounts_count\x18\x03 \x01(\x05R\x14serviceAccountsCount\x12;\n\x1atenant_user_accounts_count\x18\x04 \x01(\x05R\x17tenantUserAccountsCount\"$\n\x05State\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\n\n\x06\x41\x43TIVE\x10\x01\x42Q\n\x14\x61i.nebius.pub.iam.v1B\nGroupProtoP\x01Z+github.com/nebius/gosdk/proto/nebius/iam/v1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'nebius.iam.v1.group_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\024ai.nebius.pub.iam.v1B\nGroupProtoP\001Z+github.com/nebius/gosdk/proto/nebius/iam/v1'
  _GROUP.fields_by_name['metadata']._options = None
  _GROUP.fields_by_name['metadata']._serialized_options = b'\272H\003\310\001\001'
  _GROUP.fields_by_name['spec']._options = None
  _GROUP.fields_by_name['spec']._serialized_options = b'\272H\003\310\001\001'
  _GROUP.fields_by_name['status']._options = None
  _GROUP.fields_by_name['status']._serialized_options = b'\272J\001\005'
  _globals['_GROUP']._serialized_start=133
  _globals['_GROUP']._serialized_end=324
  _globals['_GROUPSPEC']._serialized_start=326
  _globals['_GROUPSPEC']._serialized_end=337
  _globals['_GROUPSTATUS']._serialized_start=340
  _globals['_GROUPSTATUS']._serialized_end=599
  _globals['_GROUPSTATUS_STATE']._serialized_start=563
  _globals['_GROUPSTATUS_STATE']._serialized_end=599
# @@protoc_insertion_point(module_scope)

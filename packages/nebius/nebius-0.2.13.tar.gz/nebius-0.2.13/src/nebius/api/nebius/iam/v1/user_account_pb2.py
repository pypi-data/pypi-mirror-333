# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: nebius/iam/v1/user_account.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from nebius.api.nebius import annotations_pb2 as nebius_dot_annotations__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n nebius/iam/v1/user_account.proto\x12\rnebius.iam.v1\x1a\x18nebius/annotations.proto\"~\n\x15UserAccountExternalId\x12@\n\x1a\x66\x65\x64\x65ration_user_account_id\x18\x01 \x01(\tB\x03\xc0J\x01R\x17\x66\x65\x64\x65rationUserAccountId\x12#\n\rfederation_id\x18\x02 \x01(\tR\x0c\x66\x65\x64\x65rationIdBW\n\x14\x61i.nebius.pub.iam.v1B\x10UserAccountProtoP\x01Z+github.com/nebius/gosdk/proto/nebius/iam/v1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'nebius.iam.v1.user_account_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\024ai.nebius.pub.iam.v1B\020UserAccountProtoP\001Z+github.com/nebius/gosdk/proto/nebius/iam/v1'
  _USERACCOUNTEXTERNALID.fields_by_name['federation_user_account_id']._options = None
  _USERACCOUNTEXTERNALID.fields_by_name['federation_user_account_id']._serialized_options = b'\300J\001'
  _globals['_USERACCOUNTEXTERNALID']._serialized_start=77
  _globals['_USERACCOUNTEXTERNALID']._serialized_end=203
# @@protoc_insertion_point(module_scope)

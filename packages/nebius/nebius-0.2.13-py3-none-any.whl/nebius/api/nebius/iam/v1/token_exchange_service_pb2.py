# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: nebius/iam/v1/token_exchange_service.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from nebius.api.nebius import annotations_pb2 as nebius_dot_annotations__pb2
from nebius.api.nebius.iam.v1 import token_service_pb2 as nebius_dot_iam_dot_v1_dot_token__service__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n*nebius/iam/v1/token_exchange_service.proto\x12\rnebius.iam.v1\x1a\x18nebius/annotations.proto\x1a!nebius/iam/v1/token_service.proto2z\n\x14TokenExchangeService\x12S\n\x08\x45xchange\x12#.nebius.iam.v1.ExchangeTokenRequest\x1a\".nebius.iam.v1.CreateTokenResponse\x1a\r\xbaJ\ntokens.iamB`\n\x14\x61i.nebius.pub.iam.v1B\x19TokenExchangeServiceProtoP\x01Z+github.com/nebius/gosdk/proto/nebius/iam/v1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'nebius.iam.v1.token_exchange_service_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\024ai.nebius.pub.iam.v1B\031TokenExchangeServiceProtoP\001Z+github.com/nebius/gosdk/proto/nebius/iam/v1'
  _TOKENEXCHANGESERVICE._options = None
  _TOKENEXCHANGESERVICE._serialized_options = b'\272J\ntokens.iam'
  _globals['_TOKENEXCHANGESERVICE']._serialized_start=122
  _globals['_TOKENEXCHANGESERVICE']._serialized_end=244
# @@protoc_insertion_point(module_scope)

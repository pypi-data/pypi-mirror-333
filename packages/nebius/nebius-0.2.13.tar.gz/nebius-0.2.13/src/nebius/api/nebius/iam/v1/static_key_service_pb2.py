# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: nebius/iam/v1/static_key_service.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from nebius.api.nebius import annotations_pb2 as nebius_dot_annotations__pb2
from nebius.api.nebius.common.v1 import metadata_pb2 as nebius_dot_common_dot_v1_dot_metadata__pb2
from nebius.api.nebius.common.v1 import operation_pb2 as nebius_dot_common_dot_v1_dot_operation__pb2
from nebius.api.nebius.iam.v1 import static_key_pb2 as nebius_dot_iam_dot_v1_dot_static__key__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n&nebius/iam/v1/static_key_service.proto\x12\rnebius.iam.v1\x1a\x18nebius/annotations.proto\x1a\x1fnebius/common/v1/metadata.proto\x1a nebius/common/v1/operation.proto\x1a\x1enebius/iam/v1/static_key.proto\"%\n\x13GetStaticKeyRequest\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\"L\n\x19GetStaticKeyByNameRequest\x12\x1b\n\tparent_id\x18\x01 \x01(\tR\x08parentId\x12\x12\n\x04name\x18\x02 \x01(\tR\x04name\"(\n\x16\x44\x65leteStaticKeyRequest\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\"\x88\x01\n\x15ListStaticKeysRequest\x12\x1b\n\tparent_id\x18\x01 \x01(\tR\x08parentId\x12\x1b\n\tpage_size\x18\x02 \x01(\x03R\x08pageSize\x12\x1d\n\npage_token\x18\x03 \x01(\tR\tpageToken\x12\x16\n\x06\x66ilter\x18\x04 \x01(\tR\x06\x66ilter\"p\n\x16ListStaticKeysResponse\x12.\n\x05items\x18\x01 \x03(\x0b\x32\x18.nebius.iam.v1.StaticKeyR\x05items\x12&\n\x0fnext_page_token\x18\x02 \x01(\tR\rnextPageToken\"\x89\x01\n\x15IssueStaticKeyRequest\x12>\n\x08metadata\x18\x01 \x01(\x0b\x32\".nebius.common.v1.ResourceMetadataR\x08metadata\x12\x30\n\x04spec\x18\x02 \x01(\x0b\x32\x1c.nebius.iam.v1.StaticKeySpecR\x04spec\"n\n\x16IssueStaticKeyResponse\x12\x19\n\x05token\x18\x01 \x01(\tB\x03\xc0J\x01R\x05token\x12\x39\n\toperation\x18\x02 \x01(\x0b\x32\x1b.nebius.common.v1.OperationR\toperation\"1\n\x14\x46indStaticKeyRequest\x12\x19\n\x05token\x18\x01 \x01(\tB\x03\xc0J\x01R\x05token\"P\n\x15\x46indStaticKeyResponse\x12\x37\n\nstatic_key\x18\x01 \x01(\x0b\x32\x18.nebius.iam.v1.StaticKeyR\tstaticKey\"3\n\x16RevokeStaticKeyRequest\x12\x19\n\x05token\x18\x01 \x01(\tB\x03\xc0J\x01R\x05token2\xce\x04\n\x10StaticKeyService\x12T\n\x05Issue\x12$.nebius.iam.v1.IssueStaticKeyRequest\x1a%.nebius.iam.v1.IssueStaticKeyResponse\x12S\n\x04List\x12$.nebius.iam.v1.ListStaticKeysRequest\x1a%.nebius.iam.v1.ListStaticKeysResponse\x12\x43\n\x03Get\x12\".nebius.iam.v1.GetStaticKeyRequest\x1a\x18.nebius.iam.v1.StaticKey\x12O\n\tGetByName\x12(.nebius.iam.v1.GetStaticKeyByNameRequest\x1a\x18.nebius.iam.v1.StaticKey\x12L\n\x06\x44\x65lete\x12%.nebius.iam.v1.DeleteStaticKeyRequest\x1a\x1b.nebius.common.v1.Operation\x12Q\n\x04\x46ind\x12#.nebius.iam.v1.FindStaticKeyRequest\x1a$.nebius.iam.v1.FindStaticKeyResponse\x12L\n\x06Revoke\x12%.nebius.iam.v1.RevokeStaticKeyRequest\x1a\x1b.nebius.common.v1.Operation\x1a\n\xbaJ\x07\x63pl.iamB\\\n\x14\x61i.nebius.pub.iam.v1B\x15StaticKeyServiceProtoP\x01Z+github.com/nebius/gosdk/proto/nebius/iam/v1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'nebius.iam.v1.static_key_service_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\024ai.nebius.pub.iam.v1B\025StaticKeyServiceProtoP\001Z+github.com/nebius/gosdk/proto/nebius/iam/v1'
  _ISSUESTATICKEYRESPONSE.fields_by_name['token']._options = None
  _ISSUESTATICKEYRESPONSE.fields_by_name['token']._serialized_options = b'\300J\001'
  _FINDSTATICKEYREQUEST.fields_by_name['token']._options = None
  _FINDSTATICKEYREQUEST.fields_by_name['token']._serialized_options = b'\300J\001'
  _REVOKESTATICKEYREQUEST.fields_by_name['token']._options = None
  _REVOKESTATICKEYREQUEST.fields_by_name['token']._serialized_options = b'\300J\001'
  _STATICKEYSERVICE._options = None
  _STATICKEYSERVICE._serialized_options = b'\272J\007cpl.iam'
  _globals['_GETSTATICKEYREQUEST']._serialized_start=182
  _globals['_GETSTATICKEYREQUEST']._serialized_end=219
  _globals['_GETSTATICKEYBYNAMEREQUEST']._serialized_start=221
  _globals['_GETSTATICKEYBYNAMEREQUEST']._serialized_end=297
  _globals['_DELETESTATICKEYREQUEST']._serialized_start=299
  _globals['_DELETESTATICKEYREQUEST']._serialized_end=339
  _globals['_LISTSTATICKEYSREQUEST']._serialized_start=342
  _globals['_LISTSTATICKEYSREQUEST']._serialized_end=478
  _globals['_LISTSTATICKEYSRESPONSE']._serialized_start=480
  _globals['_LISTSTATICKEYSRESPONSE']._serialized_end=592
  _globals['_ISSUESTATICKEYREQUEST']._serialized_start=595
  _globals['_ISSUESTATICKEYREQUEST']._serialized_end=732
  _globals['_ISSUESTATICKEYRESPONSE']._serialized_start=734
  _globals['_ISSUESTATICKEYRESPONSE']._serialized_end=844
  _globals['_FINDSTATICKEYREQUEST']._serialized_start=846
  _globals['_FINDSTATICKEYREQUEST']._serialized_end=895
  _globals['_FINDSTATICKEYRESPONSE']._serialized_start=897
  _globals['_FINDSTATICKEYRESPONSE']._serialized_end=977
  _globals['_REVOKESTATICKEYREQUEST']._serialized_start=979
  _globals['_REVOKESTATICKEYREQUEST']._serialized_end=1030
  _globals['_STATICKEYSERVICE']._serialized_start=1033
  _globals['_STATICKEYSERVICE']._serialized_end=1623
# @@protoc_insertion_point(module_scope)

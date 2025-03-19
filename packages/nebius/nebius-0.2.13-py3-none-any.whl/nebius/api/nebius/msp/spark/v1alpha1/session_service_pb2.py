# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: nebius/msp/spark/v1alpha1/session_service.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from nebius.api.buf.validate import validate_pb2 as buf_dot_validate_dot_validate__pb2
from nebius.api.nebius.common.v1 import metadata_pb2 as nebius_dot_common_dot_v1_dot_metadata__pb2
from nebius.api.nebius.common.v1 import operation_pb2 as nebius_dot_common_dot_v1_dot_operation__pb2
from nebius.api.nebius import annotations_pb2 as nebius_dot_annotations__pb2
from nebius.api.nebius.msp.spark.v1alpha1 import session_pb2 as nebius_dot_msp_dot_spark_dot_v1alpha1_dot_session__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n/nebius/msp/spark/v1alpha1/session_service.proto\x12\x19nebius.msp.spark.v1alpha1\x1a\x1b\x62uf/validate/validate.proto\x1a\x1fnebius/common/v1/metadata.proto\x1a nebius/common/v1/operation.proto\x1a\x18nebius/annotations.proto\x1a\'nebius/msp/spark/v1alpha1/session.proto\"+\n\x11GetSessionRequest\x12\x16\n\x02id\x18\x01 \x01(\tB\x06\xbaH\x03\xc8\x01\x01R\x02id\"Z\n\x17GetSessionByNameRequest\x12#\n\tparent_id\x18\x01 \x01(\tB\x06\xbaH\x03\xc8\x01\x01R\x08parentId\x12\x1a\n\x04name\x18\x02 \x01(\tB\x06\xbaH\x03\xc8\x01\x01R\x04name\"\x7f\n\x13ListSessionsRequest\x12#\n\tparent_id\x18\x01 \x01(\tB\x06\xbaH\x03\xc8\x01\x01R\x08parentId\x12$\n\tpage_size\x18\x02 \x01(\x03\x42\x07\xbaH\x04\"\x02(\x00R\x08pageSize\x12\x1d\n\npage_token\x18\x03 \x01(\tR\tpageToken\"\x91\x01\n\x14ListSessionsResponse\x12\x38\n\x05items\x18\x01 \x03(\x0b\x32\".nebius.msp.spark.v1alpha1.SessionR\x05items\x12+\n\x0fnext_page_token\x18\x02 \x01(\tH\x00R\rnextPageToken\x88\x01\x01\x42\x12\n\x10_next_page_token\"\xaa\x02\n\x14\x43reateSessionRequest\x12\x46\n\x08metadata\x18\x01 \x01(\x0b\x32\".nebius.common.v1.ResourceMetadataB\x06\xbaH\x03\xc8\x01\x01R\x08metadata\x12\x42\n\x04spec\x18\x02 \x01(\x0b\x32&.nebius.msp.spark.v1alpha1.SessionSpecB\x06\xbaH\x03\xc8\x01\x01R\x04spec:\x85\x01\xbaH\x81\x01\x1a\x7f\n\x17\x63reate_session.metadata\x12+\'metadata\' must have \'parent_id\' and \'name\'\x1a\x37has(this.metadata.parent_id) && has(this.metadata.name)\".\n\x14\x44\x65leteSessionRequest\x12\x16\n\x02id\x18\x01 \x01(\tB\x06\xbaH\x03\xc8\x01\x01R\x02id2\xf2\x03\n\x0eSessionService\x12W\n\x03Get\x12,.nebius.msp.spark.v1alpha1.GetSessionRequest\x1a\".nebius.msp.spark.v1alpha1.Session\x12\x63\n\tGetByName\x12\x32.nebius.msp.spark.v1alpha1.GetSessionByNameRequest\x1a\".nebius.msp.spark.v1alpha1.Session\x12g\n\x04List\x12..nebius.msp.spark.v1alpha1.ListSessionsRequest\x1a/.nebius.msp.spark.v1alpha1.ListSessionsResponse\x12V\n\x06\x43reate\x12/.nebius.msp.spark.v1alpha1.CreateSessionRequest\x1a\x1b.nebius.common.v1.Operation\x12V\n\x06\x44\x65lete\x12/.nebius.msp.spark.v1alpha1.DeleteSessionRequest\x1a\x1b.nebius.common.v1.Operation\x1a\t\xbaJ\x06sp.mspBr\n ai.nebius.pub.msp.spark.v1alpha1B\x13SessionServiceProtoP\x01Z7github.com/nebius/gosdk/proto/nebius/msp/spark/v1alpha1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'nebius.msp.spark.v1alpha1.session_service_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n ai.nebius.pub.msp.spark.v1alpha1B\023SessionServiceProtoP\001Z7github.com/nebius/gosdk/proto/nebius/msp/spark/v1alpha1'
  _GETSESSIONREQUEST.fields_by_name['id']._options = None
  _GETSESSIONREQUEST.fields_by_name['id']._serialized_options = b'\272H\003\310\001\001'
  _GETSESSIONBYNAMEREQUEST.fields_by_name['parent_id']._options = None
  _GETSESSIONBYNAMEREQUEST.fields_by_name['parent_id']._serialized_options = b'\272H\003\310\001\001'
  _GETSESSIONBYNAMEREQUEST.fields_by_name['name']._options = None
  _GETSESSIONBYNAMEREQUEST.fields_by_name['name']._serialized_options = b'\272H\003\310\001\001'
  _LISTSESSIONSREQUEST.fields_by_name['parent_id']._options = None
  _LISTSESSIONSREQUEST.fields_by_name['parent_id']._serialized_options = b'\272H\003\310\001\001'
  _LISTSESSIONSREQUEST.fields_by_name['page_size']._options = None
  _LISTSESSIONSREQUEST.fields_by_name['page_size']._serialized_options = b'\272H\004\"\002(\000'
  _CREATESESSIONREQUEST.fields_by_name['metadata']._options = None
  _CREATESESSIONREQUEST.fields_by_name['metadata']._serialized_options = b'\272H\003\310\001\001'
  _CREATESESSIONREQUEST.fields_by_name['spec']._options = None
  _CREATESESSIONREQUEST.fields_by_name['spec']._serialized_options = b'\272H\003\310\001\001'
  _CREATESESSIONREQUEST._options = None
  _CREATESESSIONREQUEST._serialized_options = b'\272H\201\001\032\177\n\027create_session.metadata\022+\'metadata\' must have \'parent_id\' and \'name\'\0327has(this.metadata.parent_id) && has(this.metadata.name)'
  _DELETESESSIONREQUEST.fields_by_name['id']._options = None
  _DELETESESSIONREQUEST.fields_by_name['id']._serialized_options = b'\272H\003\310\001\001'
  _SESSIONSERVICE._options = None
  _SESSIONSERVICE._serialized_options = b'\272J\006sp.msp'
  _globals['_GETSESSIONREQUEST']._serialized_start=241
  _globals['_GETSESSIONREQUEST']._serialized_end=284
  _globals['_GETSESSIONBYNAMEREQUEST']._serialized_start=286
  _globals['_GETSESSIONBYNAMEREQUEST']._serialized_end=376
  _globals['_LISTSESSIONSREQUEST']._serialized_start=378
  _globals['_LISTSESSIONSREQUEST']._serialized_end=505
  _globals['_LISTSESSIONSRESPONSE']._serialized_start=508
  _globals['_LISTSESSIONSRESPONSE']._serialized_end=653
  _globals['_CREATESESSIONREQUEST']._serialized_start=656
  _globals['_CREATESESSIONREQUEST']._serialized_end=954
  _globals['_DELETESESSIONREQUEST']._serialized_start=956
  _globals['_DELETESESSIONREQUEST']._serialized_end=1002
  _globals['_SESSIONSERVICE']._serialized_start=1005
  _globals['_SESSIONSERVICE']._serialized_end=1503
# @@protoc_insertion_point(module_scope)

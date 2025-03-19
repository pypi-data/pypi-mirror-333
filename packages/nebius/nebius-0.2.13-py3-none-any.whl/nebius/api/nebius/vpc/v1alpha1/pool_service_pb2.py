# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: nebius/vpc/v1alpha1/pool_service.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from nebius.api.buf.validate import validate_pb2 as buf_dot_validate_dot_validate__pb2
from nebius.api.nebius.vpc.v1alpha1 import pool_pb2 as nebius_dot_vpc_dot_v1alpha1_dot_pool__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n&nebius/vpc/v1alpha1/pool_service.proto\x12\x13nebius.vpc.v1alpha1\x1a\x1b\x62uf/validate/validate.proto\x1a\x1enebius/vpc/v1alpha1/pool.proto\"(\n\x0eGetPoolRequest\x12\x16\n\x02id\x18\x01 \x01(\tB\x06\xbaH\x03\xc8\x01\x01R\x02id\"W\n\x14GetPoolByNameRequest\x12#\n\tparent_id\x18\x01 \x01(\tB\x06\xbaH\x03\xc8\x01\x01R\x08parentId\x12\x1a\n\x04name\x18\x02 \x01(\tB\x06\xbaH\x03\xc8\x01\x01R\x04name\"\x8b\x01\n\x10ListPoolsRequest\x12#\n\tparent_id\x18\x01 \x01(\tB\x06\xbaH\x03\xc8\x01\x01R\x08parentId\x12\x1b\n\tpage_size\x18\x02 \x01(\x03R\x08pageSize\x12\x1d\n\npage_token\x18\x03 \x01(\tR\tpageToken\x12\x16\n\x06\x66ilter\x18\x04 \x01(\tR\x06\x66ilter\"l\n\x11ListPoolsResponse\x12/\n\x05items\x18\x01 \x03(\x0b\x32\x19.nebius.vpc.v1alpha1.PoolR\x05items\x12&\n\x0fnext_page_token\x18\x02 \x01(\tR\rnextPageToken2\xfe\x01\n\x0bPoolService\x12\x45\n\x03Get\x12#.nebius.vpc.v1alpha1.GetPoolRequest\x1a\x19.nebius.vpc.v1alpha1.Pool\x12Q\n\tGetByName\x12).nebius.vpc.v1alpha1.GetPoolByNameRequest\x1a\x19.nebius.vpc.v1alpha1.Pool\x12U\n\x04List\x12%.nebius.vpc.v1alpha1.ListPoolsRequest\x1a&.nebius.vpc.v1alpha1.ListPoolsResponseBc\n\x1a\x61i.nebius.pub.vpc.v1alpha1B\x10PoolServiceProtoP\x01Z1github.com/nebius/gosdk/proto/nebius/vpc/v1alpha1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'nebius.vpc.v1alpha1.pool_service_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\032ai.nebius.pub.vpc.v1alpha1B\020PoolServiceProtoP\001Z1github.com/nebius/gosdk/proto/nebius/vpc/v1alpha1'
  _GETPOOLREQUEST.fields_by_name['id']._options = None
  _GETPOOLREQUEST.fields_by_name['id']._serialized_options = b'\272H\003\310\001\001'
  _GETPOOLBYNAMEREQUEST.fields_by_name['parent_id']._options = None
  _GETPOOLBYNAMEREQUEST.fields_by_name['parent_id']._serialized_options = b'\272H\003\310\001\001'
  _GETPOOLBYNAMEREQUEST.fields_by_name['name']._options = None
  _GETPOOLBYNAMEREQUEST.fields_by_name['name']._serialized_options = b'\272H\003\310\001\001'
  _LISTPOOLSREQUEST.fields_by_name['parent_id']._options = None
  _LISTPOOLSREQUEST.fields_by_name['parent_id']._serialized_options = b'\272H\003\310\001\001'
  _globals['_GETPOOLREQUEST']._serialized_start=124
  _globals['_GETPOOLREQUEST']._serialized_end=164
  _globals['_GETPOOLBYNAMEREQUEST']._serialized_start=166
  _globals['_GETPOOLBYNAMEREQUEST']._serialized_end=253
  _globals['_LISTPOOLSREQUEST']._serialized_start=256
  _globals['_LISTPOOLSREQUEST']._serialized_end=395
  _globals['_LISTPOOLSRESPONSE']._serialized_start=397
  _globals['_LISTPOOLSRESPONSE']._serialized_end=505
  _globals['_POOLSERVICE']._serialized_start=508
  _globals['_POOLSERVICE']._serialized_end=762
# @@protoc_insertion_point(module_scope)

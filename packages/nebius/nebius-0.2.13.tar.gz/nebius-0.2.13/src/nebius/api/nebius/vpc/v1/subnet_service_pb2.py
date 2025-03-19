# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: nebius/vpc/v1/subnet_service.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from nebius.api.buf.validate import validate_pb2 as buf_dot_validate_dot_validate__pb2
from nebius.api.nebius import annotations_pb2 as nebius_dot_annotations__pb2
from nebius.api.nebius.vpc.v1 import subnet_pb2 as nebius_dot_vpc_dot_v1_dot_subnet__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\"nebius/vpc/v1/subnet_service.proto\x12\rnebius.vpc.v1\x1a\x1b\x62uf/validate/validate.proto\x1a\x18nebius/annotations.proto\x1a\x1anebius/vpc/v1/subnet.proto\"*\n\x10GetSubnetRequest\x12\x16\n\x02id\x18\x01 \x01(\tB\x06\xbaH\x03\xc8\x01\x01R\x02id\"Y\n\x16GetSubnetByNameRequest\x12#\n\tparent_id\x18\x01 \x01(\tB\x06\xbaH\x03\xc8\x01\x01R\x08parentId\x12\x1a\n\x04name\x18\x02 \x01(\tB\x06\xbaH\x03\xc8\x01\x01R\x04name\"u\n\x12ListSubnetsRequest\x12#\n\tparent_id\x18\x01 \x01(\tB\x06\xbaH\x03\xc8\x01\x01R\x08parentId\x12\x1b\n\tpage_size\x18\x02 \x01(\x03R\x08pageSize\x12\x1d\n\npage_token\x18\x03 \x01(\tR\tpageToken\"\x80\x01\n\x1bListSubnetsByNetworkRequest\x12%\n\nnetwork_id\x18\x01 \x01(\tB\x06\xbaH\x03\xc8\x01\x01R\tnetworkId\x12\x1b\n\tpage_size\x18\x02 \x01(\x03R\x08pageSize\x12\x1d\n\npage_token\x18\x03 \x01(\tR\tpageToken\"j\n\x13ListSubnetsResponse\x12+\n\x05items\x18\x01 \x03(\x0b\x32\x15.nebius.vpc.v1.SubnetR\x05items\x12&\n\x0fnext_page_token\x18\x02 \x01(\tR\rnextPageToken2\xdb\x02\n\rSubnetService\x12=\n\x03Get\x12\x1f.nebius.vpc.v1.GetSubnetRequest\x1a\x15.nebius.vpc.v1.Subnet\x12I\n\tGetByName\x12%.nebius.vpc.v1.GetSubnetByNameRequest\x1a\x15.nebius.vpc.v1.Subnet\x12M\n\x04List\x12!.nebius.vpc.v1.ListSubnetsRequest\x1a\".nebius.vpc.v1.ListSubnetsResponse\x12q\n\rListByNetwork\x12*.nebius.vpc.v1.ListSubnetsByNetworkRequest\x1a\".nebius.vpc.v1.ListSubnetsResponse\"\x10\x9a\xb5\x18\x0c\n\nnetwork_idBY\n\x14\x61i.nebius.pub.vpc.v1B\x12SubnetServiceProtoP\x01Z+github.com/nebius/gosdk/proto/nebius/vpc/v1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'nebius.vpc.v1.subnet_service_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\024ai.nebius.pub.vpc.v1B\022SubnetServiceProtoP\001Z+github.com/nebius/gosdk/proto/nebius/vpc/v1'
  _GETSUBNETREQUEST.fields_by_name['id']._options = None
  _GETSUBNETREQUEST.fields_by_name['id']._serialized_options = b'\272H\003\310\001\001'
  _GETSUBNETBYNAMEREQUEST.fields_by_name['parent_id']._options = None
  _GETSUBNETBYNAMEREQUEST.fields_by_name['parent_id']._serialized_options = b'\272H\003\310\001\001'
  _GETSUBNETBYNAMEREQUEST.fields_by_name['name']._options = None
  _GETSUBNETBYNAMEREQUEST.fields_by_name['name']._serialized_options = b'\272H\003\310\001\001'
  _LISTSUBNETSREQUEST.fields_by_name['parent_id']._options = None
  _LISTSUBNETSREQUEST.fields_by_name['parent_id']._serialized_options = b'\272H\003\310\001\001'
  _LISTSUBNETSBYNETWORKREQUEST.fields_by_name['network_id']._options = None
  _LISTSUBNETSBYNETWORKREQUEST.fields_by_name['network_id']._serialized_options = b'\272H\003\310\001\001'
  _SUBNETSERVICE.methods_by_name['ListByNetwork']._options = None
  _SUBNETSERVICE.methods_by_name['ListByNetwork']._serialized_options = b'\232\265\030\014\n\nnetwork_id'
  _globals['_GETSUBNETREQUEST']._serialized_start=136
  _globals['_GETSUBNETREQUEST']._serialized_end=178
  _globals['_GETSUBNETBYNAMEREQUEST']._serialized_start=180
  _globals['_GETSUBNETBYNAMEREQUEST']._serialized_end=269
  _globals['_LISTSUBNETSREQUEST']._serialized_start=271
  _globals['_LISTSUBNETSREQUEST']._serialized_end=388
  _globals['_LISTSUBNETSBYNETWORKREQUEST']._serialized_start=391
  _globals['_LISTSUBNETSBYNETWORKREQUEST']._serialized_end=519
  _globals['_LISTSUBNETSRESPONSE']._serialized_start=521
  _globals['_LISTSUBNETSRESPONSE']._serialized_end=627
  _globals['_SUBNETSERVICE']._serialized_start=630
  _globals['_SUBNETSERVICE']._serialized_end=977
# @@protoc_insertion_point(module_scope)

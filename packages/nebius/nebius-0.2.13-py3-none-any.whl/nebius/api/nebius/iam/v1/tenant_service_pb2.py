# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: nebius/iam/v1/tenant_service.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from nebius.api.nebius import annotations_pb2 as nebius_dot_annotations__pb2
from nebius.api.nebius.iam.v1 import container_pb2 as nebius_dot_iam_dot_v1_dot_container__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\"nebius/iam/v1/tenant_service.proto\x12\rnebius.iam.v1\x1a\x18nebius/annotations.proto\x1a\x1dnebius/iam/v1/container.proto\"\"\n\x10GetTenantRequest\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\"{\n\x12ListTenantsRequest\x12 \n\tpage_size\x18\x01 \x01(\x03H\x00R\x08pageSize\x88\x01\x01\x12\x1d\n\npage_token\x18\x02 \x01(\tR\tpageToken\x12\x16\n\x06\x66ilter\x18\x03 \x01(\tR\x06\x66ilterB\x0c\n\n_page_size\"m\n\x13ListTenantsResponse\x12.\n\x05items\x18\x01 \x03(\x0b\x32\x18.nebius.iam.v1.ContainerR\x05items\x12&\n\x0fnext_page_token\x18\x02 \x01(\tR\rnextPageToken2\xac\x01\n\rTenantService\x12@\n\x03Get\x12\x1f.nebius.iam.v1.GetTenantRequest\x1a\x18.nebius.iam.v1.Container\x12M\n\x04List\x12!.nebius.iam.v1.ListTenantsRequest\x1a\".nebius.iam.v1.ListTenantsResponse\x1a\n\xbaJ\x07\x63pl.iamBY\n\x14\x61i.nebius.pub.iam.v1B\x12TenantServiceProtoP\x01Z+github.com/nebius/gosdk/proto/nebius/iam/v1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'nebius.iam.v1.tenant_service_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\024ai.nebius.pub.iam.v1B\022TenantServiceProtoP\001Z+github.com/nebius/gosdk/proto/nebius/iam/v1'
  _TENANTSERVICE._options = None
  _TENANTSERVICE._serialized_options = b'\272J\007cpl.iam'
  _globals['_GETTENANTREQUEST']._serialized_start=110
  _globals['_GETTENANTREQUEST']._serialized_end=144
  _globals['_LISTTENANTSREQUEST']._serialized_start=146
  _globals['_LISTTENANTSREQUEST']._serialized_end=269
  _globals['_LISTTENANTSRESPONSE']._serialized_start=271
  _globals['_LISTTENANTSRESPONSE']._serialized_end=380
  _globals['_TENANTSERVICE']._serialized_start=383
  _globals['_TENANTSERVICE']._serialized_end=555
# @@protoc_insertion_point(module_scope)

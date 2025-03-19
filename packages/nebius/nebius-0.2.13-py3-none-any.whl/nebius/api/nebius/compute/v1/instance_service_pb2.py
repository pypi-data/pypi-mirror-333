# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: nebius/compute/v1/instance_service.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from nebius.api.nebius.common.v1 import metadata_pb2 as nebius_dot_common_dot_v1_dot_metadata__pb2
from nebius.api.nebius.common.v1 import operation_pb2 as nebius_dot_common_dot_v1_dot_operation__pb2
from nebius.api.nebius.common.v1 import operation_service_pb2 as nebius_dot_common_dot_v1_dot_operation__service__pb2
from nebius.api.nebius.compute.v1 import instance_pb2 as nebius_dot_compute_dot_v1_dot_instance__pb2
from nebius.api.nebius.compute.v1 import operation_service_pb2 as nebius_dot_compute_dot_v1_dot_operation__service__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n(nebius/compute/v1/instance_service.proto\x12\x11nebius.compute.v1\x1a\x1fnebius/common/v1/metadata.proto\x1a nebius/common/v1/operation.proto\x1a(nebius/common/v1/operation_service.proto\x1a nebius/compute/v1/instance.proto\x1a)nebius/compute/v1/operation_service.proto\"$\n\x12GetInstanceRequest\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\"o\n\x14ListInstancesRequest\x12\x1b\n\tparent_id\x18\x01 \x01(\tR\x08parentId\x12\x1b\n\tpage_size\x18\x02 \x01(\x03R\x08pageSize\x12\x1d\n\npage_token\x18\x03 \x01(\tR\tpageToken\"\x8c\x01\n\x15\x43reateInstanceRequest\x12>\n\x08metadata\x18\x01 \x01(\x0b\x32\".nebius.common.v1.ResourceMetadataR\x08metadata\x12\x33\n\x04spec\x18\x02 \x01(\x0b\x32\x1f.nebius.compute.v1.InstanceSpecR\x04spec\"\x8c\x01\n\x15UpdateInstanceRequest\x12>\n\x08metadata\x18\x01 \x01(\x0b\x32\".nebius.common.v1.ResourceMetadataR\x08metadata\x12\x33\n\x04spec\x18\x02 \x01(\x0b\x32\x1f.nebius.compute.v1.InstanceSpecR\x04spec\"\'\n\x15\x44\x65leteInstanceRequest\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\"r\n\x15ListInstancesResponse\x12\x31\n\x05items\x18\x01 \x03(\x0b\x32\x1b.nebius.compute.v1.InstanceR\x05items\x12&\n\x0fnext_page_token\x18\x02 \x01(\tR\rnextPageToken\"&\n\x14StartInstanceRequest\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\"%\n\x13StopInstanceRequest\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id2\x8a\x06\n\x0fInstanceService\x12I\n\x03Get\x12%.nebius.compute.v1.GetInstanceRequest\x1a\x1b.nebius.compute.v1.Instance\x12L\n\tGetByName\x12\".nebius.common.v1.GetByNameRequest\x1a\x1b.nebius.compute.v1.Instance\x12Y\n\x04List\x12\'.nebius.compute.v1.ListInstancesRequest\x1a(.nebius.compute.v1.ListInstancesResponse\x12O\n\x06\x43reate\x12(.nebius.compute.v1.CreateInstanceRequest\x1a\x1b.nebius.common.v1.Operation\x12O\n\x06Update\x12(.nebius.compute.v1.UpdateInstanceRequest\x1a\x1b.nebius.common.v1.Operation\x12O\n\x06\x44\x65lete\x12(.nebius.compute.v1.DeleteInstanceRequest\x1a\x1b.nebius.common.v1.Operation\x12M\n\x05Start\x12\'.nebius.compute.v1.StartInstanceRequest\x1a\x1b.nebius.common.v1.Operation\x12K\n\x04Stop\x12&.nebius.compute.v1.StopInstanceRequest\x1a\x1b.nebius.common.v1.Operation\x12t\n\x16ListOperationsByParent\x12\x30.nebius.compute.v1.ListOperationsByParentRequest\x1a(.nebius.common.v1.ListOperationsResponseBc\n\x18\x61i.nebius.pub.compute.v1B\x14InstanceServiceProtoP\x01Z/github.com/nebius/gosdk/proto/nebius/compute/v1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'nebius.compute.v1.instance_service_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\030ai.nebius.pub.compute.v1B\024InstanceServiceProtoP\001Z/github.com/nebius/gosdk/proto/nebius/compute/v1'
  _globals['_GETINSTANCEREQUEST']._serialized_start=249
  _globals['_GETINSTANCEREQUEST']._serialized_end=285
  _globals['_LISTINSTANCESREQUEST']._serialized_start=287
  _globals['_LISTINSTANCESREQUEST']._serialized_end=398
  _globals['_CREATEINSTANCEREQUEST']._serialized_start=401
  _globals['_CREATEINSTANCEREQUEST']._serialized_end=541
  _globals['_UPDATEINSTANCEREQUEST']._serialized_start=544
  _globals['_UPDATEINSTANCEREQUEST']._serialized_end=684
  _globals['_DELETEINSTANCEREQUEST']._serialized_start=686
  _globals['_DELETEINSTANCEREQUEST']._serialized_end=725
  _globals['_LISTINSTANCESRESPONSE']._serialized_start=727
  _globals['_LISTINSTANCESRESPONSE']._serialized_end=841
  _globals['_STARTINSTANCEREQUEST']._serialized_start=843
  _globals['_STARTINSTANCEREQUEST']._serialized_end=881
  _globals['_STOPINSTANCEREQUEST']._serialized_start=883
  _globals['_STOPINSTANCEREQUEST']._serialized_end=920
  _globals['_INSTANCESERVICE']._serialized_start=923
  _globals['_INSTANCESERVICE']._serialized_end=1701
# @@protoc_insertion_point(module_scope)

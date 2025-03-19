# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: nebius/compute/v1/gpu_cluster_service.proto
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
from nebius.api.nebius.compute.v1 import gpu_cluster_pb2 as nebius_dot_compute_dot_v1_dot_gpu__cluster__pb2
from nebius.api.nebius.compute.v1 import operation_service_pb2 as nebius_dot_compute_dot_v1_dot_operation__service__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n+nebius/compute/v1/gpu_cluster_service.proto\x12\x11nebius.compute.v1\x1a\x1fnebius/common/v1/metadata.proto\x1a nebius/common/v1/operation.proto\x1a(nebius/common/v1/operation_service.proto\x1a#nebius/compute/v1/gpu_cluster.proto\x1a)nebius/compute/v1/operation_service.proto\"&\n\x14GetGpuClusterRequest\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\"\x89\x01\n\x16ListGpuClustersRequest\x12\x1b\n\tparent_id\x18\x01 \x01(\tR\x08parentId\x12\x1b\n\tpage_size\x18\x02 \x01(\x03R\x08pageSize\x12\x1d\n\npage_token\x18\x03 \x01(\tR\tpageToken\x12\x16\n\x06\x66ilter\x18\x04 \x01(\tR\x06\x66ilter\"\x90\x01\n\x17\x43reateGpuClusterRequest\x12>\n\x08metadata\x18\x01 \x01(\x0b\x32\".nebius.common.v1.ResourceMetadataR\x08metadata\x12\x35\n\x04spec\x18\x02 \x01(\x0b\x32!.nebius.compute.v1.GpuClusterSpecR\x04spec\"\x90\x01\n\x17UpdateGpuClusterRequest\x12>\n\x08metadata\x18\x01 \x01(\x0b\x32\".nebius.common.v1.ResourceMetadataR\x08metadata\x12\x35\n\x04spec\x18\x02 \x01(\x0b\x32!.nebius.compute.v1.GpuClusterSpecR\x04spec\")\n\x17\x44\x65leteGpuClusterRequest\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\"v\n\x17ListGpuClustersResponse\x12\x33\n\x05items\x18\x01 \x03(\x0b\x32\x1d.nebius.compute.v1.GpuClusterR\x05items\x12&\n\x0fnext_page_token\x18\x02 \x01(\tR\rnextPageToken2\x80\x05\n\x11GpuClusterService\x12M\n\x03Get\x12\'.nebius.compute.v1.GetGpuClusterRequest\x1a\x1d.nebius.compute.v1.GpuCluster\x12N\n\tGetByName\x12\".nebius.common.v1.GetByNameRequest\x1a\x1d.nebius.compute.v1.GpuCluster\x12]\n\x04List\x12).nebius.compute.v1.ListGpuClustersRequest\x1a*.nebius.compute.v1.ListGpuClustersResponse\x12Q\n\x06\x43reate\x12*.nebius.compute.v1.CreateGpuClusterRequest\x1a\x1b.nebius.common.v1.Operation\x12Q\n\x06Update\x12*.nebius.compute.v1.UpdateGpuClusterRequest\x1a\x1b.nebius.common.v1.Operation\x12Q\n\x06\x44\x65lete\x12*.nebius.compute.v1.DeleteGpuClusterRequest\x1a\x1b.nebius.common.v1.Operation\x12t\n\x16ListOperationsByParent\x12\x30.nebius.compute.v1.ListOperationsByParentRequest\x1a(.nebius.common.v1.ListOperationsResponseBe\n\x18\x61i.nebius.pub.compute.v1B\x16GpuClusterServiceProtoP\x01Z/github.com/nebius/gosdk/proto/nebius/compute/v1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'nebius.compute.v1.gpu_cluster_service_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\030ai.nebius.pub.compute.v1B\026GpuClusterServiceProtoP\001Z/github.com/nebius/gosdk/proto/nebius/compute/v1'
  _globals['_GETGPUCLUSTERREQUEST']._serialized_start=255
  _globals['_GETGPUCLUSTERREQUEST']._serialized_end=293
  _globals['_LISTGPUCLUSTERSREQUEST']._serialized_start=296
  _globals['_LISTGPUCLUSTERSREQUEST']._serialized_end=433
  _globals['_CREATEGPUCLUSTERREQUEST']._serialized_start=436
  _globals['_CREATEGPUCLUSTERREQUEST']._serialized_end=580
  _globals['_UPDATEGPUCLUSTERREQUEST']._serialized_start=583
  _globals['_UPDATEGPUCLUSTERREQUEST']._serialized_end=727
  _globals['_DELETEGPUCLUSTERREQUEST']._serialized_start=729
  _globals['_DELETEGPUCLUSTERREQUEST']._serialized_end=770
  _globals['_LISTGPUCLUSTERSRESPONSE']._serialized_start=772
  _globals['_LISTGPUCLUSTERSRESPONSE']._serialized_end=890
  _globals['_GPUCLUSTERSERVICE']._serialized_start=893
  _globals['_GPUCLUSTERSERVICE']._serialized_end=1533
# @@protoc_insertion_point(module_scope)

# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: nebius/compute/v1/gpu_cluster.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from nebius.api.buf.validate import validate_pb2 as buf_dot_validate_dot_validate__pb2
from nebius.api.nebius.common.v1 import metadata_pb2 as nebius_dot_common_dot_v1_dot_metadata__pb2
from nebius.api.nebius import annotations_pb2 as nebius_dot_annotations__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n#nebius/compute/v1/gpu_cluster.proto\x12\x11nebius.compute.v1\x1a\x1b\x62uf/validate/validate.proto\x1a\x1fnebius/common/v1/metadata.proto\x1a\x18nebius/annotations.proto\"\xc0\x01\n\nGpuCluster\x12>\n\x08metadata\x18\x01 \x01(\x0b\x32\".nebius.common.v1.ResourceMetadataR\x08metadata\x12\x35\n\x04spec\x18\x02 \x01(\x0b\x32!.nebius.compute.v1.GpuClusterSpecR\x04spec\x12;\n\x06status\x18\x03 \x01(\x0b\x32#.nebius.compute.v1.GpuClusterStatusR\x06status\"I\n\x0eGpuClusterSpec\x12\x37\n\x11infiniband_fabric\x18\x01 \x01(\tB\n\xbaH\x03\xc8\x01\x01\xbaJ\x01\x02R\x10infinibandFabric\"R\n\x10GpuClusterStatus\x12\x1c\n\tinstances\x18\x01 \x03(\tR\tinstances\x12 \n\x0breconciling\x18\x02 \x01(\x08R\x0breconcilingB^\n\x18\x61i.nebius.pub.compute.v1B\x0fGpuClusterProtoP\x01Z/github.com/nebius/gosdk/proto/nebius/compute/v1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'nebius.compute.v1.gpu_cluster_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\030ai.nebius.pub.compute.v1B\017GpuClusterProtoP\001Z/github.com/nebius/gosdk/proto/nebius/compute/v1'
  _GPUCLUSTERSPEC.fields_by_name['infiniband_fabric']._options = None
  _GPUCLUSTERSPEC.fields_by_name['infiniband_fabric']._serialized_options = b'\272H\003\310\001\001\272J\001\002'
  _globals['_GPUCLUSTER']._serialized_start=147
  _globals['_GPUCLUSTER']._serialized_end=339
  _globals['_GPUCLUSTERSPEC']._serialized_start=341
  _globals['_GPUCLUSTERSPEC']._serialized_end=414
  _globals['_GPUCLUSTERSTATUS']._serialized_start=416
  _globals['_GPUCLUSTERSTATUS']._serialized_end=498
# @@protoc_insertion_point(module_scope)

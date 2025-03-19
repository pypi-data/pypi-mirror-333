# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: nebius/mk8s/v1/cluster.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from nebius.api.buf.validate import validate_pb2 as buf_dot_validate_dot_validate__pb2
from nebius.api.nebius import annotations_pb2 as nebius_dot_annotations__pb2
from nebius.api.nebius.common.v1 import metadata_pb2 as nebius_dot_common_dot_v1_dot_metadata__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1cnebius/mk8s/v1/cluster.proto\x12\x0enebius.mk8s.v1\x1a\x1b\x62uf/validate/validate.proto\x1a\x18nebius/annotations.proto\x1a\x1fnebius/common/v1/metadata.proto\"\xb1\x01\n\x07\x43luster\x12>\n\x08metadata\x18\x01 \x01(\x0b\x32\".nebius.common.v1.ResourceMetadataR\x08metadata\x12/\n\x04spec\x18\x02 \x01(\x0b\x32\x1b.nebius.mk8s.v1.ClusterSpecR\x04spec\x12\x35\n\x06status\x18\x03 \x01(\x0b\x32\x1d.nebius.mk8s.v1.ClusterStatusR\x06status\"\xa0\x01\n\x0b\x43lusterSpec\x12M\n\rcontrol_plane\x18\x02 \x01(\x0b\x32 .nebius.mk8s.v1.ControlPlaneSpecB\x06\xbaH\x03\xc8\x01\x01R\x0c\x63ontrolPlane\x12\x42\n\x0ckube_network\x18\x03 \x01(\x0b\x32\x1f.nebius.mk8s.v1.KubeNetworkSpecR\x0bkubeNetwork\"\xeb\x01\n\x10\x43ontrolPlaneSpec\x12,\n\x07version\x18\x01 \x01(\tB\x12\xbaH\x0fr\r2\x0b|^\\d\\.\\d\\d$R\x07version\x12\'\n\tsubnet_id\x18\x02 \x01(\tB\n\xbaH\x03\xc8\x01\x01\xbaJ\x01\x02R\x08subnetId\x12G\n\tendpoints\x18\x03 \x01(\x0b\x32).nebius.mk8s.v1.ControlPlaneEndpointsSpecR\tendpoints\x12\x37\n\x11\x65tcd_cluster_size\x18\x04 \x01(\x03\x42\x0b\xbaH\x08\"\x06\x30\x00\x30\x01\x30\x03R\x0f\x65tcdClusterSize\"n\n\x19\x43ontrolPlaneEndpointsSpec\x12Q\n\x0fpublic_endpoint\x18\x01 \x01(\x0b\x32\".nebius.mk8s.v1.PublicEndpointSpecB\x04\xbaJ\x01\x06R\x0epublicEndpoint\"\x14\n\x12PublicEndpointSpec\"\xd1\x01\n\x0fKubeNetworkSpec\x12\xbd\x01\n\rservice_cidrs\x18\x01 \x03(\tB\x97\x01\xbaH\x8f\x01\xba\x01\x86\x01\n\x11string.valid_cidr\x12?value must be a CIDR block or prefix length from \"/12\" to \"/28\"\x1a\x30this.all(x, x.matches(\'^(.*)/(1[2-9]|2[0-8])$\'))\x92\x01\x02\x10\x01\xbaJ\x01\x02R\x0cserviceCidrs\"\x82\x02\n\rClusterStatus\x12\x39\n\x05state\x18\x01 \x01(\x0e\x32#.nebius.mk8s.v1.ClusterStatus.StateR\x05state\x12G\n\rcontrol_plane\x18\x02 \x01(\x0b\x32\".nebius.mk8s.v1.ControlPlaneStatusR\x0c\x63ontrolPlane\x12 \n\x0breconciling\x18\x64 \x01(\x08R\x0breconciling\"K\n\x05State\x12\x15\n\x11STATE_UNSPECIFIED\x10\x00\x12\x10\n\x0cPROVISIONING\x10\x01\x12\x0b\n\x07RUNNING\x10\x02\x12\x0c\n\x08\x44\x45LETING\x10\x03\"\xe1\x01\n\x12\x43ontrolPlaneStatus\x12\x18\n\x07version\x18\x01 \x01(\tR\x07version\x12I\n\tendpoints\x18\x02 \x01(\x0b\x32+.nebius.mk8s.v1.ControlPlaneStatusEndpointsR\tendpoints\x12*\n\x11\x65tcd_cluster_size\x18\x03 \x01(\x03R\x0f\x65tcdClusterSize\x12:\n\x04\x61uth\x18\x64 \x01(\x0b\x32&.nebius.mk8s.v1.ControlPlaneStatusAuthR\x04\x61uth\"q\n\x1b\x43ontrolPlaneStatusEndpoints\x12\'\n\x0fpublic_endpoint\x18\x01 \x01(\tR\x0epublicEndpoint\x12)\n\x10private_endpoint\x18\x02 \x01(\tR\x0fprivateEndpoint\"N\n\x16\x43ontrolPlaneStatusAuth\x12\x34\n\x16\x63luster_ca_certificate\x18\x01 \x01(\tR\x14\x63lusterCaCertificateBU\n\x15\x61i.nebius.pub.mk8s.v1B\x0c\x43lusterProtoP\x01Z,github.com/nebius/gosdk/proto/nebius/mk8s/v1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'nebius.mk8s.v1.cluster_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\025ai.nebius.pub.mk8s.v1B\014ClusterProtoP\001Z,github.com/nebius/gosdk/proto/nebius/mk8s/v1'
  _CLUSTERSPEC.fields_by_name['control_plane']._options = None
  _CLUSTERSPEC.fields_by_name['control_plane']._serialized_options = b'\272H\003\310\001\001'
  _CONTROLPLANESPEC.fields_by_name['version']._options = None
  _CONTROLPLANESPEC.fields_by_name['version']._serialized_options = b'\272H\017r\r2\013|^\\d\\.\\d\\d$'
  _CONTROLPLANESPEC.fields_by_name['subnet_id']._options = None
  _CONTROLPLANESPEC.fields_by_name['subnet_id']._serialized_options = b'\272H\003\310\001\001\272J\001\002'
  _CONTROLPLANESPEC.fields_by_name['etcd_cluster_size']._options = None
  _CONTROLPLANESPEC.fields_by_name['etcd_cluster_size']._serialized_options = b'\272H\010\"\0060\0000\0010\003'
  _CONTROLPLANEENDPOINTSSPEC.fields_by_name['public_endpoint']._options = None
  _CONTROLPLANEENDPOINTSSPEC.fields_by_name['public_endpoint']._serialized_options = b'\272J\001\006'
  _KUBENETWORKSPEC.fields_by_name['service_cidrs']._options = None
  _KUBENETWORKSPEC.fields_by_name['service_cidrs']._serialized_options = b'\272H\217\001\272\001\206\001\n\021string.valid_cidr\022?value must be a CIDR block or prefix length from \"/12\" to \"/28\"\0320this.all(x, x.matches(\'^(.*)/(1[2-9]|2[0-8])$\'))\222\001\002\020\001\272J\001\002'
  _globals['_CLUSTER']._serialized_start=137
  _globals['_CLUSTER']._serialized_end=314
  _globals['_CLUSTERSPEC']._serialized_start=317
  _globals['_CLUSTERSPEC']._serialized_end=477
  _globals['_CONTROLPLANESPEC']._serialized_start=480
  _globals['_CONTROLPLANESPEC']._serialized_end=715
  _globals['_CONTROLPLANEENDPOINTSSPEC']._serialized_start=717
  _globals['_CONTROLPLANEENDPOINTSSPEC']._serialized_end=827
  _globals['_PUBLICENDPOINTSPEC']._serialized_start=829
  _globals['_PUBLICENDPOINTSPEC']._serialized_end=849
  _globals['_KUBENETWORKSPEC']._serialized_start=852
  _globals['_KUBENETWORKSPEC']._serialized_end=1061
  _globals['_CLUSTERSTATUS']._serialized_start=1064
  _globals['_CLUSTERSTATUS']._serialized_end=1322
  _globals['_CLUSTERSTATUS_STATE']._serialized_start=1247
  _globals['_CLUSTERSTATUS_STATE']._serialized_end=1322
  _globals['_CONTROLPLANESTATUS']._serialized_start=1325
  _globals['_CONTROLPLANESTATUS']._serialized_end=1550
  _globals['_CONTROLPLANESTATUSENDPOINTS']._serialized_start=1552
  _globals['_CONTROLPLANESTATUSENDPOINTS']._serialized_end=1665
  _globals['_CONTROLPLANESTATUSAUTH']._serialized_start=1667
  _globals['_CONTROLPLANESTATUSAUTH']._serialized_end=1745
# @@protoc_insertion_point(module_scope)

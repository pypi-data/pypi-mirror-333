# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: nebius/mk8s/v1/node_group.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from nebius.api.buf.validate import validate_pb2 as buf_dot_validate_dot_validate__pb2
from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
from nebius.api.nebius import annotations_pb2 as nebius_dot_annotations__pb2
from nebius.api.nebius.common.v1 import metadata_pb2 as nebius_dot_common_dot_v1_dot_metadata__pb2
from nebius.api.nebius.mk8s.v1 import instance_template_pb2 as nebius_dot_mk8s_dot_v1_dot_instance__template__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1fnebius/mk8s/v1/node_group.proto\x12\x0enebius.mk8s.v1\x1a\x1b\x62uf/validate/validate.proto\x1a\x1egoogle/protobuf/duration.proto\x1a\x18nebius/annotations.proto\x1a\x1fnebius/common/v1/metadata.proto\x1a&nebius/mk8s/v1/instance_template.proto\"\xb7\x01\n\tNodeGroup\x12>\n\x08metadata\x18\x01 \x01(\x0b\x32\".nebius.common.v1.ResourceMetadataR\x08metadata\x12\x31\n\x04spec\x18\x02 \x01(\x0b\x32\x1d.nebius.mk8s.v1.NodeGroupSpecR\x04spec\x12\x37\n\x06status\x18\x03 \x01(\x0b\x32\x1f.nebius.mk8s.v1.NodeGroupStatusR\x06status\"\xdc\x02\n\rNodeGroupSpec\x12,\n\x07version\x18\x01 \x01(\tB\x12\xbaH\x0fr\r2\x0b|^\\d\\.\\d\\d$R\x07version\x12\x35\n\x10\x66ixed_node_count\x18\x02 \x01(\x03\x42\t\xbaH\x06\"\x04\x18\x64(\x00H\x00R\x0e\x66ixedNodeCount\x12L\n\x0b\x61utoscaling\x18\x05 \x01(\x0b\x32(.nebius.mk8s.v1.NodeGroupAutoscalingSpecH\x00R\x0b\x61utoscaling\x12@\n\x08template\x18\x03 \x01(\x0b\x32\x1c.nebius.mk8s.v1.NodeTemplateB\x06\xbaH\x03\xc8\x01\x01R\x08template\x12G\n\x08strategy\x18\x04 \x01(\x0b\x32+.nebius.mk8s.v1.NodeGroupDeploymentStrategyR\x08strategyB\r\n\x04size\x12\x05\xbaH\x02\x08\x01\"\x9d\x05\n\x0cNodeTemplate\x12@\n\x08metadata\x18\x01 \x01(\x0b\x32$.nebius.mk8s.v1.NodeMetadataTemplateR\x08metadata\x12;\n\x06taints\x18\x02 \x03(\x0b\x32\x19.nebius.mk8s.v1.NodeTaintB\x08\xbaH\x05\x92\x01\x02\x10\x64R\x06taints\x12\x43\n\tresources\x18\x03 \x01(\x0b\x32\x1d.nebius.mk8s.v1.ResourcesSpecB\x06\xbaH\x03\xc8\x01\x01R\tresources\x12;\n\tboot_disk\x18\t \x01(\x0b\x32\x18.nebius.mk8s.v1.DiskSpecB\x04\xbaJ\x01\x07R\x08\x62ootDisk\x12>\n\x0cgpu_settings\x18\r \x01(\x0b\x32\x1b.nebius.mk8s.v1.GpuSettingsR\x0bgpuSettings\x12?\n\x0bgpu_cluster\x18\x04 \x01(\x0b\x32\x1e.nebius.mk8s.v1.GpuClusterSpecR\ngpuCluster\x12]\n\x12network_interfaces\x18\x05 \x03(\x0b\x32(.nebius.mk8s.v1.NetworkInterfaceTemplateB\x04\xbaJ\x01\x07R\x11networkInterfaces\x12H\n\x0b\x66ilesystems\x18\x07 \x03(\x0b\x32&.nebius.mk8s.v1.AttachedFilesystemSpecR\x0b\x66ilesystems\x12\x34\n\x14\x63loud_init_user_data\x18\x06 \x01(\tB\x03\xc0J\x01R\x11\x63loudInitUserData\x12,\n\x12service_account_id\x18\n \x01(\tR\x10serviceAccountId\"\xa5\x01\n\x14NodeMetadataTemplate\x12R\n\x06labels\x18\x01 \x03(\x0b\x32\x30.nebius.mk8s.v1.NodeMetadataTemplate.LabelsEntryB\x08\xbaH\x05\x9a\x01\x02\x10\x64R\x06labels\x1a\x39\n\x0bLabelsEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x14\n\x05value\x18\x02 \x01(\tR\x05value:\x02\x38\x01\"<\n\x0bGpuSettings\x12-\n\x0e\x64rivers_preset\x18\x01 \x01(\tB\x06\xbaH\x03\xc8\x01\x01R\rdriversPreset\" \n\x0eGpuClusterSpec\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\"\x90\x01\n\x18NetworkInterfaceTemplate\x12Q\n\x11public_ip_address\x18\x01 \x01(\x0b\x32\x1f.nebius.mk8s.v1.PublicIPAddressB\x04\xbaJ\x01\x06R\x0fpublicIpAddress\x12!\n\tsubnet_id\x18\x03 \x01(\tB\x04\xbaJ\x01\x07R\x08subnetId\"\x11\n\x0fPublicIPAddress\"\xbd\x02\n\x16\x41ttachedFilesystemSpec\x12Z\n\x0b\x61ttach_mode\x18\x01 \x01(\x0e\x32\x31.nebius.mk8s.v1.AttachedFilesystemSpec.AttachModeB\x06\xbaH\x03\xc8\x01\x01R\nattachMode\x12#\n\tmount_tag\x18\x02 \x01(\tB\x06\xbaH\x03\xc8\x01\x01R\x08mountTag\x12U\n\x13\x65xisting_filesystem\x18\x03 \x01(\x0b\x32\".nebius.mk8s.v1.ExistingFilesystemH\x00R\x12\x65xistingFilesystem\"<\n\nAttachMode\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\r\n\tREAD_ONLY\x10\x01\x12\x0e\n\nREAD_WRITE\x10\x02\x42\r\n\x04type\x12\x05\xbaH\x02\x08\x01\",\n\x12\x45xistingFilesystem\x12\x16\n\x02id\x18\x01 \x01(\tB\x06\xbaH\x03\xc8\x01\x01R\x02id\"\x8f\x02\n\x18NodeGroupAutoscalingSpec\x12/\n\x0emin_node_count\x18\x01 \x01(\x03\x42\t\xbaH\x06\"\x04\x18\x64(\x00R\x0cminNodeCount\x12/\n\x0emax_node_count\x18\x02 \x01(\x03\x42\t\xbaH\x06\"\x04\x18\x64(\x00R\x0cmaxNodeCount:\x90\x01\xbaH\x8c\x01\x1a\x89\x01\n!autoscaling.protovalidate.message\x12\x38min_node_count must be less or equal than max_node_count\x1a*this.min_node_count <= this.max_node_count\"\xe0\x01\n\tNodeTaint\x12\x18\n\x03key\x18\x01 \x01(\tB\x06\xbaH\x03\xc8\x01\x01R\x03key\x12\x1c\n\x05value\x18\x02 \x01(\tB\x06\xbaH\x03\xc8\x01\x01R\x05value\x12@\n\x06\x65\x66\x66\x65\x63t\x18\x03 \x01(\x0e\x32 .nebius.mk8s.v1.NodeTaint.EffectB\x06\xbaH\x03\xc8\x01\x01R\x06\x65\x66\x66\x65\x63t\"Y\n\x06\x45\x66\x66\x65\x63t\x12\x16\n\x12\x45\x46\x46\x45\x43T_UNSPECIFIED\x10\x00\x12\x0e\n\nNO_EXECUTE\x10\x01\x12\x0f\n\x0bNO_SCHEDULE\x10\x02\x12\x16\n\x12PREFER_NO_SCHEDULE\x10\x03\"\xed\x01\n\x1bNodeGroupDeploymentStrategy\x12G\n\x0fmax_unavailable\x18\x01 \x01(\x0b\x32\x1e.nebius.mk8s.v1.PercentOrCountR\x0emaxUnavailable\x12;\n\tmax_surge\x18\x02 \x01(\x0b\x32\x1e.nebius.mk8s.v1.PercentOrCountR\x08maxSurge\x12H\n\rdrain_timeout\x18\x03 \x01(\x0b\x32\x19.google.protobuf.DurationB\x08\xbaH\x05\xaa\x01\x02\x32\x00R\x0c\x64rainTimeout\"h\n\x0ePercentOrCount\x12%\n\x07percent\x18\x01 \x01(\x03\x42\t\xbaH\x06\"\x04\x18\x64(\x00H\x00R\x07percent\x12\x1f\n\x05\x63ount\x18\x02 \x01(\x03\x42\x07\xbaH\x04\"\x02(\x00H\x00R\x05\x63ountB\x0e\n\x05value\x12\x05\xbaH\x02\x08\x01\"\xfc\x02\n\x0fNodeGroupStatus\x12;\n\x05state\x18\x01 \x01(\x0e\x32%.nebius.mk8s.v1.NodeGroupStatus.StateR\x05state\x12\x18\n\x07version\x18\x02 \x01(\tR\x07version\x12*\n\x11target_node_count\x18\x03 \x01(\x03R\x0ftargetNodeCount\x12\x1d\n\nnode_count\x18\x04 \x01(\x03R\tnodeCount\x12.\n\x13outdated_node_count\x18\x05 \x01(\x03R\x11outdatedNodeCount\x12(\n\x10ready_node_count\x18\x06 \x01(\x03R\x0ereadyNodeCount\x12 \n\x0breconciling\x18\x64 \x01(\x08R\x0breconciling\"K\n\x05State\x12\x15\n\x11STATE_UNSPECIFIED\x10\x00\x12\x10\n\x0cPROVISIONING\x10\x01\x12\x0b\n\x07RUNNING\x10\x02\x12\x0c\n\x08\x44\x45LETING\x10\x03\x42W\n\x15\x61i.nebius.pub.mk8s.v1B\x0eNodeGroupProtoP\x01Z,github.com/nebius/gosdk/proto/nebius/mk8s/v1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'nebius.mk8s.v1.node_group_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\025ai.nebius.pub.mk8s.v1B\016NodeGroupProtoP\001Z,github.com/nebius/gosdk/proto/nebius/mk8s/v1'
  _NODEGROUPSPEC.oneofs_by_name['size']._options = None
  _NODEGROUPSPEC.oneofs_by_name['size']._serialized_options = b'\272H\002\010\001'
  _NODEGROUPSPEC.fields_by_name['version']._options = None
  _NODEGROUPSPEC.fields_by_name['version']._serialized_options = b'\272H\017r\r2\013|^\\d\\.\\d\\d$'
  _NODEGROUPSPEC.fields_by_name['fixed_node_count']._options = None
  _NODEGROUPSPEC.fields_by_name['fixed_node_count']._serialized_options = b'\272H\006\"\004\030d(\000'
  _NODEGROUPSPEC.fields_by_name['template']._options = None
  _NODEGROUPSPEC.fields_by_name['template']._serialized_options = b'\272H\003\310\001\001'
  _NODETEMPLATE.fields_by_name['taints']._options = None
  _NODETEMPLATE.fields_by_name['taints']._serialized_options = b'\272H\005\222\001\002\020d'
  _NODETEMPLATE.fields_by_name['resources']._options = None
  _NODETEMPLATE.fields_by_name['resources']._serialized_options = b'\272H\003\310\001\001'
  _NODETEMPLATE.fields_by_name['boot_disk']._options = None
  _NODETEMPLATE.fields_by_name['boot_disk']._serialized_options = b'\272J\001\007'
  _NODETEMPLATE.fields_by_name['network_interfaces']._options = None
  _NODETEMPLATE.fields_by_name['network_interfaces']._serialized_options = b'\272J\001\007'
  _NODETEMPLATE.fields_by_name['cloud_init_user_data']._options = None
  _NODETEMPLATE.fields_by_name['cloud_init_user_data']._serialized_options = b'\300J\001'
  _NODEMETADATATEMPLATE_LABELSENTRY._options = None
  _NODEMETADATATEMPLATE_LABELSENTRY._serialized_options = b'8\001'
  _NODEMETADATATEMPLATE.fields_by_name['labels']._options = None
  _NODEMETADATATEMPLATE.fields_by_name['labels']._serialized_options = b'\272H\005\232\001\002\020d'
  _GPUSETTINGS.fields_by_name['drivers_preset']._options = None
  _GPUSETTINGS.fields_by_name['drivers_preset']._serialized_options = b'\272H\003\310\001\001'
  _NETWORKINTERFACETEMPLATE.fields_by_name['public_ip_address']._options = None
  _NETWORKINTERFACETEMPLATE.fields_by_name['public_ip_address']._serialized_options = b'\272J\001\006'
  _NETWORKINTERFACETEMPLATE.fields_by_name['subnet_id']._options = None
  _NETWORKINTERFACETEMPLATE.fields_by_name['subnet_id']._serialized_options = b'\272J\001\007'
  _ATTACHEDFILESYSTEMSPEC.oneofs_by_name['type']._options = None
  _ATTACHEDFILESYSTEMSPEC.oneofs_by_name['type']._serialized_options = b'\272H\002\010\001'
  _ATTACHEDFILESYSTEMSPEC.fields_by_name['attach_mode']._options = None
  _ATTACHEDFILESYSTEMSPEC.fields_by_name['attach_mode']._serialized_options = b'\272H\003\310\001\001'
  _ATTACHEDFILESYSTEMSPEC.fields_by_name['mount_tag']._options = None
  _ATTACHEDFILESYSTEMSPEC.fields_by_name['mount_tag']._serialized_options = b'\272H\003\310\001\001'
  _EXISTINGFILESYSTEM.fields_by_name['id']._options = None
  _EXISTINGFILESYSTEM.fields_by_name['id']._serialized_options = b'\272H\003\310\001\001'
  _NODEGROUPAUTOSCALINGSPEC.fields_by_name['min_node_count']._options = None
  _NODEGROUPAUTOSCALINGSPEC.fields_by_name['min_node_count']._serialized_options = b'\272H\006\"\004\030d(\000'
  _NODEGROUPAUTOSCALINGSPEC.fields_by_name['max_node_count']._options = None
  _NODEGROUPAUTOSCALINGSPEC.fields_by_name['max_node_count']._serialized_options = b'\272H\006\"\004\030d(\000'
  _NODEGROUPAUTOSCALINGSPEC._options = None
  _NODEGROUPAUTOSCALINGSPEC._serialized_options = b'\272H\214\001\032\211\001\n!autoscaling.protovalidate.message\0228min_node_count must be less or equal than max_node_count\032*this.min_node_count <= this.max_node_count'
  _NODETAINT.fields_by_name['key']._options = None
  _NODETAINT.fields_by_name['key']._serialized_options = b'\272H\003\310\001\001'
  _NODETAINT.fields_by_name['value']._options = None
  _NODETAINT.fields_by_name['value']._serialized_options = b'\272H\003\310\001\001'
  _NODETAINT.fields_by_name['effect']._options = None
  _NODETAINT.fields_by_name['effect']._serialized_options = b'\272H\003\310\001\001'
  _NODEGROUPDEPLOYMENTSTRATEGY.fields_by_name['drain_timeout']._options = None
  _NODEGROUPDEPLOYMENTSTRATEGY.fields_by_name['drain_timeout']._serialized_options = b'\272H\005\252\001\0022\000'
  _PERCENTORCOUNT.oneofs_by_name['value']._options = None
  _PERCENTORCOUNT.oneofs_by_name['value']._serialized_options = b'\272H\002\010\001'
  _PERCENTORCOUNT.fields_by_name['percent']._options = None
  _PERCENTORCOUNT.fields_by_name['percent']._serialized_options = b'\272H\006\"\004\030d(\000'
  _PERCENTORCOUNT.fields_by_name['count']._options = None
  _PERCENTORCOUNT.fields_by_name['count']._serialized_options = b'\272H\004\"\002(\000'
  _globals['_NODEGROUP']._serialized_start=212
  _globals['_NODEGROUP']._serialized_end=395
  _globals['_NODEGROUPSPEC']._serialized_start=398
  _globals['_NODEGROUPSPEC']._serialized_end=746
  _globals['_NODETEMPLATE']._serialized_start=749
  _globals['_NODETEMPLATE']._serialized_end=1418
  _globals['_NODEMETADATATEMPLATE']._serialized_start=1421
  _globals['_NODEMETADATATEMPLATE']._serialized_end=1586
  _globals['_NODEMETADATATEMPLATE_LABELSENTRY']._serialized_start=1529
  _globals['_NODEMETADATATEMPLATE_LABELSENTRY']._serialized_end=1586
  _globals['_GPUSETTINGS']._serialized_start=1588
  _globals['_GPUSETTINGS']._serialized_end=1648
  _globals['_GPUCLUSTERSPEC']._serialized_start=1650
  _globals['_GPUCLUSTERSPEC']._serialized_end=1682
  _globals['_NETWORKINTERFACETEMPLATE']._serialized_start=1685
  _globals['_NETWORKINTERFACETEMPLATE']._serialized_end=1829
  _globals['_PUBLICIPADDRESS']._serialized_start=1831
  _globals['_PUBLICIPADDRESS']._serialized_end=1848
  _globals['_ATTACHEDFILESYSTEMSPEC']._serialized_start=1851
  _globals['_ATTACHEDFILESYSTEMSPEC']._serialized_end=2168
  _globals['_ATTACHEDFILESYSTEMSPEC_ATTACHMODE']._serialized_start=2093
  _globals['_ATTACHEDFILESYSTEMSPEC_ATTACHMODE']._serialized_end=2153
  _globals['_EXISTINGFILESYSTEM']._serialized_start=2170
  _globals['_EXISTINGFILESYSTEM']._serialized_end=2214
  _globals['_NODEGROUPAUTOSCALINGSPEC']._serialized_start=2217
  _globals['_NODEGROUPAUTOSCALINGSPEC']._serialized_end=2488
  _globals['_NODETAINT']._serialized_start=2491
  _globals['_NODETAINT']._serialized_end=2715
  _globals['_NODETAINT_EFFECT']._serialized_start=2626
  _globals['_NODETAINT_EFFECT']._serialized_end=2715
  _globals['_NODEGROUPDEPLOYMENTSTRATEGY']._serialized_start=2718
  _globals['_NODEGROUPDEPLOYMENTSTRATEGY']._serialized_end=2955
  _globals['_PERCENTORCOUNT']._serialized_start=2957
  _globals['_PERCENTORCOUNT']._serialized_end=3061
  _globals['_NODEGROUPSTATUS']._serialized_start=3064
  _globals['_NODEGROUPSTATUS']._serialized_end=3444
  _globals['_NODEGROUPSTATUS_STATE']._serialized_start=3369
  _globals['_NODEGROUPSTATUS_STATE']._serialized_end=3444
# @@protoc_insertion_point(module_scope)

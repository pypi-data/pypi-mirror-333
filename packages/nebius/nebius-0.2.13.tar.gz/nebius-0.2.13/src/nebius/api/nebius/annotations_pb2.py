# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: nebius/annotations.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import descriptor_pb2 as google_dot_protobuf_dot_descriptor__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x18nebius/annotations.proto\x12\x06nebius\x1a google/protobuf/descriptor.proto\"U\n\rRegionRouting\x12\x10\n\x03nid\x18\x01 \x03(\tR\x03nid\x12\x1a\n\x08\x64isabled\x18\x02 \x01(\x08R\x08\x64isabled\x12\x16\n\x06strict\x18\x03 \x01(\x08R\x06strict*c\n\x10ResourceBehavior\x12!\n\x1dRESOURCE_BEHAVIOR_UNSPECIFIED\x10\x00\x12\x0b\n\x07MOVABLE\x10\x01\x12\x0b\n\x07UNNAMED\x10\x02\x12\x12\n\x0eIMMUTABLE_NAME\x10\x03*\xa2\x01\n\rFieldBehavior\x12\x1e\n\x1a\x46IELD_BEHAVIOR_UNSPECIFIED\x10\x00\x12\r\n\tIMMUTABLE\x10\x02\x12\x0e\n\nIDENTIFIER\x10\x03\x12\x0e\n\nINPUT_ONLY\x10\x04\x12\x0f\n\x0bOUTPUT_ONLY\x10\x05\x12\x1a\n\x16MEANINGFUL_EMPTY_VALUE\x10\x06\x12\x15\n\x11NON_EMPTY_DEFAULT\x10\x07:J\n\x10\x61pi_service_name\x12\x1f.google.protobuf.ServiceOptions\x18\xa7\t \x01(\tR\x0e\x61piServiceName:^\n\x0eregion_routing\x12\x1e.google.protobuf.MethodOptions\x18\xd3\x86\x03 \x01(\x0b\x32\x15.nebius.RegionRoutingR\rregionRouting:g\n\x11resource_behavior\x12\x1f.google.protobuf.MessageOptions\x18\xa7\t \x03(\x0e\x32\x18.nebius.ResourceBehaviorR\x10resourceBehavior:\\\n\x0e\x66ield_behavior\x12\x1d.google.protobuf.FieldOptions\x18\xa7\t \x03(\x0e\x32\x15.nebius.FieldBehaviorR\rfieldBehavior:<\n\tsensitive\x12\x1d.google.protobuf.FieldOptions\x18\xa8\t \x01(\x08R\tsensitive:@\n\x0b\x63redentials\x12\x1d.google.protobuf.FieldOptions\x18\xa9\t \x01(\x08R\x0b\x63redentials:\\\n\x0eoneof_behavior\x12\x1d.google.protobuf.OneofOptions\x18\xa7\t \x03(\x0e\x32\x15.nebius.FieldBehaviorR\roneofBehaviorBI\n\rai.nebius.pubB\x10\x41nnotationsProtoP\x01Z$github.com/nebius/gosdk/proto/nebiusb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'nebius.annotations_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  google_dot_protobuf_dot_descriptor__pb2.ServiceOptions.RegisterExtension(api_service_name)
  google_dot_protobuf_dot_descriptor__pb2.MethodOptions.RegisterExtension(region_routing)
  google_dot_protobuf_dot_descriptor__pb2.MessageOptions.RegisterExtension(resource_behavior)
  google_dot_protobuf_dot_descriptor__pb2.FieldOptions.RegisterExtension(field_behavior)
  google_dot_protobuf_dot_descriptor__pb2.FieldOptions.RegisterExtension(sensitive)
  google_dot_protobuf_dot_descriptor__pb2.FieldOptions.RegisterExtension(credentials)
  google_dot_protobuf_dot_descriptor__pb2.OneofOptions.RegisterExtension(oneof_behavior)

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\rai.nebius.pubB\020AnnotationsProtoP\001Z$github.com/nebius/gosdk/proto/nebius'
  _globals['_RESOURCEBEHAVIOR']._serialized_start=157
  _globals['_RESOURCEBEHAVIOR']._serialized_end=256
  _globals['_FIELDBEHAVIOR']._serialized_start=259
  _globals['_FIELDBEHAVIOR']._serialized_end=421
  _globals['_REGIONROUTING']._serialized_start=70
  _globals['_REGIONROUTING']._serialized_end=155
# @@protoc_insertion_point(module_scope)

# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: nebius/storage/v1/bucket_counters.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from nebius.api.nebius.storage.v1 import base_pb2 as nebius_dot_storage_dot_v1_dot_base__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\'nebius/storage/v1/bucket_counters.proto\x12\x11nebius.storage.v1\x1a\x1cnebius/storage/v1/base.proto\"\x99\x03\n\x15\x43urrentBucketCounters\x12\x36\n\x17simple_objects_quantity\x18\x01 \x01(\x03R\x15simpleObjectsQuantity\x12.\n\x13simple_objects_size\x18\x02 \x01(\x03R\x11simpleObjectsSize\x12<\n\x1amultipart_objects_quantity\x18\x03 \x01(\x03R\x18multipartObjectsQuantity\x12\x34\n\x16multipart_objects_size\x18\x04 \x01(\x03R\x14multipartObjectsSize\x12<\n\x1amultipart_uploads_quantity\x18\x05 \x01(\x03R\x18multipartUploadsQuantity\x12\x36\n\x17inflight_parts_quantity\x18\x06 \x01(\x03R\x15inflightPartsQuantity\x12.\n\x13inflight_parts_size\x18\x07 \x01(\x03R\x11inflightPartsSize\"\xf6\x01\n\x18NonCurrentBucketCounters\x12\x36\n\x17simple_objects_quantity\x18\x01 \x01(\x03R\x15simpleObjectsQuantity\x12.\n\x13simple_objects_size\x18\x02 \x01(\x03R\x11simpleObjectsSize\x12<\n\x1amultipart_objects_quantity\x18\x03 \x01(\x03R\x18multipartObjectsQuantity\x12\x34\n\x16multipart_objects_size\x18\x04 \x01(\x03R\x14multipartObjectsSize\"\xfb\x01\n\x0e\x42ucketCounters\x12\x44\n\rstorage_class\x18\x01 \x01(\x0e\x32\x1f.nebius.storage.v1.StorageClassR\x0cstorageClass\x12\x44\n\x08\x63ounters\x18\x02 \x01(\x0b\x32(.nebius.storage.v1.CurrentBucketCountersR\x08\x63ounters\x12]\n\x14non_current_counters\x18\x03 \x01(\x0b\x32+.nebius.storage.v1.NonCurrentBucketCountersR\x12nonCurrentCountersBb\n\x18\x61i.nebius.pub.storage.v1B\x13\x42ucketCountersProtoP\x01Z/github.com/nebius/gosdk/proto/nebius/storage/v1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'nebius.storage.v1.bucket_counters_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\030ai.nebius.pub.storage.v1B\023BucketCountersProtoP\001Z/github.com/nebius/gosdk/proto/nebius/storage/v1'
  _globals['_CURRENTBUCKETCOUNTERS']._serialized_start=93
  _globals['_CURRENTBUCKETCOUNTERS']._serialized_end=502
  _globals['_NONCURRENTBUCKETCOUNTERS']._serialized_start=505
  _globals['_NONCURRENTBUCKETCOUNTERS']._serialized_end=751
  _globals['_BUCKETCOUNTERS']._serialized_start=754
  _globals['_BUCKETCOUNTERS']._serialized_end=1005
# @@protoc_insertion_point(module_scope)

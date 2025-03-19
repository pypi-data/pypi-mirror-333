# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: nebius/common/error/v1alpha1/error.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from nebius.api.nebius.common.error.v1alpha1 import common_errors_pb2 as nebius_dot_common_dot_error_dot_v1alpha1_dot_common__errors__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n(nebius/common/error/v1alpha1/error.proto\x12\x1cnebius.common.error.v1alpha1\x1a\x30nebius/common/error/v1alpha1/common_errors.proto\"\xd9\t\n\x0cServiceError\x12\x18\n\x07service\x18\x01 \x01(\tR\x07service\x12\x12\n\x04\x63ode\x18\x02 \x01(\tR\x04\x63ode\x12K\n\x0b\x62\x61\x64_request\x18\x64 \x01(\x0b\x32(.nebius.common.error.v1alpha1.BadRequestH\x00R\nbadRequest\x12^\n\x12\x62\x61\x64_resource_state\x18n \x01(\x0b\x32..nebius.common.error.v1alpha1.BadResourceStateH\x00R\x10\x62\x61\x64ResourceState\x12^\n\x12resource_not_found\x18o \x01(\x0b\x32..nebius.common.error.v1alpha1.ResourceNotFoundH\x00R\x10resourceNotFound\x12m\n\x17resource_already_exists\x18p \x01(\x0b\x32\x33.nebius.common.error.v1alpha1.ResourceAlreadyExistsH\x00R\x15resourceAlreadyExists\x12L\n\x0cout_of_range\x18q \x01(\x0b\x32(.nebius.common.error.v1alpha1.OutOfRangeH\x00R\noutOfRange\x12]\n\x11permission_denied\x18x \x01(\x0b\x32..nebius.common.error.v1alpha1.PermissionDeniedH\x00R\x10permissionDenied\x12^\n\x11resource_conflict\x18\x82\x01 \x01(\x0b\x32..nebius.common.error.v1alpha1.ResourceConflictH\x00R\x10resourceConflict\x12^\n\x11operation_aborted\x18\x83\x01 \x01(\x0b\x32..nebius.common.error.v1alpha1.OperationAbortedH\x00R\x10operationAborted\x12\\\n\x11too_many_requests\x18\x8c\x01 \x01(\x0b\x32-.nebius.common.error.v1alpha1.TooManyRequestsH\x00R\x0ftooManyRequests\x12R\n\rquota_failure\x18\x8d\x01 \x01(\x0b\x32*.nebius.common.error.v1alpha1.QuotaFailureH\x00R\x0cquotaFailure\x12U\n\x0einternal_error\x18\xe7\x07 \x01(\x0b\x32+.nebius.common.error.v1alpha1.InternalErrorH\x00R\rinternalError\x12S\n\nretry_type\x18\x1e \x01(\x0e\x32\x34.nebius.common.error.v1alpha1.ServiceError.RetryTypeR\tretryType\"E\n\tRetryType\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x08\n\x04\x43\x41LL\x10\x01\x12\x10\n\x0cUNIT_OF_WORK\x10\x02\x12\x0b\n\x07NOTHING\x10\x03:\x02\x18\x01\x42\t\n\x07\x64\x65tailsBr\n#ai.nebius.pub.common.error.v1alpha1B\nErrorProtoP\x01Z:github.com/nebius/gosdk/proto/nebius/common/error/v1alpha1\xb8\x01\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'nebius.common.error.v1alpha1.error_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n#ai.nebius.pub.common.error.v1alpha1B\nErrorProtoP\001Z:github.com/nebius/gosdk/proto/nebius/common/error/v1alpha1\270\001\001'
  _SERVICEERROR._options = None
  _SERVICEERROR._serialized_options = b'\030\001'
  _globals['_SERVICEERROR']._serialized_start=125
  _globals['_SERVICEERROR']._serialized_end=1366
  _globals['_SERVICEERROR_RETRYTYPE']._serialized_start=1282
  _globals['_SERVICEERROR_RETRYTYPE']._serialized_end=1351
# @@protoc_insertion_point(module_scope)

# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: nebius/common/v1/error.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1cnebius/common/v1/error.proto\x12\x10nebius.common.v1\"\xa0\t\n\x0cServiceError\x12\x18\n\x07service\x18\x01 \x01(\tR\x07service\x12\x12\n\x04\x63ode\x18\x02 \x01(\tR\x04\x63ode\x12?\n\x0b\x62\x61\x64_request\x18\x64 \x01(\x0b\x32\x1c.nebius.common.v1.BadRequestH\x00R\nbadRequest\x12R\n\x12\x62\x61\x64_resource_state\x18n \x01(\x0b\x32\".nebius.common.v1.BadResourceStateH\x00R\x10\x62\x61\x64ResourceState\x12R\n\x12resource_not_found\x18o \x01(\x0b\x32\".nebius.common.v1.ResourceNotFoundH\x00R\x10resourceNotFound\x12\x61\n\x17resource_already_exists\x18p \x01(\x0b\x32\'.nebius.common.v1.ResourceAlreadyExistsH\x00R\x15resourceAlreadyExists\x12@\n\x0cout_of_range\x18q \x01(\x0b\x32\x1c.nebius.common.v1.OutOfRangeH\x00R\noutOfRange\x12Q\n\x11permission_denied\x18x \x01(\x0b\x32\".nebius.common.v1.PermissionDeniedH\x00R\x10permissionDenied\x12R\n\x11resource_conflict\x18\x82\x01 \x01(\x0b\x32\".nebius.common.v1.ResourceConflictH\x00R\x10resourceConflict\x12R\n\x11operation_aborted\x18\x83\x01 \x01(\x0b\x32\".nebius.common.v1.OperationAbortedH\x00R\x10operationAborted\x12P\n\x11too_many_requests\x18\x8c\x01 \x01(\x0b\x32!.nebius.common.v1.TooManyRequestsH\x00R\x0ftooManyRequests\x12\x46\n\rquota_failure\x18\x8d\x01 \x01(\x0b\x32\x1e.nebius.common.v1.QuotaFailureH\x00R\x0cquotaFailure\x12Y\n\x14not_enough_resources\x18\x8e\x01 \x01(\x0b\x32$.nebius.common.v1.NotEnoughResourcesH\x00R\x12notEnoughResources\x12I\n\x0einternal_error\x18\xe7\x07 \x01(\x0b\x32\x1f.nebius.common.v1.InternalErrorH\x00R\rinternalError\x12G\n\nretry_type\x18\x1e \x01(\x0e\x32(.nebius.common.v1.ServiceError.RetryTypeR\tretryType\"E\n\tRetryType\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x08\n\x04\x43\x41LL\x10\x01\x12\x10\n\x0cUNIT_OF_WORK\x10\x02\x12\x0b\n\x07NOTHING\x10\x03\x42\t\n\x07\x64\x65tails\"\x91\x01\n\nBadRequest\x12\x46\n\nviolations\x18\x01 \x03(\x0b\x32&.nebius.common.v1.BadRequest.ViolationR\nviolations\x1a;\n\tViolation\x12\x14\n\x05\x66ield\x18\x01 \x01(\tR\x05\x66ield\x12\x18\n\x07message\x18\x02 \x01(\tR\x07message\"M\n\x10\x42\x61\x64ResourceState\x12\x1f\n\x0bresource_id\x18\x01 \x01(\tR\nresourceId\x12\x18\n\x07message\x18\x02 \x01(\tR\x07message\"3\n\x10ResourceNotFound\x12\x1f\n\x0bresource_id\x18\x01 \x01(\tR\nresourceId\"8\n\x15ResourceAlreadyExists\x12\x1f\n\x0bresource_id\x18\x01 \x01(\tR\nresourceId\"M\n\x10ResourceConflict\x12\x1f\n\x0bresource_id\x18\x01 \x01(\tR\nresourceId\x12\x18\n\x07message\x18\x02 \x01(\tR\x07message\"\x8d\x01\n\x10OperationAborted\x12!\n\x0coperation_id\x18\x01 \x01(\tR\x0boperationId\x12\x35\n\x17\x61\x62orted_by_operation_id\x18\x02 \x01(\tR\x14\x61\x62ortedByOperationId\x12\x1f\n\x0bresource_id\x18\x03 \x01(\tR\nresourceId\"@\n\nOutOfRange\x12\x1c\n\trequested\x18\x01 \x01(\tR\trequested\x12\x14\n\x05limit\x18\x02 \x01(\tR\x05limit\"3\n\x10PermissionDenied\x12\x1f\n\x0bresource_id\x18\x01 \x01(\tR\nresourceId\"I\n\rInternalError\x12\x1d\n\nrequest_id\x18\x01 \x01(\tR\trequestId\x12\x19\n\x08trace_id\x18\x02 \x01(\tR\x07traceId\"/\n\x0fTooManyRequests\x12\x1c\n\tviolation\x18\x01 \x01(\tR\tviolation\"\xc9\x01\n\x0cQuotaFailure\x12H\n\nviolations\x18\x01 \x03(\x0b\x32(.nebius.common.v1.QuotaFailure.ViolationR\nviolations\x1ao\n\tViolation\x12\x14\n\x05quota\x18\x01 \x01(\tR\x05quota\x12\x18\n\x07message\x18\x02 \x01(\tR\x07message\x12\x14\n\x05limit\x18\x03 \x01(\tR\x05limit\x12\x1c\n\trequested\x18\x04 \x01(\tR\trequested\"\xce\x01\n\x12NotEnoughResources\x12N\n\nviolations\x18\x01 \x03(\x0b\x32..nebius.common.v1.NotEnoughResources.ViolationR\nviolations\x1ah\n\tViolation\x12#\n\rresource_type\x18\x01 \x01(\tR\x0cresourceType\x12\x18\n\x07message\x18\x02 \x01(\tR\x07message\x12\x1c\n\trequested\x18\x03 \x01(\tR\trequestedBW\n\x17\x61i.nebius.pub.common.v1B\nErrorProtoP\x01Z.github.com/nebius/gosdk/proto/nebius/common/v1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'nebius.common.v1.error_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\027ai.nebius.pub.common.v1B\nErrorProtoP\001Z.github.com/nebius/gosdk/proto/nebius/common/v1'
  _globals['_SERVICEERROR']._serialized_start=51
  _globals['_SERVICEERROR']._serialized_end=1235
  _globals['_SERVICEERROR_RETRYTYPE']._serialized_start=1155
  _globals['_SERVICEERROR_RETRYTYPE']._serialized_end=1224
  _globals['_BADREQUEST']._serialized_start=1238
  _globals['_BADREQUEST']._serialized_end=1383
  _globals['_BADREQUEST_VIOLATION']._serialized_start=1324
  _globals['_BADREQUEST_VIOLATION']._serialized_end=1383
  _globals['_BADRESOURCESTATE']._serialized_start=1385
  _globals['_BADRESOURCESTATE']._serialized_end=1462
  _globals['_RESOURCENOTFOUND']._serialized_start=1464
  _globals['_RESOURCENOTFOUND']._serialized_end=1515
  _globals['_RESOURCEALREADYEXISTS']._serialized_start=1517
  _globals['_RESOURCEALREADYEXISTS']._serialized_end=1573
  _globals['_RESOURCECONFLICT']._serialized_start=1575
  _globals['_RESOURCECONFLICT']._serialized_end=1652
  _globals['_OPERATIONABORTED']._serialized_start=1655
  _globals['_OPERATIONABORTED']._serialized_end=1796
  _globals['_OUTOFRANGE']._serialized_start=1798
  _globals['_OUTOFRANGE']._serialized_end=1862
  _globals['_PERMISSIONDENIED']._serialized_start=1864
  _globals['_PERMISSIONDENIED']._serialized_end=1915
  _globals['_INTERNALERROR']._serialized_start=1917
  _globals['_INTERNALERROR']._serialized_end=1990
  _globals['_TOOMANYREQUESTS']._serialized_start=1992
  _globals['_TOOMANYREQUESTS']._serialized_end=2039
  _globals['_QUOTAFAILURE']._serialized_start=2042
  _globals['_QUOTAFAILURE']._serialized_end=2243
  _globals['_QUOTAFAILURE_VIOLATION']._serialized_start=2132
  _globals['_QUOTAFAILURE_VIOLATION']._serialized_end=2243
  _globals['_NOTENOUGHRESOURCES']._serialized_start=2246
  _globals['_NOTENOUGHRESOURCES']._serialized_end=2452
  _globals['_NOTENOUGHRESOURCES_VIOLATION']._serialized_start=2348
  _globals['_NOTENOUGHRESOURCES_VIOLATION']._serialized_end=2452
# @@protoc_insertion_point(module_scope)

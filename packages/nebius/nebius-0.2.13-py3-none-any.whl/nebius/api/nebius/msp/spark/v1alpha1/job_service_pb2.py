# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: nebius/msp/spark/v1alpha1/job_service.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from nebius.api.buf.validate import validate_pb2 as buf_dot_validate_dot_validate__pb2
from nebius.api.nebius.common.v1 import metadata_pb2 as nebius_dot_common_dot_v1_dot_metadata__pb2
from nebius.api.nebius.common.v1 import operation_pb2 as nebius_dot_common_dot_v1_dot_operation__pb2
from nebius.api.nebius import annotations_pb2 as nebius_dot_annotations__pb2
from nebius.api.nebius.msp.spark.v1alpha1 import job_pb2 as nebius_dot_msp_dot_spark_dot_v1alpha1_dot_job__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n+nebius/msp/spark/v1alpha1/job_service.proto\x12\x19nebius.msp.spark.v1alpha1\x1a\x1b\x62uf/validate/validate.proto\x1a\x1fnebius/common/v1/metadata.proto\x1a nebius/common/v1/operation.proto\x1a\x18nebius/annotations.proto\x1a#nebius/msp/spark/v1alpha1/job.proto\"\'\n\rGetJobRequest\x12\x16\n\x02id\x18\x01 \x01(\tB\x06\xbaH\x03\xc8\x01\x01R\x02id\"{\n\x0fListJobsRequest\x12#\n\tparent_id\x18\x01 \x01(\tB\x06\xbaH\x03\xc8\x01\x01R\x08parentId\x12$\n\tpage_size\x18\x02 \x01(\x03\x42\x07\xbaH\x04\"\x02(\x00R\x08pageSize\x12\x1d\n\npage_token\x18\x03 \x01(\tR\tpageToken\"\x89\x01\n\x10ListJobsResponse\x12\x34\n\x05items\x18\x01 \x03(\x0b\x32\x1e.nebius.msp.spark.v1alpha1.JobR\x05items\x12+\n\x0fnext_page_token\x18\x02 \x01(\tH\x00R\rnextPageToken\x88\x01\x01\x42\x12\n\x10_next_page_token\"\x9d\x02\n\x10\x43reateJobRequest\x12\x46\n\x08metadata\x18\x01 \x01(\x0b\x32\".nebius.common.v1.ResourceMetadataB\x06\xbaH\x03\xc8\x01\x01R\x08metadata\x12>\n\x04spec\x18\x02 \x01(\x0b\x32\".nebius.msp.spark.v1alpha1.JobSpecB\x06\xbaH\x03\xc8\x01\x01R\x04spec:\x80\x01\xbaH}\x1a{\n\x13\x63reate_job.metadata\x12+\'metadata\' must have \'parent_id\' and \'name\'\x1a\x37has(this.metadata.parent_id) && has(this.metadata.name)\"*\n\x10\x43\x61ncelJobRequest\x12\x16\n\x02id\x18\x01 \x01(\tB\x06\xbaH\x03\xc8\x01\x01R\x02id2\xf1\x02\n\nJobService\x12O\n\x03Get\x12(.nebius.msp.spark.v1alpha1.GetJobRequest\x1a\x1e.nebius.msp.spark.v1alpha1.Job\x12_\n\x04List\x12*.nebius.msp.spark.v1alpha1.ListJobsRequest\x1a+.nebius.msp.spark.v1alpha1.ListJobsResponse\x12R\n\x06\x43reate\x12+.nebius.msp.spark.v1alpha1.CreateJobRequest\x1a\x1b.nebius.common.v1.Operation\x12R\n\x06\x43\x61ncel\x12+.nebius.msp.spark.v1alpha1.CancelJobRequest\x1a\x1b.nebius.common.v1.Operation\x1a\t\xbaJ\x06sp.mspBn\n ai.nebius.pub.msp.spark.v1alpha1B\x0fJobServiceProtoP\x01Z7github.com/nebius/gosdk/proto/nebius/msp/spark/v1alpha1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'nebius.msp.spark.v1alpha1.job_service_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n ai.nebius.pub.msp.spark.v1alpha1B\017JobServiceProtoP\001Z7github.com/nebius/gosdk/proto/nebius/msp/spark/v1alpha1'
  _GETJOBREQUEST.fields_by_name['id']._options = None
  _GETJOBREQUEST.fields_by_name['id']._serialized_options = b'\272H\003\310\001\001'
  _LISTJOBSREQUEST.fields_by_name['parent_id']._options = None
  _LISTJOBSREQUEST.fields_by_name['parent_id']._serialized_options = b'\272H\003\310\001\001'
  _LISTJOBSREQUEST.fields_by_name['page_size']._options = None
  _LISTJOBSREQUEST.fields_by_name['page_size']._serialized_options = b'\272H\004\"\002(\000'
  _CREATEJOBREQUEST.fields_by_name['metadata']._options = None
  _CREATEJOBREQUEST.fields_by_name['metadata']._serialized_options = b'\272H\003\310\001\001'
  _CREATEJOBREQUEST.fields_by_name['spec']._options = None
  _CREATEJOBREQUEST.fields_by_name['spec']._serialized_options = b'\272H\003\310\001\001'
  _CREATEJOBREQUEST._options = None
  _CREATEJOBREQUEST._serialized_options = b'\272H}\032{\n\023create_job.metadata\022+\'metadata\' must have \'parent_id\' and \'name\'\0327has(this.metadata.parent_id) && has(this.metadata.name)'
  _CANCELJOBREQUEST.fields_by_name['id']._options = None
  _CANCELJOBREQUEST.fields_by_name['id']._serialized_options = b'\272H\003\310\001\001'
  _JOBSERVICE._options = None
  _JOBSERVICE._serialized_options = b'\272J\006sp.msp'
  _globals['_GETJOBREQUEST']._serialized_start=233
  _globals['_GETJOBREQUEST']._serialized_end=272
  _globals['_LISTJOBSREQUEST']._serialized_start=274
  _globals['_LISTJOBSREQUEST']._serialized_end=397
  _globals['_LISTJOBSRESPONSE']._serialized_start=400
  _globals['_LISTJOBSRESPONSE']._serialized_end=537
  _globals['_CREATEJOBREQUEST']._serialized_start=540
  _globals['_CREATEJOBREQUEST']._serialized_end=825
  _globals['_CANCELJOBREQUEST']._serialized_start=827
  _globals['_CANCELJOBREQUEST']._serialized_end=869
  _globals['_JOBSERVICE']._serialized_start=872
  _globals['_JOBSERVICE']._serialized_end=1241
# @@protoc_insertion_point(module_scope)

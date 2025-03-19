# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from nebius.api.nebius.common.v1 import operation_pb2 as nebius_dot_common_dot_v1_dot_operation__pb2
from nebius.api.nebius.storage.v1 import bucket_pb2 as nebius_dot_storage_dot_v1_dot_bucket__pb2
from nebius.api.nebius.storage.v1 import bucket_service_pb2 as nebius_dot_storage_dot_v1_dot_bucket__service__pb2


class BucketServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Get = channel.unary_unary(
                '/nebius.storage.v1.BucketService/Get',
                request_serializer=nebius_dot_storage_dot_v1_dot_bucket__service__pb2.GetBucketRequest.SerializeToString,
                response_deserializer=nebius_dot_storage_dot_v1_dot_bucket__pb2.Bucket.FromString,
                )
        self.GetByName = channel.unary_unary(
                '/nebius.storage.v1.BucketService/GetByName',
                request_serializer=nebius_dot_storage_dot_v1_dot_bucket__service__pb2.GetBucketByNameRequest.SerializeToString,
                response_deserializer=nebius_dot_storage_dot_v1_dot_bucket__pb2.Bucket.FromString,
                )
        self.List = channel.unary_unary(
                '/nebius.storage.v1.BucketService/List',
                request_serializer=nebius_dot_storage_dot_v1_dot_bucket__service__pb2.ListBucketsRequest.SerializeToString,
                response_deserializer=nebius_dot_storage_dot_v1_dot_bucket__service__pb2.ListBucketsResponse.FromString,
                )
        self.Create = channel.unary_unary(
                '/nebius.storage.v1.BucketService/Create',
                request_serializer=nebius_dot_storage_dot_v1_dot_bucket__service__pb2.CreateBucketRequest.SerializeToString,
                response_deserializer=nebius_dot_common_dot_v1_dot_operation__pb2.Operation.FromString,
                )
        self.Update = channel.unary_unary(
                '/nebius.storage.v1.BucketService/Update',
                request_serializer=nebius_dot_storage_dot_v1_dot_bucket__service__pb2.UpdateBucketRequest.SerializeToString,
                response_deserializer=nebius_dot_common_dot_v1_dot_operation__pb2.Operation.FromString,
                )
        self.Delete = channel.unary_unary(
                '/nebius.storage.v1.BucketService/Delete',
                request_serializer=nebius_dot_storage_dot_v1_dot_bucket__service__pb2.DeleteBucketRequest.SerializeToString,
                response_deserializer=nebius_dot_common_dot_v1_dot_operation__pb2.Operation.FromString,
                )
        self.Purge = channel.unary_unary(
                '/nebius.storage.v1.BucketService/Purge',
                request_serializer=nebius_dot_storage_dot_v1_dot_bucket__service__pb2.PurgeBucketRequest.SerializeToString,
                response_deserializer=nebius_dot_common_dot_v1_dot_operation__pb2.Operation.FromString,
                )
        self.Undelete = channel.unary_unary(
                '/nebius.storage.v1.BucketService/Undelete',
                request_serializer=nebius_dot_storage_dot_v1_dot_bucket__service__pb2.UndeleteBucketRequest.SerializeToString,
                response_deserializer=nebius_dot_common_dot_v1_dot_operation__pb2.Operation.FromString,
                )


class BucketServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Get(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetByName(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def List(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Create(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Update(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Delete(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Purge(self, request, context):
        """Purge instantly deletes the bucket in ScheduledForDeletion state.
        It can be used only for buckets in ScheduledForDeletion state.
        If you want to delete Active bucket instantly, use Delete with zero ttl.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Undelete(self, request, context):
        """Undelete recovers the bucket from ScheduledForDeletion state to Active.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_BucketServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Get': grpc.unary_unary_rpc_method_handler(
                    servicer.Get,
                    request_deserializer=nebius_dot_storage_dot_v1_dot_bucket__service__pb2.GetBucketRequest.FromString,
                    response_serializer=nebius_dot_storage_dot_v1_dot_bucket__pb2.Bucket.SerializeToString,
            ),
            'GetByName': grpc.unary_unary_rpc_method_handler(
                    servicer.GetByName,
                    request_deserializer=nebius_dot_storage_dot_v1_dot_bucket__service__pb2.GetBucketByNameRequest.FromString,
                    response_serializer=nebius_dot_storage_dot_v1_dot_bucket__pb2.Bucket.SerializeToString,
            ),
            'List': grpc.unary_unary_rpc_method_handler(
                    servicer.List,
                    request_deserializer=nebius_dot_storage_dot_v1_dot_bucket__service__pb2.ListBucketsRequest.FromString,
                    response_serializer=nebius_dot_storage_dot_v1_dot_bucket__service__pb2.ListBucketsResponse.SerializeToString,
            ),
            'Create': grpc.unary_unary_rpc_method_handler(
                    servicer.Create,
                    request_deserializer=nebius_dot_storage_dot_v1_dot_bucket__service__pb2.CreateBucketRequest.FromString,
                    response_serializer=nebius_dot_common_dot_v1_dot_operation__pb2.Operation.SerializeToString,
            ),
            'Update': grpc.unary_unary_rpc_method_handler(
                    servicer.Update,
                    request_deserializer=nebius_dot_storage_dot_v1_dot_bucket__service__pb2.UpdateBucketRequest.FromString,
                    response_serializer=nebius_dot_common_dot_v1_dot_operation__pb2.Operation.SerializeToString,
            ),
            'Delete': grpc.unary_unary_rpc_method_handler(
                    servicer.Delete,
                    request_deserializer=nebius_dot_storage_dot_v1_dot_bucket__service__pb2.DeleteBucketRequest.FromString,
                    response_serializer=nebius_dot_common_dot_v1_dot_operation__pb2.Operation.SerializeToString,
            ),
            'Purge': grpc.unary_unary_rpc_method_handler(
                    servicer.Purge,
                    request_deserializer=nebius_dot_storage_dot_v1_dot_bucket__service__pb2.PurgeBucketRequest.FromString,
                    response_serializer=nebius_dot_common_dot_v1_dot_operation__pb2.Operation.SerializeToString,
            ),
            'Undelete': grpc.unary_unary_rpc_method_handler(
                    servicer.Undelete,
                    request_deserializer=nebius_dot_storage_dot_v1_dot_bucket__service__pb2.UndeleteBucketRequest.FromString,
                    response_serializer=nebius_dot_common_dot_v1_dot_operation__pb2.Operation.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'nebius.storage.v1.BucketService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class BucketService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Get(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/nebius.storage.v1.BucketService/Get',
            nebius_dot_storage_dot_v1_dot_bucket__service__pb2.GetBucketRequest.SerializeToString,
            nebius_dot_storage_dot_v1_dot_bucket__pb2.Bucket.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetByName(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/nebius.storage.v1.BucketService/GetByName',
            nebius_dot_storage_dot_v1_dot_bucket__service__pb2.GetBucketByNameRequest.SerializeToString,
            nebius_dot_storage_dot_v1_dot_bucket__pb2.Bucket.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def List(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/nebius.storage.v1.BucketService/List',
            nebius_dot_storage_dot_v1_dot_bucket__service__pb2.ListBucketsRequest.SerializeToString,
            nebius_dot_storage_dot_v1_dot_bucket__service__pb2.ListBucketsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Create(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/nebius.storage.v1.BucketService/Create',
            nebius_dot_storage_dot_v1_dot_bucket__service__pb2.CreateBucketRequest.SerializeToString,
            nebius_dot_common_dot_v1_dot_operation__pb2.Operation.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Update(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/nebius.storage.v1.BucketService/Update',
            nebius_dot_storage_dot_v1_dot_bucket__service__pb2.UpdateBucketRequest.SerializeToString,
            nebius_dot_common_dot_v1_dot_operation__pb2.Operation.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Delete(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/nebius.storage.v1.BucketService/Delete',
            nebius_dot_storage_dot_v1_dot_bucket__service__pb2.DeleteBucketRequest.SerializeToString,
            nebius_dot_common_dot_v1_dot_operation__pb2.Operation.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Purge(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/nebius.storage.v1.BucketService/Purge',
            nebius_dot_storage_dot_v1_dot_bucket__service__pb2.PurgeBucketRequest.SerializeToString,
            nebius_dot_common_dot_v1_dot_operation__pb2.Operation.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Undelete(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/nebius.storage.v1.BucketService/Undelete',
            nebius_dot_storage_dot_v1_dot_bucket__service__pb2.UndeleteBucketRequest.SerializeToString,
            nebius_dot_common_dot_v1_dot_operation__pb2.Operation.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from nebius.api.nebius.common.v1 import operation_pb2 as nebius_dot_common_dot_v1_dot_operation__pb2
from nebius.api.nebius.vpc.v1 import pool_pb2 as nebius_dot_vpc_dot_v1_dot_pool__pb2
from nebius.api.nebius.vpc.v1 import pool_service_pb2 as nebius_dot_vpc_dot_v1_dot_pool__service__pb2


class PoolServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Get = channel.unary_unary(
                '/nebius.vpc.v1.PoolService/Get',
                request_serializer=nebius_dot_vpc_dot_v1_dot_pool__service__pb2.GetPoolRequest.SerializeToString,
                response_deserializer=nebius_dot_vpc_dot_v1_dot_pool__pb2.Pool.FromString,
                )
        self.GetByName = channel.unary_unary(
                '/nebius.vpc.v1.PoolService/GetByName',
                request_serializer=nebius_dot_vpc_dot_v1_dot_pool__service__pb2.GetPoolByNameRequest.SerializeToString,
                response_deserializer=nebius_dot_vpc_dot_v1_dot_pool__pb2.Pool.FromString,
                )
        self.List = channel.unary_unary(
                '/nebius.vpc.v1.PoolService/List',
                request_serializer=nebius_dot_vpc_dot_v1_dot_pool__service__pb2.ListPoolsRequest.SerializeToString,
                response_deserializer=nebius_dot_vpc_dot_v1_dot_pool__service__pb2.ListPoolsResponse.FromString,
                )
        self.ListBySourcePool = channel.unary_unary(
                '/nebius.vpc.v1.PoolService/ListBySourcePool',
                request_serializer=nebius_dot_vpc_dot_v1_dot_pool__service__pb2.ListPoolsBySourcePoolRequest.SerializeToString,
                response_deserializer=nebius_dot_vpc_dot_v1_dot_pool__service__pb2.ListPoolsResponse.FromString,
                )
        self.Update = channel.unary_unary(
                '/nebius.vpc.v1.PoolService/Update',
                request_serializer=nebius_dot_vpc_dot_v1_dot_pool__service__pb2.UpdatePoolRequest.SerializeToString,
                response_deserializer=nebius_dot_common_dot_v1_dot_operation__pb2.Operation.FromString,
                )


class PoolServiceServicer(object):
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

    def ListBySourcePool(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Update(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_PoolServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Get': grpc.unary_unary_rpc_method_handler(
                    servicer.Get,
                    request_deserializer=nebius_dot_vpc_dot_v1_dot_pool__service__pb2.GetPoolRequest.FromString,
                    response_serializer=nebius_dot_vpc_dot_v1_dot_pool__pb2.Pool.SerializeToString,
            ),
            'GetByName': grpc.unary_unary_rpc_method_handler(
                    servicer.GetByName,
                    request_deserializer=nebius_dot_vpc_dot_v1_dot_pool__service__pb2.GetPoolByNameRequest.FromString,
                    response_serializer=nebius_dot_vpc_dot_v1_dot_pool__pb2.Pool.SerializeToString,
            ),
            'List': grpc.unary_unary_rpc_method_handler(
                    servicer.List,
                    request_deserializer=nebius_dot_vpc_dot_v1_dot_pool__service__pb2.ListPoolsRequest.FromString,
                    response_serializer=nebius_dot_vpc_dot_v1_dot_pool__service__pb2.ListPoolsResponse.SerializeToString,
            ),
            'ListBySourcePool': grpc.unary_unary_rpc_method_handler(
                    servicer.ListBySourcePool,
                    request_deserializer=nebius_dot_vpc_dot_v1_dot_pool__service__pb2.ListPoolsBySourcePoolRequest.FromString,
                    response_serializer=nebius_dot_vpc_dot_v1_dot_pool__service__pb2.ListPoolsResponse.SerializeToString,
            ),
            'Update': grpc.unary_unary_rpc_method_handler(
                    servicer.Update,
                    request_deserializer=nebius_dot_vpc_dot_v1_dot_pool__service__pb2.UpdatePoolRequest.FromString,
                    response_serializer=nebius_dot_common_dot_v1_dot_operation__pb2.Operation.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'nebius.vpc.v1.PoolService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class PoolService(object):
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
        return grpc.experimental.unary_unary(request, target, '/nebius.vpc.v1.PoolService/Get',
            nebius_dot_vpc_dot_v1_dot_pool__service__pb2.GetPoolRequest.SerializeToString,
            nebius_dot_vpc_dot_v1_dot_pool__pb2.Pool.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/nebius.vpc.v1.PoolService/GetByName',
            nebius_dot_vpc_dot_v1_dot_pool__service__pb2.GetPoolByNameRequest.SerializeToString,
            nebius_dot_vpc_dot_v1_dot_pool__pb2.Pool.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/nebius.vpc.v1.PoolService/List',
            nebius_dot_vpc_dot_v1_dot_pool__service__pb2.ListPoolsRequest.SerializeToString,
            nebius_dot_vpc_dot_v1_dot_pool__service__pb2.ListPoolsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListBySourcePool(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/nebius.vpc.v1.PoolService/ListBySourcePool',
            nebius_dot_vpc_dot_v1_dot_pool__service__pb2.ListPoolsBySourcePoolRequest.SerializeToString,
            nebius_dot_vpc_dot_v1_dot_pool__service__pb2.ListPoolsResponse.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/nebius.vpc.v1.PoolService/Update',
            nebius_dot_vpc_dot_v1_dot_pool__service__pb2.UpdatePoolRequest.SerializeToString,
            nebius_dot_common_dot_v1_dot_operation__pb2.Operation.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from nebius.api.nebius.common.v1alpha1 import operation_pb2 as nebius_dot_common_dot_v1alpha1_dot_operation__pb2
from nebius.api.nebius.vpc.v1alpha1 import allocation_pb2 as nebius_dot_vpc_dot_v1alpha1_dot_allocation__pb2
from nebius.api.nebius.vpc.v1alpha1 import allocation_service_pb2 as nebius_dot_vpc_dot_v1alpha1_dot_allocation__service__pb2


class AllocationServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Get = channel.unary_unary(
                '/nebius.vpc.v1alpha1.AllocationService/Get',
                request_serializer=nebius_dot_vpc_dot_v1alpha1_dot_allocation__service__pb2.GetAllocationRequest.SerializeToString,
                response_deserializer=nebius_dot_vpc_dot_v1alpha1_dot_allocation__pb2.Allocation.FromString,
                )
        self.GetByName = channel.unary_unary(
                '/nebius.vpc.v1alpha1.AllocationService/GetByName',
                request_serializer=nebius_dot_vpc_dot_v1alpha1_dot_allocation__service__pb2.GetAllocationByNameRequest.SerializeToString,
                response_deserializer=nebius_dot_vpc_dot_v1alpha1_dot_allocation__pb2.Allocation.FromString,
                )
        self.List = channel.unary_unary(
                '/nebius.vpc.v1alpha1.AllocationService/List',
                request_serializer=nebius_dot_vpc_dot_v1alpha1_dot_allocation__service__pb2.ListAllocationsRequest.SerializeToString,
                response_deserializer=nebius_dot_vpc_dot_v1alpha1_dot_allocation__service__pb2.ListAllocationsResponse.FromString,
                )
        self.Create = channel.unary_unary(
                '/nebius.vpc.v1alpha1.AllocationService/Create',
                request_serializer=nebius_dot_vpc_dot_v1alpha1_dot_allocation__service__pb2.CreateAllocationRequest.SerializeToString,
                response_deserializer=nebius_dot_common_dot_v1alpha1_dot_operation__pb2.Operation.FromString,
                )
        self.Update = channel.unary_unary(
                '/nebius.vpc.v1alpha1.AllocationService/Update',
                request_serializer=nebius_dot_vpc_dot_v1alpha1_dot_allocation__service__pb2.UpdateAllocationRequest.SerializeToString,
                response_deserializer=nebius_dot_common_dot_v1alpha1_dot_operation__pb2.Operation.FromString,
                )
        self.Delete = channel.unary_unary(
                '/nebius.vpc.v1alpha1.AllocationService/Delete',
                request_serializer=nebius_dot_vpc_dot_v1alpha1_dot_allocation__service__pb2.DeleteAllocationRequest.SerializeToString,
                response_deserializer=nebius_dot_common_dot_v1alpha1_dot_operation__pb2.Operation.FromString,
                )


class AllocationServiceServicer(object):
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


def add_AllocationServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Get': grpc.unary_unary_rpc_method_handler(
                    servicer.Get,
                    request_deserializer=nebius_dot_vpc_dot_v1alpha1_dot_allocation__service__pb2.GetAllocationRequest.FromString,
                    response_serializer=nebius_dot_vpc_dot_v1alpha1_dot_allocation__pb2.Allocation.SerializeToString,
            ),
            'GetByName': grpc.unary_unary_rpc_method_handler(
                    servicer.GetByName,
                    request_deserializer=nebius_dot_vpc_dot_v1alpha1_dot_allocation__service__pb2.GetAllocationByNameRequest.FromString,
                    response_serializer=nebius_dot_vpc_dot_v1alpha1_dot_allocation__pb2.Allocation.SerializeToString,
            ),
            'List': grpc.unary_unary_rpc_method_handler(
                    servicer.List,
                    request_deserializer=nebius_dot_vpc_dot_v1alpha1_dot_allocation__service__pb2.ListAllocationsRequest.FromString,
                    response_serializer=nebius_dot_vpc_dot_v1alpha1_dot_allocation__service__pb2.ListAllocationsResponse.SerializeToString,
            ),
            'Create': grpc.unary_unary_rpc_method_handler(
                    servicer.Create,
                    request_deserializer=nebius_dot_vpc_dot_v1alpha1_dot_allocation__service__pb2.CreateAllocationRequest.FromString,
                    response_serializer=nebius_dot_common_dot_v1alpha1_dot_operation__pb2.Operation.SerializeToString,
            ),
            'Update': grpc.unary_unary_rpc_method_handler(
                    servicer.Update,
                    request_deserializer=nebius_dot_vpc_dot_v1alpha1_dot_allocation__service__pb2.UpdateAllocationRequest.FromString,
                    response_serializer=nebius_dot_common_dot_v1alpha1_dot_operation__pb2.Operation.SerializeToString,
            ),
            'Delete': grpc.unary_unary_rpc_method_handler(
                    servicer.Delete,
                    request_deserializer=nebius_dot_vpc_dot_v1alpha1_dot_allocation__service__pb2.DeleteAllocationRequest.FromString,
                    response_serializer=nebius_dot_common_dot_v1alpha1_dot_operation__pb2.Operation.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'nebius.vpc.v1alpha1.AllocationService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class AllocationService(object):
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
        return grpc.experimental.unary_unary(request, target, '/nebius.vpc.v1alpha1.AllocationService/Get',
            nebius_dot_vpc_dot_v1alpha1_dot_allocation__service__pb2.GetAllocationRequest.SerializeToString,
            nebius_dot_vpc_dot_v1alpha1_dot_allocation__pb2.Allocation.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/nebius.vpc.v1alpha1.AllocationService/GetByName',
            nebius_dot_vpc_dot_v1alpha1_dot_allocation__service__pb2.GetAllocationByNameRequest.SerializeToString,
            nebius_dot_vpc_dot_v1alpha1_dot_allocation__pb2.Allocation.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/nebius.vpc.v1alpha1.AllocationService/List',
            nebius_dot_vpc_dot_v1alpha1_dot_allocation__service__pb2.ListAllocationsRequest.SerializeToString,
            nebius_dot_vpc_dot_v1alpha1_dot_allocation__service__pb2.ListAllocationsResponse.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/nebius.vpc.v1alpha1.AllocationService/Create',
            nebius_dot_vpc_dot_v1alpha1_dot_allocation__service__pb2.CreateAllocationRequest.SerializeToString,
            nebius_dot_common_dot_v1alpha1_dot_operation__pb2.Operation.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/nebius.vpc.v1alpha1.AllocationService/Update',
            nebius_dot_vpc_dot_v1alpha1_dot_allocation__service__pb2.UpdateAllocationRequest.SerializeToString,
            nebius_dot_common_dot_v1alpha1_dot_operation__pb2.Operation.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/nebius.vpc.v1alpha1.AllocationService/Delete',
            nebius_dot_vpc_dot_v1alpha1_dot_allocation__service__pb2.DeleteAllocationRequest.SerializeToString,
            nebius_dot_common_dot_v1alpha1_dot_operation__pb2.Operation.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

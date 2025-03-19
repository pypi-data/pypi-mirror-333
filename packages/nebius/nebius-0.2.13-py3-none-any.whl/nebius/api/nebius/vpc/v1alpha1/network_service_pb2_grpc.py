# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from nebius.api.nebius.vpc.v1alpha1 import network_pb2 as nebius_dot_vpc_dot_v1alpha1_dot_network__pb2
from nebius.api.nebius.vpc.v1alpha1 import network_service_pb2 as nebius_dot_vpc_dot_v1alpha1_dot_network__service__pb2


class NetworkServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Get = channel.unary_unary(
                '/nebius.vpc.v1alpha1.NetworkService/Get',
                request_serializer=nebius_dot_vpc_dot_v1alpha1_dot_network__service__pb2.GetNetworkRequest.SerializeToString,
                response_deserializer=nebius_dot_vpc_dot_v1alpha1_dot_network__pb2.Network.FromString,
                )
        self.GetByName = channel.unary_unary(
                '/nebius.vpc.v1alpha1.NetworkService/GetByName',
                request_serializer=nebius_dot_vpc_dot_v1alpha1_dot_network__service__pb2.GetNetworkByNameRequest.SerializeToString,
                response_deserializer=nebius_dot_vpc_dot_v1alpha1_dot_network__pb2.Network.FromString,
                )
        self.List = channel.unary_unary(
                '/nebius.vpc.v1alpha1.NetworkService/List',
                request_serializer=nebius_dot_vpc_dot_v1alpha1_dot_network__service__pb2.ListNetworksRequest.SerializeToString,
                response_deserializer=nebius_dot_vpc_dot_v1alpha1_dot_network__service__pb2.ListNetworksResponse.FromString,
                )


class NetworkServiceServicer(object):
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


def add_NetworkServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Get': grpc.unary_unary_rpc_method_handler(
                    servicer.Get,
                    request_deserializer=nebius_dot_vpc_dot_v1alpha1_dot_network__service__pb2.GetNetworkRequest.FromString,
                    response_serializer=nebius_dot_vpc_dot_v1alpha1_dot_network__pb2.Network.SerializeToString,
            ),
            'GetByName': grpc.unary_unary_rpc_method_handler(
                    servicer.GetByName,
                    request_deserializer=nebius_dot_vpc_dot_v1alpha1_dot_network__service__pb2.GetNetworkByNameRequest.FromString,
                    response_serializer=nebius_dot_vpc_dot_v1alpha1_dot_network__pb2.Network.SerializeToString,
            ),
            'List': grpc.unary_unary_rpc_method_handler(
                    servicer.List,
                    request_deserializer=nebius_dot_vpc_dot_v1alpha1_dot_network__service__pb2.ListNetworksRequest.FromString,
                    response_serializer=nebius_dot_vpc_dot_v1alpha1_dot_network__service__pb2.ListNetworksResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'nebius.vpc.v1alpha1.NetworkService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class NetworkService(object):
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
        return grpc.experimental.unary_unary(request, target, '/nebius.vpc.v1alpha1.NetworkService/Get',
            nebius_dot_vpc_dot_v1alpha1_dot_network__service__pb2.GetNetworkRequest.SerializeToString,
            nebius_dot_vpc_dot_v1alpha1_dot_network__pb2.Network.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/nebius.vpc.v1alpha1.NetworkService/GetByName',
            nebius_dot_vpc_dot_v1alpha1_dot_network__service__pb2.GetNetworkByNameRequest.SerializeToString,
            nebius_dot_vpc_dot_v1alpha1_dot_network__pb2.Network.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/nebius.vpc.v1alpha1.NetworkService/List',
            nebius_dot_vpc_dot_v1alpha1_dot_network__service__pb2.ListNetworksRequest.SerializeToString,
            nebius_dot_vpc_dot_v1alpha1_dot_network__service__pb2.ListNetworksResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

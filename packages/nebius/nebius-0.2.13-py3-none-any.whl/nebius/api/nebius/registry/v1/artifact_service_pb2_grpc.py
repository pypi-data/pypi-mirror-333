# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from nebius.api.nebius.common.v1 import operation_pb2 as nebius_dot_common_dot_v1_dot_operation__pb2
from nebius.api.nebius.registry.v1 import artifact_pb2 as nebius_dot_registry_dot_v1_dot_artifact__pb2
from nebius.api.nebius.registry.v1 import artifact_service_pb2 as nebius_dot_registry_dot_v1_dot_artifact__service__pb2


class ArtifactServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Get = channel.unary_unary(
                '/nebius.registry.v1.ArtifactService/Get',
                request_serializer=nebius_dot_registry_dot_v1_dot_artifact__service__pb2.GetArtifactRequest.SerializeToString,
                response_deserializer=nebius_dot_registry_dot_v1_dot_artifact__pb2.Artifact.FromString,
                )
        self.List = channel.unary_unary(
                '/nebius.registry.v1.ArtifactService/List',
                request_serializer=nebius_dot_registry_dot_v1_dot_artifact__service__pb2.ListArtifactsRequest.SerializeToString,
                response_deserializer=nebius_dot_registry_dot_v1_dot_artifact__service__pb2.ListArtifactsResponse.FromString,
                )
        self.Delete = channel.unary_unary(
                '/nebius.registry.v1.ArtifactService/Delete',
                request_serializer=nebius_dot_registry_dot_v1_dot_artifact__service__pb2.DeleteArtifactRequest.SerializeToString,
                response_deserializer=nebius_dot_common_dot_v1_dot_operation__pb2.Operation.FromString,
                )


class ArtifactServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Get(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def List(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Delete(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ArtifactServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Get': grpc.unary_unary_rpc_method_handler(
                    servicer.Get,
                    request_deserializer=nebius_dot_registry_dot_v1_dot_artifact__service__pb2.GetArtifactRequest.FromString,
                    response_serializer=nebius_dot_registry_dot_v1_dot_artifact__pb2.Artifact.SerializeToString,
            ),
            'List': grpc.unary_unary_rpc_method_handler(
                    servicer.List,
                    request_deserializer=nebius_dot_registry_dot_v1_dot_artifact__service__pb2.ListArtifactsRequest.FromString,
                    response_serializer=nebius_dot_registry_dot_v1_dot_artifact__service__pb2.ListArtifactsResponse.SerializeToString,
            ),
            'Delete': grpc.unary_unary_rpc_method_handler(
                    servicer.Delete,
                    request_deserializer=nebius_dot_registry_dot_v1_dot_artifact__service__pb2.DeleteArtifactRequest.FromString,
                    response_serializer=nebius_dot_common_dot_v1_dot_operation__pb2.Operation.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'nebius.registry.v1.ArtifactService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ArtifactService(object):
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
        return grpc.experimental.unary_unary(request, target, '/nebius.registry.v1.ArtifactService/Get',
            nebius_dot_registry_dot_v1_dot_artifact__service__pb2.GetArtifactRequest.SerializeToString,
            nebius_dot_registry_dot_v1_dot_artifact__pb2.Artifact.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/nebius.registry.v1.ArtifactService/List',
            nebius_dot_registry_dot_v1_dot_artifact__service__pb2.ListArtifactsRequest.SerializeToString,
            nebius_dot_registry_dot_v1_dot_artifact__service__pb2.ListArtifactsResponse.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/nebius.registry.v1.ArtifactService/Delete',
            nebius_dot_registry_dot_v1_dot_artifact__service__pb2.DeleteArtifactRequest.SerializeToString,
            nebius_dot_common_dot_v1_dot_operation__pb2.Operation.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from nebius.api.nebius.logging.v1.agentmanager import version_service_pb2 as nebius_dot_logging_dot_v1_dot_agentmanager_dot_version__service__pb2


class VersionServiceStub(object):
    """VersionService provides functionality for managing nebius-observability-agent versions and health status
    in the Nebius observability system.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetVersion = channel.unary_unary(
                '/nebius.logging.agentmanager.v1.VersionService/GetVersion',
                request_serializer=nebius_dot_logging_dot_v1_dot_agentmanager_dot_version__service__pb2.GetVersionRequest.SerializeToString,
                response_deserializer=nebius_dot_logging_dot_v1_dot_agentmanager_dot_version__service__pb2.GetVersionResponse.FromString,
                )


class VersionServiceServicer(object):
    """VersionService provides functionality for managing nebius-observability-agent versions and health status
    in the Nebius observability system.
    """

    def GetVersion(self, request, context):
        """GetVersion retrieves version information and receives instructions for agent updates
        or maintenance based on the current state and health of the agent.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_VersionServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetVersion': grpc.unary_unary_rpc_method_handler(
                    servicer.GetVersion,
                    request_deserializer=nebius_dot_logging_dot_v1_dot_agentmanager_dot_version__service__pb2.GetVersionRequest.FromString,
                    response_serializer=nebius_dot_logging_dot_v1_dot_agentmanager_dot_version__service__pb2.GetVersionResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'nebius.logging.agentmanager.v1.VersionService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class VersionService(object):
    """VersionService provides functionality for managing nebius-observability-agent versions and health status
    in the Nebius observability system.
    """

    @staticmethod
    def GetVersion(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/nebius.logging.agentmanager.v1.VersionService/GetVersion',
            nebius_dot_logging_dot_v1_dot_agentmanager_dot_version__service__pb2.GetVersionRequest.SerializeToString,
            nebius_dot_logging_dot_v1_dot_agentmanager_dot_version__service__pb2.GetVersionResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

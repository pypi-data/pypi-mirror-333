# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from nebius.api.nebius.common.v1 import metadata_pb2 as nebius_dot_common_dot_v1_dot_metadata__pb2
from nebius.api.nebius.common.v1alpha1 import operation_pb2 as nebius_dot_common_dot_v1alpha1_dot_operation__pb2
from nebius.api.nebius.msp.postgresql.v1alpha1 import cluster_pb2 as nebius_dot_msp_dot_postgresql_dot_v1alpha1_dot_cluster__pb2
from nebius.api.nebius.msp.postgresql.v1alpha1 import cluster_service_pb2 as nebius_dot_msp_dot_postgresql_dot_v1alpha1_dot_cluster__service__pb2


class ClusterServiceStub(object):
    """A set of methods for managing PostgreSQL Cluster resources.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Get = channel.unary_unary(
                '/nebius.msp.postgresql.v1alpha1.ClusterService/Get',
                request_serializer=nebius_dot_msp_dot_postgresql_dot_v1alpha1_dot_cluster__service__pb2.GetClusterRequest.SerializeToString,
                response_deserializer=nebius_dot_msp_dot_postgresql_dot_v1alpha1_dot_cluster__pb2.Cluster.FromString,
                )
        self.GetByName = channel.unary_unary(
                '/nebius.msp.postgresql.v1alpha1.ClusterService/GetByName',
                request_serializer=nebius_dot_common_dot_v1_dot_metadata__pb2.GetByNameRequest.SerializeToString,
                response_deserializer=nebius_dot_msp_dot_postgresql_dot_v1alpha1_dot_cluster__pb2.Cluster.FromString,
                )
        self.List = channel.unary_unary(
                '/nebius.msp.postgresql.v1alpha1.ClusterService/List',
                request_serializer=nebius_dot_msp_dot_postgresql_dot_v1alpha1_dot_cluster__service__pb2.ListClustersRequest.SerializeToString,
                response_deserializer=nebius_dot_msp_dot_postgresql_dot_v1alpha1_dot_cluster__service__pb2.ListClustersResponse.FromString,
                )
        self.Create = channel.unary_unary(
                '/nebius.msp.postgresql.v1alpha1.ClusterService/Create',
                request_serializer=nebius_dot_msp_dot_postgresql_dot_v1alpha1_dot_cluster__service__pb2.CreateClusterRequest.SerializeToString,
                response_deserializer=nebius_dot_common_dot_v1alpha1_dot_operation__pb2.Operation.FromString,
                )
        self.Delete = channel.unary_unary(
                '/nebius.msp.postgresql.v1alpha1.ClusterService/Delete',
                request_serializer=nebius_dot_msp_dot_postgresql_dot_v1alpha1_dot_cluster__service__pb2.DeleteClusterRequest.SerializeToString,
                response_deserializer=nebius_dot_common_dot_v1alpha1_dot_operation__pb2.Operation.FromString,
                )
        self.Update = channel.unary_unary(
                '/nebius.msp.postgresql.v1alpha1.ClusterService/Update',
                request_serializer=nebius_dot_msp_dot_postgresql_dot_v1alpha1_dot_cluster__service__pb2.UpdateClusterRequest.SerializeToString,
                response_deserializer=nebius_dot_common_dot_v1alpha1_dot_operation__pb2.Operation.FromString,
                )
        self.Restore = channel.unary_unary(
                '/nebius.msp.postgresql.v1alpha1.ClusterService/Restore',
                request_serializer=nebius_dot_msp_dot_postgresql_dot_v1alpha1_dot_cluster__service__pb2.RestoreClusterRequest.SerializeToString,
                response_deserializer=nebius_dot_common_dot_v1alpha1_dot_operation__pb2.Operation.FromString,
                )


class ClusterServiceServicer(object):
    """A set of methods for managing PostgreSQL Cluster resources.
    """

    def Get(self, request, context):
        """Returns the specified PostgreSQL Cluster resource.
        To get the list of available PostgreSQL Cluster resources, make a [List] request.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetByName(self, request, context):
        """Returns the specified PostgreSQL Cluster resource by name.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def List(self, request, context):
        """Retrieves the list of PostgreSQL Cluster resources that belong
        to the specified folder.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Create(self, request, context):
        """Creates a PostgreSQL cluster in the specified folder.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Delete(self, request, context):
        """Deletes the specified PostgreSQL cluster.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Update(self, request, context):
        """Updates the PostgreSQL cluster.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Restore(self, request, context):
        """Creates a new PostgreSQL cluster from a previously created backup.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ClusterServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Get': grpc.unary_unary_rpc_method_handler(
                    servicer.Get,
                    request_deserializer=nebius_dot_msp_dot_postgresql_dot_v1alpha1_dot_cluster__service__pb2.GetClusterRequest.FromString,
                    response_serializer=nebius_dot_msp_dot_postgresql_dot_v1alpha1_dot_cluster__pb2.Cluster.SerializeToString,
            ),
            'GetByName': grpc.unary_unary_rpc_method_handler(
                    servicer.GetByName,
                    request_deserializer=nebius_dot_common_dot_v1_dot_metadata__pb2.GetByNameRequest.FromString,
                    response_serializer=nebius_dot_msp_dot_postgresql_dot_v1alpha1_dot_cluster__pb2.Cluster.SerializeToString,
            ),
            'List': grpc.unary_unary_rpc_method_handler(
                    servicer.List,
                    request_deserializer=nebius_dot_msp_dot_postgresql_dot_v1alpha1_dot_cluster__service__pb2.ListClustersRequest.FromString,
                    response_serializer=nebius_dot_msp_dot_postgresql_dot_v1alpha1_dot_cluster__service__pb2.ListClustersResponse.SerializeToString,
            ),
            'Create': grpc.unary_unary_rpc_method_handler(
                    servicer.Create,
                    request_deserializer=nebius_dot_msp_dot_postgresql_dot_v1alpha1_dot_cluster__service__pb2.CreateClusterRequest.FromString,
                    response_serializer=nebius_dot_common_dot_v1alpha1_dot_operation__pb2.Operation.SerializeToString,
            ),
            'Delete': grpc.unary_unary_rpc_method_handler(
                    servicer.Delete,
                    request_deserializer=nebius_dot_msp_dot_postgresql_dot_v1alpha1_dot_cluster__service__pb2.DeleteClusterRequest.FromString,
                    response_serializer=nebius_dot_common_dot_v1alpha1_dot_operation__pb2.Operation.SerializeToString,
            ),
            'Update': grpc.unary_unary_rpc_method_handler(
                    servicer.Update,
                    request_deserializer=nebius_dot_msp_dot_postgresql_dot_v1alpha1_dot_cluster__service__pb2.UpdateClusterRequest.FromString,
                    response_serializer=nebius_dot_common_dot_v1alpha1_dot_operation__pb2.Operation.SerializeToString,
            ),
            'Restore': grpc.unary_unary_rpc_method_handler(
                    servicer.Restore,
                    request_deserializer=nebius_dot_msp_dot_postgresql_dot_v1alpha1_dot_cluster__service__pb2.RestoreClusterRequest.FromString,
                    response_serializer=nebius_dot_common_dot_v1alpha1_dot_operation__pb2.Operation.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'nebius.msp.postgresql.v1alpha1.ClusterService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ClusterService(object):
    """A set of methods for managing PostgreSQL Cluster resources.
    """

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
        return grpc.experimental.unary_unary(request, target, '/nebius.msp.postgresql.v1alpha1.ClusterService/Get',
            nebius_dot_msp_dot_postgresql_dot_v1alpha1_dot_cluster__service__pb2.GetClusterRequest.SerializeToString,
            nebius_dot_msp_dot_postgresql_dot_v1alpha1_dot_cluster__pb2.Cluster.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/nebius.msp.postgresql.v1alpha1.ClusterService/GetByName',
            nebius_dot_common_dot_v1_dot_metadata__pb2.GetByNameRequest.SerializeToString,
            nebius_dot_msp_dot_postgresql_dot_v1alpha1_dot_cluster__pb2.Cluster.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/nebius.msp.postgresql.v1alpha1.ClusterService/List',
            nebius_dot_msp_dot_postgresql_dot_v1alpha1_dot_cluster__service__pb2.ListClustersRequest.SerializeToString,
            nebius_dot_msp_dot_postgresql_dot_v1alpha1_dot_cluster__service__pb2.ListClustersResponse.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/nebius.msp.postgresql.v1alpha1.ClusterService/Create',
            nebius_dot_msp_dot_postgresql_dot_v1alpha1_dot_cluster__service__pb2.CreateClusterRequest.SerializeToString,
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
        return grpc.experimental.unary_unary(request, target, '/nebius.msp.postgresql.v1alpha1.ClusterService/Delete',
            nebius_dot_msp_dot_postgresql_dot_v1alpha1_dot_cluster__service__pb2.DeleteClusterRequest.SerializeToString,
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
        return grpc.experimental.unary_unary(request, target, '/nebius.msp.postgresql.v1alpha1.ClusterService/Update',
            nebius_dot_msp_dot_postgresql_dot_v1alpha1_dot_cluster__service__pb2.UpdateClusterRequest.SerializeToString,
            nebius_dot_common_dot_v1alpha1_dot_operation__pb2.Operation.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Restore(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/nebius.msp.postgresql.v1alpha1.ClusterService/Restore',
            nebius_dot_msp_dot_postgresql_dot_v1alpha1_dot_cluster__service__pb2.RestoreClusterRequest.SerializeToString,
            nebius_dot_common_dot_v1alpha1_dot_operation__pb2.Operation.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

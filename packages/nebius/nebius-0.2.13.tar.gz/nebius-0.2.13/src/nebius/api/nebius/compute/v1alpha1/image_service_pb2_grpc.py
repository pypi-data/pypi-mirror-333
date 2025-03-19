# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from nebius.api.nebius.common.v1 import metadata_pb2 as nebius_dot_common_dot_v1_dot_metadata__pb2
from nebius.api.nebius.common.v1alpha1 import operation_service_pb2 as nebius_dot_common_dot_v1alpha1_dot_operation__service__pb2
from nebius.api.nebius.compute.v1alpha1 import image_pb2 as nebius_dot_compute_dot_v1alpha1_dot_image__pb2
from nebius.api.nebius.compute.v1alpha1 import image_service_pb2 as nebius_dot_compute_dot_v1alpha1_dot_image__service__pb2


class ImageServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Get = channel.unary_unary(
                '/nebius.compute.v1alpha1.ImageService/Get',
                request_serializer=nebius_dot_compute_dot_v1alpha1_dot_image__service__pb2.GetImageRequest.SerializeToString,
                response_deserializer=nebius_dot_compute_dot_v1alpha1_dot_image__pb2.Image.FromString,
                )
        self.GetByName = channel.unary_unary(
                '/nebius.compute.v1alpha1.ImageService/GetByName',
                request_serializer=nebius_dot_common_dot_v1_dot_metadata__pb2.GetByNameRequest.SerializeToString,
                response_deserializer=nebius_dot_compute_dot_v1alpha1_dot_image__pb2.Image.FromString,
                )
        self.GetLatestByFamily = channel.unary_unary(
                '/nebius.compute.v1alpha1.ImageService/GetLatestByFamily',
                request_serializer=nebius_dot_compute_dot_v1alpha1_dot_image__service__pb2.GetImageLatestByFamilyRequest.SerializeToString,
                response_deserializer=nebius_dot_compute_dot_v1alpha1_dot_image__pb2.Image.FromString,
                )
        self.List = channel.unary_unary(
                '/nebius.compute.v1alpha1.ImageService/List',
                request_serializer=nebius_dot_compute_dot_v1alpha1_dot_image__service__pb2.ListImagesRequest.SerializeToString,
                response_deserializer=nebius_dot_compute_dot_v1alpha1_dot_image__service__pb2.ListImagesResponse.FromString,
                )
        self.ListOperationsByParent = channel.unary_unary(
                '/nebius.compute.v1alpha1.ImageService/ListOperationsByParent',
                request_serializer=nebius_dot_common_dot_v1alpha1_dot_operation__service__pb2.ListOperationsByParentRequest.SerializeToString,
                response_deserializer=nebius_dot_common_dot_v1alpha1_dot_operation__service__pb2.ListOperationsResponse.FromString,
                )


class ImageServiceServicer(object):
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

    def GetLatestByFamily(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def List(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListOperationsByParent(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ImageServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Get': grpc.unary_unary_rpc_method_handler(
                    servicer.Get,
                    request_deserializer=nebius_dot_compute_dot_v1alpha1_dot_image__service__pb2.GetImageRequest.FromString,
                    response_serializer=nebius_dot_compute_dot_v1alpha1_dot_image__pb2.Image.SerializeToString,
            ),
            'GetByName': grpc.unary_unary_rpc_method_handler(
                    servicer.GetByName,
                    request_deserializer=nebius_dot_common_dot_v1_dot_metadata__pb2.GetByNameRequest.FromString,
                    response_serializer=nebius_dot_compute_dot_v1alpha1_dot_image__pb2.Image.SerializeToString,
            ),
            'GetLatestByFamily': grpc.unary_unary_rpc_method_handler(
                    servicer.GetLatestByFamily,
                    request_deserializer=nebius_dot_compute_dot_v1alpha1_dot_image__service__pb2.GetImageLatestByFamilyRequest.FromString,
                    response_serializer=nebius_dot_compute_dot_v1alpha1_dot_image__pb2.Image.SerializeToString,
            ),
            'List': grpc.unary_unary_rpc_method_handler(
                    servicer.List,
                    request_deserializer=nebius_dot_compute_dot_v1alpha1_dot_image__service__pb2.ListImagesRequest.FromString,
                    response_serializer=nebius_dot_compute_dot_v1alpha1_dot_image__service__pb2.ListImagesResponse.SerializeToString,
            ),
            'ListOperationsByParent': grpc.unary_unary_rpc_method_handler(
                    servicer.ListOperationsByParent,
                    request_deserializer=nebius_dot_common_dot_v1alpha1_dot_operation__service__pb2.ListOperationsByParentRequest.FromString,
                    response_serializer=nebius_dot_common_dot_v1alpha1_dot_operation__service__pb2.ListOperationsResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'nebius.compute.v1alpha1.ImageService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ImageService(object):
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
        return grpc.experimental.unary_unary(request, target, '/nebius.compute.v1alpha1.ImageService/Get',
            nebius_dot_compute_dot_v1alpha1_dot_image__service__pb2.GetImageRequest.SerializeToString,
            nebius_dot_compute_dot_v1alpha1_dot_image__pb2.Image.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/nebius.compute.v1alpha1.ImageService/GetByName',
            nebius_dot_common_dot_v1_dot_metadata__pb2.GetByNameRequest.SerializeToString,
            nebius_dot_compute_dot_v1alpha1_dot_image__pb2.Image.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetLatestByFamily(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/nebius.compute.v1alpha1.ImageService/GetLatestByFamily',
            nebius_dot_compute_dot_v1alpha1_dot_image__service__pb2.GetImageLatestByFamilyRequest.SerializeToString,
            nebius_dot_compute_dot_v1alpha1_dot_image__pb2.Image.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/nebius.compute.v1alpha1.ImageService/List',
            nebius_dot_compute_dot_v1alpha1_dot_image__service__pb2.ListImagesRequest.SerializeToString,
            nebius_dot_compute_dot_v1alpha1_dot_image__service__pb2.ListImagesResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListOperationsByParent(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/nebius.compute.v1alpha1.ImageService/ListOperationsByParent',
            nebius_dot_common_dot_v1alpha1_dot_operation__service__pb2.ListOperationsByParentRequest.SerializeToString,
            nebius_dot_common_dot_v1alpha1_dot_operation__service__pb2.ListOperationsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

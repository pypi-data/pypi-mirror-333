# 
# Generated by the nebius.base.protos.compiler.  DO NOT EDIT!
# 

import nebius.base.protos.pb_classes as pb_classes
import nebius.api.nebius.msp.mlflow.v1alpha1.cluster_pb2 as cluster_pb2
import nebius.base.protos.descriptor as descriptor
import google.protobuf.descriptor as descriptor_1
import google.protobuf.message as message_1
import nebius.api.nebius.common.v1 as v1_1
import nebius.api.nebius.common.v1.metadata_pb2 as metadata_pb2
import nebius.base.protos.unset as unset
import collections.abc as abc
import builtins as builtins
import nebius.api.nebius.msp.v1alpha1 as v1alpha1_1
import nebius.api.nebius.msp.v1alpha1.cluster_pb2 as cluster_pb2_1
import nebius.api.nebius.msp.mlflow.v1alpha1.cluster_service_pb2 as cluster_service_pb2
import nebius.aio.client as client
import nebius.api.nebius.common.v1alpha1 as v1alpha1_2
import grpc as grpc
import nebius.aio.request as request_1
import nebius.aio.operation as operation
import nebius.api.nebius.common.v1alpha1.operation_pb2 as operation_pb2
#@ local imports here @#

# file: nebius/msp/mlflow/v1alpha1/cluster.proto
class Cluster(pb_classes.Message):
    __PB2_CLASS__ = cluster_pb2.Cluster
    __PB2_DESCRIPTOR__ = descriptor.DescriptorWrap[descriptor_1.Descriptor](".nebius.msp.mlflow.v1alpha1.Cluster",cluster_pb2.DESCRIPTOR,descriptor_1.Descriptor)
    __mask_functions__ = {
    }
    
    def __init__(
        self,
        initial_message: message_1.Message|None = None,
        *,
        metadata: "v1_1.ResourceMetadata|metadata_pb2.ResourceMetadata|None|unset.UnsetType" = unset.Unset,
        spec: "ClusterSpec|cluster_pb2.ClusterSpec|None|unset.UnsetType" = unset.Unset,
        status: "MlflowClusterStatus|cluster_pb2.MlflowClusterStatus|None|unset.UnsetType" = unset.Unset,
    ) -> None:
        super().__init__(initial_message)
        if not isinstance(metadata, unset.UnsetType):
            self.metadata = metadata
        if not isinstance(spec, unset.UnsetType):
            self.spec = spec
        if not isinstance(status, unset.UnsetType):
            self.status = status
    
    def __dir__(self) ->abc.Iterable[builtins.str]:
        return [
            "metadata",
            "spec",
            "status",
        ]
    
    @builtins.property
    def metadata(self) -> "v1_1.ResourceMetadata":
        return super()._get_field("metadata", explicit_presence=False,
        wrap=v1_1.ResourceMetadata,
        )
    @metadata.setter
    def metadata(self, value: "v1_1.ResourceMetadata|metadata_pb2.ResourceMetadata|None") -> None:
        return super()._set_field("metadata",value,explicit_presence=False,
        )
    
    @builtins.property
    def spec(self) -> "ClusterSpec":
        return super()._get_field("spec", explicit_presence=False,
        wrap=ClusterSpec,
        )
    @spec.setter
    def spec(self, value: "ClusterSpec|cluster_pb2.ClusterSpec|None") -> None:
        return super()._set_field("spec",value,explicit_presence=False,
        )
    
    @builtins.property
    def status(self) -> "MlflowClusterStatus":
        return super()._get_field("status", explicit_presence=False,
        wrap=MlflowClusterStatus,
        )
    @status.setter
    def status(self, value: "MlflowClusterStatus|cluster_pb2.MlflowClusterStatus|None") -> None:
        return super()._set_field("status",value,explicit_presence=False,
        )
    
    __PY_TO_PB2__: builtins.dict[builtins.str,builtins.str] = {
        "metadata":"metadata",
        "spec":"spec",
        "status":"status",
    }
    
class ClusterSpec(pb_classes.Message):
    """
     Cluster specification
    """
    
    __PB2_CLASS__ = cluster_pb2.ClusterSpec
    __PB2_DESCRIPTOR__ = descriptor.DescriptorWrap[descriptor_1.Descriptor](".nebius.msp.mlflow.v1alpha1.ClusterSpec",cluster_pb2.DESCRIPTOR,descriptor_1.Descriptor)
    __mask_functions__ = {
    }
    
    def __init__(
        self,
        initial_message: message_1.Message|None = None,
        *,
        description: "builtins.str|None|unset.UnsetType" = unset.Unset,
        public_access: "builtins.bool|None|unset.UnsetType" = unset.Unset,
        admin_username: "builtins.str|None|unset.UnsetType" = unset.Unset,
        admin_password: "builtins.str|None|unset.UnsetType" = unset.Unset,
        service_account_id: "builtins.str|None|unset.UnsetType" = unset.Unset,
        storage_bucket_name: "builtins.str|None|unset.UnsetType" = unset.Unset,
        network_id: "builtins.str|None|unset.UnsetType" = unset.Unset,
    ) -> None:
        super().__init__(initial_message)
        if not isinstance(description, unset.UnsetType):
            self.description = description
        if not isinstance(public_access, unset.UnsetType):
            self.public_access = public_access
        if not isinstance(admin_username, unset.UnsetType):
            self.admin_username = admin_username
        if not isinstance(admin_password, unset.UnsetType):
            self.admin_password = admin_password
        if not isinstance(service_account_id, unset.UnsetType):
            self.service_account_id = service_account_id
        if not isinstance(storage_bucket_name, unset.UnsetType):
            self.storage_bucket_name = storage_bucket_name
        if not isinstance(network_id, unset.UnsetType):
            self.network_id = network_id
    
    def __dir__(self) ->abc.Iterable[builtins.str]:
        return [
            "description",
            "public_access",
            "admin_username",
            "admin_password",
            "service_account_id",
            "storage_bucket_name",
            "network_id",
        ]
    
    @builtins.property
    def description(self) -> "builtins.str":
        """
         Description of the cluster.
        """
        
        return super()._get_field("description", explicit_presence=False,
        )
    @description.setter
    def description(self, value: "builtins.str|None") -> None:
        return super()._set_field("description",value,explicit_presence=False,
        )
    
    @builtins.property
    def public_access(self) -> "builtins.bool":
        """
         Either make cluster public accessible or accessible only via private VPC.
        """
        
        return super()._get_field("public_access", explicit_presence=False,
        )
    @public_access.setter
    def public_access(self, value: "builtins.bool|None") -> None:
        return super()._set_field("public_access",value,explicit_presence=False,
        )
    
    @builtins.property
    def admin_username(self) -> "builtins.str":
        """
         MLflow admin username.
        """
        
        return super()._get_field("admin_username", explicit_presence=False,
        )
    @admin_username.setter
    def admin_username(self, value: "builtins.str|None") -> None:
        return super()._set_field("admin_username",value,explicit_presence=False,
        )
    
    @builtins.property
    def admin_password(self) -> "builtins.str":
        """
         MLflow admin password.
        """
        
        return super()._get_field("admin_password", explicit_presence=False,
        )
    @admin_password.setter
    def admin_password(self, value: "builtins.str|None") -> None:
        return super()._set_field("admin_password",value,explicit_presence=False,
        )
    
    @builtins.property
    def service_account_id(self) -> "builtins.str":
        """
         Id of the service account that will be used to access S3 bucket (and create one if not provided).
        """
        
        return super()._get_field("service_account_id", explicit_presence=False,
        )
    @service_account_id.setter
    def service_account_id(self, value: "builtins.str|None") -> None:
        return super()._set_field("service_account_id",value,explicit_presence=False,
        )
    
    @builtins.property
    def storage_bucket_name(self) -> "builtins.str":
        """
         Name of the Nebius S3 bucket for MLflow artifacts. If not provided, will be created under the same parent.
        """
        
        return super()._get_field("storage_bucket_name", explicit_presence=False,
        )
    @storage_bucket_name.setter
    def storage_bucket_name(self, value: "builtins.str|None") -> None:
        return super()._set_field("storage_bucket_name",value,explicit_presence=False,
        )
    
    @builtins.property
    def network_id(self) -> "builtins.str":
        """
         ID of the vpc network.
        """
        
        return super()._get_field("network_id", explicit_presence=False,
        )
    @network_id.setter
    def network_id(self, value: "builtins.str|None") -> None:
        return super()._set_field("network_id",value,explicit_presence=False,
        )
    
    __PY_TO_PB2__: builtins.dict[builtins.str,builtins.str] = {
        "description":"description",
        "public_access":"public_access",
        "admin_username":"admin_username",
        "admin_password":"admin_password",
        "service_account_id":"service_account_id",
        "storage_bucket_name":"storage_bucket_name",
        "network_id":"network_id",
    }
    
class MlflowClusterStatus(pb_classes.Message):
    __PB2_CLASS__ = cluster_pb2.MlflowClusterStatus
    __PB2_DESCRIPTOR__ = descriptor.DescriptorWrap[descriptor_1.Descriptor](".nebius.msp.mlflow.v1alpha1.MlflowClusterStatus",cluster_pb2.DESCRIPTOR,descriptor_1.Descriptor)
    __mask_functions__ = {
    }
    
    def __init__(
        self,
        initial_message: message_1.Message|None = None,
        *,
        phase: "v1alpha1_1.ClusterStatus.Phase|cluster_pb2_1.ClusterStatus.Phase|None|unset.UnsetType" = unset.Unset,
        state: "v1alpha1_1.ClusterStatus.State|cluster_pb2_1.ClusterStatus.State|None|unset.UnsetType" = unset.Unset,
        tracking_endpoint: "builtins.str|None|unset.UnsetType" = unset.Unset,
        effective_storage_bucket_name: "builtins.str|None|unset.UnsetType" = unset.Unset,
        experiments_count: "builtins.int|None|unset.UnsetType" = unset.Unset,
        mlflow_version: "builtins.str|None|unset.UnsetType" = unset.Unset,
        tracking_endpoints: "Endpoints|cluster_pb2.Endpoints|None|unset.UnsetType" = unset.Unset,
    ) -> None:
        super().__init__(initial_message)
        if not isinstance(phase, unset.UnsetType):
            self.phase = phase
        if not isinstance(state, unset.UnsetType):
            self.state = state
        if not isinstance(tracking_endpoint, unset.UnsetType):
            self.tracking_endpoint = tracking_endpoint
        if not isinstance(effective_storage_bucket_name, unset.UnsetType):
            self.effective_storage_bucket_name = effective_storage_bucket_name
        if not isinstance(experiments_count, unset.UnsetType):
            self.experiments_count = experiments_count
        if not isinstance(mlflow_version, unset.UnsetType):
            self.mlflow_version = mlflow_version
        if not isinstance(tracking_endpoints, unset.UnsetType):
            self.tracking_endpoints = tracking_endpoints
    
    def __dir__(self) ->abc.Iterable[builtins.str]:
        return [
            "phase",
            "state",
            "tracking_endpoint",
            "effective_storage_bucket_name",
            "experiments_count",
            "mlflow_version",
            "tracking_endpoints",
        ]
    
    @builtins.property
    def phase(self) -> "v1alpha1_1.ClusterStatus.Phase":
        """
         Current phase of the cluster.
        """
        
        return super()._get_field("phase", explicit_presence=False,
        wrap=v1alpha1_1.ClusterStatus.Phase,
        )
    @phase.setter
    def phase(self, value: "v1alpha1_1.ClusterStatus.Phase|cluster_pb2_1.ClusterStatus.Phase|None") -> None:
        return super()._set_field("phase",value,explicit_presence=False,
        )
    
    @builtins.property
    def state(self) -> "v1alpha1_1.ClusterStatus.State":
        """
         State reflects substatus of the phase to define whether it's healthy or not.
        """
        
        return super()._get_field("state", explicit_presence=False,
        wrap=v1alpha1_1.ClusterStatus.State,
        )
    @state.setter
    def state(self, value: "v1alpha1_1.ClusterStatus.State|cluster_pb2_1.ClusterStatus.State|None") -> None:
        return super()._set_field("state",value,explicit_presence=False,
        )
    
    @builtins.property
    def tracking_endpoint(self) -> "builtins.str":
        """
         Tracking endpoint url.
         Will be removed soon in favor of private_tracking_endpoint and public_tracking_endpoint.
        """
        
        return super()._get_field("tracking_endpoint", explicit_presence=False,
        )
    @tracking_endpoint.setter
    def tracking_endpoint(self, value: "builtins.str|None") -> None:
        return super()._set_field("tracking_endpoint",value,explicit_presence=False,
        )
    
    @builtins.property
    def effective_storage_bucket_name(self) -> "builtins.str":
        """
         Name of the Nebius S3 bucket for MLflow artifacts.
        """
        
        return super()._get_field("effective_storage_bucket_name", explicit_presence=False,
        )
    @effective_storage_bucket_name.setter
    def effective_storage_bucket_name(self, value: "builtins.str|None") -> None:
        return super()._set_field("effective_storage_bucket_name",value,explicit_presence=False,
        )
    
    @builtins.property
    def experiments_count(self) -> "builtins.int":
        """
         Count of experiments in the MLflow cluster
        """
        
        return super()._get_field("experiments_count", explicit_presence=False,
        )
    @experiments_count.setter
    def experiments_count(self, value: "builtins.int|None") -> None:
        return super()._set_field("experiments_count",value,explicit_presence=False,
        )
    
    @builtins.property
    def mlflow_version(self) -> "builtins.str":
        """
         MLflow version
        """
        
        return super()._get_field("mlflow_version", explicit_presence=False,
        )
    @mlflow_version.setter
    def mlflow_version(self, value: "builtins.str|None") -> None:
        return super()._set_field("mlflow_version",value,explicit_presence=False,
        )
    
    @builtins.property
    def tracking_endpoints(self) -> "Endpoints":
        """
         Public and private tracking endpoints
        """
        
        return super()._get_field("tracking_endpoints", explicit_presence=False,
        wrap=Endpoints,
        )
    @tracking_endpoints.setter
    def tracking_endpoints(self, value: "Endpoints|cluster_pb2.Endpoints|None") -> None:
        return super()._set_field("tracking_endpoints",value,explicit_presence=False,
        )
    
    __PY_TO_PB2__: builtins.dict[builtins.str,builtins.str] = {
        "phase":"phase",
        "state":"state",
        "tracking_endpoint":"tracking_endpoint",
        "effective_storage_bucket_name":"effective_storage_bucket_name",
        "experiments_count":"experiments_count",
        "mlflow_version":"mlflow_version",
        "tracking_endpoints":"tracking_endpoints",
    }
    
class Endpoints(pb_classes.Message):
    __PB2_CLASS__ = cluster_pb2.Endpoints
    __PB2_DESCRIPTOR__ = descriptor.DescriptorWrap[descriptor_1.Descriptor](".nebius.msp.mlflow.v1alpha1.Endpoints",cluster_pb2.DESCRIPTOR,descriptor_1.Descriptor)
    __mask_functions__ = {
    }
    
    def __init__(
        self,
        initial_message: message_1.Message|None = None,
        *,
        private: "builtins.str|None|unset.UnsetType" = unset.Unset,
        public: "builtins.str|None|unset.UnsetType" = unset.Unset,
    ) -> None:
        super().__init__(initial_message)
        if not isinstance(private, unset.UnsetType):
            self.private = private
        if not isinstance(public, unset.UnsetType):
            self.public = public
    
    def __dir__(self) ->abc.Iterable[builtins.str]:
        return [
            "private",
            "public",
        ]
    
    @builtins.property
    def private(self) -> "builtins.str":
        """
         Private endpoint
        """
        
        return super()._get_field("private", explicit_presence=False,
        )
    @private.setter
    def private(self, value: "builtins.str|None") -> None:
        return super()._set_field("private",value,explicit_presence=False,
        )
    
    @builtins.property
    def public(self) -> "builtins.str":
        """
         Public endpoint
        """
        
        return super()._get_field("public", explicit_presence=False,
        )
    @public.setter
    def public(self, value: "builtins.str|None") -> None:
        return super()._set_field("public",value,explicit_presence=False,
        )
    
    __PY_TO_PB2__: builtins.dict[builtins.str,builtins.str] = {
        "private":"private",
        "public":"public",
    }
    
# file: nebius/msp/mlflow/v1alpha1/cluster_service.proto
class GetClusterRequest(pb_classes.Message):
    __PB2_CLASS__ = cluster_service_pb2.GetClusterRequest
    __PB2_DESCRIPTOR__ = descriptor.DescriptorWrap[descriptor_1.Descriptor](".nebius.msp.mlflow.v1alpha1.GetClusterRequest",cluster_service_pb2.DESCRIPTOR,descriptor_1.Descriptor)
    __mask_functions__ = {
    }
    
    def __init__(
        self,
        initial_message: message_1.Message|None = None,
        *,
        id: "builtins.str|None|unset.UnsetType" = unset.Unset,
    ) -> None:
        super().__init__(initial_message)
        if not isinstance(id, unset.UnsetType):
            self.id = id
    
    def __dir__(self) ->abc.Iterable[builtins.str]:
        return [
            "id",
        ]
    
    @builtins.property
    def id(self) -> "builtins.str":
        """
         ID of the cluster to retrieve.
        """
        
        return super()._get_field("id", explicit_presence=False,
        )
    @id.setter
    def id(self, value: "builtins.str|None") -> None:
        return super()._set_field("id",value,explicit_presence=False,
        )
    
    __PY_TO_PB2__: builtins.dict[builtins.str,builtins.str] = {
        "id":"id",
    }
    
class GetClusterByNameRequest(pb_classes.Message):
    __PB2_CLASS__ = cluster_service_pb2.GetClusterByNameRequest
    __PB2_DESCRIPTOR__ = descriptor.DescriptorWrap[descriptor_1.Descriptor](".nebius.msp.mlflow.v1alpha1.GetClusterByNameRequest",cluster_service_pb2.DESCRIPTOR,descriptor_1.Descriptor)
    __mask_functions__ = {
    }
    
    def __init__(
        self,
        initial_message: message_1.Message|None = None,
        *,
        parent_id: "builtins.str|None|unset.UnsetType" = unset.Unset,
        name: "builtins.str|None|unset.UnsetType" = unset.Unset,
    ) -> None:
        super().__init__(initial_message)
        if not isinstance(parent_id, unset.UnsetType):
            self.parent_id = parent_id
        if not isinstance(name, unset.UnsetType):
            self.name = name
    
    def __dir__(self) ->abc.Iterable[builtins.str]:
        return [
            "parent_id",
            "name",
        ]
    
    @builtins.property
    def parent_id(self) -> "builtins.str":
        """
         Identifier of IAM container to get cluster from.
        """
        
        return super()._get_field("parent_id", explicit_presence=False,
        )
    @parent_id.setter
    def parent_id(self, value: "builtins.str|None") -> None:
        return super()._set_field("parent_id",value,explicit_presence=False,
        )
    
    @builtins.property
    def name(self) -> "builtins.str":
        """
         Name of the cluster.
        """
        
        return super()._get_field("name", explicit_presence=False,
        )
    @name.setter
    def name(self, value: "builtins.str|None") -> None:
        return super()._set_field("name",value,explicit_presence=False,
        )
    
    __PY_TO_PB2__: builtins.dict[builtins.str,builtins.str] = {
        "parent_id":"parent_id",
        "name":"name",
    }
    
class ListClustersRequest(pb_classes.Message):
    __PB2_CLASS__ = cluster_service_pb2.ListClustersRequest
    __PB2_DESCRIPTOR__ = descriptor.DescriptorWrap[descriptor_1.Descriptor](".nebius.msp.mlflow.v1alpha1.ListClustersRequest",cluster_service_pb2.DESCRIPTOR,descriptor_1.Descriptor)
    __mask_functions__ = {
    }
    
    def __init__(
        self,
        initial_message: message_1.Message|None = None,
        *,
        parent_id: "builtins.str|None|unset.UnsetType" = unset.Unset,
        page_size: "builtins.int|None|unset.UnsetType" = unset.Unset,
        page_token: "builtins.str|None|unset.UnsetType" = unset.Unset,
    ) -> None:
        super().__init__(initial_message)
        if not isinstance(parent_id, unset.UnsetType):
            self.parent_id = parent_id
        if not isinstance(page_size, unset.UnsetType):
            self.page_size = page_size
        if not isinstance(page_token, unset.UnsetType):
            self.page_token = page_token
    
    def __dir__(self) ->abc.Iterable[builtins.str]:
        return [
            "parent_id",
            "page_size",
            "page_token",
        ]
    
    @builtins.property
    def parent_id(self) -> "builtins.str":
        """
         Identifier of IAM container to list clusters from.
        """
        
        return super()._get_field("parent_id", explicit_presence=False,
        )
    @parent_id.setter
    def parent_id(self, value: "builtins.str|None") -> None:
        return super()._set_field("parent_id",value,explicit_presence=False,
        )
    
    @builtins.property
    def page_size(self) -> "builtins.int":
        """
         Specifies the maximum number of items to return in the response. Default value is 100.
        """
        
        return super()._get_field("page_size", explicit_presence=False,
        )
    @page_size.setter
    def page_size(self, value: "builtins.int|None") -> None:
        return super()._set_field("page_size",value,explicit_presence=False,
        )
    
    @builtins.property
    def page_token(self) -> "builtins.str":
        """
         Token for pagination, allowing the retrieval of the next set of results.
        """
        
        return super()._get_field("page_token", explicit_presence=False,
        )
    @page_token.setter
    def page_token(self, value: "builtins.str|None") -> None:
        return super()._set_field("page_token",value,explicit_presence=False,
        )
    
    __PY_TO_PB2__: builtins.dict[builtins.str,builtins.str] = {
        "parent_id":"parent_id",
        "page_size":"page_size",
        "page_token":"page_token",
    }
    
class ListClustersResponse(pb_classes.Message):
    __PB2_CLASS__ = cluster_service_pb2.ListClustersResponse
    __PB2_DESCRIPTOR__ = descriptor.DescriptorWrap[descriptor_1.Descriptor](".nebius.msp.mlflow.v1alpha1.ListClustersResponse",cluster_service_pb2.DESCRIPTOR,descriptor_1.Descriptor)
    __mask_functions__ = {
    }
    
    def __init__(
        self,
        initial_message: message_1.Message|None = None,
        *,
        items: "abc.Iterable[Cluster]|None|unset.UnsetType" = unset.Unset,
        next_page_token: "builtins.str|None|unset.UnsetType" = unset.Unset,
    ) -> None:
        super().__init__(initial_message)
        if not isinstance(items, unset.UnsetType):
            self.items = items
        if not isinstance(next_page_token, unset.UnsetType):
            self.next_page_token = next_page_token
    
    def __dir__(self) ->abc.Iterable[builtins.str]:
        return [
            "items",
            "next_page_token",
        ]
    
    @builtins.property
    def items(self) -> "abc.MutableSequence[Cluster]":
        """
         List of clusters.
        """
        
        return super()._get_field("items", explicit_presence=False,
        wrap=pb_classes.Repeated.with_wrap(Cluster,None,None),
        )
    @items.setter
    def items(self, value: "abc.Iterable[Cluster]|None") -> None:
        return super()._set_field("items",value,explicit_presence=False,
        )
    
    @builtins.property
    def next_page_token(self) -> "builtins.str":
        """
         Token for pagination, indicating the next set of results can be retrieved using this token.
        """
        
        return super()._get_field("next_page_token", explicit_presence=False,
        )
    @next_page_token.setter
    def next_page_token(self, value: "builtins.str|None") -> None:
        return super()._set_field("next_page_token",value,explicit_presence=False,
        )
    
    __PY_TO_PB2__: builtins.dict[builtins.str,builtins.str] = {
        "items":"items",
        "next_page_token":"next_page_token",
    }
    
class CreateClusterRequest(pb_classes.Message):
    __PB2_CLASS__ = cluster_service_pb2.CreateClusterRequest
    __PB2_DESCRIPTOR__ = descriptor.DescriptorWrap[descriptor_1.Descriptor](".nebius.msp.mlflow.v1alpha1.CreateClusterRequest",cluster_service_pb2.DESCRIPTOR,descriptor_1.Descriptor)
    __mask_functions__ = {
    }
    
    def __init__(
        self,
        initial_message: message_1.Message|None = None,
        *,
        metadata: "v1_1.ResourceMetadata|metadata_pb2.ResourceMetadata|None|unset.UnsetType" = unset.Unset,
        spec: "ClusterSpec|cluster_pb2.ClusterSpec|None|unset.UnsetType" = unset.Unset,
    ) -> None:
        super().__init__(initial_message)
        if not isinstance(metadata, unset.UnsetType):
            self.metadata = metadata
        if not isinstance(spec, unset.UnsetType):
            self.spec = spec
    
    def __dir__(self) ->abc.Iterable[builtins.str]:
        return [
            "metadata",
            "spec",
        ]
    
    @builtins.property
    def metadata(self) -> "v1_1.ResourceMetadata":
        """
         Metadata associated with the new cluster. Must include parent_id in which we create the cluster.
        """
        
        return super()._get_field("metadata", explicit_presence=False,
        wrap=v1_1.ResourceMetadata,
        )
    @metadata.setter
    def metadata(self, value: "v1_1.ResourceMetadata|metadata_pb2.ResourceMetadata|None") -> None:
        return super()._set_field("metadata",value,explicit_presence=False,
        )
    
    @builtins.property
    def spec(self) -> "ClusterSpec":
        """
         Specification for the new cluster.
        """
        
        return super()._get_field("spec", explicit_presence=False,
        wrap=ClusterSpec,
        )
    @spec.setter
    def spec(self, value: "ClusterSpec|cluster_pb2.ClusterSpec|None") -> None:
        return super()._set_field("spec",value,explicit_presence=False,
        )
    
    __PY_TO_PB2__: builtins.dict[builtins.str,builtins.str] = {
        "metadata":"metadata",
        "spec":"spec",
    }
    
class DeleteClusterRequest(pb_classes.Message):
    __PB2_CLASS__ = cluster_service_pb2.DeleteClusterRequest
    __PB2_DESCRIPTOR__ = descriptor.DescriptorWrap[descriptor_1.Descriptor](".nebius.msp.mlflow.v1alpha1.DeleteClusterRequest",cluster_service_pb2.DESCRIPTOR,descriptor_1.Descriptor)
    __mask_functions__ = {
    }
    
    def __init__(
        self,
        initial_message: message_1.Message|None = None,
        *,
        id: "builtins.str|None|unset.UnsetType" = unset.Unset,
    ) -> None:
        super().__init__(initial_message)
        if not isinstance(id, unset.UnsetType):
            self.id = id
    
    def __dir__(self) ->abc.Iterable[builtins.str]:
        return [
            "id",
        ]
    
    @builtins.property
    def id(self) -> "builtins.str":
        """
         ID of the cluster to delete.
        """
        
        return super()._get_field("id", explicit_presence=False,
        )
    @id.setter
    def id(self, value: "builtins.str|None") -> None:
        return super()._set_field("id",value,explicit_presence=False,
        )
    
    __PY_TO_PB2__: builtins.dict[builtins.str,builtins.str] = {
        "id":"id",
    }
    

class ClusterServiceClient(client.Client):
    __PB2_DESCRIPTOR__ = descriptor.DescriptorWrap[descriptor_1.ServiceDescriptor](".nebius.msp.mlflow.v1alpha1.ClusterService",cluster_service_pb2.DESCRIPTOR,descriptor_1.ServiceDescriptor)
    __service_name__ = ".nebius.msp.mlflow.v1alpha1.ClusterService"
    __operation_type__ = v1alpha1_2.Operation
    
    def get(self,
        request: "GetClusterRequest",
        metadata: abc.Iterable[builtins.tuple[builtins.str,builtins.str]]|None = None,
        timeout: builtins.float|None = None,
        credentials: grpc.CallCredentials | None = None,
        compression: grpc.Compression | None = None,
        retries: builtins.int | None = 3,
    ) -> request_1.Request["GetClusterRequest","Cluster"]:
        """
         Returns the specified cluster.
        """
        
        return super().request(
            method="Get",
            request=request,
            result_pb2_class=cluster_pb2.Cluster,
            metadata=metadata,
            timeout=timeout,
            credentials=credentials,
            compression=compression,
            retries=retries,
            result_wrapper=pb_classes.simple_wrapper(Cluster),
        )
    
    def get_by_name(self,
        request: "GetClusterByNameRequest",
        metadata: abc.Iterable[builtins.tuple[builtins.str,builtins.str]]|None = None,
        timeout: builtins.float|None = None,
        credentials: grpc.CallCredentials | None = None,
        compression: grpc.Compression | None = None,
        retries: builtins.int | None = 3,
    ) -> request_1.Request["GetClusterByNameRequest","Cluster"]:
        """
         Returns the specified cluster.
        """
        
        return super().request(
            method="GetByName",
            request=request,
            result_pb2_class=cluster_pb2.Cluster,
            metadata=metadata,
            timeout=timeout,
            credentials=credentials,
            compression=compression,
            retries=retries,
            result_wrapper=pb_classes.simple_wrapper(Cluster),
        )
    
    def list(self,
        request: "ListClustersRequest",
        metadata: abc.Iterable[builtins.tuple[builtins.str,builtins.str]]|None = None,
        timeout: builtins.float|None = None,
        credentials: grpc.CallCredentials | None = None,
        compression: grpc.Compression | None = None,
        retries: builtins.int | None = 3,
    ) -> request_1.Request["ListClustersRequest","ListClustersResponse"]:
        """
         Retrieves a list of clusters.
        """
        
        return super().request(
            method="List",
            request=request,
            result_pb2_class=cluster_service_pb2.ListClustersResponse,
            metadata=metadata,
            timeout=timeout,
            credentials=credentials,
            compression=compression,
            retries=retries,
            result_wrapper=pb_classes.simple_wrapper(ListClustersResponse),
        )
    
    def create(self,
        request: "CreateClusterRequest",
        metadata: abc.Iterable[builtins.tuple[builtins.str,builtins.str]]|None = None,
        timeout: builtins.float|None = None,
        credentials: grpc.CallCredentials | None = None,
        compression: grpc.Compression | None = None,
        retries: builtins.int | None = 3,
    ) -> request_1.Request["CreateClusterRequest","operation.Operation[v1alpha1_2.Operation]"]:
        """
         Creates a cluster.
        """
        
        return super().request(
            method="Create",
            request=request,
            result_pb2_class=operation_pb2.Operation,
            metadata=metadata,
            timeout=timeout,
            credentials=credentials,
            compression=compression,
            retries=retries,
            result_wrapper=operation.Operation,
        )
    
    def delete(self,
        request: "DeleteClusterRequest",
        metadata: abc.Iterable[builtins.tuple[builtins.str,builtins.str]]|None = None,
        timeout: builtins.float|None = None,
        credentials: grpc.CallCredentials | None = None,
        compression: grpc.Compression | None = None,
        retries: builtins.int | None = 3,
    ) -> request_1.Request["DeleteClusterRequest","operation.Operation[v1alpha1_2.Operation]"]:
        """
         Delete a cluster.
        """
        
        return super().request(
            method="Delete",
            request=request,
            result_pb2_class=operation_pb2.Operation,
            metadata=metadata,
            timeout=timeout,
            credentials=credentials,
            compression=compression,
            retries=retries,
            result_wrapper=operation.Operation,
        )
    

__all__ = [
    #@ local import names here @#
    "Cluster",
    "ClusterSpec",
    "MlflowClusterStatus",
    "Endpoints",
    "GetClusterRequest",
    "GetClusterByNameRequest",
    "ListClustersRequest",
    "ListClustersResponse",
    "CreateClusterRequest",
    "DeleteClusterRequest",
    "ClusterServiceClient",
]

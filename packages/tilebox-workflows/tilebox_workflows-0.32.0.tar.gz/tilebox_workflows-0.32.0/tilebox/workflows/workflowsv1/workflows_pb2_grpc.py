# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from tilebox.workflows.workflowsv1 import core_pb2 as workflows_dot_v1_dot_core__pb2
from tilebox.workflows.workflowsv1 import workflows_pb2 as workflows_dot_v1_dot_workflows__pb2


class WorkflowsServiceStub(object):
    """A service for managing workflows.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateCluster = channel.unary_unary(
                '/workflows.v1.WorkflowsService/CreateCluster',
                request_serializer=workflows_dot_v1_dot_workflows__pb2.CreateClusterRequest.SerializeToString,
                response_deserializer=workflows_dot_v1_dot_core__pb2.Cluster.FromString,
                _registered_method=True)
        self.GetCluster = channel.unary_unary(
                '/workflows.v1.WorkflowsService/GetCluster',
                request_serializer=workflows_dot_v1_dot_workflows__pb2.GetClusterRequest.SerializeToString,
                response_deserializer=workflows_dot_v1_dot_core__pb2.Cluster.FromString,
                _registered_method=True)
        self.DeleteCluster = channel.unary_unary(
                '/workflows.v1.WorkflowsService/DeleteCluster',
                request_serializer=workflows_dot_v1_dot_workflows__pb2.DeleteClusterRequest.SerializeToString,
                response_deserializer=workflows_dot_v1_dot_workflows__pb2.DeleteClusterResponse.FromString,
                _registered_method=True)
        self.ListClusters = channel.unary_unary(
                '/workflows.v1.WorkflowsService/ListClusters',
                request_serializer=workflows_dot_v1_dot_workflows__pb2.ListClustersRequest.SerializeToString,
                response_deserializer=workflows_dot_v1_dot_workflows__pb2.ListClustersResponse.FromString,
                _registered_method=True)


class WorkflowsServiceServicer(object):
    """A service for managing workflows.
    """

    def CreateCluster(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetCluster(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteCluster(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListClusters(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_WorkflowsServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CreateCluster': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateCluster,
                    request_deserializer=workflows_dot_v1_dot_workflows__pb2.CreateClusterRequest.FromString,
                    response_serializer=workflows_dot_v1_dot_core__pb2.Cluster.SerializeToString,
            ),
            'GetCluster': grpc.unary_unary_rpc_method_handler(
                    servicer.GetCluster,
                    request_deserializer=workflows_dot_v1_dot_workflows__pb2.GetClusterRequest.FromString,
                    response_serializer=workflows_dot_v1_dot_core__pb2.Cluster.SerializeToString,
            ),
            'DeleteCluster': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteCluster,
                    request_deserializer=workflows_dot_v1_dot_workflows__pb2.DeleteClusterRequest.FromString,
                    response_serializer=workflows_dot_v1_dot_workflows__pb2.DeleteClusterResponse.SerializeToString,
            ),
            'ListClusters': grpc.unary_unary_rpc_method_handler(
                    servicer.ListClusters,
                    request_deserializer=workflows_dot_v1_dot_workflows__pb2.ListClustersRequest.FromString,
                    response_serializer=workflows_dot_v1_dot_workflows__pb2.ListClustersResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'workflows.v1.WorkflowsService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('workflows.v1.WorkflowsService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class WorkflowsService(object):
    """A service for managing workflows.
    """

    @staticmethod
    def CreateCluster(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/workflows.v1.WorkflowsService/CreateCluster',
            workflows_dot_v1_dot_workflows__pb2.CreateClusterRequest.SerializeToString,
            workflows_dot_v1_dot_core__pb2.Cluster.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetCluster(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/workflows.v1.WorkflowsService/GetCluster',
            workflows_dot_v1_dot_workflows__pb2.GetClusterRequest.SerializeToString,
            workflows_dot_v1_dot_core__pb2.Cluster.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def DeleteCluster(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/workflows.v1.WorkflowsService/DeleteCluster',
            workflows_dot_v1_dot_workflows__pb2.DeleteClusterRequest.SerializeToString,
            workflows_dot_v1_dot_workflows__pb2.DeleteClusterResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def ListClusters(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/workflows.v1.WorkflowsService/ListClusters',
            workflows_dot_v1_dot_workflows__pb2.ListClustersRequest.SerializeToString,
            workflows_dot_v1_dot_workflows__pb2.ListClustersResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

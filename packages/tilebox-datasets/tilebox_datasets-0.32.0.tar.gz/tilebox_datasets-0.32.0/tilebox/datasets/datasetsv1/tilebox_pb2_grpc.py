# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from tilebox.datasets.datasetsv1 import core_pb2 as datasets_dot_v1_dot_core__pb2
from tilebox.datasets.datasetsv1 import tilebox_pb2 as datasets_dot_v1_dot_tilebox__pb2


class TileboxServiceStub(object):
    """TileboxService is the service definition for the Tilebox datasets service, which provides access to datasets
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateDataset = channel.unary_unary(
                '/datasets.v1.TileboxService/CreateDataset',
                request_serializer=datasets_dot_v1_dot_tilebox__pb2.CreateDatasetRequest.SerializeToString,
                response_deserializer=datasets_dot_v1_dot_core__pb2.Dataset.FromString,
                _registered_method=True)
        self.GetDataset = channel.unary_unary(
                '/datasets.v1.TileboxService/GetDataset',
                request_serializer=datasets_dot_v1_dot_tilebox__pb2.GetDatasetRequest.SerializeToString,
                response_deserializer=datasets_dot_v1_dot_core__pb2.Dataset.FromString,
                _registered_method=True)
        self.UpdateDataset = channel.unary_unary(
                '/datasets.v1.TileboxService/UpdateDataset',
                request_serializer=datasets_dot_v1_dot_tilebox__pb2.UpdateDatasetRequest.SerializeToString,
                response_deserializer=datasets_dot_v1_dot_core__pb2.Dataset.FromString,
                _registered_method=True)
        self.UpdateDatasetDescription = channel.unary_unary(
                '/datasets.v1.TileboxService/UpdateDatasetDescription',
                request_serializer=datasets_dot_v1_dot_tilebox__pb2.UpdateDatasetDescriptionRequest.SerializeToString,
                response_deserializer=datasets_dot_v1_dot_core__pb2.Dataset.FromString,
                _registered_method=True)
        self.ListDatasets = channel.unary_unary(
                '/datasets.v1.TileboxService/ListDatasets',
                request_serializer=datasets_dot_v1_dot_tilebox__pb2.ListDatasetsRequest.SerializeToString,
                response_deserializer=datasets_dot_v1_dot_tilebox__pb2.ListDatasetsResponse.FromString,
                _registered_method=True)
        self.CreateCollection = channel.unary_unary(
                '/datasets.v1.TileboxService/CreateCollection',
                request_serializer=datasets_dot_v1_dot_core__pb2.CreateCollectionRequest.SerializeToString,
                response_deserializer=datasets_dot_v1_dot_core__pb2.CollectionInfo.FromString,
                _registered_method=True)
        self.GetCollections = channel.unary_unary(
                '/datasets.v1.TileboxService/GetCollections',
                request_serializer=datasets_dot_v1_dot_core__pb2.GetCollectionsRequest.SerializeToString,
                response_deserializer=datasets_dot_v1_dot_core__pb2.Collections.FromString,
                _registered_method=True)
        self.GetCollectionByName = channel.unary_unary(
                '/datasets.v1.TileboxService/GetCollectionByName',
                request_serializer=datasets_dot_v1_dot_core__pb2.GetCollectionByNameRequest.SerializeToString,
                response_deserializer=datasets_dot_v1_dot_core__pb2.CollectionInfo.FromString,
                _registered_method=True)
        self.GetDatasetForInterval = channel.unary_unary(
                '/datasets.v1.TileboxService/GetDatasetForInterval',
                request_serializer=datasets_dot_v1_dot_core__pb2.GetDatasetForIntervalRequest.SerializeToString,
                response_deserializer=datasets_dot_v1_dot_tilebox__pb2.Datapoints.FromString,
                _registered_method=True)
        self.GetDatapointByID = channel.unary_unary(
                '/datasets.v1.TileboxService/GetDatapointByID',
                request_serializer=datasets_dot_v1_dot_core__pb2.GetDatapointByIdRequest.SerializeToString,
                response_deserializer=datasets_dot_v1_dot_tilebox__pb2.Datapoint.FromString,
                _registered_method=True)
        self.IngestDatapoints = channel.unary_unary(
                '/datasets.v1.TileboxService/IngestDatapoints',
                request_serializer=datasets_dot_v1_dot_tilebox__pb2.IngestDatapointsRequest.SerializeToString,
                response_deserializer=datasets_dot_v1_dot_tilebox__pb2.IngestDatapointsResponse.FromString,
                _registered_method=True)
        self.DeleteDatapoints = channel.unary_unary(
                '/datasets.v1.TileboxService/DeleteDatapoints',
                request_serializer=datasets_dot_v1_dot_tilebox__pb2.DeleteDatapointsRequest.SerializeToString,
                response_deserializer=datasets_dot_v1_dot_tilebox__pb2.DeleteDatapointsResponse.FromString,
                _registered_method=True)


class TileboxServiceServicer(object):
    """TileboxService is the service definition for the Tilebox datasets service, which provides access to datasets
    """

    def CreateDataset(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetDataset(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateDataset(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateDatasetDescription(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListDatasets(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateCollection(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetCollections(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetCollectionByName(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetDatasetForInterval(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetDatapointByID(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def IngestDatapoints(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteDatapoints(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_TileboxServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CreateDataset': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateDataset,
                    request_deserializer=datasets_dot_v1_dot_tilebox__pb2.CreateDatasetRequest.FromString,
                    response_serializer=datasets_dot_v1_dot_core__pb2.Dataset.SerializeToString,
            ),
            'GetDataset': grpc.unary_unary_rpc_method_handler(
                    servicer.GetDataset,
                    request_deserializer=datasets_dot_v1_dot_tilebox__pb2.GetDatasetRequest.FromString,
                    response_serializer=datasets_dot_v1_dot_core__pb2.Dataset.SerializeToString,
            ),
            'UpdateDataset': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateDataset,
                    request_deserializer=datasets_dot_v1_dot_tilebox__pb2.UpdateDatasetRequest.FromString,
                    response_serializer=datasets_dot_v1_dot_core__pb2.Dataset.SerializeToString,
            ),
            'UpdateDatasetDescription': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateDatasetDescription,
                    request_deserializer=datasets_dot_v1_dot_tilebox__pb2.UpdateDatasetDescriptionRequest.FromString,
                    response_serializer=datasets_dot_v1_dot_core__pb2.Dataset.SerializeToString,
            ),
            'ListDatasets': grpc.unary_unary_rpc_method_handler(
                    servicer.ListDatasets,
                    request_deserializer=datasets_dot_v1_dot_tilebox__pb2.ListDatasetsRequest.FromString,
                    response_serializer=datasets_dot_v1_dot_tilebox__pb2.ListDatasetsResponse.SerializeToString,
            ),
            'CreateCollection': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateCollection,
                    request_deserializer=datasets_dot_v1_dot_core__pb2.CreateCollectionRequest.FromString,
                    response_serializer=datasets_dot_v1_dot_core__pb2.CollectionInfo.SerializeToString,
            ),
            'GetCollections': grpc.unary_unary_rpc_method_handler(
                    servicer.GetCollections,
                    request_deserializer=datasets_dot_v1_dot_core__pb2.GetCollectionsRequest.FromString,
                    response_serializer=datasets_dot_v1_dot_core__pb2.Collections.SerializeToString,
            ),
            'GetCollectionByName': grpc.unary_unary_rpc_method_handler(
                    servicer.GetCollectionByName,
                    request_deserializer=datasets_dot_v1_dot_core__pb2.GetCollectionByNameRequest.FromString,
                    response_serializer=datasets_dot_v1_dot_core__pb2.CollectionInfo.SerializeToString,
            ),
            'GetDatasetForInterval': grpc.unary_unary_rpc_method_handler(
                    servicer.GetDatasetForInterval,
                    request_deserializer=datasets_dot_v1_dot_core__pb2.GetDatasetForIntervalRequest.FromString,
                    response_serializer=datasets_dot_v1_dot_tilebox__pb2.Datapoints.SerializeToString,
            ),
            'GetDatapointByID': grpc.unary_unary_rpc_method_handler(
                    servicer.GetDatapointByID,
                    request_deserializer=datasets_dot_v1_dot_core__pb2.GetDatapointByIdRequest.FromString,
                    response_serializer=datasets_dot_v1_dot_tilebox__pb2.Datapoint.SerializeToString,
            ),
            'IngestDatapoints': grpc.unary_unary_rpc_method_handler(
                    servicer.IngestDatapoints,
                    request_deserializer=datasets_dot_v1_dot_tilebox__pb2.IngestDatapointsRequest.FromString,
                    response_serializer=datasets_dot_v1_dot_tilebox__pb2.IngestDatapointsResponse.SerializeToString,
            ),
            'DeleteDatapoints': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteDatapoints,
                    request_deserializer=datasets_dot_v1_dot_tilebox__pb2.DeleteDatapointsRequest.FromString,
                    response_serializer=datasets_dot_v1_dot_tilebox__pb2.DeleteDatapointsResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'datasets.v1.TileboxService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('datasets.v1.TileboxService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class TileboxService(object):
    """TileboxService is the service definition for the Tilebox datasets service, which provides access to datasets
    """

    @staticmethod
    def CreateDataset(request,
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
            '/datasets.v1.TileboxService/CreateDataset',
            datasets_dot_v1_dot_tilebox__pb2.CreateDatasetRequest.SerializeToString,
            datasets_dot_v1_dot_core__pb2.Dataset.FromString,
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
    def GetDataset(request,
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
            '/datasets.v1.TileboxService/GetDataset',
            datasets_dot_v1_dot_tilebox__pb2.GetDatasetRequest.SerializeToString,
            datasets_dot_v1_dot_core__pb2.Dataset.FromString,
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
    def UpdateDataset(request,
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
            '/datasets.v1.TileboxService/UpdateDataset',
            datasets_dot_v1_dot_tilebox__pb2.UpdateDatasetRequest.SerializeToString,
            datasets_dot_v1_dot_core__pb2.Dataset.FromString,
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
    def UpdateDatasetDescription(request,
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
            '/datasets.v1.TileboxService/UpdateDatasetDescription',
            datasets_dot_v1_dot_tilebox__pb2.UpdateDatasetDescriptionRequest.SerializeToString,
            datasets_dot_v1_dot_core__pb2.Dataset.FromString,
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
    def ListDatasets(request,
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
            '/datasets.v1.TileboxService/ListDatasets',
            datasets_dot_v1_dot_tilebox__pb2.ListDatasetsRequest.SerializeToString,
            datasets_dot_v1_dot_tilebox__pb2.ListDatasetsResponse.FromString,
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
    def CreateCollection(request,
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
            '/datasets.v1.TileboxService/CreateCollection',
            datasets_dot_v1_dot_core__pb2.CreateCollectionRequest.SerializeToString,
            datasets_dot_v1_dot_core__pb2.CollectionInfo.FromString,
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
    def GetCollections(request,
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
            '/datasets.v1.TileboxService/GetCollections',
            datasets_dot_v1_dot_core__pb2.GetCollectionsRequest.SerializeToString,
            datasets_dot_v1_dot_core__pb2.Collections.FromString,
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
    def GetCollectionByName(request,
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
            '/datasets.v1.TileboxService/GetCollectionByName',
            datasets_dot_v1_dot_core__pb2.GetCollectionByNameRequest.SerializeToString,
            datasets_dot_v1_dot_core__pb2.CollectionInfo.FromString,
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
    def GetDatasetForInterval(request,
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
            '/datasets.v1.TileboxService/GetDatasetForInterval',
            datasets_dot_v1_dot_core__pb2.GetDatasetForIntervalRequest.SerializeToString,
            datasets_dot_v1_dot_tilebox__pb2.Datapoints.FromString,
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
    def GetDatapointByID(request,
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
            '/datasets.v1.TileboxService/GetDatapointByID',
            datasets_dot_v1_dot_core__pb2.GetDatapointByIdRequest.SerializeToString,
            datasets_dot_v1_dot_tilebox__pb2.Datapoint.FromString,
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
    def IngestDatapoints(request,
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
            '/datasets.v1.TileboxService/IngestDatapoints',
            datasets_dot_v1_dot_tilebox__pb2.IngestDatapointsRequest.SerializeToString,
            datasets_dot_v1_dot_tilebox__pb2.IngestDatapointsResponse.FromString,
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
    def DeleteDatapoints(request,
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
            '/datasets.v1.TileboxService/DeleteDatapoints',
            datasets_dot_v1_dot_tilebox__pb2.DeleteDatapointsRequest.SerializeToString,
            datasets_dot_v1_dot_tilebox__pb2.DeleteDatapointsResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

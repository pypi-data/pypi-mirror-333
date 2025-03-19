# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from velocitas_sdk.proto import broker_pb2 as sdv_dot_databroker_dot_v1_dot_broker__pb2


class BrokerStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetDatapoints = channel.unary_unary(
                '/sdv.databroker.v1.Broker/GetDatapoints',
                request_serializer=sdv_dot_databroker_dot_v1_dot_broker__pb2.GetDatapointsRequest.SerializeToString,
                response_deserializer=sdv_dot_databroker_dot_v1_dot_broker__pb2.GetDatapointsReply.FromString,
                )
        self.SetDatapoints = channel.unary_unary(
                '/sdv.databroker.v1.Broker/SetDatapoints',
                request_serializer=sdv_dot_databroker_dot_v1_dot_broker__pb2.SetDatapointsRequest.SerializeToString,
                response_deserializer=sdv_dot_databroker_dot_v1_dot_broker__pb2.SetDatapointsReply.FromString,
                )
        self.Subscribe = channel.unary_stream(
                '/sdv.databroker.v1.Broker/Subscribe',
                request_serializer=sdv_dot_databroker_dot_v1_dot_broker__pb2.SubscribeRequest.SerializeToString,
                response_deserializer=sdv_dot_databroker_dot_v1_dot_broker__pb2.SubscribeReply.FromString,
                )
        self.GetMetadata = channel.unary_unary(
                '/sdv.databroker.v1.Broker/GetMetadata',
                request_serializer=sdv_dot_databroker_dot_v1_dot_broker__pb2.GetMetadataRequest.SerializeToString,
                response_deserializer=sdv_dot_databroker_dot_v1_dot_broker__pb2.GetMetadataReply.FromString,
                )


class BrokerServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetDatapoints(self, request, context):
        """Request a set of datapoints (values)

        Returns a list of requested data points.

        InvalidArgument is returned if the request is malformed.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetDatapoints(self, request, context):
        """Set a datapoint (values)
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Subscribe(self, request, context):
        """Subscribe to a set of data points or conditional expressions
        using the Data Broker Query Syntax (described in QUERY.md)

        Returns a stream of replies.

        InvalidArgument is returned if the request is malformed.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetMetadata(self, request, context):
        """Request the metadata of a set of datapoints

        Returns metadata of the requested data points that exist.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_BrokerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetDatapoints': grpc.unary_unary_rpc_method_handler(
                    servicer.GetDatapoints,
                    request_deserializer=sdv_dot_databroker_dot_v1_dot_broker__pb2.GetDatapointsRequest.FromString,
                    response_serializer=sdv_dot_databroker_dot_v1_dot_broker__pb2.GetDatapointsReply.SerializeToString,
            ),
            'SetDatapoints': grpc.unary_unary_rpc_method_handler(
                    servicer.SetDatapoints,
                    request_deserializer=sdv_dot_databroker_dot_v1_dot_broker__pb2.SetDatapointsRequest.FromString,
                    response_serializer=sdv_dot_databroker_dot_v1_dot_broker__pb2.SetDatapointsReply.SerializeToString,
            ),
            'Subscribe': grpc.unary_stream_rpc_method_handler(
                    servicer.Subscribe,
                    request_deserializer=sdv_dot_databroker_dot_v1_dot_broker__pb2.SubscribeRequest.FromString,
                    response_serializer=sdv_dot_databroker_dot_v1_dot_broker__pb2.SubscribeReply.SerializeToString,
            ),
            'GetMetadata': grpc.unary_unary_rpc_method_handler(
                    servicer.GetMetadata,
                    request_deserializer=sdv_dot_databroker_dot_v1_dot_broker__pb2.GetMetadataRequest.FromString,
                    response_serializer=sdv_dot_databroker_dot_v1_dot_broker__pb2.GetMetadataReply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'sdv.databroker.v1.Broker', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Broker(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetDatapoints(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sdv.databroker.v1.Broker/GetDatapoints',
            sdv_dot_databroker_dot_v1_dot_broker__pb2.GetDatapointsRequest.SerializeToString,
            sdv_dot_databroker_dot_v1_dot_broker__pb2.GetDatapointsReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SetDatapoints(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sdv.databroker.v1.Broker/SetDatapoints',
            sdv_dot_databroker_dot_v1_dot_broker__pb2.SetDatapointsRequest.SerializeToString,
            sdv_dot_databroker_dot_v1_dot_broker__pb2.SetDatapointsReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Subscribe(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/sdv.databroker.v1.Broker/Subscribe',
            sdv_dot_databroker_dot_v1_dot_broker__pb2.SubscribeRequest.SerializeToString,
            sdv_dot_databroker_dot_v1_dot_broker__pb2.SubscribeReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetMetadata(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sdv.databroker.v1.Broker/GetMetadata',
            sdv_dot_databroker_dot_v1_dot_broker__pb2.GetMetadataRequest.SerializeToString,
            sdv_dot_databroker_dot_v1_dot_broker__pb2.GetMetadataReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

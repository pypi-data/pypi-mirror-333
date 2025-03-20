import base64
import grpc

from . import link_pb2
from . import link_pb2_grpc


class GuardeyeUnaryUnaryMultiCallable:
    def __init__(self,
                 channel,
                 cid,
                 method,
                 request_serializer,
                 response_deserializer):
        self._channel = channel
        self._cid = cid
        self._method = method
        self._request_serializer = request_serializer
        self._response_deserializer = response_deserializer
        self.link_cli = link_pb2_grpc.LinkStub(self._channel)

    def __call__(self,
                 request,
                 timeout=None):
        req_bytes = self._request_serializer(request)
        req = link_pb2.LinkCallReq(
            cid=self._cid,
            method=self._method,
            data=base64.b64encode(req_bytes))
        rsp = self.link_cli.LinkCall(req)

        return self._response_deserializer(base64.b64decode(rsp.data))


class GuardeyeChannel:
    def __init__(self, target, cid):
        self._channel = grpc.insecure_channel(target)
        self._cid = cid

    def unary_unary(
            self,
            method: str,
            request_serializer=None,
            response_deserializer=None,
            _registered_method=False,
    ):
        return GuardeyeUnaryUnaryMultiCallable(
            self._channel,
            self._cid,
            method,
            request_serializer,
            response_deserializer,
        )


__all__ = [
    'GuardeyeChannel'
]

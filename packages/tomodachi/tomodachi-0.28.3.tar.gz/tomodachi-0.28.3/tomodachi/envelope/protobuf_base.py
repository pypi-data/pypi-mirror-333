import base64
import time
import uuid
import zlib
from typing import Any, Dict, Tuple, Union

from tomodachi import logging
from tomodachi.envelope.proto_build.protobuf.sns_sqs_message_pb2 import SNSSQSMessage

PROTOCOL_VERSION = "tomodachi-protobuf-base--1.0.0"


class ProtobufBase(object):
    @classmethod
    def validate(cls, **kwargs: Any) -> None:
        if "proto_class" not in kwargs:
            raise Exception("No proto_class defined")
        if kwargs.get("proto_class", None).__class__.__name__ not in ("GeneratedProtocolMessageType", "MessageMeta"):
            from google.protobuf.message import Message  # isort: skip

            if not issubclass(kwargs.get("proto_class", None), Message):
                raise Exception("keyword argument 'proto_class' is not a protobuf message class")

    @classmethod
    async def build_message(cls, service: Any, topic: str, data: Any, **kwargs: Any) -> str:
        message_data = data.SerializeToString()

        data_encoding = "proto"
        if len(message_data) > 60000:
            message_data = zlib.compress(data.SerializeToString())
            data_encoding = "gzip_proto"

        message = SNSSQSMessage()
        message.service.name = str(getattr(service, "name", None) or "")
        message.service.uuid = str(getattr(service, "uuid", None) or "")
        message.metadata.message_uuid = "{}.{}".format(getattr(service, "uuid", ""), str(uuid.uuid4()))
        message.metadata.protocol_version = PROTOCOL_VERSION
        message.metadata.timestamp = time.time()
        message.metadata.topic = topic
        message.metadata.data_encoding = data_encoding
        message.data = message_data

        return base64.b64encode(message.SerializeToString()).decode("ascii")

    @classmethod
    async def parse_message(
        cls, payload: str, proto_class: Any = None, validator: Any = None, **kwargs: Any
    ) -> Union[Dict, Tuple]:
        message = SNSSQSMessage()
        message.ParseFromString(base64.b64decode(payload))

        message_uuid = message.metadata.message_uuid
        timestamp = message.metadata.timestamp

        raw_data = None
        obj = None

        if not proto_class:
            raw_data = message.data
        else:
            obj = proto_class()
            if message.metadata.data_encoding == "proto":
                obj.ParseFromString(message.data)
            elif message.metadata.data_encoding == "base64":  # deprecated
                obj.ParseFromString(base64.b64decode(message.data))
            elif message.metadata.data_encoding == "gzip_proto":
                obj.ParseFromString(zlib.decompress(message.data))
            elif message.metadata.data_encoding == "base64_gzip_proto":  # deprecated
                obj.ParseFromString(zlib.decompress(base64.b64decode(message.data)))
            elif message.metadata.data_encoding == "raw":
                raw_data = message.data

        if validator is not None:
            try:
                if hasattr(validator, "__func__"):
                    # for static functions
                    validator.__func__(obj)
                else:
                    # for non-static functions
                    validator(obj)
            except Exception as e:
                logging.getLogger("tomodachi.envelope").warning(e.__str__(), envelope="ProtobufBase")
                raise e

        return (
            {
                "service": {"name": message.service.name, "uuid": message.service.uuid},
                "metadata": {
                    "message_uuid": message.metadata.message_uuid,
                    "protocol_version": message.metadata.protocol_version,
                    "timestamp": message.metadata.timestamp,
                    "topic": message.metadata.topic,
                    "data_encoding": message.metadata.data_encoding,
                },
                "data": raw_data if raw_data is not None else obj,
            },
            message_uuid,
            timestamp,
        )


__all__ = [
    "PROTOCOL_VERSION",
    "ProtobufBase",
    "SNSSQSMessage",
]

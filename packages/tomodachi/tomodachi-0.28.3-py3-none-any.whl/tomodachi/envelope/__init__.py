from typing import Any, Dict, Tuple, Union

__cached_defs: Dict[str, Any] = {}


def __getattr__(name: str) -> Any:
    if name in __cached_defs:
        return __cached_defs[name]

    import importlib  # noqa  # isort:skip

    if name == "JsonBase":
        module = importlib.import_module(".json_base", "tomodachi.envelope")
    elif name == "ProtobufBase":
        try:
            module = importlib.import_module(".protobuf_base", "tomodachi.envelope")
        except Exception:  # pragma: no cover

            class ProtobufBase(object):
                @classmethod
                def validate(cls, **kwargs: Any) -> None:
                    raise Exception("google.protobuf package not installed")

                @classmethod
                async def build_message(cls, service: Any, topic: str, data: Any, **kwargs: Any) -> str:
                    raise Exception("google.protobuf package not installed")

                @classmethod
                async def parse_message(
                    cls, payload: str, proto_class: Any = None, validator: Any = None, **kwargs: Any
                ) -> Union[Dict, Tuple]:
                    raise Exception("google.protobuf package not installed")

            __cached_defs[name] = ProtobufBase
            return __cached_defs[name]
    elif name == "json_base":
        __cached_defs[name] = module = importlib.import_module(".json_base", "tomodachi.envelope")
        return __cached_defs[name]
    elif name == "protobuf_base":
        __cached_defs[name] = module = importlib.import_module(".protobuf_base", "tomodachi.envelope")
        return __cached_defs[name]
    else:
        raise AttributeError("module 'tomodachi.envelope' has no attribute '{}'".format(name))

    __cached_defs[name] = getattr(module, name)
    return __cached_defs[name]


__all__ = ["JsonBase", "ProtobufBase", "json_base", "protobuf_base"]

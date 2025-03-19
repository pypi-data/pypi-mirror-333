import functools
import types
from typing import Any, Callable, Dict, Optional, Tuple, cast

from tomodachi.options import Options

FUNCTION_ATTRIBUTE = "_tomodachi_function_is_invoker_function"
START_ATTRIBUTE = "_tomodachi_deprecated_invoker_function_start_marker"
INVOKER_TASK_START_KEYWORD = "_tomodachi_invoker_task_start_keyword"


class Invoker(object):
    context: Dict = {}

    @classmethod
    def decorator(cls, cls_func: Callable) -> Callable:
        def _wrapper(*args: Any, **kwargs: Any) -> Callable:
            def wrapper(func: Callable) -> Callable:
                fn: Optional[Callable] = func
                unwrapped_func = func
                while fn:
                    unwrapped_func = fn
                    if getattr(fn, "__wrapped__", None) and not getattr(fn, FUNCTION_ATTRIBUTE, None):
                        break
                    fn = getattr(fn, "__wrapped__", None)

                @functools.wraps(unwrapped_func)
                async def _decorator(obj: Any, *a: Any, **kw: Any) -> Any:
                    if not kw or not kw.get(INVOKER_TASK_START_KEYWORD):
                        return await unwrapped_func(obj, *a, **kw)

                    setattr(_decorator, START_ATTRIBUTE, False)  # deprecated
                    if not cls.context.get(obj, None):
                        if getattr(obj, "context", None):
                            cls.context[obj] = obj.context
                        else:
                            cls.context[obj] = {}
                        cls.context[obj].update(
                            {
                                i: getattr(obj, i)
                                for i in dir(obj)
                                if not callable(i)
                                and not i.startswith("__")
                                and not isinstance(getattr(obj, i), types.MethodType)
                            }
                        )
                    context = cls.context[obj]
                    obj.context = context
                    bound_cls_func = getattr(cls_func, "__get__")(cls)
                    start_func = await bound_cls_func(obj, context, unwrapped_func, *args, **kwargs)

                    # Work-around if the decorators are stacked with multiple decorators for the same method
                    if getattr(func, FUNCTION_ATTRIBUTE, None):
                        decorated_func = cast(Callable, getattr(func, "func"))
                        decorated_cls_func = cast(Callable, getattr(func, "cls_func"))
                        decorated_args = cast(Tuple, getattr(func, "args"))
                        decorated_kwargs = cast(Dict, getattr(func, "kwargs"))

                        fn = cast(
                            Callable,
                            cls.decorator(decorated_cls_func)(*decorated_args, **decorated_kwargs)(decorated_func),
                        )
                        setattr(fn, START_ATTRIBUTE, True)
                        await fn(obj, *a, **kw)

                    return start_func

                # Work-around if the decorators are stacked with multiple decorators for the same method
                if not getattr(_decorator, FUNCTION_ATTRIBUTE, None):
                    setattr(_decorator, "func", func)
                    setattr(_decorator, "cls_func", cls_func)
                    setattr(_decorator, "args", args)
                    setattr(_decorator, "kwargs", kwargs)

                    setattr(_decorator, FUNCTION_ATTRIBUTE, True)

                return _decorator

            if not kwargs and len(args) == 1 and callable(args[0]):
                func = args[0]
                args = ()
                return wrapper(func)
            else:
                return wrapper

        return _wrapper

    @staticmethod
    def options(context: Dict) -> Options:
        return cast(
            Options,
            (
                context.get("options")
                if isinstance(context.get("options"), Options)
                else Options(**context.get("options", {}))
            ),
        )

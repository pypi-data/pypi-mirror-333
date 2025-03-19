import asyncio
import datetime
import functools
import inspect
import random
import time
from typing import Any, Callable, Dict, List, Optional, Tuple, Union, cast

import pytz
import tzlocal

from tomodachi import get_contextvar, logging
from tomodachi._exception import limit_exception_traceback
from tomodachi.helpers.crontab import get_next_datetime
from tomodachi.helpers.execution_context import (
    decrease_execution_context_value,
    increase_execution_context_value,
    set_execution_context,
)
from tomodachi.helpers.middleware import execute_middlewares
from tomodachi.invoker import Invoker


class Scheduler(Invoker):
    close_waiter: Optional[asyncio.Future] = None

    @classmethod
    async def schedule_handler(
        cls,
        obj: Any,
        context: Dict,
        func: Any,
        interval: Optional[Union[str, int]] = None,
        timestamp: Optional[str] = None,
        timezone: Optional[str] = None,
        immediately: Optional[bool] = False,
    ) -> Any:
        values = inspect.getfullargspec(func)
        original_kwargs = (
            {k: values.defaults[i] for i, k in enumerate(values.args[len(values.args) - len(values.defaults) :])}
            if values.defaults
            else {}
        )
        args_list = values.args[1 : len(values.args) - len(values.defaults or ())]
        args_set = (set(values.args[1:]) | set(values.kwonlyargs)) - set(["self"])

        async def handler(invocation_time: str) -> None:
            logger = logging.getLogger("tomodachi.schedule.handler").bind(
                handler=func.__name__, type="tomodachi.schedule"
            )
            get_contextvar("service.logger").set("tomodachi.schedule.handler")

            increase_execution_context_value("scheduled_functions_current_tasks")
            try:
                kwargs = dict(original_kwargs)
                arg_matches: Dict[str, Any] = {}

                if "invocation_time" in args_set:
                    kwargs["invocation_time"] = invocation_time
                if "interval" in args_set:
                    kwargs["interval"] = interval

                increase_execution_context_value("scheduled_functions_total_tasks")

                middlewares = context.get("_schedule_pre_middleware", [])

                if middlewares:

                    @functools.wraps(func)
                    async def routine_func(*a: Any, **kw: Any) -> None:
                        logging.bind_logger(logger)
                        get_contextvar("service.logger").set("tomodachi.schedule.handler")

                        kw_values = {k: v for k, v in {**kwargs, **kw}.items() if values.varkw or k in args_set}
                        args_values = [
                            kw_values.pop(key) if key in kw_values else a[i + 1]
                            for i, key in enumerate(values.args[1 : len(a) + 1])
                        ]
                        if values.varargs and not values.defaults and len(a) > len(args_values) + 1:
                            args_values += a[len(args_values) + 1 :]

                        routine = func(*(obj, *args_values), **kw_values)
                        if inspect.isawaitable(routine):
                            await routine

                    logging.bind_logger(
                        logging.getLogger("tomodachi.schedule.middleware").bind(
                            middleware=Ellipsis, handler=func.__name__, type="tomodachi.schedule"
                        )
                    )
                    await asyncio.create_task(
                        execute_middlewares(
                            func, routine_func, middlewares, *(obj,), invocation_time=invocation_time, interval=interval
                        )
                    )
                else:
                    logging.bind_logger(logger)
                    get_contextvar("service.logger").set("tomodachi.schedule.handler")

                    a = [arg_matches[k] if k in arg_matches else ()[i] for i, k in enumerate(args_list)]
                    args_values = [kwargs.pop(key) if key in kwargs else a[i] for i, key in enumerate(args_list)]

                    if values.varargs and not values.defaults and len(a) > len(args_values) + 1:
                        args_values += a[len(args_values) + 1 :]

                    routine = func(obj, *args_values, **kwargs)
                    if inspect.isawaitable(routine):
                        await routine

            except (Exception, asyncio.CancelledError) as e:
                limit_exception_traceback(e, ("tomodachi.transport.schedule", "tomodachi.helpers.middleware"))
                logging.getLogger("exception").exception("uncaught exception: {}".format(str(e)))
            except BaseException as e:
                limit_exception_traceback(e, ("tomodachi.transport.schedule",))
                logging.getLogger("exception").exception("uncaught exception: {}".format(str(e)))
            finally:
                decrease_execution_context_value("scheduled_functions_current_tasks")

        context["_schedule_scheduled_functions"] = context.get("_schedule_scheduled_functions", [])
        context["_schedule_scheduled_functions"].append((interval, timestamp, timezone, immediately, func, handler))

        start_func = cls.start_scheduler(obj, context)
        return (await start_func) if start_func else None

    @classmethod
    def schedule_handler_with_interval(cls, interval: Union[str, int]) -> Callable:
        def _func(_: Any, obj: Any, context: Dict, func: Any) -> Any:
            return cls.schedule_handler(obj, context, func, interval=interval)

        return _func

    @staticmethod
    def next_call_at(
        current_time: float,
        interval: Optional[Union[str, int]] = None,
        timestamp: Optional[str] = None,
        timezone: Optional[str] = None,
    ) -> int:
        if not timezone:
            tz = tzlocal.get_localzone()
        else:
            try:
                tz = pytz.timezone(timezone or "")
            except Exception as e:
                raise Exception("Unknown timezone: {}".format(timezone)) from e
        local_tz = tzlocal.get_localzone()

        if interval is None and timestamp is not None:
            if isinstance(timestamp, str):
                try:
                    datetime_object = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                    interval = "{} {} {} {} * {}".format(
                        datetime_object.minute,
                        datetime_object.hour,
                        datetime_object.day,
                        datetime_object.month,
                        datetime_object.year,
                    )
                    second_modifier = 1
                    if datetime_object.replace(tzinfo=tz) > datetime.datetime.fromtimestamp(current_time).replace(
                        tzinfo=local_tz
                    ):
                        second_modifier = -60
                    next_at = get_next_datetime(
                        interval,
                        datetime.datetime.fromtimestamp(current_time + second_modifier)
                        .replace(tzinfo=local_tz)
                        .astimezone(tz),
                    )
                    if not next_at:
                        return int(current_time + 60 * 60 * 24 * 365 * 100)
                    return int(next_at.timestamp() + datetime_object.second)
                except ValueError:
                    pass

                try:
                    datetime_object = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M")
                    interval = "{} {} {} {} * {}".format(
                        datetime_object.minute,
                        datetime_object.hour,
                        datetime_object.day,
                        datetime_object.month,
                        datetime_object.year,
                    )
                    next_at = get_next_datetime(
                        interval,
                        datetime.datetime.fromtimestamp(current_time + 1).replace(tzinfo=local_tz).astimezone(tz),
                    )
                    if not next_at:
                        return int(current_time + 60 * 60 * 24 * 365 * 100)
                    return int(next_at.timestamp())
                except ValueError:
                    pass

                try:
                    datetime_object = datetime.datetime.strptime(timestamp, "%H:%M:%S")
                    datetime_object = datetime.datetime(
                        datetime.datetime.fromtimestamp(current_time).year,
                        datetime.datetime.fromtimestamp(current_time).month,
                        datetime.datetime.fromtimestamp(current_time).day,
                        datetime_object.hour,
                        datetime_object.minute,
                        datetime_object.second,
                    )
                    interval = "{} {} * * *".format(datetime_object.minute, datetime_object.hour)
                    second_modifier = 1

                    if datetime_object.replace(tzinfo=tz) > datetime.datetime.fromtimestamp(current_time).replace(
                        tzinfo=local_tz
                    ):
                        second_modifier = -60
                    next_at = get_next_datetime(
                        interval,
                        datetime.datetime.fromtimestamp(current_time + second_modifier)
                        .replace(tzinfo=local_tz)
                        .astimezone(tz),
                    )
                    if not next_at:
                        return int(current_time + 60 * 60 * 24 * 365 * 100)
                    return int(next_at.timestamp() + datetime_object.second)
                except ValueError:
                    pass

                try:
                    datetime_object = datetime.datetime.strptime(timestamp, "%H:%M")
                    interval = "{} {} * * *".format(datetime_object.minute, datetime_object.hour)
                    next_at = get_next_datetime(
                        interval,
                        datetime.datetime.fromtimestamp(current_time + 1).replace(tzinfo=local_tz).astimezone(tz),
                    )
                    if not next_at:
                        return int(current_time + 60 * 60 * 24 * 365 * 100)
                    return int(next_at.timestamp())
                except ValueError:
                    pass

                raise Exception("Invalid timestamp")

        if interval is not None:
            if isinstance(interval, int):
                return int(current_time + interval)

            interval_aliases: Dict[Tuple[str, ...], Union[str, int]] = {
                ("every second", "1s", "1 s", "1second", "1 second", "second", "secondly", "once per second"): 1,
                (
                    "every minute",
                    "1m",
                    "1 m",
                    "1minute",
                    "1 minute",
                    "minute",
                    "minutely",
                    "once per minute",
                ): "@minutely",
                ("every hour", "1h", "1 h", "1hour", "1 hour", "hour", "hourly", "once per hour"): "@hourly",
                ("every day", "1d", "1 d", "1day", "1 day", "day", "daily", "once per day", "nightly"): "@daily",
                ("every month", "1month", "1 month", "month", "monthly", "once per month"): "@monthly",
                (
                    "every year",
                    "1y",
                    "1 y",
                    "1year",
                    "1 year",
                    "year",
                    "yearly",
                    "once per year",
                    "annually",
                ): "@yearly",
                (
                    "monday",
                    "mondays",
                    "mon",
                    "every monday",
                    "once per monday",
                    "weekly",
                    "once per week",
                    "week",
                    "every week",
                ): "0 0 * * 1",
                ("tuesday", "tuesdays", "tue", "every tuesday", "once per tuesday"): "0 0 * * 2",
                ("wednesday", "wednesdays", "wed", "every wednesday", "once per wednesday"): "0 0 * * 3",
                ("thursday", "thursdays", "thu", "every thursday", "once per thursday"): "0 0 * * 4",
                ("friday", "fridays", "fri", "every friday", "once per friday"): "0 0 * * 5",
                ("saturday", "saturdays", "sat", "every saturday", "once per saturday"): "0 0 * * 6",
                ("sunday", "sundays", "sun", "every sunday", "once per sunday"): "0 0 * * 0",
                ("weekday", "weekdays", "every weekday"): "0 0 * * 1-5",
                ("weekend", "weekends", "every weekend"): "0 0 * * 0,6",
            }
            interval = interval.lower()

            if interval.endswith("s") or interval.endswith("seconds"):
                try:
                    interval = int(interval.replace("seconds", "").replace("s", "").replace(" ", ""))
                except ValueError:
                    pass

            try:
                interval_value: Union[str, int] = [v for k, v in interval_aliases.items() if interval in k][0]
            except IndexError:
                interval_value = interval
            if isinstance(interval_value, int):
                return int(current_time + interval_value)

            try:
                next_at = get_next_datetime(
                    interval_value,
                    datetime.datetime.fromtimestamp(current_time + 1).replace(tzinfo=local_tz).astimezone(tz),
                )
                if not next_at:
                    return int(current_time + 60 * 60 * 24 * 365 * 100)
                return int(next_at.timestamp())
            except Exception:
                raise Exception("Invalid interval")

        return int(current_time + 60 * 60 * 24 * 365 * 100)

    @staticmethod
    def get_timezone(timezone: Optional[str] = None) -> Optional[str]:
        if timezone:
            tz_aliases: Dict[Tuple[str, ...], str] = {
                (
                    "+00:00",
                    "-00:00",
                    "00:00",
                    "0000",
                    "GMT +0000",
                    "GMT +00:00",
                    "GMT -00",
                    "GMT +00",
                    "GMT -0",
                    "GMT +0",
                ): "GMT0",
                ("+01:00", "+0100", "GMT +0100", "GMT +01:00", "GMT +01", "GMT +1"): "Etc/GMT-1",
                ("+02:00", "+0200", "GMT +0200", "GMT +02:00", "GMT +02", "GMT +2"): "Etc/GMT-2",
                ("+03:00", "+0300", "GMT +0300", "GMT +03:00", "GMT +03", "GMT +3"): "Etc/GMT-3",
                ("+04:00", "+0400", "GMT +0400", "GMT +04:00", "GMT +04", "GMT +4"): "Etc/GMT-4",
                ("+05:00", "+0500", "GMT +0500", "GMT +05:00", "GMT +05", "GMT +5"): "Etc/GMT-5",
                ("+06:00", "+0600", "GMT +0600", "GMT +06:00", "GMT +06", "GMT +6"): "Etc/GMT-6",
                ("+07:00", "+0700", "GMT +0700", "GMT +07:00", "GMT +07", "GMT +7"): "Etc/GMT-7",
                ("+08:00", "+0800", "GMT +0800", "GMT +08:00", "GMT +08", "GMT +8"): "Etc/GMT-8",
                ("+09:00", "+0900", "GMT +0900", "GMT +09:00", "GMT +09", "GMT +9"): "Etc/GMT-9",
                ("+10:00", "+1000", "GMT +1000", "GMT +10:00", "GMT +10"): "Etc/GMT-10",
                ("+11:00", "+1100", "GMT +1100", "GMT +11:00", "GMT +11"): "Etc/GMT-11",
                ("+12:00", "+1200", "GMT +1200", "GMT +12:00", "GMT +12"): "Etc/GMT-12",
                ("-01:00", "-0100", "GMT -0100", "GMT -01:00", "GMT -01", "GMT -1"): "Etc/GMT+1",
                ("-02:00", "-0200", "GMT -0200", "GMT -02:00", "GMT -02", "GMT -2"): "Etc/GMT+2",
                ("-03:00", "-0300", "GMT -0300", "GMT -03:00", "GMT -03", "GMT -3"): "Etc/GMT+3",
                ("-04:00", "-0400", "GMT -0400", "GMT -04:00", "GMT -04", "GMT -4"): "Etc/GMT+4",
                ("-05:00", "-0500", "GMT -0500", "GMT -05:00", "GMT -05", "GMT -5"): "Etc/GMT+5",
                ("-06:00", "-0600", "GMT -0600", "GMT -06:00", "GMT -06", "GMT -6"): "Etc/GMT+6",
                ("-07:00", "-0700", "GMT -0700", "GMT -07:00", "GMT -07", "GMT -7"): "Etc/GMT+7",
                ("-08:00", "-0800", "GMT -0800", "GMT -08:00", "GMT -08", "GMT -8"): "Etc/GMT+8",
                ("-09:00", "-0900", "GMT -0900", "GMT -09:00", "GMT -09", "GMT -9"): "Etc/GMT+9",
                ("-10:00", "-1000", "GMT -1000", "GMT -10:00", "GMT -10"): "Etc/GMT+10",
                ("-11:00", "-1100", "GMT -1100", "GMT -11:00", "GMT -11"): "Etc/GMT+11",
                ("-12:00", "-1200", "GMT -1200", "GMT -12:00", "GMT -12"): "Etc/GMT+12",
            }
            try:
                try:
                    timezone = [
                        v
                        for k, v in tz_aliases.items()
                        if timezone in k or timezone.replace(" ", "") in [x.replace(" ", "") for x in k]
                    ][0]
                except IndexError:
                    pass
                pytz.timezone(timezone or "")
            except Exception as e:
                raise Exception("Unknown timezone: {}".format(timezone)) from e

        return timezone

    @classmethod
    async def start_schedule_loop(
        cls,
        obj: Any,
        context: Dict,
        handler: Callable,
        func: Callable,
        interval: Optional[Union[str, int]] = None,
        timestamp: Optional[str] = None,
        timezone: Optional[str] = None,
        immediately: Optional[bool] = False,
    ) -> None:
        logger = logging.getLogger("tomodachi.scheduler").bind(handler=func.__name__)
        logging.bind_logger(logger)

        timezone = cls.get_timezone(timezone)

        if not cls.close_waiter:
            cls.close_waiter = asyncio.Future()
        stop_waiter: asyncio.Future = asyncio.Future()
        start_waiter: asyncio.Future = asyncio.Future()

        async def schedule_loop() -> None:
            sleep_task: asyncio.Future
            current_time = time.time()
            max_sleep_time = 300

            try:
                sleep_task = asyncio.ensure_future(asyncio.sleep(10))
                await asyncio.wait([sleep_task, start_waiter], return_when=asyncio.FIRST_COMPLETED)
                if not sleep_task.done():
                    sleep_task.cancel()
                else:
                    logger.warning(
                        "scheduled function loop cannot start yet - start waiter not done for 10 seconds",
                    )
                    sleep_task = asyncio.ensure_future(asyncio.sleep(110))
                    await asyncio.wait([sleep_task, start_waiter], return_when=asyncio.FIRST_COMPLETED)
                    if not sleep_task.done():
                        sleep_task.cancel()
                    else:
                        logger.warning(
                            "scheduled function loop cannot start yet - start waiter not done for 120 seconds",
                        )
                        try:
                            raise Exception("scheduled function loop not started for 120 seconds")
                        except Exception as e:
                            logging.getLogger("exception").exception(str(e))

                await asyncio.sleep(0.001)
                await start_waiter

                if not cls.close_waiter or cls.close_waiter.done():
                    logger.warning(
                        "scheduled function loop never started before service termination",
                    )
                else:
                    ts0 = cls.next_call_at(current_time, interval, timestamp, timezone)
                    for _ in range(10):
                        ts1 = cls.next_call_at(ts0, interval, timestamp, timezone)
                        ts2 = cls.next_call_at(ts1, interval, timestamp, timezone)
                        if int(ts2 - ts1) // 2 < max_sleep_time:
                            max_sleep_time = int(ts2 - ts1) // 2
                    max_sleep_time = min(max(max_sleep_time, 10), 300)
            except (Exception, asyncio.CancelledError) as e:
                logging.getLogger("exception").exception("uncaught exception: {}".format(str(e)))

                await asyncio.sleep(0.001)
                await start_waiter

                if not cls.close_waiter or cls.close_waiter.done():
                    logger.warning(
                        "scheduled function loop never started before service termination",
                    )

            next_call_at: Optional[int] = None
            prev_call_at: Optional[int] = None
            tasks: List = []
            too_many_tasks = False
            threshold = 20
            run_immediately = immediately

            while cls.close_waiter and not cls.close_waiter.done():
                try:
                    if not run_immediately:
                        last_time = current_time
                        actual_time = time.time()
                        current_time = last_time + 1 if int(last_time + 1) < int(actual_time) else actual_time

                        if next_call_at is None:
                            next_call_at = cls.next_call_at(current_time, interval, timestamp, timezone)
                            if prev_call_at and prev_call_at == next_call_at:
                                if int(last_time + 60) < int(actual_time):
                                    logger.warning(
                                        "scheduled function loop has lost time sync and may not run",
                                    )
                                    try:
                                        raise Exception("scheduled function loop has lost time sync and may not run")
                                    except Exception as e:
                                        logging.getLogger("exception").exception(str(e))

                                next_call_at = None
                                await asyncio.sleep(1)
                                continue
                        sleep_diff = int(current_time + 1) - actual_time + 0.001
                        if next_call_at > time.time() + 8:
                            sleep_diff = int((next_call_at - time.time()) / 3)
                        if sleep_diff >= max_sleep_time:
                            sleep_diff = int(max_sleep_time - random.random() * 5)
                        if sleep_diff >= 2:
                            sleep_task = asyncio.ensure_future(asyncio.sleep(sleep_diff))
                            await asyncio.wait([sleep_task, cls.close_waiter], return_when=asyncio.FIRST_COMPLETED)
                            if not sleep_task.done():
                                sleep_task.cancel()
                            current_time = time.time()
                        else:
                            await asyncio.sleep(sleep_diff)
                        if next_call_at > time.time():
                            continue
                    run_immediately = False
                    if cls.close_waiter.done():
                        continue
                    prev_call_at = next_call_at
                    next_call_at = None

                    tasks = [task for task in tasks if not task.done()]

                    if len(tasks) >= 20:
                        if not too_many_tasks and len(tasks) >= threshold:
                            too_many_tasks = True
                            logger.warning(
                                "too many scheduled tasks for function in scheduled function loop",
                                task_count=len(tasks),
                                task_limit=threshold,
                            )
                            threshold = threshold * 2
                        await asyncio.sleep(1)
                        current_time = time.time()
                        next_call_at = cls.next_call_at(current_time + 10, interval, timestamp, timezone)
                        continue
                    if too_many_tasks and len(tasks) >= 15:
                        await asyncio.sleep(1)
                        current_time = time.time()
                        next_call_at = cls.next_call_at(current_time + 10, interval, timestamp, timezone)
                        continue
                    if too_many_tasks and len(tasks) < 15:
                        threshold = 20
                        logger.info(
                            "scheduled function loop resumed as task count is within threshold",
                            task_count=len(tasks),
                            task_limit=threshold,
                        )

                    too_many_tasks = False

                    current_time = time.time()
                    invocation_time = (
                        datetime.datetime.fromtimestamp(int(prev_call_at or current_time), tz=datetime.timezone.utc)
                        .isoformat()
                        .replace("+00:00", "Z")
                    )

                    task = asyncio.ensure_future(handler(invocation_time=invocation_time))
                    if hasattr(task, "set_name"):
                        getattr(task, "set_name")(
                            "{}/{}".format(
                                func.__qualname__,
                                datetime.datetime.fromtimestamp(current_time, tz=datetime.timezone.utc)
                                .isoformat(timespec="microseconds")
                                .replace("+00:00", "Z"),
                            )
                        )
                    tasks.append(task)
                except (Exception, asyncio.CancelledError) as e:
                    logging.getLogger("exception").exception("uncaught exception: {}".format(str(e)))
                    await asyncio.sleep(1)
                except BaseException as e:
                    logging.getLogger("exception").exception("uncaught exception: {}".format(str(e)))
                    await asyncio.sleep(1)

            if tasks:
                task_waiter = asyncio.ensure_future(asyncio.wait(tasks))
                sleep_task = asyncio.ensure_future(asyncio.sleep(2))
                await asyncio.wait([sleep_task, task_waiter], return_when=asyncio.FIRST_COMPLETED)
                if not sleep_task.done():
                    sleep_task.cancel()
                for task in tasks:
                    if task.done():
                        continue
                    task_name = getattr(task, "get_name")() if hasattr(task, "get_name") else func.__name__
                    logger.warning(
                        "awaiting task to complete",
                        task_name=task_name,
                    )

                while not task_waiter.done():
                    sleep_task = asyncio.ensure_future(asyncio.sleep(10))
                    await asyncio.wait([sleep_task, task_waiter], return_when=asyncio.FIRST_COMPLETED)
                    if not sleep_task.done():
                        sleep_task.cancel()
                    for task in tasks:
                        if task.done():
                            continue
                        task_name = getattr(task, "get_name")() if hasattr(task, "get_name") else func.__name__
                        logger.warning(
                            "still awaiting task to finish",
                            task_name=task_name,
                        )

            if not stop_waiter.done():
                stop_waiter.set_result(None)

        stop_method = getattr(obj, "_stop_service", None)

        async def stop_service(*args: Any, **kwargs: Any) -> None:
            if cls.close_waiter and not cls.close_waiter.done():
                cls.close_waiter.set_result(None)

                if not start_waiter.done():
                    start_waiter.set_result(None)

                await stop_waiter
                if stop_method:
                    await stop_method(*args, **kwargs)
            else:
                if not start_waiter.done():
                    start_waiter.set_result(None)

                await stop_waiter
                if stop_method:
                    await stop_method(*args, **kwargs)

        setattr(obj, "_stop_service", stop_service)

        started_method = getattr(obj, "_started_service", None)

        async def started_service(*args: Any, **kwargs: Any) -> None:
            if started_method:
                await started_method(*args, **kwargs)
            if not start_waiter.done():
                start_waiter.set_result(None)

        setattr(obj, "_started_service", started_service)

        asyncio.create_task(schedule_loop())

    @classmethod
    async def start_scheduler(cls, obj: Any, context: Dict) -> Optional[Callable]:
        if context.get("_schedule_loop_started"):
            return None
        context["_schedule_loop_started"] = True

        set_execution_context(
            {
                "scheduled_functions_enabled": True,
                "scheduled_functions_current_tasks": 0,
                "scheduled_functions_total_tasks": 0,
            }
        )

        async def _schedule() -> None:
            cls.close_waiter = asyncio.Future()

            for interval, timestamp, timezone, immediately, func, handler in context.get(
                "_schedule_scheduled_functions", []
            ):
                cls.next_call_at(
                    time.time(), interval, timestamp, cls.get_timezone(timezone)
                )  # test provided interval/timestamp on init

            for interval, timestamp, timezone, immediately, func, handler in context.get(
                "_schedule_scheduled_functions", []
            ):
                await asyncio.create_task(
                    cls.start_schedule_loop(obj, context, handler, func, interval, timestamp, timezone, immediately)
                )

        return _schedule


__schedule = Scheduler.decorator(Scheduler.schedule_handler)
__scheduler = Scheduler.decorator(Scheduler.schedule_handler)

__heartbeat = Scheduler.decorator(Scheduler.schedule_handler_with_interval(1))
__every_second = Scheduler.decorator(Scheduler.schedule_handler_with_interval(1))

__minutely = Scheduler.decorator(Scheduler.schedule_handler_with_interval("minutely"))
__hourly = Scheduler.decorator(Scheduler.schedule_handler_with_interval("hourly"))
__daily = Scheduler.decorator(Scheduler.schedule_handler_with_interval("daily"))
__monthly = Scheduler.decorator(Scheduler.schedule_handler_with_interval("monthly"))


def schedule(
    interval: Optional[Union[str, int]] = None,
    timestamp: Optional[str] = None,
    timezone: Optional[str] = None,
    immediately: Optional[bool] = False,
) -> Callable:
    return cast(
        Callable, __schedule(interval=interval, timestamp=timestamp, timezone=timezone, immediately=immediately)
    )


def scheduler(
    interval: Optional[Union[str, int]] = None,
    timestamp: Optional[str] = None,
    timezone: Optional[str] = None,
    immediately: Optional[bool] = False,
) -> Callable:
    return cast(
        Callable, __scheduler(interval=interval, timestamp=timestamp, timezone=timezone, immediately=immediately)
    )


def heartbeat(func: Optional[Callable] = None) -> Callable:
    return cast(Callable, __heartbeat(func))


def every_second(func: Optional[Callable] = None) -> Callable:
    return cast(Callable, __every_second(func))


def minutely(func: Optional[Callable] = None) -> Callable:
    return cast(Callable, __minutely(func))


def hourly(func: Optional[Callable] = None) -> Callable:
    return cast(Callable, __hourly(func))


def daily(func: Optional[Callable] = None) -> Callable:
    return cast(Callable, __daily(func))


def monthly(func: Optional[Callable] = None) -> Callable:
    return cast(Callable, __monthly(func))

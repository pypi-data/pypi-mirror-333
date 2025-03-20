from opentelemetry.metrics import (get_meter,
                                   Meter)
from typing import Union
from typing import Iterable
from opentelemetry.metrics import (
    CallbackOptions,
    Observation
)
from opentelemetry.util.types import Attributes
from threading import Lock
from aliyun.semconv.version import __version__


class SingletonMeta(type):
    """
    This is a thread-safe implementation of Singleton.
    """

    _instances = {}

    _lock: Lock = Lock()
    """
    We now have a lock object that will be used to synchronize threads during
    first access to the Singleton.
    """

    @classmethod
    def reset(cls):
        with cls._lock:
            cls._instances.clear()

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        # Now, imagine that the program has just been launched. Since there's no
        # Singleton instance yet, multiple threads can simultaneously pass the
        # previous conditional and reach this point almost at the same time. The
        # first of them will acquire lock and will proceed further, while the
        # rest will wait here.
        with cls._lock:
            # The first thread to acquire the lock, reaches this conditional,
            # goes inside and creates the Singleton instance. Once it leaves the
            # lock block, a thread that might have been waiting for the lock
            # release may then enter this section. But since the Singleton field
            # is already initialized, the thread won't create a new object.
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class MetricUnit:
    COUNT = "count"

    MS = "ms"

    S = "s"

    BYTE = "b"


class MetricInstruments:
    """
    app metrics
    """
    ARMS_LLM_CALLS = "arms_llm_calls"

    ARMS_LLM_USAGE_TOKENS = "arms_llm_usage_tokens"


class ArmsLLMMetrics(metaclass=SingletonMeta):
    __slots__ = ("llm_calls",
                 "llm_usage_tokens",
                 )

    def __init__(self, meter: Meter):
        self.llm_calls = meter.create_counter(
            name=MetricInstruments.ARMS_LLM_CALLS,
            unit=MetricUnit.COUNT,
            description="The total number of llm calls")

        self.llm_calls = meter.create_counter(
            name=MetricInstruments.ARMS_LLM_CALLS,
            unit=MetricUnit.COUNT,
            description="The total number of llm call")

        self.llm_usage_tokens = meter.create_counter(
            name=MetricInstruments.ARMS_LLM_USAGE_TOKENS,
            unit=MetricUnit.COUNT,
            description="The user llm usage tokens count")



_meter = get_meter(
            __name__,
            __version__,
            meter_provider=None,
            schema_url="https://opentelemetry.io/schemas/1.11.0",
        )
arms_llm_metrics = ArmsLLMMetrics(meter=_meter)

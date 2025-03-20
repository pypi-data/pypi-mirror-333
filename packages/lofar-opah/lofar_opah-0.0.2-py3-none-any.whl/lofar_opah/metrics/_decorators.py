"""Util class for exception handling"""

# Copyright (C) 2025 ASTRON (Netherlands Institute for Radio Astronomy)
# SPDX-License-Identifier: Apache-2.0

import logging
from functools import wraps

from prometheus_client import Counter

from ._metrics import AttributeMetric

logger = logging.getLogger()


def exception_to_str(ex: Exception) -> str:
    """Convert an exception into a human-readable string."""

    return f"{ex.__class__.__name__}: {': '.join(str(arg) for arg in ex.args)}"


def call_exception_metrics(
    service_name: str, static_labels: dict[str, str] | None = None
):
    """Decorator that provides gRPC function boiler plate:

    - Call and exception counts are maintained, if provided,
    - Calls and exceptions are logged,
    """

    def wrapper(func):
        labels = {"service": service_name}
        labels.update(static_labels or {})

        call_count_metric = AttributeMetric(
            f"{func.__name__}_calls",
            f"Call statistics for {func.__qualname__}",
            labels,
            metric_class=Counter,
        )
        exception_count_metric = AttributeMetric(
            f"{func.__name__}_exceptions",
            f"Number of exceptions thrown by {func.__qualname__}",
            labels,
            metric_class=Counter,
        )

        @wraps(func)
        def inner(*args, **kwargs):
            try:
                logger.info("gRPC function called: %s", func.__name__)

                call_count_metric.get_metric().inc()

                return func(*args, **kwargs)
            except Exception as e:
                exception_count_metric.get_metric().inc()

                logger.exception(
                    "gRPC function failed: %s raised %s: %s",
                    func.__name__,
                    e.__class__.__name__,
                    e,
                )

                raise

        return inner

    return wrapper

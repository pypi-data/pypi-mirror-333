"""Metric service"""

#  Copyright (C) 2025 ASTRON (Netherlands Institute for Radio Astronomy)
#  SPDX-License-Identifier: Apache-2.0
from prometheus_client import start_http_server, disable_created_metrics
from ._metrics import AttributeMetric
from ._decorators import call_exception_metrics

__all__ = [
    "start_metrics_server",
    "AttributeMetric",
    "call_exception_metrics",
]


def start_metrics_server(port: int = 8000):
    """Start the metrics servers, defaults to port 8000"""
    # configure
    disable_created_metrics()

    # start server
    start_http_server(port)

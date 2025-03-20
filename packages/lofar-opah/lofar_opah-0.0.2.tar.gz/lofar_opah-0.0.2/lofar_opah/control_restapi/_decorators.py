# Copyright (C) 2025 ASTRON (Netherlands Institute for Radio Astronomy)
# SPDX-License-Identifier: Apache-2.0
from functools import wraps
from flask import jsonify
from grpc import RpcError
import logging

logger = logging.getLogger()


def grpc_error_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except RpcError as e:
            logger.error(f"gRPC error: {e.details()}")
            return (
                jsonify(
                    {
                        "error": "gRPC service unavailable",
                        "exception": e.details(),
                        "success": False,
                    }
                ),
                503,
            )

    return wrapper

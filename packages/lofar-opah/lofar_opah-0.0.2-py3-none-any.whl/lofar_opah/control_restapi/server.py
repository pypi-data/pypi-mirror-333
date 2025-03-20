# Copyright (C) 2025 ASTRON (Netherlands Institute for Radio Astronomy)
# SPDX-License-Identifier: Apache-2.0
"""Main class for the  API Server"""

import logging
import argparse
from rest_server import start_rest_server
from lofar_opah.metrics import start_metrics_server
import sys

logger = logging.getLogger()
REST_PORT = 50052
STATION_SUFFIX = ".control.lofar"  # This is added to the stationname

logging.basicConfig(level=logging.DEBUG)


def _create_parser():
    """Define the parser"""
    parser = argparse.ArgumentParser(description="Serve the station rest interface.")
    parser.add_argument(
        "--port",
        default=50053,
        help="HTTP port to listen on. Defaults to 50053",
    )
    parser.add_argument(
        "--metrics-port",
        default=8002,
        help="Prometheus metrics HTTP port. Defaults to 8002",
    )
    parser.add_argument(
        "--stationsuffix",
        default=".control.lofar",
        help=(
            "Append this to all station_name e.g. .control.lofar."
            "Leave empty for rest on localserver. Defaults to .control.lofar"
        ),
    )
    parser.add_argument(
        "--remotegrpcport",
        default="50051",
        help="The port the remotegrpc service is listening on. defaults to 50051",
    )
    return parser


def main(argv=None):
    parser = _create_parser()
    args = parser.parse_args(argv or sys.argv[1:])
    start_metrics_server(args.metrics_port)

    logging.info(
        "Launching Control Rest Server port:%s, stationsuffix:%s,remotegrpcport:%s",
        args.port,
        args.stationsuffix,
        args.remotegrpcport,
    )
    # Create gRPC server
    start_rest_server(logger, args.port, args.stationsuffix, args.remotegrpcport)


if __name__ == "__main__":
    main()

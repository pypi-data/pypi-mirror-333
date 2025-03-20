# Copyright (C) 2025 ASTRON (Netherlands Institute for Radio Astronomy)
# SPDX-License-Identifier: Apache-2.0
from flask import Flask, jsonify, request, redirect, url_for
from flask_cors import CORS
from flasgger import Swagger
from waitress import serve
import grpc
from lofar_sid.interface.stationcontrol import antennafield_pb2, antennafield_pb2_grpc

from lofar_opah.control_restapi._decorators import grpc_error_handler
from http import HTTPStatus


app = Flask(__name__)


def get_grpc_stub(logger, station_name, station_suffix, remote_grpc_port):
    """Create a grpc Stub to the station"""
    grpc_endpoint = f"{station_name}{station_suffix}:{remote_grpc_port}"
    logger.debug("REST API Will Remotely connect to  %s", grpc_endpoint)
    channel = grpc.insecure_channel(grpc_endpoint)
    return antennafield_pb2_grpc.AntennafieldStub(channel)


def start_rest_server(logger, rest_port, station_suffix, remote_grpc_port):
    """Starts a REST API server that acts as a proxy to gRPC."""
    logger.debug(
        'start_rest_server(rest_port:%s, station_suffix:"%s",remotegrpcport:%s) ',
        rest_port,
        station_suffix,
        remote_grpc_port,
    )

    CORS(app)
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "The Lofar Control API",
            "description": "API for controlling Lofar Antennas",
        },
        "basePath": "/v1",
    }
    Swagger(app, template=swagger_template)

    @app.after_request
    def log_failed_requests(response):
        """Log requests that resulted in client or server errors."""
        logmessage = f"Method: {request.method} | Path: {request.path}"
        f" | Status: {response.status_code} "
        f" | IP: {request.remote_addr} | User-Agent: {request.user_agent}"

        if response.status_code >= 400:
            logger.error(logmessage)
        else:
            logger.debug(logmessage)
        return response

    def cast_antennareply_to_json(response):
        """Clear Cast, gets rid of additional grpc fields"""

        return jsonify(
            {
                "success": response.success,
                "exception": response.exception,
                "result": {
                    "antenna_use": response.result.antenna_use,
                    "antenna_status": response.result.antenna_status,
                },
                "identifier": {
                    "antennafield_name": response.result.identifier.antennafield_name,
                    "antenna_name": response.result.identifier.antenna_name,
                },
            }
        )

    @app.route("/")
    def redirect_to_apidocs():
        return redirect(url_for("flasgger.apidocs"))

    @app.route(
        "/v1/<station_name>/antenna/<antennafield_name>/<antenna_name>", methods=["GET"]
    )
    @grpc_error_handler
    def get_antenna(station_name, antennafield_name, antenna_name):
        """Get Antenna Information
        ---
        parameters:
          - name: station_name
            description : Use localhost for localstation
            in: path
            type: string
            required: true
          - name: antennafield_name
            in: path
            type: string
            required: true
          - name: antenna_name
            in: path
            type: string
            required: true
        responses:
          200:
            description: Antenna information retrieved successfully
        """
        antenna_request = antennafield_pb2.GetAntennaRequest(
            identifier=antennafield_pb2.Identifier(
                antennafield_name=antennafield_name,
                antenna_name=antenna_name,
            )
        )

        stub = get_grpc_stub(logger, station_name, station_suffix, remote_grpc_port)
        response = stub.GetAntenna(antenna_request)
        return cast_antennareply_to_json(response), (
            HTTPStatus.OK if response.success else HTTPStatus.BAD_GATEWAY
        )

    @app.route(
        "/v1/<station_name>/antenna/"
        "<antennafield_name>/<antenna_name>"
        "/status/<int:status>",
        methods=["POST"],
    )
    @grpc_error_handler
    def set_antenna_status(station_name, antennafield_name, antenna_name, status):
        """Set Antenna Status
        ---
        parameters:
          - name: station_name
            description : Use localhost for localstation
            in: path
            type: string
            required: true
          - name: antennafield_name
            in: path
            type: string
            required: true
          - name: antenna_name
            in: path
            type: string
            required: true
          - name: status
            in: path
            type: integer
            required: true
        responses:
          200:
            description: Antenna status updated
        """
        set_antenna_status_request = antennafield_pb2.SetAntennaStatusRequest(
            identifier=antennafield_pb2.Identifier(
                antennafield_name=antennafield_name,
                antenna_name=antenna_name,
            ),
            antenna_status=status,
        )
        stub = get_grpc_stub(logger, station_name, station_suffix, remote_grpc_port)
        response = stub.SetAntennaStatus(set_antenna_status_request)
        return cast_antennareply_to_json(response), (
            HTTPStatus.OK if response.success else HTTPStatus.BAD_GATEWAY
        )

    @app.route(
        "/v1/<station_name>/antenna/<antennafield_name>/<antenna_name>/use/<int:use>",
        methods=["POST"],
    )
    @grpc_error_handler
    def set_antenna_use(station_name, antennafield_name, antenna_name, use):
        """Set Antenna Use
        ---
        parameters:
          - name: station_name
            in: path
            type: string
            required: true
          - name: antennafield_name
            in: path
            type: string
            required: true
          - name: antenna_name
            in: path
            type: string
            required: true
          - name: use
            in: path
            type: integer
            required: true
        responses:
          200:
            description: Antenna use updated
        """
        set_antenna_use_request = antennafield_pb2.SetAntennaUseRequest(
            identifier=antennafield_pb2.Identifier(
                antennafield_name=antennafield_name,
                antenna_name=antenna_name,
            ),
            antenna_use=use,
        )
        stub = get_grpc_stub(logger, station_name, station_suffix, remote_grpc_port)
        response = stub.SetAntennaUse(set_antenna_use_request)
        return cast_antennareply_to_json(response), (
            HTTPStatus.OK if response.success else HTTPStatus.BAD_GATEWAY
        )

    logger.info("Control REST API server started on port %s", rest_port)
    serve(app, host="0.0.0.0", port=rest_port)

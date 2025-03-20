# Copyright (C) 2025 ASTRON (Netherlands Institute for Radio Astronomy)
# SPDX-License-Identifier: Apache-2.0

"""Exposure of the station's statistics
for the innius-rpc-datasource plugin in Grafana."""

from datetime import datetime, timezone
import itertools
import math

import grpc

from lofar_sid.interface.opah import grafana_apiv3_pb2
from lofar_sid.interface.opah import grafana_apiv3_pb2_grpc
from lofar_sid.interface.stationcontrol import statistics_pb2
from lofar_sid.interface.stationcontrol import statistics_pb2_grpc
from lofar_opah.metrics import (
    call_exception_metrics,
)


class NotAvailableError(RuntimeError):
    pass


class TooOldError(NotAvailableError):
    pass


class StatisticsToGrafana:
    """Abstract base class for converting Statistics responses to Grafana Frames."""

    # Meta information for our statistics
    meta = grafana_apiv3_pb2.FrameMeta(
        type=grafana_apiv3_pb2.FrameMeta.FrameType.FrameTypeTimeSeriesLong,
        PreferredVisualization=grafana_apiv3_pb2.FrameMeta.VisType.VisTypeGraph,
    )

    def __init__(self, statistics_api):
        super().__init__()

        self.statistics_api = statistics_api

    @staticmethod
    def verify_call_result(reply, time_window: tuple[datetime, datetime]):
        """Verify reply from Statistics service. Raises if verification fails."""

        if not (
            time_window[0]
            <= reply.result.timestamp.ToDatetime(tzinfo=timezone.utc)
            < time_window[1]
        ):
            raise TooOldError(
                f"Stastistics not available in time window {time_window}."
                f"Available is {reply.result.timestamp}."
            )

        return True


class BstToGrafana(StatisticsToGrafana):
    """Converts Statistics.BST responses to Grafana Frames."""

    def _get_latest_in_window(
        self, time_window: tuple[datetime, datetime], antenna_field: str
    ) -> statistics_pb2.BstReply:
        """Get the latest statistics in the given time window, if any."""

        request = statistics_pb2.BstRequest(
            antenna_field=antenna_field,
        )

        try:
            reply = self.statistics_api.Bst(request, None)
        except grpc.RpcError as ex:
            raise NotAvailableError() from ex

        self.verify_call_result(reply, time_window)

        return reply

    @call_exception_metrics("StatisticsToGrafana", {"type": "bst"})
    def all_frames(
        self,
        time_window: tuple[datetime, datetime],
        antenna_field: str,
        pol: str | None,
    ) -> list[grafana_apiv3_pb2.Frame]:
        """Return all Grafana Frames for the requested data."""

        try:
            reply = self._get_latest_in_window(time_window, antenna_field)
            result = reply.result
        except NotAvailableError:
            return []

        # Turn result into Grafana fields
        #
        # Each value describes the power for one beamlet.
        #
        # Each polarisation results in one field.
        frames = [
            grafana_apiv3_pb2.Frame(
                metric="BST",
                timestamps=[result.timestamp for _ in result.beamlets],
                fields=list(
                    filter(
                        None,
                        [
                            grafana_apiv3_pb2.Field(
                                name="beamlet",
                                values=[b.beamlet for b in result.beamlets],
                            ),
                            (
                                grafana_apiv3_pb2.Field(
                                    name="xx",
                                    config=grafana_apiv3_pb2.config(
                                        unit="dB",
                                    ),
                                    values=[b.x_power_db for b in result.beamlets],
                                )
                                if pol in ["xx", None]
                                else None
                            ),
                            (
                                grafana_apiv3_pb2.Field(
                                    name="yy",
                                    config=grafana_apiv3_pb2.config(
                                        unit="dB",
                                    ),
                                    values=[b.y_power_db for b in result.beamlets],
                                )
                                if pol in ["yy", None]
                                else None
                            ),
                        ],
                    )
                ),
                meta=self.meta,
            )
        ]

        return frames


class SstToGrafana(StatisticsToGrafana):
    """Converts Statistics.SST responses to Grafana Frames."""

    def _get_latest_in_window(
        self, time_window: tuple[datetime, datetime], antenna_field: str
    ) -> statistics_pb2.SstReply:
        """Get the latest statistics in the given time window, if any."""

        request = statistics_pb2.SstRequest(
            antenna_field=antenna_field,
        )

        try:
            reply = self.statistics_api.Sst(request, None)
        except grpc.RpcError as ex:
            raise NotAvailableError() from ex

        self.verify_call_result(reply, time_window)

        return reply

    @call_exception_metrics("StatisticsToGrafana", {"type": "sst"})
    def all_frames(
        self,
        time_window: tuple[datetime, datetime],
        antenna_field: str,
        selected_pol: str | None,
    ) -> list[grafana_apiv3_pb2.Frame]:
        """Return all Grafana Frames for the requested data."""

        try:
            reply = self._get_latest_in_window(time_window, antenna_field)
            result = reply.result
        except NotAvailableError:
            return []

        # Turn result into Grafana fields
        #
        # Each value describes the power of an antenna for a specific subband.
        #
        # Field 0 are the spectral frequencies for each value.
        # Field 1+ is one field for each antenna and each requested polarisation.
        antenna_nrs = [antenna.antenna for antenna in result.subbands[0].antennas]
        fields_per_antenna = [
            [
                (
                    grafana_apiv3_pb2.Field(
                        name="power",
                        labels=[
                            grafana_apiv3_pb2.Label(
                                key="antenna",
                                value="%03d" % antenna_nr,
                            ),
                            grafana_apiv3_pb2.Label(
                                key="pol",
                                value="xx",
                            ),
                        ],
                        config=grafana_apiv3_pb2.config(
                            unit="dB",
                        ),
                        values=[
                            subband.antennas[antenna_nr].x_power_db
                            for subband in result.subbands
                        ],
                    )
                    if selected_pol in ["xx", None]
                    else None
                ),
                (
                    grafana_apiv3_pb2.Field(
                        name="power",
                        labels=[
                            grafana_apiv3_pb2.Label(
                                key="antenna",
                                value="%03d" % antenna_nr,
                            ),
                            grafana_apiv3_pb2.Label(
                                key="pol",
                                value="yy",
                            ),
                        ],
                        config=grafana_apiv3_pb2.config(
                            unit="dB",
                        ),
                        values=[
                            subband.antennas[antenna_nr].y_power_db
                            for subband in result.subbands
                        ],
                    )
                    if selected_pol in ["yy", None]
                    else None
                ),
            ]
            for antenna_nr in antenna_nrs
        ]

        frames = [
            grafana_apiv3_pb2.Frame(
                metric="SST",
                timestamps=[result.timestamp for _ in result.subbands],
                fields=[
                    grafana_apiv3_pb2.Field(
                        name="frequency",
                        config=grafana_apiv3_pb2.config(
                            unit="Hz",
                        ),
                        values=[subband.frequency for subband in result.subbands],
                    ),
                ]
                + list(filter(None, itertools.chain(*fields_per_antenna))),
                meta=self.meta,
            )
        ]

        return frames


class XstToGrafana(StatisticsToGrafana):
    """Converts Statistics.XST responses to Grafana Frames."""

    def _get_latest_in_window(
        self, time_window: tuple[datetime, datetime], antenna_field: str
    ) -> statistics_pb2.XstReply:
        """Get the latest statistics in the given time window, if any."""

        request = statistics_pb2.XstRequest(
            antenna_field=antenna_field,
        )

        try:
            reply = self.statistics_api.Xst(request, None)
        except grpc.RpcError as ex:
            raise NotAvailableError() from ex

        self.verify_call_result(reply, time_window)

        return reply

    @call_exception_metrics("StatisticsToGrafana", {"type": "xst"})
    def all_frames(
        self,
        time_window: tuple[datetime, datetime],
        antenna_field: str,
        selected_pol: str | None,
    ) -> list[grafana_apiv3_pb2.Frame]:
        """Return all Grafana Frames for the requested data."""

        try:
            reply = self._get_latest_in_window(time_window, antenna_field)
            result = reply.result
        except NotAvailableError:
            return []

        # Turn result into Grafana fields
        #
        # Each value describes a baseline.
        #
        # Field 0 & 1 are the (antenna1, antenna2) indices describing each baseline.
        # Field 2 is the central frequency of the values for each baseline.
        fields = [
            grafana_apiv3_pb2.Field(
                name="antenna1",
                values=[baseline.antenna1 for baseline in result.baselines],
            ),
            grafana_apiv3_pb2.Field(
                name="antenna2",
                values=[baseline.antenna2 for baseline in result.baselines],
            ),
            grafana_apiv3_pb2.Field(
                name="frequency",
                config=grafana_apiv3_pb2.config(
                    unit="Hz",
                ),
                values=[result.frequency for _ in result.baselines],
            ),
        ]

        # Subsequent fields describe the power and phase for each baseline, and
        # the requested, or all, polarisations.
        for pol in ("xx", "xy", "yx", "yy"):
            if selected_pol is None or pol == selected_pol:
                labels = (
                    [
                        grafana_apiv3_pb2.Label(
                            key="pol",
                            value=pol,
                        )
                    ]
                    if not selected_pol
                    else []
                )

                fields.extend(
                    [
                        grafana_apiv3_pb2.Field(
                            name="power",
                            labels=labels,
                            config=grafana_apiv3_pb2.config(
                                unit="dB",
                            ),
                            values=[
                                getattr(baseline, pol).power_db
                                for baseline in result.baselines
                            ],
                        ),
                        grafana_apiv3_pb2.Field(
                            name="phase",
                            labels=labels,
                            config=grafana_apiv3_pb2.config(
                                unit="deg",
                            ),
                            values=[
                                math.fabs(
                                    getattr(baseline, pol).phase * 360.0 / math.pi
                                )
                                for baseline in result.baselines
                            ],
                        ),
                    ]
                )

        frames = [
            grafana_apiv3_pb2.Frame(
                metric="XST",
                timestamps=[result.timestamp for _ in result.baselines],
                fields=fields,
                meta=self.meta,
            )
        ]

        return frames


class GrafanaAPIV3(grafana_apiv3_pb2_grpc.GrafanaQueryAPIServicer):
    """Implements the Grafana interface for the innius simple-rpc-datasource,
    see https://github.com/innius/grafana-simple-grpc-datasource"""

    def __init__(self, stations: list[str]):
        super().__init__()

        self.stations = stations
        self.antenna_fields = ["LBA", "HBA", "HBA0", "HBA1"]

    def GetQueryOptions(self, request: grafana_apiv3_pb2.GetOptionsRequest, context):
        """List options per query."""

        return grafana_apiv3_pb2.GetOptionsResponse(options=[])

    def ListDimensionKeys(
        self, request: grafana_apiv3_pb2.ListDimensionKeysRequest, context
    ):
        """List available data dimensions."""

        results = [
            grafana_apiv3_pb2.ListDimensionKeysResponse.Result(
                key="station",
                description="Station",
            ),
            grafana_apiv3_pb2.ListDimensionKeysResponse.Result(
                key="antenna_field",
                description="Antenna field",
            ),
            grafana_apiv3_pb2.ListDimensionKeysResponse.Result(
                key="pol",
                description="Polarisation",
            ),
        ]
        return grafana_apiv3_pb2.ListDimensionKeysResponse(results=results)

    def ListDimensionValues(
        self, request: grafana_apiv3_pb2.ListDimensionValuesRequest, context
    ):
        """List possible values for each data dimension."""

        results = []

        if request.dimension_key == "station":
            for station in self.stations:
                results.append(
                    grafana_apiv3_pb2.ListDimensionValuesResponse.Result(
                        value=station,
                    )
                )

        if request.dimension_key == "antenna_field":
            for antenna_field in self.antenna_fields:
                results.append(
                    grafana_apiv3_pb2.ListDimensionValuesResponse.Result(
                        value=antenna_field,
                    )
                )

        if request.dimension_key == "pol":
            for pol in ["xx", "xy", "yx", "yy"]:
                results.append(
                    grafana_apiv3_pb2.ListDimensionValuesResponse.Result(
                        value=pol,
                    )
                )

        return grafana_apiv3_pb2.ListDimensionValuesResponse(results=results)

    def ListMetrics(self, request: grafana_apiv3_pb2.ListMetricsRequest, context):
        """List available metrics."""

        metrics = [
            grafana_apiv3_pb2.ListMetricsResponse.Metric(
                name="BST",
                description="Beamlet statistics",
            ),
            grafana_apiv3_pb2.ListMetricsResponse.Metric(
                name="SST",
                description="Subband statistics",
            ),
            grafana_apiv3_pb2.ListMetricsResponse.Metric(
                name="XST",
                description="Crosslet statistics",
            ),
        ]

        return grafana_apiv3_pb2.ListMetricsResponse(Metrics=metrics)

    @call_exception_metrics("GrafanaAPIV3")
    def GetMetricValue(self, request: grafana_apiv3_pb2.GetMetricValueRequest, context):
        return grafana_apiv3_pb2.GetMetricValueResponse(frames=[])

    @staticmethod
    def _station_rpc_address(station_name: str, port: int = 50051) -> str:
        if station_name == "localhost":
            return f"rpc.service.consul:{port}"
        else:
            return f"rpc.service.lofar-{station_name.lower()}.consul:{port}"

    @call_exception_metrics("GrafanaAPIV3")
    def GetMetricAggregate(
        self, request: grafana_apiv3_pb2.GetMetricAggregateRequest, context
    ):
        """Return the set of values for the request metrics and dimensions."""

        frames = []

        dimensions = {d.key: d.value for d in request.dimensions}
        time_window = (
            request.startDate.ToDatetime(tzinfo=timezone.utc),
            request.endDate.ToDatetime(tzinfo=timezone.utc),
        )

        address = self._station_rpc_address(dimensions["station"])

        with grpc.insecure_channel(address) as channel:
            statistics_api = statistics_pb2_grpc.StatisticsStub(channel)

            for metric in request.metrics:
                if metric == "BST":
                    bst = BstToGrafana(statistics_api)

                    frames.extend(
                        bst.all_frames(
                            time_window,
                            dimensions["antenna_field"].lower(),
                            dimensions.get("pol"),
                        )
                    )
                elif metric == "SST":
                    sst = SstToGrafana(statistics_api)

                    frames.extend(
                        sst.all_frames(
                            time_window,
                            dimensions["antenna_field"].lower(),
                            dimensions.get("pol"),
                        )
                    )
                elif metric == "XST":
                    xst = XstToGrafana(statistics_api)

                    frames.extend(
                        xst.all_frames(
                            time_window,
                            dimensions["antenna_field"].lower(),
                            dimensions.get("pol"),
                        )
                    )

        return grafana_apiv3_pb2.GetMetricAggregateResponse(frames=frames)

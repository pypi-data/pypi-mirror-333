# Copyright The OpenTelemetry Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# pylint: disable=unused-import

from abc import ABC, abstractmethod
from threading import Lock
from typing import Iterable, List, Mapping

# This kind of import is needed to avoid Sphinx errors.
import opensafely._vendor.opentelemetry.sdk.metrics
import opensafely._vendor.opentelemetry.sdk.metrics._internal.instrument
import opensafely._vendor.opentelemetry.sdk.metrics._internal.sdk_configuration
from opensafely._vendor.opentelemetry.metrics._internal.instrument import CallbackOptions
from opensafely._vendor.opentelemetry.sdk.metrics._internal.exceptions import MetricsTimeoutError
from opensafely._vendor.opentelemetry.sdk.metrics._internal.measurement import Measurement
from opensafely._vendor.opentelemetry.sdk.metrics._internal.metric_reader_storage import (
    MetricReaderStorage,
)
from opensafely._vendor.opentelemetry.sdk.metrics._internal.point import Metric
from opensafely._vendor.opentelemetry.util._time import _time_ns


class MeasurementConsumer(ABC):
    @abstractmethod
    def consume_measurement(self, measurement: Measurement) -> None:
        pass

    @abstractmethod
    def register_asynchronous_instrument(
        self,
        instrument: (
            "opensafely._vendor.opentelemetry.sdk.metrics._internal.instrument_Asynchronous"
        ),
    ):
        pass

    @abstractmethod
    def collect(
        self,
        metric_reader: "opensafely._vendor.opentelemetry.sdk.metrics.MetricReader",
        timeout_millis: float = 10_000,
    ) -> Iterable[Metric]:
        pass


class SynchronousMeasurementConsumer(MeasurementConsumer):
    def __init__(
        self,
        sdk_config: "opensafely._vendor.opentelemetry.sdk.metrics._internal.SdkConfiguration",
    ) -> None:
        self._lock = Lock()
        self._sdk_config = sdk_config
        # should never be mutated
        self._reader_storages: Mapping[
            "opensafely._vendor.opentelemetry.sdk.metrics.MetricReader", MetricReaderStorage
        ] = {
            reader: MetricReaderStorage(
                sdk_config,
                reader._instrument_class_temporality,
                reader._instrument_class_aggregation,
            )
            for reader in sdk_config.metric_readers
        }
        self._async_instruments: List[
            "opensafely._vendor.opentelemetry.sdk.metrics._internal.instrument._Asynchronous"
        ] = []

    def consume_measurement(self, measurement: Measurement) -> None:
        for reader_storage in self._reader_storages.values():
            reader_storage.consume_measurement(measurement)

    def register_asynchronous_instrument(
        self,
        instrument: (
            "opensafely._vendor.opentelemetry.sdk.metrics._internal.instrument._Asynchronous"
        ),
    ) -> None:
        with self._lock:
            self._async_instruments.append(instrument)

    def collect(
        self,
        metric_reader: "opensafely._vendor.opentelemetry.sdk.metrics.MetricReader",
        timeout_millis: float = 10_000,
    ) -> Iterable[Metric]:

        with self._lock:
            metric_reader_storage = self._reader_storages[metric_reader]
            # for now, just use the defaults
            callback_options = CallbackOptions()
            deadline_ns = _time_ns() + timeout_millis * 10**6

            default_timeout_millis = 10000 * 10**6

            for async_instrument in self._async_instruments:

                remaining_time = deadline_ns - _time_ns()

                if remaining_time < default_timeout_millis:

                    callback_options = CallbackOptions(
                        timeout_millis=remaining_time
                    )

                measurements = async_instrument.callback(callback_options)
                if _time_ns() >= deadline_ns:
                    raise MetricsTimeoutError(
                        "Timed out while executing callback"
                    )

                for measurement in measurements:
                    metric_reader_storage.consume_measurement(measurement)

        return self._reader_storages[metric_reader].collect()

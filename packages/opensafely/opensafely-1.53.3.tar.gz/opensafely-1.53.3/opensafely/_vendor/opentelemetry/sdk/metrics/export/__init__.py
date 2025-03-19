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
# FIXME Remove when 3.6 is no longer supported
from sys import version_info as _version_info

from opensafely._vendor.opentelemetry.sdk.metrics._internal.export import (  # noqa: F401
    AggregationTemporality,
    ConsoleMetricExporter,
    InMemoryMetricReader,
    MetricExporter,
    MetricExportResult,
    MetricReader,
    PeriodicExportingMetricReader,
)

# The point module is not in the export directory to avoid a circular import.
from opensafely._vendor.opentelemetry.sdk.metrics._internal.point import (  # noqa: F401
    DataPointT,
    DataT,
    Gauge,
    Histogram,
    HistogramDataPoint,
    Metric,
    MetricsData,
    NumberDataPoint,
    ResourceMetrics,
    ScopeMetrics,
    Sum,
)

__all__ = []
for key, value in globals().copy().items():
    if not key.startswith("_"):
        if _version_info.minor == 6 and key in ["DataPointT", "DataT"]:
            continue
        value.__module__ = __name__
        __all__.append(key)

from typing import Dict

from py_vertica_prom.metrics.sql_metric import SQLMetric
from py_vertica_prom.vertica_base import VerticaBase


class VerticaMetrics(VerticaBase):
    def __init__(self, conn_details: Dict) -> None:
        super().__init__(conn_details)

        # load version-agnostic metrics
        from py_vertica_prom.metrics.versions import base

        self.version = self.get_version()
        if self.version == "9.3.0":
            # load version-specific metrics before subclass introspection
            from py_vertica_prom.metrics.versions import v9_3_0

        self.sql_metrics = [cls() for cls in SQLMetric.__subclasses__()]

    def collect_data(self):
        for sql_metric in self.sql_metrics:
            sql_metric.query_result = self.query(sql_metric.sql_query)

    def refresh_all(self):
        self.collect_data()
        for sql_metric in self.sql_metrics:
            sql_metric.refresh()

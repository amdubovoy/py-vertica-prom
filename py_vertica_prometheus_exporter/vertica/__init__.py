from typing import Dict

from py_vertica_prometheus_exporter.vertica.vertica_base import VerticaBase


class Metrics:
    def __init__(self, conn_details: Dict) -> None:
        self.vertica = VerticaBase(conn_details)
        self.vertica_version = self.vertica.get_version()
        if self.vertica_version == "9.3.0":
            from py_vertica_prometheus_exporter.vertica.vertica_93 import Vertica93

            self.vertica = Vertica93(conn_details)
        else:
            raise NotImplementedError(
                f"Vertica {self.vertica_version} currently not supported."
            )

    def refresh(self):
        self.vertica.refresh_metrics()

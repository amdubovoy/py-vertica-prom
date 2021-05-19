from py_vertica_prometheus_exporter.vertica import VerticaBase
from py_vertica_prometheus_exporter.vertica.vertica_93.sql import SQL
from py_vertica_prometheus_exporter.vertica.vertica_93.metrics import node_states_enum


class Vertica93(VerticaBase):
    def __init__(self, conn_details) -> None:
        super().__init__(conn_details)

    def get_node_states(self):
        return self.query(SQL.node_states)

    def get_disk_usage(self):
        return self.query(SQL.disk_usage)

    def get_delete_vectors_count(self):
        return self.query(SQL.delete_vectors_count)

    def refresh_metrics(self):
        node_states = self.get_node_states()
        for node_state in node_states:
            node_states_enum.labels(
                node_state["node_id"], node_state["node_name"]
            ).state(node_state["node_state"])

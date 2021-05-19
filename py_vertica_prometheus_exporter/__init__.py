from prometheus_client.exposition import generate_latest
from prometheus_client.core import REGISTRY

from py_vertica_prometheus_exporter.config import config
from py_vertica_prometheus_exporter.vertica import Metrics


if __name__ == "__main__":
    m = Metrics(conn_details=config.vertica_conn_details)
    m.refresh()
    print(generate_latest(REGISTRY).decode("utf-8"))

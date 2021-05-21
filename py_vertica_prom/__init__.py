import copy
import logging
from time import sleep

from prometheus_client import start_http_server
from prometheus_client.core import REGISTRY

from py_vertica_prom.config import Config
from py_vertica_prom.cli import parser
from py_vertica_prom.metrics import VerticaMetrics


def run_server():
    logging.basicConfig(
        format=(
            f"%(asctime)s - [%(levelname)s] - %(name)s - "
            f"(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
        )
    )
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    server_config = Config()

    # Unregister defaults
    collectors = copy.copy(REGISTRY._collector_to_names)
    for collector in collectors:
        REGISTRY.unregister(collector)

    # Initialize metric objects
    metrics = VerticaMetrics(conn_details=server_config.vertica_conn_details)

    logger.info(f"Starting server. Listening on port {server_config.expose}")
    start_http_server(server_config.expose)

    try:
        while True:
            metrics.refresh_all()
            sleep(server_config.rate)
    except KeyboardInterrupt:
        logger.info("Server stopped")


if __name__ == "__main__":
    run_server()

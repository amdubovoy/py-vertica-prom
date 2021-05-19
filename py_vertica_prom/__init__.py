import copy
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler

from prometheus_client.core import REGISTRY
from prometheus_client.exposition import generate_latest

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

    # Serve metrics via exposed location
    class MetricsServer(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == server_config.location:
                # Refresh metrics only if Prometheus requested them
                metrics.refresh_all()

                self.send_response(200)
                self.send_header("Content-type", "text/plain")
                self.end_headers()
                self.wfile.write(generate_latest(REGISTRY))
            else:
                self.send_response(404)

    # Run web server
    web_server = HTTPServer(("", server_config.expose), MetricsServer)
    logger.info(
        "Server started. Get metrics at "
        f"http://localhost:{str(server_config.expose) + server_config.location}",
    )

    try:
        web_server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        web_server.server_close()
        logger.info("Server stopped.")


if __name__ == "__main__":
    run_server()

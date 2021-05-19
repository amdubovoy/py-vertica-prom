import copy
from http.server import HTTPServer, BaseHTTPRequestHandler

from prometheus_client.core import REGISTRY
from prometheus_client.exposition import generate_latest

from py_vertica_prom.config import config
from py_vertica_prom.metrics import VerticaMetrics


if __name__ == "__main__":
    # Unregister defaults
    collectors = copy.copy(REGISTRY._collector_to_names)
    for collector in collectors:
        REGISTRY.unregister(collector)

    # Initialize metric objects
    metrics = VerticaMetrics(conn_details=config.vertica_conn_details)

    # Serve metrics via exposed location
    class MetricsServer(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == config.location:
                # Refresh metrics only if Prometheus requested them
                metrics.refresh_all()

                self.send_response(200)
                self.send_header("Content-type", "text/plain")
                self.end_headers()
                self.wfile.write(generate_latest(REGISTRY))
            else:
                self.send_response(404)

    # Run web server
    web_server = HTTPServer(("", config.expose), MetricsServer)
    print(
        f"Server started http://localhost:{config.expose}. "
        f"Get metrics at http://localhost:{config.expose}{config.location}"
    )

    try:
        web_server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        web_server.server_close()
        print("Server stopped.")

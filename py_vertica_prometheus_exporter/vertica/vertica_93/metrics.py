from prometheus_client import Counter, Enum, Gauge, Histogram

node_states_enum = Enum(
    "vertica_node_state",
    "Vertica node state",
    labelnames=["node_id", "node_name"],
    states=["UP", "DOWN", "INITIALIZING"],
)

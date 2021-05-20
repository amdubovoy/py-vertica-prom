from prometheus_client import Gauge

from py_vertica_prom.metrics.sql_metric import SQLMetric


class WOSRowCount(SQLMetric):
    sql_query = """
        select  node_name,
                schema_name || '.' || storage_containers.projection_name as projection_name,
                total_row_count as vertica_wos_row_count
        from    v_monitor.storage_containers
        where   storage_type = 'WOS'
        order by
                vertica_wos_row_count desc
        limit   10;
    """
    metric_name = "vertica_wos_row_count"
    label_names = ["node_name", "projection_name"]
    metric = Gauge(metric_name, "WOS Projection row count.", label_names)

    def update_metric(self, new_value, labels):
        self.metric.labels(*labels).set(new_value)


class WOSUsedBytes(SQLMetric):
    sql_query = """
        select  node_name,
                schema_name || '.' || storage_containers.projection_name as projection_name,
                used_bytes as vertica_wos_used_bytes
        from    v_monitor.storage_containers
        where   storage_type = 'WOS'
        order by
                vertica_wos_used_bytes desc
        limit   10;
    """
    metric_name = "vertica_wos_used_bytes"
    label_names = ["node_name", "projection_name"]
    metric = Gauge(metric_name, "WOS Projection memory usage in bytes.", label_names)

    def update_metric(self, new_value, labels):
        self.metric.labels(*labels).set(new_value)

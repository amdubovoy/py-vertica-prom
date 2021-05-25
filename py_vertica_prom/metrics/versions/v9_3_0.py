from prometheus_client import Gauge

from py_vertica_prom.metrics.sql_metric import SQLMetric


class WOSRowCount(SQLMetric):
    sql_query = """
        select  node_name,
                sum(total_row_count) as vertica_wos_row_count
        from    storage_containers
        where   storage_type = 'WOS'
        group by
                node_name;
    """
    metric_name = "vertica_wos_row_count"
    label_names = ["node_name"]
    metric = Gauge(metric_name, "Current WOS row count.", label_names)

    def update_metric(self, new_value, labels):
        self.metric.labels(*labels).set(new_value)


class WOSUsedBytes(SQLMetric):
    sql_query = """
        select  node_name,
                sum(used_bytes) as vertica_wos_used_bytes
        from    storage_containers
        where   storage_type = 'WOS'
        group by
                node_name;
    """
    metric_name = "vertica_wos_used_bytes"
    label_names = ["node_name"]
    metric = Gauge(metric_name, "WOS memory usage in bytes.", label_names)

    def update_metric(self, new_value, labels):
        self.metric.labels(*labels).set(new_value)


class WOSContainerCount(SQLMetric):
    sql_query = """
        select  node_name,
                count(*) as vertica_wos_storage_container_count
        from    storage_containers
        where   storage_type = 'WOS'
        group by
                node_name;
    """
    metric_name = "vertica_wos_storage_container_count"
    label_names = ["node_name"]
    metric = Gauge(metric_name, "WOS storage container count.", label_names)

    def update_metric(self, new_value, labels):
        self.metric.labels(*labels).set(new_value)

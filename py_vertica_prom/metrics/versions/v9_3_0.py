from prometheus_client import Gauge, Enum

from py_vertica_prom.metrics.sql_metric import SQLMetric


class NodeState(SQLMetric):
    sql_query = """
        select  node_id,
                node_name,
                node_state as vertica_node_state
        from    nodes;
    """
    metric_name = "vertica_node_state"
    label_names = ["node_id", "node_name"]
    states = ["UP", "DOWN", "INITIALIZING"]
    metric = Enum(metric_name, "Vertica nodes states.", label_names, states=states)

    def update_metric(self, new_value, labels):
        self.metric.labels(*labels).state(new_value)


class DiskSpaceUsedMb(SQLMetric):
    sql_query = """
        select  node_name,
                storage_usage,
                disk_space_used_mb as vertica_disk_space_used_mb
        from    disk_storage;
    """
    metric_name = "vertica_disk_space_used_mb"
    label_names = ["node_name", "storage_usage"]
    metric = Gauge(metric_name, "Used disk space in mb.", label_names)

    def update_metric(self, new_value, labels):
        self.metric.labels(*labels).set(new_value)


class DiskSpaceFreeMb(SQLMetric):
    sql_query = """
        select  node_name,
                storage_usage,
                disk_space_free_mb as vertica_disk_space_free_mb
        from    disk_storage;
    """
    metric_name = "vertica_disk_space_free_mb"
    label_names = ["node_name", "storage_usage"]
    metric = Gauge(metric_name, "Free disk space in mb.", label_names)

    def update_metric(self, new_value, labels):
        self.metric.labels(*labels).set(new_value)


class DiskSpaceFreePercent(SQLMetric):
    sql_query = """
        select  node_name,
                storage_usage,
                rtrim(disk_space_free_percent, '%') as vertica_disk_space_free_percent
        from    disk_storage;
    """
    metric_name = "vertica_disk_space_free_percent"
    label_names = ["node_name", "storage_usage"]
    metric = Gauge(metric_name, "Free disk space percentage.", label_names)

    def update_metric(self, new_value, labels):
        self.metric.labels(*labels).set(new_value)


class DeleteVectorsCount(SQLMetric):
    sql_query = """
        select  node_name,
                count(*) as vertica_delete_vectors_cnt
        from    delete_vectors
        group by
                node_name;
    """
    metric_name = "vertica_delete_vectors_cnt"
    label_names = ["node_name"]
    metric = Gauge(metric_name, "Current delete vectors count.", label_names)

    def update_metric(self, new_value, labels):
        self.metric.labels(*labels).set(new_value)


class ProjectionDefragmentation(SQLMetric):
    sql_query = """
        select  node_name,
                projection_schema || '.' || projection_name as projection_name,
                sum(ros_count) as vertica_ros_count
        from    v_monitor.projection_storage
        group by
                node_name,
                projection_schema,
                projection_name
        order by
                vertica_ros_count desc
        limit   10;
    """
    metric_name = "vertica_ros_count"
    label_names = ["node_name", "projection_name"]
    metric = Gauge(metric_name, "Top 10 highest defragmented projections.", label_names)

    def update_metric(self, new_value, labels):
        self.metric.labels(*labels).set(new_value)

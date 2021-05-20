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


class ProjectionRowCount(SQLMetric):
    sql_query = """
        select  node_name,
                projection_schema || '.' || projection_storage.projection_name as projection_name,
                row_count as vertica_projection_row_count
        from    projection_storage
        order by
                vertica_projection_row_count desc
        limit   10;
    """
    metric_name = "vertica_projection_row_count"
    label_names = ["node_name", "projection_name"]
    metric = Gauge(metric_name, "Top 10 projections by row count", label_names)

    def update_metric(self, new_value, labels):
        self.metric.labels(*labels).set(new_value)


class ProjectionUsedBytes(SQLMetric):
    sql_query = """
        select  node_name,
                projection_schema || '.' || projection_storage.projection_name as projection_name,
                used_bytes as vertica_projection_used_bytes
        from    projection_storage
        order by
                vertica_projection_used_bytes desc
        limit   10;
    """
    metric_name = "vertica_projection_used_bytes"
    label_names = ["node_name", "projection_name"]
    metric = Gauge(metric_name, "Top 10 projections by bytes used", label_names)

    def update_metric(self, new_value, labels):
        self.metric.labels(*labels).set(new_value)


class TableRowCount(SQLMetric):
    sql_query = """
        select  node_name,
                table_name,
                sum(row_count) as vertica_table_row_count
        from    (
                    select  node_name,
                            projection_schema || '.' || anchor_table_name as table_name,
                            row_count,
                            rank() over (partition by node_name, projection_schema, anchor_table_name order by projection_name) as r
                    from    projection_storage ps
                ) as d
        where   r = 1
        group by
                1, 2
        order by
                vertica_table_row_count desc
        limit   10;
    """
    metric_name = "vertica_table_row_count"
    label_names = ["node_name", "table_name"]
    metric = Gauge(metric_name, "Top 10 tables by row count.", label_names)

    def update_metric(self, new_value, labels):
        self.metric.labels(*labels).set(new_value)


class TotalSessions(SQLMetric):
    sql_query = """
        select  node_name,
                total_user_session_count as vertica_total_user_session_count
        from    query_metrics;
    """
    metric_name = "vertica_total_user_session_count"
    label_names = ["node_name"]
    metric = Gauge(metric_name, "Total all-time user sessions.", label_names)

    def update_metric(self, new_value, labels):
        self.metric.labels(*labels).set(new_value)


class TotalQueriesExecuted(SQLMetric):
    sql_query = """
        select  node_name,
                executed_query_count as vertica_executed_query_count
        from    query_metrics;
    """
    metric_name = "vertica_executed_query_count"
    label_names = ["node_name"]
    metric = Gauge(metric_name, "Total all-time queries executed.", label_names)

    def update_metric(self, new_value, labels):
        self.metric.labels(*labels).set(new_value)


class TotalRowCount(SQLMetric):
    sql_query = """
        select  node_name,
                sum(row_count) as vertica_total_row_count
        from    projection_storage
        group by
                node_name;
    """
    metric_name = "vertica_total_row_count"
    label_names = ["node_name"]
    metric = Gauge(
        metric_name, "Total current row count for all tables in db.", label_names
    )

    def update_metric(self, new_value, labels):
        self.metric.labels(*labels).set(new_value)

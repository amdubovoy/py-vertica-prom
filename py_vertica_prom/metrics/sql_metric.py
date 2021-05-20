from typing import Optional, List, Union

from prometheus_client import Gauge, Summary, Histogram, Info, Enum


class SQLMetric:
    """
    Generic class that describes attributes and abstract update method,
    which is specific to each Prometheus metric update mechanism. All the
    metrics should inherit from this class.

    It also implements refresh logic through calling update methods on all
    children.
    """

    sql_query: str
    metric_name: str
    label_names: Optional[List]
    states: Optional[List]
    metric: Union[Gauge, Summary, Histogram, Info, Enum]
    query_result = Optional[List]

    def update_metric(self, new_value, labels):
        raise NotImplementedError

    def refresh(self):
        if self.query_result is not None:
            for row in self.query_result:
                new_value = row.get(self.metric_name)
                if new_value is not None:
                    labels = [row[label] for label in self.label_names]
                    self.update_metric(new_value, labels)

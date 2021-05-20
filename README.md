# Python Vertica Prometheus exporter

Runs as standalone container, thus can be isolated from your Vertica
instances and other services.

Feel free to contribute!

## Running in Docker

```shell
docker pull adubovoy/py-vertica-prom:latest
```

Or clone git repository to the target machine and execute docker build command:

```shell
docker build -t py-vertica-prom .
```

Run py-vertica-prom:

```shell
docker run -p 8000:5005 \
  --env DB_HOST=localhost \
  --env DB_PORT=5433 \
  --env DB_NAME=some_db \
  --env DB_USERNAME=dbadmin \
  --env DB_PASSWORD=qwerty123 \
  --env EXPOSE=5005 \
  --env LOCATION=/metrics \
  adubovoy/py-vertica-prom
```

All the values except for DB_NAME and DB_PASSWORD default to the values above.

Metrics will soon be available on `localhost:8000/metrics`.

## Metrics

Metrics available out of the box:

- `vertica_node_state`
- `vertica_disk_space_used_mb`
- `vertica_disk_space_free_mb`
- `vertica_disk_space_free_percent`
- `vertica_delete_vectors_cnt`
- `vertica_ros_count`
- `vertica_projection_row_count`
- `vertica_projection_used_bytes`
- `vertica_table_row_count`
- `vertica_total_user_session_count`
- `vertica_executed_query_count`
- `vertica_total_row_count`

_Specific to Vertica 9.3_:

- `vertica_wos_row_count`
- `vertica_wos_used_bytes`

## Adding custom metrics

There is a folder named `versions` in metrics module. Add your own custom files there,
and don't forget to import them to `VerticaMetrics` `__init__` method alongside
existing imports.

## About

- Easy to run.
- Lightweight (built image is ~70mb).
- Lazy: collects metrics only when Prometheus requests them.
- Only necessary dependencies (`vertica-python` and `prometheus-client`).

## TODO:

- Collect metrics in one big transaction instead of bunch of small ones
- Tests
- Project-wide exception handling
- More version-specific metrics

# Python Vertica Prometheus exporter

Runs as standalone container, thus can be isolated from your Vertica
instances and other services.

Currently, supports Vertica 9.3.0 only, but package can be easily adopted
to run with other Vertica releases. Feel free to contribute!

## Running in Docker

Clone repository to the target machine.

Execute following commands:

```shell
docker build -t py-vertica-prom .
```

```shell
docker run -p 8000:5005 \
  --env DB_HOST=localhost \
  --env DB_PORT=5433 \
  --env DB_NAME=some_db \
  --env DB_USERNAME=dbadmin \
  --env DB_PASSWORD=qwerty123 \
  --env EXPOSE=5005 \
  --env LOCATION=/metrics \
  py-vertica-prom
```

All the values except for DB_NAME and DB_PASSWORD default to the values above.

Metrics will soon be available on `localhost:8000/metrics`.

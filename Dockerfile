FROM python:3.9.5-alpine

RUN addgroup -S exporter
RUN adduser -SD exporter -G exporter

COPY --chown=exporter:exporter . /py_vertica_prom

RUN pip3 install -e py_vertica_prom

USER exporter

ENTRYPOINT ["py-vertica-prom"]

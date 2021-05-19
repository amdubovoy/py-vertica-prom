import argparse


parser = argparse.ArgumentParser(
    description=(
        "Provide general settings and vertica connection details. "
        "Overwrites environment variables."
    )
)
parser.add_argument(
    "--expose",
    "-e",
    help="Specify port to expose. Defaults to `8000`.",
    type=int,
)
parser.add_argument(
    "--location",
    "-l",
    help="Specify metrics location. Defaults to `/metrics`.",
    type=str,
)
parser.add_argument(
    "--host",
    "-H",
    help="Vertica host address without port. Defaults to `localhost`.",
    type=str,
)
parser.add_argument(
    "--port",
    "-p",
    help="Vertica port. Defaults to `5433`.",
    type=int,
)
parser.add_argument(
    "--db",
    "-d",
    help="Vertica database name.",
    type=str,
)
parser.add_argument(
    "--username",
    "-u",
    help="Vertica admin username. Defaults to `dbadmin`.",
    type=str,
)
parser.add_argument(
    "--password",
    "-P",
    help="Vertica admin password.",
    type=str,
)

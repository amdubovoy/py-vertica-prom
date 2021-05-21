import os

from py_vertica_prom.cli import parser


class Config:
    def __init__(self):
        args = parser.parse_args()

        host = args.host or os.environ.get("DB_HOST") or "localhost"
        port = int(args.port or os.environ.get("DB_PORT") or 5433)
        db = args.db or os.environ.get("DB_NAME")
        if db is None:
            raise ValueError("Database name not provided in env or CLI arguments.")
        username = args.username or os.environ.get("DB_USERNAME") or "dbadmin"
        password = args.password or os.environ.get("DB_PASSWORD")
        if password is None:
            raise ValueError(
                "Vertica admin user password not provided in env or CLI arguments."
            )

        self.expose = int(args.expose or os.environ.get("EXPOSE") or 8000)
        self.rate = int(args.rate or os.environ.get("RATE") or 15)
        self.vertica_conn_details = {
            "host": host,
            "port": port,
            "database": db,
            "user": username,
            "password": password,
        }

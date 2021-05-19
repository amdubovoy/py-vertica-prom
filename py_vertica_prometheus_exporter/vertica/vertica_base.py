import re
from typing import Optional, List, Dict

import vertica_python
from vertica_python import Connection
from vertica_python.vertica.cursor import Cursor


version_re = re.compile(r"\d+.\d+.\d+")


class VerticaBase:
    def __init__(self, conn_details: Dict) -> None:
        self.conn_details = conn_details
        self.conn_details.update({"connection_load_balance": True})

    def get_connection(self) -> Connection:
        conn = vertica_python.connect(**self.conn_details)
        return conn

    @staticmethod
    def get_cursor(conn: Connection) -> Cursor:
        return conn.cursor("dict")

    def query(self, sql: str) -> Optional[List]:
        with self.get_connection() as conn:
            with self.get_cursor(conn) as cur:
                cur.execute(sql)
                return cur.fetchall()

    def query_first(self, sql: str) -> Optional[Dict]:
        with self.get_connection() as conn:
            with self.get_cursor(conn) as cur:
                cur.execute(sql)
                return cur.fetchone()

    def query_multiple(self, sql_list: List) -> List:  # TODO: use this pls
        with self.get_connection() as conn:
            with self.get_cursor(conn) as cur:
                res = []
                for sql in sql_list:
                    res.append(cur.execute(sql))
                return res

    def get_version(self) -> str:
        query_result = self.query_first(""" select version(); """)["version"]
        return re.search(version_re, query_result).group(0)

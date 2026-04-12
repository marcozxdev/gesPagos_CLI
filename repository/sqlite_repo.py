from data.database import conn, cursor


class Sqlite:
    def __init__(self, conn=conn, cursor=cursor):
        self.conn = conn
        self.cursor = cursor


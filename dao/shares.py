import psycopg2
from dbconfig.pg_config import pg_config

class SharesDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host='localhost'" % (
        pg_config['dbname'], pg_config['user'], pg_config['password'], pg_config['dbport'])
        self.conn = psycopg2.connect(connection_url)

    def getAllShares(self):
        cursor = self.conn.cursor()
        query = "select * from shares;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def insertShare(self, uid, mid):
        cursor = self.conn.cursor()
        query = "insert into shares (uid,mid) values (%s,%s) returning sid; "
        cursor.execute(query, (uid, mid))
        sid = cursor.fetchone()[0]
        self.conn.commit()
        return sid
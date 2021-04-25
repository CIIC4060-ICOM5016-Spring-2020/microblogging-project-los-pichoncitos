import psycopg2
from dbconfig.pg_config import pg_config


class ReplyDAO:
    def __init__(self):
        connection_url = "host=%s dbname=%s user=%s password=%s port=%s" % (pg_config['host'], pg_config['dbname'], pg_config['user'], pg_config['password'], pg_config['dbport'])
        self.conn = psycopg2.connect(connection_url)

    def getAllReply(self):
        cursor = self.conn.cursor()
        query = "select rmessage,uid,mid from reply;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def insertReply(self,rmessage, uid, mid):
        cursor = self.conn.cursor()
        query = "insert into reply (rmessage,uid,mid) values (%s,%s,%s) returning rid; "
        cursor.execute(query, (rmessage,uid, mid))
        id = cursor.fetchone()[0]
        self.conn.commit()
        return id
import psycopg2
from dbconfig.pg_config import pg_config


class BlockDAO:
    def __init__(self):
        connection_url = "host=%s dbname=%s user=%s password=%s port=%s" % (pg_config['host'], pg_config['dbname'], pg_config['user'], pg_config['password'], pg_config['dbport'])
        self.conn = psycopg2.connect(connection_url)

    def insertBlock(self, blockingid, uid):
        cursor = self.conn.cursor()
        query = "insert into blocks(blockingid,uid) values (%s,%s) returning bid; "
        cursor.execute(query, (blockingid, uid,))
        bid = cursor.fetchone()[0]
        self.conn.commit()
        return bid

    def getAllBlockedby(self, uid):
        cursor = self.conn.cursor()
        query = "select blockingid from blocks where uid = %s;"
        cursor.execute(query, (uid,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllBlocking(self, blockingid):
        cursor = self.conn.cursor()
        query = "select uid from blocks where blockingid = %s;"
        cursor.execute(query, (blockingid,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def insertUnblock(self, uid, blockingid):
        cursor = self.conn.cursor()
        query = "delete from blocks where blockingid = %s and uid = %s;"
        cursor.execute(query, (uid, blockingid,))
        affected_rows = cursor.rowcount
        self.conn.commit()
        return affected_rows != 0

    def checkBlocked(self, id, blockingid):
        cursor = self.conn.cursor()
        query = "select bid from blocks where (blockingid = %s and uid = %s) or (uid = %s and blockingid = %s);"
        cursor.execute(query, (id, blockingid))
        rows = cursor.rowcount

        return rows >= 1


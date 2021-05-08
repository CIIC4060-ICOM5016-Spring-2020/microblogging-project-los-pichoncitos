import psycopg2
from dbconfig.pg_config import pg_config


class ReactDAO:
    def __init__(self):
        connection_url = "host=%s dbname=%s user=%s password=%s port=%s" % (pg_config['host'], pg_config['dbname'], pg_config['user'], pg_config['password'], pg_config['dbport'])
        self.conn = psycopg2.connect(connection_url)

    def insertReact(self, uid, mid, isLiked):
        cursor = self.conn.cursor()
        query = "insert into reacts (uid, mid, isLiked) values (%s,%s,%s) returning reid;"
        cursor.execute(query, (uid, mid, isLiked,))
        reactid = cursor.fetchone()[0]
        self.conn.commit()
        return reactid

    def getLikesById(self, mid):
        cursor = self.conn.cursor()
        query = "select distinct uid from reacts where mid = %s and isLiked = true;"
        cursor.execute(query, (mid,))
        result = cursor.fetchall()
        return result

    def getUnlikesById(self, mid):
        cursor = self.conn.cursor()
        query = "select distinct uid from reacts where mid = %s and isLiked = false;"
        cursor.execute(query, (mid,))
        result = cursor.fetchall()
        return result

    def deleteLike(self, uid, mid):
        cursor = self.conn.cursor()
        query = "delete from reacts where uid = %s and mid = %s and isLiked = True;"
        cursor.execute(query, (uid, mid,))
        # determine affected rows
        affected_rows = cursor.rowcount
        self.conn.commit()
        # if affected rows == 0, the part was not found and hence not deleted
        # otherwise, it was deleted, so check if affected_rows != 0
        return affected_rows != 0

    def deleteUnlike(self, uid, mid):
        cursor = self.conn.cursor()
        query = "delete from reacts where uid=%s and mid = %s and isLiked = False;"
        cursor.execute(query, (uid, mid,))
        # determine affected rows
        affected_rows = cursor.rowcount
        self.conn.commit()
        # if affected rows == 0, the part was not found and hence not deleted
        # otherwise, it was deleted, so check if affected_rows != 0
        return affected_rows != 0

    def checkBlocked(self, uid,  mid):
        cursor = self.conn.cursor()
        query = "select bid from blocks inner join messages on blocks.uid = messages.uid where blocks.uid = %s and messages.uid = %s;"
        cursor.execute(query, (uid, mid,))
        rows = cursor.rowcount
        # if affected rows == 0, the part was not found and hence not deleted
        # otherwise, it was deleted, so check if affected_rows != 0
        return rows != 0
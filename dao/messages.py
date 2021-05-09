import psycopg2
from dbconfig.pg_config import pg_config


class MessageDAO:
    def __init__(self):
        connection_url = "host=%s dbname=%s user=%s password=%s port=%s" % (pg_config['host'], pg_config['dbname'], pg_config['user'], pg_config['password'], pg_config['dbport'])
        self.conn = psycopg2.connect(connection_url)

    def getAllMessages(self):
        cursor = self.conn.cursor()
        query = "select mid, message, uid from messages where isShare = False and isReply = False;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        cursor = self.conn.cursor()
        query = "select mid, message, uid, replyingto from messages where isShare = False and isReply = True;"
        cursor.execute(query)
        for row in cursor:
            result.append(row)
        cursor = self.conn.cursor()
        query = "select mid, uid, sharing from messages where isShare = True and isReply = False;"
        cursor.execute(query)
        for row in cursor:
            result.append(row)

        return result

    def getMessagebyId(self, mid):
        cursor = self.conn.cursor()
        query = "select mid,message,uid from messages where mid = %s and isShare = False and isReply = False;"
        cursor.execute(query, (mid,))
        check = cursor.rowcount
        if check != 0:
            return cursor.fetchone()

        cursor = self.conn.cursor()
        query = "select mid,message,uid,replyingto from messages where mid = %s and isShare = False and isReply = True;"
        cursor.execute(query, (mid,))
        check = cursor.rowcount
        if check != 0:
            return cursor.fetchone()

        cursor = self.conn.cursor()
        query = "select mid,uid,sharing from messages where mid = %s and isShare = True and isReply = False;"
        cursor.execute(query, (mid,))
        result = cursor.fetchone()
        return result

    def insertMessage(self, message, uid, isShare,  isReply):
        cursor = self.conn.cursor()
        query = "insert into messages (message,uid, isShare, isReply) values (%s,%s,%s,%s) returning mid; "
        cursor.execute(query,  (message, uid, isShare,  isReply))
        mid = cursor.fetchone()[0]
        self.conn.commit()
        return mid

    def insertReply(self, message, uid, replyingto, isShare, isReply):
        cursor = self.conn.cursor()
        query = "insert into messages (message,uid,replyingto,isShare,isReply) values (%s,%s,%s,%s,%s) returning mid; "
        cursor.execute(query, (message, uid, replyingto, isShare, isReply))
        id = cursor.fetchone()[0]
        self.conn.commit()
        return id

    def insertShare(self, uid, sharing, isShare, isReply):
        cursor = self.conn.cursor()
        query = "insert into messages (uid,sharing,isShare,isReply) values (%s,%s,%s,%s) returning mid; "
        cursor.execute(query, (uid, sharing, isShare, isReply))
        mid = cursor.fetchone()[0]
        self.conn.commit()
        return mid

    def isShare(self, mid):
        cursor = self.conn.cursor()
        query = "select isShare from messages where mid = %s;"
        cursor.execute(query, (mid,))
        isShare = cursor.fetchone()[0]
        return isShare

    def isReply(self, mid):
        cursor = self.conn.cursor()
        query = "select isReply from messages where mid = %s;"
        cursor.execute(query, (mid,))
        isReply = cursor.fetchone()[0]
        return isReply

    def checkBlocked(self, uid, mid):
        cursor = self.conn.cursor()
        query = "select uid from messages where mid = %s;"
        cursor.execute(query, (mid))
        id = cursor.fetchone()[0]
        query = "select bid from blocks where (uid = %s and blockingid = %s) or (blockingid = %s and uid = %s);"
        cursor.execute(query, (uid, id, uid, id))
        rows = cursor.rowcount
        return rows != 0

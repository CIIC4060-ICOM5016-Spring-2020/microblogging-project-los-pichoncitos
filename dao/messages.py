import psycopg2
from dbconfig.pg_config import pg_config


class MessageDAO:
    def __init__(self):
        connection_url = "host=%s dbname=%s user=%s password=%s port=%s" % (pg_config['host'], pg_config['dbname'], pg_config['user'], pg_config['password'], pg_config['dbport'])
        self.conn = psycopg2.connect(connection_url)

    def getAllMessages(self):
        cursor = self.conn.cursor()
        query = "select mid, mdate, message, uid from messages;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getMessagebyId(self, mid):
        cursor = self.conn.cursor()
        query = "select mid,mdate,message,uid from messages where mid = %s;"
        cursor.execute(query, (mid,))
        result = cursor.fetchone()
        return result

    def insertMessage(self, mdate, message, uid):
        cursor = self.conn.cursor()
        query = "insert into messages (mdate, message, uid) values (%s,%s,%s) returning mid; "
        cursor.execute(query, (mdate, message, uid))
        mid = cursor.fetchone()[0]
        self.conn.commit()
        return mid

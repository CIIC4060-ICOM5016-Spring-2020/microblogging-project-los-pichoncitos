import psycopg2
from dbconfig.pg_config import pg_config


class UserDAO:
    def __init__(self):
        connection_url = "host=%s dbname=%s user=%s password=%s port=%s" % (pg_config['host'], pg_config['dbname'], pg_config['user'], pg_config['password'], pg_config['dbport'])
        self.conn = psycopg2.connect(connection_url)

    def getAllUsers(self):
        cursor = self.conn.cursor()
        query = "select uid, first_name, last_name, email, username, password from users;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getUserbyId(self, uid):
        cursor = self.conn.cursor()
        query = "select uid, first_name, last_name, email, username, password from users where uid = %s;"
        cursor.execute(query, (uid,))
        result = cursor.fetchone()
        return result

    def insertUser(self, first_name, last_name, email, username, password):
        cursor = self.conn.cursor()
        query = "insert into users (first_name, last_name, email, username, password) values (%s,%s,%s,%s,%s) returning uid; "
        cursor.execute(query, (first_name, last_name, email, username, password))
        uid = cursor.fetchone()[0]
        self.conn.commit()
        return uid

    def updateUser(self, uid, first_name, last_name, email, username, password):
        cursor = self.conn.cursor()
        query = "update users set first_name=%s, last_name = %s, email=%s, username=%s, password=%s, " \
                "where uid=%s; "
        cursor.execute(query, (first_name, last_name, email,username, password, uid))
        self.conn.commit()
        return True

    def deleteUser(self, uid):
        cursor = self.conn.cursor()
        query = "delete from users where uid=%s;"
        cursor.execute(query, (uid,))
        # determine affected rows
        affected_rows = cursor.rowcount
        self.conn.commit()
        # if affected rows == 0, the part was not found and hence not deleted
        # otherwise, it was deleted, so check if affected_rows != 0
        return affected_rows != 0

    def checkUser(self, email, username):
        cursor = self.conn.cursor()
        query = "select uid from users where email=%s or username=%s;"
        cursor.execute(query, (email,username))
        rows = cursor.rowcount

        return rows>=1

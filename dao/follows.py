import psycopg2
from dbconfig.pg_config import pg_config


class FollowDAO:
    def __init__(self):
        connection_url = "host=%s dbname=%s user=%s password=%s port=%s" % (pg_config['host'], pg_config['dbname'], pg_config['user'], pg_config['password'], pg_config['dbport'])
        self.conn = psycopg2.connect(connection_url)

    def getFollowedBy(self, followingid):
        cursor = self.conn.cursor()
        query = "select distinct followerid from follows where followingid = %s;"
        cursor.execute(query, (followingid,))
        result = cursor.fetchall()
        return result

    def getFollowing(self,followerid):
        cursor = self.conn.cursor()
        query = "select distinct followingid from follows where followerid = %s;"
        cursor.execute(query, (followerid,))
        result = cursor.fetchall()
        return result

    def insertFollow(self, followerid, followingid):
        cursor = self.conn.cursor()
        query = "insert into follows (followerid, followingid) values (%s,%s) returning fid; "
        cursor.execute(query, (followerid,followingid,))
        fid = cursor.fetchone()[0]
        self.conn.commit()
        return fid

    def deleteFollow(self, followerid, followingid):
        cursor = self.conn.cursor()
        query = "delete from follows where followerid= %s and followingid = %s;"
        cursor.execute(query, (followerid, followingid,))
        # determine affected rows
        affected_rows = cursor.rowcount
        self.conn.commit()
        return affected_rows != 0

    def checkFollow(self, followerid, followingid):
        cursor = self.conn.cursor()
        query = "select fid from follows where followerid= %s and followingid = %s;"
        cursor.execute(query, (followerid, followingid,))
        rows = cursor.rowcount
        return rows >= 1

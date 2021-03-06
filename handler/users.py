from flask import jsonify
from dao.users import UserDAO
import psycopg2
from dbconfig.pg_config import pg_config


class BaseUser:
    def __init__(self):
        connection_url = "host=%s dbname=%s user=%s password=%s port=%s" % (pg_config['host'], pg_config['dbname'], pg_config['user'], pg_config['password'], pg_config['dbport'])
        self.conn = psycopg2.connect(connection_url)

    def getAllUsers(self):
        dao = UserDAO()
        user_list = dao.getAllUsers()
        result = []
        for row in user_list:
            obj = self.build_map_dict(row)
            result.append(obj)
        return jsonify(result)

    def build_attr_dict(self, uid, first_name, last_name, email, username, password):
        result = {}
        result['uid'] = uid
        result['first_name'] = first_name
        result['last_name'] = last_name
        result['email'] = email
        result['username'] = username
        result['password'] = password
        return result

    def build_map_dict(self, row):
        result = {}
        result['uid'] = row[0]
        result['first_name'] = row[1]
        result['last_name'] = row[2]
        result['email'] = row[3]
        result['username'] = row[4]
        result['password'] = row[5]
        return result

    def getUserbyId(self, uid):
        dao = UserDAO()
        user_tuple = dao.getUserbyId(uid)
        if not user_tuple:
            return jsonify("Not Found"), 404
        else:
            result = self.build_map_dict(user_tuple)
            return jsonify(result) 

    def addNewUser(self, json):

        first_name = json['first_name']
        last_name = json['last_name']
        email = json['email']
        username = json['username']
        password = json['password']
        dao = UserDAO()
        checkUser = dao.checkUser(email, username)
        
        if checkUser:
            return jsonify("Username or Email are already used by an existing user"), 200
        uid = dao.insertUser(first_name, last_name, email, username, password)
        result = self.build_attr_dict(uid, first_name, last_name, email, username,  password)
        return jsonify(result), 201

    def updateUser(self, uid, json):
        first_name = json['first_name']
        last_name = json['last_name']
        email = json['email']
        username = json['username']
        password = json['password']
        dao = UserDAO()
        updated_code = dao.updateUser(uid, first_name, last_name, email, username, password)
        result = self.build_attr_dict(uid, first_name, last_name, email, username, password)
        return jsonify(result), 200

    def deleteUser(self, uid):
        dao = UserDAO()
        result = dao.deleteUser(uid)
        if result:
            return jsonify("DELETED"), 200
        else:
            return jsonify("NOT FOUND"), 404
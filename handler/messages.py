from flask import jsonify
from dao.messages import MessageDAO


class BaseMessage:
    def getAllMessages(self):
        dao = MessageDAO()
        message_list = dao.getAllMessages()
        result = []
        for row in message_list:
            obj = self.build_map_dict(row)
            result.append(obj)
        return jsonify(result)

    def build_attr_dict(self, mid, message, uid):
        result = {}
        result['ID'] = mid
        result['Text'] = message
        result['RegisteredUser'] = uid
        return result

    def build_map_dict(self, row):
        result = {}
        result['ID'] = row[0]
        result['Text'] = row[1]
        result['RegisteredUser'] = row[2]
        return result

    def getMessagebyId(self, uid):
        dao = MessageDAO()
        user_tuple = dao.getMessagebyId(uid)
        if not user_tuple:
            return jsonify("Not Found"), 404
        else:
            result = self.build_map_dict(user_tuple)
            return jsonify(result)

    def addNewMessage(self, json):
        message = json['Text']
        uid = json['RegisteredUser']
        dao = MessageDAO()
        mid = dao.insertMessage(message, uid)
        result = self.build_attr_dict(mid, message, uid)
        return jsonify(result), 201


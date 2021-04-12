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

    def build_attr_dict(self, mid, mdate, message, uid):
        result = {}
        result['mid'] = mid
        result['mdate'] = mdate
        result['message'] = message
        result['uid'] = uid
        return result

    def build_map_dict(self, row):
        result = {}
        result['mid'] = row[0]
        result['mdate'] = row[1]
        result['message'] = row[2]
        result['uid'] = row[3]
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
        mdate = json['mdate']
        message = json['message']
        uid = json['uid']
        dao = MessageDAO()
        mid = dao.insertMessage(mdate,message, uid)
        result = self.build_attr_dict(mid, mdate, message, uid)
        return jsonify(result), 201


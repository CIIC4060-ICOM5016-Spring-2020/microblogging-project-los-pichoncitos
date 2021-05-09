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
        message_list = dao.getAllReplies()
        for row in message_list:
            obj = self.build_map_dict_reply(row)
            result.append(obj)
        message_list = dao.getAllShares()
        for row in message_list:
            obj = self.build_map_dict_share(row)
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

    def build_attr_dict_reply(self, mid, message, uid, rid):
        result = {}
        result['ID'] = mid
        result['RegisteredUser'] = uid
        result['Text'] = message
        result['replyingto'] = rid
        return result

    def build_map_dict_reply(self, row):
        result = {}
        result['ID'] = row[0]
        result['RegisteredUser'] = row[1]
        result['Text'] = row[2]
        result['replyingto'] = row[3]
        return result

    def build_attr_dict_share(self,id,uid,mid):
        result = {}
        result['ID'] = id
        result['RegisteredUser'] = uid
        result['sharing'] = mid
        return result

    def build_map_dict_share(self, row):
        result = {}
        result['ID'] = row[0]
        result['RegisteredUser'] = row[1]
        result['sharing'] = row[2]
        return result

    def getMessagebyId(self, id):
        dao = MessageDAO()
        user_tuple = dao.getMessagebyId(id)

        if not user_tuple:
            return jsonify("Not Found"), 404

        isShare = dao.isShare(id)
        isReply = dao.isReply(id)

        if isShare == False and isReply == False:
            result = self.build_map_dict(user_tuple)
            return jsonify(result)
        if isShare == False and isReply == True:
            result = self.build_map_dict_reply(user_tuple)
            return jsonify(result)
        else:
            result = self.build_map_dict_share(user_tuple)
            return jsonify(result)

    def addNewMessage(self, json):
        message = json['Text']
        uid = json['RegisteredUser']
        isShare = False
        isReply = False
        dao = MessageDAO()
        mid = dao.insertMessage(message, uid, isShare, isReply)
        result = self.build_attr_dict(mid, message, uid)
        return jsonify(result), 201

    def addNewReply(self, json):
        uid = json['RegisteredUser']
        message = json['Text']
        rid = json['replyingto']
        isShare = False
        isReply = True
        dao = MessageDAO()
        checkBlock = dao.checkBlocked(uid, rid)
        if checkBlock:
            return jsonify("BLOCKED, can't reply message"), 200
        mid = dao.insertReply(message, uid, rid, isShare, isReply)
        result = self.build_attr_dict_reply(mid, message, uid, rid)
        return jsonify(result), 201

    def addNewShare(self, json):
        uid = json['RegisteredUser']
        sid = json['sharing']
        isShare = True
        isReply = False
        dao = MessageDAO()
        checkBlock = dao.checkBlocked(uid, sid)
        if checkBlock:
            return jsonify("BLOCKED, can't share message"), 200
        id = dao.insertShare(uid, sid, isShare, isReply)
        result = self.build_attr_dict_share(id,uid,sid)
        return jsonify(result), 201


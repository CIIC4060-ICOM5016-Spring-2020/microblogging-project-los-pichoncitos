from flask import jsonify

from dao.reply import ReplyDAO


class BaseReply:
    def getAllReply(self):
        dao = ReplyDAO()
        reply_list = dao.getAllReply()
        result = []
        for row in reply_list:
            obj = self.build_map_dict(row)
            result.append(obj)
        return jsonify(result)

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

    def addNewReply(self, json):
        uid = json['RegisteredUser']
        rmessage = json['Text']
        mid = json['replyingto']
        dao = ReplyDAO()
        id = dao.insertReply(rmessage, uid, mid)
        result = self.build_attr_dict(rmessage, uid, mid)
        return jsonify(result), 201
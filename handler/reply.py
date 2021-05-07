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

    def build_attr_dict(self, rmessage, uid, mid):
        result = {}
        result['RegisteredUser'] = uid
        result['Text'] = rmessage
        result['replyingto'] = mid
        return result

    def build_map_dict(self, row):
        result = {}
        result['RegisteredUser'] = row[0]
        result['Text'] = row[1]
        result['replyingto'] = row[2]
        return result

    def addNewReply(self, json):
        uid = json['RegisteredUser']
        rmessage = json['Text']
        mid = json['replyingto']
        dao = ReplyDAO()
        id = dao.insertReply(rmessage, uid, mid)
        result = self.build_attr_dict(rmessage, uid, mid)
        return jsonify(result), 201
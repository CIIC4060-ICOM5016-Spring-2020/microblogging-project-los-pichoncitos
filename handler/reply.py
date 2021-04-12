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
        result['rmessage'] = rmessage
        result['uid'] = uid
        result['mid'] = mid
        return result

    def build_map_dict(self, row):
        result = {}
        result['rmessage'] = row[0]
        result['uid'] = row[1]
        result['mid'] = row[2]
        return result

    def addNewReply(self, json):
        rmessage = json['rmessage']
        uid = json['uid']
        mid = json['mid']
        dao = ReplyDAO()
        id = dao.insertReply(rmessage, uid, mid)
        result = self.build_attr_dict(rmessage, uid, mid)
        return jsonify(result), 201
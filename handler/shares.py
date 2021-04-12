from flask import jsonify
from dao.shares import SharesDAO


class BaseShare:
    def getAllShares(self):
        dao = SharesDAO()
        share_list = dao.getAllShares()
        result = []
        for row in share_list:
            obj = self.build_map_dict(row)
            result.append(obj)
        return jsonify(result)

    def build_attr_dict(self, uid,mid):
        result = {}
        result['uid'] = uid
        result['mid'] = mid
        return result

    def build_map_dict(self, row):
        result = {}
        result['uid'] = row[1]
        result['mid'] = row[2]
        return result


    def addNewShare(self, json):
        uid = json['uid']
        mid = json['mid']
        dao = SharesDAO()
        id =dao.insertShare(uid, mid)
        result = self.build_attr_dict(uid,mid)
        return jsonify(result), 201

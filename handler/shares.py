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


    def addNewShare(self, json):
        uid = json['RegisteredUser']
        mid = json['sharing']
        isShare = True
        isReply = False
        dao = SharesDAO()
        id =dao.insertShare(uid, mid)
        result = self.build_attr_dict(id,uid,mid)
        return jsonify(result), 201

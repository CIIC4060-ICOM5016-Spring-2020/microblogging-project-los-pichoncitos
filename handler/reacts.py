from flask import jsonify
from dao.reacts import ReactDAO


class BaseReact:

    def build_attr_dict(self, uid, mid, isLiked):
        result = {}
        result['RegisteredUser'] = uid
        result['mid'] = mid
        result['isLiked'] = isLiked
        return result

    def build_map_dict(self, row):
        result = {}
        result['RegisteredUser'] = row[0]
        return result

    def getLikesById(self, mid):
        dao = ReactDAO()
        follow_list = dao.getLikesById(mid)
        result = []
        for row in follow_list:
            obj = self.build_map_dict(row)
            result.append(obj)
        return jsonify(result)

    def getUnlikesById(self, mid):
        dao = ReactDAO()
        follow_list = dao.getUnlikesById(mid)
        result = []
        for row in follow_list:
            obj = self.build_map_dict(row)
            result.append(obj)
        return jsonify(result)

    def insertLike(self, json, mid):
        uid = json['RegisteredUser']
        isLiked = True
        dao = ReactDAO()
        checkBlock = dao.checkBlocked(uid, mid)
        if checkBlock:
            return jsonify("Registered user has message's user blocked, can't react to message"), 200
        reid = dao.insertReact(uid, mid, isLiked)
        result = self.build_attr_dict(uid, mid, isLiked)
        return jsonify(result), 201

    def insertUnlike(self, json, mid):
        uid = json['RegisteredUser']
        isLiked = False
        dao = ReactDAO()
        reid = dao.insertReact(uid, mid, isLiked)
        result = self.build_attr_dict(uid, mid, isLiked)
        return jsonify(result), 201


    def deleteLike(self, json, mid):
        uid = json['RegisteredUser']
        dao = ReactDAO()
        result = dao.deleteLike(uid, mid)
        if result:
            return jsonify("DELETED"), 200
        else:
            return jsonify("NOT FOUND"), 404

    def deleteUnlike(self, json, mid):
        uid = json['RegisteredUser']
        dao = ReactDAO()
        result = dao.deleteUnlike(uid, mid)
        if result:
            return jsonify("DELETED"), 200
        else:
            return jsonify("NOT FOUND"), 404
from flask import jsonify, json
from dao.blocks import BlockDAO


class BaseBlock:

    def getBlockedBy(self, blockingid):
        dao = BlockDAO()
        follow_list = dao.getAllBlockedby(blockingid)
        result = []
        for row in follow_list:
            obj = self.build_map_dictBlocked(row)
            result.append(obj)

        if len(result) == 0:
            return jsonify("Doesn't have a user blocked"), 404

        return jsonify(result)

    def getBlocking(self,uid):
        dao = BlockDAO()
        follow_list = dao.getAllBlocking(uid)
        result = []
        for row in follow_list:
            obj = self.build_map_dictBlocking(row)
            result.append(obj)

        if len(result) == 0:
            return jsonify("Is not blocked by a user"), 404

        return jsonify(result)

    def build_attr_dict(self, blockingid, uid):
        result = {}
        # result['fid'] = fid
        result['blocking'] = blockingid
        result['RegisteredUser'] = uid
        return result

    def build_map_dictBlocked(self, row):
        result = {}
        # result['fid'] = row[0]
        # result['uid'] = row[0]
        result['blocking user'] = row[0]
        return result

    def build_map_dictBlocking(self, row):
        result = {}
        # result['fid'] = row[0]
        # result['rid'] = row[0]
        result['blocked by user'] = row[0]
        return result

    def addNewBlock(self, json, blockingid):
        # fid = json['fid']
        uid = json['RegisteredUser']
        if uid == blockingid:
            return jsonify("ERROR, same userid"), 404
        dao = BlockDAO()
        checkBlock = dao.checkBlocked2(blockingid, uid)
        if checkBlock:
            return jsonify("User is already blocked"), 200
        checkFollow = dao.checkFollow(uid, blockingid)
        if checkFollow:
            unfollowed = dao.deleteFollow(uid, blockingid)
        bid = dao.insertBlock(blockingid, uid)
        result = self.build_attr_dict(blockingid, uid)
        return jsonify(result), 201

    def deleteBlock(self, json, blockingid):
        uid = json['RegisteredUser']
        if uid == blockingid:
            return jsonify("ERROR, same userid"), 404
        dao = BlockDAO()
        result = dao.insertUnblock(blockingid, uid)
        if result:
            return jsonify("UNBLOCKED"), 200
        else:
            return jsonify("NOT FOUND"), 404
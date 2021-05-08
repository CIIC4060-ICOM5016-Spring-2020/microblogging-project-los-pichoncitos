from flask import jsonify, json

from dao.blocks import BlockDAO
from dao.follows import FollowDAO


class BaseFollow:

    def getFollowedBy(self, followingid):
        dao = FollowDAO()
        follow_list = dao.getFollowedBy(followingid)
        result = []
        for row in follow_list:
            obj = self.build_map_dictFollowed(row)
            result.append(obj)
        return jsonify(result)

    def getFollowing(self,followerid):
        dao = FollowDAO()
        follow_list = dao.getFollowing(followerid)
        result = []
        for row in follow_list:
            obj = self.build_map_dictFollowing(row)
            result.append(obj)
        return jsonify(result)

    def build_attr_dict(self, followingid, followerid):
        result = {}
        result['follower'] = followerid
        result['RegisteredUser'] = followingid
        return result

    def build_map_dictFollowed(self, row):
        result = {}
        result['follower'] = row[0]
        return result

    def build_map_dictFollowing(self, row):
        result = {}
        result['follows'] = row[0]
        return result

    def addNewFollow(self, json, followingid):
        followerid = json['RegisteredUser']
        daoBlock = BlockDAO()
        checkBlock = daoBlock.checkBlocked(followerid, followingid)
        if checkBlock:
            return jsonify("User is blocked"), 200
        dao = FollowDAO()
        checkFollow = dao.checkFollow(followerid, followingid)

        if checkFollow:
            return jsonify("User already Followed"), 200

        fid = dao.insertFollow(followerid, followingid)
        result = self.build_attr_dict(followerid, followingid)
        return jsonify(result), 201

    def deleteFollow(self, json, followerid):
        followingid = json['RegisteredUser']
        if followerid == followingid:
            return jsonify("ERROR, same userid"), 404
        dao = FollowDAO()
        result = dao.deleteFollow(followingid, followerid)
        if result:
            return jsonify("UNFOLLOWED"), 200
        else:
            return jsonify("NOT FOUND"), 404

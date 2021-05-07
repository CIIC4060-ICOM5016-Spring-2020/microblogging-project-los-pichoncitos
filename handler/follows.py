from flask import jsonify, json
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
        # result['fid'] = fid
        result['followingid'] = followingid
        result['RegisteredUser'] = followerid
        return result

    def build_map_dictFollowed(self, row):
        result = {}
        # result['fid'] = row[0]
        # result['uid'] = row[0]
        result['followedBy'] = row[0]
        return result

    def build_map_dictFollowing(self, row):
        result = {}
        # result['fid'] = row[0]
        # result['rid'] = row[0]
        result['follows'] = row[0]
        return result

    def addNewFollow(self, json, followingid):
        # fid = json['fid']
        followerid = json['registeredUser']
        dao = FollowDAO()
        fid = dao.insertFollow(followerid, followingid)
        result = self.build_attr_dict(followerid, followingid)
        return jsonify(result), 201

    def deleteFollow(self, json, followerid):
        followingid = json['registeredUser']
        if followerid == followingid:
            return jsonify("ERROR, same userid"), 404
        dao = FollowDAO()
        result = dao.deleteFollow(followerid, followingid)
        if result:
            return jsonify("UNFOLLOWED"), 200
        else:
            return jsonify("NOT FOUND"), 404
from flask import Flask, request, jsonify
#from flask_cors import CORS

from handler.reply import BaseReply
from handler.shares import BaseShare
from handler.users import BaseUser
from handler.messages import BaseMessage
from handler.follows import BaseFollow
from handler.reacts import BaseReact
from handler.blocks import BaseBlock


app = Flask(__name__)
#cors = CORS(app)

@app.route('/Pichon',methods=['GET'])
def getApp():
    if request.method == 'GET':
        return "Hello"
    else:
        return jsonify("Method not Allowed"), 405


#USER

#Register
@app.route('/Pichon/users', methods=['GET', 'POST'])
def handle_getUser():
    if request.method == 'POST':
        return BaseUser().addNewUser(request.json)
    elif request.method == 'GET':
        return BaseUser().getAllUsers()
    else:
        return jsonify("Method not Allowed"),405


#Get by id
@app.route('/Pichon/users/<int:uid>', methods=['GET','PUT','DELETE'])
def handle_getUserbyId(uid):
    if request.method == 'GET':
        return BaseUser().getUserbyId(uid)
    elif  request.method == 'PUT':
        return BaseUser().updateUser(request.json)
    elif request.method == 'DELETE':
        return BaseUser().deleteUser(uid)
    else:
        return jsonify("Method not Allowed"),405

#FOLLOW

#Follow a user
@app.route('/Pichon/follow/<int:rid>', methods=['POST'])
def handle_getFollow(rid):
    if request.method == 'POST':
        return BaseFollow().addNewFollow(request.json, rid)
    else:
        return jsonify("Method not Allowed"),405

#Get users followed by a specific user
@app.route('/Pichon/followedBy/<int:rid>', methods=['GET'])
def handle_getFollowedBy(rid):
    if request.method == 'GET':
        return BaseFollow().getFollowedBy(rid)
    else:
        return jsonify("Method not Allowed"),405

#Get users following a specific user
@app.route('/Pichon/follows/<int:uid>', methods=['GET'])
def handle_getFollows(uid):
    if request.method == 'GET':
        return BaseFollow().getFollowing(uid)
    else:
        return jsonify("Method not Allowed"),405

#UNFOLLOW
@app.route('/Pichon/unfollow/<int:uid>', methods=['POST'])
def handle_getUnfollow(uid):
    if request.method == 'POST':
        return BaseFollow().deleteFollow(request.json, uid)
    else:
        return jsonify("Method not Allowed"),405

#BLOCK

#User blocks another user
@app.route('/Pichon/block/<int:uid>', methods=['POST'])
def handle_getBlock(uid):
    if request.method == 'POST':
        return BaseBlock().addNewBlock(request.json, uid)
    else:
        return jsonify("Method not Allowed"),405

#Get all users ublocked by a registered user
@app.route('/Pichon/blockedBy/<int:uid>', methods=['GET'])
def handle_getBlockedBy(uid):
    if request.method == 'GET':
        return BaseBlock().getBlockedBy(uid)
    else:
        return jsonify("Method not Allowed"),405

#Get all users blocking a registered user
@app.route('/Pichon/blocking/<int:uid>', methods=['GET'])
def handle_getBlocking(uid):
    if request.method == 'GET':
        return BaseBlock().getBlocking(uid)
    else:
        return jsonify("Method not Allowed"),405

#UNBLOCK
@app.route('/Pichon/unblock/<int:uid>', methods=['POST'])
def handle_getUnblock(uid):
    if request.method == 'POST':
        return BaseBlock().deleteBlock(request.json, uid)
    else:
        return jsonify("Method not Allowed"),405

#MESSAGES

#Post message
@app.route('/Pichon/posts', methods=['POST'])
def handle_getMessage():
    if request.method == 'POST':
        return BaseMessage().addNewMessage(request.json)
    else:
        return jsonify("Method not Allowed"),405

#Reply message
@app.route('/Pichon/reply', methods=['POST','GET'])
def handle_replyMessage():
    if request.method == 'POST':
        return BaseReply().addNewReply(request.json)
    elif request.method == 'GET':
        return BaseReply().getAllReply()
    else:
        return jsonify("Method not Allowed"),405

#Share message
@app.route('/Pichon/share', methods=['POST','GET'])
def handle_shareMessage():
    if request.method == 'POST':
        return BaseShare().addNewShare(request.json)
    elif request.method == 'GET':
        return BaseShare().getAllShares()
    else:
        return jsonify("Method not Allowed"),405

#Get message by id
@app.route('/Pichon/msg/<int:mid>', methods=['GET','PUT','DELETE'])
def handle_getMessagebyId(mid):
    if request.method == 'GET':
        return BaseMessage().getMessagebyId(mid)
    else:
        return jsonify("Method not Allowed"),405

#Get all messages
@app.route('/Pichon/msg', methods=['GET'])
def handle_getAllMessages():
    if request.method == 'GET':
        return BaseMessage().getAllMessages()
    else:
        return jsonify("Method not Allowed"),405

#LIKE

#User likes a post
@app.route('/Pichon/like/<int:mid>', methods=['POST'])
def handle_like(mid):
    if request.method == 'POST':
        return BaseReact().insertLike(request.json, mid)
    else:
        return jsonify("Method not Allowed"),405

#Remove like from a message
@app.route('/Pichon/like/remove/<int:mid>', methods=['DELETE'])
def handle_removeLike(mid):
    if request.method == 'DELETE':
        return BaseReact().deleteLike(request.json, mid)
    else:
        return jsonify("Method not Allowed"),405

#Get all user that liked a message
@app.route('/Pichon/liked/<int:mid>', methods=['GET'])
def handle_getLikes(mid):
    if request.method == 'GET':
        return BaseReact().getLikesById(mid)
    else:
        return jsonify("Method not Allowed"),405

#UNLIKE

#User unlikes a message
@app.route('/Pichon/unlike/<int:mid>', methods=['POST'])
def handle_unlike(mid):
    if request.method == 'POST':
        return BaseReact().insertUnlike(request.json, mid)
    else:
        return jsonify("Method not Allowed"),405

#Remove unlike from a message
@app.route('/Pichon/unlike/remove/<int:mid>', methods=['DELETE'])
def handle_removeUnlike(mid):
    if request.method == 'DELETE':
        return BaseReact().deleteUnlike(request.json, mid)
    else:
        return jsonify("Method not Allowed"),405

#Get all unlikes (dislikes) on a message
@app.route('/Pichon/unliked/<int:mid>', methods=['GET'])
def handle_getUnlikes(mid):
    if request.method == 'GET':
        return BaseReact().getUnlikesById(mid)
    else:
        return jsonify("Method not Allowed"),405


if __name__ == '__main__':
    app.run(debug=True)
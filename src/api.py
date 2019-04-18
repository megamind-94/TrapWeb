from flask import jsonify
from flask import Blueprint, Flask, request
from config import *
from db import *
from utils import *

# api = Blueprint("api", __name__)
api = Flask(__name__, static_folder='data')
_db = DB(username=username, passwd=passwd, database=dbbase)


@api.route("/search/<s>", methods=["GET"])
def get_search(s):
    _status, _content, _msg = getSearch(_db, s)
    content = []
    for _ in _content:
        content.append(
            {
                "ctid": _["id"],
                "title": _["title"],
                "lid": _["lid"]
            }
        )
    result_dict = {
        "status": _status,
        "content": content,
        "msg": _msg
    }
    return jsonify(result_dict)


@api.route("/recommend/<city>/<lid>", methods=["GET"])
def get_recommend(city, lid):
    _status, _content, _msg = getRecommend(_db, city, lid)
    content = []
    for _ in _content:
        content.append({
            "ctid": _["ctid"],
            "coverid": hostname + _["coverid"],
            # "coverid": hostname + 'test.png',
            "tagname": _["tagname"],
            "lid": _["lid"],
            "tid": _["tid"]
        })
    result_dict = {
        "status": _status,
        "content": content,
        "msg": _msg
    }
    return jsonify(result_dict)


@api.route("/getimage/<id>", methods=["GET"])
def get_image(id):
    sql = "SELECT * FROM images WHERE id={id};".format(id=id)
    rows = _db.excute(sql)
    if len(rows) == 0:
        status = -1
        content = []
        msg = "数据为空"
    else:
        status = 1
        content = []
        msg = ""
        for row in rows:
            _ = {
                "imgid": row[0],
                "stored": row[1],
                "ctid": row[2]
            }
            content.append(_)

    result_dict = {
        "status": status,
        "content": content,
        "msg": msg
    }

    return jsonify(result_dict)


@api.route("/contents", methods=["POST"])
def get_content():
    data = request.get_json()
    uid = data['uid']
    _status, _content, _msg = getContent(_db, _cond=["id={ctid}".format(ctid=data['ctid'])])
    for _ in range(len(_content)):
        _content[_]['is_keep'] = isKeep(_db, uid, _content[_]['id'])

    result_dict = {
        "status": _status,
        "content": _content,
        "msg": _msg
    }
    return jsonify(result_dict)


@api.route("/user/<id>")
def get_user(id):
    _status, _msg, _content = getUserinfo(_db, id)

    result_dict = {
        "status": _status,
        "content": _content,
        "msg": _msg
    }

    return jsonify(result_dict)


@api.route("/keeps/<uid>")
def get_keeps(uid, p=0):
    _status, _msg, _content = getKeeps(_db, uid, p)

    result_dict = {
        "status": _status,
        "content": _content,
        "msg": _msg
    }

    return jsonify(result_dict)


@api.route("/history/<uid>")
def get_history(uid, p=0):
    _status, _msg, _content = getHistorys(_db, uid, p)
    result_dict = {
        "status": _status,
        "content": _content,
        "msg": _msg
    }
    return jsonify(result_dict)


@api.route("/comments/<ctid>")
def get_comments(ctid):
    _status, _content, _msg = getComment(_db, ctid)
    result_dict = {
        "status": _status,
        "content": _content,
        "msg": _msg
    }
    return jsonify(result_dict)


@api.route("/comments/add", methods=["POST"])
def add_comments():
    data = request.get_json()
    _status, _msg = addComment(_db, data['ctid'], data['uid'], data['text'])
    result_dict = {
        "status": _status,
        "msg": _msg
    }
    return jsonify(result_dict)


@api.route("/comments/resp", methods=["POST"])
def resp_comments():
    data = request.get_data()
    _status, _msg = resp_comments(_db, data['ctid'], data['uid'], data['text'], data['cmid'])
    result_dict = {
        "status": _status,
        "msg": _msg
    }
    return jsonify(result_dict)


@api.route("/historys/add", methods=["POST"])
def add_history():
    data = request.get_json()
    _status, _msg = addHistory(_db, data['uid'], data['ctid'])
    result_dict = {
        "status": _status,
        "msg": _msg
    }
    return jsonify(result_dict)


@api.route("/keeps/add", methods=["POST"])
def add_keeps():
    data = request.get_json()
    _status, _msg = addKeeps(_db, data['uid'], data['ctid'])
    result_dict = {
        "status": _status,
        "msg": _msg
    }
    return jsonify(result_dict)


@api.route("/keeps/del", methods=["POST"])
def del_keeps():
    data = request.get_json()
    _status, _msg = delKeeps(_db, data['uid'], data['ctid'])
    result_dict = {
        "status": _status,
        "msg": _msg
    }
    return jsonify(result_dict)


@api.route("/historys/del", methods=["POST"])
def del_historys():
    data = request.json
    _status, _msg = delHistorys(_db, data['uid'], data['ctid'])
    result_dict = {
        "status": _status,
        "msg": _msg
    }
    return jsonify(result_dict)
@api.route("/user/add", methods=["POST"])
def add_user():
    data = request.get_json()
    _status, msg = addUser(_db, data['openid'], data['name'], data['avatarurl'])
    return jsonify({
        "status": _status,
        "msg": msg
    })

@api.route("/more/<tid>")
def get_more(tid):
    _status, msg, content = getMore(_db, tid)
    return jsonify({
        "status": _status,
        "msg": msg,
        "content": content
    })

if __name__ == "__main__":
    # app = Flask(__name__)
    # app.register_blueprint(api)
    # app.run()
    api.run()

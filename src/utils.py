from datetime import datetime
import os
from config import *
import json

def print_msg(msg, flag="INFO"):
    today = datetime.strftime(datetime.now(), "%y-%m-%d")
    if not os.path.isdir(LOG_DIR) or not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    logfile = os.path.join(LOG_DIR, today+".log")
    msg = "[{time}][{flag}]:{msg}".format(time=datetime.strftime(datetime.now(), "%y-%m-%d %H:%M:%S"), flag=flag, msg=msg)
    print(msg)
    os.system("echo {msg} >> {logfile}".format(msg=msg, logfile=logfile))

def getSearch(_db, s, p=0):
    _cond = ["title like '%{s}%'".format(s=s)]
    status, msg, content = getContent(_db, _cond=_cond, offset=p)
    return status, msg, content

def getUserinfo(_db, id):
    content = {
        "uid": "",
        "name": ""
    }
    sql = "SELECT id, username FROM users WHERE openid='{id}';".format(id=id)
    row = _db.fetchone(sql)
    # import pdb;pdb.set_trace()
    if not row:
        status = -1
        msg = "数据为空"
    else:
        status = 1
        msg = ""
        content["uid"] = row[0]
        content["name"] = row[1]

    return status, msg, content

def getKeeps(_db, uid, p):
    size = 10
    p = int(p)
    # sql = "SELECT ctid FROM keeps WHERE uid=(SELECT id FROM users WHERE openid='{uid}') LIMIT {size} OFFSET {p};".format(uid=uid, size=size, p=p * size)
    sql = "SELECT ctid FROM keeps WHERE uid={uid} LIMIT {size} OFFSET {p};".format(uid=uid, size=size, p=p * size)
    rows = _db.fetchall(sql)
    # import pdb; pdb.set_trace()
    if not rows:
        status = -1
        content = {}
        msg = "数据为空"
    else:
        status = 1
        msg = ""
        content = {}
        content["num"] = len(rows)
        details = []
        result = getContent(_db, _cond=["id in ({ctids})".format(ctids=" , ".join([str(_[0]) for _ in rows]))])
        for row in result[1]:
            details.append({
                "ctid": row["id"],
                "title": row["title"],
                "lid": row["lid"]
            })
        content["details"] = details

    return status, msg, content

def getHistorys(_db, uid, p=0):
    size = 10
    p = int(p)
    sql = "SELECT ctid FROM historys WHERE uid={uid} LIMIT {size} OFFSET {p};".format(uid=uid, size=size, p=p * size)
    rows = _db.fetchall(sql)
    if not rows:
        status = -1
        content = {}
        msg = "数据为空"
    else:
        status = 1
        msg = ""
        content = {}
        content["num"] = len(rows)
        details = []
        result = getContent(_db, _cond=["id in ({ctids})".format(ctids=" , ".join([str(_[0]) for _ in rows]))])
        for row in result[1]:
            details.append({
                "ctid": row["id"],
                "title": row["title"],
                "lid": row["lid"]
            })
        content["details"] = details
    return status, msg, content

def getImage(_db, imgid):
    _sql = "SELECT stored FROM images WHERE id={imgid}".format(imgid=imgid)
    return _db.fetchone(table='images', col='stored', cond=['id={imgid}'.format(imgid=imgid)])

def getContent(_db, _sql=None, _cond=None, offset=0, limit=10):
    if _sql:
        rows = _db.excute(_sql)
    else:
        assert _cond, "Error: Not condition"
        _sql = "SELECT * FROM contents WHERE {_cond};".format(_cond=' and '.join(_cond))
        rows = _db.fetchall(_sql)
    if not rows:
        status = -1
        content = []
        msg = "数据为空"
    else:
        status = 1
        msg = ""
        content = []
        for row in rows:
            rows1 = _db.fetchall("SELECT * FROM items WHERE ctid={ctid}".format(ctid=row[0]))
            # import pdb; pdb.set_trace()
            jd = []
            ms = []
            if rows1:
                for row1 in rows1:
                    if row1[5] == 'jd':
                        jd.append(
                            {
                                'item_id': row1[0],
                                'image': hostname + row1[1],
                                'title': row1[2],
                                'price': row1[3],
                                'addr': row1[4],
                                'label': row1[5],
                                'ctid': row1[6]
                            }
                        )
                    else:
                        ms.append(
                            {
                                'item_id': row1[0],
                                'image': hostname + row1[1],
                                'title': row1[2],
                                'price': row1[3],
                                'addr': row1[4],
                                'label': row1[5],
                                'ctid': row1[6]
                            }
                        )

            sql2 = "SELECT * FROM keeps WHERE uid={uid}"

            content.append({
                "id": row[0],
                "coverid": hostname + row[1],
                "content": hostname + row[3],
                "addr": row[4],
                "coverid2": hostname + row[2],
                "title": row[5],
                "city": row[6],
                "tid": row[7],
                "lid": row[8],
                "time": row[10],
                "price": row[11],
                "jd": jd,
                'ms': ms
            })

    return status, content, msg

def getRecommend(_db, city, lid):
    sql = "SELECT c.id AS ctid, c.coverid AS coverid, t.name AS tagname, c.label_id AS lid, c.tag_id AS tid FROM contents c LEFT JOIN tags t ON c.tag_id=t.id WHERE c.is_recommend = 1 AND c.label_id={label_id} AND c.city='{city}';".format(
        label_id=lid, city=city)
    rows = _db.fetchall(sql)
    if not rows:
        status = -1
        content = []
        msg = "数据为空"
    else:
        status = 1
        msg = ""
        content = []
        # import pdb; pdb.set_trace()
        for row in rows:
            _ = {
                "ctid": row[0],
                "coverid": row[1],
                "tagname": row[2],
                "lid": row[3],
                "tid": row[4]
            }
            content.append(_)

    return status, content, msg

def getComment(_db, ctid, uid=None):
    sql = "SELECT c.id AS commend_id, c.uid AS uid, c.text AS text, u.username AS name, u.avatarurl AS face FROM comments c LEFT JOIN users u ON c.uid=u.id WHERE c.ctid={ctid};".format(ctid=ctid)
    rows = _db.fetchall(sql)
    # import pdb; pdb.set_trace()
    if not rows:
        status = -1
        content = []
        msg = "数据为空"
    else:
        status = 1
        msg = ""
        content = []
        for row in rows:
            _ = {
                "id": row[0],
                "uid": row[1],
                "text": row[2],
                "name": row[3],
                "face": row[4]
            }
            content.append(_)

    return status, content, msg

def addComment(_db, ctid, uid, text):
    sql = "INSERT INTO comments (uid, ctid, text, types) VALUES ({uid}, {ctid}, '{text}', 0);".format(uid=uid, ctid=ctid, text=text)
    result = _db.excute(sql)
    if result:
        status = 1
        msg = ""
    else:
        status = -1
        msg = "数据为空"

    return status, msg


def respComment(_db, ctid, uid, cmid, text):
    sql = "INSERT INTO comments (uid, ctid, text, cmid, status) VALUES ({uid}, {ctid}, {text}, {cmid}, 1);".format(uid=uid, ctid=ctid, text=text, cmid=cmid)
    result = _db.excute(sql)
    if result:
        status = 1
        msg = ""
    else:
        status = -1
        msg = "数据为空"

    return status, msg

def addHistory(_db, uid, ctid):
    status = -1
    msg = "添加浏览记录失败"
    # import pdb;pdb.set_trace()
    if uid != '':
        sql = "SELECT id FROM historys WHERE uid={uid} AND ctid={ctid};".format(uid=uid, ctid=ctid)
        result = _db.excute(sql)

        if not result:
            sql = "INSERT INTO historys (uid, ctid) VALUES ({uid}, {ctid});".format(uid=uid, ctid=ctid)
            result = _db.excute(sql)
            if result:
                status = 1
                msg = "添加浏览记录成功"

    return status, msg

def addKeeps(_db, uid, ctid):

    status = -1
    msg = "添加失败"

    sql1 = "SELECT * FROM keeps WHERE uid={uid} AND ctid={ctid}".format(uid=uid, ctid=ctid)
    # import pdb;pdb.set_trace()
    if not _db.excute(sql1):
        sql = "INSERT INTO keeps (uid, ctid) VALUES ({uid}, {ctid});".format(uid=uid, ctid=ctid)
        result = _db.excute(sql)
        # import pdb;pdb.set_trace()
        if result:
            status = 1
            msg = ""
    return status, msg


def delKeeps(_db, uid, ctid):
    sql = "DELETE FROM keeps WHERE uid={uid} and ctid={ctid};".format(uid=uid, ctid=ctid)
    result = _db.excute(sql)
    if result:
        status = 1
        msg = ""
    else:
        status = -1
        msg = "数据为空"

    return status, msg


def delHistory(_db, uid, ctid):
    sql = "DELETE FROM historys WHERE uid={uid} and ctid={ctid};".format(uid=uid, ctid=ctid)
    result = _db.excute(sql)
    if result:
        status = 1
        msg = ""
    else:
        status = -1
        msg = "数据为空"
    return status, msg

def addUser(_db, openid, name, avatarurl):
    sql = "INSERT INTO users (openid, username, avatarurl) VALUES ('{openid}', '{name}', '{avatarurl}')".format(openid=openid, name=name, avatarurl=avatarurl)
    print(sql)
    result = _db.excute(sql)
    if not result:
        status = -1
        msg = "添加失败"
    else:
        status = 1
        msg = ""
    return status, msg

def addData(_db):
    res = getImagesPath('data')
    for _ in res:
        coverid = _[0]
        coverid2 = _[0]
        content = _[1]
        info = _[2]
        sql = "INSERT INTO contents (coverid, coverid2, content, addr, title, city, tag_id, label_id, is_recommend) VALUE " \
              "({coverid}, {coverid2}, {content}, {addr}, {title}, {city}, {tag_id}, {label_id}, 0)".format(
                coverid=coverid, coverid2=coverid2, content=content, addr=info.get('addr', ''),
                title=info.get('title', ''), tag_id=info.get('tag_id'), label_id=info.get('label_id', '')
        )
        print(sql)
        result = _db.excute(sql)
        if result:
            print('添加成功')
        else:
            print('添加失败')



def getImagesPath(dirname):
    result = []
    dirlist = os.listdir(dirname)
    info = {}
    if 'content.png' in dirlist or 'cover.png' in dirlist:
        if 'info.json' in dirlist:
            info = json.load(open(dirname+'/'+'info.json', 'r'))
        return dirname+'/'+'content.png', dirname+'/'+'cover.png', info
    for _ in dirlist:
        result.extend(getImagesPath(dirname+'/'+_))
    return result

def getMore(_db, tid):
    sql = "SELECT * FROM contents WHERE tag_id={tid}".format(tid=tid)
    rows = _db.fetchall(sql)
    content = []
    if not rows:
        status = -1
        msg = "数据为空"
    else:
        for row in rows:
            _ = {
                "lid": row[8],
                "title": row[5],
                "ctid": row[0],
                "coverid": hostname + row[1]
            }
            content.append(_)
        status = 1
        msg = ""
    return status, msg, content

def isKeep(_db, uid, ctid):
    sql = "SELECT * FROM keeps WHERE uid={uid} AND ctid={ctid};".format(uid=uid, ctid=ctid)
    result = _db.excute(sql)
    if result:
        return True
    else:
        return False

if __name__ == '__main__':
    result = getImagesPath('data')
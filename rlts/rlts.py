import os
import sqlite3
import iteminsert
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash

# app create
app = Flask(__name__)

# update config
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, "rlts.db"),
    DEBUG=True,
    SECRET_KEY="WhyAreYouReadingThis?",
    USERNAME="admin",
    PASSWORD="default"
))
app.config.from_envvar("RLTS_SETTINGS", silent=True)


def connect_db():
    rv = sqlite3.connect(app.config["DATABASE"])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    if not hasattr(g, "sqlite_db"):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, "sqlite_db"):
        g.sqlite_db.close()


def init_db():
    db = get_db()
    with app.open_resource("schema.sql", mode="r") as f:
        db.cursor().executescript(f.read())
    db.commit()
    iteminsert.main(db)


@app.cli.command("initdb")
def initdb_command():
    init_db()
    print "Database initialized"


# routes
@app.route('/', methods=["GET", "POST"])
def index():
    error = None
    db = get_db()
    if not session.get("logged_in"):
        # show login page in root directory if user is not logged in
        # Handle post request on login
        if request.method == "POST":
            cur = db.execute('select username, password from Player;')
            entries = cur.fetchall()
            # return list of tuples that contain username (should be 1)
            exists = [item for item in entries if item[0] == request.form["username"]]
            if len(exists) == 0:
                error = "User does not exist."
            else:
                userinfo = exists.pop()
                if request.form['password'] != userinfo[1]:
                    error = "Invalid password."
            if error is None:
                session["logged_in"] = True
                session["username"] = request.form["username"]
                return redirect(url_for("index"))
        # render login form
        return render_template("login.html", error=error)
    else:
        query = "select W.wID WID, I.name INAME, I.type ITYPE, I.quality IQUALITY, I.collection ICOLLECTION, I.painted IPAINTED, I.certified ICERTIFIED "
        query += "from Player P, Item I, Wants W "
        query += "where P.username = '" + session["username"] + "' AND "
        query += "P.uID = W.userID AND I.iID = W.itemID;"
        cur = db.execute(query)
        wantEntries = cur.fetchall()
        query = "select H.hID HID, I.name INAME, I.type ITYPE, I.quality IQUALITY, I.collection ICOLLECTION, I.painted IPAINTED, I.certified ICERTIFIED "
        query += "from Player P, Item I, Has H "
        query += "where P.username = '" + session["username"] + "' AND "
        query += "P.uID = H.userID AND I.iID = H.itemID;"
        cur = db.execute(query)
        hasEntries = cur.fetchall()
        return render_template("root.html", error=error, wantEntries=wantEntries, hasEntries=hasEntries)


@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    session.pop("username", None)
    return redirect(url_for("index"))


@app.route("/newuser", methods=["GET", "POST"])
def new_user():
    error = None
    if request.method == "POST":
        db = get_db()
        cur = db.execute('select username, password from Player;')
        entries = cur.fetchall()
        exists = [item for item in entries if item[0] == request.form["username"]]
        if len(request.form["username"]) < 1:
            error = "Username cannot be left blank."
        elif len(exists) == 0:
            if request.form["password"] != request.form["cpassword"]:
                error = "Passwords do not match."
            else:
                db.execute("insert into Player (username, password, platform) values (?, ?, ?)",
                    [request.form["username"], request.form["password"], request.form["platform"]])
                db.commit()
        else:
            error = "A user already exists with the specified username."
        # successful account creation
        if error is None:
            return redirect(url_for("index"))
    return render_template("newuser.html", error=error)


@app.route("/search", methods=["POST"])
def search():
    error = None
    db = get_db()
    # set up query
    query = []  # list containing components of query
    itemname = request.form["itemname"]
    if len(itemname) > 0:
        query.append("name = '" + itemname + "'")
    itemtype = request.form["type"]
    if itemtype != "Any":
        query.append("type = '" + itemtype + "'")
    quality = request.form["quality"]
    if quality != "Any":
        query.append("quality = '" + quality + "'")
    collection = request.form["collection"]
    if collection != "Any":
        if collection == "None":
            query.append("collection is null")
        else:
            query.append("collection = '" + collection + "'")
    painted = request.form["painted"]
    if painted != "Any":
        if painted == "None":
            query.append("painted is null")
        else:
            query.append("painted = '" + painted + "'")
    certified = request.form["certified"]
    if certified != "Any":
        if certified == "None":
            query.append("certified is null")
        else:
            query.append("certified = '" + certified + "'")
    # Create string to be used in sql statement
    if len(query) > 0:
        whereStr = " AND ".join(query)
        queryStr = "select * from Item where " + whereStr
        print queryStr
    else:
        error = "Please refine your search."
        return render_template("root.html", error=error)

    cur = db.execute(queryStr)
    entries = cur.fetchall()
    return render_template('results.html', entries=entries)


@app.route('/want/<itemID>')
def item_want(itemID):
    db = get_db()
    print itemID
    query = "select uID from Player where username = '" + session["username"] + "'"
    cur = db.execute(query)
    entries = cur.fetchall()
    uID = int(entries[0][0])
    db.execute("insert into Wants (userID, itemID) values (?, ?)",
               [uID, itemID])
    db.commit()
    return redirect(url_for("index"))


@app.route('/have/<itemID>')
def item_have(itemID):
    db = get_db()
    print itemID
    query = "select uID from Player where username = '" + session["username"] + "'"
    cur = db.execute(query)
    entries = cur.fetchall()
    uID = int(entries[0][0])
    db.execute("insert into Has (userID, itemID) values (?, ?)",
               [uID, itemID])
    db.commit()
    return redirect(url_for("index"))


@app.route('/w_remove/<wantID>')
def remove_want(wantID):
    db = get_db()
    print wantID
    query = "delete from Wants where wID = " + str(wantID)
    db.execute(query)
    db.commit()
    return redirect(url_for("index"))


@app.route('/h_remove/<hasID>')
def remove_has(hasID):
    db = get_db()
    print hasID
    query = "delete from Has where hID = " + str(hasID)
    db.execute(query)
    db.commit()
    return redirect(url_for("index"))


@app.route('/find')
def find():
    # get user id
    db = get_db()
    query = "select uID from Player where username = '" + session["username"] + "'"
    cur = db.execute(query)
    entries = cur.fetchall()
    uID = int(entries[0][0])

    # Advanced function
    query = "select Pl.username uName, CNT.uID usID "
    query += "from (select TR uID "
    query += "from (select T.TRADER TR from ("
    query += "select T1.USER1 SELF, T1.USER2 TRADER from ("
    query += "select W.userID USER1, H.userID USER2 "
    query += "from Wants W, Has H "
    query += "where W.itemID = H.itemID) T1, ("
    query += "select H.userID USER1, W.userID USER2 "
    query += "from Has H, Wants W "
    query += "where H.itemID = W.itemID) T2 "
    query += "where T1.USER1 = T2.USER1 AND T1.USER2 = T2.USER2) T "
    query += "where T.SELF = " + str(uID) + ") "
    query += "GROUP BY TR "
    query += "ORDER BY COUNT(*) DESC) CNT, Player Pl "
    query += "where Pl.uID = CNT.uID"
    cur = db.execute(query)
    entries = cur.fetchall()
    print entries
    return render_template("playerlist.html", entries=entries)

@app.route("/view/<userID>")
def view_profile(userID):
    db = get_db()
    query = "select username from Player where uID = " + str(userID)
    cur = db.execute(query)
    entries = cur.fetchall()
    uName = str(entries[0][0])
    query = "select W.wID WID, I.name INAME, I.type ITYPE, I.quality IQUALITY, I.collection ICOLLECTION, I.painted IPAINTED, I.certified ICERTIFIED "
    query += "from Player P, Item I, Wants W "
    query += "where P.username = '" + uName + "' AND "
    query += "P.uID = W.userID AND I.iID = W.itemID;"
    cur = db.execute(query)
    wantEntries = cur.fetchall()
    query = "select H.hID HID, I.name INAME, I.type ITYPE, I.quality IQUALITY, I.collection ICOLLECTION, I.painted IPAINTED, I.certified ICERTIFIED "
    query += "from Player P, Item I, Has H "
    query += "where P.username = '" + uName + "' AND "
    query += "P.uID = H.userID AND I.iID = H.itemID;"
    cur = db.execute(query)
    hasEntries = cur.fetchall()
    return render_template("profileview.html", uName=uName, wantEntries=wantEntries, hasEntries=hasEntries)
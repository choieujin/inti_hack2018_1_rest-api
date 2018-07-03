#-*- coding: utf-8 -*-
from flask import Flask
from flask import render_template, request
from flask_restful import reqparse
import pymysql
import json
import sys
import datetime
import os
import uuid
from flask import Flask, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from werkzeug import SharedDataMiddleware

reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)
conn = pymysql.connect(
        host='localhost',
        user='root',
        password='intI2017!@',
        db='movie',
        charset='utf8')
cursor = conn.cursor()

@app.route('/')
def hello():
    return 'Hello World'

@app.route('/movie')
def fun():
    var = ""
    cursor.execute("select * from movie")
    for line in cursor.fetchall():
        var += line[1]
        var += line[2]
        var += str(line[3])
        var += line[4]
        var += "<br>"
    conn.close()
    jsonstr = json.dumps(var, ensure_ascii=False).encode('utf8')
    print type(jsonstr)
    return jsonstr

@app.route('/create',methods=['POST'])
def create(charset='utf-8'):
    try:
        file = request.files['file']
        print(file)
        filename = secure_filename(file.filename)
        file.save("./static/"+filename)
        print(filename)
        info = request.form['info']
        print(info)
        data = json.loads(info)
        title = data['title']
        showtime = data['showtime']
        content = data['content']
        dt=datetime.datetime.now()
        upload_time = dt.strftime("%Y-%m-%d %H:%M:%S")
        path = "./static/"
        status = {"status" : "success" }

        cursor.execute("INSERT INTO movie (title,showtime,path,content,upload_time) VALUES(%s,%s,%s,%s,%s)",(title,showtime,path,content,upload_time))
        conn.commit()
    except BaseException:
        status = {"status" : "fail" }
    jsonstr = json.dumps(status)
    return jsonstr

@app.route('/delete',methods=['DELETE'])
def delete(charset='utf-8'):
    try:
        title=request.form['info']
        print(title)
        info = json.loads(title)
        title = info['title']
        status = {"status" : "success" }
        cursor.execute("SELECT * FROM movie")
        cursor.execute("DELETE FROM movie WHERE title=%s",(title))
        conn.commit()
    except BaseException:
        status = {"status" : "fail" }
    jsonstr = json.dumps(status)
    return jsonstr

@app.route('/update',methods=['PUT'])
def update(charset='utf-8'):
    try:
        file = request.files['file']
        print(file)
        filename = secure_filename(file.filename)
        file.save("./static/"+filename)
        print(filename)

        info = request.form['info']
        print(info)
        data = json.loads(info)
        title = data['title']
        showtime = data['showtime']
        content = data['content']
        dt=datetime.datetime.now()
        upload_time = dt.strftime("%Y-%m-%d %H:%M:%S")
        path = "./static/"
        status = {"status" : "success" }
        cursor.execute("SELECT * FROM movie")
        cursor.execute("UPDATE movie SET showtime=%s,path=%s,content=%s,upload_time=%s WHERE title = %s",(showtime,path,content,upload_time,title))
        conn.commit()
    except BaseException:
        status = {"status" : "fail" }
    jsonstr = json.dumps(status)
    return jsonstr

@app.route('/read',methods=['GET'])
def read(charset='utf-8'):
    movies = []
    cursor.execute("select * from movie")
    for data in cursor.fetchall():
        movies.append({'id' : data[0],'title' : data[1],'path' : data[2],'showtime' : data[3],'content' : data[4],'upload_time' : str(data[5])})
    conn.close()
    diction={}
    index = 0
    status = "success"
    for data in movies:
        dict = {}
        dict["id"] = data["id"]
        dict["title"] = data["title"]
        dict["path"] = data["path"]
        dict["showtime"] = data["showtime"]
        dict["content"] = data["content"]
        dict["upload_time"] = data["upload_time"]
        dict["status"] = status
        diction[index]=dict
        index+=1
    jsonstr = json.dumps(diction, ensure_ascii=False).encode('utf8')
    return jsonstr



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4109, debug=True)

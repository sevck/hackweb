#!/usr/bin/env python
# coding:utf-8
# @Date    : 2017/4/17 10:45
# @File    : main.py
# @Author  : sevck (sevck@jdsec.cn)
# @Link    : http://www.javsec.cn
# -------------------------------------------------------------------------
from flask import Flask, render_template, request
import re
import gaodeip
from password import PasswdGenerator
import cms
import whois
import skg
import ConfigParser
import MySQLdb
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

config = ConfigParser.RawConfigParser()
config.read("./config/config.conf")
MYSQL_HOST = config.get("mysql", "host")
MYSQL_USERNAME = config.get("mysql", "username")
MYSQL_PASSWORD = config.get("mysql", "password")
MYSQL_PORT = config.get("mysql", "port")
MYSQL_DB = config.get("mysql", "databases")
MYSQL_TABLES = config.get("mysql", "tables")

app = Flask(__name__)


# 连接数据库操作
def conn():
    db = MySQLdb.connect(MYSQL_HOST, MYSQL_USERNAME,
                         MYSQL_PASSWORD, MYSQL_DB,
                         int(MYSQL_PORT), charset='utf8')
    db.ping(True)
    cursor = db.cursor()
    return cursor


@app.route('/', methods=["get", "post"])
def index():
    return render_template('wooyun.html')


# IP地址定位
@app.route('/ip', methods=["get", "post"])
def BaiduIp():
    if request.method == 'POST':
        ip = request.form.get("search")
        addr = ip.strip().split('.')  # 切割IP地址为一个列表
        data = {}
        if len(addr) != 4:
            data['error'] ="IP 错误!"
            return render_template('ip.html', data=data, title="高精度IP查询")
        else:
            data = gaodeip.search(ip)
            if data.has_key('error'):
                data['error'] = "查询失败,请尝试再次查询"
                return render_template('ip.html', data=data, title="高精度IP查询")
            else:
                return render_template('ip.html', data=data, title="高精度IP查询")

    else:
        return render_template('ip.html', title="高精度IP查询")


# CMS在线识别
@app.route('/webdna', methods=["get", "post"])
def webdna():
    if request.method == 'POST':
        url = request.form.get("search")
        if re.match(r'^https?:/{2}\w.+$', url):
            data = cms.cms(url)
            if data.has_key('error'):
                data['error'] = "没有找到合适的CMS"
        return render_template('cms.html', data=data, title="CMS识别")
    else:
        return render_template('cms.html', title="CMS识别")


# 在线密码生成
@app.route('/password', methods=["get", "post"])
def password_build():
    if request.method == 'POST':
        from flask import make_response
        birthday = request.form.get("birthday", "")
        fullname = request.form.get("fullname", "")
        nickname = request.form.get("nickname", "")
        englishname = request.form.get("englishname", "")
        partnername = request.form.get("partnername", "")
        phone = request.form.get("phone", "")
        qq = request.form.get("qq", "")
        company = request.form.get("company", "")
        domain = request.form.get("domain", "")
        oldpasswd = request.form.get("oldpasswd", "")
        keywords = request.form.get("keywords", "")
        keynumbers = request.form.get("keynumbers", "")
        pwgen = PasswdGenerator(fullname=fullname, nickname=nickname, englishname=englishname, partnername=partnername,
                                phone=phone, qq=qq, company=company, domain=domain, oldpasswd=oldpasswd,
                                keywords=keywords, keynumbers=keynumbers, birthday=birthday)
        wordlist = pwgen.generate()
        content = '\n'.join(wordlist)

        response = make_response(content)
        response.headers["Content-Disposition"] = "attachment; filename=pass.txt"
        return response
        # return render_template('password.html',data=wordlist,title="社工密码生成")
    else:
        return render_template('password.html', title="社工密码生成")


# Whois 在线查询
@app.route('/whois', methods=["get", "post"])
def whoisa():
    if request.method == 'POST':
        url = request.form.get("search")
        data = whois.whois(url).replace("\n", "</br>")
        return render_template('whois.html', data=data, title="Whois查询")
    else:
        return render_template('whois.html', title="Whois查询")


# 调用外部社工库进行查询
@app.route('/pass', methods=["get", "post"])
def findpass():
    if request.method == 'POST':
        info = request.form.get("search")
        data = skg.findpass(info)
        return render_template('skg.html', data=data, title="社工库查询")
    else:
        return render_template('skg.html', title="社工库查询")


# 集成wooyun漏洞平台
@app.route('/wooyun', methods=["get", "post"])
@app.route('/wooyun/<int:pages>', methods=["get", "post"])
def wooyun(pages=0):
    searchword = request.args.get('key', '').strip()
    log_id = request.args.get('id', '').strip()
    data = {}
    table = list()
    cursor = conn()
    if log_id:
        # 使用execute方法执行SQL语句
        cursor.execute(MySQLdb.escape_string("SELECT * from {MYSQL_TABLES} where gid={log_id}"
                                             .format(MYSQL_TABLES=MYSQL_TABLES,log_id=log_id)))
        # 使用 fetchone() 方法获取一条数据库。
        results = cursor.fetchone()
        data["id"] = results[0]
        data["text"] = results[2]
        data["title"] = results[1]
    if searchword:
        sql = 'SELECT gid,title from {MYSQL_TABLES} where title like "%{searchword}%"'\
            .format(MYSQL_TABLES=MYSQL_TABLES, searchword=searchword)
        cursor.execute(sql)
        results = cursor.fetchall()

        for rows in results:
            tdata = {"id": rows[0], "title": rows[1]}
            table.append(tdata)
    cursor.close()
    return render_template("wooyun.html", title="乌云漏洞查询", data=data, table=table)


# 集成wooyun漏洞平台 -被忽略的漏洞
@app.route('/wooyun1', methods=["get", "post"])
@app.route('/wooyun1/<int:pages>', methods=["get", "post"])
def wooyun1(pages=0):
    if pages is None:
        pages = 0
    if pages < 0:
        pages = 0
    sql = 'SELECT gid,title from %s where content like "%%%s%%" limit %d,%d' % MYSQL_TABLES, ("无影响厂商忽略", pages * 20, 20)
    cursor = conn()
    cursor.execute(sql)
    results = cursor.fetchall()
    table = list()
    for rows in results:
        tdata = {}
        tdata["id"] = rows[0]
        tdata["title"] = rows[1]
        table.append(tdata)
    cursor.close()
    return render_template("wooyun.html", title="乌云忽略漏洞查询", table=table, next=pages + 1, prev=pages - 1)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)

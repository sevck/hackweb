#!/usr/bin/env python
# coding:utf-8
# @Date    : 2017/4/17 10:45
# @File    : gaodeip.py
# @Author  : sevck (sevck@jdsec.cn)
# @Link    : http://www.javsec.cn
# -------------------------------------------------------------------------
import urllib2
import json

# api doc http://lbs.amap.com/api/webservice/guide/api/ipconfig/
key = '4e4e15d218b85d0b8dd35c0a0c7cedb5'
#IP为空默认本机IP
def search(ip=""):
    url = "http://restapi.amap.com/v3/ip?ip={IP}&output=json&key={KEY}".format(IP=ip, KEY=key)
    print url
    response = urllib2.urlopen(url)
    html = response.read()
    print html
    res = json.loads(html)
    data = {}
    if res['status'] == '1' and ip != "127.0.0.1":
        print res
        data['province'] = res['province'] or ""
        data['city'] = res['city'] or ""
        data['adcode'] = res['adcode'] or ""
        try:
            rectangle = res['rectangle'].split(";")
            data['rectangle_left'] = rectangle[0].split(",")[0]
            data['rectangle_down'] = rectangle[0].split(",")[1]
            data['rectangle_right'] = rectangle[1].split(",")[0]
            data['rectangle_top'] = rectangle[1].split(",")[1]
        except Exception, e:
            data['rectangle_left'] = ""
            data['rectangle_down'] = ""
            data['rectangle_right'] = ""
            data['rectangle_top'] = ""
        return data
    else:
        msg = {"error": "查询失败,请尝试再次查询"}
        print msg
        return msg

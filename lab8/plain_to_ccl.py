#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import time
import urllib2

url = "http://ws.clarin-pl.eu/nlprest2/base"

input_file = 'resources/potop.txt'
out_path = 'resources/'


def upload(filename):
    with open(filename, "r") as my_file:
        doc = my_file.read()
    return urllib2.urlopen(urllib2.Request(url + '/upload/', doc, {'Content-Type': 'binary/octet-stream'})).read();


def tool(lpmn, user):
    data = dict()
    data['lpmn'] = lpmn
    data['user'] = user

    doc = json.dumps(data)
    taskid = urllib2.urlopen(urllib2.Request(url + '/startTask/', doc, {'Content-Type': 'application/json'})).read();
    time.sleep(0.1)
    resp = urllib2.urlopen(urllib2.Request(url + '/getStatus/' + taskid))
    data = json.load(resp)
    while data["status"] == "QUEUE" or data["status"] == "PROCESSING":
        time.sleep(0.1)
        resp = urllib2.urlopen(urllib2.Request(url + '/getStatus/' + taskid))
        data = json.load(resp)
    if data["status"] == "ERROR":
        print("Error " + data["value"])
        return None
    return data["value"]


def main():
    start_time = time.time()

    model = '5nam'
    user = 'user@gmail.com'
    data = upload(input_file)

    processing_pipe = 'file({})|any2txt|wcrft2|liner2({{"model":"{}"}})'.format(data, model)

    data = tool(processing_pipe, user=user)
    if data:
        data = data[0]["fileID"]
        content = urllib2.urlopen(urllib2.Request(url + '/download' + data)).read()
        with open(out_path + os.path.basename(input_file) + '.ccl', "w") as outfile:
            outfile.write(content)

        print("Time: {}s".format(time.time() - start_time))


if __name__ == '__main__':
    main()

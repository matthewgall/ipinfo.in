#!/usr/bin/env python

import os
import sys
import json
from random import randint
from bottle import route, request, response, run, template, error, default_app, HTTPResponse
import pydenticon

def getIPAddress():
    if request.headers.get('Cf-Connecting-Ip') != None:
        ip = request.headers.get('Cf-Connecting-Ip')
    elif request.headers.get('X-Forwarded-For') != None:
        ip = request.headers.get('X-Forwarded-For')
    else:
        ip = request.get('REMOTE_ADDR')
    return ip

def getRequestHeaders():
    return request.headers.keys()

@error(404)
def error404(error):
    response.status = 404
    response.content_type = 'text/plain'
    return 'Nothing here, sorry'

@route('/version')
def getVersion():
    f = open(os.getenv('VERSION_PATH', '.git/refs/heads/master'), 'r')
    content = f.read()
    response.content_type = 'text/plain'
    return content

@route('/icon')
@route('/icon/<height:int>')
@route('/icon/<height:int>/<width:int>')
def getIcon(height=100,width=100):
    response.content_type = 'image/png'
    colors = []
    for _ in range(8):
        colors.append("rgb(" + str(randint(1,255)) + "," + str(randint(1,255)) + "," + str(randint(1,255)) + ")")
    generator = pydenticon.Generator(8,8,foreground=colors)
    identicon = generator.generate(getIPAddress(), height, width)
    return identicon

@route('/headers/json')
def headersJSON():
    headers = {}
    for key in getRequestHeaders():
        headers[key] = request.headers.get(key)

    response.content_type = 'application/json'
    return json.dumps(headers)

@route('/headers')
def headers():
    content = ""
    for key in getRequestHeaders():
        content = content + "<strong>" + key + "</strong>: " + str(request.headers.get(key)) + "</br>"

    response.content_type = 'text/html'
    return content

@route('/json')
def ipJSON():
    content = {
        'ip': getIPAddress()
    }
    response.content_type = 'application/json'
    return json.dumps(content)

@route('/')
def ip():
    response.content_type = 'text/plain'
    return getIPAddress()

if __name__ == '__main__':

    application = default_app()

    serverHost = os.getenv('SERVER_HOST', 'localhost')
    serverPort = os.getenv('PORT', '5000')

    # Now we're ready, so start the server
    try:
        application.run(host=serverHost, port=serverPort)
    finally:
        exit()

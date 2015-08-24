#!/usr/bin/env python

import os
import sys
import json
import socket
from random import randint
from bottle import route, request, response, run, template, error, default_app, HTTPResponse
from dicttoxml import dicttoxml
import pydenticon

def getIPAddress():
    if request.headers.get('Cf-Connecting-Ip') != None:
        ip = request.headers.get('Cf-Connecting-Ip')
    elif request.headers.get('X-Forwarded-For') != None:
        ip = request.headers.get('X-Forwarded-For')
    else:
        ip = request.get('REMOTE_ADDR')
    return ip

def getReverseHost():
    try:
        return socket.gethostbyaddr(getIPAddress())[0]
    except:
        return "Unable to resolve IP address to reverse hostname"
    
def getRequestHeaders():
    return request.headers.keys()

def addHeadersToAllRequests():
    response.set_header('X-Contact-The-Author', 'themaster@ipinfo.in')
    return True

def isJSONResponse():
    if request.headers.get('Accept') == "application/json" \
    or request.path.endswith('.json'):
        response.content_type = 'application/json'
        return True

def isXMLResponse():
    if request.headers.get('Accept') == "application/xml" \
    or request.path.endswith('.xml'):
        response.content_type = 'application/xml'
        return True

@error(404)
def error404(error):
    response.status = 404
    response.content_type = 'text/plain'
    return 'Nothing here, sorry'

@route('/version')
def getVersion():
    addHeadersToAllRequests()
    try:
        dirname, filename = os.path.split(os.path.abspath(__file__))
        f = open(os.getenv('VERSION_PATH', dirname + '/.git/refs/heads/master'), 'r')
        content = f.read()
        response.content_type = 'text/plain'
        return content
    except:
        return "Unable to open version file."

@route('/icon')
@route('/icon/<height:int>')
@route('/icon/<height:int>/<width:int>')
def getIcon(height=100,width=100):
    addHeadersToAllRequests()
    response.content_type = 'image/png'
    colors = []
    for _ in range(2):
        colors.append("rgb(" + str(randint(1,255)) + "," + str(randint(1,255)) + "," + str(randint(1,255)) + ")")
    generator = pydenticon.Generator(8,8,foreground=colors)
    identicon = generator.generate(getIPAddress(), height, width)
    return identicon

@route('/headers')
@route('/headers.json')
@route('/headers.xml')
def headers():
    addHeadersToAllRequests()
    content = {}
    for key in getRequestHeaders():
        content[key] = request.headers.get(key)
    if isJSONResponse():
        return json.dumps(content)
    if isXMLResponse():
        return dicttoxml(content)
    else:
        content = ""
        for key in getRequestHeaders():
            content = content + "<strong>" + key + "</strong>: " + str(request.headers.get(key)) + "</br>"
        response.content_type = 'text/html'
        return content

@route('/reverse')
@route('/reverse.json')
@route('/reverse.xml')
def reverse():
    addHeadersToAllRequests()
    content = {
        'reverse': getReverseHost()
    }
    if isJSONResponse():
        return json.dumps(content)
    elif isXMLResponse():
        return dicttoxml(content)
    else:
        response.content_type = 'text/plain'
        return getReverseHost()

@route('/')
@route('/ip')
@route('/ip.json')
@route('/ip.xml')
def ip():
    addHeadersToAllRequests()
    content = {
        'ip': getIPAddress()
    }
    if isJSONResponse():
        return json.dumps(content)
    elif isXMLResponse():
        return dicttoxml(content)
    else:
        response.content_type = 'text/plain'
        return getIPAddress()

if __name__ == '__main__':

    application = default_app()

    serverHost = os.getenv('SERVER_HOST', 'localhost')
    serverPort = os.getenv('SERVER_PORT', '5000')

    # Now we're ready, so start the server
    try:
        application.run(host=serverHost, port=serverPort)
    finally:
        exit()

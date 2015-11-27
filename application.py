#!/usr/bin/env python

import os
import json
import socket
import logging
from random import randint
from bottle import route, request, response, run, error, default_app
from logentries import LogentriesHandler
from dicttoxml import dicttoxml
import pydenticon

def getIPAddress():
    try:
        if request.headers.get('Cf-Connecting-Ip') == None and request.headers.get('X-Forwarded-For') == None:
            raise TypeError
        elif request.headers.get('Cf-Connecting-Ip') != None:
            return request.headers.get('Cf-Connecting-Ip')
        else:
            return request.headers.get('X-Forwarded-For')
    except TypeError:
        return request.get('REMOTE_ADDR')

def getReverseHost():
    try:
        return socket.gethostbyaddr(getIPAddress())[0]
    except:
        return "Unable to resolve IP address to reverse hostname"
    
def getRequestHeaders():
    return request.headers.keys()

def addHeadersToAllRequests():
    response.set_header('X-ContactTheAuthor', 'themaster@ipinfo.in')
    return True

def buildContentResponse(content):
    # First, we're going to add our headers as needed
    addHeadersToAllRequests()
    # And define a default dictionary
    content = {
        "results": ""
    }
    return content

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

@route('favicon.ico')
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
    colors.append("rgb(" + str(randint(1, 255)) + "," + str(randint(1, 255)) + "," + str(randint(1, 255)) + ")")
    generator = pydenticon.Generator(8,8,foreground=colors)
    identicon = generator.generate(getIPAddress(), height, width)
    return identicon

@route('/headers')
@route('/headers.json')
@route('/headers.xml')
def headers():
    content = {
        "results": {}
    }
    for key in getRequestHeaders():
        content["results"][key] = request.headers.get(key)
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
        "results": {
            'reverse': getReverseHost()
        }
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
        "results": {
            'ip': getIPAddress()
        }
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
    # Instantiate the logger
    log = logging.getLogger('log')
    console = logging.StreamHandler()
    log.setLevel(logging.INFO)
    log.addHandler(console)

    if os.getenv('LOGENTRIES_TOKEN') == '':
        log.addHandler(LogentriesHandler(os.getenv('LOGENTRIES_TOKEN', '')))

    # Now we're ready, so start the server
    try:
        log.info("Successfully started application server on " + socket.gethostname())
        application.run(host=serverHost, port=serverPort)
    except:
        log.info("Failed to start application server on " + socket.gethostname())
